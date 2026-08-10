# TaskMasterService

> 33 nodes · cohesion 0.10

## Key Concepts

- **TaskMasterService** (38 connections) — `src/merged_agentic_swarm/services/task_master_service.py`
- **TestTaskMasterService** (21 connections) — `tests/test_task_master_service.py`
- **.optimize_and_parse_prd()** (8 connections) — `src/merged_agentic_swarm/services/task_master_service.py`
- **.save_state()** (4 connections) — `src/merged_agentic_swarm/services/task_master_service.py`
- **.update_task_status()** (4 connections) — `src/merged_agentic_swarm/services/task_master_service.py`
- **.test_concurrent_saves_produce_complete_json()** (4 connections) — `tests/test_task_master_service.py`
- **.test_save_state_uses_unique_temp_name()** (4 connections) — `tests/test_task_master_service.py`
- **._estimate_turns()** (3 connections) — `src/merged_agentic_swarm/services/task_master_service.py`
- **test_task_master_service.py** (3 connections) — `tests/test_task_master_service.py`
- **.test_optimize_and_parse_prd()** (3 connections) — `tests/test_task_master_service.py`
- **.test_empty_state()** (2 connections) — `tests/test_task_master_service.py`
- **.test_estimate_turns_capped()** (2 connections) — `tests/test_task_master_service.py`
- **.test_estimate_turns_complex()** (2 connections) — `tests/test_task_master_service.py`
- **.test_estimate_turns_simple()** (2 connections) — `tests/test_task_master_service.py`
- **.test_get_tasks_for_wave()** (2 connections) — `tests/test_task_master_service.py`
- **.test_get_tasks_for_wave_no_analysis()** (2 connections) — `tests/test_task_master_service.py`
- **.test_load_corrupted_state()** (2 connections) — `tests/test_task_master_service.py`
- **.test_load_existing_state()** (2 connections) — `tests/test_task_master_service.py`
- **.test_optimize_and_parse_prd_persists()** (2 connections) — `tests/test_task_master_service.py`
- **.test_prd_analysis_includes_fabric_preview()** (2 connections) — `tests/test_task_master_service.py`
- **.test_update_task_status_epic()** (2 connections) — `tests/test_task_master_service.py`
- **.test_update_task_status_no_analysis()** (2 connections) — `tests/test_task_master_service.py`
- **.test_update_task_status_subtask()** (2 connections) — `tests/test_task_master_service.py`
- **.test_update_task_status_with_error()** (2 connections) — `tests/test_task_master_service.py`
- **Parses and optimizes PRD via Task Master AI model fabric routing. Calls the…** (1 connections) — `src/merged_agentic_swarm/services/task_master_service.py`
- *... and 8 more nodes in this community*

## Relationships

- [WorkerRole](WorkerRole.md) (15 shared connections)
- [test_streaming_proxy.py](test_streaming_proxy.py.md) (5 shared connections)
- [TestTokenSavior](TestTokenSavior.md) (2 shared connections)
- [PassthroughStreamingProxy](PassthroughStreamingProxy.md) (1 shared connections)
- [conftest.py](conftest.py.md) (1 shared connections)
- [test_multi_provider_fabric.py](test_multi_provider_fabric.py.md) (1 shared connections)

## Source Files

- `src/merged_agentic_swarm/services/task_master_service.py`
- `tests/test_task_master_service.py`

## Audit Trail

- EXTRACTED: 81 (63%)
- INFERRED: 48 (37%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*