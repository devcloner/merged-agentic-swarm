# conftest.py

> 31 nodes · cohesion 0.09

## Key Concepts

- **conftest.py** (16 connections) — `tests/conftest.py`
- **fixture** (15 connections)
- **isolated_agent_factory()** (4 connections) — `tests/conftest.py`
- **isolated_chain_registry()** (4 connections) — `tests/conftest.py`
- **isolated_codebase_mapper()** (4 connections) — `tests/conftest.py`
- **isolated_fabric()** (4 connections) — `tests/conftest.py`
- **isolated_key_pool()** (4 connections) — `tests/conftest.py`
- **isolated_knowledge_cache()** (4 connections) — `tests/conftest.py`
- **isolated_progress_ledger()** (4 connections) — `tests/conftest.py`
- **isolated_swarm_manager()** (4 connections) — `tests/conftest.py`
- **isolated_task_master()** (4 connections) — `tests/conftest.py`
- **isolated_wave_controller()** (4 connections) — `tests/conftest.py`
- **make_epic()** (3 connections) — `tests/conftest.py`
- **owner_map_file()** (3 connections) — `tests/conftest.py`
- **temp_dir()** (3 connections) — `tests/conftest.py`
- **temp_env_file()** (3 connections) — `tests/conftest.py`
- **Factory fixture that returns a function to create SubTask instances.** (2 connections) — `tests/conftest.py`
- **pytest fixtures and shared test utilities for Merged Agentic Swarm.** (1 connections) — `tests/conftest.py`
- **Return a fresh WaveGateController (no persistent state to worry about).** (1 connections) — `tests/conftest.py`
- **Return a fresh OpenCodeSwarmManager.** (1 connections) — `tests/conftest.py`
- **Return a CodebaseMapService pointed at an isolated repo root.** (1 connections) — `tests/conftest.py`
- **Create a minimal ownership-map.json and return its path.** (1 connections) — `tests/conftest.py`
- **Provide a temporary directory that is cleaned up after the test.** (1 connections) — `tests/conftest.py`
- **Create a minimal env.txt with one key for testing.** (1 connections) — `tests/conftest.py`
- **Return a KeyPoolManager pointed at a temp env file.** (1 connections) — `tests/conftest.py`
- *... and 6 more nodes in this community*

## Relationships

- [SubTask](SubTask.md) (4 shared connections)
- [DurableAgentRouter](DurableAgentRouter.md) (1 shared connections)
- [swarm_run.py](swarm_run.py.md) (1 shared connections)
- [_router_with_keys](_router_with_keys.md) (1 shared connections)
- [MultiProviderFabric](MultiProviderFabric.md) (1 shared connections)
- [KeyPoolManager](KeyPoolManager.md) (1 shared connections)
- [KnowledgeCache](KnowledgeCache.md) (1 shared connections)
- [TestRunFullAgenticWorkflow](TestRunFullAgenticWorkflow.md) (1 shared connections)
- [TaskMasterService](TaskMasterService.md) (1 shared connections)
- [models/__init__.py](models-__init__.py.md) (1 shared connections)

## Source Files

- `tests/conftest.py`

## Audit Trail

- EXTRACTED: 89 (90%)
- INFERRED: 10 (10%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*