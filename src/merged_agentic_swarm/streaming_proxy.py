"""
Zero-buffering streaming passthrough proxy for Anthropic Messages API.

Accepts streaming /v1/messages requests, forwards them to an upstream
Anthropic-compatible endpoint via httpx streaming, and passes raw SSE
bytes back to the client with no transformation, aggregation, or
buffering beyond what the OS/httpx transport layer requires.

Streaming path: the upstream response is iterated with ``aiter_raw()``
(chunk_size=None), which yields each network chunk immediately.  This is
deliberate — httpx's ``aiter_bytes()``/``aiter_raw(chunk_size=...)`` route
through a ``ByteChunker`` that aggregates chunks up to the requested size,
which would introduce SSE event latency.  ``aiter_raw()`` passes bytes
through untouched (no decode, no re-chunking), so SSE events reach the
client as fast as the transport delivers them.

Design goals:
  - Zero-copy byte forwarding: raw bytes chunks pass through untouched
  - Circuit breaker: fail fast when upstream is unhealthy (no retry loop)
  - Connection pre-warming for first-request latency reduction
  - Drop-in: usable as a standalone Starlette ASGI app or as a
    component mounted into a larger application.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass, field

import httpx
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response, StreamingResponse
from starlette.routing import Route

logger = logging.getLogger("streaming_proxy")

# ── Configuration ──────────────────────────────────────────────────────────


@dataclass
class StreamingProxyConfig:
    """Configuration for the zero-buffering streaming proxy."""

    upstream_url: str = "http://127.0.0.1:3456"
    """Base URL of the upstream Anthropic-compatible API."""

    upstream_messages_path: str = "/v1/messages"
    """Path appended to upstream_url for messages endpoint."""

    health_check_path: str = "/health"
    """Path appended to upstream_url for health checks."""

    prewarm: bool = True
    """Whether to pre-warm the connection pool on startup."""

    circuit_breaker_threshold: int = 5
    """Number of consecutive upstream failures before circuit opens."""

    circuit_breaker_cooldown_seconds: float = 30.0
    """Seconds to wait before testing the circuit after it opens."""

    connect_timeout: float = 5.0
    """Timeout for establishing TCP connections (seconds)."""

    read_timeout: float = 120.0
    """Timeout for reading the first upstream byte after connect (seconds)."""

    pool_max_connections: int = 20
    """Maximum connections in the httpx connection pool."""

    pool_max_keepalive: int = 10
    """Maximum keep-alive connections to retain."""

    request_headers_allowlist: frozenset[str] = field(
        default_factory=lambda: frozenset(
            {
                "content-type",
                "x-api-key",
                "anthropic-version",
                "anthropic-beta",
                "authorization",
            }
        )
    )
    """Headers forwarded from the client request to upstream."""

    response_headers_allowlist: frozenset[str] = field(
        default_factory=lambda: frozenset(
            {
                "content-type",
                "x-request-id",
                "request-id",
            }
        )
    )
    """Headers forwarded from the upstream response to the client."""


# ── Circuit Breaker ────────────────────────────────────────────────────────


class CircuitBreaker:
    """Simple fail-fast circuit breaker.

    Tracks consecutive failures.  After *threshold* consecutive failures
    the circuit opens and all requests are rejected immediately for
    *cooldown_seconds*.  A single successful request resets the counter.
    """

    def __init__(self, threshold: int = 5, cooldown_seconds: float = 30.0) -> None:
        self._threshold = threshold
        self._cooldown = cooldown_seconds
        self._failures: int = 0
        self._opened_at: float = 0.0
        self._lock = asyncio.Lock()

    @property
    def is_open(self) -> bool:
        """True when the circuit is open (requests should be rejected)."""
        if self._failures < self._threshold:
            return False
        elapsed = time.monotonic() - self._opened_at
        if elapsed >= self._cooldown:
            # Allow one probe request through
            self._failures = self._threshold - 1
            return False
        return True

    @property
    def failure_count(self) -> int:
        """Current consecutive failure count."""
        return self._failures

    async def record_success(self) -> None:
        """Reset the failure counter after a successful request."""
        async with self._lock:
            self._failures = 0

    async def record_failure(self) -> None:
        """Increment the failure counter; open circuit if threshold reached."""
        async with self._lock:
            self._failures += 1
            if self._failures >= self._threshold:
                self._opened_at = time.monotonic()


# ── Streaming Proxy ────────────────────────────────────────────────────────


class PassthroughStreamingProxy:
    """Zero-buffering SSE passthrough proxy.

    Accepts Anthropic Messages API streaming requests at ``/v1/messages``,
    forwards them to an upstream with httpx streaming, and passes raw
    SSE bytes back to the client without transformation.

    Usage as a standalone ASGI app::

        config = StreamingProxyConfig(upstream_url="http://127.0.0.1:3456")
        proxy = PassthroughStreamingProxy(config)
        app = proxy.as_asgi_app()
        uvicorn.run(app, host="0.0.0.0", port=8080)

    Usage as a component::

        proxy = PassthroughStreamingProxy(config)
        await proxy.prewarm()
        # ... mount proxy.router into a larger Starlette app
    """

    def __init__(
        self,
        config: StreamingProxyConfig | None = None,
        *,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self.config = config or StreamingProxyConfig()
        self.circuit_breaker = CircuitBreaker(
            threshold=self.config.circuit_breaker_threshold,
            cooldown_seconds=self.config.circuit_breaker_cooldown_seconds,
        )
        self._transport = transport
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Return the shared httpx client, creating it if needed."""
        if self._client is None:
            limits = httpx.Limits(
                max_connections=self.config.pool_max_connections,
                max_keepalive_connections=self.config.pool_max_keepalive,
            )
            timeout = httpx.Timeout(
                connect=self.config.connect_timeout,
                read=self.config.read_timeout,
                write=30.0,
                pool=5.0,
            )
            self._client = httpx.AsyncClient(
                transport=self._transport,
                limits=limits,
                timeout=timeout,
                http2=False,
                follow_redirects=False,
            )
        return self._client

    async def close(self) -> None:
        """Close the underlying httpx client and release connections."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    # ── Pre-warming ───────────────────────────────────────────────────

    async def prewarm(self) -> bool:
        """Pre-establish connections to the upstream.

        Sends a health-check request to warm the connection pool so the
        first real request does not pay the TCP/TLS handshake cost.

        Returns True if pre-warming succeeded.
        """
        try:
            client = await self._get_client()
            url = f"{self.config.upstream_url.rstrip('/')}{self.config.health_check_path}"
            resp = await client.get(url)
            status = resp.status_code
            await resp.aclose()
            logger.info("Streaming proxy pre-warmed to %s [%s]", url, status)
            return status < 500
        except Exception:
            logger.warning("Streaming proxy pre-warm failed (upstream may be starting)")
            return False

    # ── Health ────────────────────────────────────────────────────────

    async def health(self) -> dict:
        """Check upstream health.  Returns a status dict."""
        try:
            client = await self._get_client()
            url = f"{self.config.upstream_url.rstrip('/')}{self.config.health_check_path}"
            resp = await client.get(url)
            body = None
            try:
                body = resp.json()
            except Exception:
                body = resp.text
            await resp.aclose()
            return {
                "status": "ok" if resp.status_code < 500 else "degraded",
                "upstream_status": resp.status_code,
                "upstream_body": body,
                "circuit_open": self.circuit_breaker.is_open,
                "circuit_failures": self.circuit_breaker.failure_count,
            }
        except Exception as exc:
            return {
                "status": "error",
                "error": str(exc),
                "circuit_open": self.circuit_breaker.is_open,
                "circuit_failures": self.circuit_breaker.failure_count,
            }

    # ── Request forwarding ────────────────────────────────────────────

    async def proxy_request(self, request: Request) -> Response:
        """Forward an incoming streaming request to upstream.

        Reads the request body, forwards headers, and streams the
        upstream SSE response bytes directly back to the client with
        no buffering or transformation.
        """
        # Circuit breaker gate — fail fast, no retry loop
        if self.circuit_breaker.is_open:
            return Response(
                content='{"error":{"type":"service_unavailable","message":"Circuit breaker open"}}',
                status_code=503,
                media_type="application/json",
            )

        client = await self._get_client()
        upstream_url = f"{self.config.upstream_url.rstrip('/')}{self.config.upstream_messages_path}"

        # Build upstream headers — only forward allowed headers
        upstream_headers: dict[str, str] = {}
        for key in self.config.request_headers_allowlist:
            value = request.headers.get(key)
            if value is not None:
                upstream_headers[key] = value
        upstream_headers.setdefault("content-type", "application/json")
        # Discourage upstream from gzip-compressing the SSE stream: compressed
        # frames would re-buffer event boundaries, and raw bytes are forwarded
        # as-is (no decode).  We never forward content-encoding downstream.
        upstream_headers.setdefault("accept-encoding", "identity")

        # Read request body
        body_bytes = await request.body()

        try:
            upstream_req = client.build_request(
                method="POST",
                url=upstream_url,
                headers=upstream_headers,
                content=body_bytes,
            )
            upstream_resp = await client.send(upstream_req, stream=True)
        except httpx.TransportError as exc:
            await self.circuit_breaker.record_failure()
            return Response(
                content=json.dumps(
                    {
                        "error": {
                            "type": "upstream_connection_error",
                            "message": f"Failed to connect to upstream: {exc}",
                        }
                    }
                ),
                status_code=502,
                media_type="application/json",
            )

        # On non-2xx, read the full response, record failure, and return error
        if not (200 <= upstream_resp.status_code < 300):
            await self.circuit_breaker.record_failure()
            error_body = await upstream_resp.aread()
            await upstream_resp.aclose()
            return Response(
                content=error_body or b'{"error":"upstream error"}',
                status_code=upstream_resp.status_code,
                media_type=upstream_resp.headers.get("content-type", "application/json"),
            )

        # Upstream responded successfully — reset the circuit counter
        await self.circuit_breaker.record_success()

        # Collect response headers to forward
        response_headers: dict[str, str] = {}
        for key in self.config.response_headers_allowlist:
            value = upstream_resp.headers.get(key)
            if value is not None:
                response_headers[key] = value

        # Build the streaming response.  aiter_raw() (chunk_size=None) yields
        # each raw network chunk immediately with no ByteChunker aggregation
        # and no content decoding — SSE bytes reach the client untouched.
        async def byte_stream() -> AsyncIterator[bytes]:
            try:
                async for chunk in upstream_resp.aiter_raw():
                    yield chunk
            except Exception:
                # Mid-stream read failure (transport drop, client abort):
                # close the upstream connection and stop the stream.  The
                # client sees a truncated response, never a proxy error.
                logger.debug("Streaming proxy: mid-stream upstream failure", exc_info=True)
                return
            finally:
                if not upstream_resp.is_closed:
                    await upstream_resp.aclose()

        return StreamingResponse(
            byte_stream(),
            status_code=upstream_resp.status_code,
            headers=response_headers,
        )

    # ── ASGI integration ──────────────────────────────────────────────

    @property
    def router(self) -> list[Route]:
        """Return Starlette routes for this proxy.

        Mount these into a parent Starlette app for composition.
        """
        return [
            Route("/v1/messages", self._handle_messages, methods=["POST"]),
            Route("/v1/messages/", self._handle_messages, methods=["POST"]),
            Route("/health", self._handle_health, methods=["GET"]),
        ]

    async def _handle_messages(self, request: Request) -> Response:
        return await self.proxy_request(request)

    async def _handle_health(self, request: Request) -> Response:
        status = await self.health()
        return Response(
            content=json.dumps(status, default=str),
            status_code=200 if status["status"] != "error" else 503,
            media_type="application/json",
        )

    def as_asgi_app(self) -> Starlette:
        """Return a standalone Starlette ASGI application."""

        @asynccontextmanager
        async def lifespan(app: Starlette) -> AsyncIterator[None]:
            if self.config.prewarm:
                await self.prewarm()
            try:
                yield
            finally:
                await self.close()

        return Starlette(routes=self.router, lifespan=lifespan)


# ── Convenience factory ────────────────────────────────────────────────────


def create_streaming_proxy_app(
    upstream_url: str = "http://127.0.0.1:3456",
    **kwargs,
) -> Starlette:
    """Create a configured streaming proxy Starlette app in one call."""
    config = StreamingProxyConfig(upstream_url=upstream_url, **kwargs)
    proxy = PassthroughStreamingProxy(config)
    return proxy.as_asgi_app()
