---
type: community
cohesion: 0.05
members: 54
---

# LatencyTracker

**Cohesion:** 0.05 - loosely connected
**Members:** 54 nodes

## Members
- [[dot-__init__()_4]] - code - src/merged_agentic_swarm/latency_tracker.py
- [[dot-fail()]] - code - src/merged_agentic_swarm/latency_tracker.py
- [[dot-finish()]] - code - src/merged_agentic_swarm/latency_tracker.py
- [[dot-format_report()]] - code - src/merged_agentic_swarm/latency_tracker.py
- [[dot-in_flight_count()]] - code - src/merged_agentic_swarm/latency_tracker.py
- [[dot-mark_first_byte()_1]] - code - src/merged_agentic_swarm/latency_tracker.py
- [[dot-mark_first_byte()]] - code - src/merged_agentic_swarm/latency_tracker.py
- [[dot-prune_stale_active()]] - code - src/merged_agentic_swarm/latency_tracker.py
- [[dot-record_count()]] - code - src/merged_agentic_swarm/latency_tracker.py
- [[dot-reset()_1]] - code - src/merged_agentic_swarm/latency_tracker.py
- [[dot-start_request()]] - code - src/merged_agentic_swarm/latency_tracker.py
- [[dot-stats()]] - code - src/merged_agentic_swarm/latency_tracker.py
- [[dot-tokens_per_second()]] - code - src/merged_agentic_swarm/latency_tracker.py
- [[dot-total_seconds()]] - code - src/merged_agentic_swarm/latency_tracker.py
- [[dot-ttfb_seconds()]] - code - src/merged_agentic_swarm/latency_tracker.py
- [[Aggregates per-request streaming latency stats, grouped by provider. Thread-…]] - rationale - src/merged_agentic_swarm/latency_tracker.py
- [[Begin tracking a request and return its timing record.]] - rationale - src/merged_agentic_swarm/latency_tracker.py
- [[Compute aggregate latency stats, grouped by provider. Args since_seconds if…]] - rationale - src/merged_agentic_swarm/latency_tracker.py
- [[Drop all retained records and any in-flight timings.]] - rationale - src/merged_agentic_swarm/latency_tracker.py
- [[Drop in-flight records abandoned before meth`finish`. A caller that raises…]] - rationale - src/merged_agentic_swarm/latency_tracker.py
- [[Finalize a request as failed.]] - rationale - src/merged_agentic_swarm/latency_tracker.py
- [[Finalize a request. ``error=None`` marks it completed.]] - rationale - src/merged_agentic_swarm/latency_tracker.py
- [[LatencyTracker]] - code - src/merged_agentic_swarm/latency_tracker.py
- [[Mutable timing record for a single streaming request. Call sites mutate this…]] - rationale - src/merged_agentic_swarm/latency_tracker.py
- [[Nearest-rank percentile of an already-sorted ascending list. Returns 0.0 for an…]] - rationale - src/merged_agentic_swarm/latency_tracker.py
- [[Number of finished records currently retained.]] - rationale - src/merged_agentic_swarm/latency_tracker.py
- [[Number of requests currently being tracked (stale ones excluded).]] - rationale - src/merged_agentic_swarm/latency_tracker.py
- [[Per-request streaming latency tracking and provider health reporting. Tracks…]] - rationale - src/merged_agentic_swarm/latency_tracker.py
- [[Record the first-byte (TTFB) moment on a timing record.]] - rationale - src/merged_agentic_swarm/latency_tracker.py
- [[Record the first-byte (TTFB) moment. Idempotent per request.]] - rationale - src/merged_agentic_swarm/latency_tracker.py
- [[RequestTiming]] - code - src/merged_agentic_swarm/latency_tracker.py
- [[Return a human-readable report string for loggingdashboards.]] - rationale - src/merged_agentic_swarm/latency_tracker.py
- [[Return a p50p95p99 summary dict for a list of raw values.]] - rationale - src/merged_agentic_swarm/latency_tracker.py
- [[Return the module-level default tracker.]] - rationale - src/merged_agentic_swarm/latency_tracker.py
- [[Streaming throughput in tokenssec, or None if not computable.]] - rationale - src/merged_agentic_swarm/latency_tracker.py
- [[Time-to-first-byte in seconds, or None if no byte was received.]] - rationale - src/merged_agentic_swarm/latency_tracker.py
- [[Total request duration in seconds, or None if still in flight.]] - rationale - src/merged_agentic_swarm/latency_tracker.py
- [[_pct_stats()]] - code - src/merged_agentic_swarm/latency_tracker.py
- [[_to_ms()]] - code - src/merged_agentic_swarm/latency_tracker.py
- [[get_tracker()]] - code - src/merged_agentic_swarm/latency_tracker.py
- [[latency_tracker.py]] - code - src/merged_agentic_swarm/latency_tracker.py
- [[percentile()]] - code - src/merged_agentic_swarm/latency_tracker.py
- [[test_format_report_empty_and_populated()]] - code - tests/test_latency_tracker.py
- [[test_get_tracker_returns_default_singleton()]] - code - tests/test_latency_tracker.py
- [[test_in_flight_count_excludes_stale()]] - code - tests/test_latency_tracker.py
- [[test_latency_tracker.py]] - code - tests/test_latency_tracker.py
- [[test_percentile_and_pct_stats_edge_cases()]] - code - tests/test_latency_tracker.py
- [[test_prune_keeps_recent_in_flight()]] - code - tests/test_latency_tracker.py
- [[test_prune_stale_active_finalizes_abandoned()]] - code - tests/test_latency_tracker.py
- [[test_request_timing_lifecycle()]] - code - tests/test_latency_tracker.py
- [[test_stats_aggregation_and_fail_count()]] - code - tests/test_latency_tracker.py
- [[test_stats_prunes_stale_before_reporting()]] - code - tests/test_latency_tracker.py
- [[test_tracker_bookkeeping_and_finish_fail()]] - code - tests/test_latency_tracker.py
- [[test_zero_stale_threshold_disables_pruning()]] - code - tests/test_latency_tracker.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/LatencyTracker
SORT file.name ASC
```
