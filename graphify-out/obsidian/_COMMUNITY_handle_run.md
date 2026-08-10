---
type: community
cohesion: 0.33
members: 6
---

# handle_run

**Cohesion:** 0.33 - loosely connected
**Members:** 6 nodes

## Members
- [[Registry entry for a background workflow run.]] - rationale - src/merged_agentic_swarm/webapp.py
- [[RunHandle]] - code - src/merged_agentic_swarm/webapp.py
- [[Start a real agentic workflow in a background daemon thread; return now.]] - rationale - src/merged_agentic_swarm/webapp.py
- [[Start a real agentic workflow on a background daemon thread (returns now).…]] - rationale - src/merged_agentic_swarm/webapp.py
- [[_spawn_agentic_run()]] - code - src/merged_agentic_swarm/webapp.py
- [[handle_run()]] - code - src/merged_agentic_swarm/webapp.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/handle_run
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_webapp.py]]
- 2 edges to [[_COMMUNITY_services__init__.py]]
- 2 edges to [[_COMMUNITY_MultiLayeredAgenticOrchestrator]]
- 1 edge to [[_COMMUNITY_swarm_run.py]]

## Top bridge nodes
- [[_spawn_agentic_run()]] - degree 6, connects to 3 communities
- [[handle_run()]] - degree 8, connects to 2 communities
- [[RunHandle]] - degree 5, connects to 2 communities