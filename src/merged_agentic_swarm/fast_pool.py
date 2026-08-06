"""
Fast HTTP Connection Pool — latency-optimized transport for multi-provider dispatch.

Replaces bare ``urllib.request.urlopen()`` with a thread-local ``httpx.Client``
that reuses TCP/TLS connections, caches DNS, and maintains keepalive across
sequential requests on the same thread.

Design
~~~~~~
- **Thread-local clients** — ``httpx.Client`` is not thread-safe. We use
  ``threading.local()`` to create one client per thread. Each client maintains
  its own connection pool; within a thread, connections to the same host are
  reused across dispatches.
- **DNS caching** — httpx uses the stdlib ``socket.getaddrinfo`` which honours
  the OS resolver cache. We additionally keep a small in-process TTL cache so
  frequently hit providers skip repeated DNS lookups entirely.
- **Keepalive** — httpx sends ``Connection: keep-alive`` by default and the
  underlying ``httpcore`` connection pool holds idle connections open for
  ``keepalive_expiry`` seconds.
- **Timeout tiers** — localhost targets (litellm, fcc-proxy, routatic-proxy)
  get shorter connect timeouts; remote providers get longer ones. Per-route
  timeout overrides are passed through unchanged.
"""

from __future__ import annotations

import logging
import socket
import threading
import time
from dataclasses import dataclass
from typing import Any

import httpcore
import httpx
from httpcore import ConnectError, SyncBackend

logger = logging.getLogger("fast_pool")

# ── Configuration ────────────────────────────────────────────────────────────


@dataclass
class FastPoolConfig:
    """Connection-pool tunables for the multi-provider fabric."""

    # How many connections to keep open per host (httpx default: 100).
    max_connections: int = 200

    # Maximum idle connections across all hosts.
    max_keepalive: int = 20

    # Seconds an idle connection stays alive before being pruned.
    keepalive_expiry: float = 30.0

    # Connect timeout for remote hosts (seconds).
    connect_timeout: float = 5.0

    # Connect timeout for localhost targets (seconds).
    local_connect_timeout: float = 2.0

    # DNS cache TTL (seconds). 0 disables in-process caching.
    dns_cache_ttl: float = 300.0


_default_config = FastPoolConfig()

# ── In-process DNS cache ─────────────────────────────────────────────────────


class _DNSCache:
    """Lightweight TTL-bounded DNS cache to avoid repeated gethostbyname calls."""

    def __init__(self, ttl: float = 300.0):
        self._ttl = ttl
        self._cache: dict[str, tuple[str, float]] = {}  # hostname -> (ip, expiry)

    def get(self, hostname: str) -> str | None:
        if not self._ttl:
            return None
        entry = self._cache.get(hostname)
        if entry is None:
            return None
        ip, expiry = entry
        if time.time() > expiry:
            del self._cache[hostname]
            return None
        return ip

    def set(self, hostname: str, ip: str) -> None:
        if self._ttl:
            self._cache[hostname] = (ip, time.time() + self._ttl)

    def delete(self, hostname: str) -> None:
        """Drop one entry (used to invalidate a stale cached IP)."""
        self._cache.pop(hostname, None)

    def clear(self) -> None:
        self._cache.clear()


_dns_cache = _DNSCache(ttl=_default_config.dns_cache_ttl)

# ── Thread-local client factory ──────────────────────────────────────────────


def _resolve_host(hostname: str) -> str:
    """Resolve hostname to IP, consulting the in-process DNS cache first.

    Returns the hostname itself if resolution fails, so callers fall through
    to the OS resolver. Failed lookups are not cached.
    """
    cached = _dns_cache.get(hostname)
    if cached:
        return cached
    try:
        ip = socket.gethostbyname(hostname)
    except socket.gaierror:
        return hostname  # fall through — let the transport handle resolution
    _dns_cache.set(hostname, ip)
    return ip


