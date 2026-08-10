---
type: community
cohesion: 0.14
members: 29
---

# _args

**Cohesion:** 0.14 - loosely connected
**Members:** 29 nodes

## Members
- [[19 cmd_status must point at the live ProgressLedgerService ledger.]] - rationale - tests/test_agentic_cli.py
- [[dot-_ledger()]] - code - tests/test_agentic_cli.py
- [[dot-_registry()]] - code - tests/test_agentic_cli.py
- [[dot-test_run_auto_saves_report_on_success()]] - code - tests/test_agentic_cli.py
- [[dot-test_run_does_not_autosave_on_failure()]] - code - tests/test_agentic_cli.py
- [[dot-test_run_exception_exits()]] - code - tests/test_agentic_cli.py
- [[dot-test_run_missing_prd_exits()]] - code - tests/test_agentic_cli.py
- [[dot-test_run_profile_resolves_and_passes_ramp_and_model()]] - code - tests/test_agentic_cli.py
- [[dot-test_run_profile_through_main()]] - code - tests/test_agentic_cli.py
- [[dot-test_run_success_prints_result()]] - code - tests/test_agentic_cli.py
- [[dot-test_run_unknown_profile_exits()]] - code - tests/test_agentic_cli.py
- [[dot-test_run_verbose_prints_full_json()]] - code - tests/test_agentic_cli.py
- [[dot-test_status_corrupt_ledger()]] - code - tests/test_agentic_cli.py
- [[dot-test_status_custom_progress_path()]] - code - tests/test_agentic_cli.py
- [[dot-test_status_defaults_to_real_ledger()]] - code - tests/test_agentic_cli.py
- [[dot-test_status_legacy_snapshot_still_renders()]] - code - tests/test_agentic_cli.py
- [[dot-test_status_no_progress()]] - code - tests/test_agentic_cli.py
- [[dot-test_status_with_ledger_and_registries()]] - code - tests/test_agentic_cli.py
- [[Fake save_run_report return, so auto-save never writes into the real repo.]] - rationale - tests/test_agentic_cli.py
- [[Old progress.json snapshots passed via --progress keep working.]] - rationale - tests/test_agentic_cli.py
- [[TestCmdRun]] - code - tests/test_agentic_cli.py
- [[TestCmdRunAutoSave]] - code - tests/test_agentic_cli.py
- [[TestCmdStatus]] - code - tests/test_agentic_cli.py
- [[_args()]] - code - tests/test_agentic_cli.py
- [[_fake_saved()]] - code - tests/test_agentic_cli.py
- [[_patch_auto_save()]] - code - tests/test_agentic_cli.py
- [[_write()]] - code - tests/test_agentic_cli.py
- [[`run --profile review` resolves the profile's waves as the ramp and the tier-…]] - rationale - tests/test_agentic_cli.py
- [[argparse wires `run --profile patch` into cmd_run with profile resolved.]] - rationale - tests/test_agentic_cli.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/_args
SORT file.name ASC
```

## Connections to other communities
- 12 edges to [[_COMMUNITY_test_agentic_cli.py]]
- 3 edges to [[_COMMUNITY_KeyPoolManager]]
- 1 edge to [[_COMMUNITY_services__init__.py]]
- 1 edge to [[_COMMUNITY__main_with_args]]

## Top bridge nodes
- [[TestCmdStatus]] - degree 10, connects to 2 communities
- [[TestCmdRun]] - degree 9, connects to 2 communities
- [[TestCmdRunAutoSave]] - degree 4, connects to 2 communities
- [[_args()]] - degree 18, connects to 1 community
- [[_write()]] - degree 14, connects to 1 community