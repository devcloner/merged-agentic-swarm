---
type: community
cohesion: 0.10
members: 33
---

# TaskMasterService

**Cohesion:** 0.10 - loosely connected
**Members:** 33 nodes

## Members
- [[dot-_estimate_turns()]] - code - src/merged_agentic_swarm/services/task_master_service.py
- [[dot-optimize_and_parse_prd()]] - code - src/merged_agentic_swarm/services/task_master_service.py
- [[dot-save_state()]] - code - src/merged_agentic_swarm/services/task_master_service.py
- [[dot-test_concurrent_saves_produce_complete_json()]] - code - tests/test_task_master_service.py
- [[dot-test_empty_state()]] - code - tests/test_task_master_service.py
- [[dot-test_estimate_turns_capped()]] - code - tests/test_task_master_service.py
- [[dot-test_estimate_turns_complex()]] - code - tests/test_task_master_service.py
- [[dot-test_estimate_turns_simple()]] - code - tests/test_task_master_service.py
- [[dot-test_get_tasks_for_wave()]] - code - tests/test_task_master_service.py
- [[dot-test_get_tasks_for_wave_no_analysis()]] - code - tests/test_task_master_service.py
- [[dot-test_load_corrupted_state()]] - code - tests/test_task_master_service.py
- [[dot-test_load_existing_state()]] - code - tests/test_task_master_service.py
- [[dot-test_optimize_and_parse_prd()]] - code - tests/test_task_master_service.py
- [[dot-test_optimize_and_parse_prd_persists()]] - code - tests/test_task_master_service.py
- [[dot-test_prd_analysis_includes_fabric_preview()]] - code - tests/test_task_master_service.py
- [[dot-test_save_state_uses_unique_temp_name()]] - code - tests/test_task_master_service.py
- [[dot-test_update_task_status_epic()]] - code - tests/test_task_master_service.py
- [[dot-test_update_task_status_no_analysis()]] - code - tests/test_task_master_service.py
- [[dot-test_update_task_status_subtask()]] - code - tests/test_task_master_service.py
- [[dot-test_update_task_status_with_error()]] - code - tests/test_task_master_service.py
- [[dot-update_task_status()]] - code - src/merged_agentic_swarm/services/task_master_service.py
- [[Concurrent save_state calls must never leave a torn JSON target.]] - rationale - tests/test_task_master_service.py
- [[Orchestrator wrapping the real Task Master AI spine. NOTE on state paths -…]] - rationale - src/merged_agentic_swarm/services/task_master_service.py
- [[Parses and optimizes PRD via Task Master AI model fabric routing. Calls the…]] - rationale - src/merged_agentic_swarm/services/task_master_service.py
- [[Regression for 41 temp file must not be the fixed target.tmp._1]] - rationale - tests/test_task_master_service.py
- [[Rough complexity analysis estimate turns based on task scope.]] - rationale - src/merged_agentic_swarm/services/task_master_service.py
- [[Saves Task Master state as the authoritative single source of truth.]] - rationale - src/merged_agentic_swarm/services/task_master_service.py
- [[TaskMasterService]] - code - src/merged_agentic_swarm/services/task_master_service.py
- [[TestTaskMasterService]] - code - tests/test_task_master_service.py
- [[Tests for servicestask_master_service.py Coverage TaskMasterService —…]] - rationale - tests/test_task_master_service.py
- [[Updates task status in state and syncs to file.]] - rationale - src/merged_agentic_swarm/services/task_master_service.py
- [[Verify PRD parsing creates expected epics and structure.]] - rationale - tests/test_task_master_service.py
- [[test_task_master_service.py]] - code - tests/test_task_master_service.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/TaskMasterService
SORT file.name ASC
```

## Connections to other communities
- 15 edges to [[_COMMUNITY_PRDAnalysisResult]]
- 5 edges to [[_COMMUNITY_SubTask]]
- 2 edges to [[_COMMUNITY_TestWaveGatesWithRealState]]
- 1 edge to [[_COMMUNITY_services__init__.py]]
- 1 edge to [[_COMMUNITY_conftest.py]]
- 1 edge to [[_COMMUNITY_TestWaveGateController]]

## Top bridge nodes
- [[TaskMasterService]] - degree 38, connects to 6 communities
- [[dot-optimize_and_parse_prd()]] - degree 8, connects to 2 communities
- [[TestTaskMasterService]] - degree 21, connects to 1 community
- [[dot-update_task_status()]] - degree 4, connects to 1 community
- [[dot-test_concurrent_saves_produce_complete_json()]] - degree 4, connects to 1 community