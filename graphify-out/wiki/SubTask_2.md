# SubTask

> God node · 55 connections · `src/merged_agentic_swarm/models/prd_models.py`

**Community:** [test_streaming_proxy.py](test_streaming_proxy.py.md)

## Connections by Relation

### calls
- ._with_epics() `EXTRACTED`
- .load_state() `EXTRACTED`
- ._with_wave3_epics() `EXTRACTED`
- .optimize_and_parse_prd() `EXTRACTED`
- _epic() `INFERRED`
- .test_find_matching_agent_by_category_and_keywords() `EXTRACTED`
- .test_find_matching_agent_no_match_returns_none() `EXTRACTED`
- .test_default_creation() `EXTRACTED`
- .test_to_dict_serializes_nested() `EXTRACTED`
- .test_with_subtasks() `EXTRACTED`
- .test_check_ownership_map_absent_passes() `EXTRACTED`
- .test_check_ownership_pool_missing_hard_fails() `EXTRACTED`
- .test_check_ownership_valid() `EXTRACTED`
- .test_default_creation() `EXTRACTED`
- .test_marked_completed_sets_timestamp() `EXTRACTED`
- .test_to_dict_serializes_enum() `EXTRACTED`
- .test_with_error() `EXTRACTED`

### contains
- prd_models.py `EXTRACTED`

### imports
- [models/__init__.py](models-__init__.py.md) `EXTRACTED`
- opencode_swarm_service.py `EXTRACTED`
- task_master_service.py `EXTRACTED`
- wave_gate_service.py `EXTRACTED`

### method
- .to_dict() `EXTRACTED`

### references
- .execute_subtask_with_worker() `EXTRACTED`
- .find_matching_agent() `EXTRACTED`
- .execute_subtask_batch_parallel() `EXTRACTED`
- ._check_ownership() `EXTRACTED`

### uses
- [TaskMasterService](TaskMasterService.md) `INFERRED`
- [OpenCodeSwarmManager](OpenCodeSwarmManager.md) `INFERRED`
- [DurableAgentRouter](DurableAgentRouter.md) `INFERRED`
- [TestWaveGatesWithRealState](TestWaveGatesWithRealState.md) `INFERRED`
- TestOpenCodeSwarmManager `INFERRED`
- [TestWaveGateController](TestWaveGateController.md) `INFERRED`
- TestDurableAgentRouter `INFERRED`
- [ConcurrencyRampController](ConcurrencyRampController.md) `INFERRED`
- WaveGateController `INFERRED`
- TestExecuteSubtaskDecisionLogic `INFERRED`
- [TestRunFullAgenticWorkflow](TestRunFullAgenticWorkflow.md) `INFERRED`
- TestConcurrencyRampController `INFERRED`
- TestSubTask `INFERRED`
- [TestTargetRepoRoot](TestTargetRepoRoot.md) `INFERRED`
- TestEpicTask `INFERRED`
- TestPRDAnalysisResult `INFERRED`
- TestSpecGap `INFERRED`
- TestRunSyntaxVerificationPaths `INFERRED`
- TestPRDDocument `INFERRED`
- TestApplyWorkerOutputsPaths `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*