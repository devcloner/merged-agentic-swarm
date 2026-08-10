---
type: community
cohesion: 0.08
members: 40
---

# CodebaseMapService

**Cohesion:** 0.08 - loosely connected
**Members:** 40 nodes

## Members
- [[37 `!` negation re-includes a path ignored by a broader pattern.]] - rationale - tests/test_codebase_map_service.py
- [[37 symlinked dirs must not be walked (avoids duplicate trees).]] - rationale - tests/test_codebase_map_service.py
- [[37 vendoredbuild dirs and .gitignore'd paths must be excluded.]] - rationale - tests/test_codebase_map_service.py
- [[dot-__init__()_12]] - code - src/merged_agentic_swarm/services/codebase_map_service.py
- [[dot-_is_gitignored()]] - code - src/merged_agentic_swarm/services/codebase_map_service.py
- [[dot-_is_ignored_path()]] - code - src/merged_agentic_swarm/services/codebase_map_service.py
- [[dot-_load_gitignore()]] - code - src/merged_agentic_swarm/services/codebase_map_service.py
- [[dot-_load_state()]] - code - src/merged_agentic_swarm/services/codebase_map_service.py
- [[dot-_parse_python_ast()]] - code - src/merged_agentic_swarm/services/codebase_map_service.py
- [[dot-_pattern_matches()]] - code - src/merged_agentic_swarm/services/codebase_map_service.py
- [[dot-_save_state()]] - code - src/merged_agentic_swarm/services/codebase_map_service.py
- [[dot-close_spec_gap()]] - code - src/merged_agentic_swarm/services/codebase_map_service.py
- [[dot-detect_spec_gaps()]] - code - src/merged_agentic_swarm/services/codebase_map_service.py
- [[dot-scan_repository()]] - code - src/merged_agentic_swarm/services/codebase_map_service.py
- [[dot-test_close_spec_gap()]] - code - tests/test_codebase_map_service.py
- [[dot-test_close_spec_gap_not_found()]] - code - tests/test_codebase_map_service.py
- [[dot-test_detect_hidden_directory()]] - code - tests/test_codebase_map_service.py
- [[dot-test_detect_spec_gaps_no_gaps()]] - code - tests/test_codebase_map_service.py
- [[dot-test_detect_spec_gaps_with_gaps()]] - code - tests/test_codebase_map_service.py
- [[dot-test_gitignore_negation_allows_ignored_dir_file()]] - code - tests/test_codebase_map_service.py
- [[dot-test_load_from_cache()]] - code - tests/test_codebase_map_service.py
- [[dot-test_parse_invalid_file()]] - code - tests/test_codebase_map_service.py
- [[dot-test_parse_python_ast_extracts_symbols()]] - code - tests/test_codebase_map_service.py
- [[dot-test_scan_empty_repo()]] - code - tests/test_codebase_map_service.py
- [[dot-test_scan_excludes_vendored_and_gitignored_paths()]] - code - tests/test_codebase_map_service.py
- [[dot-test_scan_preserves_state_file()]] - code - tests/test_codebase_map_service.py
- [[dot-test_scan_repo_with_python_file()]] - code - tests/test_codebase_map_service.py
- [[dot-test_scan_skips_symlinked_directories()]] - code - tests/test_codebase_map_service.py
- [[Any_14]] - code
- [[Closes a specific spec gap after verifying fixes.]] - rationale - src/merged_agentic_swarm/services/codebase_map_service.py
- [[CodebaseMapService]] - code - src/merged_agentic_swarm/services/codebase_map_service.py
- [[Cross-references required components against mapped codebase to find spec gaps.…]] - rationale - src/merged_agentic_swarm/services/codebase_map_service.py
- [[Load persisted codebase map state from disk.]] - rationale - src/merged_agentic_swarm/services/codebase_map_service.py
- [[Load the repo-root .gitignore into (pattern, dir_only) matcher lists. Covers…]] - rationale - src/merged_agentic_swarm/services/codebase_map_service.py
- [[Parses Python file to extract top-level functions, classes, and imports.]] - rationale - src/merged_agentic_swarm/services/codebase_map_service.py
- [[Persist codebase map state so restart doesn't require re-scan.]] - rationale - src/merged_agentic_swarm/services/codebase_map_service.py
- [[Scans workspace repository files and parses AST definitions.]] - rationale - src/merged_agentic_swarm/services/codebase_map_service.py
- [[TestCodebaseMapService]] - code - tests/test_codebase_map_service.py
- [[Tests for servicescodebase_map_service.py Coverage CodebaseMapService —…]] - rationale - tests/test_codebase_map_service.py
- [[test_codebase_map_service.py]] - code - tests/test_codebase_map_service.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/CodebaseMapService
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_SubTask]]
- 2 edges to [[_COMMUNITY_TestWaveGatesWithRealState]]
- 1 edge to [[_COMMUNITY_services__init__.py]]
- 1 edge to [[_COMMUNITY_conftest.py]]
- 1 edge to [[_COMMUNITY_TestWaveGateController]]

## Top bridge nodes
- [[CodebaseMapService]] - degree 33, connects to 5 communities
- [[TestCodebaseMapService]] - degree 17, connects to 1 community
- [[dot-detect_spec_gaps()]] - degree 4, connects to 1 community
- [[test_codebase_map_service.py]] - degree 3, connects to 1 community
- [[dot-test_close_spec_gap()]] - degree 3, connects to 1 community