---
type: community
cohesion: 0.09
members: 42
---

# WaveGateController

**Cohesion:** 0.09 - loosely connected
**Members:** 42 nodes

## Members
- [[dot-__init__()_20]] - code - src/merged_agentic_swarm/services/wave_gate_service.py
- [[dot-_check_ownership()]] - code - src/merged_agentic_swarm/services/wave_gate_service.py
- [[dot-_evaluate_verification_criteria()]] - code - src/merged_agentic_swarm/services/wave_gate_service.py
- [[dot-advance_wave()]] - code - src/merged_agentic_swarm/services/wave_gate_service.py
- [[dot-evaluate_gate_criteria()]] - code - src/merged_agentic_swarm/services/wave_gate_service.py
- [[dot-get_wave_state()]] - code - src/merged_agentic_swarm/services/wave_gate_service.py
- [[dot-record_verification_results()]] - code - src/merged_agentic_swarm/services/wave_gate_service.py
- [[dot-test_advance_to_in_progress()]] - code - tests/test_wave_models.py
- [[dot-test_custom_checks()]] - code - tests/test_wave_models.py
- [[dot-test_default_creation()_13]] - code - tests/test_wave_models.py
- [[dot-test_default_creation()_12]] - code - tests/test_wave_models.py
- [[dot-test_failure()]] - code - tests/test_wave_models.py
- [[dot-test_ordering()]] - code - tests/test_wave_models.py
- [[dot-test_to_dict()_8]] - code - tests/test_wave_models.py
- [[dot-test_to_dict()_7]] - code - tests/test_wave_models.py
- [[dot-test_values()_4]] - code - tests/test_wave_models.py
- [[dot-test_values()_5]] - code - tests/test_wave_models.py
- [[dot-to_dict()_12]] - code - src/merged_agentic_swarm/models/wave_models.py
- [[dot-to_dict()_11]] - code - src/merged_agentic_swarm/models/wave_models.py
- [[Any_7]] - code
- [[Any_20]] - code
- [[Attempts to pass the current wave gate and advance to the next wave.]] - rationale - src/merged_agentic_swarm/services/wave_gate_service.py
- [[Enum_2]] - code
- [[Evaluate Wave 3's Zero-Defect verification criteria. Uses the results recorded…]] - rationale - src/merged_agentic_swarm/services/wave_gate_service.py
- [[Evaluates whether all criteria for a wave gate are met.]] - rationale - src/merged_agentic_swarm/services/wave_gate_service.py
- [[Record the Wave-3 verification outcome for the Zero-Defect gate. Accepts the…]] - rationale - src/merged_agentic_swarm/services/wave_gate_service.py
- [[TestWaveExecutionState]] - code - tests/test_wave_models.py
- [[TestWaveGateCriteria]] - code - tests/test_wave_models.py
- [[TestWavePhase]] - code - tests/test_wave_models.py
- [[TestWaveStatus]] - code - tests/test_wave_models.py
- [[Tests for modelswave_models.py Coverage WavePhase, WaveStatus,…]] - rationale - tests/test_wave_models.py
- [[Verify each subtask's output paths against the ownership map for pool_id.…]] - rationale - src/merged_agentic_swarm/services/wave_gate_service.py
- [[Wave Gates Data Models]] - rationale - src/merged_agentic_swarm/models/wave_models.py
- [[WaveExecutionState]] - code - src/merged_agentic_swarm/models/wave_models.py
- [[WaveGateController]] - code - src/merged_agentic_swarm/services/wave_gate_service.py
- [[WaveGateCriteria]] - code - src/merged_agentic_swarm/models/wave_models.py
- [[WavePhase]] - code - src/merged_agentic_swarm/models/wave_models.py
- [[WaveStatus]] - code - src/merged_agentic_swarm/models/wave_models.py
- [[int]] - code
- [[str_2]] - code
- [[test_wave_models.py]] - code - tests/test_wave_models.py
- [[wave_models.py]] - code - src/merged_agentic_swarm/models/wave_models.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/WaveGateController
SORT file.name ASC
```

## Connections to other communities
- 10 edges to [[_COMMUNITY_PRDAnalysisResult]]
- 2 edges to [[_COMMUNITY_SubTask]]
- 2 edges to [[_COMMUNITY_TestWaveGateController]]
- 2 edges to [[_COMMUNITY_TestWaveGatesWithRealState]]
- 1 edge to [[_COMMUNITY_services__init__.py]]
- 1 edge to [[_COMMUNITY_conftest.py]]

## Top bridge nodes
- [[WaveGateController]] - degree 18, connects to 6 communities
- [[WaveExecutionState]] - degree 16, connects to 1 community
- [[WaveGateCriteria]] - degree 13, connects to 1 community
- [[WaveStatus]] - degree 10, connects to 1 community
- [[wave_models.py]] - degree 9, connects to 1 community