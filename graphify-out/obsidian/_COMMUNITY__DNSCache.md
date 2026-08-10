---
type: community
cohesion: 0.13
members: 16
---

# _DNSCache

**Cohesion:** 0.13 - loosely connected
**Members:** 16 nodes

## Members
- [[dot-__init__()_1]] - code - src/merged_agentic_swarm/fast_pool.py
- [[dot-clear()]] - code - src/merged_agentic_swarm/fast_pool.py
- [[dot-connect_tcp()]] - code - src/merged_agentic_swarm/fast_pool.py
- [[dot-delete()]] - code - src/merged_agentic_swarm/fast_pool.py
- [[dot-get()]] - code - src/merged_agentic_swarm/fast_pool.py
- [[dot-set()]] - code - src/merged_agentic_swarm/fast_pool.py
- [[Any_2]] - code
- [[Drop one entry (used to invalidate a stale cached IP).]] - rationale - src/merged_agentic_swarm/fast_pool.py
- [[Lightweight TTL-bounded DNS cache to avoid repeated gethostbyname calls. All…]] - rationale - src/merged_agentic_swarm/fast_pool.py
- [[NetworkStream]] - code
- [[Resolve hostname to IP, consulting the in-process DNS cache first. Returns the…]] - rationale - src/merged_agentic_swarm/fast_pool.py
- [[SyncBackend]] - code
- [[_CachedDNSBackend]] - code - src/merged_agentic_swarm/fast_pool.py
- [[_DNSCache]] - code - src/merged_agentic_swarm/fast_pool.py
- [[_resolve_host()]] - code - src/merged_agentic_swarm/fast_pool.py
- [[httpcore sync backend that connects to a cached IP for each hostname.…]] - rationale - src/merged_agentic_swarm/fast_pool.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/_DNSCache
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_multi_provider_fabric.py]]

## Top bridge nodes
- [[_DNSCache]] - degree 7, connects to 1 community
- [[_CachedDNSBackend]] - degree 5, connects to 1 community
- [[_resolve_host()]] - degree 4, connects to 1 community