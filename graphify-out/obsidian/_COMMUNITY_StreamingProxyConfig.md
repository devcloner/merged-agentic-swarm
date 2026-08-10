---
type: community
cohesion: 0.22
members: 11
---

# StreamingProxyConfig

**Cohesion:** 0.22 - loosely connected
**Members:** 11 nodes

## Members
- [[dot-as_asgi_app()]] - code - src/merged_agentic_swarm/streaming_proxy.py
- [[Configuration for the zero-buffering streaming proxy.]] - rationale - src/merged_agentic_swarm/streaming_proxy.py
- [[Create a configured streaming proxy Starlette app in one call.]] - rationale - src/merged_agentic_swarm/streaming_proxy.py
- [[Return a standalone Starlette ASGI application.]] - rationale - src/merged_agentic_swarm/streaming_proxy.py
- [[Starlette]] - code
- [[StreamingProxyConfig]] - code - src/merged_agentic_swarm/streaming_proxy.py
- [[Zero-buffering streaming passthrough proxy for Anthropic Messages API. Accepts…]] - rationale - src/merged_agentic_swarm/streaming_proxy.py
- [[create_streaming_proxy_app()]] - code - src/merged_agentic_swarm/streaming_proxy.py
- [[streaming_proxy.py]] - code - src/merged_agentic_swarm/streaming_proxy.py
- [[test_config_defaults()]] - code - tests/test_streaming_proxy.py
- [[test_create_streaming_proxy_app_factory()]] - code - tests/test_streaming_proxy.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/StreamingProxyConfig
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_test_streaming_proxy.py]]
- 3 edges to [[_COMMUNITY_PassthroughStreamingProxy]]
- 2 edges to [[_COMMUNITY_CircuitBreaker]]
- 1 edge to [[_COMMUNITY__ChunkStream]]
- 1 edge to [[_COMMUNITY__StallStream]]

## Top bridge nodes
- [[StreamingProxyConfig]] - degree 8, connects to 4 communities
- [[streaming_proxy.py]] - degree 7, connects to 3 communities
- [[create_streaming_proxy_app()]] - degree 7, connects to 1 community
- [[dot-as_asgi_app()]] - degree 4, connects to 1 community
- [[test_config_defaults()]] - degree 2, connects to 1 community