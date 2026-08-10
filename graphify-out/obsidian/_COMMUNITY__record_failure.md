---
type: community
cohesion: 0.18
members: 14
---

# _record_failure

**Cohesion:** 0.18 - loosely connected
**Members:** 14 nodes

## Members
- [[dot-setup_method()_13]] - code - tests/test_multi_provider_fabric.py
- [[dot-test_perma_ban_expiry_clears()]] - code - tests/test_multi_provider_fabric.py
- [[dot-test_record_failure_403_trips_circuit_breaker()]] - code - tests/test_multi_provider_fabric.py
- [[dot-test_record_failure_circuit_breaker()]] - code - tests/test_multi_provider_fabric.py
- [[dot-test_record_failure_perma_ban_401()]] - code - tests/test_multi_provider_fabric.py
- [[dot-test_record_success_resets()]] - code - tests/test_multi_provider_fabric.py
- [[Atomically write the perma-ban map to disk. Caller must hold _fabric_lock.]] - rationale - src/merged_agentic_swarm/providers/multi_provider_fabric.py
- [[Provider should be retried after perma-ban duration expires.]] - rationale - tests/test_multi_provider_fabric.py
- [[Record a provider failure — perma-ban on 401 auth errors, circuit-break on…]] - rationale - src/merged_agentic_swarm/providers/multi_provider_fabric.py
- [[Record a provider success — reset circuit breaker and update last-working cache.]] - rationale - src/merged_agentic_swarm/providers/multi_provider_fabric.py
- [[TestCircuitBreaker_1]] - code - tests/test_multi_provider_fabric.py
- [[_persist_bans()]] - code - src/merged_agentic_swarm/providers/multi_provider_fabric.py
- [[_record_failure()]] - code - src/merged_agentic_swarm/providers/multi_provider_fabric.py
- [[_record_success()]] - code - src/merged_agentic_swarm/providers/multi_provider_fabric.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/_record_failure
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_multi_provider_fabric.py]]
- 4 edges to [[_COMMUNITY_MultiProviderFabric]]
- 1 edge to [[_COMMUNITY_KeyPoolManager]]
- 1 edge to [[_COMMUNITY_test_multi_provider_fabric.py]]

## Top bridge nodes
- [[TestCircuitBreaker_1]] - degree 9, connects to 3 communities
- [[_record_failure()]] - degree 9, connects to 2 communities
- [[_record_success()]] - degree 5, connects to 2 communities
- [[_persist_bans()]] - degree 3, connects to 1 community
- [[dot-test_perma_ban_expiry_clears()]] - degree 3, connects to 1 community