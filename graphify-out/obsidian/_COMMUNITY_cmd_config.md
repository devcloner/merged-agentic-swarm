---
type: community
cohesion: 0.25
members: 9
---

# cmd_config

**Cohesion:** 0.25 - loosely connected
**Members:** 9 nodes

## Members
- [[dot-test_cmd_config_output()]] - code - tests/test_agentic_cli.py
- [[dot-test_cmd_config_routes_printed()]] - code - tests/test_agentic_cli.py
- [[dot-test_main_entry_points()]] - code - tests/test_agentic_cli.py
- [[Show configuration state.]] - rationale - src/merged_agentic_swarm/tools/agentic_cli.py
- [[TestCmdConfig]] - code - tests/test_agentic_cli.py
- [[Verify argparse setup works for each subcommand.]] - rationale - tests/test_agentic_cli.py
- [[Verify model routes appear in config output.]] - rationale - tests/test_agentic_cli.py
- [[cmd_config should print key pool, routes, and swarm info without crashing.]] - rationale - tests/test_agentic_cli.py
- [[cmd_config()]] - code - src/merged_agentic_swarm/tools/agentic_cli.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/cmd_config
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_services__init__.py]]
- 1 edge to [[_COMMUNITY_WorkerRole]]
- 1 edge to [[_COMMUNITY_KeyPoolManager]]
- 1 edge to [[_COMMUNITY_test_agentic_cli.py]]

## Top bridge nodes
- [[cmd_config()]] - degree 6, connects to 2 communities
- [[TestCmdConfig]] - degree 5, connects to 2 communities
- [[dot-test_main_entry_points()]] - degree 3, connects to 1 community