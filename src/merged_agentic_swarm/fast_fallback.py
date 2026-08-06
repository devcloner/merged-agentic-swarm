"""
Fast Fallback Router — parallel-probe, minimal-latency fallback dispatch.

Why this exists
~~~~~~~~~~~~~~~
The sequential cascade in ``MultiProviderFabric.dispatch_request`` walks the
provider chain one route at a time. Each dead attempt adds its own latency
(connect + request round-trip) before the next provider is tried, and the
existing ``except httpx.HTTPStatusError`` handler never fires because
``fast_pool.dispatch`` returns non-2xx responses instead of raising — so a 401
primary is retried on every request and the whole chain is re-walked serially.

This module replaces that cascade with a hedged, parallel probe:

- **Parallel probing** — the primary route and the next ``parallel_probes - 1``
  fallbacks are dispatched simultaneously, so the latency of a failed primary
  overlaps the latency of a healthy fallback instead of adding to it.
- **First success wins** — the first provider to return a 2xx response provides
  the answer; the runner returns immediately without waiting for the rest.
- **Cancellation** — on the first success, not-yet-started probes are cancelled
  and in-flight probes are signalled via a ``threading.Event`` to discard their
  results without recording spurious failures. (Python threads cannot be killed
  mid-request, so cancellation is cooperative; stragglers finish in the
  background but are ignored.)
- **Circuit breaker** — after ``circuit_breaker_threshold`` consecutive failures
  a provider is skipped for ``circuit_breaker_cooldown`` seconds. The router
  also honours the shared perma-ban/circuit state in ``multi_provider_fabric``,
  so a 401-blacklisted provider is skipped cheaply on every dispatch.
- **Adaptive selection** — routes are re-ordered by a composite score of static
  priority and recent EWMA latency, so a consistently fast fallback can jump
  ahead of a slow primary without abandoning the verified-first ordering.

Configuration
~~~~~~~~~~~~~
All knobs live in :class:`FastFallbackConfig`; the ``default_fast_fallback``
singleton reads them from environment variables at import time:

===============  =====================  ============  =========================
Env var          Field                  Default       Meaning
===============  =====================  ============  =========================
FAST_FALLBACK_ENABLED                enabled             True  Master switch
FAST_FALLBACK_PARALLEL_PROBES        parallel_probes       2  Concurrent probes per wave
FAST_FALLBACK_PROBE_STAGGER_MS       probe_stagger_ms       0  Head-start ms for earlier probes
FAST_FALLBACK_CIRCUIT_BREAKER_THRESHOLD circuit_breaker_threshold 3  Consecutive failures before skip
FAST_FALLBACK_CIRCUIT_BREAKER_COOLDOWN  circuit_breaker_cooldown  120.0  Skip duration (s)
FAST_FALLBACK_ADAPTIVE_SELECTION     enable_adaptive_selection True  Latency-based reordering
FAST_FALLBACK_MIN_LATENCY_SAMPLES    min_latency_samples      3  Samples before latency is trusted
FAST_FALLBACK_LATENCY_WINDOW         latency_window          20  Max tracked samples per provider
FAST_FALLBACK_REFERENCE_LATENCY_MS   reference_latency_ms  1000.0  Latency normalization base
FAST_FALLBACK_DEFAULT_TIMEOUT        default_timeout         10.0  Remote per-probe timeout (s)
FAST_FALLBACK_LOCAL_TIMEOUT          local_timeout            5.0  Localhost per-probe timeout (s)
FAST_FALLBACK_WAVE_TIMEOUT_SLACK     wave_timeout_slack       2.0  Extra wait above slowest probe
FAST_FALLBACK_MAX_WORKER_THREADS     max_worker_threads       8  Probe pool size
===============  =====================  ============  =========================
"""

from __future__ import annotations

import json
import logging
import os
import threading
import time
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Any

import httpx

from merged_agentic_swarm.fast_pool import dispatch as pool_dispatch
from merged_agentic_swarm.providers.key_pool import APIKeyInfo, default_key_pool
from merged_agentic_swarm.providers.multi_provider_fabric import (
    MultiProviderFabric,
)
from merged_agentic_swarm.providers.multi_provider_fabric import (
    _circuit_open_until as _fabric_circuit_open_until,
)
from merged_agentic_swarm.providers.multi_provider_fabric import (
    _permanently_dead as _fabric_permanently_dead,
)
from merged_agentic_swarm.providers.multi_provider_fabric import (
    _record_failure as _fabric_record_failure,
)
from merged_agentic_swarm.providers.multi_provider_fabric import (
    _record_success as _fabric_record_success,
)

