---
type: community
cohesion: 0.25
members: 8
---

# _run_latency_test

**Cohesion:** 0.25 - loosely connected
**Members:** 8 nodes

## Members
- [[AsyncClient_1]] - code
- [[Exception]] - code
- [[Live litellm v1models aliases; on failure (aliases=, note).]] - rationale - src/merged_agentic_swarm/webapp.py
- [[Stream one chatcompletions request; report TTFB and total wall time.]] - rationale - src/merged_agentic_swarm/webapp.py
- [[_fetch_litellm_aliases()]] - code - src/merged_agentic_swarm/webapp.py
- [[_latency_error()]] - code - src/merged_agentic_swarm/webapp.py
- [[_run_latency_test()]] - code - src/merged_agentic_swarm/webapp.py
- [[okfalse payload — short error, never the key.]] - rationale - src/merged_agentic_swarm/webapp.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/_run_latency_test
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_webapp.py]]

## Top bridge nodes
- [[_run_latency_test()]] - degree 5, connects to 1 community
- [[_fetch_litellm_aliases()]] - degree 4, connects to 1 community
- [[_latency_error()]] - degree 4, connects to 1 community
- [[AsyncClient_1]] - degree 3, connects to 1 community