class _CachedDNSBackend(SyncBackend):
    """httpcore sync backend that connects to a cached IP for each hostname.

    ``connect_tcp`` receives the original hostname from httpcore, and the TLS
    handshake (``start_tls``) is invoked later with the *original* hostname for
    SNI/certificate validation, so connecting to a pre-resolved IP is safe.

    On a connection failure against a cached IP we re-resolve once and retry —
    this covers the stale-entry case where the provider's address changed while
    an entry was still within its TTL.
    """

    def connect_tcp(
        self,
        host: str,
        port: int,
        timeout: float | None = None,
        local_address: str | None = None,
        socket_options: list[Any] | None = None,
    ) -> httpcore.NetworkStream:
        target_ip = _resolve_host(host)
        if target_ip == host:
            # Resolution was skipped/failed — connect the normal way.
            return super().connect_tcp(host, port, timeout, local_address, socket_options)
        try:
            return super().connect_tcp(target_ip, port, timeout, local_address, socket_options)
        except ConnectError:
            # Stale cache entry — invalidate, re-resolve once, retry.
            _dns_cache.delete(host)
            fresh_ip = _resolve_host(host)
            if fresh_ip == host:
                raise
            return super().connect_tcp(fresh_ip, port, timeout, local_address, socket_options)


class _PooledTransport(httpx.HTTPTransport):
    """``httpx.HTTPTransport`` whose httpcore pool uses the DNS-cached backend.

    ``httpx.HTTPTransport`` does not expose a ``network_backend`` parameter, so
    we rebuild the internal ``httpcore.ConnectionPool`` with our backend while
    reusing the exact SSL context the parent constructed.
    """

    def __init__(self, limits: httpx.Limits, config: FastPoolConfig) -> None:
        super().__init__(limits=limits)
        pool = self._pool
        # Close the parent's (unused, backend-less) pool, then rebuild ours.
        pool.close()
        self._pool = httpcore.ConnectionPool(
            ssl_context=pool._ssl_context,
            max_connections=limits.max_connections,
            max_keepalive_connections=limits.max_keepalive_connections,
            keepalive_expiry=limits.keepalive_expiry,
            http1=pool._http1,
            http2=pool._http2,
            network_backend=_CachedDNSBackend(),
        )


def _build_transport(config: FastPoolConfig) -> httpx.HTTPTransport:
    """Build an httpx transport with connection pooling, keepalive, and DNS cache."""
    limits = httpx.Limits(
        max_connections=config.max_connections,
        max_keepalive_connections=config.max_keepalive,
        keepalive_expiry=config.keepalive_expiry,
    )
    return _PooledTransport(limits, config)


_thread_local = threading.local()


def _create_client(config: FastPoolConfig | None = None) -> httpx.Client:
    """Create a fresh httpx.Client with connection pooling.

    Each thread gets its own client via ``get_client()`` because
    ``httpx.Client`` is not thread-safe.
    """
    cfg = config or _default_config
    transport = _build_transport(cfg)
    return httpx.Client(
        transport=transport,
        timeout=httpx.Timeout(
            connect=cfg.connect_timeout,
            read=None,  # read timeout is per-request via route config
            write=None,
            pool=None,
        ),
        headers={"User-Agent": "MergedAgenticSwarm/1.0"},
    )


def get_client(config: FastPoolConfig | None = None) -> httpx.Client:
    """Return the thread-local httpx client, creating one on first access.

    Within a thread, this reuses the same client (and its connection pool)
    across every ``dispatch_request`` call, so connections to frequently-hit
    providers stay warm.
    """
    client = getattr(_thread_local, "client", None)
    if client is None or client.is_closed:
        client = _create_client(config)
        _thread_local.client = client
    return client


def close_thread_client() -> None:
    """Close the current thread's httpx client (called at thread shutdown)."""
    client = getattr(_thread_local, "client", None)
    if client is not None:
        client.close()
        _thread_local.client = None


