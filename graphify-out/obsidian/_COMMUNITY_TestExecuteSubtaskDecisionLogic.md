---
type: community
cohesion: 0.22
members: 20
---

# TestExecuteSubtaskDecisionLogic

**Cohesion:** 0.22 - loosely connected
**Members:** 20 nodes

## Members
- [[dot-_manager()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_execute_subtask_batch_parallel()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_execute_subtask_resolves_per_role_alias_when_none()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_execute_subtask_uses_explicit_model_alias()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_execute_subtask_with_worker_fabric()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_loop_exception_fails_subtask()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_no_worker_returns_error()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_opencode_mode_routes_to_opencode_worker()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_routed_to_durable_agent()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_run_opencode_worker_completed()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_run_opencode_worker_failed()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_simulation_worker_fails()]] - code - tests/test_opencode_swarm_service.py
- [[A worker subtask goes through the agentic tool loop and reports honestly. A…]] - rationale - tests/test_opencode_swarm_service.py
- [[An explicit model_alias is passed through untouched (no re-resolution).]] - rationale - tests/test_opencode_swarm_service.py
- [[Build a real DurableAgentRouter over tmp JSONL + agent dir.]] - rationale - tests/test_opencode_swarm_service.py
- [[TestExecuteSubtaskDecisionLogic]] - code - tests/test_opencode_swarm_service.py
- [[_router()]] - code - tests/test_opencode_swarm_service.py
- [[live]] - code
- [[make_subtask()]] - code - tests/conftest.py
- [[model_alias=None resolves the role's litellm alias and feeds it to the worker…]] - rationale - tests/test_opencode_swarm_service.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/TestExecuteSubtaskDecisionLogic
SORT file.name ASC
```

## Connections to other communities
- 9 edges to [[_COMMUNITY_OpenCodeSwarmManager]]
- 5 edges to [[_COMMUNITY_DurableAgentRouter]]
- 4 edges to [[_COMMUNITY_WorkerRole]]
- 3 edges to [[_COMMUNITY_conftest.py]]
- 1 edge to [[_COMMUNITY_PRDAnalysisResult]]
- 1 edge to [[_COMMUNITY_SubTask]]
- 1 edge to [[_COMMUNITY_ConcurrencyRampController]]

## Top bridge nodes
- [[TestExecuteSubtaskDecisionLogic]] - degree 18, connects to 6 communities
- [[make_subtask()]] - degree 17, connects to 2 communities
- [[_router()]] - degree 13, connects to 2 communities
- [[dot-_manager()]] - degree 11, connects to 1 community
- [[dot-test_execute_subtask_with_worker_fabric()]] - degree 4, connects to 1 community