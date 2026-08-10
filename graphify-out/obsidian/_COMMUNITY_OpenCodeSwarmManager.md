---
type: community
cohesion: 0.08
members: 45
---

# OpenCodeSwarmManager

**Cohesion:** 0.08 - loosely connected
**Members:** 45 nodes

## Members
- [[dot-_manager()]] - code - tests/test_opencode_swarm_service.py
- [[dot-setup_method()_17]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_batch_parallel_custom_ramp_clamped_and_bounded()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_batch_parallel_omits_alias_when_none()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_batch_parallel_threads_explicit_model_alias()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_batch_parallel_uses_custom_ramp()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_batch_parallel_uses_ramp_concurrency()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_execute_subtask_batch_parallel()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_execute_subtask_resolves_per_role_alias_when_none()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_execute_subtask_uses_explicit_model_alias()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_execute_subtask_with_worker_fabric()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_get_available_worker_fallback_to_core_engineer()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_get_available_worker_returns_correct_role()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_get_available_worker_round_robin()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_get_available_worker_tester_round_robin()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_get_pool_id_fallback()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_get_pool_id_mapped()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_initializes_40_workers()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_loop_exception_fails_subtask()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_no_worker_returns_error()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_opencode_mode_routes_to_opencode_worker()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_routed_to_durable_agent()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_run_opencode_worker_completed()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_run_opencode_worker_failed()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_simulation_worker_fails()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_workers_by_role()]] - code - tests/test_opencode_swarm_service.py
- [[A custom ramp past the configured cap is clamped to max_total_workers; levels…]] - rationale - tests/test_opencode_swarm_service.py
- [[A provided ramp_sequence overrides the default wave_gate_level mapping.]] - rationale - tests/test_opencode_swarm_service.py
- [[A worker subtask goes through the agentic tool loop and reports honestly. A…]] - rationale - tests/test_opencode_swarm_service.py
- [[An explicit model_alias is passed through untouched (no re-resolution).]] - rationale - tests/test_opencode_swarm_service.py
- [[An explicit model_alias on the batch is threaded into every worker.]] - rationale - tests/test_opencode_swarm_service.py
- [[Build a real DurableAgentRouter over tmp JSONL + agent dir.]] - rationale - tests/test_opencode_swarm_service.py
- [[Factory fixture that returns a function to create SubTask instances.]] - rationale - tests/conftest.py
- [[Getting a role with zero allocation should fall back to core engineer.]] - rationale - tests/test_opencode_swarm_service.py
- [[OpenCodeSwarmManager]] - code - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[TestExecuteSubtaskDecisionLogic]] - code - tests/test_opencode_swarm_service.py
- [[TestOpenCodeSwarmManager]] - code - tests/test_opencode_swarm_service.py
- [[Tests for servicesopencode_swarm_service.py Coverage…]] - rationale - tests/test_opencode_swarm_service.py
- [[Wave N batch executes at rampN concurrency, not the 4-worker default.]] - rationale - tests/test_opencode_swarm_service.py
- [[With model_alias=None the worker receives no alias kwarg — each worker resolves…]] - rationale - tests/test_opencode_swarm_service.py
- [[_router()]] - code - tests/test_opencode_swarm_service.py
- [[live]] - code
- [[make_subtask()]] - code - tests/conftest.py
- [[model_alias=None resolves the role's litellm alias and feeds it to the worker…]] - rationale - tests/test_opencode_swarm_service.py
- [[test_opencode_swarm_service.py]] - code - tests/test_opencode_swarm_service.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/OpenCodeSwarmManager
SORT file.name ASC
```

## Connections to other communities
- 11 edges to [[_COMMUNITY_DurableAgentRouter]]
- 8 edges to [[_COMMUNITY_WorkerPoolConfig]]
- 7 edges to [[_COMMUNITY_WorkerRole]]
- 7 edges to [[_COMMUNITY_SubTask]]
- 5 edges to [[_COMMUNITY_ConcurrencyRampController]]
- 3 edges to [[_COMMUNITY_TestTargetRepoRoot]]
- 3 edges to [[_COMMUNITY_conftest.py]]
- 2 edges to [[_COMMUNITY_services__init__.py]]
- 2 edges to [[_COMMUNITY_dot-get_available_worker]]
- 1 edge to [[_COMMUNITY_AgentSpec]]

## Top bridge nodes
- [[OpenCodeSwarmManager]] - degree 32, connects to 10 communities
- [[test_opencode_swarm_service.py]] - degree 11, connects to 6 communities
- [[TestOpenCodeSwarmManager]] - degree 24, connects to 5 communities
- [[TestExecuteSubtaskDecisionLogic]] - degree 18, connects to 5 communities
- [[make_subtask()]] - degree 17, connects to 1 community