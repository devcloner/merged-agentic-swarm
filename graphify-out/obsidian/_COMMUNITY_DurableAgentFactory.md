---
type: community
cohesion: 0.08
members: 39
---

# DurableAgentFactory

**Cohesion:** 0.08 - loosely connected
**Members:** 39 nodes

## Members
- [[17 COLD_DURABLE spawns must be written to the durable agents.jsonl registry.]] - rationale - tests/test_agent_factory_service.py
- [[17 HOT micro-specialists are transient and must NOT hit agents.jsonl.]] - rationale - tests/test_agent_factory_service.py
- [[17 a fresh factory discovers persisted COLD_DURABLE agents (restart survival).]] - rationale - tests/test_agent_factory_service.py
- [[17 persisting an already-registered agent id must not duplicate the line.]] - rationale - tests/test_agent_factory_service.py
- [[31 the factory's default registry path goes through the shared resolver.]] - rationale - tests/test_agent_factory_service.py
- [[dot-__init__()_9]] - code - src/merged_agentic_swarm/services/agent_factory_service.py
- [[dot-_agents_registry_path()]] - code - src/merged_agentic_swarm/services/agent_factory_service.py
- [[dot-_load_cold_agents_from_registry()]] - code - src/merged_agentic_swarm/services/agent_factory_service.py
- [[dot-_persist_cold_agent()]] - code - src/merged_agentic_swarm/services/agent_factory_service.py
- [[dot-_write_agent_spec_file()]] - code - src/merged_agentic_swarm/services/agent_factory_service.py
- [[dot-purge_expired()]] - code - src/merged_agentic_swarm/services/agent_factory_service.py
- [[dot-spawn_from_learning()]] - code - src/merged_agentic_swarm/services/agent_factory_service.py
- [[dot-sync_agent_specs()]] - code - src/merged_agentic_swarm/services/agent_factory_service.py
- [[dot-test_cold_agents_loaded_from_registry_on_restart()]] - code - tests/test_agent_factory_service.py
- [[dot-test_cold_persist_is_idempotent()]] - code - tests/test_agent_factory_service.py
- [[dot-test_default_factory_resolves_shared_registry_path()]] - code - tests/test_agent_factory_service.py
- [[dot-test_purge_expired_durable_untouched()]] - code - tests/test_agent_factory_service.py
- [[dot-test_purge_expired_removes_hot_agents()]] - code - tests/test_agent_factory_service.py
- [[dot-test_spawn_cold_persists_to_agents_registry()]] - code - tests/test_agent_factory_service.py
- [[dot-test_spawn_from_learning_cold()]] - code - tests/test_agent_factory_service.py
- [[dot-test_spawn_from_learning_hot()]] - code - tests/test_agent_factory_service.py
- [[dot-test_spawn_from_learning_registers_in_chain()]] - code - tests/test_agent_factory_service.py
- [[dot-test_spawn_from_learning_with_force_type()]] - code - tests/test_agent_factory_service.py
- [[dot-test_spawn_hot_not_persisted_to_agents_registry()]] - code - tests/test_agent_factory_service.py
- [[dot-test_sync_agent_specs_missing_registry()]] - code - tests/test_agent_factory_service.py
- [[dot-test_write_agent_spec_file_creates_md()]] - code - tests/test_agent_factory_service.py
- [[dot-test_write_agent_spec_file_skips_existing()]] - code - tests/test_agent_factory_service.py
- [[Any_11]] - code
- [[Append a COLD_DURABLE agent record to the durable agents.jsonl registry.…]] - rationale - src/merged_agentic_swarm/services/agent_factory_service.py
- [[DurableAgentFactory]] - code - src/merged_agentic_swarm/services/agent_factory_service.py
- [[Evaluates validated learning from Knowledge-Box and spawns HOT or COLD agent.]] - rationale - src/merged_agentic_swarm/services/agent_factory_service.py
- [[Load durable agents from the cold-path agents.jsonl registry. Called once at…]] - rationale - src/merged_agentic_swarm/services/agent_factory_service.py
- [[Read agents.jsonl and write spec files for every entry. Returns the count of…]] - rationale - src/merged_agentic_swarm/services/agent_factory_service.py
- [[Remove and return count of expired HOT micro-specialists (FIX-09).]] - rationale - src/merged_agentic_swarm/services/agent_factory_service.py
- [[Resolve the durable cold-path agents registry (agents.jsonl). Prefers an…]] - rationale - src/merged_agentic_swarm/services/agent_factory_service.py
- [[TestDurableAgentFactory]] - code - tests/test_agent_factory_service.py
- [[Write an agent spec .md file from a JSONL entry. Returns the file path, or None…]] - rationale - src/merged_agentic_swarm/services/agent_factory_service.py
- [[agents_registry_path()]] - code - src/merged_agentic_swarm/services/agent_factory_service.py
- [[sync_agent_specs should handle missing agents.jsonl gracefully.]] - rationale - tests/test_agent_factory_service.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/DurableAgentFactory
SORT file.name ASC
```

## Connections to other communities
- 10 edges to [[_COMMUNITY_WorkerRole]]
- 6 edges to [[_COMMUNITY_AgentSpec]]
- 5 edges to [[_COMMUNITY_ChainRegistry]]
- 1 edge to [[_COMMUNITY_services__init__.py]]
- 1 edge to [[_COMMUNITY_DurableAgentRouter]]
- 1 edge to [[_COMMUNITY_conftest.py]]

## Top bridge nodes
- [[DurableAgentFactory]] - degree 31, connects to 5 communities
- [[TestDurableAgentFactory]] - degree 20, connects to 3 communities
- [[dot-spawn_from_learning()]] - degree 7, connects to 3 communities
- [[dot-_load_cold_agents_from_registry()]] - degree 6, connects to 2 communities
- [[agents_registry_path()]] - degree 5, connects to 2 communities