# ── HTTP dispatch helpers ────────────────────────────────────────────────────


def dispatch(
    target_url: str,
    req_data: bytes,
    headers: dict[str, str],
    timeout: float,
    config: FastPoolConfig | None = None,
) -> httpx.Response:
    """Send a POST request through the pooled client and return the response.

    Parameters
    ----------
    target_url:
        Full provider endpoint URL.
    req_data:
        UTF-8-encoded JSON payload bytes.
    headers:
        Request headers (Content-Type, Authorization, User-Agent, etc.).
    timeout:
        Per-request total timeout in seconds. Overrides the pool default.
    config:
        Optional pool configuration (uses ``FastPoolConfig`` defaults if omitted).

    Returns
    -------
    httpx.Response
        The server response (caller must drain ``.read()`` and close or
        let the context-manager handle it).

    Raises
    ------
    httpx.HTTPStatusError
        On 4xx/5xx responses.
    httpx.TimeoutException
        On connect/read/write/pool timeout.
    httpx.RequestError
        On other transport errors (DNS, TLS, connection refused).
    """
    client = get_client(config)
    cfg = config or _default_config
    # For localhost targets, use a shorter connect timeout if the pool
    # default is longer.
    is_local = "localhost" in target_url or "127.0.0.1" in target_url
    if is_local and client.timeout.connect > cfg.local_connect_timeout:
        # Override per-request; the pool-wide default stays unchanged.
        client.timeout = httpx.Timeout(
            connect=cfg.local_connect_timeout,
            read=timeout,
            write=timeout,
            pool=timeout,
        )
    else:
        client.timeout = httpx.Timeout(
            connect=client.timeout.connect,
            read=timeout,
            write=timeout,
            pool=timeout,
        )

    response = client.post(
        target_url,
        content=req_data,
        headers=headers,
    )
    # Raise on 4xx/5xx so callers' ``httpx.HTTPStatusError`` handling
    # (fabric fallback cascade, circuit breaker) actually triggers instead
    # of a non-2xx body flowing into the success path.
    response.raise_for_status()
    return response


def prewarm_hosts(hosts: list[str], config: FastPoolConfig | None = None) -> dict[str, bool]:
    """Pre-warm DNS + TLS handshake for a list of hostnames.

    Opens a TCP connection to each host and completes the TLS handshake
    (for HTTPS targets), then holds the connection in the pool for reuse.
    Call once at startup for frequently-used providers.

    Returns a dict mapping hostname to success boolean.
    """
    results: dict[str, bool] = {}
    for host in hosts:
        scheme = "https" if not host.startswith("localhost") and not host.startswith("127.0.0.1") else "http"
        url = f"{scheme}://{host if '://' not in host else host.split('://', 1)[1]}"
        if "://" in host:
            url = host.rstrip("/")
        try:
            client = get_client(config)
            # Send an HTTP HEAD to warm the connection without transferring a body.
            resp = client.head(url, timeout=5.0)
            resp.read()
            results[host] = True
            logger.debug(f"Pool warmed for {host} (HTTP {resp.status_code})")
        except Exception as exc:
            logger.debug(f"Pool warm failed for {host}: {exc}")
            results[host] = False
    return results


# ── Startup helper ───────────────────────────────────────────────────────────

# Known provider hosts whose connections should be pre-warmed at startup.
_KNOWN_PROVIDER_HOSTS = [
    "generativelanguage.googleapis.com",
    "integrate.api.nvidia.com",
    "api.mistral.ai",
    "openrouter.ai",
    "http://localhost:4000",  # litellm
    "http://localhost:8080",  # fcc-proxy
    "http://localhost:3456",  # routatic-proxy
]


def warm_all(config: FastPoolConfig | None = None) -> dict[str, bool]:
    """Pre-warm connections to all known provider hosts. Call at startup."""
    return prewarm_hosts(_KNOWN_PROVIDER_HOSTS, config)
