---
type: community
cohesion: 0.09
members: 44
---

# WorkerRole

**Cohesion:** 0.09 - loosely connected
**Members:** 44 nodes

## Members
- [[dot-__init__()_21]] - code - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[dot-_get_opencode_bin()]] - code - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[dot-test_custom_config()]] - code - tests/test_agent_models.py
- [[dot-test_default_allocations()]] - code - tests/test_agent_models.py
- [[dot-test_default_creation()_1]] - code - tests/test_agent_models.py
- [[dot-test_detect_mode_returns_valid()]] - code - tests/test_worker_runtime_adapter.py
- [[dot-test_opencode_available_is_bool()]] - code - tests/test_worker_runtime_adapter.py
- [[dot-test_resolve_opencode_bin_is_str_or_none()]] - code - tests/test_worker_runtime_adapter.py
- [[dot-test_to_dict()]] - code - tests/test_agent_models.py
- [[dot-test_values()_1]] - code - tests/test_agent_models.py
- [[dot-test_values()]] - code - tests/test_agent_models.py
- [[Agent, Worker Pool, and Spawn Chain Data Models]] - rationale - src/merged_agentic_swarm/models/agent_models.py
- [[AgentType]] - code - src/merged_agentic_swarm/models/agent_models.py
- [[Auto-detect the best available runtime mode. Priority opencode …]] - rationale - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[Durable Agent Factory & Knowledge-Box - Spawn Chain Registry Turns validated…]] - rationale - src/merged_agentic_swarm/services/agent_factory_service.py
- [[Enum]] - code
- [[OpenCode Swarm Pack Coordinator (40-Worker Pool Manager) Allocates worker pools…]] - rationale - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[Resolve the opencode binary from PATH or known locations.]] - rationale - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[Return True if the OpenCode binary exists and responds to --help.]] - rationale - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[Return the resolved opencode binary, or None if unavailable.]] - rationale - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[SpawnChainEntry]] - code - src/merged_agentic_swarm/models/agent_models.py
- [[TestAgentType]] - code - tests/test_agent_models.py
- [[TestModeDetection]] - code - tests/test_worker_runtime_adapter.py
- [[TestShutdown]] - code - tests/test_worker_runtime_adapter.py
- [[TestSpawnChainEntry]] - code - tests/test_agent_models.py
- [[TestWorkerPoolConfig]] - code - tests/test_agent_models.py
- [[TestWorkerRole]] - code - tests/test_agent_models.py
- [[Tests for modelsagent_models.py Coverage AgentSpec, WorkerPoolConfig,…]] - rationale - tests/test_agent_models.py
- [[Tests for servicesopencode_swarm_service.py Coverage…]] - rationale - tests/test_opencode_swarm_service.py
- [[Tests for servicesworker_runtime_adapter.py Real-behavior coverage of the…]] - rationale - tests/test_worker_runtime_adapter.py
- [[Worker Runtime Adapter — Unified launcher for OpenCode swarm workers. Supports…]] - rationale - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[WorkerPoolConfig]] - code - src/merged_agentic_swarm/models/agent_models.py
- [[WorkerRole]] - code - src/merged_agentic_swarm/models/agent_models.py
- [[_opencode_available()]] - code - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[_resolve_opencode_bin()]] - code - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[agent_factory_service.py]] - code - src/merged_agentic_swarm/services/agent_factory_service.py
- [[agent_models.py]] - code - src/merged_agentic_swarm/models/agent_models.py
- [[detect_mode()]] - code - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[opencode_swarm_service.py]] - code - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[str]] - code
- [[test_agent_models.py]] - code - tests/test_agent_models.py
- [[test_opencode_swarm_service.py]] - code - tests/test_opencode_swarm_service.py
- [[test_worker_runtime_adapter.py]] - code - tests/test_worker_runtime_adapter.py
- [[worker_runtime_adapter.py]] - code - src/merged_agentic_swarm/services/worker_runtime_adapter.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/WorkerRole
SORT file.name ASC
```

## Connections to other communities
- 37 edges to [[_COMMUNITY_AgentSpec]]
- 14 edges to [[_COMMUNITY_OpenCodeSwarmManager]]
- 13 edges to [[_COMMUNITY_PRDAnalysisResult]]
- 12 edges to [[_COMMUNITY_WorkerPoolState]]
- 11 edges to [[_COMMUNITY_ChainRegistry]]
- 10 edges to [[_COMMUNITY_DurableAgentFactory]]
- 10 edges to [[_COMMUNITY_DurableAgentRouter]]
- 8 edges to [[_COMMUNITY_ConcurrencyRampController]]
- 6 edges to [[_COMMUNITY_services__init__.py]]
- 4 edges to [[_COMMUNITY_TestExecuteSubtaskDecisionLogic]]
- 3 edges to [[_COMMUNITY_knowledge_cache.py]]
- 3 edges to [[_COMMUNITY_TestTargetRepoRoot]]
- 2 edges to [[_COMMUNITY_MultiLayeredAgenticOrchestrator]]
- 1 edge to [[_COMMUNITY_cmd_config]]
- 1 edge to [[_COMMUNITY_SubTask]]
- 1 edge to [[_COMMUNITY_multi_provider_fabric.py]]
- 1 edge to [[_COMMUNITY_AgenticWorkerLoop]]

## Top bridge nodes
- [[WorkerRole]] - degree 42, connects to 11 communities
- [[WorkerPoolConfig]] - degree 24, connects to 10 communities
- [[opencode_swarm_service.py]] - degree 23, connects to 10 communities
- [[AgentType]] - degree 31, connects to 9 communities
- [[test_opencode_swarm_service.py]] - degree 11, connects to 7 communities