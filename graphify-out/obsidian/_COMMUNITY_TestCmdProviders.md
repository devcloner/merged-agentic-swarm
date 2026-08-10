---
type: community
cohesion: 0.70
members: 5
---

# TestCmdProviders

**Cohesion:** 0.70 - tightly connected
**Members:** 5 nodes

## Members
- [[dot-_setup()]] - code - tests/test_agentic_cli.py
- [[dot-test_providers_never_leaks_key_values()]] - code - tests/test_agentic_cli.py
- [[dot-test_providers_renders_key_names_env_names_and_routes()]] - code - tests/test_agentic_cli.py
- [[dot-test_providers_through_main()]] - code - tests/test_agentic_cli.py
- [[TestCmdProviders]] - code - tests/test_agentic_cli.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/TestCmdProviders
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_KeyPoolManager]]
- 1 edge to [[_COMMUNITY_test_agentic_cli.py]]
- 1 edge to [[_COMMUNITY__main_with_args]]

## Top bridge nodes
- [[TestCmdProviders]] - degree 6, connects to 2 communities
- [[dot-_setup()]] - degree 5, connects to 1 community
- [[dot-test_providers_through_main()]] - degree 3, connects to 1 community