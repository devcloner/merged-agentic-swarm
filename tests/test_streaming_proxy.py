"""Tests for ``merged_agentic_swarm.streaming_proxy``.

Covers the zero-buffering SSE passthrough path, circuit-breaker fail-fast
behavior (no retry loop), header allowlisting, connection pre-warming,
health checks, non-2xx error passthrough, mid-stream failure handling,
and client-disconnect cleanup.

The upstream is simulated with ``httpx.MockTransport`` whose handler
returns streaming ``httpx.Response`` objects backed by ``_ChunkStream``
(a subclass of ``httpx.AsyncByteStream``).  This keeps every test off the
network while still exercising the real httpx streaming machinery.
"""

import asyncio

import httpx
import pytest
from starlette.applications import Starlette
from starlette.requests import Request

from merged_agentic_swarm.streaming_proxy import (
    CircuitBreaker,
    PassthroughStreamingProxy,
    StreamingProxyConfig,
    create_streaming_proxy_app,
)

# ── Test-double helpers ────────────────────────────────────────────────────


class _ChunkStream(httpx.AsyncByteStream):
    """Async byte stream over a fixed list of chunks.

    Optionally raises ``exc`` after yielding every chunk, and invokes
    ``on_close`` when the response stream is closed.  ``closed`` is set by
    ``aclose()`` so tests can assert upstream teardown.
    """

    def __init__(self, chunks, *, exc=None, on_close=None):
        self._chunks = list(chunks)
        self._exc = exc
        self._on_close = on_close
        self.closed = False

    async def __aiter__(self):
        for chunk in self._chunks:
            yield chunk
        if self._exc is not None:
            raise self._exc

    async def aclose(self):
        self.closed = True
        if self._on_close is not None:
            self._on_close()


class _StallStream(httpx.AsyncByteStream):
    """Async byte stream that never yields (simulates a stalled upstream)."""

    def __init__(self):
        self.closed = False

    async def __aiter__(self):
        await asyncio.Event().wait()  # never set → each read stalls forever
        yield  # unreachable; the yield makes this an async generator

    async def aclose(self):
        self.closed = True


def _sse_response(chunks, *, request, status=200, headers=None, stream=None):
    """Build an upstream ``httpx.Response`` that streams ``chunks`` as SSE."""
    all_headers = {"content-type": "text/event-stream"}
    if headers:
        all_headers.update(headers)
    return httpx.Response(
        status,
        headers=all_headers,
        stream=stream or _ChunkStream(chunks),
        request=request,
    )


def make_proxy(handler, **config_kwargs):
    """Build a PassthroughStreamingProxy pointed at a MockTransport upstream."""
    config = StreamingProxyConfig(**config_kwargs)
    return PassthroughStreamingProxy(config, transport=httpx.MockTransport(handler))


def make_request(body):
    """Build a Starlette Request carrying an Anthropic Messages body."""
    scope = {
        "type": "http",
        "method": "POST",
        "path": "/v1/messages",
        "query_string": b"",
        "headers": [
            (b"content-type", b"application/json"),
            (b"x-api-key", b"test-key"),
            (b"anthropic-version", b"2023-06-01"),
            (b"x-custom-header", b"should-not-forward"),
        ],
        "http_version": "1.1",
        "scheme": "http",
        "client": ("127.0.0.1", 12345),
        "server": ("testserver", 80),
        "root_path": "",
        "state": {},
        "app": None,
    }

    async def receive():
        return {"type": "http.request", "body": body, "more_body": False}

    async def send(message):
        return None

    return Request(scope, receive=receive, send=send)


async def drain(response):
    """Consume (or close) a StreamingResponse so upstream streams are torn down."""
    gen = response.body_iterator
    async for _ in gen:
        pass
    await gen.aclose()


async def post(proxy, body=b'{"model":"opus","stream":true}'):
    """Send one proxied request and return the proxy's Response."""
    return await proxy.proxy_request(make_request(body))


# ── Zero-buffering passthrough ─────────────────────────────────────────────


