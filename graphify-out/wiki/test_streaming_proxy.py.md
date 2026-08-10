# test_streaming_proxy.py

> 31 nodes · cohesion 0.11

## Key Concepts

- **SubTask** (55 connections) — `src/merged_agentic_swarm/models/prd_models.py`
- **EpicTask** (32 connections) — `src/merged_agentic_swarm/models/prd_models.py`
- **test_agentic_orchestrator.py** (14 connections) — `tests/test_agentic_orchestrator.py`
- **TestSubTask** (12 connections) — `tests/test_prd_models.py`
- **TestEpicTask** (11 connections) — `tests/test_prd_models.py`
- **TestApplyWorkerOutputsPaths** (9 connections) — `tests/test_agentic_orchestrator.py`
- **TestApplyWorkerOutputs** (7 connections) — `tests/test_agentic_orchestrator.py`
- **TestInitializeSystemProxyFailure** (7 connections) — `tests/test_agentic_orchestrator.py`
- **TestPromoteColdPathAgentFileExists** (7 connections) — `tests/test_agentic_orchestrator.py`
- **TestPromoteColdPathChainEntryIds** (7 connections) — `tests/test_agentic_orchestrator.py`
- **_analysis()** (4 connections) — `tests/test_agentic_orchestrator.py`
- **_epic()** (4 connections) — `tests/test_agentic_orchestrator.py`
- **.test_existing_agent_file_skipped()** (3 connections) — `tests/test_agentic_orchestrator.py`
- **.test_chain_entry_ids_unique_within_batch()** (3 connections) — `tests/test_agentic_orchestrator.py`
- **.test_default_creation()** (3 connections) — `tests/test_prd_models.py`
- **.test_to_dict_serializes_nested()** (3 connections) — `tests/test_prd_models.py`
- **.test_with_subtasks()** (3 connections) — `tests/test_prd_models.py`
- **.get_tasks_for_wave()** (2 connections) — `src/merged_agentic_swarm/services/task_master_service.py`
- **.setup_method()** (2 connections) — `tests/test_agentic_orchestrator.py`
- **.setup_method()** (2 connections) — `tests/test_agentic_orchestrator.py`
- **.test_relative_path_resolves_and_write_failure_logged()** (2 connections) — `tests/test_agentic_orchestrator.py`
- **.test_proxy_start_failure_is_nonfatal()** (2 connections) — `tests/test_agentic_orchestrator.py`
- **.test_default_creation()** (2 connections) — `tests/test_prd_models.py`
- **.test_marked_completed_sets_timestamp()** (2 connections) — `tests/test_prd_models.py`
- **.test_to_dict_serializes_enum()** (2 connections) — `tests/test_prd_models.py`
- *... and 6 more nodes in this community*

## Relationships

- [WorkerRole](WorkerRole.md) (42 shared connections)
- [ProxyChainHealth](ProxyChainHealth.md) (19 shared connections)
- [TestTokenSavior](TestTokenSavior.md) (6 shared connections)
- [CodebaseMapService](CodebaseMapService.md) (6 shared connections)
- [TaskMasterService](TaskMasterService.md) (5 shared connections)
- [test_multi_provider_fabric.py](test_multi_provider_fabric.py.md) (5 shared connections)
- [generate_progress_report.sh](generate_progress_report.sh.md) (4 shared connections)
- [ChainRegistry](ChainRegistry.md) (3 shared connections)
- [SubTask](SubTask.md) (3 shared connections)
- [Post-Commit Auto-Rebuild Hook](Post-Commit_Auto-Rebuild_Hook.md) (2 shared connections)
- [AgentSpec](AgentSpec.md) (2 shared connections)
- [models/__init__.py](models-__init__.py.md) (2 shared connections)

## Source Files

- `src/merged_agentic_swarm/models/prd_models.py`
- `src/merged_agentic_swarm/services/task_master_service.py`
- `tests/test_agentic_orchestrator.py`
- `tests/test_prd_models.py`

## Audit Trail

- EXTRACTED: 116 (56%)
- INFERRED: 91 (44%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*