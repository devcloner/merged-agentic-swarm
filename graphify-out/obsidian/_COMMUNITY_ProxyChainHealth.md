---
type: community
cohesion: 0.10
members: 38
---

# ProxyChainHealth

**Cohesion:** 0.10 - loosely connected
**Members:** 38 nodes

## Members
- [[Endpoints and request tuning for the health checks. Each field falls back to…]] - rationale - src/merged_agentic_swarm/health_check.py
- [[HealthConfig]] - code - src/merged_agentic_swarm/health_check.py
- [[ProxyChainHealth]] - code - src/merged_agentic_swarm/health_check.py
- [[Runs reachability, streaming, and provider-status checks.]] - rationale - src/merged_agentic_swarm/health_check.py
- [[_patch_client()]] - code - tests/test_health_check.py
- [[check_opencode probes the upstream opencode models endpoint.]] - rationale - tests/test_health_check.py
- [[check_opencode reports failure on HTTP 500 from upstream.]] - rationale - tests/test_health_check.py
- [[check_opencode reports failure on connection errors.]] - rationale - tests/test_health_check.py
- [[check_providers handles a plain list response (not wrapped in {data ...}).]] - rationale - tests/test_health_check.py
- [[check_providers returns routatic health + FCC models list count.]] - rationale - tests/test_health_check.py
- [[check_providers still returns routatic result even when FCC models fails.]] - rationale - tests/test_health_check.py
- [[check_routatic parses JSON health response, extracting circuit-breakers and…]] - rationale - tests/test_health_check.py
- [[check_routatic reports failure on connection errors.]] - rationale - tests/test_health_check.py
- [[check_routatic tolerates non-JSON response body gracefully.]] - rationale - tests/test_health_check.py
- [[check_streaming reports failure immediately on non-2xx response.]] - rationale - tests/test_health_check.py
- [[check_streaming reports failure on transport errors.]] - rationale - tests/test_health_check.py
- [[check_streaming reports unhealthy when no content_block_delta arrives.]] - rationale - tests/test_health_check.py
- [[run_all returns results in a predictable order including streaming.]] - rationale - tests/test_health_check.py
- [[run_all skips streaming when include_stream=False.]] - rationale - tests/test_health_check.py
- [[test_check_fcc_accepts_json_status_healthy()]] - code - tests/test_health_check.py
- [[test_check_fcc_accepts_json_status_ok()]] - code - tests/test_health_check.py
- [[test_check_fcc_connection_error_reports_fail()]] - code - tests/test_health_check.py
- [[test_check_fcc_plain_text_healthy()]] - code - tests/test_health_check.py
- [[test_check_fcc_rejects_json_status_degraded()]] - code - tests/test_health_check.py
- [[test_check_opencode_connection_error()]] - code - tests/test_health_check.py
- [[test_check_opencode_error_response()]] - code - tests/test_health_check.py
- [[test_check_opencode_happy_path()]] - code - tests/test_health_check.py
- [[test_check_providers_fcc_models_error()]] - code - tests/test_health_check.py
- [[test_check_providers_fcc_models_list_format()]] - code - tests/test_health_check.py
- [[test_check_providers_happy_path()]] - code - tests/test_health_check.py
- [[test_check_routatic_connection_error()]] - code - tests/test_health_check.py
- [[test_check_routatic_happy_path()]] - code - tests/test_health_check.py
- [[test_check_routatic_non_json_body()]] - code - tests/test_health_check.py
- [[test_check_streaming_connection_error()]] - code - tests/test_health_check.py
- [[test_check_streaming_http_error()]] - code - tests/test_health_check.py
- [[test_check_streaming_no_deltas()]] - code - tests/test_health_check.py
- [[test_run_all_stable_order()]] - code - tests/test_health_check.py
- [[test_run_all_without_stream()]] - code - tests/test_health_check.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ProxyChainHealth
SORT file.name ASC
```

## Connections to other communities
- 27 edges to [[_COMMUNITY_test_health_check.py]]
- 7 edges to [[_COMMUNITY_test_check_streaming_fcc_happy_path]]
- 6 edges to [[_COMMUNITY_dot-run_all]]
- 5 edges to [[_COMMUNITY_HopResult]]

## Top bridge nodes
- [[ProxyChainHealth]] - degree 31, connects to 4 communities
- [[HealthConfig]] - degree 27, connects to 3 communities
- [[_patch_client()]] - degree 27, connects to 2 communities
- [[test_check_opencode_connection_error()]] - degree 5, connects to 1 community
- [[test_check_opencode_error_response()]] - degree 5, connects to 1 community