@pytest.mark.asyncio
async def test_passthrough_preserves_bytes_and_headers():
    chunks = [
        b"event: message_start\n",
        b'data: {"type":"message_start","message":{"id":"m1"}}\n\n',
        b"event: content_block_delta\n",
        b'data: {"type":"content_block_delta","delta":{"text":"Hello"}}\n\n',
        b'data: {"type":"message_stop"}\n\n',
    ]

    def handler(request):
        return _sse_response(
            chunks,
            request=request,
            headers={"x-request-id": "req-123", "set-cookie": "session=secret"},
        )

    proxy = make_proxy(handler)
    app = proxy.as_asgi_app()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post(
            "/v1/messages",
            content=b'{"model":"opus","stream":true}',
            headers={"x-api-key": "k", "anthropic-version": "2023-06-01"},
        )
        assert resp.status_code == 200
        assert resp.headers["content-type"] == "text/event-stream"
        assert resp.headers["x-request-id"] == "req-123"
        assert "set-cookie" not in resp.headers  # not in the response allowlist
        assert resp.content == b"".join(chunks)  # byte-for-byte
    await proxy.close()


@pytest.mark.asyncio
async def test_zero_buffering_preserves_chunk_boundaries():
    """Each upstream network chunk must reach the client with identical
    boundaries — no ByteChunker aggregation, no decode, no re-encode."""
    chunks = [b"event: message_start\n", b'data: {"a":1}\n\n', b'data: {"b":2}\n\n']

    def handler(request):
        return _sse_response(chunks, request=request)

    proxy = make_proxy(handler)
    resp = await post(proxy)
    got = []
    async for chunk in resp.body_iterator:
        got.append(chunk)
    assert got == chunks  # boundaries preserved exactly
    await proxy.close()


@pytest.mark.asyncio
async def test_first_chunk_delivered_before_upstream_emits_rest():
    """Proves no-buffering: the first chunk is yielded the instant the
    upstream writes it, before any later bytes exist."""
    release = asyncio.Event()
    first_chunk = b"event: message_start\n"

    class GatedStream(_ChunkStream):
        async def __aiter__(self):
            yield first_chunk
            await release.wait()
            yield b'data: {"type":"done"}\n\n'

    def handler(request):
        return _sse_response([], request=request, stream=GatedStream([first_chunk]))

    proxy = make_proxy(handler)
    resp = await post(proxy)
    gen = resp.body_iterator
    got = await anext(gen)  # must return without waiting on release
    assert got == first_chunk
    release.set()
    await gen.aclose()
    await proxy.close()


# ── Circuit breaker: fail fast, no retry loop ──────────────────────────────


@pytest.mark.asyncio
async def test_connect_error_fails_fast_without_retry():
    calls = []

    def handler(request):
        calls.append(request)
        raise httpx.ConnectError("upstream down")

    proxy = make_proxy(handler)
    r1 = await post(proxy)
    r2 = await post(proxy)
    assert r1.status_code == 502
    assert r2.status_code == 502
    # Exactly one upstream attempt per request — no retry loop
    assert len(calls) == 2
    assert proxy.circuit_breaker.failure_count == 2
    await proxy.close()


@pytest.mark.asyncio
async def test_circuit_opens_and_rejects_with_503():
    calls = []

    def handler(request):
        calls.append(request)
        raise httpx.ConnectError("upstream down")

    proxy = make_proxy(handler, circuit_breaker_threshold=3)
    for _ in range(3):
        r = await post(proxy)
        assert r.status_code == 502
    assert proxy.circuit_breaker.is_open

    r4 = await post(proxy)
    assert r4.status_code == 503  # circuit open → immediate reject
    assert len(calls) == 3  # upstream never contacted while open
    await proxy.close()


@pytest.mark.asyncio
async def test_circuit_recovers_after_cooldown_half_open_probe():
    count = {"calls": 0}

    def handler(request):
        if count["calls"] < 2:
            count["calls"] += 1
            raise httpx.ConnectError("upstream down")
        count["calls"] += 1
        return _sse_response([b'data: {"ok":true}\n\n'], request=request)

    proxy = make_proxy(
        handler,
        circuit_breaker_threshold=2,
        circuit_breaker_cooldown_seconds=0.05,
    )
    assert (await post(proxy)).status_code == 502  # failure 1
    assert (await post(proxy)).status_code == 502  # failure 2 → circuit opens
    assert (await post(proxy)).status_code == 503  # open, rejected
    assert count["calls"] == 2

    await asyncio.sleep(0.08)  # cooldown elapses
    r = await post(proxy)  # half-open probe → success resets the counter
    assert r.status_code == 200
    assert proxy.circuit_breaker.failure_count == 0
    assert count["calls"] == 3
    await proxy.close()


