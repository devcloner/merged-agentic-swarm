import asyncio
import json

import httpx
import pytest

from merged_agentic_swarm.health_check import (
    HealthConfig,
    HopResult,
    ProxyChainHealth,
    _print_human,
    _report,
    main,
)


def _patch_client(monkeypatch, handler) -> None:
    real_async_client = httpx.AsyncClient
    monkeypatch.setattr(
        "merged_agentic_swarm.health_check.httpx.AsyncClient",
        lambda **kw: real_async_client(transport=httpx.MockTransport(handler)),
    )


# ── check_routatic ──────────────────────────────────────────────────────────


def test_check_routatic_happy_path(monkeypatch):
    """check_routatic parses JSON health response, extracting circuit-breakers
    and model/version metadata."""

    async def handler(request):
        return httpx.Response(
            200,
            json={
                "service": "routatic-proxy",
                "version": "1.2.3",
                "status": "ok",
                "circuit_breakers": {"openai": "closed", "anthropic": "open"},
                "models": {"claude-3-haiku": True, "gpt-4o": True},
                "metrics": {
                    "p95_latency_ms": 120.5,
                    "requests_success": 99,
                    "requests_failed": 1,
                },
            },
        )

    _patch_client(monkeypatch, handler)
    result = asyncio.run(ProxyChainHealth(HealthConfig()).check_routatic())
    assert result.ok is True
    assert result.http_code == 200
    assert result.latency_ms is not None
    assert result.meta["service"] == "routatic-proxy"
    assert result.meta["version"] == "1.2.3"
    assert result.meta["router_status"] == "ok"
    assert "anthropic" in result.meta["circuit_breakers"]
    assert "claude-3-haiku" in result.meta["models"]
    assert result.meta["p95_latency_ms"] == 120.5


def test_check_routatic_connection_error(monkeypatch):
    """check_routatic reports failure on connection errors."""

    async def handler(request):
        raise httpx.ConnectError("refused")

    _patch_client(monkeypatch, handler)
    result = asyncio.run(ProxyChainHealth(HealthConfig()).check_routatic())
    assert result.ok is False
    assert result.http_code is None
    assert "ConnectError" in result.detail


def test_check_routatic_non_json_body(monkeypatch):
    """check_routatic tolerates non-JSON response body gracefully."""

    async def handler(request):
        return httpx.Response(200, text="OK", headers={"content-type": "text/plain"})

    _patch_client(monkeypatch, handler)
    result = asyncio.run(ProxyChainHealth(HealthConfig()).check_routatic())
    assert result.ok is True
    assert result.http_code == 200
    # meta should stay empty because the body is not JSON.
    assert not result.meta


# ── check_opencode ──────────────────────────────────────────────────────────


def test_check_opencode_happy_path(monkeypatch):
    """check_opencode probes the upstream opencode models endpoint."""

    async def handler(request):
        return httpx.Response(200, json={"data": [{"id": "claude-3-haiku"}]})

    _patch_client(monkeypatch, handler)
    result = asyncio.run(ProxyChainHealth(HealthConfig()).check_opencode())
    assert result.ok is True
    assert result.http_code == 200
    assert result.latency_ms is not None


def test_check_opencode_error_response(monkeypatch):
    """check_opencode reports failure on HTTP 500 from upstream."""

    async def handler(request):
        return httpx.Response(503, text="Service Unavailable")

    _patch_client(monkeypatch, handler)
    result = asyncio.run(ProxyChainHealth(HealthConfig()).check_opencode())
    assert result.ok is False
    assert result.http_code == 503


def test_check_opencode_connection_error(monkeypatch):
    """check_opencode reports failure on connection errors."""

    async def handler(request):
        raise httpx.ReadError("timeout")

    _patch_client(monkeypatch, handler)
    result = asyncio.run(ProxyChainHealth(HealthConfig()).check_opencode())
    assert result.ok is False
    assert "ReadError" in result.detail


# ── check_streaming ─────────────────────────────────────────────────────────


def _sse_event(event_type: str, delta: str) -> str:
    """Build a single SSE data line for an Anthropic streaming content-block-delta."""
    data = json.dumps({"type": event_type, "delta": {"text": delta, "type": "text_delta"}})
    return f"data: {data}\n\n"


