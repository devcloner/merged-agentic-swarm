# generate_progress_report.sh

> 19 nodes · cohesion 0.16

## Key Concepts

- **TestRunFullAgenticWorkflow** (17 connections) — `tests/test_agentic_orchestrator.py`
- **._stub_workflow()** (14 connections) — `tests/test_agentic_orchestrator.py`
- **.test_workflow_batch_exception_remediated()** (3 connections) — `tests/test_agentic_orchestrator.py`
- **.test_workflow_cancel_event_aborts_between_waves()** (3 connections) — `tests/test_agentic_orchestrator.py`
- **.test_workflow_default_path_omits_profile_kwargs()** (3 connections) — `tests/test_agentic_orchestrator.py`
- **.test_workflow_gates_disabled_does_not_abort()** (3 connections) — `tests/test_agentic_orchestrator.py`
- **.test_workflow_logs_deploy_events()** (3 connections) — `tests/test_agentic_orchestrator.py`
- **.test_workflow_threads_profile_ramp_and_model()** (3 connections) — `tests/test_agentic_orchestrator.py`
- **.test_workflow_threads_wave_level_into_swarm()** (3 connections) — `tests/test_agentic_orchestrator.py`
- **.test_workflow_simulation_failure_logged_and_epic_failed()** (2 connections) — `tests/test_agentic_orchestrator.py`
- **.test_workflow_success_all_waves()** (2 connections) — `tests/test_agentic_orchestrator.py`
- **.test_workflow_wave0_gate_failure_aborts()** (2 connections) — `tests/test_agentic_orchestrator.py`
- **gates=False keeps advance_wave() running (state advances) but a non-passing…** (1 connections) — `tests/test_agentic_orchestrator.py`
- **A run emits proxy_deployed (after init) and run_deployed (pre-wave)…** (1 connections) — `tests/test_agentic_orchestrator.py`
- **Each wave threads its wave number as wave_gate_level so the swarm executes at…** (1 connections) — `tests/test_agentic_orchestrator.py`
- **A provided ramp_sequence reaches every swarm batch, default_model is recorded…** (1 connections) — `tests/test_agentic_orchestrator.py`
- **Without a profile, the swarm batch gets no ramp_sequence kwarg and the ledger…** (1 connections) — `tests/test_agentic_orchestrator.py`
- **#32: a set cancel_event makes the workflow return an aborted result.** (1 connections) — `tests/test_agentic_orchestrator.py`
- **Wire the orchestrator singletons for a deterministic workflow run.** (1 connections) — `tests/test_agentic_orchestrator.py`

## Relationships

- [test_streaming_proxy.py](test_streaming_proxy.py.md) (4 shared connections)
- [WorkerRole](WorkerRole.md) (2 shared connections)
- [ProxyChainHealth](ProxyChainHealth.md) (2 shared connections)
- [AgenticWorkerLoop](AgenticWorkerLoop.md) (1 shared connections)

## Source Files

- `tests/test_agentic_orchestrator.py`

## Audit Trail

- EXTRACTED: 59 (91%)
- INFERRED: 6 (9%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*