@pytest.mark.asyncio
async def test_success_resets_failure_counter():
    count = {"calls": 0}

    def handler(request):
        if count["calls"] == 0:
            count["calls"] += 1
            raise httpx.ConnectError("upstream down")
        count["calls"] += 1
        return _sse_response([b'data: {"ok":true}\n\n'], request=request)

    proxy = make_proxy(handler)
    assert (await post(proxy)).status_code == 502
    assert proxy.circuit_breaker.failure_count == 1
    r2 = await post(proxy)
    assert r2.status_code == 200
    assert proxy.circuit_breaker.failure_count == 0
    await proxy.close()


@pytest.mark.asyncio
async def test_circuit_breaker_unit_transitions():
    cb = CircuitBreaker(threshold=3, cooldown_seconds=10.0)
    assert not cb.is_open
    await cb.record_failure()
    await cb.record_failure()
    assert not cb.is_open
    assert cb.failure_count == 2
    await cb.record_failure()
    assert cb.is_open
    await cb.record_success()
    assert not cb.is_open
    assert cb.failure_count == 0


# ── Non-2xx upstream handling ──────────────────────────────────────────────


@pytest.mark.asyncio
async def test_non_2xx_upstream_body_passthrough_and_failure_recorded():
    error_body = b'{"error":{"type":"rate_limit_error","message":"slow down"}}'

    def handler(request):
        return httpx.Response(
            429,
            headers={"content-type": "application/json", "x-request-id": "e-1"},
            content=error_body,
            request=request,
        )

    proxy = make_proxy(handler)
    resp = await post(proxy)
    assert resp.status_code == 429
    assert resp.body == error_body
    assert resp.headers["content-type"] == "application/json"
    assert proxy.circuit_breaker.failure_count == 1
    await proxy.close()


# ── Header allowlisting ────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_request_headers_allowlisted_and_defaults():
    seen = {}

    def handler(request):
        seen.update(
            {
                "content-type": request.headers.get("content-type"),
                "x-api-key": request.headers.get("x-api-key"),
                "anthropic-version": request.headers.get("anthropic-version"),
                "x-custom-header": request.headers.get("x-custom-header"),
                "accept-encoding": request.headers.get("accept-encoding"),
            }
        )
        return _sse_response([b"data: {}"], request=request)

    proxy = make_proxy(handler)
    resp = await post(proxy)
    await drain(resp)
    assert resp.status_code == 200
    # Allowlisted headers forwarded verbatim
    assert seen["x-api-key"] == "test-key"
    assert seen["anthropic-version"] == "2023-06-01"
    assert seen["content-type"] == "application/json"
    # Non-allowlisted header dropped
    assert seen["x-custom-header"] is None
    # Default identity encoding added so upstream cannot gzip the SSE stream
    assert seen["accept-encoding"] == "identity"
    await proxy.close()


# ── Mid-stream failure and client disconnect ───────────────────────────────


@pytest.mark.asyncio
async def test_mid_stream_failure_stops_gracefully_and_closes_upstream():
    holder = {}

    def handler(request):
        stream = _ChunkStream([b"event: a\n\n", b"event: b\n\n"], exc=httpx.ReadError("conn dropped"))
        holder["stream"] = stream
        return _sse_response([], request=request, stream=stream)

    proxy = make_proxy(handler)
    resp = await post(proxy)
    gen = resp.body_iterator
    assert await anext(gen) == b"event: a\n\n"
    assert await anext(gen) == b"event: b\n\n"
    # The read error is swallowed at the proxy boundary → stream just ends,
    # but the mid-stream transport drop is counted against the breaker.
    with pytest.raises(StopAsyncIteration):
        await anext(gen)
    assert holder["stream"].closed is True
    assert proxy.circuit_breaker.failure_count == 1
    await proxy.close()


