# models/__init__.py

> 43 nodes · cohesion 0.09

## Key Concepts

- **WaveGateController** (18 connections) — `src/merged_agentic_swarm/services/wave_gate_service.py`
- **WaveExecutionState** (16 connections) — `src/merged_agentic_swarm/models/wave_models.py`
- **WaveGateCriteria** (13 connections) — `src/merged_agentic_swarm/models/wave_models.py`
- **WaveStatus** (10 connections) — `src/merged_agentic_swarm/models/wave_models.py`
- **wave_models.py** (9 connections) — `src/merged_agentic_swarm/models/wave_models.py`
- **TestWaveExecutionState** (9 connections) — `tests/test_wave_models.py`
- **WavePhase** (8 connections) — `src/merged_agentic_swarm/models/wave_models.py`
- **TestWaveGateCriteria** (8 connections) — `tests/test_wave_models.py`
- **TestWavePhase** (7 connections) — `tests/test_wave_models.py`
- **test_wave_models.py** (6 connections) — `tests/test_wave_models.py`
- **TestWaveStatus** (6 connections) — `tests/test_wave_models.py`
- **.evaluate_gate_criteria()** (5 connections) — `src/merged_agentic_swarm/services/wave_gate_service.py`
- **._check_ownership()** (4 connections) — `src/merged_agentic_swarm/services/wave_gate_service.py`
- **._evaluate_verification_criteria()** (4 connections) — `src/merged_agentic_swarm/services/wave_gate_service.py`
- **Enum** (3 connections)
- **.advance_wave()** (3 connections) — `src/merged_agentic_swarm/services/wave_gate_service.py`
- **.__init__()** (3 connections) — `src/merged_agentic_swarm/services/wave_gate_service.py`
- **.record_verification_results()** (3 connections) — `src/merged_agentic_swarm/services/wave_gate_service.py`
- **Any** (2 connections)
- **.to_dict()** (2 connections) — `src/merged_agentic_swarm/models/wave_models.py`
- **.to_dict()** (2 connections) — `src/merged_agentic_swarm/models/wave_models.py`
- **.get_wave_state()** (2 connections) — `src/merged_agentic_swarm/services/wave_gate_service.py`
- **.setup_method()** (2 connections) — `tests/test_wave_gate_service.py`
- **.test_advance_to_in_progress()** (2 connections) — `tests/test_wave_models.py`
- **.test_default_creation()** (2 connections) — `tests/test_wave_models.py`
- *... and 18 more nodes in this community*

## Relationships

- [WorkerRole](WorkerRole.md) (10 shared connections)
- [test_streaming_proxy.py](test_streaming_proxy.py.md) (2 shared connections)
- [test_multi_provider_fabric.py](test_multi_provider_fabric.py.md) (2 shared connections)
- [TestTokenSavior](TestTokenSavior.md) (2 shared connections)
- [PassthroughStreamingProxy](PassthroughStreamingProxy.md) (1 shared connections)
- [conftest.py](conftest.py.md) (1 shared connections)

## Source Files

- `src/merged_agentic_swarm/models/wave_models.py`
- `src/merged_agentic_swarm/services/wave_gate_service.py`
- `tests/test_wave_gate_service.py`
- `tests/test_wave_models.py`

## Audit Trail

- EXTRACTED: 127 (74%)
- INFERRED: 45 (26%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*