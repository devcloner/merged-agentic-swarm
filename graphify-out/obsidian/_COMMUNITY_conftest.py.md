---
type: community
cohesion: 0.09
members: 31
---

# conftest.py

**Cohesion:** 0.09 - loosely connected
**Members:** 31 nodes

## Members
- [[Create a minimal env.txt with one key for testing.]] - rationale - tests/conftest.py
- [[Create a minimal ownership-map.json and return its path.]] - rationale - tests/conftest.py
- [[Factory fixture that returns a function to create EpicTask instances.]] - rationale - tests/conftest.py
- [[Provide a temporary directory that is cleaned up after the test.]] - rationale - tests/conftest.py
- [[Return a ChainRegistry that writes to a temp file.]] - rationale - tests/conftest.py
- [[Return a CodebaseMapService pointed at an isolated repo root.]] - rationale - tests/conftest.py
- [[Return a DurableAgentFactory with an isolated chain registry.]] - rationale - tests/conftest.py
- [[Return a KeyPoolManager pointed at a temp env file.]] - rationale - tests/conftest.py
- [[Return a KnowledgeCache that writes to a temp file.]] - rationale - tests/conftest.py
- [[Return a MultiProviderFabric backed by the isolated key pool.]] - rationale - tests/conftest.py
- [[Return a ProgressLedgerService that writes to a temp file.]] - rationale - tests/conftest.py
- [[Return a TaskMasterService that writes to a temp file.]] - rationale - tests/conftest.py
- [[Return a fresh OpenCodeSwarmManager.]] - rationale - tests/conftest.py
- [[Return a fresh WaveGateController (no persistent state to worry about).]] - rationale - tests/conftest.py
- [[conftest.py]] - code - tests/conftest.py
- [[fixture]] - code
- [[isolated_agent_factory()]] - code - tests/conftest.py
- [[isolated_chain_registry()]] - code - tests/conftest.py
- [[isolated_codebase_mapper()]] - code - tests/conftest.py
- [[isolated_fabric()]] - code - tests/conftest.py
- [[isolated_key_pool()]] - code - tests/conftest.py
- [[isolated_knowledge_cache()]] - code - tests/conftest.py
- [[isolated_progress_ledger()]] - code - tests/conftest.py
- [[isolated_swarm_manager()]] - code - tests/conftest.py
- [[isolated_task_master()]] - code - tests/conftest.py
- [[isolated_wave_controller()]] - code - tests/conftest.py
- [[make_epic()]] - code - tests/conftest.py
- [[owner_map_file()]] - code - tests/conftest.py
- [[pytest fixtures and shared test utilities for Merged Agentic Swarm.]] - rationale - tests/conftest.py
- [[temp_dir()]] - code - tests/conftest.py
- [[temp_env_file()]] - code - tests/conftest.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/conftestpy
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_OpenCodeSwarmManager]]
- 1 edge to [[_COMMUNITY_KeyPoolManager]]
- 1 edge to [[_COMMUNITY_MultiProviderFabric]]
- 1 edge to [[_COMMUNITY_ChainRegistry]]
- 1 edge to [[_COMMUNITY_DurableAgentFactory]]
- 1 edge to [[_COMMUNITY_CodebaseMapService]]
- 1 edge to [[_COMMUNITY_ProgressLedgerService]]
- 1 edge to [[_COMMUNITY_TaskMasterService]]
- 1 edge to [[_COMMUNITY_WaveGateController]]
- 1 edge to [[_COMMUNITY_KnowledgeCache]]

## Top bridge nodes
- [[conftest.py]] - degree 16, connects to 1 community
- [[fixture]] - degree 15, connects to 1 community
- [[isolated_agent_factory()]] - degree 4, connects to 1 community
- [[isolated_chain_registry()]] - degree 4, connects to 1 community
- [[isolated_codebase_mapper()]] - degree 4, connects to 1 community