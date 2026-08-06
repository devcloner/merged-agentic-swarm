"""
Agentic Swarm — Web UI Control Panel.

A Starlette control panel (JSON API + a minimal single-page HTML dashboard with
inline CSS/JS, no build step) for inspecting and probing the swarm:

  GET  /api/status          key pools (active/total + key_id list), fabric
                            routes, PROVIDER_REGISTRY backends, latest report
                            summary. Never exposes secret values.
  GET  /api/reports         list of reports/*.json (name, mtime).
  GET  /api/reports/{name}  JSON content of one report (404 when missing).
  GET  /api/profiles        swarm profiles from swarm_profiles.load_profiles().
  PUT  /api/profiles/{name} update one profile in swarm-profiles.json.
  GET  /api/models          litellm live aliases + role -> alias mapping.
  POST /api/latency-test    streaming TTFB/total latency probe against litellm.
  POST /api/run-plan        resolve a profile into a run plan WITHOUT executing.

The dashboard is served at GET /. It renders provider/proxy status, the latest
run report summary + timeline, reports, profiles, the model routing table, and
a latency-test form. All secrets are referenced by env-var NAME only — never
printed, logged, or returned.

Modeled on ``streaming_proxy.create_app``: a factory returning a Starlette app
plus a separate uvicorn entry point (``agentic-ui``).
"""

from __future__ import annotations

import json
import os
import re
import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

import httpx
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse
from starlette.routing import Route

from merged_agentic_swarm.providers.key_pool import default_key_pool
from merged_agentic_swarm.providers.multi_provider_fabric import MODEL_FABRIC_ROUTES
from merged_agentic_swarm.services import model_routing, swarm_profiles

# ── Paths & litellm endpoints ───────────────────────────────────────────────

_REPO_ROOT = Path(__file__).resolve().parents[2]
_REPORTS_DIR = _REPO_ROOT / "reports"

_LITELLM_BASE = "http://127.0.0.1:4000"
_LITELLM_MODELS_URL = f"{_LITELLM_BASE}/v1/models"
_LITELLM_CHAT_URL = f"{_LITELLM_BASE}/v1/chat/completions"

# The ramp agentic-cli applies when a profile's waves list is empty.
DEFAULT_RAMP = [4, 8, 16, 24, 40]

# Keys a profile update may carry (unknown keys are rejected with a 400).
PROFILE_KEYS = {"description", "waves", "default_tier", "model_alias", "gates", "worker_roles"}

_REPORT_NAME_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


# ── Helpers (all read-only; no secrets ever leave these functions) ─────────


def _key_pool_snapshot() -> dict:
    """Provider -> {active, total, key_ids} — key_id list only, never values."""
    summary = default_key_pool.get_summary()
    pools: dict = {}
    for provider, info in summary.items():
        pools[provider] = {
            "active": info.get("active_keys", 0),
            "total": info.get("total_keys", 0),
            "key_ids": [k.key_id for k in default_key_pool.keys_by_provider.get(provider, [])],
        }
    return pools


def _fabric_routes() -> dict:
    """MODEL_FABRIC_ROUTES as alias -> [{provider, model}] chains."""
    return {
        alias: [{"provider": route.get("provider"), "model": route.get("model")} for route in routes]
        for alias, routes in MODEL_FABRIC_ROUTES.items()
    }


def _registry_backends() -> dict:
    """PROVIDER_REGISTRY backends -> {base_url, auth_env NAME, status, primary}."""
    path = _REPO_ROOT / "docs" / "agentic" / "providers" / "PROVIDER_REGISTRY.json"
    try:
        with open(path, encoding="utf-8") as f:
            registry = json.load(f)
    except OSError, ValueError:
        return {}
    backends = registry.get("backends")
    if not isinstance(backends, dict):
        return {}
    out: dict = {}
    for name, backend in backends.items():
        if not isinstance(backend, dict):
            continue
        out[name] = {
            "base_url": backend.get("base_url"),
            "auth_env": backend.get("auth_env"),
            "status": backend.get("status"),
            "primary": bool(backend.get("primary", False)),
        }
    return out


