---
type: community
cohesion: 0.29
members: 7
---

# _StallStream

**Cohesion:** 0.29 - loosely connected
**Members:** 7 nodes

## Members
- [[dot-__aiter__()_1]] - code - tests/test_streaming_proxy.py
- [[dot-__init__()_32]] - code - tests/test_streaming_proxy.py
- [[dot-aclose()_1]] - code - tests/test_streaming_proxy.py
- [[Async byte stream that never yields (simulates a stalled upstream).]] - rationale - tests/test_streaming_proxy.py
- [[Consume (or close) a StreamingResponse so upstream streams are torn down.]] - rationale - tests/test_streaming_proxy.py
- [[_StallStream]] - code - tests/test_streaming_proxy.py
- [[drain()]] - code - tests/test_streaming_proxy.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/_StallStream
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_test_streaming_proxy.py]]
- 1 edge to [[_COMMUNITY_StreamingProxyConfig]]
- 1 edge to [[_COMMUNITY_CircuitBreaker]]
- 1 edge to [[_COMMUNITY_PassthroughStreamingProxy]]

## Top bridge nodes
- [[_StallStream]] - degree 8, connects to 4 communities
- [[drain()]] - degree 5, connects to 1 community
- [[dot-aclose()_1]] - degree 4, connects to 1 community