logger = logging.getLogger("fast_fallback")

# ── Configuration ────────────────────────────────────────────────────────────


@dataclass
class FastFallbackConfig:
    """Tunables for the fast-fallback router (dataclass defaults + env overrides)."""

    # Master switch — when False, ``dispatch`` delegates to the sequential fabric.
    enabled: bool = True

    # How many routes are probed concurrently per wave. 2 = primary + first fallback.
    parallel_probes: int = 2

    # Head-start (ms) given to earlier probes in a wave so the primary gets a
    # chance to respond before a fallback is fired. 0 fires all probes together.
    probe_stagger_ms: float = 0.0

    # Circuit breaker: consecutive failures before a provider is skipped.
    circuit_breaker_threshold: int = 3

    # Circuit breaker: how long a tripped provider stays skipped (seconds).
    circuit_breaker_cooldown: float = 120.0

    # Adaptive selection: reorder routes by recent latency when enough samples exist.
    enable_adaptive_selection: bool = True

    # Minimum number of latency samples before a provider's EWMA is trusted.
    min_latency_samples: int = 3

    # Maximum number of latency samples tracked per provider.
    latency_window: int = 20

    # EWMA latency normalization base (ms) for the adaptive ordering penalty.
    reference_latency_ms: float = 1000.0

    # Per-probe timeout for remote providers (seconds).
    default_timeout: float = 10.0

    # Per-probe timeout for localhost providers (seconds).
    local_timeout: float = 5.0

    # Extra seconds a wave waits above its slowest probe before giving up.
    wave_timeout_slack: float = 2.0

    # Maximum worker threads in the probe pool.
    max_worker_threads: int = 8

    def __post_init__(self) -> None:
        self.parallel_probes = max(self.parallel_probes, 1)
        self.max_worker_threads = max(self.max_worker_threads, 1)

    @classmethod
    def from_env(cls) -> FastFallbackConfig:
        """Build a config from ``FAST_FALLBACK_*`` environment variables."""

        def _env_bool(name: str, default: bool) -> bool:
            value = os.environ.get(name)
            if value is None:
                return default
            return value.strip().lower() in ("1", "true", "yes", "on")

        def _env_int(name: str, default: int) -> int:
            try:
                return int(os.environ.get(name, default))
            except (TypeError, ValueError):
                return default

        def _env_float(name: str, default: float) -> float:
            try:
                return float(os.environ.get(name, default))
            except (TypeError, ValueError):
                return default

        return cls(
            enabled=_env_bool("FAST_FALLBACK_ENABLED", True),
            parallel_probes=_env_int("FAST_FALLBACK_PARALLEL_PROBES", 2),
            probe_stagger_ms=_env_float("FAST_FALLBACK_PROBE_STAGGER_MS", 0.0),
            circuit_breaker_threshold=_env_int("FAST_FALLBACK_CIRCUIT_BREAKER_THRESHOLD", 3),
            circuit_breaker_cooldown=_env_float("FAST_FALLBACK_CIRCUIT_BREAKER_COOLDOWN", 120.0),
            enable_adaptive_selection=_env_bool("FAST_FALLBACK_ADAPTIVE_SELECTION", True),
            min_latency_samples=_env_int("FAST_FALLBACK_MIN_LATENCY_SAMPLES", 3),
            latency_window=_env_int("FAST_FALLBACK_LATENCY_WINDOW", 20),
            reference_latency_ms=_env_float("FAST_FALLBACK_REFERENCE_LATENCY_MS", 1000.0),
            default_timeout=_env_float("FAST_FALLBACK_DEFAULT_TIMEOUT", 10.0),
            local_timeout=_env_float("FAST_FALLBACK_LOCAL_TIMEOUT", 5.0),
            wave_timeout_slack=_env_float("FAST_FALLBACK_WAVE_TIMEOUT_SLACK", 2.0),
            max_worker_threads=_env_int("FAST_FALLBACK_MAX_WORKER_THREADS", 8),
        )


# ── Internal result/context records ─────────────────────────────────────────


@dataclass
class _ProbeResult:
    success: bool
    provider: str
    route: dict[str, Any]
    response: dict[str, Any] | None = None
    error: str | None = None
    cancelled: bool = False


@dataclass
class _ProbeContext:
    model_alias: str
    payload: dict[str, Any]
    stagger_seconds: float = 0.0