def _latest_report() -> dict | None:
    """Newest reports/*.json parsed into a summary + timeline (or None)."""
    files = sorted(_REPORTS_DIR.glob("*.json"))
    if not files:
        return None
    path = files[-1]
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except OSError, ValueError:
        return None
    if not isinstance(data, dict):
        return None
    return {
        "name": path.stem,
        "mtime": path.stat().st_mtime,
        "generated_at_utc": data.get("generated_at_utc"),
        "prd_title": data.get("prd_title"),
        "total_tokens_used": data.get("total_tokens_used"),
        "success_markers": data.get("success_markers"),
        "chain_registry_entries": data.get("chain_registry_entries"),
        "knowledge_registry_entries": data.get("knowledge_registry_entries"),
        "waves": data.get("waves", {}),
        "gates": data.get("gates", {}),
        "timeline": data.get("timeline", []),
    }


def _report_list() -> list[dict]:
    """[{name, mtime}] for every reports/*.json, newest first."""
    entries: list[dict] = []
    for path in _REPORTS_DIR.glob("*.json"):
        try:
            mtime = path.stat().st_mtime
        except OSError:
            mtime = 0.0
        entries.append({"name": path.stem, "mtime": mtime})
    entries.sort(key=lambda entry: entry["mtime"], reverse=True)
    return entries


def _report_detail(name: str) -> dict | None:
    """Load one report by safe stem; None when missing or unreadable."""
    name = name.strip().removesuffix(".json")
    if not _REPORT_NAME_RE.fullmatch(name):
        return None
    path = _REPORTS_DIR / f"{name}.json"
    if not path.exists():
        return None
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except OSError, ValueError:
        return None


def _write_profiles(profiles: dict) -> None:
    """Persist profiles to disk atomically and invalidate the load cache."""
    path = swarm_profiles._PROFILES_PATH
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(profiles, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)
    swarm_profiles._profiles_cache = None


def _role_mapping() -> dict[str, str]:
    """Tier + registered-role -> litellm alias via model_routing resolution."""
    roles = ["deep", "main", "fast"]
    registered = set(model_routing.DEFAULT_TIER_BY_ROLE)
    registry = model_routing._load_registry()
    rr = registry.get("role_routing") if isinstance(registry, dict) else None
    if isinstance(rr, dict):
        rr_roles = rr.get("roles")
        if isinstance(rr_roles, dict):
            registered |= set(rr_roles)
    mapping: dict[str, str] = {}
    for role in roles + sorted(registered - set(roles)):
        mapping[role] = model_routing.resolve_litellm_model_for_role(role)
    return mapping


async def _fetch_litellm_aliases(client: httpx.AsyncClient) -> tuple[list[str], str | None]:
    """Live litellm /v1/models aliases; on failure (aliases=[], note)."""
    key = os.environ.get("LITELLM_PROXY_KEY")
    headers = {"Authorization": f"Bearer {key}"} if key else {}
    try:
        resp = await client.get(_LITELLM_MODELS_URL, headers=headers)
    except Exception as exc:
        return [], f"litellm unreachable: {exc}"
    if resp.status_code >= 300:
        return [], f"litellm /v1/models HTTP {resp.status_code}"
    try:
        payload = resp.json()
    except ValueError:
        return [], "litellm /v1/models returned a non-JSON body"
    items = payload.get("data")
    if not isinstance(items, list):
        return [], "litellm /v1/models response missing data list"
    return [m.get("id") for m in items if isinstance(m, dict) and m.get("id")], None


def _latency_error(model: str, exc: Exception) -> dict:
    """ok:false payload — short error, never the key."""
    return {
        "model": model,
        "ok": False,
        "ttft_ms": 0.0,
        "total_ms": 0.0,
        "status_code": None,
        "error": f"latency test failed: {str(exc)[:200]}",
    }


