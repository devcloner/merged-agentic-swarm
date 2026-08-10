# OpenCodeSwarmManager

> 48 nodes · cohesion 0.08

## Key Concepts

- **AgentSpec** (46 connections) — `src/merged_agentic_swarm/models/agent_models.py`
- **WorkerRuntimeAdapter** (32 connections) — `src/merged_agentic_swarm/services/worker_runtime_adapter.py`
- **TestAgentSpec** (13 connections) — `tests/test_agent_models.py`
- **TestAdapterConstruction** (10 connections) — `tests/test_worker_runtime_adapter.py`
- **TestLaunchWorker** (10 connections) — `tests/test_worker_runtime_adapter.py`
- **._launch_via_opencode()** (7 connections) — `src/merged_agentic_swarm/services/worker_runtime_adapter.py`
- **.launch_worker()** (7 connections) — `src/merged_agentic_swarm/services/worker_runtime_adapter.py`
- **_spec()** (7 connections) — `tests/test_worker_runtime_adapter.py`
- **TestLaunchBatch** (7 connections) — `tests/test_worker_runtime_adapter.py`
- **get_runtime_adapter()** (6 connections) — `src/merged_agentic_swarm/services/worker_runtime_adapter.py`
- **._launch_via_native()** (6 connections) — `src/merged_agentic_swarm/services/worker_runtime_adapter.py`
- **.launch_batch()** (5 connections) — `src/merged_agentic_swarm/services/worker_runtime_adapter.py`
- **._launch_via_fabric()** (5 connections) — `src/merged_agentic_swarm/services/worker_runtime_adapter.py`
- **._get_opencode_bin()** (4 connections) — `src/merged_agentic_swarm/services/worker_runtime_adapter.py`
- **.test_native_launch_simulated_is_hard_failure()** (4 connections) — `tests/test_worker_runtime_adapter.py`
- **.test_direct_fabric_launch_delegates()** (3 connections) — `tests/test_worker_runtime_adapter.py`
- **.test_native_launch_completed()** (3 connections) — `tests/test_worker_runtime_adapter.py`
- **.test_native_launch_failed_on_exception()** (3 connections) — `tests/test_worker_runtime_adapter.py`
- **.test_opencode_falls_back_to_native_when_no_bin()** (3 connections) — `tests/test_worker_runtime_adapter.py`
- **.is_expired()** (2 connections) — `src/merged_agentic_swarm/models/agent_models.py`
- **Any** (2 connections)
- **._next_port()** (2 connections) — `src/merged_agentic_swarm/services/worker_runtime_adapter.py`
- **.shutdown()** (2 connections) — `src/merged_agentic_swarm/services/worker_runtime_adapter.py`
- **.test_custom_fields()** (2 connections) — `tests/test_agent_models.py`
- **.test_default_creation()** (2 connections) — `tests/test_agent_models.py`
- *... and 23 more nodes in this community*

## Relationships

- [AgentSpec](AgentSpec.md) (29 shared connections)
- [WorkerPoolConfig](WorkerPoolConfig.md) (10 shared connections)
- [DurableAgentRouter](DurableAgentRouter.md) (6 shared connections)
- [CodebaseMapService](CodebaseMapService.md) (3 shared connections)
- [SubTask](SubTask.md) (3 shared connections)
- [swarm_run.py](swarm_run.py.md) (2 shared connections)
- [ChainRegistry](ChainRegistry.md) (2 shared connections)
- [WorkerRole](WorkerRole.md) (1 shared connections)

## Source Files

- `src/merged_agentic_swarm/models/agent_models.py`
- `src/merged_agentic_swarm/services/worker_runtime_adapter.py`
- `tests/test_agent_models.py`
- `tests/test_worker_runtime_adapter.py`

## Audit Trail

- EXTRACTED: 183 (80%)
- INFERRED: 45 (20%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*