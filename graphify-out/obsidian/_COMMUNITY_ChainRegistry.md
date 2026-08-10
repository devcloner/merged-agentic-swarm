---
type: community
cohesion: 0.13
members: 22
---

# ChainRegistry

**Cohesion:** 0.13 - loosely connected
**Members:** 22 nodes

## Members
- [[18 entry_ids in one promotion batch must never collide.]] - rationale - tests/test_agent_factory_service.py
- [[18 separate registry instances sharing a file must not reuse entry_ids.]] - rationale - tests/test_agent_factory_service.py
- [[dot-__init__()_8]] - code - src/merged_agentic_swarm/services/agent_factory_service.py
- [[dot-_next_entry_id()]] - code - src/merged_agentic_swarm/services/agent_factory_service.py
- [[dot-load_registry()]] - code - src/merged_agentic_swarm/services/agent_factory_service.py
- [[dot-register_spawn()]] - code - src/merged_agentic_swarm/services/agent_factory_service.py
- [[dot-save_registry()]] - code - src/merged_agentic_swarm/services/agent_factory_service.py
- [[dot-test_default_registry()]] - code - tests/test_agent_factory_service.py
- [[dot-test_load_corrupted_file()]] - code - tests/test_agent_factory_service.py
- [[dot-test_persists_across_loads()]] - code - tests/test_agent_factory_service.py
- [[dot-test_register_spawn()]] - code - tests/test_agent_factory_service.py
- [[dot-test_register_spawn_entry_ids_unique_across_instances()]] - code - tests/test_agent_factory_service.py
- [[dot-test_register_spawn_entry_ids_unique_within_batch()]] - code - tests/test_agent_factory_service.py
- [[dot-test_register_spawn_with_parent()]] - code - tests/test_agent_factory_service.py
- [[ChainRegistry]] - code - src/merged_agentic_swarm/services/agent_factory_service.py
- [[Generate a collision-proof spawn-chain entry_id (sequence + timestamp suffix).…]] - rationale - src/merged_agentic_swarm/services/agent_factory_service.py
- [[Return a temp path for the durable cold-path agents.jsonl registry.]] - rationale - tests/test_agent_factory_service.py
- [[TestChainRegistry]] - code - tests/test_agent_factory_service.py
- [[Tests for servicesagent_factory_service.py Coverage ChainRegistry (load,…]] - rationale - tests/test_agent_factory_service.py
- [[fixture_1]] - code
- [[isolated_agents_registry()]] - code - tests/test_agent_factory_service.py
- [[test_agent_factory_service.py]] - code - tests/test_agent_factory_service.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ChainRegistry
SORT file.name ASC
```

## Connections to other communities
- 8 edges to [[_COMMUNITY_WorkerRole]]
- 5 edges to [[_COMMUNITY_DurableAgentFactory]]
- 3 edges to [[_COMMUNITY_WorkerPoolConfig]]
- 2 edges to [[_COMMUNITY_AgentSpec]]
- 1 edge to [[_COMMUNITY_services__init__.py]]
- 1 edge to [[_COMMUNITY_conftest.py]]

## Top bridge nodes
- [[ChainRegistry]] - degree 22, connects to 6 communities
- [[TestChainRegistry]] - degree 13, connects to 3 communities
- [[dot-register_spawn()]] - degree 6, connects to 3 communities
- [[test_agent_factory_service.py]] - degree 5, connects to 2 communities
- [[dot-load_registry()]] - degree 4, connects to 2 communities