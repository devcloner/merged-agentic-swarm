---
type: community
cohesion: 0.25
members: 8
---

# .load_keys

**Cohesion:** 0.25 - loosely connected
**Members:** 8 nodes

## Members
- [[dot-__init__()_5]] - code - src/merged_agentic_swarm/providers/key_pool.py
- [[dot-_collect_keys_from_sources()]] - code - src/merged_agentic_swarm/providers/key_pool.py
- [[dot-add_key()]] - code - src/merged_agentic_swarm/providers/key_pool.py
- [[dot-load_keys()]] - code - src/merged_agentic_swarm/providers/key_pool.py
- [[dot-reload()]] - code - src/merged_agentic_swarm/providers/key_pool.py
- [[Gather (provider, secret_value, key_id) candidates from all key sources.…]] - rationale - src/merged_agentic_swarm/providers/key_pool.py
- [[Hot-reload keys from all sources, preserving runtime stats for persistent keys.…]] - rationale - src/merged_agentic_swarm/providers/key_pool.py
- [[Loads API keys from env file, environment variables, and local key files.]] - rationale - src/merged_agentic_swarm/providers/key_pool.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/load_keys
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_KeyPoolManager]]
- 2 edges to [[_COMMUNITY_APIKeyInfo]]

## Top bridge nodes
- [[dot-reload()]] - degree 4, connects to 2 communities
- [[dot-add_key()]] - degree 3, connects to 2 communities
- [[dot-load_keys()]] - degree 5, connects to 1 community
- [[dot-_collect_keys_from_sources()]] - degree 4, connects to 1 community
- [[dot-__init__()_5]] - degree 2, connects to 1 community