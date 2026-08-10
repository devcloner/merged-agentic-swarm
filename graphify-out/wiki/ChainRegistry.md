# ChainRegistry

> 21 nodes · cohesion 0.10

## Key Concepts

- **ConcurrencyRampController** (18 connections) — `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- **TestConcurrencyRampController** (17 connections) — `tests/test_opencode_swarm_service.py`
- **.execute_subtask_batch_parallel()** (6 connections) — `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- **.__init__()** (5 connections) — `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- **._initialize_worker_pool()** (5 connections) — `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- **.get_current_max_workers()** (3 connections) — `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- **.get_ramp_sequence()** (2 connections) — `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- **.setup_method()** (2 connections) — `tests/test_opencode_swarm_service.py`
- **Controls worker concurrency ramp-up across wave gates.** (1 connections) — `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- **Map wave gate level to max workers. Gate 0 -> 4, gate 1 -> 8, gate 2 -> 16,…** (1 connections) — `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- **Return the full ramp sequence.** (1 connections) — `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- **Initializes the 40 worker specs across role allocations.** (1 connections) — `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- **Executes a batch of subtasks in parallel using ThreadPoolExecutor up to max…** (1 connections) — `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- **.test_get_current_max_workers_beyond_gates()** (1 connections) — `tests/test_opencode_swarm_service.py`
- **.test_get_current_max_workers_gate_0()** (1 connections) — `tests/test_opencode_swarm_service.py`
- **.test_get_current_max_workers_gate_1()** (1 connections) — `tests/test_opencode_swarm_service.py`
- **.test_get_current_max_workers_gate_2()** (1 connections) — `tests/test_opencode_swarm_service.py`
- **.test_get_current_max_workers_gate_3()** (1 connections) — `tests/test_opencode_swarm_service.py`
- **.test_get_current_max_workers_negative()** (1 connections) — `tests/test_opencode_swarm_service.py`
- **.test_get_ramp_sequence()** (1 connections) — `tests/test_opencode_swarm_service.py`
- **.test_ramp_sequence_length()** (1 connections) — `tests/test_opencode_swarm_service.py`

## Relationships

- [SubTask](SubTask.md) (7 shared connections)
- [AgentSpec](AgentSpec.md) (6 shared connections)
- [WorkerPoolConfig](WorkerPoolConfig.md) (5 shared connections)
- [test_streaming_proxy.py](test_streaming_proxy.py.md) (3 shared connections)
- [CodebaseMapService](CodebaseMapService.md) (3 shared connections)
- [OpenCodeSwarmManager](OpenCodeSwarmManager.md) (2 shared connections)
- [WorkerRole](WorkerRole.md) (2 shared connections)
- [promotion_policy](promotion_policy.md) (1 shared connections)

## Source Files

- `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- `tests/test_opencode_swarm_service.py`

## Audit Trail

- EXTRACTED: 52 (73%)
- INFERRED: 19 (27%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*