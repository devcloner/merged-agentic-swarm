---
type: community
cohesion: 0.10
members: 35
---

# WorkerPoolConfig

**Cohesion:** 0.10 - loosely connected
**Members:** 35 nodes

## Members
- [[dot-__init__()_14]] - code - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[dot-_initialize_worker_pool()]] - code - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[dot-get_pool_summary()]] - code - src/merged_agentic_swarm/models/agent_models.py
- [[dot-record_pool_failure()]] - code - src/merged_agentic_swarm/models/agent_models.py
- [[dot-record_pool_success()]] - code - src/merged_agentic_swarm/models/agent_models.py
- [[dot-test_custom_config()]] - code - tests/test_agent_models.py
- [[dot-test_default_allocations()]] - code - tests/test_agent_models.py
- [[dot-test_default_creation()_1]] - code - tests/test_agent_models.py
- [[dot-test_default_state()]] - code - tests/test_agent_models.py
- [[dot-test_get_pool_summary_returns_copy()]] - code - tests/test_agent_models.py
- [[dot-test_record_pool_failure()]] - code - tests/test_agent_models.py
- [[dot-test_record_pool_success()]] - code - tests/test_agent_models.py
- [[dot-test_record_rate_limit()]] - code - tests/test_agent_models.py
- [[dot-test_to_dict()]] - code - tests/test_agent_models.py
- [[dot-test_to_dict()_1]] - code - tests/test_agent_models.py
- [[dot-test_values()_1]] - code - tests/test_agent_models.py
- [[dot-test_values()]] - code - tests/test_agent_models.py
- [[dot-to_dict()]] - code - src/merged_agentic_swarm/models/agent_models.py
- [[dot-to_dict()_1]] - code - src/merged_agentic_swarm/models/agent_models.py
- [[dot-to_dict()_2]] - code - src/merged_agentic_swarm/models/agent_models.py
- [[Any_4]] - code
- [[Increment the completed counter for the given pool.]] - rationale - src/merged_agentic_swarm/models/agent_models.py
- [[Increment the failed or rate_limited counter for the given pool.]] - rationale - src/merged_agentic_swarm/models/agent_models.py
- [[Initializes the 40 worker specs across role allocations.]] - rationale - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[Return a copy of the pool_health dict.]] - rationale - src/merged_agentic_swarm/models/agent_models.py
- [[SpawnChainEntry]] - code - src/merged_agentic_swarm/models/agent_models.py
- [[TestAgentType]] - code - tests/test_agent_models.py
- [[TestSpawnChainEntry]] - code - tests/test_agent_models.py
- [[TestWorkerPoolConfig]] - code - tests/test_agent_models.py
- [[TestWorkerPoolState]] - code - tests/test_agent_models.py
- [[TestWorkerRole]] - code - tests/test_agent_models.py
- [[Tests for modelsagent_models.py Coverage AgentSpec, WorkerPoolConfig,…]] - rationale - tests/test_agent_models.py
- [[WorkerPoolConfig]] - code - src/merged_agentic_swarm/models/agent_models.py
- [[WorkerPoolState]] - code - src/merged_agentic_swarm/models/agent_models.py
- [[test_agent_models.py]] - code - tests/test_agent_models.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/WorkerPoolConfig
SORT file.name ASC
```

## Connections to other communities
- 18 edges to [[_COMMUNITY_WorkerRole]]
- 11 edges to [[_COMMUNITY_AgentSpec]]
- 8 edges to [[_COMMUNITY_OpenCodeSwarmManager]]
- 4 edges to [[_COMMUNITY_ConcurrencyRampController]]
- 3 edges to [[_COMMUNITY_SubTask]]
- 3 edges to [[_COMMUNITY_DurableAgentRouter]]
- 3 edges to [[_COMMUNITY_ChainRegistry]]
- 1 edge to [[_COMMUNITY_services__init__.py]]
- 1 edge to [[_COMMUNITY_cmd_config]]
- 1 edge to [[_COMMUNITY_TestTargetRepoRoot]]
- 1 edge to [[_COMMUNITY_DurableAgentFactory]]

## Top bridge nodes
- [[WorkerPoolConfig]] - degree 24, connects to 9 communities
- [[WorkerPoolState]] - degree 23, connects to 6 communities
- [[SpawnChainEntry]] - degree 16, connects to 5 communities
- [[dot-_initialize_worker_pool()]] - degree 5, connects to 3 communities
- [[TestWorkerPoolState]] - degree 13, connects to 2 communities