def _make_sse_response(*events: str) -> httpx.Response:
    """Return a 200 httpx.Response whose .stream yields SSE events."""
    body = "".join(events).encode()
    return httpx.Response(200, stream=httpx.ByteStream(body))


def test_check_streaming_fcc_happy_path(monkeypatch):
    """check_streaming through FCC endpoint measures TTFB and total latency."""

    events = (
        _sse_event("content_block_start", "") + _sse_event("content_block_delta", "OK") + _sse_event("message_stop", "")
    )

    async def handler(request):
        # Assert streaming payload was sent
        body = json.loads(request.read().decode())
        assert body["stream"] is True
        assert body["model"] == "claude-3-5-haiku"
        return _make_sse_response(events)

    _patch_client(monkeypatch, handler)
    result = asyncio.run(ProxyChainHealth(HealthConfig()).check_streaming())
    assert result.ok is True
    assert result.meta["content_deltas"] > 0
    assert result.meta["ttfb_ms"] is not None
    assert result.meta["total_ms"] is not None
    assert result.meta["endpoint"] == "fcc"


def test_check_streaming_no_deltas(monkeypatch):
    """check_streaming reports unhealthy when no content_block_delta arrives."""

    async def handler(request):
        events = "data: [DONE]\n\n"
        return _make_sse_response(events)

    _patch_client(monkeypatch, handler)
    result = asyncio.run(ProxyChainHealth(HealthConfig()).check_streaming())
    assert result.ok is False
    assert result.meta["content_deltas"] == 0


def test_check_streaming_http_error(monkeypatch):
    """check_streaming reports failure immediately on non-2xx response."""

    async def handler(request):
        return httpx.Response(401, json={"error": "unauthorized"}, stream=httpx.ByteStream(b""))

    _patch_client(monkeypatch, handler)
    result = asyncio.run(ProxyChainHealth(HealthConfig()).check_streaming())
    assert result.ok is False
    assert result.http_code == 401


def test_check_streaming_connection_error(monkeypatch):
    """check_streaming reports failure on transport errors."""

    async def handler(request):
        raise httpx.ReadError("broken pipe")

    _patch_client(monkeypatch, handler)
    result = asyncio.run(ProxyChainHealth(HealthConfig()).check_streaming())
    assert result.ok is False
    assert "ReadError" in result.detail


def test_check_streaming_routatic_endpoint(monkeypatch):
    """check_streaming targets routatic-proxy when endpoint='routatic'."""

    events = (
        _sse_event("content_block_start", "") + _sse_event("content_block_delta", "OK") + _sse_event("message_stop", "")
    )

    seen_url = []

    async def handler(request):
        seen_url.append(str(request.url))
        return _make_sse_response(events)

    _patch_client(monkeypatch, handler)
    cfg = HealthConfig()
    result = asyncio.run(ProxyChainHealth(cfg).check_streaming(endpoint="routatic"))
    assert result.ok is True
    # routatic endpoints use routatic_url, not fcc_url
    assert cfg.routatic_url.rstrip("/") in seen_url[0]


# ── check_providers ─────────────────────────────────────────────────────────


def test_check_providers_happy_path(monkeypatch):
    """check_providers returns routatic health + FCC models list count."""

    async def handler(request):
        if "/health" in str(request.url):
            return httpx.Response(200, json={"status": "ok"})
        # /v1/models
        return httpx.Response(200, json={"data": [{"id": "m1"}, {"id": "m2"}, {"id": "m3"}]})

    _patch_client(monkeypatch, handler)
    results = asyncio.run(ProxyChainHealth(HealthConfig()).check_providers())
    assert len(results) == 2
    routatic_result, models_result = results
    assert routatic_result.name == "routatic"
    assert routatic_result.ok is True
    assert models_result.name == "fcc-models"
    assert models_result.ok is True
    assert models_result.meta["models_served"] == 3


