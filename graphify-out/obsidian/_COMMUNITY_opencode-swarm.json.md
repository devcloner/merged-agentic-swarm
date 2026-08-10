---
type: community
cohesion: 0.33
members: 6
---

# opencode-swarm.json

**Cohesion:** 0.33 - loosely connected
**Members:** 6 nodes

## Members
- [[$schema]] - code - opencode-swarm.json
- [[agent_pools]] - code - opencode-swarm.json
- [[control_agents]] - code - opencode-swarm.json
- [[opencode-swarm.json]] - code - opencode-swarm.json
- [[phase_1_agents]] - code - opencode-swarm.json
- [[version]] - code - opencode-swarm.json

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/opencode-swarmjson
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_dynamic_learning_loop]]
- 1 edge to [[_COMMUNITY_orchestrator]]
- 1 edge to [[_COMMUNITY_project]]
- 1 edge to [[_COMMUNITY_role_allocations]]

## Top bridge nodes
- [[opencode-swarm.json]] - degree 9, connects to 4 communities