async def _run_latency_test(client: httpx.AsyncClient, model: str, max_tokens: int) -> dict:
    """Stream one chat/completions request; report TTFB and total wall time."""
    key = os.environ.get("LITELLM_PROXY_KEY")
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "Reply with a single word: ok"}],
        "max_tokens": max_tokens,
        "stream": True,
    }
    sent_at = time.monotonic()
    try:
        req = client.build_request("POST", _LITELLM_CHAT_URL, json=payload, headers=headers)
        resp = await client.send(req, stream=True)
    except Exception as exc:
        return _latency_error(model, exc)

    first_at: float | None = None
    ttft_ms = 0.0
    try:
        async for _chunk in resp.aiter_bytes():
            if first_at is None:
                first_at = time.monotonic()
                ttft_ms = (first_at - sent_at) * 1000.0
    except Exception as exc:
        return _latency_error(model, exc)
    finally:
        if not resp.is_closed:
            await resp.aclose()

    total_ms = (time.monotonic() - sent_at) * 1000.0
    return {
        "model": model,
        "ok": 200 <= resp.status_code < 300,
        "ttft_ms": round(ttft_ms, 1),
        "total_ms": round(total_ms, 1),
        "status_code": resp.status_code,
    }


# ── Route handlers ──────────────────────────────────────────────────────────


async def handle_dashboard(request: Request) -> HTMLResponse:
    return HTMLResponse(_DASHBOARD_HTML)


async def handle_status(request: Request) -> JSONResponse:
    return JSONResponse(
        {
            "key_pools": _key_pool_snapshot(),
            "fabric_routes": _fabric_routes(),
            "registry_backends": _registry_backends(),
            "latest_report": _latest_report(),
        }
    )


async def handle_reports_list(request: Request) -> JSONResponse:
    return JSONResponse({"reports": _report_list()})


async def handle_report_detail(request: Request) -> JSONResponse:
    detail = _report_detail(request.path_params["name"])
    if detail is None:
        return JSONResponse({"error": "report not found"}, status_code=404)
    return JSONResponse(detail)


async def handle_profiles(request: Request) -> JSONResponse:
    return JSONResponse(swarm_profiles.load_profiles())


async def handle_profile_update(request: Request) -> JSONResponse:
    name = request.path_params["name"]
    profiles = swarm_profiles.load_profiles()
    if name not in profiles:
        return JSONResponse({"error": f"unknown profile: {name}"}, status_code=404)
    try:
        body = await request.json()
    except ValueError:
        return JSONResponse({"error": "invalid JSON body"}, status_code=400)
    if not isinstance(body, dict):
        return JSONResponse({"error": "body must be a JSON object"}, status_code=400)
    unknown = set(body) - PROFILE_KEYS
    if unknown:
        return JSONResponse({"error": f"unknown keys: {sorted(unknown)}"}, status_code=400)
    profile = dict(profiles[name])
    profile.update(body)
    profiles[name] = profile
    _write_profiles(profiles)
    return JSONResponse({"ok": True, "profile": profile})


async def handle_models(request: Request) -> JSONResponse:
    client: httpx.AsyncClient = request.app.state.httpx_client
    aliases, error = await _fetch_litellm_aliases(client)
    return JSONResponse({"aliases": aliases, "error": error, "role_mapping": _role_mapping()})


async def handle_latency_test(request: Request) -> JSONResponse:
    try:
        body = await request.json()
    except ValueError:
        return JSONResponse({"error": "invalid JSON body"}, status_code=400)
    if not isinstance(body, dict):
        return JSONResponse({"error": "body must be a JSON object"}, status_code=400)
    model = body.get("model")
    if not isinstance(model, str) or not model.strip():
        return JSONResponse({"error": "model is required"}, status_code=400)
    try:
        max_tokens = int(body.get("max_tokens") or 256)
    except TypeError, ValueError:
        max_tokens = 256
    client: httpx.AsyncClient = request.app.state.httpx_client
    result = await _run_latency_test(client, model, max_tokens)
    return JSONResponse(result)