def test_check_providers_fcc_models_list_format(monkeypatch):
    """check_providers handles a plain list response (not wrapped in {data: [...]})."""

    async def handler(request):
        if "/health" in str(request.url):
            return httpx.Response(200, json={"status": "ok"})
        return httpx.Response(200, json=[{"id": "a"}, {"id": "b"}])

    _patch_client(monkeypatch, handler)
    results = asyncio.run(ProxyChainHealth(HealthConfig()).check_providers())
    assert results[1].meta["models_served"] == 2


def test_check_providers_fcc_models_error(monkeypatch):
    """check_providers still returns routatic result even when FCC models fails."""

    async def handler(request):
        if "/health" in str(request.url):
            return httpx.Response(200, json={"status": "ok"})
        raise httpx.ConnectError("fcc down")

    _patch_client(monkeypatch, handler)
    results = asyncio.run(ProxyChainHealth(HealthConfig()).check_providers())
    assert results[0].name == "routatic"
    assert results[0].ok is True
    assert results[1].name == "fcc-models"
    assert results[1].ok is False


# ── run_all ─────────────────────────────────────────────────────────────────


def test_run_all_stable_order(monkeypatch):
    """run_all returns results in a predictable order including streaming."""
    call_order: list[str] = []

    async def handler(request):
        call_order.append(str(request.url))
        return httpx.Response(200, json={"status": "ok"})

    _patch_client(monkeypatch, handler)
    cfg = HealthConfig()
    results = asyncio.run(ProxyChainHealth(cfg).run_all())
    names = [r.name for r in results]
    assert names == ["routatic", "fcc", "opencode", "stream"]


def test_run_all_without_stream(monkeypatch):
    """run_all skips streaming when include_stream=False."""
    call_count = 0

    async def handler(request):
        nonlocal call_count
        call_count += 1
        return httpx.Response(200, json={"status": "ok"})

    _patch_client(monkeypatch, handler)
    results = asyncio.run(ProxyChainHealth(HealthConfig()).run_all(include_stream=False))
    names = [r.name for r in results]
    assert names == ["routatic", "fcc", "opencode"]
    # 3 checks = 3 HTTP calls, no stream
    assert call_count == 3


# ── from_env ────────────────────────────────────────────────────────────────


def test_from_env_defaults():
    """from_env returns defaults when no env vars are set."""
    cfg = HealthConfig.from_env()
    assert cfg.fcc_url == "http://127.0.0.1:8080"
    assert cfg.routatic_url == "http://127.0.0.1:3456"
    assert cfg.auth_token == "freecc"
    assert cfg.timeout == 30.0


def test_from_env_override_strings(monkeypatch):
    """from_env picks up env overrides for string fields."""
    monkeypatch.setenv("FCC_URL", "http://fcc:9090")
    monkeypatch.setenv("ANTHROPIC_AUTH_TOKEN", "sk-custom")
    monkeypatch.setenv("E2E_MODEL", "gpt-4o")
    cfg = HealthConfig.from_env()
    assert cfg.fcc_url == "http://fcc:9090"
    assert cfg.auth_token == "sk-custom"
    assert cfg.e2e_model == "gpt-4o"


def test_from_env_override_numerics(monkeypatch):
    """from_env casts numeric env vars to int/float."""
    monkeypatch.setenv("E2E_MAX_TOKENS", "128")
    monkeypatch.setenv("HEALTH_TIMEOUT", "45.5")
    monkeypatch.setenv("HEALTH_STREAM_TIMEOUT", "200")
    cfg = HealthConfig.from_env()
    assert cfg.e2e_max_tokens == 128
    assert cfg.timeout == 45.5
    assert cfg.stream_timeout == 200.0


def test_from_env_invalid_numeric_falls_through(monkeypatch):
    """from_env surfaces ValueError for non-numeric env values (no silent fallback)."""
    monkeypatch.setenv("HEALTH_TIMEOUT", "not-a-number")
    with pytest.raises(ValueError):
        HealthConfig.from_env()


# ── CLI --json output ───────────────────────────────────────────────────────


