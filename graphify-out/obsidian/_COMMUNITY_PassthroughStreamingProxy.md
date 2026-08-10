---
type: community
cohesion: 0.15
members: 20
---

# PassthroughStreamingProxy

**Cohesion:** 0.15 - loosely connected
**Members:** 20 nodes

## Members
- [[dot-_get_client()]] - code - src/merged_agentic_swarm/streaming_proxy.py
- [[dot-_handle_health()]] - code - src/merged_agentic_swarm/streaming_proxy.py
- [[dot-_handle_messages()]] - code - src/merged_agentic_swarm/streaming_proxy.py
- [[dot-close()]] - code - src/merged_agentic_swarm/streaming_proxy.py
- [[dot-health()]] - code - src/merged_agentic_swarm/streaming_proxy.py
- [[dot-prewarm()]] - code - src/merged_agentic_swarm/streaming_proxy.py
- [[dot-proxy_request()]] - code - src/merged_agentic_swarm/streaming_proxy.py
- [[dot-router()]] - code - src/merged_agentic_swarm/streaming_proxy.py
- [[AsyncClient]] - code
- [[Check upstream health. Returns a status dict.]] - rationale - src/merged_agentic_swarm/streaming_proxy.py
- [[Close the underlying httpx client and release connections.]] - rationale - src/merged_agentic_swarm/streaming_proxy.py
- [[Forward an incoming streaming request to upstream. Reads the request body,…]] - rationale - src/merged_agentic_swarm/streaming_proxy.py
- [[PassthroughStreamingProxy]] - code - src/merged_agentic_swarm/streaming_proxy.py
- [[Pre-establish connections to the upstream. Sends a health-check request to warm…]] - rationale - src/merged_agentic_swarm/streaming_proxy.py
- [[Request]] - code
- [[Response_1]] - code
- [[Return Starlette routes for this proxy. Mount these into a parent Starlette app…]] - rationale - src/merged_agentic_swarm/streaming_proxy.py
- [[Return the shared httpx client, creating it if needed.]] - rationale - src/merged_agentic_swarm/streaming_proxy.py
- [[Route]] - code
- [[Zero-buffering SSE passthrough proxy. Accepts Anthropic Messages API streaming…]] - rationale - src/merged_agentic_swarm/streaming_proxy.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/PassthroughStreamingProxy
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_StreamingProxyConfig]]
- 3 edges to [[_COMMUNITY_CircuitBreaker]]
- 1 edge to [[_COMMUNITY__ChunkStream]]
- 1 edge to [[_COMMUNITY_test_streaming_proxy.py]]
- 1 edge to [[_COMMUNITY__StallStream]]
- 1 edge to [[_COMMUNITY_webapp.py]]

## Top bridge nodes
- [[PassthroughStreamingProxy]] - degree 16, connects to 5 communities
- [[dot-proxy_request()]] - degree 8, connects to 1 community
- [[Route]] - degree 2, connects to 1 community