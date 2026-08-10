---
source_file: "tests/test_latency_tracker.py"
type: "code"
community: "LatencyTracker"
location: "L1"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/LatencyTracker
---

# test_latency_tracker.py

## Connections
- [[latency_tracker.py]] - `imports_from` [EXTRACTED]
- [[test_format_report_empty_and_populated()]] - `contains` [EXTRACTED]
- [[test_get_tracker_returns_default_singleton()]] - `contains` [EXTRACTED]
- [[test_in_flight_count_excludes_stale()]] - `contains` [EXTRACTED]
- [[test_percentile_and_pct_stats_edge_cases()]] - `contains` [EXTRACTED]
- [[test_prune_keeps_recent_in_flight()]] - `contains` [EXTRACTED]
- [[test_prune_stale_active_finalizes_abandoned()]] - `contains` [EXTRACTED]
- [[test_request_timing_lifecycle()]] - `contains` [EXTRACTED]
- [[test_stats_aggregation_and_fail_count()]] - `contains` [EXTRACTED]
- [[test_stats_prunes_stale_before_reporting()]] - `contains` [EXTRACTED]
- [[test_tracker_bookkeeping_and_finish_fail()]] - `contains` [EXTRACTED]
- [[test_zero_stale_threshold_disables_pruning()]] - `contains` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/LatencyTracker