---
type: community
cohesion: 0.29
members: 7
---

# _ChunkStream

**Cohesion:** 0.29 - loosely connected
**Members:** 7 nodes

## Members
- [[dot-__aiter__()]] - code - tests/test_streaming_proxy.py
- [[dot-__init__()_31]] - code - tests/test_streaming_proxy.py
- [[dot-aclose()]] - code - tests/test_streaming_proxy.py
- [[Async byte stream over a fixed list of chunks. Optionally raises ``exc`` after…]] - rationale - tests/test_streaming_proxy.py
- [[Build an upstream ``httpx.Response`` that streams ``chunks`` as SSE.]] - rationale - tests/test_streaming_proxy.py
- [[_ChunkStream]] - code - tests/test_streaming_proxy.py
- [[_sse_response()]] - code - tests/test_streaming_proxy.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/_ChunkStream
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_test_streaming_proxy.py]]
- 1 edge to [[_COMMUNITY_StreamingProxyConfig]]
- 1 edge to [[_COMMUNITY_CircuitBreaker]]
- 1 edge to [[_COMMUNITY_PassthroughStreamingProxy]]

## Top bridge nodes
- [[_ChunkStream]] - degree 9, connects to 4 communities
- [[_sse_response()]] - degree 3, connects to 1 community