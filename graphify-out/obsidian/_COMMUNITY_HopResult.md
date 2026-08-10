---
type: community
cohesion: 0.11
members: 30
---

# HopResult

**Cohesion:** 0.11 - loosely connected
**Members:** 30 nodes

## Members
- [[dot-as_dict()]] - code - src/merged_agentic_swarm/health_check.py
- [[Any_3]] - code
- [[ArgumentParser]] - code
- [[HopResult]] - code - src/merged_agentic_swarm/health_check.py
- [[Namespace]] - code
- [[Outcome of a single health check.]] - rationale - src/merged_agentic_swarm/health_check.py
- [[Proxy-chain health check for the merged agentic swarm. Verifies the full proxy…]] - rationale - src/merged_agentic_swarm/health_check.py
- [[_build_parser()]] - code - src/merged_agentic_swarm/health_check.py
- [[_print_header()]] - code - src/merged_agentic_swarm/health_check.py
- [[_print_human includes TTFB when present in meta.]] - rationale - tests/test_health_check.py
- [[_print_human renders FAIL with detail.]] - rationale - tests/test_health_check.py
- [[_print_human renders PASS with latency and metadata.]] - rationale - tests/test_health_check.py
- [[_print_human renders open circuit breakers.]] - rationale - tests/test_health_check.py
- [[_print_human()]] - code - src/merged_agentic_swarm/health_check.py
- [[_report emits JSON and returns 0 for healthy.]] - rationale - tests/test_health_check.py
- [[_report emits JSON with degraded status and returns 1.]] - rationale - tests/test_health_check.py
- [[_report renders DEGRADED and returns 1 when checks fail.]] - rationale - tests/test_health_check.py
- [[_report renders HEALTHY when all checks pass.]] - rationale - tests/test_health_check.py
- [[_report()]] - code - src/merged_agentic_swarm/health_check.py
- [[_run_command()]] - code - src/merged_agentic_swarm/health_check.py
- [[health_check.py]] - code - src/merged_agentic_swarm/health_check.py
- [[main()_4]] - code - src/merged_agentic_swarm/health_check.py
- [[test_print_human_circuit_breakers()]] - code - tests/test_health_check.py
- [[test_print_human_fail()]] - code - tests/test_health_check.py
- [[test_print_human_pass()]] - code - tests/test_health_check.py
- [[test_print_human_ttfb_rendering()]] - code - tests/test_health_check.py
- [[test_report_human_degraded()]] - code - tests/test_health_check.py
- [[test_report_human_healthy()]] - code - tests/test_health_check.py
- [[test_report_json_degraded()]] - code - tests/test_health_check.py
- [[test_report_json_healthy()]] - code - tests/test_health_check.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/HopResult
SORT file.name ASC
```

## Connections to other communities
- 14 edges to [[_COMMUNITY_test_health_check.py]]
- 10 edges to [[_COMMUNITY_dot-run_all]]
- 5 edges to [[_COMMUNITY_ProxyChainHealth]]
- 1 edge to [[_COMMUNITY_test_streaming_proxy.py]]
- 1 edge to [[_COMMUNITY_test_check_streaming_fcc_happy_path]]

## Top bridge nodes
- [[health_check.py]] - degree 13, connects to 4 communities
- [[main()_4]] - degree 12, connects to 2 communities
- [[_run_command()]] - degree 9, connects to 2 communities
- [[HopResult]] - degree 20, connects to 1 community
- [[test_print_human_circuit_breakers()]] - degree 4, connects to 1 community