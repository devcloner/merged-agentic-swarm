# Operator Runbook

> 12 nodes · cohesion 0.17

## Key Concepts

- **TestRun** (11 connections) — `tests/test_webapp.py`
- **.test_run_cancel_marks_cancelling()** (2 connections) — `tests/test_webapp.py`
- **.test_run_status_lists_and_details_runs()** (2 connections) — `tests/test_webapp.py`
- **#32: GET /api/run/status reports runs started by POST /api/run.** (1 connections) — `tests/test_webapp.py`
- **#32: POST /api/run/{id}/cancel signals the workflow's cancel_event.** (1 connections) — `tests/test_webapp.py`
- **.test_run_cancel_unknown_404()** (1 connections) — `tests/test_webapp.py`
- **.test_run_learning_profile_forwards_none_ramp()** (1 connections) — `tests/test_webapp.py`
- **.test_run_missing_prd_400()** (1 connections) — `tests/test_webapp.py`
- **.test_run_missing_profile_400()** (1 connections) — `tests/test_webapp.py`
- **.test_run_starts_workflow_in_background()** (1 connections) — `tests/test_webapp.py`
- **.test_run_status_unknown_404()** (1 connections) — `tests/test_webapp.py`
- **.test_run_unknown_profile_404()** (1 connections) — `tests/test_webapp.py`

## Relationships

- [ProxyChainHealth](ProxyChainHealth.md) (1 shared connections)
- [ObstaclePlaybookEngine](ObstaclePlaybookEngine.md) (1 shared connections)

## Source Files

- `tests/test_webapp.py`

## Audit Trail

- EXTRACTED: 23 (96%)
- INFERRED: 1 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*