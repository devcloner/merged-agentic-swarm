---
type: community
cohesion: 0.15
members: 18
---

# WorkerPoolState

**Cohesion:** 0.15 - loosely connected
**Members:** 18 nodes

## Members
- [[dot-get_pool_summary()]] - code - src/merged_agentic_swarm/models/agent_models.py
- [[dot-record_pool_failure()]] - code - src/merged_agentic_swarm/models/agent_models.py
- [[dot-record_pool_success()]] - code - src/merged_agentic_swarm/models/agent_models.py
- [[dot-test_default_state()]] - code - tests/test_agent_models.py
- [[dot-test_get_pool_summary_returns_copy()]] - code - tests/test_agent_models.py
- [[dot-test_record_pool_failure()]] - code - tests/test_agent_models.py
- [[dot-test_record_pool_success()]] - code - tests/test_agent_models.py
- [[dot-test_record_rate_limit()]] - code - tests/test_agent_models.py
- [[dot-test_to_dict()_1]] - code - tests/test_agent_models.py
- [[dot-to_dict()]] - code - src/merged_agentic_swarm/models/agent_models.py
- [[dot-to_dict()_1]] - code - src/merged_agentic_swarm/models/agent_models.py
- [[dot-to_dict()_2]] - code - src/merged_agentic_swarm/models/agent_models.py
- [[Any_4]] - code
- [[Increment the completed counter for the given pool.]] - rationale - src/merged_agentic_swarm/models/agent_models.py
- [[Increment the failed or rate_limited counter for the given pool.]] - rationale - src/merged_agentic_swarm/models/agent_models.py
- [[Return a copy of the pool_health dict.]] - rationale - src/merged_agentic_swarm/models/agent_models.py
- [[TestWorkerPoolState]] - code - tests/test_agent_models.py
- [[WorkerPoolState]] - code - src/merged_agentic_swarm/models/agent_models.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/WorkerPoolState
SORT file.name ASC
```

## Connections to other communities
- 12 edges to [[_COMMUNITY_WorkerRole]]
- 3 edges to [[_COMMUNITY_AgentSpec]]
- 2 edges to [[_COMMUNITY_OpenCodeSwarmManager]]
- 1 edge to [[_COMMUNITY_PRDAnalysisResult]]
- 1 edge to [[_COMMUNITY_ConcurrencyRampController]]
- 1 edge to [[_COMMUNITY_DurableAgentRouter]]

## Top bridge nodes
- [[WorkerPoolState]] - degree 23, connects to 6 communities
- [[TestWorkerPoolState]] - degree 13, connects to 2 communities
- [[dot-to_dict()]] - degree 2, connects to 1 community
- [[dot-to_dict()_1]] - degree 2, connects to 1 community