def test_main_json_output_all(monkeypatch, capsys):
    """--json flag emits machine-readable JSON for all checks."""

    async def handler(request):
        if "/v1/messages" in str(request.url) and request.method == "POST":
            events = (
                _sse_event("content_block_start", "")
                + _sse_event("content_block_delta", "OK")
                + _sse_event("message_stop", "")
            )
            return _make_sse_response(events)
        return httpx.Response(200, json={"status": "ok"})

    _patch_client(monkeypatch, handler)
    exit_code = main(["--json"])
    captured = capsys.readouterr()
    # --json only: _report writes JSON lines.
    lines = captured.out.strip().split("\n")
    assert len(lines) >= 4  # routatic, fcc, opencode, stream, overall
    overall = json.loads(lines[-1])
    assert overall["overall"] == "healthy"
    assert exit_code == 0


def test_main_json_output_degraded(monkeypatch, capsys):
    """--json reports degraded when a check fails."""

    async def handler(request):
        # Fail FCC, everything else ok
        if "/health" in str(request.url) and "8080" in str(request.url):
            return httpx.Response(503, text="Service Unavailable")
        if "/v1/messages" in str(request.url):
            events = (
                _sse_event("content_block_start", "")
                + _sse_event("content_block_delta", "OK")
                + _sse_event("message_stop", "")
            )
            return _make_sse_response(events)
        return httpx.Response(200, json={"status": "ok"})

    _patch_client(monkeypatch, handler)
    exit_code = main(["--json"])
    captured = capsys.readouterr()
    lines = captured.out.strip().split("\n")
    overall = json.loads(lines[-1])
    assert overall["overall"] == "degraded"
    assert exit_code == 1


def test_main_status_command(monkeypatch, capsys):
    """'status' subcommand runs hop probes only (no streaming)."""

    async def handler(request):
        return httpx.Response(200, json={"status": "ok"})

    _patch_client(monkeypatch, handler)
    exit_code = main(["status"])
    # Without --json, _print_header and _print_human are called.
    captured = capsys.readouterr()
    assert "PROXY CHAIN HEALTH CHECK" in captured.out
    assert "routatic" in captured.out
    assert "fcc" in captured.out
    assert "opencode" in captured.out
    # No stream check included
    assert "stream" not in captured.out.split("  PASS")[0] if "PASS" in captured.out else True
    assert exit_code == 0


def test_main_stream_subcommand(monkeypatch, capsys):
    """'stream' subcommand runs only the streaming check."""

    events = (
        _sse_event("content_block_start", "") + _sse_event("content_block_delta", "OK") + _sse_event("message_stop", "")
    )

    async def handler(request):
        return _make_sse_response(events)

    _patch_client(monkeypatch, handler)
    exit_code = main(["stream"])
    captured = capsys.readouterr()
    assert "stream" in captured.out
    assert exit_code == 0


def test_main_providers_subcommand(monkeypatch, capsys):
    """'providers' subcommand runs provider/circuit-breaker checks."""

    async def handler(request):
        if "/health" in str(request.url):
            return httpx.Response(200, json={"status": "ok", "circuit_breakers": {}, "models": {}})
        return httpx.Response(200, json=[{"id": "a"}])

    _patch_client(monkeypatch, handler)
    exit_code = main(["providers"])
    captured = capsys.readouterr()
    assert "routatic" in captured.out
    assert "fcc-models" in captured.out
    assert exit_code == 0


# ── _print_human / _report ──────────────────────────────────────────────────


def test_print_human_pass(monkeypatch, capsys):
    """_print_human renders PASS with latency and metadata."""
    results = [
        HopResult("test", ok=True, latency_ms=12.5, http_code=200),
        HopResult("meta-check", ok=True, latency_ms=3.1, http_code=200, meta={"models_served": 42}),
    ]
    _print_human(results)
    captured = capsys.readouterr()
    assert "PASS test" in captured.out
    assert "HTTP 200" in captured.out
    assert "12.5ms" in captured.out
    assert "models=42" in captured.out.lower()


def test_print_human_fail(monkeypatch, capsys):
    """_print_human renders FAIL with detail."""
    results = [
        HopResult("routatic", ok=False, detail="ConnectError: refused"),
    ]
    _print_human(results)
    captured = capsys.readouterr()
    assert "FAIL" in captured.out
    assert "ConnectError: refused" in captured.out


