# TestTokenSavior

> 24 nodes · cohesion 0.20

## Key Concepts

- **TestWaveGatesWithRealState** (25 connections) — `tests/test_wave_gate_service.py`
- **._controller()** (16 connections) — `tests/test_wave_gate_service.py`
- **._with_epics()** (13 connections) — `tests/test_wave_gate_service.py`
- **._with_wave3_epics()** (9 connections) — `tests/test_wave_gate_service.py`
- **_ownership_map()** (6 connections) — `tests/test_wave_gate_service.py`
- **._wave3_ownership()** (6 connections) — `tests/test_wave_gate_service.py`
- **test_wave_gate_service.py** (5 connections) — `tests/test_wave_gate_service.py`
- **.test_wave3_gate_fails_when_tests_not_run()** (5 connections) — `tests/test_wave_gate_service.py`
- **.test_wave3_gate_fails_without_verification()** (5 connections) — `tests/test_wave_gate_service.py`
- **.test_ownership_forbidden_path_violation()** (4 connections) — `tests/test_wave_gate_service.py`
- **.test_ownership_outside_owned_paths()** (4 connections) — `tests/test_wave_gate_service.py`
- **.test_ownership_pool_not_found()** (4 connections) — `tests/test_wave_gate_service.py`
- **.test_wave1_passes_when_all_completed()** (4 connections) — `tests/test_wave_gate_service.py`
- **.test_wave3_gate_fails_on_syntax_errors()** (4 connections) — `tests/test_wave_gate_service.py`
- **.test_wave3_gate_passes_with_clean_verification()** (4 connections) — `tests/test_wave_gate_service.py`
- **.test_advance_wave_fails_when_gate_not_passed()** (3 connections) — `tests/test_wave_gate_service.py`
- **.test_corrupt_ownership_map()** (3 connections) — `tests/test_wave_gate_service.py`
- **.test_ownership_map_missing_warns_and_passes()** (3 connections) — `tests/test_wave_gate_service.py`
- **.test_wave1_fails_on_incomplete_epics()** (3 connections) — `tests/test_wave_gate_service.py`
- **Tests for services/wave_gate_service.py Coverage: WaveGateController —…** (1 connections) — `tests/test_wave_gate_service.py`
- **Attach real epics (wave 1) with subtasks carrying output artifacts.** (1 connections) — `tests/test_wave_gate_service.py`
- **Attach real wave-3 epics whose subtasks output src/ artifacts.** (1 connections) — `tests/test_wave_gate_service.py`
- **Wave 3 must not pass on statuses alone — verification must have run.** (1 connections) — `tests/test_wave_gate_service.py`
- **Inline syntax fallback (no tests_ran) must not satisfy tests_passing.** (1 connections) — `tests/test_wave_gate_service.py`

## Relationships

- [WorkerRole](WorkerRole.md) (6 shared connections)
- [test_streaming_proxy.py](test_streaming_proxy.py.md) (6 shared connections)
- [_router_with_keys](_router_with_keys.md) (2 shared connections)
- [TaskMasterService](TaskMasterService.md) (2 shared connections)
- [models/__init__.py](models-__init__.py.md) (2 shared connections)
- [test_multi_provider_fabric.py](test_multi_provider_fabric.py.md) (1 shared connections)

## Source Files

- `tests/test_wave_gate_service.py`

## Audit Trail

- EXTRACTED: 120 (92%)
- INFERRED: 11 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*