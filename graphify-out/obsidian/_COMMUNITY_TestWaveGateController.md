---
type: community
cohesion: 0.08
members: 25
---

# TestWaveGateController

**Cohesion:** 0.08 - loosely connected
**Members:** 25 nodes

## Members
- [[36 absent ownership map is an optional gate — warn and pass.]] - rationale - tests/test_wave_gate_service.py
- [[dot-setup_method()_20]] - code - tests/test_wave_gate_service.py
- [[dot-test_advance_wave_beyond_all()]] - code - tests/test_wave_gate_service.py
- [[dot-test_advance_wave_passes()]] - code - tests/test_wave_gate_service.py
- [[dot-test_advance_wave_sets_timestamps()]] - code - tests/test_wave_gate_service.py
- [[dot-test_check_ownership_map_absent_passes()]] - code - tests/test_wave_gate_service.py
- [[dot-test_check_ownership_pool_missing_hard_fails()]] - code - tests/test_wave_gate_service.py
- [[dot-test_check_ownership_valid()]] - code - tests/test_wave_gate_service.py
- [[dot-test_evaluate_gate_invalid_wave()]] - code - tests/test_wave_gate_service.py
- [[dot-test_evaluate_gate_wave_0_passes()]] - code - tests/test_wave_gate_service.py
- [[dot-test_fail_advance_if_wave_not_pass()]] - code - tests/test_wave_gate_service.py
- [[dot-test_get_wave_state_invalid_defaults_to_0()]] - code - tests/test_wave_gate_service.py
- [[dot-test_get_wave_state_valid()]] - code - tests/test_wave_gate_service.py
- [[dot-test_initial_state()]] - code - tests/test_wave_gate_service.py
- [[dot-test_wave_2_gate_checks_execution()]] - code - tests/test_wave_gate_service.py
- [[dot-test_wave_3_gate_checks_verification()]] - code - tests/test_wave_gate_service.py
- [[Map exists but the requested pool is absent — keep the hard-fail.]] - rationale - tests/test_wave_gate_service.py
- [[Subtasks producing output within owned paths should have no violations.]] - rationale - tests/test_wave_gate_service.py
- [[TestWaveGateController]] - code - tests/test_wave_gate_service.py
- [[Wave 0 should pass when there are no unresolved spec gaps.]] - rationale - tests/test_wave_gate_service.py
- [[Wave 1 fails because task master has no tasks for it.]] - rationale - tests/test_wave_gate_service.py
- [[Wave 2 gate should evaluate with task_master data.]] - rationale - tests/test_wave_gate_service.py
- [[Wave 3 gate should evaluate with task_master data and ownership.]] - rationale - tests/test_wave_gate_service.py
- [[advance_wave should complete after wave 3 (with verification recorded).]] - rationale - tests/test_wave_gate_service.py
- [[advance_wave should move from wave 0 to wave 1 if gate criteria pass.]] - rationale - tests/test_wave_gate_service.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/TestWaveGateController
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_SubTask]]
- 3 edges to [[_COMMUNITY_PRDAnalysisResult]]
- 2 edges to [[_COMMUNITY_WaveGateController]]
- 1 edge to [[_COMMUNITY_CodebaseMapService]]
- 1 edge to [[_COMMUNITY_TaskMasterService]]
- 1 edge to [[_COMMUNITY_TestWaveGatesWithRealState]]

## Top bridge nodes
- [[TestWaveGateController]] - degree 24, connects to 6 communities
- [[dot-test_check_ownership_map_absent_passes()]] - degree 3, connects to 1 community
- [[dot-test_check_ownership_pool_missing_hard_fails()]] - degree 3, connects to 1 community
- [[dot-test_check_ownership_valid()]] - degree 3, connects to 1 community
- [[dot-setup_method()_20]] - degree 2, connects to 1 community