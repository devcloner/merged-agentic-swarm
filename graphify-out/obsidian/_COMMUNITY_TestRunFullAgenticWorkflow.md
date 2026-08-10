---
type: community
cohesion: 0.16
members: 19
---

# TestRunFullAgenticWorkflow

**Cohesion:** 0.16 - loosely connected
**Members:** 19 nodes

## Members
- [[32 a set cancel_event makes the workflow return an aborted result.]] - rationale - tests/test_agentic_orchestrator.py
- [[dot-_stub_workflow()]] - code - tests/test_agentic_orchestrator.py
- [[dot-test_workflow_batch_exception_remediated()]] - code - tests/test_agentic_orchestrator.py
- [[dot-test_workflow_cancel_event_aborts_between_waves()]] - code - tests/test_agentic_orchestrator.py
- [[dot-test_workflow_default_path_omits_profile_kwargs()]] - code - tests/test_agentic_orchestrator.py
- [[dot-test_workflow_gates_disabled_does_not_abort()]] - code - tests/test_agentic_orchestrator.py
- [[dot-test_workflow_logs_deploy_events()]] - code - tests/test_agentic_orchestrator.py
- [[dot-test_workflow_simulation_failure_logged_and_epic_failed()]] - code - tests/test_agentic_orchestrator.py
- [[dot-test_workflow_success_all_waves()]] - code - tests/test_agentic_orchestrator.py
- [[dot-test_workflow_threads_profile_ramp_and_model()]] - code - tests/test_agentic_orchestrator.py
- [[dot-test_workflow_threads_wave_level_into_swarm()]] - code - tests/test_agentic_orchestrator.py
- [[dot-test_workflow_wave0_gate_failure_aborts()]] - code - tests/test_agentic_orchestrator.py
- [[A provided ramp_sequence reaches every swarm batch, default_model is recorded…]] - rationale - tests/test_agentic_orchestrator.py
- [[A run emits proxy_deployed (after init) and run_deployed (pre-wave)…]] - rationale - tests/test_agentic_orchestrator.py
- [[Each wave threads its wave number as wave_gate_level so the swarm executes at…]] - rationale - tests/test_agentic_orchestrator.py
- [[TestRunFullAgenticWorkflow]] - code - tests/test_agentic_orchestrator.py
- [[Wire the orchestrator singletons for a deterministic workflow run.]] - rationale - tests/test_agentic_orchestrator.py
- [[Without a profile, the swarm batch gets no ramp_sequence kwarg and the ledger…]] - rationale - tests/test_agentic_orchestrator.py
- [[gates=False keeps advance_wave() running (state advances) but a non-passing…]] - rationale - tests/test_agentic_orchestrator.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/TestRunFullAgenticWorkflow
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_SubTask]]
- 2 edges to [[_COMMUNITY_PRDAnalysisResult]]
- 2 edges to [[_COMMUNITY_MultiLayeredAgenticOrchestrator]]
- 1 edge to [[_COMMUNITY_AgenticWorkerLoop]]

## Top bridge nodes
- [[TestRunFullAgenticWorkflow]] - degree 17, connects to 3 communities
- [[dot-_stub_workflow()]] - degree 14, connects to 2 communities
- [[dot-test_workflow_batch_exception_remediated()]] - degree 3, connects to 1 community