@pytest.mark.asyncio
async def test_stalled_upstream_times_out_and_records_failure():
    """#39: an upstream that stalls mid-stream must not hang the client forever."""
    holder = {}

    def handler(request):
        stream = _StallStream()
        holder["stream"] = stream
        return _sse_response([], request=request, stream=stream)

    proxy = make_proxy(handler, stream_idle_timeout_seconds=0.05)
    resp = await post(proxy)
    gen = resp.body_iterator
    with pytest.raises(StopAsyncIteration):
        await anext(gen)
    assert holder["stream"].closed is True
    assert proxy.circuit_breaker.failure_count == 1
    await proxy.close()


@pytest.mark.asyncio
async def test_client_disconnect_closes_upstream():
    closed = []

    def handler(request):
        stream = _ChunkStream([b"event: a\n\n", b"event: b\n\n"], on_close=lambda: closed.append(True))
        return _sse_response([], request=request, stream=stream)

    proxy = make_proxy(handler)
    resp = await post(proxy)
    gen = resp.body_iterator
    assert await anext(gen) == b"event: a\n\n"
    # Client hangs up mid-stream → generator aborted → upstream released
    await gen.aclose()
    assert closed == [True]
    await proxy.close()


# ── Pre-warming and health ─────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_prewarm_true_on_healthy_upstream():
    def handler(request):
        return httpx.Response(200, content=b'{"status":"ok"}', request=request)

    proxy = make_proxy(handler)
    assert await proxy.prewarm() is True
    await proxy.close()


@pytest.mark.asyncio
async def test_prewarm_false_when_upstream_degraded_or_down():
    def handler(request):
        raise httpx.ConnectError("down")

    proxy = make_proxy(handler)
    assert await proxy.prewarm() is False
    await proxy.close()

    def degraded(request):
        return httpx.Response(503, content=b"unavailable", request=request)

    proxy2 = make_proxy(degraded)
    assert await proxy2.prewarm() is False
    await proxy2.close()


@pytest.mark.asyncio
async def test_health_endpoint_ok():
    def handler(request):
        return httpx.Response(200, content=b'{"status":"ok"}', request=request)

    proxy = make_proxy(handler)
    app = proxy.as_asgi_app()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"
        assert resp.json()["circuit_open"] is False
    await proxy.close()


@pytest.mark.asyncio
async def test_health_endpoint_503_when_upstream_down():
    def handler(request):
        raise httpx.ConnectError("down")

    proxy = make_proxy(handler)
    app = proxy.as_asgi_app()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/health")
        assert resp.status_code == 503
        assert resp.json()["status"] == "error"
    await proxy.close()


# ── Drop-in ASGI composition ───────────────────────────────────────────────


@pytest.mark.asyncio
async def test_drop_in_asgi_app_handles_messages_endpoint():
    def handler(request):
        return _sse_response([b'data: {"ok":true}\n\n'], request=request)

    proxy = make_proxy(handler)
    app = proxy.as_asgi_app()
    assert isinstance(app, Starlette)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post(
            "/v1/messages/",
            content=b'{"model":"sonnet","stream":true}',
            headers={"x-api-key": "k"},
        )
        assert resp.status_code == 200
        assert resp.content == b'data: {"ok":true}\n\n'
    await proxy.close()


@pytest.mark.asyncio
async def test_connection_reuse_single_pooled_client():
    """All requests share one httpx.AsyncClient (connection pooling)."""
    calls = []

    def handler(request):
        calls.append(request)
        return _sse_response([b'data: {"ok":true}\n\n'], request=request)

    proxy = make_proxy(handler)
    client = await proxy._get_client()
    for _ in range(3):
        resp = await post(proxy)
        await drain(resp)
    assert (await proxy._get_client()) is client  # same pooled client
    assert len(calls) == 3
    await proxy.close()


def test_create_streaming_proxy_app_factory():
    app = create_streaming_proxy_app(upstream_url="http://example.test", circuit_breaker_threshold=7)
    assert isinstance(app, Starlette)


def test_config_defaults():
    cfg = StreamingProxyConfig()
    assert cfg.upstream_url == "http://127.0.0.1:3456"
    assert cfg.upstream_messages_path == "/v1/messages"
    assert cfg.health_check_path == "/health"
    assert cfg.circuit_breaker_threshold == 5
    assert "x-api-key" in cfg.request_headers_allowlist
    assert "x-request-id" in cfg.response_headers_allowlist