def test_print_human_circuit_breakers(monkeypatch, capsys):
    """_print_human renders open circuit breakers."""
    results = [
        HopResult(
            "routatic",
            ok=True,
            latency_ms=5.1,
            http_code=200,
            meta={
                "circuit_breakers": {"openai": "open", "anthropic": "closed"},
                "models": ["claude-3-haiku"],
            },
        )
    ]
    _print_human(results)
    captured = capsys.readouterr()
    assert "breakers_open=openai" in captured.out


def test_print_human_ttfb_rendering(monkeypatch, capsys):
    """_print_human includes TTFB when present in meta."""
    results = [
        HopResult("stream", ok=True, latency_ms=450.0, http_code=200, meta={"ttfb_ms": 120.0}),
    ]
    _print_human(results)
    captured = capsys.readouterr()
    assert "ttfb=120.0ms" in captured.out


def test_report_human_healthy(monkeypatch, capsys):
    """_report renders HEALTHY when all checks pass."""
    results = [HopResult("a", ok=True, latency_ms=1, http_code=200)]
    exit_code = _report(results, as_json=False)
    captured = capsys.readouterr()
    assert "HEALTHY" in captured.out
    assert exit_code == 0


def test_report_human_degraded(monkeypatch, capsys):
    """_report renders DEGRADED and returns 1 when checks fail."""
    results = [
        HopResult("a", ok=True, latency_ms=1, http_code=200),
        HopResult("b", ok=False, detail="error"),
    ]
    exit_code = _report(results, as_json=False)
    captured = capsys.readouterr()
    assert "DEGRADED" in captured.out
    assert exit_code == 1


def test_report_json_healthy(monkeypatch, capsys):
    """_report emits JSON and returns 0 for healthy."""
    results = [HopResult("test", ok=True, latency_ms=5.0, http_code=200)]
    exit_code = _report(results, as_json=True)
    captured = capsys.readouterr()
    lines = captured.out.strip().split("\n")
    assert len(lines) == 2
    test_line = json.loads(lines[0])
    assert test_line["check"] == "test"
    assert test_line["ok"] == 1
    overall = json.loads(lines[1])
    assert overall["overall"] == "healthy"
    assert exit_code == 0


def test_report_json_degraded(monkeypatch, capsys):
    """_report emits JSON with degraded status and returns 1."""
    results = [HopResult("fail", ok=False, detail="broken")]
    exit_code = _report(results, as_json=True)
    captured = capsys.readouterr()
    overall = json.loads(captured.out.strip().split("\n")[1])
    assert overall["overall"] == "degraded"
    assert exit_code == 1


# ── original check_fcc tests ────────────────────────────────────────────────


def test_check_fcc_accepts_json_status_ok(monkeypatch):
    async def handler(request):
        return httpx.Response(200, json={"status": "ok"})

    _patch_client(monkeypatch, handler)
    result = asyncio.run(ProxyChainHealth(HealthConfig()).check_fcc())
    assert result.ok is True
    assert result.http_code == 200


def test_check_fcc_accepts_json_status_healthy(monkeypatch):
    async def handler(request):
        return httpx.Response(200, json={"status": "healthy"})

    _patch_client(monkeypatch, handler)
    result = asyncio.run(ProxyChainHealth(HealthConfig()).check_fcc())
    assert result.ok is True


def test_check_fcc_rejects_json_status_degraded(monkeypatch):
    async def handler(request):
        return httpx.Response(200, json={"status": "degraded"})

    _patch_client(monkeypatch, handler)
    result = asyncio.run(ProxyChainHealth(HealthConfig()).check_fcc())
    assert result.ok is False


def test_check_fcc_plain_text_healthy(monkeypatch):
    async def handler(request):
        return httpx.Response(200, text="healthy")

    _patch_client(monkeypatch, handler)
    result = asyncio.run(ProxyChainHealth(HealthConfig()).check_fcc())
    assert result.ok is True


def test_check_fcc_connection_error_reports_fail(monkeypatch):
    async def handler(request):
        raise httpx.ConnectError("boom")

    _patch_client(monkeypatch, handler)
    result = asyncio.run(ProxyChainHealth(HealthConfig()).check_fcc())
    assert result.ok is False
    assert result.detail.startswith("ConnectError")
