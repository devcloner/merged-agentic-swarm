---
type: community
cohesion: 0.17
members: 20
---

# ProgressLedgerService

**Cohesion:** 0.17 - loosely connected
**Members:** 20 nodes

## Members
- [[dot-__init__()_16]] - code - src/merged_agentic_swarm/services/progress_ledger_service.py
- [[dot-load_ledger()]] - code - src/merged_agentic_swarm/services/progress_ledger_service.py
- [[dot-test_concurrent_save_ledger_produces_complete_json()]] - code - tests/test_progress_ledger_service.py
- [[dot-test_empty_ledger()]] - code - tests/test_progress_ledger_service.py
- [[dot-test_handle_task_failure()]] - code - tests/test_progress_ledger_service.py
- [[dot-test_load_corrupted_ledger()]] - code - tests/test_progress_ledger_service.py
- [[dot-test_log_progress()]] - code - tests/test_progress_ledger_service.py
- [[dot-test_log_progress_accepts_model_and_roundtrips()]] - code - tests/test_report_service.py
- [[dot-test_log_progress_model_appears_in_report()]] - code - tests/test_report_service.py
- [[dot-test_log_progress_model_defaults_to_none()]] - code - tests/test_report_service.py
- [[dot-test_log_progress_persists()]] - code - tests/test_progress_ledger_service.py
- [[dot-test_record_success_marker()]] - code - tests/test_progress_ledger_service.py
- [[dot-test_record_success_with_command_executed()]] - code - tests/test_progress_ledger_service.py
- [[dot-test_save_and_load_success_markers()]] - code - tests/test_progress_ledger_service.py
- [[dot-test_save_ledger_uses_unique_temp_name()]] - code - tests/test_progress_ledger_service.py
- [[Concurrent save_ledger calls must never leave a torn JSON target.]] - rationale - tests/test_progress_ledger_service.py
- [[ProgressLedgerService]] - code - src/merged_agentic_swarm/services/progress_ledger_service.py
- [[Regression for 41 temp file must not be the fixed target.tmp.]] - rationale - tests/test_progress_ledger_service.py
- [[TestLogProgressModelArg]] - code - tests/test_report_service.py
- [[TestProgressLedgerService]] - code - tests/test_progress_ledger_service.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ProgressLedgerService
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_ProgressLogEntry]]
- 4 edges to [[_COMMUNITY_ObstaclePlaybookEngine]]
- 4 edges to [[_COMMUNITY_dot-handle_task_failure]]
- 4 edges to [[_COMMUNITY_test_report_service.py]]
- 1 edge to [[_COMMUNITY_services__init__.py]]
- 1 edge to [[_COMMUNITY_PRDAnalysisResult]]
- 1 edge to [[_COMMUNITY_conftest.py]]

## Top bridge nodes
- [[ProgressLedgerService]] - degree 31, connects to 7 communities
- [[TestProgressLedgerService]] - degree 13, connects to 1 community
- [[TestLogProgressModelArg]] - degree 5, connects to 1 community
- [[dot-load_ledger()]] - degree 4, connects to 1 community
- [[dot-__init__()_16]] - degree 3, connects to 1 community