# SubTask

> 48 nodes · cohesion 0.08

## Key Concepts

- **OpenCodeSwarmManager** (32 connections) — `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- **TestOpenCodeSwarmManager** (24 connections) — `tests/test_opencode_swarm_service.py`
- **TestExecuteSubtaskDecisionLogic** (18 connections) — `tests/test_opencode_swarm_service.py`
- **make_subtask()** (17 connections) — `tests/conftest.py`
- **_router()** (13 connections) — `tests/test_opencode_swarm_service.py`
- **test_opencode_swarm_service.py** (11 connections) — `tests/test_opencode_swarm_service.py`
- **._manager()** (11 connections) — `tests/test_opencode_swarm_service.py`
- **.get_available_worker()** (6 connections) — `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- **._get_available_worker_unlocked()** (5 connections) — `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- **.test_execute_subtask_resolves_per_role_alias_when_none()** (5 connections) — `tests/test_opencode_swarm_service.py`
- **.test_execute_subtask_uses_explicit_model_alias()** (5 connections) — `tests/test_opencode_swarm_service.py`
- **.test_batch_parallel_custom_ramp_clamped_and_bounded()** (5 connections) — `tests/test_opencode_swarm_service.py`
- **.test_loop_exception_fails_subtask()** (4 connections) — `tests/test_opencode_swarm_service.py`
- **.test_no_worker_returns_error()** (4 connections) — `tests/test_opencode_swarm_service.py`
- **.test_opencode_mode_routes_to_opencode_worker()** (4 connections) — `tests/test_opencode_swarm_service.py`
- **.test_routed_to_durable_agent()** (4 connections) — `tests/test_opencode_swarm_service.py`
- **.test_simulation_worker_fails()** (4 connections) — `tests/test_opencode_swarm_service.py`
- **.test_batch_parallel_omits_alias_when_none()** (4 connections) — `tests/test_opencode_swarm_service.py`
- **.test_batch_parallel_threads_explicit_model_alias()** (4 connections) — `tests/test_opencode_swarm_service.py`
- **.test_batch_parallel_uses_custom_ramp()** (4 connections) — `tests/test_opencode_swarm_service.py`
- **.test_batch_parallel_uses_ramp_concurrency()** (4 connections) — `tests/test_opencode_swarm_service.py`
- **.test_execute_subtask_with_worker_fabric()** (4 connections) — `tests/test_opencode_swarm_service.py`
- **.test_get_available_worker_fallback_to_core_engineer()** (4 connections) — `tests/test_opencode_swarm_service.py`
- **.test_execute_subtask_batch_parallel()** (3 connections) — `tests/test_opencode_swarm_service.py`
- **live** (2 connections)
- *... and 23 more nodes in this community*

## Relationships

- [CodebaseMapService](CodebaseMapService.md) (12 shared connections)
- [AgentSpec](AgentSpec.md) (9 shared connections)
- [ChainRegistry](ChainRegistry.md) (7 shared connections)
- [WorkerPoolConfig](WorkerPoolConfig.md) (6 shared connections)
- [WorkerRole](WorkerRole.md) (4 shared connections)
- [conftest.py](conftest.py.md) (4 shared connections)
- [OpenCodeSwarmManager](OpenCodeSwarmManager.md) (3 shared connections)
- [test_streaming_proxy.py](test_streaming_proxy.py.md) (3 shared connections)
- [promotion_policy](promotion_policy.md) (3 shared connections)
- [PassthroughStreamingProxy](PassthroughStreamingProxy.md) (2 shared connections)

## Source Files

- `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- `tests/conftest.py`
- `tests/test_opencode_swarm_service.py`

## Audit Trail

- EXTRACTED: 172 (76%)
- INFERRED: 55 (24%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*