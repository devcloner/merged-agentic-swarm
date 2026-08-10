---
source_file: "src/merged_agentic_swarm/latency_tracker.py"
type: "code"
community: "LatencyTracker"
location: "L136"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/LatencyTracker
---

# LatencyTracker

## Connections
- [[dot-__init__()_4]] - `method` [EXTRACTED]
- [[dot-fail()]] - `method` [EXTRACTED]
- [[dot-finish()]] - `method` [EXTRACTED]
- [[dot-format_report()]] - `method` [EXTRACTED]
- [[dot-in_flight_count()]] - `method` [EXTRACTED]
- [[dot-mark_first_byte()_1]] - `method` [EXTRACTED]
- [[dot-prune_stale_active()]] - `method` [EXTRACTED]
- [[dot-record_count()]] - `method` [EXTRACTED]
- [[dot-reset()_1]] - `method` [EXTRACTED]
- [[dot-start_request()]] - `method` [EXTRACTED]
- [[dot-stats()]] - `method` [EXTRACTED]
- [[Aggregates per-request streaming latency stats, grouped by provider. Thread-…]] - `rationale_for` [EXTRACTED]
- [[get_tracker()]] - `references` [EXTRACTED]
- [[latency_tracker.py]] - `contains` [EXTRACTED]
- [[test_format_report_empty_and_populated()]] - `calls` [EXTRACTED]
- [[test_in_flight_count_excludes_stale()]] - `calls` [EXTRACTED]
- [[test_prune_keeps_recent_in_flight()]] - `calls` [EXTRACTED]
- [[test_prune_stale_active_finalizes_abandoned()]] - `calls` [EXTRACTED]
- [[test_request_timing_lifecycle()]] - `calls` [EXTRACTED]
- [[test_stats_aggregation_and_fail_count()]] - `calls` [EXTRACTED]
- [[test_stats_prunes_stale_before_reporting()]] - `calls` [EXTRACTED]
- [[test_tracker_bookkeeping_and_finish_fail()]] - `calls` [EXTRACTED]
- [[test_zero_stale_threshold_disables_pruning()]] - `calls` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/LatencyTracker