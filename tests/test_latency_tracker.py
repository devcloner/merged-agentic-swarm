import time

import pytest

from merged_agentic_swarm.latency_tracker import (
    LatencyTracker,
    _pct_stats,
    get_tracker,
    percentile,
)


def test_percentile_and_pct_stats_edge_cases():
    assert percentile([], 50) == 0.0
    assert percentile([7], 0) == 7
    assert percentile([7], 100) == 7
    assert percentile([1, 2, 3, 4], 0) == 1
    assert percentile([1, 2, 3, 4], 100) == 4
    assert percentile([1, 2, 3, 4], 50) == 2
    assert _pct_stats([]) == {"p50": 0.0, "p95": 0.0, "p99": 0.0}
    assert _pct_stats([3.14159]) == {"p50": 3.14, "p95": 3.14, "p99": 3.14}
    # nearest-rank percentile: rank = ceil(0.95 * 4) = 4 -> sorted[3] == 4
    assert _pct_stats([4, 1, 2, 3]) == {"p50": 2, "p95": 4, "p99": 4}


def test_request_timing_lifecycle(monkeypatch):
    clock = iter([10.25, 11.0])
    monkeypatch.setattr("merged_agentic_swarm.latency_tracker.time.monotonic", lambda: next(clock))
    tracker = LatencyTracker()
    timing = tracker.start_request("provider", "model", "request")
    timing.started_at = 10.0
    assert timing.ttfb_seconds is None
    assert timing.total_seconds is None
    tracker.mark_first_byte(timing)
    assert timing.ttfb_seconds == pytest.approx(0.25)
    tracker.finish(timing, total_tokens=100)
    assert timing.total_seconds == pytest.approx(1.0)
    assert timing.tokens_per_second == pytest.approx(100 / 1.0)


def test_tracker_bookkeeping_and_finish_fail():
    tracker = LatencyTracker()
    success = tracker.start_request("p", "m", "success")
    failed = tracker.start_request("p", "m", "failed")
    assert tracker.record_count == 0
    assert tracker.in_flight_count == 2
    tracker.finish(success, total_tokens=4)
    assert tracker.record_count == 1
    assert tracker.in_flight_count == 1
    tracker.fail(failed, "upstream error")
    assert tracker.record_count == 2
    assert tracker.in_flight_count == 0


def test_stats_aggregation_and_fail_count(monkeypatch):
    times = iter([0.1, 1.0, 2.2, 4.0])
    monkeypatch.setattr("merged_agentic_swarm.latency_tracker.time.monotonic", lambda: next(times))
    tracker = LatencyTracker(slow_provider_threshold_ms=2500)
    first = tracker.start_request("api", "m", "one")
    first.started_at = 0.0
    tracker.mark_first_byte(first)
    tracker.finish(first, total_tokens=10)
    second = tracker.start_request("api", "m", "two")
    second.started_at = 2.0
    tracker.mark_first_byte(second)
    tracker.fail(second, "timeout")
    stats = tracker.stats()
    entry = stats["by_provider"]["api"]
    assert stats["requests"] == 2
    assert stats["errors"] == 1
    assert entry["errors"] == 1
    # Both requests end with a total time (the failed one is finalized too):
    # [1000ms, 2000ms] -> avg 1500ms.
    # nearest-rank: ceil(0.5*2)=1, ceil(0.95*2)=2, ceil(0.99*2)=2.
    assert entry["avg_total_ms"] == pytest.approx(1500.0)
    assert entry["total_ms"]["p50"] == 1000.0
    assert entry["total_ms"]["p95"] == 2000.0
    assert entry["total_ms"]["p99"] == 2000.0
    assert entry["total_ms"]["p50"] <= entry["total_ms"]["p95"]
    assert "min_total_ms" not in entry
    assert "max_total_ms" not in entry
    assert stats["slow_providers"] == []


def test_format_report_empty_and_populated():
    tracker = LatencyTracker()
    report = tracker.format_report()
    assert "Latency report:" in report
    assert "0 requests" in report
    timing = tracker.start_request("provider", "model", "id")
    tracker.finish(timing, total_tokens=1)
    report = tracker.format_report()
    assert "provider:" in report
    assert "TTFB p50/p95/p99" in report
    assert "total p50/p95/p99" in report


def test_get_tracker_returns_default_singleton():
    assert isinstance(get_tracker(), LatencyTracker)
    assert get_tracker() is get_tracker()


# ── Stale active-record pruning (#38) ─────────────────────────────────────


def test_prune_stale_active_finalizes_abandoned():
    tracker = LatencyTracker(active_stale_seconds=10.0)
    timing = tracker.start_request("p", "m", "r1")
    timing.started_at = time.monotonic() - 15.0
    assert tracker.prune_stale_active() == 1
    assert tracker.in_flight_count == 0
    assert tracker.record_count == 1
    rec = tracker._records[0]
    assert rec.error == "pruned: abandoned before finish"
    assert rec.completed is False


def test_prune_keeps_recent_in_flight():
    tracker = LatencyTracker(active_stale_seconds=10.0)
    tracker.start_request("p", "m", "fresh")
    assert tracker.prune_stale_active() == 0
    assert tracker.in_flight_count == 1


def test_in_flight_count_excludes_stale():
    tracker = LatencyTracker(active_stale_seconds=10.0)
    fresh = tracker.start_request("p", "m", "fresh")
    stale = tracker.start_request("p", "m", "stale")
    now = time.monotonic()
    stale.started_at = now - 20.0
    fresh.started_at = now
    assert tracker.in_flight_count == 1  # only the fresh one counts


def test_zero_stale_threshold_disables_pruning():
    tracker = LatencyTracker(active_stale_seconds=0)
    tracker.start_request("p", "m", "r1")
    assert tracker.prune_stale_active() == 0
    assert tracker.in_flight_count == 1


def test_stats_prunes_stale_before_reporting():
    tracker = LatencyTracker(active_stale_seconds=10.0)
    timing = tracker.start_request("p", "m", "r1")
    timing.started_at = time.monotonic() - 20.0
    stats = tracker.stats()
    assert stats["requests"] == 1
    assert stats["errors"] == 1
    assert stats["in_flight"] == 0
