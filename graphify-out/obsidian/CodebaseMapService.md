---
source_file: "src/merged_agentic_swarm/services/codebase_map_service.py"
type: "code"
community: "CodebaseMapService"
location: "L18"
tags:
  - graphify/code
  - graphify/INFERRED
  - community/CodebaseMapService
---

# CodebaseMapService

## Connections
- [[dot-__init__()_12]] - `method` [EXTRACTED]
- [[dot-_controller()]] - `calls` [INFERRED]
- [[dot-_is_gitignored()]] - `method` [EXTRACTED]
- [[dot-_is_ignored_path()]] - `method` [EXTRACTED]
- [[dot-_load_gitignore()]] - `method` [EXTRACTED]
- [[dot-_load_state()]] - `method` [EXTRACTED]
- [[dot-_parse_python_ast()]] - `method` [EXTRACTED]
- [[dot-_pattern_matches()]] - `method` [EXTRACTED]
- [[dot-_save_state()]] - `method` [EXTRACTED]
- [[dot-close_spec_gap()]] - `method` [EXTRACTED]
- [[dot-detect_spec_gaps()]] - `method` [EXTRACTED]
- [[dot-scan_repository()]] - `method` [EXTRACTED]
- [[dot-test_close_spec_gap()]] - `calls` [INFERRED]
- [[dot-test_close_spec_gap_not_found()]] - `calls` [INFERRED]
- [[dot-test_detect_hidden_directory()]] - `calls` [INFERRED]
- [[dot-test_detect_spec_gaps_no_gaps()]] - `calls` [INFERRED]
- [[dot-test_detect_spec_gaps_with_gaps()]] - `calls` [INFERRED]
- [[dot-test_gitignore_negation_allows_ignored_dir_file()]] - `calls` [INFERRED]
- [[dot-test_load_from_cache()]] - `calls` [INFERRED]
- [[dot-test_parse_invalid_file()]] - `calls` [INFERRED]
- [[dot-test_parse_python_ast_extracts_symbols()]] - `calls` [INFERRED]
- [[dot-test_scan_empty_repo()]] - `calls` [INFERRED]
- [[dot-test_scan_excludes_vendored_and_gitignored_paths()]] - `calls` [INFERRED]
- [[dot-test_scan_preserves_state_file()]] - `calls` [INFERRED]
- [[dot-test_scan_repo_with_python_file()]] - `calls` [INFERRED]
- [[dot-test_scan_skips_symlinked_directories()]] - `calls` [INFERRED]
- [[SpecGap]] - `uses` [INFERRED]
- [[TestCodebaseMapService]] - `uses` [INFERRED]
- [[TestWaveGateController]] - `uses` [INFERRED]
- [[TestWaveGatesWithRealState]] - `uses` [INFERRED]
- [[codebase_map_service.py]] - `contains` [EXTRACTED]
- [[isolated_codebase_mapper()]] - `calls` [INFERRED]
- [[services__init__.py]] - `imports` [EXTRACTED]

#graphify/code #graphify/INFERRED #community/CodebaseMapService