---
type: community
cohesion: 0.14
members: 14
---

# CircuitBreaker

**Cohesion:** 0.14 - loosely connected
**Members:** 14 nodes

## Members
- [[dot-__init__()_22]] - code - src/merged_agentic_swarm/streaming_proxy.py
- [[dot-__init__()_23]] - code - src/merged_agentic_swarm/streaming_proxy.py
- [[dot-failure_count()]] - code - src/merged_agentic_swarm/streaming_proxy.py
- [[dot-is_open()]] - code - src/merged_agentic_swarm/streaming_proxy.py
- [[dot-record_failure()]] - code - src/merged_agentic_swarm/streaming_proxy.py
- [[dot-record_success()]] - code - src/merged_agentic_swarm/streaming_proxy.py
- [[AsyncBaseTransport]] - code
- [[CircuitBreaker]] - code - src/merged_agentic_swarm/streaming_proxy.py
- [[Current consecutive failure count.]] - rationale - src/merged_agentic_swarm/streaming_proxy.py
- [[Increment the failure counter; open circuit if threshold reached.]] - rationale - src/merged_agentic_swarm/streaming_proxy.py
- [[Reset the failure counter after a successful request.]] - rationale - src/merged_agentic_swarm/streaming_proxy.py
- [[Simple fail-fast circuit breaker. Tracks consecutive failures. After…]] - rationale - src/merged_agentic_swarm/streaming_proxy.py
- [[True when the circuit is open (requests should be rejected).]] - rationale - src/merged_agentic_swarm/streaming_proxy.py
- [[test_circuit_breaker_unit_transitions()]] - code - tests/test_streaming_proxy.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/CircuitBreaker
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_PassthroughStreamingProxy]]
- 2 edges to [[_COMMUNITY_StreamingProxyConfig]]
- 2 edges to [[_COMMUNITY_test_streaming_proxy.py]]
- 1 edge to [[_COMMUNITY__ChunkStream]]
- 1 edge to [[_COMMUNITY__StallStream]]

## Top bridge nodes
- [[CircuitBreaker]] - degree 11, connects to 3 communities
- [[dot-__init__()_23]] - degree 4, connects to 2 communities
- [[dot-record_failure()]] - degree 3, connects to 1 community
- [[dot-record_success()]] - degree 3, connects to 1 community
- [[test_circuit_breaker_unit_transitions()]] - degree 3, connects to 1 community