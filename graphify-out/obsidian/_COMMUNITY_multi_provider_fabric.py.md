---
type: community
cohesion: 0.10
members: 32
---

# multi_provider_fabric.py

**Cohesion:** 0.10 - loosely connected
**Members:** 32 nodes

## Members
- [[dot-__init__()_2]] - code - src/merged_agentic_swarm/fast_pool.py
- [[Build an httpx transport with connection pooling, keepalive, and DNS cache.]] - rationale - src/merged_agentic_swarm/fast_pool.py
- [[Clear the overlay cache so the next dispatch re-reads the JSON file.]] - rationale - src/merged_agentic_swarm/providers/multi_provider_fabric.py
- [[Client]] - code
- [[Close the current thread's httpx client (called at thread shutdown).]] - rationale - src/merged_agentic_swarm/fast_pool.py
- [[Connection-pool tunables for the multi-provider fabric.]] - rationale - src/merged_agentic_swarm/fast_pool.py
- [[Create a fresh httpx.Client with connection pooling. Each thread gets its own…]] - rationale - src/merged_agentic_swarm/fast_pool.py
- [[Fast HTTP Connection Pool — latency-optimized transport for multi-provider…]] - rationale - src/merged_agentic_swarm/fast_pool.py
- [[FastPoolConfig]] - code - src/merged_agentic_swarm/fast_pool.py
- [[HTTPTransport]] - code
- [[Limits]] - code
- [[Load persisted perma-bans into _permanently_dead, dropping expired entries.]] - rationale - src/merged_agentic_swarm/providers/multi_provider_fabric.py
- [[Multi-Backend Model Fabric Routes requests across providers with priority…]] - rationale - src/merged_agentic_swarm/providers/multi_provider_fabric.py
- [[Pre-warm DNS + TLS handshake for a list of hostnames. Opens a TCP connection to…]] - rationale - src/merged_agentic_swarm/fast_pool.py
- [[Pre-warm connections to all known provider hosts. Call at startup.]] - rationale - src/merged_agentic_swarm/fast_pool.py
- [[Response]] - code
- [[Return the thread-local httpx client, creating one on first access. Within a…]] - rationale - src/merged_agentic_swarm/fast_pool.py
- [[Send a POST request through the pooled client and return the response.…]] - rationale - src/merged_agentic_swarm/fast_pool.py
- [[_PooledTransport]] - code - src/merged_agentic_swarm/fast_pool.py
- [[_build_transport()]] - code - src/merged_agentic_swarm/fast_pool.py
- [[_create_client()]] - code - src/merged_agentic_swarm/fast_pool.py
- [[_load_bans()]] - code - src/merged_agentic_swarm/providers/multi_provider_fabric.py
- [[``httpx.HTTPTransport`` whose httpcore pool uses the DNS-cached backend.…]] - rationale - src/merged_agentic_swarm/fast_pool.py
- [[client()]] - code - tests/test_webapp.py
- [[close_thread_client()]] - code - src/merged_agentic_swarm/fast_pool.py
- [[dispatch()]] - code - src/merged_agentic_swarm/fast_pool.py
- [[fast_pool.py]] - code - src/merged_agentic_swarm/fast_pool.py
- [[get_client()]] - code - src/merged_agentic_swarm/fast_pool.py
- [[multi_provider_fabric.py]] - code - src/merged_agentic_swarm/providers/multi_provider_fabric.py
- [[prewarm_hosts()]] - code - src/merged_agentic_swarm/fast_pool.py
- [[reload_fabric_routes()]] - code - src/merged_agentic_swarm/providers/multi_provider_fabric.py
- [[warm_all()]] - code - src/merged_agentic_swarm/fast_pool.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/multi_provider_fabricpy
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY__FakeClient]]
- 4 edges to [[_COMMUNITY__DNSCache]]
- 3 edges to [[_COMMUNITY_FastFallbackRouter]]
- 3 edges to [[_COMMUNITY_claude_proxy_server.py]]
- 3 edges to [[_COMMUNITY__record_failure]]
- 2 edges to [[_COMMUNITY_APIKeyInfo]]
- 2 edges to [[_COMMUNITY_MultiProviderFabric]]
- 2 edges to [[_COMMUNITY_webapp.py]]
- 1 edge to [[_COMMUNITY_ProxyServerDaemon]]
- 1 edge to [[_COMMUNITY_AgenticWorkerLoop]]
- 1 edge to [[_COMMUNITY_SubTask]]
- 1 edge to [[_COMMUNITY_WorkerRole]]
- 1 edge to [[_COMMUNITY__router_with_keys]]
- 1 edge to [[_COMMUNITY_test_multi_provider_fabric.py]]
- 1 edge to [[_COMMUNITY_test_webapp.py]]
- 1 edge to [[_COMMUNITY_TestChains]]

## Top bridge nodes
- [[multi_provider_fabric.py]] - degree 20, connects to 11 communities
- [[fast_pool.py]] - degree 17, connects to 4 communities
- [[dispatch()]] - degree 9, connects to 2 communities
- [[warm_all()]] - degree 6, connects to 2 communities
- [[client()]] - degree 4, connects to 2 communities