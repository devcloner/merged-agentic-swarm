---
type: community
cohesion: 0.13
members: 21
---

# TestDispatchRequest

**Cohesion:** 0.13 - loosely connected
**Members:** 21 nodes

## Members
- [[dot-_block_all_providers()]] - code - tests/test_multi_provider_fabric.py
- [[dot-setup_method()_15]] - code - tests/test_multi_provider_fabric.py
- [[dot-test_consecutive_429s_trip_circuit_breaker()]] - code - tests/test_multi_provider_fabric.py
- [[dot-test_dispatch_http_status_error_triggers_cascade()]] - code - tests/test_multi_provider_fabric.py
- [[dot-test_dispatch_non_dict_json_body_falls_through()]] - code - tests/test_multi_provider_fabric.py
- [[dot-test_dispatch_non_json_body_falls_through()]] - code - tests/test_multi_provider_fabric.py
- [[dot-test_dispatch_successful_call()]] - code - tests/test_multi_provider_fabric.py
- [[dot-test_dispatch_with_context_objects()]] - code - tests/test_multi_provider_fabric.py
- [[dot-test_simulation_fallback()]] - code - tests/test_multi_provider_fabric.py
- [[dot-test_skip_perma_banned_provider()]] - code - tests/test_multi_provider_fabric.py
- [[4xx5xx from dispatch() must be caught by HTTPStatusError handling.]] - rationale - tests/test_multi_provider_fabric.py
- [[A 2xx with a non-dict JSON body must cascade, not crash on .get().]] - rationale - tests/test_multi_provider_fabric.py
- [[A 2xx with an emptynon-JSON body must cascade, not raise JSONDecodeError.]] - rationale - tests/test_multi_provider_fabric.py
- [[Block all real providers so dispatch falls to simulation.]] - rationale - tests/test_multi_provider_fabric.py
- [[Consecutive 429 responses must count as a provider circuit-breaker event (not…]] - rationale - tests/test_multi_provider_fabric.py
- [[Provider under perma-ban should be skipped.]] - rationale - tests/test_multi_provider_fabric.py
- [[Test a successful API call returns formatted Anthropic response.]] - rationale - tests/test_multi_provider_fabric.py
- [[Test that content blocks (list) are flattened correctly before dispatch.]] - rationale - tests/test_multi_provider_fabric.py
- [[TestDispatchRequest]] - code - tests/test_multi_provider_fabric.py
- [[Without any working providers, should fall through to simulation.]] - rationale - tests/test_multi_provider_fabric.py
- [[patch_1]] - code

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/TestDispatchRequest
SORT file.name ASC
```

## Connections to other communities
- 9 edges to [[_COMMUNITY_MultiProviderFabric]]
- 2 edges to [[_COMMUNITY_KeyPoolManager]]
- 1 edge to [[_COMMUNITY_test_multi_provider_fabric.py]]

## Top bridge nodes
- [[TestDispatchRequest]] - degree 13, connects to 3 communities
- [[dot-test_consecutive_429s_trip_circuit_breaker()]] - degree 5, connects to 2 communities
- [[dot-test_dispatch_http_status_error_triggers_cascade()]] - degree 4, connects to 1 community
- [[dot-test_dispatch_non_dict_json_body_falls_through()]] - degree 4, connects to 1 community
- [[dot-test_dispatch_non_json_body_falls_through()]] - degree 4, connects to 1 community