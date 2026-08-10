---
type: community
cohesion: 0.50
members: 4
---

# .get_available_worker

**Cohesion:** 0.50 - moderately connected
**Members:** 4 nodes

## Members
- [[dot-_get_available_worker_unlocked()]] - code - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[dot-get_available_worker()]] - code - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[Gets an available worker matching the specified role using round-robin…]] - rationale - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[Internal must be called while holding self._worker_lock.]] - rationale - src/merged_agentic_swarm/services/opencode_swarm_service.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/get_available_worker
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_WorkerRole]]
- 2 edges to [[_COMMUNITY_AgentSpec]]
- 2 edges to [[_COMMUNITY_OpenCodeSwarmManager]]
- 1 edge to [[_COMMUNITY_DurableAgentRouter]]

## Top bridge nodes
- [[dot-get_available_worker()]] - degree 6, connects to 4 communities
- [[dot-_get_available_worker_unlocked()]] - degree 5, connects to 3 communities