# ── Router ──────────────────────────────────────────────────────────────────


class FastFallbackRouter:
    """Parallel-probe fallback router over the model fabric's route table.

    ``dispatch`` mirrors the signature and return shape of
    ``MultiProviderFabric.dispatch_request`` so callers can swap it in without
    touching request/response formatting (which is reused from the fabric).
    """

    def __init__(
        self,
        config: FastFallbackConfig | None = None,
        key_pool: Any | None = None,
        fabric: MultiProviderFabric | None = None,
    ) -> None:
        self.config = config or FastFallbackConfig.from_env()
        self.key_pool = key_pool or default_key_pool
        self.fabric = fabric or MultiProviderFabric(key_pool=self.key_pool)
        self._circuit_failures: dict[str, int] = {}
        self._circuit_open_until: dict[str, float] = {}
        self._ewma_latency: dict[str, float] = {}
        self._latency_samples: dict[str, int] = {}
        self._lock = threading.Lock()
        self._executor: ThreadPoolExecutor = ThreadPoolExecutor(
            max_workers=self.config.max_worker_threads,
            thread_name_prefix="fast-fallback",
        )

    # ── Public API ────────────────────────────────────────────────────────

    def dispatch(
        self,
        model_alias: str,
        messages: list[dict[str, Any]],
        system_prompt: str | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        tools: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Dispatch a request across providers with parallel fallback probing.

        Returns an Anthropic-shaped response dict, exactly like
        ``MultiProviderFabric.dispatch_request`` (including the simulation
        fallback when every provider is unhealthy).
        """
        if not self.config.enabled:
            return self.fabric.dispatch_request(
                model_alias=model_alias,
                messages=messages,
                system_prompt=system_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                tools=tools,
            )

        # Empty conversation is a malformed request — don't burn provider calls.
        if not messages and not system_prompt:
            logger.warning("Fast-fallback dispatch called with empty messages; returning error response.")
            return self._error_response(model_alias, "[ERROR] Empty conversation: provide at least one message.")

        candidates = self._order_candidates(self.fabric._build_route_list(model_alias))
        if not candidates:
            return self._simulation_fallback(model_alias, "no healthy providers available")

        cancel_event = threading.Event()
        last_error: str | None = None
        for start in range(0, len(candidates), self.config.parallel_probes):
            wave = candidates[start : start + self.config.parallel_probes]
            result = self._probe_wave(
                model_alias, messages, system_prompt, max_tokens, temperature, tools, wave, cancel_event
            )
            if result is not None and result.success:
                return result.response
            if result is not None and result.error:
                last_error = result.error
            if cancel_event.is_set():
                break

        return self._simulation_fallback(model_alias, last_error)

    def reset(self) -> None:
        """Clear circuit-breaker and latency state (used by tests/health checks)."""
        with self._lock:
            self._circuit_failures.clear()
            self._circuit_open_until.clear()
            self._ewma_latency.clear()
            self._latency_samples.clear()

    def circuit_status(self) -> dict[str, dict[str, Any]]:
        """Snapshot of circuit-breaker and latency state per provider."""
        with self._lock:
            return {
                provider: {
                    "consecutive_failures": self._circuit_failures.get(provider, 0),
                    "open_until": self._circuit_open_until.get(provider, 0.0),
                    "ewma_latency_ms": round(self._ewma_latency.get(provider, 0.0), 1),
                    "latency_samples": self._latency_samples.get(provider, 0),
                }
                for provider in sorted(
                    set(self._circuit_failures)
                    | set(self._circuit_open_until)
                    | set(self._ewma_latency)
                    | set(self._latency_samples)
                )
            }

    # ── Circuit breaker ───────────────────────────────────────────────────

    def _record_failure(self, provider: str) -> None:
        now = time.time()
        with self._lock:
            if now < self._circuit_open_until.get(provider, 0.0):
                return  # already open
            count = self._circuit_failures.get(provider, 0) + 1
            self._circuit_failures[provider] = count
            if count >= self.config.circuit_breaker_threshold:
                self._circuit_open_until[provider] = now + self.config.circuit_breaker_cooldown
                self._circuit_failures[provider] = 0
                logger.warning(
                    f"Fast-fallback: circuit opened for {provider} after {count} failures; "
                    f"skipping for {self.config.circuit_breaker_cooldown}s."
                )

    def _record_success(self, provider: str, latency_ms: float) -> None:
        with self._lock:
            self._circuit_failures[provider] = 0
            self._circuit_open_until.pop(provider, None)
            alpha = 0.3
            old = self._ewma_latency.get(provider)
            self._ewma_latency[provider] = latency_ms if old is None else (alpha * latency_ms + (1 - alpha) * old)
            self._latency_samples[provider] = min(
                self._latency_samples.get(provider, 0) + 1, self.config.latency_window
            )

    def _maybe_reset_expired(self, provider: str) -> None:
        now = time.time()
        with self._lock:
            open_until = self._circuit_open_until.get(provider)
            if open_until is not None and now >= open_until:
                # Cooldown expired — reset and allow a half-open probe.
                self._circuit_open_until.pop(provider, None)
                self._circuit_failures[provider] = 0

    def _is_skipped(self, provider: str) -> bool:
        now = time.time()
        # Shared fabric state (perma-ban on 401, circuit tripped by the cascade).
        if provider in _fabric_permanently_dead and now < _fabric_permanently_dead[provider]:
            return True
        if provider in _fabric_circuit_open_until and now < _fabric_circuit_open_until[provider]:
            return True
        with self._lock:
            open_until = self._circuit_open_until.get(provider)
        return open_until is not None and now < open_until

    # ── Adaptive ordering ─────────────────────────────────────────────────

    def _order_candidates(self, routes: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Return healthy routes ordered by static priority + EWMA latency.

        Score = static index + latency penalty, where the penalty is the
        provider's EWMA latency normalized by ``reference_latency_ms`` (capped).
        Providers without enough latency samples keep their static position, so
        the verified-first ordering is preserved until real data exists.
        """
        healthy: list[tuple[int, dict[str, Any]]] = []
        for idx, route in enumerate(routes):
            provider = route["provider"]
            if self._is_skipped(provider):
                continue
            self._maybe_reset_expired(provider)
            healthy.append((idx, route))

        if not healthy:
            return []
        if not self.config.enable_adaptive_selection:
            return [route for _, route in healthy]

        scored: list[tuple[float, int, dict[str, Any]]] = []
        for idx, route in healthy:
            provider = route["provider"]
            with self._lock:
                ewma = self._ewma_latency.get(provider)
                samples = self._latency_samples.get(provider, 0)
            if samples >= self.config.min_latency_samples and ewma is not None:
                penalty = min(3.0, ewma / self.config.reference_latency_ms)
            else:
                penalty = 0.0
            scored.append((idx + penalty, idx, route))
        scored.sort(key=lambda item: (item[0], item[1]))
        return [route for _, _, route in scored]

    # ── Parallel probing ──────────────────────────────────────────────────

    def _probe_wave(
        self,
        model_alias: str,
        messages: list[dict[str, Any]],
        system_prompt: str | None,
        max_tokens: int,
        temperature: float,
        tools: list[dict[str, Any]] | None,
        wave_routes: list[dict[str, Any]],
        cancel_event: threading.Event,
    ) -> _ProbeResult | None:
        """Fire one wave of probes concurrently; return the first success (or None)."""
        future_map: dict[Future[Any], dict[str, Any]] = {}
        for i, route in enumerate(wave_routes):
            if cancel_event.is_set():
                break
            payload = self._build_payload(route, model_alias, messages, system_prompt, max_tokens, temperature, tools)
            ctx = _ProbeContext(
                model_alias=model_alias,
                payload=payload,
                stagger_seconds=i * self.config.probe_stagger_ms / 1000.0,
            )
            future_map[self._executor.submit(self._probe_single, route, ctx, cancel_event)] = route

        if not future_map:
            return None

        wave_timeout = max(self._route_timeout(route) for route in future_map.values()) + self.config.wave_timeout_slack
        wave_last_error: str | None = None
        try:
            for fut in as_completed(future_map, timeout=wave_timeout):
                try:
                    result = fut.result()
                except Exception as exc:
                    logger.warning(f"Fast-fallback: unexpected probe error: {exc}")
                    wave_last_error = wave_last_error or str(exc)
                    continue
                if result.cancelled:
                    continue
                if result.success:
                    # First success wins — cancel queued probes and stop waiting.
                    cancel_event.set()
                    for other in future_map:
                        if other is not fut:
                            other.cancel()
                    return result
                if result.error:
                    wave_last_error = result.error
        except TimeoutError:
            for fut in future_map:
                fut.cancel()
            wave_last_error = wave_last_error or f"probe wave timed out after {wave_timeout:.1f}s"

        return _ProbeResult(success=False, provider="", route={}, error=wave_last_error)

    def _probe_single(
        self,
        route: dict[str, Any],
        ctx: _ProbeContext,
        cancel_event: threading.Event,
    ) -> _ProbeResult:
        """Probe one route; returns a result that records its own health effects."""
        provider = route["provider"]
        if cancel_event.is_set():
            return _ProbeResult(success=False, provider=provider, route=route, cancelled=True)

        if self._is_skipped(provider):
            return _ProbeResult(success=False, provider=provider, route=route, cancelled=True)

        # Optional head-start: if a faster probe wins during the stagger window,
        # bail before spending a request.
        if ctx.stagger_seconds and cancel_event.wait(ctx.stagger_seconds):
            return _ProbeResult(success=False, provider=provider, route=route, cancelled=True)

        key_info = self.key_pool.get_key(provider)
        if key_info is None:
            logger.debug(f"Fast-fallback: no key available for provider {provider} ({route['model']}).")
            return _ProbeResult(success=False, provider=provider, route=route, error="no key available")

        start_time = time.time()
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {key_info.secret_value}",
            }
            req_data = json.dumps(ctx.payload).encode("utf-8")
            response = pool_dispatch(route["url"], req_data, headers, self._route_timeout(route))

            if response.status_code >= 400:
                return self._handle_http_error(route, ctx, cancel_event, key_info, response.status_code, response.text)

            if cancel_event.is_set():
                # Another probe won while we were in flight — keep the key's
                # stats honest but discard the response (no spurious failure).
                latency_ms = (time.time() - start_time) * 1000
                self.key_pool.mark_success(key_info, latency_ms=latency_ms)
                return _ProbeResult(success=False, provider=provider, route=route, cancelled=True)

            try:
                resp_json = response.json()
            except ValueError:
                # 2xx with a non-JSON/empty body — the provider is misbehaving;
                # trip the breakers and treat as a failure (matches the fabric).
                _fabric_record_failure(provider)
                self._record_failure(provider)
                return _ProbeResult(success=False, provider=provider, route=route, error="non-JSON response body")
            if not isinstance(resp_json, dict):
                _fabric_record_failure(provider)
                self._record_failure(provider)
                return _ProbeResult(success=False, provider=provider, route=route, error="non-object response body")

            latency_ms = (time.time() - start_time) * 1000
            tokens = resp_json.get("usage", {}).get("total_tokens", 0)
            self.key_pool.mark_success(key_info, latency_ms=latency_ms, tokens=tokens)
            self._record_success(provider, latency_ms)
            _fabric_record_success(provider, model_alias=ctx.model_alias)
            return _ProbeResult(
                success=True,
                provider=provider,
                route=route,
                response=self._format_response(route, ctx.model_alias, resp_json),
            )
        except httpx.HTTPStatusError as e:
            if cancel_event.is_set():
                return _ProbeResult(success=False, provider=provider, route=route, cancelled=True)
            return self._handle_http_error(route, ctx, cancel_event, key_info, e.response.status_code, e.response.text)
        except (httpx.TimeoutException, httpx.RequestError) as e:
            if cancel_event.is_set():
                return _ProbeResult(success=False, provider=provider, route=route, cancelled=True)
            logger.warning(f"Fast-fallback: {type(e).__name__} calling provider {provider}: {e}")
            _fabric_record_failure(provider)
            self._record_failure(provider)
            return _ProbeResult(success=False, provider=provider, route=route, error=str(e))

    def _handle_http_error(
        self,
        route: dict[str, Any],
        ctx: _ProbeContext,
        cancel_event: threading.Event,
        key_info: APIKeyInfo,
        status: int,
        body: str,
    ) -> _ProbeResult:
        """Record an HTTP error's health effects and return a failure result."""
        provider = route["provider"]
        if cancel_event.is_set():
            return _ProbeResult(success=False, provider=provider, route=route, cancelled=True)
        err_text = body[:200]
        logger.warning(f"Fast-fallback: HTTP {status} on provider {provider} ({route['model']}): {err_text}")
        if status == 401:
            # Auth failure — perma-ban via the shared fabric state (24h).
            _fabric_record_failure(provider, http_code=status)
        elif status in (429, 503):
            # Key-level throttle — cool this key down; next request rotates keys.
            self.key_pool.mark_rate_limited(key_info, cooldown_seconds=60.0)
        else:
            # Other HTTP errors — provider-level failure, trip both breakers.
            _fabric_record_failure(provider, http_code=status)
            self._record_failure(provider)
        return _ProbeResult(success=False, provider=provider, route=route, error=f"HTTP {status}: {err_text}")

    # ── Request/response helpers ─────────────────────────────────────────

    def _build_payload(
        self,
        route: dict[str, Any],
        model_alias: str,
        messages: list[dict[str, Any]],
        system_prompt: str | None,
        max_tokens: int,
        temperature: float,
        tools: list[dict[str, Any]] | None,
    ) -> dict[str, Any]:
        """Build the per-provider payload, reusing the fabric's format helpers."""
        if "/v1/messages" in route["url"]:
            payload: dict[str, Any] = {
                "model": route["model"],
                "messages": self.fabric.format_anthropic_to_anthropic(messages, system_prompt),
                "max_tokens": max_tokens,
                "temperature": temperature,
            }
            if system_prompt:
                payload["system"] = system_prompt
            if tools:
                payload["tools"] = self.fabric._tools_to_anthropic(tools)
        else:
            payload = {
                "model": route["model"],
                "messages": self.fabric.format_anthropic_to_openai(messages, system_prompt),
                "max_tokens": max_tokens,
                "temperature": temperature,
            }
            if tools:
                payload["tools"] = tools
        return payload

    def _format_response(self, route: dict[str, Any], model_alias: str, resp_json: dict[str, Any]) -> dict[str, Any]:
        """Normalize a provider response into the Anthropic-shaped return value."""
        if resp_json.get("type") == "message":
            resp_json["model"] = model_alias  # override model name in response
            tool_calls = self.fabric._extract_anthropic_tool_calls(resp_json)
            if tool_calls:
                resp_json["tool_calls"] = tool_calls
            return resp_json
        return self.fabric.format_openai_to_anthropic_response(resp_json, model_alias)

    def _route_timeout(self, route: dict[str, Any]) -> float:
        if route.get("timeout"):
            return float(route["timeout"])
        url = route.get("url", "")
        is_local = "localhost" in url or "127.0.0.1" in url
        return self.config.local_timeout if is_local else self.config.default_timeout

    @staticmethod
    def _simulation_fallback(model_alias: str, last_error: str | None = None) -> dict[str, Any]:
        logger.warning(
            f"Fast-fallback: all providers unreachable for {model_alias} (last error: {last_error}). "
            "Using simulation fallback."
        )
        return {
            "id": f"msg_sim_{int(time.time() * 1000)}",
            "type": "message",
            "role": "assistant",
            "model": model_alias,
            "content": [
                {
                    "type": "text",
                    "text": f"[SIMULATION — Model: {model_alias}]\n"
                    "Request processed via offline backup synthesis. All live providers failed.",
                }
            ],
            "stop_reason": "end_turn",
            "stop_sequence": None,
            "usage": {"input_tokens": 0, "output_tokens": 0},
            "simulation_fallback": True,  # flag for callers to detect synthetic responses
        }

    @staticmethod
    def _error_response(model_alias: str, text: str) -> dict[str, Any]:
        return {
            "id": f"msg_err_{int(time.time() * 1000)}",
            "type": "message",
            "role": "assistant",
            "model": model_alias,
            "content": [{"type": "text", "text": text}],
            "stop_reason": "end_turn",
            "stop_sequence": None,
            "usage": {"input_tokens": 0, "output_tokens": 0},
            "error": "empty_conversation",
        }


# ── Global Singleton & convenience entry point ──────────────────────────────

default_fast_fallback = FastFallbackRouter()


def dispatch_fast(
    model_alias: str,
    messages: list[dict[str, Any]],
    system_prompt: str | None = None,
    max_tokens: int = 4096,
    temperature: float = 0.7,
    tools: list[dict[str, Any]] | None = None,
    router: FastFallbackRouter | None = None,
) -> dict[str, Any]:
    """Dispatch a request through the fast-fallback router.

    Mirrors ``MultiProviderFabric.dispatch_request``'s signature so the proxy
    server can switch to it in one line:

        response_data = dispatch_fast(model_alias=model, messages=messages, ...)

    Pass ``router`` to use a non-default router (e.g. an isolated test instance).
    """
    selected = router or default_fast_fallback
    return selected.dispatch(
        model_alias=model_alias,
        messages=messages,
        system_prompt=system_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        tools=tools,
    )
