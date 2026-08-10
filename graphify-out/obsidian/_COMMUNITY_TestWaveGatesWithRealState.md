---
type: community
cohesion: 0.20
members: 24
---

# TestWaveGatesWithRealState

**Cohesion:** 0.20 - loosely connected
**Members:** 24 nodes

## Members
- [[dot-_controller()]] - code - tests/test_wave_gate_service.py
- [[dot-_wave3_ownership()]] - code - tests/test_wave_gate_service.py
- [[dot-_with_epics()]] - code - tests/test_wave_gate_service.py
- [[dot-_with_wave3_epics()]] - code - tests/test_wave_gate_service.py
- [[dot-test_advance_wave_fails_when_gate_not_passed()]] - code - tests/test_wave_gate_service.py
- [[dot-test_corrupt_ownership_map()]] - code - tests/test_wave_gate_service.py
- [[dot-test_ownership_forbidden_path_violation()]] - code - tests/test_wave_gate_service.py
- [[dot-test_ownership_map_missing_warns_and_passes()]] - code - tests/test_wave_gate_service.py
- [[dot-test_ownership_outside_owned_paths()]] - code - tests/test_wave_gate_service.py
- [[dot-test_ownership_pool_not_found()]] - code - tests/test_wave_gate_service.py
- [[dot-test_wave1_fails_on_incomplete_epics()]] - code - tests/test_wave_gate_service.py
- [[dot-test_wave1_passes_when_all_completed()]] - code - tests/test_wave_gate_service.py
- [[dot-test_wave3_gate_fails_on_syntax_errors()]] - code - tests/test_wave_gate_service.py
- [[dot-test_wave3_gate_fails_when_tests_not_run()]] - code - tests/test_wave_gate_service.py
- [[dot-test_wave3_gate_fails_without_verification()]] - code - tests/test_wave_gate_service.py
- [[dot-test_wave3_gate_passes_with_clean_verification()]] - code - tests/test_wave_gate_service.py
- [[Attach real epics (wave 1) with subtasks carrying output artifacts.]] - rationale - tests/test_wave_gate_service.py
- [[Attach real wave-3 epics whose subtasks output src artifacts.]] - rationale - tests/test_wave_gate_service.py
- [[Inline syntax fallback (no tests_ran) must not satisfy tests_passing.]] - rationale - tests/test_wave_gate_service.py
- [[TestWaveGatesWithRealState]] - code - tests/test_wave_gate_service.py
- [[Tests for serviceswave_gate_service.py Coverage WaveGateController —…]] - rationale - tests/test_wave_gate_service.py
- [[Wave 3 must not pass on statuses alone — verification must have run.]] - rationale - tests/test_wave_gate_service.py
- [[_ownership_map()]] - code - tests/test_wave_gate_service.py
- [[test_wave_gate_service.py]] - code - tests/test_wave_gate_service.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/TestWaveGatesWithRealState
SORT file.name ASC
```

## Connections to other communities
- 12 edges to [[_COMMUNITY_SubTask]]
- 2 edges to [[_COMMUNITY_CodebaseMapService]]
- 2 edges to [[_COMMUNITY_TaskMasterService]]
- 2 edges to [[_COMMUNITY_WaveGateController]]
- 1 edge to [[_COMMUNITY_TestWaveGateController]]

## Top bridge nodes
- [[TestWaveGatesWithRealState]] - degree 25, connects to 4 communities
- [[dot-_controller()]] - degree 16, connects to 3 communities
- [[test_wave_gate_service.py]] - degree 5, connects to 2 communities
- [[dot-_with_epics()]] - degree 13, connects to 1 community
- [[dot-_with_wave3_epics()]] - degree 9, connects to 1 community