# TestRunFullAgenticWorkflow

> 20 nodes · cohesion 0.17

## Key Concepts

- **ProgressLedgerService** (31 connections) — `src/merged_agentic_swarm/services/progress_ledger_service.py`
- **TestProgressLedgerService** (13 connections) — `tests/test_progress_ledger_service.py`
- **TestLogProgressModelArg** (5 connections) — `tests/test_report_service.py`
- **.load_ledger()** (4 connections) — `src/merged_agentic_swarm/services/progress_ledger_service.py`
- **.__init__()** (3 connections) — `src/merged_agentic_swarm/services/progress_ledger_service.py`
- **.test_concurrent_save_ledger_produces_complete_json()** (3 connections) — `tests/test_progress_ledger_service.py`
- **.test_save_ledger_uses_unique_temp_name()** (3 connections) — `tests/test_progress_ledger_service.py`
- **.test_empty_ledger()** (2 connections) — `tests/test_progress_ledger_service.py`
- **.test_handle_task_failure()** (2 connections) — `tests/test_progress_ledger_service.py`
- **.test_load_corrupted_ledger()** (2 connections) — `tests/test_progress_ledger_service.py`
- **.test_log_progress()** (2 connections) — `tests/test_progress_ledger_service.py`
- **.test_log_progress_persists()** (2 connections) — `tests/test_progress_ledger_service.py`
- **.test_record_success_marker()** (2 connections) — `tests/test_progress_ledger_service.py`
- **.test_record_success_with_command_executed()** (2 connections) — `tests/test_progress_ledger_service.py`
- **.test_save_and_load_success_markers()** (2 connections) — `tests/test_progress_ledger_service.py`
- **.test_log_progress_accepts_model_and_roundtrips()** (2 connections) — `tests/test_report_service.py`
- **.test_log_progress_model_appears_in_report()** (2 connections) — `tests/test_report_service.py`
- **.test_log_progress_model_defaults_to_none()** (2 connections) — `tests/test_report_service.py`
- **Regression for #41: temp file must not be the fixed <target>.tmp.** (1 connections) — `tests/test_progress_ledger_service.py`
- **Concurrent save_ledger calls must never leave a torn JSON target.** (1 connections) — `tests/test_progress_ledger_service.py`

## Relationships

- [ProgressLogEntry](ProgressLogEntry.md) (6 shared connections)
- [verify_worker_runtime.sh](verify_worker_runtime.sh.md) (4 shared connections)
- [_evaluate_promotion_criteria](_evaluate_promotion_criteria.md) (4 shared connections)
- [APIKeyInfo](APIKeyInfo.md) (4 shared connections)
- [PassthroughStreamingProxy](PassthroughStreamingProxy.md) (1 shared connections)
- [conftest.py](conftest.py.md) (1 shared connections)

## Source Files

- `src/merged_agentic_swarm/services/progress_ledger_service.py`
- `tests/test_progress_ledger_service.py`
- `tests/test_report_service.py`

## Audit Trail

- EXTRACTED: 47 (55%)
- INFERRED: 39 (45%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*