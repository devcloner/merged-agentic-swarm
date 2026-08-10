---
source_file: "src/merged_agentic_swarm/services/agent_factory_service.py"
type: "code"
community: "DurableAgentFactory"
location: "L111"
tags:
  - graphify/code
  - graphify/INFERRED
  - community/DurableAgentFactory
---

# DurableAgentFactory

## Connections
- [[dot-__init__()_9]] - `method` [EXTRACTED]
- [[dot-_agents_registry_path()]] - `method` [EXTRACTED]
- [[dot-_load_cold_agents_from_registry()]] - `method` [EXTRACTED]
- [[dot-_persist_cold_agent()]] - `method` [EXTRACTED]
- [[dot-_write_agent_spec_file()]] - `method` [EXTRACTED]
- [[dot-purge_expired()]] - `method` [EXTRACTED]
- [[dot-spawn_from_learning()]] - `method` [EXTRACTED]
- [[dot-sync_agent_specs()]] - `method` [EXTRACTED]
- [[dot-test_cold_agents_loaded_from_registry_on_restart()]] - `calls` [INFERRED]
- [[dot-test_cold_persist_is_idempotent()]] - `calls` [INFERRED]
- [[dot-test_default_factory_resolves_shared_registry_path()]] - `calls` [INFERRED]
- [[dot-test_purge_expired_durable_untouched()]] - `calls` [INFERRED]
- [[dot-test_purge_expired_removes_hot_agents()]] - `calls` [INFERRED]
- [[dot-test_spawn_cold_persists_to_agents_registry()]] - `calls` [INFERRED]
- [[dot-test_spawn_from_learning_cold()]] - `calls` [INFERRED]
- [[dot-test_spawn_from_learning_hot()]] - `calls` [INFERRED]
- [[dot-test_spawn_from_learning_registers_in_chain()]] - `calls` [INFERRED]
- [[dot-test_spawn_from_learning_with_force_type()]] - `calls` [INFERRED]
- [[dot-test_spawn_hot_not_persisted_to_agents_registry()]] - `calls` [INFERRED]
- [[dot-test_sync_agent_specs_missing_registry()]] - `calls` [INFERRED]
- [[dot-test_write_agent_spec_file_creates_md()]] - `calls` [INFERRED]
- [[dot-test_write_agent_spec_file_skips_existing()]] - `calls` [INFERRED]
- [[AgentSpec]] - `uses` [INFERRED]
- [[AgentType]] - `uses` [INFERRED]
- [[SpawnChainEntry]] - `uses` [INFERRED]
- [[TestChainRegistry]] - `uses` [INFERRED]
- [[TestDurableAgentFactory]] - `uses` [INFERRED]
- [[WorkerRole]] - `uses` [INFERRED]
- [[agent_factory_service.py]] - `contains` [EXTRACTED]
- [[isolated_agent_factory()]] - `calls` [INFERRED]
- [[services__init__.py]] - `imports` [EXTRACTED]

#graphify/code #graphify/INFERRED #community/DurableAgentFactory