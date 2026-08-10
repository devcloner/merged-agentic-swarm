---
type: community
cohesion: 0.25
members: 8
---

# orchestrator

**Cohesion:** 0.25 - loosely connected
**Members:** 8 nodes

## Members
- [[control_plane]] - code - opencode-swarm.json
- [[heartbeat_interval_ms]] - code - opencode-swarm.json
- [[max_concurrency]] - code - opencode-swarm.json
- [[orchestrator]] - code - opencode-swarm.json
- [[proxy_endpoint]] - code - opencode-swarm.json
- [[ramp_sequence]] - code - opencode-swarm.json
- [[runner]] - code - opencode-swarm.json
- [[telemetry_enabled]] - code - opencode-swarm.json

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/orchestrator
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_opencode-swarm.json]]
- 1 edge to [[_COMMUNITY_phase_gates]]
- 1 edge to [[_COMMUNITY_retry_policy]]

## Top bridge nodes
- [[orchestrator]] - degree 10, connects to 3 communities