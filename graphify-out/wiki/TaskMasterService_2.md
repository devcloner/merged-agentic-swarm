# TaskMasterService

> God node · 38 connections · `src/merged_agentic_swarm/services/task_master_service.py`

**Community:** [TaskMasterService](TaskMasterService.md)

## Connections by Relation

### calls
- ._controller() `INFERRED`
- isolated_task_master() `INFERRED`
- .test_concurrent_saves_produce_complete_json() `INFERRED`
- .test_save_state_uses_unique_temp_name() `INFERRED`
- .test_optimize_and_parse_prd() `INFERRED`
- .test_empty_state() `INFERRED`
- .test_estimate_turns_capped() `INFERRED`
- .test_estimate_turns_complex() `INFERRED`
- .test_estimate_turns_simple() `INFERRED`
- .test_get_tasks_for_wave() `INFERRED`
- .test_get_tasks_for_wave_no_analysis() `INFERRED`
- .test_load_corrupted_state() `INFERRED`
- .test_load_existing_state() `INFERRED`
- .test_optimize_and_parse_prd_persists() `INFERRED`
- .test_prd_analysis_includes_fabric_preview() `INFERRED`
- .test_update_task_status_epic() `INFERRED`
- .test_update_task_status_no_analysis() `INFERRED`
- .test_update_task_status_subtask() `INFERRED`
- .test_update_task_status_with_error() `INFERRED`

### contains
- task_master_service.py `EXTRACTED`

### imports
- [services/__init__.py](services-__init__.py.md) `EXTRACTED`

### method
- .load_state() `EXTRACTED`
- .optimize_and_parse_prd() `EXTRACTED`
- .save_state() `EXTRACTED`
- .update_task_status() `EXTRACTED`
- ._estimate_turns() `EXTRACTED`
- .get_tasks_for_wave() `EXTRACTED`
- .__init__() `EXTRACTED`

### rationale_for
- Orchestrator wrapping the real Task Master AI spine. NOTE on state paths: -… `EXTRACTED`

### uses
- [SubTask](SubTask.md) `INFERRED`
- [PRDAnalysisResult](PRDAnalysisResult.md) `INFERRED`
- EpicTask `INFERRED`
- [TaskStatus](TaskStatus.md) `INFERRED`
- TaskPriority `INFERRED`
- [TestWaveGatesWithRealState](TestWaveGatesWithRealState.md) `INFERRED`
- [TestWaveGateController](TestWaveGateController.md) `INFERRED`
- SpecGap `INFERRED`
- TestTaskMasterService `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*