# swarm_run.py

> 22 nodes · cohesion 0.13

## Key Concepts

- **ChainRegistry** (22 connections) — `src/merged_agentic_swarm/services/agent_factory_service.py`
- **TestChainRegistry** (13 connections) — `tests/test_agent_factory_service.py`
- **.register_spawn()** (6 connections) — `src/merged_agentic_swarm/services/agent_factory_service.py`
- **test_agent_factory_service.py** (5 connections) — `tests/test_agent_factory_service.py`
- **.load_registry()** (4 connections) — `src/merged_agentic_swarm/services/agent_factory_service.py`
- **._next_entry_id()** (3 connections) — `src/merged_agentic_swarm/services/agent_factory_service.py`
- **isolated_agents_registry()** (3 connections) — `tests/test_agent_factory_service.py`
- **.test_register_spawn_entry_ids_unique_across_instances()** (3 connections) — `tests/test_agent_factory_service.py`
- **.test_register_spawn_entry_ids_unique_within_batch()** (3 connections) — `tests/test_agent_factory_service.py`
- **.__init__()** (2 connections) — `src/merged_agentic_swarm/services/agent_factory_service.py`
- **.save_registry()** (2 connections) — `src/merged_agentic_swarm/services/agent_factory_service.py`
- **.test_default_registry()** (2 connections) — `tests/test_agent_factory_service.py`
- **.test_load_corrupted_file()** (2 connections) — `tests/test_agent_factory_service.py`
- **.test_persists_across_loads()** (2 connections) — `tests/test_agent_factory_service.py`
- **.test_register_spawn()** (2 connections) — `tests/test_agent_factory_service.py`
- **.test_register_spawn_with_parent()** (2 connections) — `tests/test_agent_factory_service.py`
- **Generate a collision-proof spawn-chain entry_id (sequence + timestamp suffix).…** (1 connections) — `src/merged_agentic_swarm/services/agent_factory_service.py`
- **fixture** (1 connections)
- **Tests for services/agent_factory_service.py Coverage: ChainRegistry (load,…** (1 connections) — `tests/test_agent_factory_service.py`
- **Return a temp path for the durable cold-path agents.jsonl registry.** (1 connections) — `tests/test_agent_factory_service.py`
- **#18: entry_ids in one promotion batch must never collide.** (1 connections) — `tests/test_agent_factory_service.py`
- **#18: separate registry instances sharing a file must not reuse entry_ids.** (1 connections) — `tests/test_agent_factory_service.py`

## Relationships

- [AgentSpec](AgentSpec.md) (8 shared connections)
- [DurableAgentRouter](DurableAgentRouter.md) (5 shared connections)
- [WorkerPoolConfig](WorkerPoolConfig.md) (3 shared connections)
- [OpenCodeSwarmManager](OpenCodeSwarmManager.md) (2 shared connections)
- [PassthroughStreamingProxy](PassthroughStreamingProxy.md) (1 shared connections)
- [conftest.py](conftest.py.md) (1 shared connections)

## Source Files

- `src/merged_agentic_swarm/services/agent_factory_service.py`
- `tests/test_agent_factory_service.py`

## Audit Trail

- EXTRACTED: 56 (68%)
- INFERRED: 26 (32%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*