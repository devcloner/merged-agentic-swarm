"""
Per-request streaming latency tracking and provider health reporting.

Tracks streaming latency for individual LLM requests and aggregates the
results into percentile stats (TTFB, tokens/sec, total time) so slow
providers can be identified and flagged.

The tracker is deliberately framework-agnostic: call sites only need to start
a timing, mark the first byte, and finish (or fail).  Aggregation and
slow-provider detection happen lazily in :meth:`LatencyTracker.stats`, so the
tracker has no effect on the hot request path beyond recording a few
monotonic timestamps.

Usage::

    tracker = LatencyTracker(slow_provider_threshold_ms=2000)

    timing = tracker.start_request(provider="litellm", model="gemini-2.5-flash")
    # ... stream from upstream ...
    timing.mark_first_byte()
    # ... finish streaming ...
    tracker.finish(timing, total_tokens=128)

    report = tracker.stats()
    print(report["slow_providers"])
"""

from __future__ import annotations

import math
import statistics
import threading
import time
from dataclasses import dataclass, field

# ── Percentile helpers ─────────────────────────────────────────────────────


def percentile(sorted_values: list[float], pct: float) -> float:
    """Nearest-rank percentile of an already-sorted ascending list.

    Returns 0.0 for an empty list.  ``pct`` is a percentage between 0 and 100.
    """
    if not sorted_values:
        return 0.0
    rank = math.ceil((pct / 100.0) * len(sorted_values))
    rank = min(max(rank, 1), len(sorted_values))
    return sorted_values[rank - 1]


def _pct_stats(values: list[float]) -> dict[str, float]:
    """Return a p50/p95/p99 summary dict for a list of raw values."""
    if not values:
        return {"p50": 0.0, "p95": 0.0, "p99": 0.0}
    ordered = sorted(values)
    return {
        "p50": round(percentile(ordered, 50), 2),
        "p95": round(percentile(ordered, 95), 2),
        "p99": round(percentile(ordered, 99), 2),
    }


def _to_ms(seconds: float) -> float:
    return round(seconds * 1000.0, 2)


# ── Per-request timing record ──────────────────────────────────────────────


@dataclass
class RequestTiming:
    """Mutable timing record for a single streaming request.

    Call sites mutate this object via the tracker methods; fields are public
    for convenience but should be treated as write-once-after-start.
    """

    provider: str
    """Provider name, e.g. ``litellm`` or ``routatic-proxy``."""

    model: str
    """Model identifier used for the request."""

    request_id: str
    """Unique request identifier (generated if not supplied)."""

    started_at: float = field(default_factory=time.monotonic)
    """Monotonic timestamp of request start."""

    first_byte_at: float | None = None
    """Monotonic timestamp of first upstream byte (TTFB anchor)."""

    ended_at: float | None = None
    """Monotonic timestamp of request completion/failure."""

    total_tokens: int = 0
    """Tokens produced by the request (0 if unknown)."""

    error: str | None = None
    """Error message if the request failed, else None."""

    completed: bool = False
    """True when the request finished without error."""

    def mark_first_byte(self) -> None:
        """Record the first-byte (TTFB) moment.  Idempotent per request."""
        if self.first_byte_at is None:
            self.first_byte_at = time.monotonic()

    @property
    def ttfb_seconds(self) -> float | None:
        """Time-to-first-byte in seconds, or None if no byte was received."""
        if self.first_byte_at is None:
            return None
        return self.first_byte_at - self.started_at

    @property
    def total_seconds(self) -> float | None:
        """Total request duration in seconds, or None if still in flight."""
        if self.ended_at is None:
            return None
        return self.ended_at - self.started_at

    @property
    def tokens_per_second(self) -> float | None:
        """Streaming throughput in tokens/sec, or None if not computable."""
        total = self.total_seconds
        if total is None or total <= 0.0 or self.total_tokens <= 0:
            return None
        return self.total_tokens / total


# ── Tracker ────────────────────────────────────────────────────────────────


