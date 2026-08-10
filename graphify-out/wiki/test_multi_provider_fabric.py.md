# test_multi_provider_fabric.py

> 24 nodes · cohesion 0.08

## Key Concepts

- **TestWaveGateController** (24 connections) — `tests/test_wave_gate_service.py`
- **.test_check_ownership_map_absent_passes()** (3 connections) — `tests/test_wave_gate_service.py`
- **.test_check_ownership_pool_missing_hard_fails()** (3 connections) — `tests/test_wave_gate_service.py`
- **.test_check_ownership_valid()** (3 connections) — `tests/test_wave_gate_service.py`
- **.test_advance_wave_beyond_all()** (2 connections) — `tests/test_wave_gate_service.py`
- **.test_advance_wave_passes()** (2 connections) — `tests/test_wave_gate_service.py`
- **.test_evaluate_gate_wave_0_passes()** (2 connections) — `tests/test_wave_gate_service.py`
- **.test_fail_advance_if_wave_not_pass()** (2 connections) — `tests/test_wave_gate_service.py`
- **.test_wave_2_gate_checks_execution()** (2 connections) — `tests/test_wave_gate_service.py`
- **.test_wave_3_gate_checks_verification()** (2 connections) — `tests/test_wave_gate_service.py`
- **Subtasks producing output within owned paths should have no violations.** (1 connections) — `tests/test_wave_gate_service.py`
- **#36: absent ownership map is an optional gate — warn and pass.** (1 connections) — `tests/test_wave_gate_service.py`
- **Map exists but the requested pool is absent — keep the hard-fail.** (1 connections) — `tests/test_wave_gate_service.py`
- **Wave 1 fails because task master has no tasks for it.** (1 connections) — `tests/test_wave_gate_service.py`
- **Wave 2 gate should evaluate with task_master data.** (1 connections) — `tests/test_wave_gate_service.py`
- **Wave 3 gate should evaluate with task_master data and ownership.** (1 connections) — `tests/test_wave_gate_service.py`
- **Wave 0 should pass when there are no unresolved spec gaps.** (1 connections) — `tests/test_wave_gate_service.py`
- **advance_wave should move from wave 0 to wave 1 if gate criteria pass.** (1 connections) — `tests/test_wave_gate_service.py`
- **advance_wave should complete after wave 3 (with verification recorded).** (1 connections) — `tests/test_wave_gate_service.py`
- **.test_advance_wave_sets_timestamps()** (1 connections) — `tests/test_wave_gate_service.py`
- **.test_evaluate_gate_invalid_wave()** (1 connections) — `tests/test_wave_gate_service.py`
- **.test_get_wave_state_invalid_defaults_to_0()** (1 connections) — `tests/test_wave_gate_service.py`
- **.test_get_wave_state_valid()** (1 connections) — `tests/test_wave_gate_service.py`
- **.test_initial_state()** (1 connections) — `tests/test_wave_gate_service.py`

## Relationships

- [test_streaming_proxy.py](test_streaming_proxy.py.md) (5 shared connections)
- [WorkerRole](WorkerRole.md) (3 shared connections)
- [models/__init__.py](models-__init__.py.md) (2 shared connections)
- [_router_with_keys](_router_with_keys.md) (1 shared connections)
- [TaskMasterService](TaskMasterService.md) (1 shared connections)
- [TestTokenSavior](TestTokenSavior.md) (1 shared connections)

## Source Files

- `tests/test_wave_gate_service.py`

## Audit Trail

- EXTRACTED: 51 (86%)
- INFERRED: 8 (14%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*