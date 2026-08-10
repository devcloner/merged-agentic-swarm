# _router_with_keys

> 40 nodes · cohesion 0.08

## Key Concepts

- **CodebaseMapService** (33 connections) — `src/merged_agentic_swarm/services/codebase_map_service.py`
- **TestCodebaseMapService** (17 connections) — `tests/test_codebase_map_service.py`
- **.scan_repository()** (7 connections) — `src/merged_agentic_swarm/services/codebase_map_service.py`
- **.detect_spec_gaps()** (4 connections) — `src/merged_agentic_swarm/services/codebase_map_service.py`
- **._parse_python_ast()** (4 connections) — `src/merged_agentic_swarm/services/codebase_map_service.py`
- **.__init__()** (3 connections) — `src/merged_agentic_swarm/services/codebase_map_service.py`
- **._is_gitignored()** (3 connections) — `src/merged_agentic_swarm/services/codebase_map_service.py`
- **._is_ignored_path()** (3 connections) — `src/merged_agentic_swarm/services/codebase_map_service.py`
- **._load_gitignore()** (3 connections) — `src/merged_agentic_swarm/services/codebase_map_service.py`
- **._load_state()** (3 connections) — `src/merged_agentic_swarm/services/codebase_map_service.py`
- **._save_state()** (3 connections) — `src/merged_agentic_swarm/services/codebase_map_service.py`
- **test_codebase_map_service.py** (3 connections) — `tests/test_codebase_map_service.py`
- **.test_close_spec_gap()** (3 connections) — `tests/test_codebase_map_service.py`
- **.test_gitignore_negation_allows_ignored_dir_file()** (3 connections) — `tests/test_codebase_map_service.py`
- **.test_scan_excludes_vendored_and_gitignored_paths()** (3 connections) — `tests/test_codebase_map_service.py`
- **.test_scan_skips_symlinked_directories()** (3 connections) — `tests/test_codebase_map_service.py`
- **.close_spec_gap()** (2 connections) — `src/merged_agentic_swarm/services/codebase_map_service.py`
- **._pattern_matches()** (2 connections) — `src/merged_agentic_swarm/services/codebase_map_service.py`
- **Any** (2 connections)
- **.test_close_spec_gap_not_found()** (2 connections) — `tests/test_codebase_map_service.py`
- **.test_detect_hidden_directory()** (2 connections) — `tests/test_codebase_map_service.py`
- **.test_detect_spec_gaps_no_gaps()** (2 connections) — `tests/test_codebase_map_service.py`
- **.test_detect_spec_gaps_with_gaps()** (2 connections) — `tests/test_codebase_map_service.py`
- **.test_load_from_cache()** (2 connections) — `tests/test_codebase_map_service.py`
- **.test_parse_invalid_file()** (2 connections) — `tests/test_codebase_map_service.py`
- *... and 15 more nodes in this community*

## Relationships

- [WorkerRole](WorkerRole.md) (6 shared connections)
- [TestTokenSavior](TestTokenSavior.md) (2 shared connections)
- [PassthroughStreamingProxy](PassthroughStreamingProxy.md) (1 shared connections)
- [conftest.py](conftest.py.md) (1 shared connections)
- [test_multi_provider_fabric.py](test_multi_provider_fabric.py.md) (1 shared connections)

## Source Files

- `src/merged_agentic_swarm/services/codebase_map_service.py`
- `tests/test_codebase_map_service.py`

## Audit Trail

- EXTRACTED: 99 (73%)
- INFERRED: 36 (27%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*