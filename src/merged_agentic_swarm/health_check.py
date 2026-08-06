"""Proxy-chain health check for the merged agentic swarm.

Verifies the full proxy chain that clients use for LLM traffic:

    client -> FCC (port 8080) -> routatic-proxy (port 3456) -> opencode.ai (upstream)

Responsibilities:
  * Probe each hop for reachability and latency.
  * Measure end-to-end streaming latency (time-to-first-token and total
    stream duration) through the chain.
  * Monitor provider/circuit-breaker status reported by routatic-proxy.

CLI (also importable):

    uv run python -m merged_agentic_swarm.health_check            # all checks
    uv run python -m merged_agentic_swarm.health_check status     # hop probes only
    uv run python -m merged_agentic_swarm.health_check stream     # streaming latency
    uv run python -m merged_agentic_swarm.health_check providers  # provider status
    uv run python -m merged_agentic_swarm.health_check --json     # machine output

Endpoints/auth are overridable via env vars (see :class:`HealthConfig`).
Exit code is 0 when every enabled check passes, 1 otherwise.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
from dataclasses import dataclass, field
from typing import Any

import httpx

DEFAULT_PROMPT = "Reply with the single word: OK"


# ── Configuration ─────────────────────────────────────────────────────────


@dataclass
class HealthConfig:
    """Endpoints and request tuning for the health checks.

    Each field falls back to the matching env var, then to a default.
    """

    fcc_url: str = "http://127.0.0.1:8080"
    routatic_url: str = "http://127.0.0.1:3456"
    opencode_url: str = "https://opencode.ai/zen"
    auth_token: str = "freecc"
    e2e_model: str = "claude-3-5-haiku"
    e2e_max_tokens: int = 16
    timeout: float = 30.0
    stream_timeout: float = 120.0

    @classmethod
    def from_env(cls) -> HealthConfig:
        env = os.environ.get
        return cls(
            fcc_url=env("FCC_URL", cls.fcc_url),
            routatic_url=env("ROUTATIC_URL", cls.routatic_url),
            opencode_url=env("OPENCODE_URL", cls.opencode_url),
            auth_token=env("ANTHROPIC_AUTH_TOKEN", cls.auth_token),
            e2e_model=env("E2E_MODEL", cls.e2e_model),
            e2e_max_tokens=int(env("E2E_MAX_TOKENS", str(cls.e2e_max_tokens))),
            timeout=float(env("HEALTH_TIMEOUT", str(cls.timeout))),
            stream_timeout=float(env("HEALTH_STREAM_TIMEOUT", str(cls.stream_timeout))),
        )


# ── Results ───────────────────────────────────────────────────────────────


@dataclass
class HopResult:
    """Outcome of a single health check."""

    name: str
    ok: bool
    latency_ms: float | None = None
    http_code: int | None = None
    detail: str = ""
    meta: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "check": self.name,
            "ok": 1 if self.ok else 0,
            "http": self.http_code,
            "latency_ms": self.latency_ms,
            "detail": self.detail,
            **self.meta,
        }


def _truncate(text: str, limit: int = 160) -> str:
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


# ── Checks ────────────────────────────────────────────────────────────────


class ProxyChainHealth:
    """Runs reachability, streaming, and provider-status checks."""

    def __init__(self, config: HealthConfig | None = None) -> None:
        self.cfg = config or HealthConfig.from_env()
        self._messages_headers = {
            "Content-Type": "application/json",
            "x-api-key": self.cfg.auth_token,
            "anthropic-version": "2023-06-01",
        }

    async def check_routatic(self) -> HopResult:
        """Probe routatic-proxy /health and surface circuit-breaker metrics."""
        url = f"{self.cfg.routatic_url.rstrip('/')}/health"
        start = time.monotonic()
        try:
            async with httpx.AsyncClient(timeout=self.cfg.timeout) as client:
                resp = await client.get(url)
            elapsed_ms = (time.monotonic() - start) * 1000
            ok = resp.status_code < 400
            meta: dict[str, Any] = {}
            try:
                data = resp.json()
                meta["service"] = data.get("service")
                meta["version"] = data.get("version")
                meta["router_status"] = data.get("status")
                breakers = data.get("circuit_breakers") or {}
                meta["circuit_breakers"] = breakers
                meta["models"] = list((data.get("models") or {}).keys())
                metrics = data.get("metrics") or {}
                meta["p95_latency_ms"] = metrics.get("p95_latency_ms")
                meta["requests_success"] = metrics.get("requests_success")
                meta["requests_failed"] = metrics.get("requests_failed")
            except ValueError, AttributeError:
                pass
            detail = _truncate(resp.text)
            return HopResult("routatic", ok, round(elapsed_ms, 2), resp.status_code, detail, meta)
        except httpx.HTTPError as exc:
            return HopResult("routatic", False, None, None, f"{type(exc).__name__}: {exc}")

    async def check_fcc(self) -> HopResult:
        """Probe the FCC gateway /health endpoint."""
        url = f"{self.cfg.fcc_url.rstrip('/')}/health"
        start = time.monotonic()
        try:
            async with httpx.AsyncClient(timeout=self.cfg.timeout) as client:
                resp = await client.get(url)
            elapsed_ms = (time.monotonic() - start) * 1000
            ok = resp.status_code < 400 and "healthy" in resp.text
            detail = _truncate(resp.text, 120)
            return HopResult("fcc", ok, round(elapsed_ms, 2), resp.status_code, detail)
        except httpx.HTTPError as exc:
            return HopResult("fcc", False, None, None, f"{type(exc).__name__}: {exc}")

    async def check_opencode(self) -> HopResult:
        """Check upstream OpenCode API reachability (models endpoint)."""
        url = f"{self.cfg.opencode_url.rstrip('/')}/v1/models"
        start = time.monotonic()
        try:
            async with httpx.AsyncClient(timeout=self.cfg.timeout) as client:
                resp = await client.get(url)
            elapsed_ms = (time.monotonic() - start) * 1000
            ok = resp.status_code < 400
            detail = _truncate(resp.text, 120)
            return HopResult("opencode", ok, round(elapsed_ms, 2), resp.status_code, detail)
        except httpx.HTTPError as exc:
            return HopResult("opencode", False, None, None, f"{type(exc).__name__}: {exc}")

    async def check_streaming(
        self,
        *,
        endpoint: str = "fcc",
        model: str | None = None,
        prompt: str = DEFAULT_PROMPT,
        max_tokens: int | None = None,
    ) -> HopResult:
        """Stream a tiny /v1/messages request and time first token + total.

        ``endpoint`` selects the entry point: ``fcc`` (full chain) or
        ``routatic`` (proxy hop only). Requires at least one
        ``content_block_delta`` to count as healthy.
        """
        base = self.cfg.fcc_url if endpoint == "fcc" else self.cfg.routatic_url
        url = f"{base.rstrip('/')}/v1/messages"
        selected_model = model or self.cfg.e2e_model
        payload = {
            "model": selected_model,
            "max_tokens": max_tokens or self.cfg.e2e_max_tokens,
            "stream": True,
            "messages": [{"role": "user", "content": prompt}],
        }
        start = time.monotonic()
        first_token_ms: float | None = None
        deltas = 0
        finished = False
        status_code: int | None = None
        try:
            timeout = httpx.Timeout(self.cfg.timeout, read=self.cfg.stream_timeout)
            async with (
                httpx.AsyncClient(timeout=timeout) as client,
                client.stream("POST", url, headers=self._messages_headers, json=payload) as resp,
            ):
                status_code = resp.status_code
                if resp.status_code >= 400:
                    body = (await resp.aread()).decode("utf-8", "replace")
                    return HopResult("stream", False, None, resp.status_code, _truncate(body, 160))
                async for line in resp.aiter_lines():
                    if first_token_ms is None and line.startswith("data:") and "content_block_delta" in line:
                        first_token_ms = (time.monotonic() - start) * 1000
                    if "content_block_delta" in line:
                        deltas += 1
                    if '"message_stop"' in line or line.strip() == "data: [DONE]":
                        finished = True
        except httpx.HTTPError as exc:
            return HopResult("stream", False, None, None, f"{type(exc).__name__}: {exc}")

        total_ms = (time.monotonic() - start) * 1000
        ok = deltas > 0
        meta = {
            "endpoint": endpoint,
            "model": selected_model,
            "ttfb_ms": round(first_token_ms, 2) if first_token_ms is not None else None,
            "total_ms": round(total_ms, 2),
            "content_deltas": deltas,
            "finished": finished,
        }
        ttfb = f"{meta['ttfb_ms']}ms" if meta["ttfb_ms"] is not None else "n/a"
        detail = f"model={selected_model} first_token={ttfb} total={total_ms:.0f}ms deltas={deltas}"
        return HopResult("stream", ok, round(total_ms, 2), status_code, detail, meta)

    async def check_providers(self) -> list[HopResult]:
        """Monitor provider/circuit-breaker status via routatic + FCC models list."""
        results = [await self.check_routatic()]
        # Surface the model catalog FCC exposes (names only, no credentials).
        url = f"{self.cfg.fcc_url.rstrip('/')}/v1/models"
        start = time.monotonic()
        try:
            async with httpx.AsyncClient(timeout=self.cfg.timeout) as client:
                resp = await client.get(url, headers=self._messages_headers)
            elapsed_ms = (time.monotonic() - start) * 1000
            ok = resp.status_code < 400
            model_count: int | None = None
            try:
                data = resp.json()
                if isinstance(data, list):
                    model_count = len(data)
                elif isinstance(data, dict) and isinstance(data.get("data"), list):
                    model_count = len(data["data"])
            except ValueError, AttributeError:
                pass
            detail = f"models={model_count}" if model_count is not None else _truncate(resp.text, 120)
            meta = {"models_served": model_count} if model_count is not None else {}
            results.append(HopResult("fcc-models", ok, round(elapsed_ms, 2), resp.status_code, detail, meta))
        except httpx.HTTPError as exc:
            results.append(HopResult("fcc-models", False, None, None, f"{type(exc).__name__}: {exc}"))
        return results

    async def run_all(self, include_stream: bool = True) -> list[HopResult]:
        """Run every check; returns results in a stable order."""
        results: list[HopResult] = [
            await self.check_routatic(),
            await self.check_fcc(),
            await self.check_opencode(),
        ]
        if include_stream:
            results.append(await self.check_streaming())
        return results


# ── Output ────────────────────────────────────────────────────────────────


def _print_header(cfg: HealthConfig) -> None:
    print("============================================================")
    print(f" PROXY CHAIN HEALTH CHECK  |  {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")
    print(f" Chain: FCC ({cfg.fcc_url}) -> routatic-proxy ({cfg.routatic_url}) -> opencode ({cfg.opencode_url})")
    print("============================================================")


def _print_human(results: list[HopResult]) -> None:
    for result in results:
        marker = "\033[0;32mPASS\033[0m" if result.ok else "\033[0;31mFAIL\033[0m"
        latency = f"{result.latency_ms}ms" if result.latency_ms is not None else "n/a"
        http = f"HTTP {result.http_code}" if result.http_code is not None else "HTTP ?"
        line = f"  {marker} {result.name} ({http}, {latency})"
        if result.meta:
            extras = []
            if "ttfb_ms" in result.meta:
                extras.append(f"ttfb={result.meta['ttfb_ms']}ms")
            if "models_served" in result.meta:
                extras.append(f"models={result.meta['models_served']}")
            if "models" in result.meta:
                extras.append(f"routed_models={','.join(result.meta['models'])}")
            if result.meta.get("circuit_breakers"):
                state = {k: v for k, v in result.meta["circuit_breakers"].items() if v == "open"}
                extras.append("breakers_open=" + (",".join(state) if state else "none"))
            if extras:
                line += "  [" + " ".join(extras) + "]"
        print(line)
        if not result.ok and result.detail:
            print(f"            detail: {result.detail}")


def _report(results: list[HopResult], as_json: bool) -> int:
    failed = [r for r in results if not r.ok]
    if as_json:
        for result in results:
            print(json.dumps(result.as_dict(), sort_keys=True))
        print(json.dumps({"overall": "healthy" if not failed else "degraded", "checks_failed": len(failed)}))
        return 0 if not failed else 1

    print()
    print("============================================================")
    if failed:
        print(f" RESULT: \033[0;31mDEGRADED\033[0m — {len(failed)} check(s) failed")
        return 1
    print(" RESULT: \033[0;32mHEALTHY\033[0m — all checks passed")
    return 0


# ── CLI ──────────────────────────────────────────────────────────────────


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m merged_agentic_swarm.health_check",
        description="Health check for the proxy chain: FCC -> routatic-proxy -> opencode.ai.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python -m merged_agentic_swarm.health_check             all checks
  python -m merged_agentic_swarm.health_check status      hop reachability + latency
  python -m merged_agentic_swarm.health_check stream      end-to-end streaming latency
  python -m merged_agentic_swarm.health_check providers   provider / circuit-breaker status
  python -m merged_agentic_swarm.health_check --json      machine-readable output

Env overrides: FCC_URL, ROUTATIC_URL, OPENCODE_URL, ANTHROPIC_AUTH_TOKEN,
E2E_MODEL, E2E_MAX_TOKENS, HEALTH_TIMEOUT, HEALTH_STREAM_TIMEOUT.""",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON results instead of a human report")
    sub = parser.add_subparsers(dest="command")

    p_status = sub.add_parser("status", help="Reachability + latency for every hop")
    p_status.set_defaults(func="status")

    p_stream = sub.add_parser("stream", help="End-to-end streaming latency")
    p_stream.add_argument(
        "--endpoint",
        choices=("fcc", "routatic"),
        default="fcc",
        help="Entry point for the streaming test (default: fcc, full chain)",
    )
    p_stream.add_argument("--model", default=None, help="Model alias to request")
    p_stream.add_argument(
        "--prompt", default=DEFAULT_PROMPT, help="Prompt text (default: 'Reply with the single word: OK')"
    )
    p_stream.add_argument("--max-tokens", type=int, default=None, help="max_tokens for the test request")
    p_stream.set_defaults(func="stream")

    p_providers = sub.add_parser("providers", help="Provider / circuit-breaker status")
    p_providers.set_defaults(func="providers")

    p_all = sub.add_parser("all", help="Run all checks (default)")
    p_all.set_defaults(func="all")
    return parser


async def _run_command(cmd: str, args: argparse.Namespace, cfg: HealthConfig) -> list[HopResult]:
    health = ProxyChainHealth(cfg)
    if cmd == "stream":
        return [
            await health.check_streaming(
                endpoint=args.endpoint, model=args.model, prompt=args.prompt, max_tokens=args.max_tokens
            )
        ]
    if cmd == "providers":
        return await health.check_providers()
    # status / all
    return await health.run_all(include_stream=(cmd == "all"))


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    cmd = args.command or "all"
    cfg = HealthConfig.from_env()

    results = asyncio.run(_run_command(cmd, args, cfg))
    if not args.json:
        _print_header(cfg)
        _print_human(results)
    return _report(results, as_json=args.json)


if __name__ == "__main__":
    sys.exit(main())
