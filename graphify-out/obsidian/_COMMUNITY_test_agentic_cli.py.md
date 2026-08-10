---
type: community
cohesion: 0.07
members: 56
---

# test_agentic_cli.py

**Cohesion:** 0.07 - loosely connected
**Members:** 56 nodes

## Members
- [[19 cmd_status must point at the live ProgressLedgerService ledger.]] - rationale - tests/test_agentic_cli.py
- [[dot-_ledger()]] - code - tests/test_agentic_cli.py
- [[dot-_registry()]] - code - tests/test_agentic_cli.py
- [[dot-_swarm_args()]] - code - tests/test_agentic_cli.py
- [[dot-_write_ledger()]] - code - tests/test_agentic_cli.py
- [[dot-setup_method()]] - code - tests/test_agentic_cli.py
- [[dot-test_config_routes_through_main()]] - code - tests/test_agentic_cli.py
- [[dot-test_no_command_prints_help_and_exits()]] - code - tests/test_agentic_cli.py
- [[dot-test_promote_exception_exits()]] - code - tests/test_agentic_cli.py
- [[dot-test_promote_success()]] - code - tests/test_agentic_cli.py
- [[dot-test_report_missing_ledger_writes_empty_report()]] - code - tests/test_agentic_cli.py
- [[dot-test_report_through_main()]] - code - tests/test_agentic_cli.py
- [[dot-test_report_writes_both_files_with_model_timeline()]] - code - tests/test_agentic_cli.py
- [[dot-test_run_auto_saves_report_on_success()]] - code - tests/test_agentic_cli.py
- [[dot-test_run_does_not_autosave_on_failure()]] - code - tests/test_agentic_cli.py
- [[dot-test_run_exception_exits()]] - code - tests/test_agentic_cli.py
- [[dot-test_run_missing_prd_exits()]] - code - tests/test_agentic_cli.py
- [[dot-test_run_missing_prd_exits_through_main()]] - code - tests/test_agentic_cli.py
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
- [[dot-test_swarm_handler_returns_resolved_profile()]] - code - tests/test_agentic_cli.py
- [[dot-test_swarm_learning_profile_reports_no_runnable_waves()]] - code - tests/test_agentic_cli.py
- [[dot-test_swarm_list_through_main()]] - code - tests/test_agentic_cli.py
- [[dot-test_swarm_profile_through_main()]] - code - tests/test_agentic_cli.py
- [[dot-test_swarm_unknown_profile_errors_clearly()]] - code - tests/test_agentic_cli.py
- [[dot-test_swarm_without_args_errors()]] - code - tests/test_agentic_cli.py
- [[Coverage for the swarm subcommand --list, --profile, and error paths.]] - rationale - tests/test_agentic_cli.py
- [[Fake save_run_report return, so auto-save never writes into the real repo.]] - rationale - tests/test_agentic_cli.py
- [[Old progress.json snapshots passed via --progress keep working.]] - rationale - tests/test_agentic_cli.py
- [[TestCmdPromote]] - code - tests/test_agentic_cli.py
- [[TestCmdReport]] - code - tests/test_agentic_cli.py
- [[TestCmdRun]] - code - tests/test_agentic_cli.py
- [[TestCmdRunAutoSave]] - code - tests/test_agentic_cli.py
- [[TestCmdStatus]] - code - tests/test_agentic_cli.py
- [[TestCmdSwarm]] - code - tests/test_agentic_cli.py
- [[TestMain]] - code - tests/test_agentic_cli.py
- [[Tests for toolsagentic_cli.py Coverage cmd_config, basic CLI parsing, cmd_run…]] - rationale - tests/test_agentic_cli.py
- [[_args()]] - code - tests/test_agentic_cli.py
- [[_fake_saved()]] - code - tests/test_agentic_cli.py
- [[_ledger_json()]] - code - tests/test_agentic_cli.py
- [[_ledger_log()]] - code - tests/test_agentic_cli.py
- [[_main_with_args()]] - code - tests/test_agentic_cli.py
- [[_patch_auto_save()]] - code - tests/test_agentic_cli.py
- [[_write()]] - code - tests/test_agentic_cli.py
- [[`run --profile review` resolves the profile's waves as the ramp and the tier-…]] - rationale - tests/test_agentic_cli.py
- [[argparse wires `run --profile patch` into cmd_run with profile resolved.]] - rationale - tests/test_agentic_cli.py
- [[test_agentic_cli.py]] - code - tests/test_agentic_cli.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/test_agentic_clipy
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_KeyPoolManager]]
- 3 edges to [[_COMMUNITY_services__init__.py]]
- 2 edges to [[_COMMUNITY_TestCmdProviders]]
- 1 edge to [[_COMMUNITY_AgenticWorkerLoop]]
- 1 edge to [[_COMMUNITY_TestTokenSavior]]
- 1 edge to [[_COMMUNITY_TestCLIStringFunctions]]
- 1 edge to [[_COMMUNITY_cmd_config]]

## Top bridge nodes
- [[test_agentic_cli.py]] - degree 20, connects to 5 communities
- [[_main_with_args()]] - degree 13, connects to 2 communities
- [[TestCmdSwarm]] - degree 11, connects to 1 community
- [[TestCmdStatus]] - degree 10, connects to 1 community
- [[TestCmdRun]] - degree 9, connects to 1 community