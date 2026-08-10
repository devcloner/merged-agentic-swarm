---
type: community
cohesion: 0.11
members: 53
---

# SubTask

**Cohesion:** 0.11 - loosely connected
**Members:** 53 nodes

## Members
- [[dot-__init__()_17]] - code - src/merged_agentic_swarm/services/task_master_service.py
- [[dot-get_tasks_for_wave()]] - code - src/merged_agentic_swarm/services/task_master_service.py
- [[dot-load_state()]] - code - src/merged_agentic_swarm/services/task_master_service.py
- [[dot-setup_method()_2]] - code - tests/test_agentic_orchestrator.py
- [[dot-test_custom_title()]] - code - tests/test_prd_models.py
- [[dot-test_default_creation()_8]] - code - tests/test_prd_models.py
- [[dot-test_default_creation()_11]] - code - tests/test_prd_models.py
- [[dot-test_default_creation()_10]] - code - tests/test_prd_models.py
- [[dot-test_default_creation()_9]] - code - tests/test_prd_models.py
- [[dot-test_default_creation()_7]] - code - tests/test_prd_models.py
- [[dot-test_marked_completed_sets_timestamp()]] - code - tests/test_prd_models.py
- [[dot-test_proxy_start_failure_is_nonfatal()]] - code - tests/test_agentic_orchestrator.py
- [[dot-test_resolve()]] - code - tests/test_prd_models.py
- [[dot-test_to_dict()_6]] - code - tests/test_prd_models.py
- [[dot-test_to_dict_serializes_enum()]] - code - tests/test_prd_models.py
- [[dot-test_to_dict_serializes_nested()]] - code - tests/test_prd_models.py
- [[dot-test_to_dict_with_preview()]] - code - tests/test_prd_models.py
- [[dot-test_to_dict_without_preview()]] - code - tests/test_prd_models.py
- [[dot-test_values()_3]] - code - tests/test_prd_models.py
- [[dot-test_values()_2]] - code - tests/test_prd_models.py
- [[dot-test_with_error()]] - code - tests/test_prd_models.py
- [[dot-test_with_subtasks()]] - code - tests/test_prd_models.py
- [[Codebase Mapper & Spec Gap Closer Service Maps repository structure, AST…]] - rationale - src/merged_agentic_swarm/services/codebase_map_service.py
- [[Enum_1]] - code
- [[EpicTask]] - code - src/merged_agentic_swarm/models/prd_models.py
- [[Loads persistent Task Master state from JSON file if present.]] - rationale - src/merged_agentic_swarm/services/task_master_service.py
- [[Models Package Initialization]] - rationale - src/merged_agentic_swarm/models/__init__.py
- [[PRD and Task Master Data Models]] - rationale - src/merged_agentic_swarm/models/prd_models.py
- [[PRDAnalysisResult]] - code - src/merged_agentic_swarm/models/prd_models.py
- [[PRDDocument]] - code - src/merged_agentic_swarm/models/prd_models.py
- [[SpecGap]] - code - src/merged_agentic_swarm/models/prd_models.py
- [[SubTask]] - code - src/merged_agentic_swarm/models/prd_models.py
- [[Task Master AI Spine Service PRD optimization, task parsing, dependency…]] - rationale - src/merged_agentic_swarm/services/task_master_service.py
- [[TaskPriority]] - code - src/merged_agentic_swarm/models/prd_models.py
- [[TaskStatus]] - code - src/merged_agentic_swarm/models/prd_models.py
- [[TestApplyWorkerOutputs]] - code - tests/test_agentic_orchestrator.py
- [[TestEpicTask]] - code - tests/test_prd_models.py
- [[TestInitializeSystemProxyFailure]] - code - tests/test_agentic_orchestrator.py
- [[TestPRDAnalysisResult]] - code - tests/test_prd_models.py
- [[TestPRDDocument]] - code - tests/test_prd_models.py
- [[TestSpecGap]] - code - tests/test_prd_models.py
- [[TestSubTask]] - code - tests/test_prd_models.py
- [[TestTaskPriority]] - code - tests/test_prd_models.py
- [[TestTaskStatus]] - code - tests/test_prd_models.py
- [[Tests for modelsprd_models.py Coverage TaskStatus, TaskPriority, SubTask,…]] - rationale - tests/test_prd_models.py
- [[Wave Gates Controller Service Enforces gated phase boundaries (Wave 0 to Wave…]] - rationale - src/merged_agentic_swarm/services/wave_gate_service.py
- [[codebase_map_service.py]] - code - src/merged_agentic_swarm/services/codebase_map_service.py
- [[models__init__.py]] - code - src/merged_agentic_swarm/models/__init__.py
- [[prd_models.py]] - code - src/merged_agentic_swarm/models/prd_models.py
- [[str_1]] - code
- [[task_master_service.py]] - code - src/merged_agentic_swarm/services/task_master_service.py
- [[test_prd_models.py]] - code - tests/test_prd_models.py
- [[wave_gate_service.py]] - code - src/merged_agentic_swarm/services/wave_gate_service.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/SubTask
SORT file.name ASC
```

## Connections to other communities
- 34 edges to [[_COMMUNITY_MultiLayeredAgenticOrchestrator]]
- 20 edges to [[_COMMUNITY_TaskMasterService]]
- 12 edges to [[_COMMUNITY_WaveGateController]]
- 12 edges to [[_COMMUNITY_TestWaveGatesWithRealState]]
- 11 edges to [[_COMMUNITY_WorkerRole]]
- 8 edges to [[_COMMUNITY_DurableAgentRouter]]
- 8 edges to [[_COMMUNITY_TestWaveGateController]]
- 7 edges to [[_COMMUNITY_OpenCodeSwarmManager]]
- 6 edges to [[_COMMUNITY_ProgressLogEntry]]
- 6 edges to [[_COMMUNITY_CodebaseMapService]]
- 5 edges to [[_COMMUNITY_ConcurrencyRampController]]
- 4 edges to [[_COMMUNITY_TestRunFullAgenticWorkflow]]
- 4 edges to [[_COMMUNITY_Any]]
- 3 edges to [[_COMMUNITY_WorkerPoolConfig]]
- 3 edges to [[_COMMUNITY_services__init__.py]]
- 2 edges to [[_COMMUNITY_TestTargetRepoRoot]]
- 1 edge to [[_COMMUNITY_AgentSpec]]
- 1 edge to [[_COMMUNITY_multi_provider_fabric.py]]

## Top bridge nodes
- [[SubTask]] - degree 55, connects to 12 communities
- [[TaskStatus]] - degree 29, connects to 9 communities
- [[PRDAnalysisResult]] - degree 34, connects to 6 communities
- [[EpicTask]] - degree 32, connects to 6 communities
- [[models__init__.py]] - degree 26, connects to 5 communities