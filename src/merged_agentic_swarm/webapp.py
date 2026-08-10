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
  PUT  /api/models/{role}   set one role -> alias mapping in PROVIDER_REGISTRY.json.
  GET  /api/chains          merged fabric chain view (code defaults + overlay).
  PUT  /api/chains/{alias}  upsert one chain alias into fabric-routes.json.
  GET  /api/run-plan        resolve a profile into a run plan WITHOUT executing.
  POST /api/run             start a REAL agentic workflow in a background thread.
  POST /api/latency-test    streaming TTFB/total latency probe against litellm.

The dashboard is served at GET /. It renders provider/proxy status, the latest
run report summary + timeline, reports, profiles, the model routing table, and
a latency-test form. All secrets are referenced by env-var NAME only — never
printed, logged, or returned.

Modeled on ``streaming_proxy.create_app``: a factory returning a Starlette app
plus a separate uvicorn entry point (``agentic-ui``).
"""

from __future__ import annotations

import json
import logging
import os
import re
import threading
import time
import uuid
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path

import httpx
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, StreamingResponse
from starlette.routing import Route

from merged_agentic_swarm.providers import multi_provider_fabric
from merged_agentic_swarm.providers.key_pool import default_key_pool
from merged_agentic_swarm.providers.multi_provider_fabric import MODEL_FABRIC_ROUTES
from merged_agentic_swarm.services import model_routing, swarm_profiles

logger = logging.getLogger("webapp")

# ── Paths & litellm endpoints ───────────────────────────────────────────────

_REPO_ROOT = Path(__file__).resolve().parents[2]
_REPORTS_DIR = _REPO_ROOT / "reports"

_LITELLM_BASE = "http://127.0.0.1:4000"
_LITELLM_MODELS_URL = f"{_LITELLM_BASE}/v1/models"
_LITELLM_CHAT_URL = f"{_LITELLM_BASE}/v1/chat/completions"

# ── Chat session store ─────────────────────────────────────────────────────

_CHAT_SESSIONS: dict[str, dict] = {}
_CHAT_SESSIONS_LOCK = threading.Lock()
_CHAT_SESSION_TTL = 3600  # 1 hour


def _clean_expired_sessions() -> None:
    """Remove sessions older than TTL."""
    now = time.time()
    with _CHAT_SESSIONS_LOCK:
        expired = [sid for sid, s in _CHAT_SESSIONS.items() if now - s["last_active"] > _CHAT_SESSION_TTL]
        for sid in expired:
            del _CHAT_SESSIONS[sid]


# The ramp agentic-cli applies when a profile's waves list is empty.
DEFAULT_RAMP = [4, 8, 16, 24, 40]

# Keys a profile update may carry (unknown keys are rejected with a 400).
PROFILE_KEYS = {"description", "waves", "default_tier", "model_alias", "gates", "worker_roles"}

_REPORT_NAME_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")

# Chain alias / role alias identifiers must be a sane dotted/dashed token.
_ALIAS_RE = re.compile(r"[A-Za-z][A-Za-z0-9._-]*")

# Optional per-alias fabric route overlay merged over the code MODEL_FABRIC_ROUTES.
_FABRIC_ROUTES_PATH = _REPO_ROOT / "docs" / "agentic" / "fabric-routes.json"


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


def _write_registry_roles(role: str, alias: str) -> None:
    """Persist one role -> alias mapping into PROVIDER_REGISTRY.json atomically.

    The rest of the registry (tiers, policy, backends, …) is preserved verbatim.
    The parsed-registry cache is invalidated so the next resolution re-reads disk;
    ``model_routing.reload_registry()`` is also invoked when available so other
    callers that cache the registry observe the change immediately.
    """
    path = model_routing._REGISTRY_PATH
    try:
        with open(path, encoding="utf-8") as f:
            registry = json.load(f)
    except OSError, ValueError:
        registry = {}
    if not isinstance(registry, dict):
        registry = {}
    role_routing = registry.get("role_routing")
    if not isinstance(role_routing, dict):
        role_routing = {}
        registry["role_routing"] = role_routing
    roles = role_routing.get("roles")
    if not isinstance(roles, dict):
        roles = {}
        role_routing["roles"] = roles
    roles[role] = alias
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)
    model_routing._registry_cache = None
    reload_registry = getattr(model_routing, "reload_registry", None)
    if reload_registry is not None:
        reload_registry()


def _load_fabric_overlay() -> dict:
    """fabric-routes.json as {"routes": {alias: [route, …]}}; {} when absent."""
    try:
        with open(_FABRIC_ROUTES_PATH, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
    except OSError, ValueError:
        pass
    return {}


def _fabric_chains() -> dict:
    """Merged fabric chain view: code MODEL_FABRIC_ROUTES overlaid per alias."""
    merged: dict = {}
    for alias, routes in MODEL_FABRIC_ROUTES.items():
        merged[alias] = [dict(route) for route in routes]
    overlay = _load_fabric_overlay()
    table = overlay.get("routes")
    if isinstance(table, dict):
        merged.update(table)
    return merged


def _write_fabric_overlay(alias: str, routes: list[dict]) -> None:
    """Upsert one chain alias into fabric-routes.json atomically."""
    path = _FABRIC_ROUTES_PATH
    overlay = _load_fabric_overlay()
    table = overlay.get("routes")
    if not isinstance(table, dict):
        table = {}
        overlay["routes"] = table
    table[alias] = routes
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(overlay, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)
    reload_fabric = getattr(multi_provider_fabric, "reload_fabric_routes", None)
    if reload_fabric is not None:
        reload_fabric()


@dataclass
class RunHandle:
    """Registry entry for a background workflow run."""

    id: str
    cancel_event: threading.Event
    started_at: float
    status: str = "running"
    thread: threading.Thread | None = None


_run_registry: dict[str, RunHandle] = {}
_run_registry_lock = threading.Lock()


def _serialize_run(handle: RunHandle) -> dict:
    status = handle.status
    if status == "running" and handle.thread is not None and not handle.thread.is_alive():
        status = "completed"
    return {
        "run_id": handle.id,
        "status": status,
        "started_at": handle.started_at,
        "cancel_requested": handle.cancel_event.is_set(),
        "alive": handle.thread is not None and handle.thread.is_alive(),
    }


def _spawn_agentic_run(profile: dict, alias: str, prd: str) -> RunHandle:
    """Start a real agentic workflow on a background daemon thread (returns now).

    Returns a :class:`RunHandle` so callers can poll ``/api/run/status`` and
    cancel the run via its ``cancel_event`` (checked between waves).
    """
    from merged_agentic_swarm.tools.agentic_orchestrator import MultiLayeredAgenticOrchestrator

    cancel_event = threading.Event()
    handle = RunHandle(id=f"run-{int(time.time() * 1000)}", cancel_event=cancel_event, started_at=time.time())

    def _runner() -> None:
        try:
            orchestrator = MultiLayeredAgenticOrchestrator()
            result = orchestrator.run_full_agentic_workflow(
                prd_content=prd,
                ramp_sequence=profile.get("waves") or None,
                default_model=alias,
                gates=profile.get("gates"),
                cancel_event=cancel_event,
            )
            handle.status = "aborted" if result.get("status") == "aborted" else "completed"
        except Exception:
            logger.exception("agentic run failed in background thread")
            handle.status = "error"

    thread = threading.Thread(target=_runner, name=f"agentic-run-{handle.id}", daemon=True)
    handle.thread = thread
    thread.start()
    return handle


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


# ── Chat handlers ──────────────────────────────────────────────────────────


async def _stream_chat_response(
    client: httpx.AsyncClient, model: str, messages: list[dict], max_tokens: int, temperature: float
):
    """Generator that yields SSE chunks from litellm chat/completions."""
    key = os.environ.get("LITELLM_PROXY_KEY")
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": True,
    }
    try:
        req = client.build_request("POST", _LITELLM_CHAT_URL, json=payload, headers=headers)
        resp = await client.send(req, stream=True)
    except Exception as exc:
        error_chunk = json.dumps({"error": f"litellm unreachable: {exc}", "model": model, "provider": "litellm"})
        yield b"data: " + error_chunk.encode() + b"\n\n"
        yield b"data: [DONE]\n\n"
        return

    try:
        async for chunk in resp.aiter_bytes():
            if chunk:
                yield (
                    b"data: "
                    + json.dumps(
                        {"model": model, "provider": "litellm", "chunk": chunk.decode(errors="replace")}
                    ).encode()
                    + b"\n\n"
                )
    except Exception as exc:
        error_chunk = json.dumps({"error": f"stream read error: {exc}", "model": model, "provider": "litellm"})
        yield b"data: " + error_chunk.encode() + b"\n\n"
    finally:
        if not resp.is_closed:
            await resp.aclose()
    yield b"data: [DONE]\n\n"


async def handle_chat(request: Request):
    """POST /api/chat — send a chat message, optionally stream the response."""
    _clean_expired_sessions()
    try:
        body = await request.json()
    except ValueError:
        return JSONResponse({"error": "invalid JSON body"}, status_code=400)
    if not isinstance(body, dict):
        return JSONResponse({"error": "body must be a JSON object"}, status_code=400)

    model = body.get("model")
    if not isinstance(model, str) or not model.strip():
        return JSONResponse({"error": "model is required"}, status_code=400)

    messages = body.get("messages")
    if not isinstance(messages, list) or not messages:
        return JSONResponse({"error": "messages must be a non-empty list"}, status_code=400)

    stream = bool(body.get("stream", True))
    max_tokens = int(body.get("max_tokens") or 1024)
    temperature = float(body.get("temperature") or 0.7)

    client: httpx.AsyncClient = request.app.state.httpx_client

    if stream:
        return StreamingResponse(
            _stream_chat_response(client, model, messages, max_tokens, temperature),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )

    # Non-streaming path
    key = os.environ.get("LITELLM_PROXY_KEY")
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": False,
    }
    try:
        resp = await client.post(_LITELLM_CHAT_URL, json=payload, headers=headers)
        data = resp.json()
        return JSONResponse({"model": model, "provider": "litellm", "response": data})
    except Exception as exc:
        return JSONResponse({"error": f"chat request failed: {exc}", "model": model}, status_code=502)


async def handle_chat_sessions(request: Request):
    """GET /api/chat/sessions — list active sessions.
    POST /api/chat/sessions — create a new session."""
    _clean_expired_sessions()
    if request.method == "GET":
        with _CHAT_SESSIONS_LOCK:
            sessions = [
                {
                    "session_id": sid,
                    "created_at": s["created_at"],
                    "last_active": s["last_active"],
                    "message_count": len(s["messages"]),
                }
                for sid, s in _CHAT_SESSIONS.items()
            ]
        return JSONResponse({"sessions": sessions})

    # POST — create session
    session_id = uuid.uuid4().hex[:12]
    now = time.time()
    with _CHAT_SESSIONS_LOCK:
        _CHAT_SESSIONS[session_id] = {
            "id": session_id,
            "created_at": now,
            "last_active": now,
            "messages": [],
        }
    return JSONResponse({"session_id": session_id, "created_at": now}, status_code=201)


async def handle_chat_session(request: Request):
    """GET /api/chat/sessions/{session_id} — get session messages.
    POST /api/chat/sessions/{session_id} — send message in session.
    DELETE /api/chat/sessions/{session_id} — delete session."""
    _clean_expired_sessions()
    session_id = request.path_params["session_id"]

    with _CHAT_SESSIONS_LOCK:
        session = _CHAT_SESSIONS.get(session_id)

    if session is None:
        return JSONResponse({"error": f"unknown session: {session_id}"}, status_code=404)

    if request.method == "GET":
        return JSONResponse(
            {
                "session_id": session_id,
                "messages": session["messages"],
                "created_at": session["created_at"],
                "last_active": session["last_active"],
            }
        )

    if request.method == "DELETE":
        with _CHAT_SESSIONS_LOCK:
            _CHAT_SESSIONS.pop(session_id, None)
        return JSONResponse({"deleted": True, "session_id": session_id})

    # POST — send message in session context
    try:
        body = await request.json()
    except ValueError:
        return JSONResponse({"error": "invalid JSON body"}, status_code=400)
    if not isinstance(body, dict):
        return JSONResponse({"error": "body must be a JSON object"}, status_code=400)

    model = body.get("model")
    if not isinstance(model, str) or not model.strip():
        return JSONResponse({"error": "model is required"}, status_code=400)

    content = body.get("content")
    if not isinstance(content, str) or not content.strip():
        return JSONResponse({"error": "content is required"}, status_code=400)

    stream = bool(body.get("stream", True))
    max_tokens = int(body.get("max_tokens") or 1024)
    temperature = float(body.get("temperature") or 0.7)

    # Append user message
    user_msg = {"role": "user", "content": content}
    with _CHAT_SESSIONS_LOCK:
        session["messages"].append(user_msg)
        session["last_active"] = time.time()
        messages = list(session["messages"])

    client: httpx.AsyncClient = request.app.state.httpx_client

    if stream:

        async def session_stream():
            full_response = ""
            async for chunk in _stream_chat_response(client, model, messages, max_tokens, temperature):
                yield chunk
                # Accumulate assistant response from chunks
                try:
                    if chunk.startswith(b"data: ") and not chunk.startswith(b"data: [DONE]"):
                        data = json.loads(chunk[6:].decode(errors="replace"))
                        if "chunk" in data:
                            # Try to parse litellm SSE chunk for delta content
                            try:
                                sse_data = json.loads(data["chunk"].removeprefix("data: ").strip())
                                for choice in sse_data.get("choices", []):
                                    delta = choice.get("delta", {})
                                    if "content" in delta:
                                        full_response += delta["content"]
                            except json.JSONDecodeError, KeyError:
                                pass
                except Exception:
                    pass
            # Append assistant message to session
            if full_response:
                with _CHAT_SESSIONS_LOCK:
                    session["messages"].append({"role": "assistant", "content": full_response})
                    session["last_active"] = time.time()

        return StreamingResponse(
            session_stream(),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive", "X-Accel-Buffering": "no"},
        )

    # Non-streaming session
    key = os.environ.get("LITELLM_PROXY_KEY")
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": False,
    }
    try:
        resp = await client.post(_LITELLM_CHAT_URL, json=payload, headers=headers)
        data = resp.json()
        assistant_content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        assistant_msg = {"role": "assistant", "content": assistant_content}
        with _CHAT_SESSIONS_LOCK:
            session["messages"].append(assistant_msg)
            session["last_active"] = time.time()
        return JSONResponse(
            {"session_id": session_id, "model": model, "provider": "litellm", "messages": session["messages"]}
        )
    except Exception as exc:
        return JSONResponse({"error": f"chat request failed: {exc}", "model": model}, status_code=502)


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


async def handle_model_role_update(request: Request) -> JSONResponse:
    role = request.path_params["role"]
    if not isinstance(role, str) or not role.strip():
        return JSONResponse({"error": "role must be a non-empty string"}, status_code=400)
    try:
        body = await request.json()
    except ValueError:
        return JSONResponse({"error": "invalid JSON body"}, status_code=400)
    if not isinstance(body, dict):
        return JSONResponse({"error": "body must be a JSON object"}, status_code=400)
    alias = body.get("alias")
    if not isinstance(alias, str) or not _ALIAS_RE.fullmatch(alias):
        return JSONResponse({"error": "alias must match ^[A-Za-z][A-Za-z0-9._-]*$"}, status_code=400)
    _write_registry_roles(role, alias)
    return JSONResponse({"ok": True, "role": role, "alias": alias, "role_mapping": _role_mapping()})


async def handle_chains(request: Request) -> JSONResponse:
    return JSONResponse({"chains": _fabric_chains()})


async def handle_chain_update(request: Request) -> JSONResponse:
    alias = request.path_params["alias"]
    if not isinstance(alias, str) or not _ALIAS_RE.fullmatch(alias):
        return JSONResponse({"error": f"invalid chain alias: {alias}"}, status_code=400)
    try:
        body = await request.json()
    except ValueError:
        return JSONResponse({"error": "invalid JSON body"}, status_code=400)
    if not isinstance(body, dict):
        return JSONResponse({"error": "body must be a JSON object"}, status_code=400)
    routes = body.get("routes")
    if not isinstance(routes, list) or not routes:
        return JSONResponse({"error": "routes must be a non-empty list"}, status_code=400)
    cleaned: list[dict] = []
    for i, route in enumerate(routes):
        if not isinstance(route, dict):
            return JSONResponse({"error": f"route {i} must be an object"}, status_code=400)
        provider = route.get("provider")
        if not isinstance(provider, str) or not provider.strip():
            return JSONResponse({"error": f"route {i}: provider must be a non-empty string"}, status_code=400)
        model = route.get("model")
        if not isinstance(model, str) or not model.strip():
            return JSONResponse({"error": f"route {i}: model must be a non-empty string"}, status_code=400)
        entry: dict = {"provider": provider, "model": model}
        url = route.get("url")
        if url is not None:
            if not isinstance(url, str) or not url.strip():
                return JSONResponse({"error": f"route {i}: url must be a string"}, status_code=400)
            entry["url"] = url
        timeout = route.get("timeout")
        if timeout is not None:
            if isinstance(timeout, bool) or not isinstance(timeout, (int, float)):
                return JSONResponse({"error": f"route {i}: timeout must be a number"}, status_code=400)
            entry["timeout"] = timeout
        cleaned.append(entry)
    _write_fabric_overlay(alias, cleaned)
    return JSONResponse({"ok": True, "alias": alias, "routes": cleaned, "chains": _fabric_chains()})


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


async def handle_run(request: Request) -> JSONResponse:
    """Start a real agentic workflow in a background daemon thread; return now."""
    try:
        body = await request.json()
    except ValueError:
        return JSONResponse({"error": "invalid JSON body"}, status_code=400)
    if not isinstance(body, dict):
        return JSONResponse({"error": "body must be a JSON object"}, status_code=400)
    name = body.get("profile")
    if not isinstance(name, str) or not name:
        return JSONResponse({"error": "profile is required"}, status_code=400)
    prd = body.get("prd")
    if not isinstance(prd, str) or not prd.strip():
        return JSONResponse({"error": "prd is required"}, status_code=400)
    try:
        profile = swarm_profiles.resolve_profile(name)
    except KeyError:
        return JSONResponse({"error": f"unknown profile: {name}"}, status_code=404)
    alias = swarm_profiles.resolve_model_alias_for_profile(name)
    handle = _spawn_agentic_run(profile, alias, prd)
    with _run_registry_lock:
        _run_registry[handle.id] = handle
    request.app.state.last_run_thread = handle.thread
    return JSONResponse({"started": True, "profile": name, "model_alias": alias})


async def handle_run_status(request: Request) -> JSONResponse:
    """Report live status for a run (or all runs when no ``run_id`` is given)."""
    run_id = request.query_params.get("run_id")
    with _run_registry_lock:
        if run_id is None:
            return JSONResponse({"runs": {rid: _serialize_run(h) for rid, h in _run_registry.items()}})
        handle = _run_registry.get(run_id)
    if handle is None:
        return JSONResponse({"error": f"unknown run: {run_id}"}, status_code=404)
    return JSONResponse(_serialize_run(handle))


async def handle_run_cancel(request: Request) -> JSONResponse:
    """Signal a running workflow to abort at the next wave boundary."""
    run_id = request.path_params.get("run_id")
    with _run_registry_lock:
        handle = _run_registry.get(run_id)
    if handle is None:
        return JSONResponse({"error": f"unknown run: {run_id}"}, status_code=404)
    handle.cancel_event.set()
    if handle.status == "running":
        handle.status = "cancelling"
    return JSONResponse({"cancelled": True, "run_id": run_id, "status": handle.status})


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
            Route("/api/models/{role}", handle_model_role_update, methods=["PUT"]),
            Route("/api/chains", handle_chains, methods=["GET"]),
            Route("/api/chains/{alias}", handle_chain_update, methods=["PUT"]),
            Route("/api/latency-test", handle_latency_test, methods=["POST"]),
            Route("/api/chat", handle_chat, methods=["POST"]),
            Route("/api/chat/sessions", handle_chat_sessions, methods=["GET", "POST"]),
            Route("/api/chat/sessions/{session_id}", handle_chat_session, methods=["GET", "POST", "DELETE"]),
            Route("/api/run-plan", handle_run_plan, methods=["POST"]),
            Route("/api/run", handle_run, methods=["POST"]),
            Route("/api/run/status", handle_run_status, methods=["GET"]),
            Route("/api/run/{run_id}/cancel", handle_run_cancel, methods=["POST"]),
        ],
        lifespan=lifespan,
    )
    app.state.httpx_client = client
    return app


def main() -> None:
    """Run the control panel. Defaults to loopback; pass --host 0.0.0.0 to expose."""
    import sys

    import uvicorn

    host = os.environ.get("WEBAPP_HOST", "127.0.0.1")
    port = int(os.environ.get("WEBAPP_PORT", "8123"))

    # Allow --host and --port CLI overrides
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--host" and i + 1 < len(args):
            host = args[i + 1]
            i += 2
        elif args[i] == "--port" and i + 1 < len(args):
            port = int(args[i + 1])
            i += 2
        else:
            i += 1

    if host in ("0.0.0.0", "::"):
        print(f"⚠ Web UI bound to {host} — accessible on your network. Secrets are never exposed.", flush=True)

    uvicorn.run(create_app(), host=host, port=port)


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
  /* ── Chat ── */
  #chat { display:flex; flex-direction:column; }
  .chat-header { display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:6px; }
  .chat-header h2 { margin:0; }
  #chat-messages { flex:1; min-height:220px; max-height:450px; overflow-y:auto; display:flex; flex-direction:column; gap:8px; padding:4px 0; }
  .chat-msg { padding:8px 12px; border-radius:10px; max-width:85%; font-size:13px; line-height:1.5; white-space:pre-wrap; word-break:break-word; }
  .chat-msg.user { align-self:flex-end; background:var(--acc); color:#fff; border-bottom-right-radius:3px; }
  .chat-msg.assistant { align-self:flex-start; background:#0d0f13; border:1px solid var(--line); border-bottom-left-radius:3px; }
  .chat-msg.streaming::after { content:"\\25A0"; animation:chat-blink 1s step-end infinite; margin-left:2px; }
  @keyframes chat-blink { 50% { opacity:0; } }
  .chat-msg.error { align-self:flex-start; background:transparent; border:1px solid var(--bad); color:var(--bad); font-size:12px; }
  #chat-system-toggle { margin-bottom:8px; font-size:12px; color:var(--dim); }
  #chat-system-toggle summary { cursor:pointer; user-select:none; }
  #chat-system { width:100%; resize:vertical; margin-top:6px; }
  #chat-send { white-space:nowrap; }
  #chat-send:disabled { opacity:.55; cursor:not-allowed; }
</style>
</head>
<body>
<header>
  <h1>Agentic Swarm Control Panel</h1>
  <p>Provider pools, fabric routes, run reports, swarm profiles, and model routing. Secrets are never shown — auth is referenced by env-var name only.</p>
</header>
<main>
  <section id="chat">
    <div class="chat-header">
      <h2>Chat</h2>
      <div class="row">
        <select id="chat-model"><option>Loading models…</option></select>
        <button id="chat-new-btn" title="Start a new chat session">+ New</button>
      </div>
    </div>
    <details id="chat-system-toggle">
      <summary>System prompt</summary>
      <textarea id="chat-system" rows="3" placeholder="Optional system prompt (set before sending the first message)…"></textarea>
    </details>
    <div id="chat-messages"><p class="dim" style="margin:auto;padding:40px 0">Select a model and send a message to start.</p></div>
    <div class="row" style="margin-top:8px">
      <textarea id="chat-input" rows="2" placeholder="Type a message… (Enter to send, Shift+Enter for newline)" style="flex:1;resize:none"></textarea>
      <button id="chat-send">Send</button>
    </div>
    <span id="chat-status" class="dim" style="font-size:11px;margin-top:4px"></span>
  </section>

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
    <h3>Run Profile — executes for real</h3>
    <form id="run-form" class="row">
      <select id="run-profile" style="min-width:110px"></select>
      <textarea name="prd" rows="3" placeholder="# title&#10;&#10;body" required style="min-width:300px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px"></textarea>
      <button type="submit">Start run</button>
    </form>
    <p class="bad" style="font-size:12px;margin:6px 0 0">Warning: this starts a real agentic workflow in the background.</p>
    <span id="run-result" class="dim"></span>
  </section>

  <section>
    <h2>Model Routing</h2>
    <h3>Litellm Live Aliases</h3>
    <div id="model-aliases"><p class="dim">Loading…</p></div>
    <h3>Role → Alias</h3>
    <div id="role-mapping"><p class="dim">Loading…</p></div>
    <h3>Edit Role Alias</h3>
    <form id="role-form" class="row">
      <input name="role" placeholder="role, e.g. deep" required style="width:140px">
      <input name="alias" placeholder="alias, e.g. gemini-batch" required style="min-width:180px">
      <button type="submit">Save role</button>
    </form>
    <span id="role-result" class="dim"></span>
  </section>

  <section>
    <h2>Fabric Chains</h2>
    <div id="chains"><p class="dim">Loading…</p></div>
    <h3>Edit Chain Alias</h3>
    <form id="chain-form" class="row">
      <input name="alias" placeholder="chain alias, e.g. claude-3-7-sonnet" required style="min-width:190px">
      <textarea name="routes" rows="3" placeholder='[{"provider":"gemini","model":"gemini-2.5-flash","timeout":30}]' required style="min-width:280px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px"></textarea>
      <button type="submit">Save chain</button>
    </form>
    <span id="chain-result" class="dim"></span>
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
  const opts = Object.keys(profiles || {}).map(n => "<option value='" + esc(n) + "'>" + esc(n) + "</option>").join("");
  document.getElementById("plan-profile").innerHTML = opts;
  document.getElementById("run-profile").innerHTML = opts;
}

function renderChains(chains) {
  const el = document.getElementById("chains");
  const rows = Object.entries(chains || {}).map(([alias, routes]) =>
    "<tr><td class='mono'><a data-alias='" + esc(alias) + "'>" + esc(alias) + "</a></td><td class='mono'>" + (routes || []).map(r => esc(r.provider) + "/" + esc(r.model)).join("<br>") + "</td></tr>"
  );
  el.innerHTML = rows.length ? table(["alias", "route chain (provider/model)"], rows) : '<p class="dim">No fabric chains.</p>';
  el.querySelectorAll("a").forEach(a => a.addEventListener("click", () => {
    const f = document.getElementById("chain-form");
    f.alias.value = a.dataset.alias;
    f.routes.value = JSON.stringify(chains[a.dataset.alias], null, 2);
    document.getElementById("chain-result").textContent = "Loaded " + a.dataset.alias + " — edit and Save chain to persist.";
  }));
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
  /* Also populate the chat model dropdown */
  const chatSel = document.getElementById("chat-model");
  const chatAliases = (models.aliases || []).filter(function(a) { return a; });
  if (chatAliases.length) {
    chatSel.innerHTML = chatAliases.map(function(a) { return "<option value='" + esc(a) + "'>" + esc(a) + "</option>"; }).join("");
  } else if (!models.error) {
    chatSel.innerHTML = "<option>No models available</option>";
  }
}

/* ── Chat logic ── */

var _chatSessionId = "s" + Date.now().toString(36);
var _chatAbortCtrl = null;

function _chatMsgEl(role, text) {
  var div = document.createElement("div");
  div.className = "chat-msg " + role;
  div.textContent = text;
  return div;
}

function _chatBubble(role) {
  var div = document.createElement("div");
  div.className = "chat-msg " + role;
  return div;
}

async function chatSend() {
  var input = document.getElementById("chat-input");
  var text = input.value.trim();
  if (!text) return;

  var model = document.getElementById("chat-model").value;
  var system = document.getElementById("chat-system").value.trim();
  var area = document.getElementById("chat-messages");
  var status = document.getElementById("chat-status");
  var sendBtn = document.getElementById("chat-send");

  /* Remove placeholder if present */
  var placeholder = area.querySelector("p.dim");
  if (placeholder) placeholder.remove();

  /* Append user bubble */
  area.appendChild(_chatMsgEl("user", text));
  input.value = "";
  area.scrollTop = area.scrollHeight;

  /* Create assistant bubble */
  var assistantBubble = _chatBubble("assistant");
  assistantBubble.classList.add("streaming");
  area.appendChild(assistantBubble);
  area.scrollTop = area.scrollHeight;

  status.textContent = "Streaming…";
  sendBtn.disabled = true;

  /* Abort any in-flight request */
  if (_chatAbortCtrl) { _chatAbortCtrl.abort(); }
  _chatAbortCtrl = new AbortController();

  try {
    var messages = [{ role: "user", content: text }];
    var body = { model: model, messages: messages, stream: true };
    if (system) body.system = system;

    var resp = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      signal: _chatAbortCtrl.signal
    });

    if (!resp.ok) {
      assistantBubble.classList.remove("streaming");
      var errText;
      try {
        var errJson = await resp.json();
        errText = "Error: " + (errJson.error || ("HTTP " + resp.status));
      } catch (_) {
        errText = "Error: HTTP " + resp.status;
      }
      assistantBubble.textContent = errText;
      assistantBubble.className = "chat-msg error";
      status.textContent = "";
      sendBtn.disabled = false;
      _chatAbortCtrl = null;
      return;
    }

    var reader = resp.body.getReader();
    var decoder = new TextDecoder();
    var buf = "";

    while (true) {
      var chunk = await reader.read();
      if (chunk.done) break;
      buf += decoder.decode(chunk.value, { stream: true });
      var lines = buf.split("\\n");
      buf = lines.pop() || "";
      for (var i = 0; i < lines.length; i++) {
        var line = lines[i];
        if (line.indexOf("data: ") === 0) {
          var data = line.slice(6);
          if (data === "[DONE]") continue;
          try {
            var parsed = JSON.parse(data);
            var choices = parsed.choices;
            if (choices && choices[0]) {
              var delta = choices[0].delta;
              if (delta && delta.content) {
                assistantBubble.textContent += delta.content;
              }
            }
          } catch (_) { /* skip unparseable chunks */ }
        }
      }
      area.scrollTop = area.scrollHeight;
    }

    assistantBubble.classList.remove("streaming");
    status.textContent = "";
    sendBtn.disabled = false;
    _chatAbortCtrl = null;
  } catch (err) {
    if (err.name === "AbortError") {
      assistantBubble.textContent = (assistantBubble.textContent || "") + "\\n[stopped]";
    } else {
      assistantBubble.textContent = "Error: " + err;
      assistantBubble.className = "chat-msg error";
    }
    assistantBubble.classList.remove("streaming");
    status.textContent = "";
    sendBtn.disabled = false;
    _chatAbortCtrl = null;
  }
}

function chatNewSession() {
  /* Abort any in-flight streaming */
  if (_chatAbortCtrl) { _chatAbortCtrl.abort(); _chatAbortCtrl = null; }

  var area = document.getElementById("chat-messages");
  area.innerHTML = '<p class="dim" style="margin:auto;padding:40px 0">Select a model and send a message to start.</p>';

  document.getElementById("chat-system").value = "";
  document.getElementById("chat-system-toggle").open = false;
  document.getElementById("chat-input").value = "";
  document.getElementById("chat-status").textContent = "";
  document.getElementById("chat-send").disabled = false;

  _chatSessionId = "s" + Date.now().toString(36);
}

document.getElementById("chat-send").addEventListener("click", chatSend);
document.getElementById("chat-input").addEventListener("keydown", function(e) {
  if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); chatSend(); }
});
document.getElementById("chat-new-btn").addEventListener("click", chatNewSession);

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

document.getElementById("role-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const f = e.target;
  const out = document.getElementById("role-result");
  out.textContent = "Saving role…";
  try {
    const r = await fetch("/api/models/" + encodeURIComponent(f.role.value.trim()), {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ alias: f.alias.value.trim() })
    });
    const data = await r.json();
    if (!r.ok) { out.textContent = "error: " + (data.error || r.status); return; }
    out.textContent = "Saved " + f.role.value.trim() + " -> " + f.alias.value.trim();
    load();
  } catch (err) { out.textContent = "error: " + err; }
});

document.getElementById("chain-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const f = e.target;
  const out = document.getElementById("chain-result");
  let routes;
  try { routes = JSON.parse(f.routes.value); }
  catch { out.textContent = "error: routes must be valid JSON"; return; }
  out.textContent = "Saving chain…";
  try {
    const r = await fetch("/api/chains/" + encodeURIComponent(f.alias.value.trim()), {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ routes: routes })
    });
    const data = await r.json();
    if (!r.ok) { out.textContent = "error: " + (data.error || r.status); return; }
    out.textContent = "Saved chain " + f.alias.value.trim();
    load();
  } catch (err) { out.textContent = "error: " + err; }
});

document.getElementById("run-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const f = e.target;
  const out = document.getElementById("run-result");
  out.textContent = "Starting run…";
  try {
    const r = await fetch("/api/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ profile: document.getElementById("run-profile").value, prd: f.prd.value })
    });
    const data = await r.json();
    if (!r.ok) { out.textContent = "error: " + (data.error || r.status); return; }
    out.textContent = "Started " + data.profile + " (" + data.model_alias + ") — watch System Status / Reports.";
  } catch (err) { out.textContent = "error: " + err; }
});

async function load() {
  try {
    const [status, profiles, models, reports, chains] = await Promise.all([
      getJSON("/api/status"), getJSON("/api/profiles"), getJSON("/api/models"), getJSON("/api/reports"), getJSON("/api/chains")
    ]);
    renderStatus(status);
    renderTimeline(status);
    renderProfiles(profiles);
    renderModels(models);
    renderReports(reports);
    renderChains(chains.chains);
  } catch (err) {
    document.body.insertAdjacentHTML("afterbegin", "<p style='color:#e74c3c;padding:10px 24px'>Failed to load: " + esc(err) + "</p>");
  }
}
load();
</script>
</body>
</html>
"""
