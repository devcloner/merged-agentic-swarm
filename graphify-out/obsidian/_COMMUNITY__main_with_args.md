---
type: community
cohesion: 0.20
members: 15
---

# _main_with_args

**Cohesion:** 0.20 - loosely connected
**Members:** 15 nodes

## Members
- [[dot-_swarm_args()]] - code - tests/test_agentic_cli.py
- [[dot-setup_method()]] - code - tests/test_agentic_cli.py
- [[dot-test_config_routes_through_main()]] - code - tests/test_agentic_cli.py
- [[dot-test_no_command_prints_help_and_exits()]] - code - tests/test_agentic_cli.py
- [[dot-test_run_missing_prd_exits_through_main()]] - code - tests/test_agentic_cli.py
- [[dot-test_swarm_handler_returns_resolved_profile()]] - code - tests/test_agentic_cli.py
- [[dot-test_swarm_learning_profile_reports_no_runnable_waves()]] - code - tests/test_agentic_cli.py
- [[dot-test_swarm_list_through_main()]] - code - tests/test_agentic_cli.py
- [[dot-test_swarm_profile_through_main()]] - code - tests/test_agentic_cli.py
- [[dot-test_swarm_unknown_profile_errors_clearly()]] - code - tests/test_agentic_cli.py
- [[dot-test_swarm_without_args_errors()]] - code - tests/test_agentic_cli.py
- [[Coverage for the swarm subcommand --list, --profile, and error paths.]] - rationale - tests/test_agentic_cli.py
- [[TestCmdSwarm]] - code - tests/test_agentic_cli.py
- [[TestMain]] - code - tests/test_agentic_cli.py
- [[_main_with_args()]] - code - tests/test_agentic_cli.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/_main_with_args
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_test_agentic_cli.py]]
- 2 edges to [[_COMMUNITY_KeyPoolManager]]
- 1 edge to [[_COMMUNITY_services__init__.py]]
- 1 edge to [[_COMMUNITY_TestCmdProviders]]
- 1 edge to [[_COMMUNITY__args]]

## Top bridge nodes
- [[_main_with_args()]] - degree 13, connects to 4 communities
- [[TestCmdSwarm]] - degree 11, connects to 2 communities
- [[TestMain]] - degree 5, connects to 2 communities