class LatencyTracker:
    """Aggregates per-request streaming latency stats, grouped by provider.

    Thread-safe: concurrent requests may record timings from multiple worker
    tasks.  Finished records are retained until :meth:`reset` is called or a
    rolling window (:attr:`max_records`) evicts the oldest entries.
    """

    def __init__(
        self,
        slow_provider_threshold_ms: float = 2000.0,
        max_records: int = 10_000,
        active_stale_seconds: float = 300.0,
    ) -> None:
        self.slow_provider_threshold_ms = slow_provider_threshold_ms
        """p95 total time (ms) at/above which a provider is flagged slow."""

        self.max_records = max_records
        """Maximum finished records retained; oldest are evicted when exceeded."""

        self.active_stale_seconds = active_stale_seconds
        """In-flight records older than this (seconds) are pruned as abandoned."""

        self._lock = threading.RLock()
        self._records: list[RequestTiming] = []
        self._active: dict[str, RequestTiming] = {}

    # ── Recording ─────────────────────────────────────────────────────

    def start_request(
        self,
        provider: str,
        model: str,
        request_id: str | None = None,
    ) -> RequestTiming:
        """Begin tracking a request and return its timing record."""
        timing = RequestTiming(
            provider=provider,
            model=model,
            request_id=request_id or f"req-{time.monotonic_ns()}",
        )
        with self._lock:
            self._active[timing.request_id] = timing
        return timing

    def mark_first_byte(self, timing: RequestTiming) -> None:
        """Record the first-byte (TTFB) moment on a timing record."""
        timing.mark_first_byte()

    def finish(
        self,
        timing: RequestTiming,
        total_tokens: int = 0,
        error: str | None = None,
    ) -> None:
        """Finalize a request.  ``error=None`` marks it completed."""
        with self._lock:
            timing.total_tokens = total_tokens
            timing.error = error
            timing.completed = error is None
            timing.ended_at = time.monotonic()
            self._active.pop(timing.request_id, None)
            self._records.append(timing)
            # Trim to a bounded rolling window
            over = len(self._records) - self.max_records
            if over > 0:
                del self._records[:over]

    def fail(self, timing: RequestTiming, error: str) -> None:
        """Finalize a request as failed."""
        self.finish(timing, error=error)

    def reset(self) -> None:
        """Drop all retained records and any in-flight timings."""
        with self._lock:
            self._records.clear()
            self._active.clear()

    def prune_stale_active(self, now: float | None = None) -> int:
        """Drop in-flight records abandoned before :meth:`finish`.

        A caller that raises after :meth:`start_request` leaves the record in
        ``_active`` forever, so ``in_flight_count`` drifts upward. Records older
        than ``active_stale_seconds`` are finalized as failures and moved into
        the retained history. Returns the number pruned.
        """
        if not self.active_stale_seconds:
            return 0
        with self._lock:
            if not self._active:
                return 0
            now = now if now is not None else time.monotonic()
            cutoff = now - self.active_stale_seconds
            stale_ids = [rid for rid, t in self._active.items() if t.started_at < cutoff]
            pruned = 0
            for rid in stale_ids:
                t = self._active.pop(rid, None)
                if t is None:
                    continue
                t.ended_at = now
                t.error = t.error or "pruned: abandoned before finish"
                t.completed = False
                self._records.append(t)
                over = len(self._records) - self.max_records
                if over > 0:
                    del self._records[:over]
                pruned += 1
        return pruned

    @property
    def record_count(self) -> int:
        """Number of finished records currently retained."""
        with self._lock:
            return len(self._records)

    @property
    def in_flight_count(self) -> int:
        """Number of requests currently being tracked (stale ones excluded)."""
        with self._lock:
            if not self.active_stale_seconds or not self._active:
                return len(self._active)
            cutoff = time.monotonic() - self.active_stale_seconds
            return sum(1 for t in self._active.values() if t.started_at >= cutoff)

    # ── Reporting ─────────────────────────────────────────────────────

    def stats(self, since_seconds: float | None = None) -> dict:
        """Compute aggregate latency stats, grouped by provider.

        Args:
            since_seconds: if set, only include records that finished within
                this many seconds of the call (rolling window).

        Returns:
            A dict with ``requests``, ``errors``, ``by_provider`` and
            ``slow_providers`` (sorted slowest first).
        """
        with self._lock:
            self.prune_stale_active()
            records = self._records
            if since_seconds is not None:
                cutoff = time.monotonic() - since_seconds
                records = [r for r in records if r.ended_at is not None and r.ended_at >= cutoff]

            by_provider: dict[str, dict] = {}
            for rec in records:
                entry = by_provider.setdefault(
                    rec.provider,
                    {
                        "requests": 0,
                        "errors": 0,
                        "ttfb_ms": [],
                        "total_ms": [],
                        "tokens_per_sec": [],
                    },
                )
                entry["requests"] += 1
                if rec.error is not None:
                    entry["errors"] += 1
                if rec.ttfb_seconds is not None:
                    entry["ttfb_ms"].append(_to_ms(rec.ttfb_seconds))
                if rec.total_seconds is not None:
                    entry["total_ms"].append(_to_ms(rec.total_seconds))
                if rec.tokens_per_second is not None:
                    entry["tokens_per_sec"].append(rec.tokens_per_second)

            error_count = sum(1 for r in records if r.error is not None)

            # Replace raw value lists with percentile summaries and compute
            # averages from the raw values before they are replaced.
            slow: list[tuple[str, float]] = []
            for provider, entry in by_provider.items():
                raw_total = entry["total_ms"]
                raw_ttfb = entry["ttfb_ms"]
                raw_tps = entry["tokens_per_sec"]
                entry["ttfb_ms"] = _pct_stats(raw_ttfb)
                entry["total_ms"] = _pct_stats(raw_total)
                entry["tokens_per_sec"] = _pct_stats(raw_tps)
                entry["avg_total_ms"] = round(statistics.fmean(raw_total), 2) if raw_total else 0.0
                entry["avg_ttfb_ms"] = round(statistics.fmean(raw_ttfb), 2) if raw_ttfb else 0.0
                if entry["total_ms"]["p95"] >= self.slow_provider_threshold_ms:
                    slow.append((provider, entry["total_ms"]["p95"]))

        slow.sort(key=lambda item: item[1], reverse=True)

        return {
            "requests": len(records),
            "errors": error_count,
            "in_flight": self.in_flight_count,
            "by_provider": by_provider,
            "slow_providers": [name for name, _ in slow],
            "slow_provider_p95_ms": {name: p95 for name, p95 in slow},
        }

    def format_report(self, since_seconds: float | None = None) -> str:
        """Return a human-readable report string for logging/dashboards."""
        stats = self.stats(since_seconds=since_seconds)
        lines = [
            f"Latency report: {stats['requests']} requests, {stats['errors']} errors, {stats['in_flight']} in flight",
        ]
        for provider, entry in stats["by_provider"].items():
            lines.append(
                f"  {provider}: "
                f"TTFB p50/p95/p99 = {entry['ttfb_ms']['p50']}/{entry['ttfb_ms']['p95']}/{entry['ttfb_ms']['p99']} ms, "
                f"total p50/p95/p99 = {entry['total_ms']['p50']}/{entry['total_ms']['p95']}/{entry['total_ms']['p99']} ms, "
                f"tok/s p50 = {entry['tokens_per_sec']['p50']}"
            )
        if stats["slow_providers"]:
            lines.append("SLOW PROVIDERS: " + ", ".join(stats["slow_providers"]))
        return "\n".join(lines)


# ── Module-level default instance ──────────────────────────────────────────

default_tracker = LatencyTracker()
"""Convenience singleton for applications without an explicit tracker."""


def get_tracker() -> LatencyTracker:
    """Return the module-level default tracker."""
    return default_tracker
