---
type: community
cohesion: 0.33
members: 6
---

# TestCLIStringFunctions

**Cohesion:** 0.33 - loosely connected
**Members:** 6 nodes

## Members
- [[dot-test_cmd_promote_without_orchestrator_state()]] - code - tests/test_agentic_cli.py
- [[dot-test_cmd_status_no_progress_file()]] - code - tests/test_agentic_cli.py
- [[Test internal helper behaviors exposed through the CLI module.]] - rationale - tests/test_agentic_cli.py
- [[TestCLIStringFunctions]] - code - tests/test_agentic_cli.py
- [[cmd_promote should not crash when called directly (uses fresh orchestrator).]] - rationale - tests/test_agentic_cli.py
- [[cmd_status should handle a missing progress ledger gracefully.]] - rationale - tests/test_agentic_cli.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/TestCLIStringFunctions
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_services__init__.py]]
- 1 edge to [[_COMMUNITY_KeyPoolManager]]
- 1 edge to [[_COMMUNITY_test_agentic_cli.py]]

## Top bridge nodes
- [[TestCLIStringFunctions]] - degree 5, connects to 2 communities
- [[dot-test_cmd_promote_without_orchestrator_state()]] - degree 3, connects to 1 community
- [[dot-test_cmd_status_no_progress_file()]] - degree 3, connects to 1 community