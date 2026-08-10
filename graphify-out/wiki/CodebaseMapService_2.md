# CodebaseMapService

> God node · 33 connections · `src/merged_agentic_swarm/services/codebase_map_service.py`

**Community:** [_router_with_keys](_router_with_keys.md)

## Connections by Relation

### calls
- ._controller() `INFERRED`
- isolated_codebase_mapper() `INFERRED`
- .test_close_spec_gap() `INFERRED`
- .test_gitignore_negation_allows_ignored_dir_file() `INFERRED`
- .test_scan_excludes_vendored_and_gitignored_paths() `INFERRED`
- .test_scan_skips_symlinked_directories() `INFERRED`
- .test_close_spec_gap_not_found() `INFERRED`
- .test_detect_hidden_directory() `INFERRED`
- .test_detect_spec_gaps_no_gaps() `INFERRED`
- .test_detect_spec_gaps_with_gaps() `INFERRED`
- .test_load_from_cache() `INFERRED`
- .test_parse_invalid_file() `INFERRED`
- .test_parse_python_ast_extracts_symbols() `INFERRED`
- .test_scan_empty_repo() `INFERRED`
- .test_scan_preserves_state_file() `INFERRED`
- .test_scan_repo_with_python_file() `INFERRED`

### contains
- codebase_map_service.py `EXTRACTED`

### imports
- [services/__init__.py](services-__init__.py.md) `EXTRACTED`

### method
- .scan_repository() `EXTRACTED`
- .detect_spec_gaps() `EXTRACTED`
- ._parse_python_ast() `EXTRACTED`
- .__init__() `EXTRACTED`
- ._is_gitignored() `EXTRACTED`
- ._is_ignored_path() `EXTRACTED`
- ._load_gitignore() `EXTRACTED`
- ._load_state() `EXTRACTED`
- ._save_state() `EXTRACTED`
- .close_spec_gap() `EXTRACTED`
- ._pattern_matches() `EXTRACTED`

### uses
- [TestWaveGatesWithRealState](TestWaveGatesWithRealState.md) `INFERRED`
- [TestWaveGateController](TestWaveGateController.md) `INFERRED`
- SpecGap `INFERRED`
- TestCodebaseMapService `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*