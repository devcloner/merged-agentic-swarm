# DurableAgentRouter

> 39 nodes · cohesion 0.08

## Key Concepts

- **DurableAgentFactory** (31 connections) — `src/merged_agentic_swarm/services/agent_factory_service.py`
- **TestDurableAgentFactory** (20 connections) — `tests/test_agent_factory_service.py`
- **.spawn_from_learning()** (7 connections) — `src/merged_agentic_swarm/services/agent_factory_service.py`
- **._agents_registry_path()** (6 connections) — `src/merged_agentic_swarm/services/agent_factory_service.py`
- **._load_cold_agents_from_registry()** (6 connections) — `src/merged_agentic_swarm/services/agent_factory_service.py`
- **agents_registry_path()** (5 connections) — `src/merged_agentic_swarm/services/agent_factory_service.py`
- **._persist_cold_agent()** (5 connections) — `src/merged_agentic_swarm/services/agent_factory_service.py`
- **._write_agent_spec_file()** (5 connections) — `src/merged_agentic_swarm/services/agent_factory_service.py`
- **.sync_agent_specs()** (4 connections) — `src/merged_agentic_swarm/services/agent_factory_service.py`
- **.__init__()** (3 connections) — `src/merged_agentic_swarm/services/agent_factory_service.py`
- **.test_cold_agents_loaded_from_registry_on_restart()** (3 connections) — `tests/test_agent_factory_service.py`
- **.test_cold_persist_is_idempotent()** (3 connections) — `tests/test_agent_factory_service.py`
- **.test_default_factory_resolves_shared_registry_path()** (3 connections) — `tests/test_agent_factory_service.py`
- **.test_purge_expired_durable_untouched()** (3 connections) — `tests/test_agent_factory_service.py`
- **.test_purge_expired_removes_hot_agents()** (3 connections) — `tests/test_agent_factory_service.py`
- **.test_spawn_cold_persists_to_agents_registry()** (3 connections) — `tests/test_agent_factory_service.py`
- **.test_spawn_hot_not_persisted_to_agents_registry()** (3 connections) — `tests/test_agent_factory_service.py`
- **.test_sync_agent_specs_missing_registry()** (3 connections) — `tests/test_agent_factory_service.py`
- **.purge_expired()** (2 connections) — `src/merged_agentic_swarm/services/agent_factory_service.py`
- **Any** (2 connections)
- **Resolve the durable cold-path agents registry (agents.jsonl). Prefers an…** (2 connections) — `src/merged_agentic_swarm/services/agent_factory_service.py`
- **.test_spawn_from_learning_cold()** (2 connections) — `tests/test_agent_factory_service.py`
- **.test_spawn_from_learning_hot()** (2 connections) — `tests/test_agent_factory_service.py`
- **.test_spawn_from_learning_registers_in_chain()** (2 connections) — `tests/test_agent_factory_service.py`
- **.test_spawn_from_learning_with_force_type()** (2 connections) — `tests/test_agent_factory_service.py`
- *... and 14 more nodes in this community*

## Relationships

- [AgentSpec](AgentSpec.md) (9 shared connections)
- [OpenCodeSwarmManager](OpenCodeSwarmManager.md) (6 shared connections)
- [swarm_run.py](swarm_run.py.md) (5 shared connections)
- [CodebaseMapService](CodebaseMapService.md) (1 shared connections)
- [WorkerPoolConfig](WorkerPoolConfig.md) (1 shared connections)
- [PassthroughStreamingProxy](PassthroughStreamingProxy.md) (1 shared connections)
- [conftest.py](conftest.py.md) (1 shared connections)

## Source Files

- `src/merged_agentic_swarm/services/agent_factory_service.py`
- `tests/test_agent_factory_service.py`

## Audit Trail

- EXTRACTED: 106 (73%)
- INFERRED: 40 (27%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*