async def handle_run_plan(request: Request) -> JSONResponse:
    try:
        body = await request.json()
    except ValueError:
        return JSONResponse({"error": "invalid JSON body"}, status_code=400)
    if not isinstance(body, dict):
        return JSONResponse({"error": "body must be a JSON object"}, status_code=400)
    name = body.get("profile")
    if not isinstance(name, str) or not name:
        return JSONResponse({"error": "profile is required"}, status_code=400)
    try:
        profile = swarm_profiles.resolve_profile(name)
    except KeyError:
        return JSONResponse({"error": f"unknown profile: {name}"}, status_code=404)
    alias = swarm_profiles.resolve_model_alias_for_profile(name)
    waves = profile.get("waves", [])
    return JSONResponse(
        {
            "profile": name,
            "description": profile.get("description", ""),
            "default_tier": profile.get("default_tier", ""),
            "gates": bool(profile.get("gates", True)),
            "worker_roles": profile.get("worker_roles", []),
            "waves": waves,
            "ramp": waves if waves else DEFAULT_RAMP,
            "model_alias": alias,
        }
    )


# ── App factory ─────────────────────────────────────────────────────────────


def create_app(transport: httpx.AsyncBaseTransport | None = None) -> Starlette:
    """Create the control-panel Starlette app.

    A shared ``httpx.AsyncClient`` (optionally backed by ``transport`` for
    tests) lives on ``app.state.httpx_client`` and is closed on shutdown.
    """
    client = httpx.AsyncClient(
        transport=transport,
        timeout=httpx.Timeout(connect=5.0, read=120.0, write=30.0, pool=5.0),
    )

    @asynccontextmanager
    async def lifespan(app: Starlette) -> AsyncIterator[None]:
        try:
            yield
        finally:
            await client.aclose()

    app = Starlette(
        routes=[
            Route("/", handle_dashboard, methods=["GET"]),
            Route("/api/status", handle_status, methods=["GET"]),
            Route("/api/reports", handle_reports_list, methods=["GET"]),
            Route("/api/reports/{name}", handle_report_detail, methods=["GET"]),
            Route("/api/profiles", handle_profiles, methods=["GET"]),
            Route("/api/profiles/{name}", handle_profile_update, methods=["PUT"]),
            Route("/api/models", handle_models, methods=["GET"]),
            Route("/api/latency-test", handle_latency_test, methods=["POST"]),
            Route("/api/run-plan", handle_run_plan, methods=["POST"]),
        ],
        lifespan=lifespan,
    )
    app.state.httpx_client = client
    return app


def main() -> None:
    """Run the control panel on loopback only."""
    import uvicorn

    uvicorn.run(create_app(), host="127.0.0.1", port=8123)


# ── Dashboard (single page, inline CSS/JS, no build step) ───────────────────


_DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Agentic Swarm Control Panel</title>
<style>
  :root { --bg:#0f1115; --panel:#171a21; --line:#2a2f3a; --text:#d7dce3; --dim:#8b93a1; --acc:#4f8cff; --ok:#2ecc71; --bad:#e74c3c; }
  * { box-sizing: border-box; }
  body { margin:0; font:14px/1.5 system-ui, sans-serif; background:var(--bg); color:var(--text); }
  header { padding:16px 24px; border-bottom:1px solid var(--line); background:var(--panel); }
  header h1 { margin:0; font-size:18px; }
  header p { margin:4px 0 0; color:var(--dim); font-size:12px; }
  main { display:grid; grid-template-columns:repeat(auto-fit, minmax(430px,1fr)); gap:16px; padding:20px 24px; }
  section { background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:14px 16px; }
  section h2 { margin:0 0 10px; font-size:13px; text-transform:uppercase; letter-spacing:.06em; color:var(--acc); }
  section h3 { margin:16px 0 6px; font-size:12px; color:var(--dim); }
  table { width:100%; border-collapse:collapse; font-size:13px; }
  th,td { text-align:left; padding:5px 8px; border-bottom:1px solid var(--line); vertical-align:top; }
  th { color:var(--dim); font-weight:600; white-space:nowrap; }
  .ok { color:var(--ok); } .bad { color:var(--bad); } .dim { color:var(--dim); }
  .mono { font-family:ui-monospace, SFMono-Regular, Menlo, monospace; font-size:12px; }
  .row { display:flex; gap:8px; align-items:center; flex-wrap:wrap; }
  input,select,button { background:#0d0f13; border:1px solid var(--line); color:var(--text); border-radius:6px; padding:7px 10px; font:inherit; }
  button { background:var(--acc); color:#fff; cursor:pointer; border-color:var(--acc); }
  pre { background:#0d0f13; border:1px solid var(--line); border-radius:6px; padding:10px; overflow:auto; font-size:12px; max-height:320px; }
  a { color:var(--acc); cursor:pointer; }
</style>
</head>
<body>
<header>
  <h1>Agentic Swarm Control Panel</h1>
  <p>Provider pools, fabric routes, run reports, swarm profiles, and model routing. Secrets are never shown — auth is referenced by env-var name only.</p>
</header>
<main>
  <section id="status">
    <h2>System Status</h2>
    <h3>Latest Report</h3>
    <div id="latest-report"><p class="dim">Loading…</p></div>
    <h3>Key Pools</h3>
    <div id="key-pools"><p class="dim">Loading…</p></div>
    <h3>Fabric Routes</h3>
    <div id="fabric-routes"><p class="dim">Loading…</p></div>
    <h3>Registry Backends</h3>
    <div id="registry-backends"><p class="dim">Loading…</p></div>
  </section>

  <section>
    <h2>Run Timeline (latest report)</h2>
    <div id="timeline"><p class="dim">Loading…</p></div>
  </section>

  <section>
    <h2>Reports</h2>
    <div id="reports"><p class="dim">Loading…</p></div>
    <pre id="report-body">…click a report to view…</pre>
  </section>

  <section>
    <h2>Swarm Profiles</h2>
    <div id="profiles"><p class="dim">Loading…</p></div>
    <div class="row" style="margin-top:10px">
      <select id="plan-profile"></select>
      <button id="plan-btn">Resolve plan (no run)</button>
    </div>
    <pre id="run-plan-result">…</pre>
  </section>

  <section>
    <h2>Model Routing</h2>
    <h3>Litellm Live Aliases</h3>
    <div id="model-aliases"><p class="dim">Loading…</p></div>
    <h3>Role → Alias</h3>
    <div id="role-mapping"><p class="dim">Loading…</p></div>
  </section>

  <section>
    <h2>Latency Test</h2>
    <form id="latency-form" class="row">
      <input name="model" placeholder="model alias, e.g. gemini-batch" required style="min-width:220px">
      <input name="max_tokens" type="number" value="256" min="1" style="width:110px" title="reasoning-heavy aliases need >= 256">
      <button type="submit">Run probe</button>
    </form>
    <pre id="latency-result">…</pre>
  </section>
</main>
<script>
async function getJSON(url) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(url + " -> HTTP " + r.status);
  return r.json();
}
function esc(s) {
  return String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
}
function statusSpan(s) {
  const ok = s === "ok" || s === "available" || s === true || s === "completed" || s === "spawned";
  return '<span class="' + (ok ? "ok" : "bad") + '">' + esc(s) + "</span>";
}
function table(headers, rows) {
  return "<table><tr>" + headers.map(h => "<th>" + esc(h) + "</th>").join("") + "</tr>" + rows.join("") + "</table>";
}

function renderStatus(status) {
  const lr = status.latest_report;
  const rep = document.getElementById("latest-report");
  if (!lr) {
    rep.innerHTML = '<p class="dim">No run report generated yet.</p>';
  } else {
    const waves = Object.entries(lr.waves || {}).map(([w, d]) =>
      w + ": " + Object.entries(d.status_counts || {}).map(([k, v]) => k + "=" + v).join(", ") + " (" + d.tokens_used + " tok)"
    ).join("<br>");
    rep.innerHTML = table(
      ["field", "value"],
      [
        "<tr><th>report</th><td class='mono'>" + esc(lr.name) + "</td></tr>",
        "<tr><th>generated (UTC)</th><td>" + esc(lr.generated_at_utc) + "</td></tr>",
        "<tr><th>prd</th><td>" + esc(lr.prd_title || "-") + "</td></tr>",
        "<tr><th>tokens</th><td>" + esc(lr.total_tokens_used) + "</td></tr>",
        "<tr><th>markers</th><td>" + esc(lr.success_markers) + "</td></tr>",
        "<tr><th>chain entries</th><td>" + esc(lr.chain_registry_entries) + "</td></tr>",
        "<tr><th>knowledge entries</th><td>" + esc(lr.knowledge_registry_entries) + "</td></tr>",
        (waves ? "<tr><th>waves</th><td>" + waves + "</td></tr>" : "")
      ]
    );
  }

  const pools = document.getElementById("key-pools");
  const poolRows = Object.entries(status.key_pools || {}).map(([p, info]) =>
    "<tr><td class='mono'>" + esc(p) + "</td><td>" + esc(info.active) + "/" + esc(info.total) + " active</td><td class='mono'>" + (info.key_ids || []).map(esc).join(", ") + "</td></tr>"
  );
  pools.innerHTML = poolRows.length ? table(["provider", "active/total", "keys"], poolRows) : '<p class="dim">No key pools loaded.</p>';

  const fabric = document.getElementById("fabric-routes");
  const fRows = Object.entries(status.fabric_routes || {}).map(([alias, routes]) =>
    "<tr><td class='mono'>" + esc(alias) + "</td><td class='mono'>" + routes.map(r => esc(r.provider) + "/" + esc(r.model)).join("<br>") + "</td></tr>"
  );
  fabric.innerHTML = fRows.length ? table(["alias", "route chain (provider/model)"], fRows) : '<p class="dim">No fabric routes.</p>';

  const reg = document.getElementById("registry-backends");
  const rRows = Object.entries(status.registry_backends || {}).map(([name, b]) =>
    "<tr><td class='mono'>" + esc(name) + "</td><td class='mono'>" + esc(b.base_url) + "</td><td class='mono'>" + esc(b.auth_env) + "</td><td>" + statusSpan(b.status) + "</td></tr>"
  );
  reg.innerHTML = rRows.length ? table(["backend", "base_url", "auth env", "status"], rRows) : '<p class="dim">No registry backends.</p>';
}

function renderTimeline(status) {
  const lr = status.latest_report;
  const evts = (lr && lr.timeline) || [];
  const el = document.getElementById("timeline");
  if (!evts.length) { el.innerHTML = '<p class="dim">No timeline events.</p>'; return; }
  const rows = evts.slice(-40).reverse().map(e => {
    const ts = e.timestamp ? new Date(e.timestamp * 1000).toISOString().replace("T", " ").slice(0, 19) : "-";
    return "<tr><td class='mono'>" + esc(ts) + "</td><td>" + esc(e.kind) + "</td><td>" + esc(e.wave_id == null ? "-" : e.wave_id) + "</td><td class='mono'>" + esc(e.action) + "</td><td>" + statusSpan(e.status) + "</td><td class='mono'>" + esc(e.model || "-") + "</td><td>" + esc(e.tokens_used) + "</td></tr>";
  });
  el.innerHTML = table(["time (UTC)", "kind", "wave", "action", "status", "model", "tok"], rows);
}

function renderReports(reports) {
  const el = document.getElementById("reports");
  const list = (reports.reports || []);
  if (!list.length) { el.innerHTML = '<p class="dim">No reports yet.</p>'; return; }
  const rows = list.map(r =>
    "<tr><td class='mono'><a data-name='" + esc(r.name) + "'>" + esc(r.name) + "</a></td><td>" + esc(new Date(r.mtime * 1000).toISOString()) + "</td></tr>"
  );
  el.innerHTML = table(["report", "mtime"], rows);
  el.querySelectorAll("a").forEach(a => a.addEventListener("click", async () => {
    const pre = document.getElementById("report-body");
    pre.textContent = "Loading…";
    try {
      const data = await getJSON("/api/reports/" + encodeURIComponent(a.dataset.name));
      pre.textContent = JSON.stringify(data, null, 2);
    } catch (err) { pre.textContent = "error: " + err; }
  }));
}

function renderProfiles(profiles) {
  const el = document.getElementById("profiles");
  const rows = Object.entries(profiles || {}).map(([name, p]) =>
    "<tr><td class='mono'>" + esc(name) + "</td><td>" + esc(p.description) + "</td><td>" + esc((p.waves || []).join(", ")) + "</td><td>" + esc(p.default_tier) + "</td><td>" + esc((p.worker_roles || []).join(", ")) + "</td></tr>"
  );
  el.innerHTML = rows.length ? table(["name", "description", "waves", "tier", "roles"], rows) : '<p class="dim">No profiles.</p>';
  const sel = document.getElementById("plan-profile");
  sel.innerHTML = Object.keys(profiles || {}).map(n => "<option value='" + esc(n) + "'>" + esc(n) + "</option>").join("");
}

function renderModels(models) {
  const aliases = document.getElementById("model-aliases");
  if (models.error) {
    aliases.innerHTML = '<p class="dim">' + esc(models.error) + "</p>";
  } else {
    const items = (models.aliases || []).map(a => "<code>" + esc(a) + "</code>").join(" ");
    aliases.innerHTML = items || '<p class="dim">No aliases returned.</p>';
  }
  const mapping = document.getElementById("role-mapping");
  const rows = Object.entries(models.role_mapping || {}).map(([role, alias]) =>
    "<tr><td class='mono'>" + esc(role) + "</td><td class='mono'>" + esc(alias) + "</td></tr>"
  );
  mapping.innerHTML = rows.length ? table(["role", "alias"], rows) : '<p class="dim">No mapping.</p>';
}

document.getElementById("latency-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const f = e.target;
  const body = { model: f.model.value.trim() };
  const mt = parseInt(f.max_tokens.value, 10);
  if (mt > 0) body.max_tokens = mt;
  const pre = document.getElementById("latency-result");
  pre.textContent = "Running probe…";
  try {
    const r = await fetch("/api/latency-test", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });
    pre.textContent = JSON.stringify(await r.json(), null, 2);
  } catch (err) { pre.textContent = "error: " + err; }
});

document.getElementById("plan-btn").addEventListener("click", async () => {
  const name = document.getElementById("plan-profile").value;
  const pre = document.getElementById("run-plan-result");
  pre.textContent = "Resolving plan…";
  try {
    const r = await fetch("/api/run-plan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ profile: name })
    });
    pre.textContent = JSON.stringify(await r.json(), null, 2);
  } catch (err) { pre.textContent = "error: " + err; }
});

async function load() {
  try {
    const [status, profiles, models, reports] = await Promise.all([
      getJSON("/api/status"), getJSON("/api/profiles"), getJSON("/api/models"), getJSON("/api/reports")
    ]);
    renderStatus(status);
    renderTimeline(status);
    renderProfiles(profiles);
    renderModels(models);
    renderReports(reports);
  } catch (err) {
    document.body.insertAdjacentHTML("afterbegin", "<p style='color:#e74c3c;padding:10px 24px'>Failed to load: " + esc(err) + "</p>");
  }
}
load();
</script>
</body>
</html>
"""
