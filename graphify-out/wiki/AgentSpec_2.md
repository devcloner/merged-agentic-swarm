# AgentSpec

> God node · 46 connections · `src/merged_agentic_swarm/models/agent_models.py`

**Community:** [OpenCodeSwarmManager](OpenCodeSwarmManager.md)

## Connections by Relation

### calls
- ._run_opencode_worker() `EXTRACTED`
- _spec() `EXTRACTED`
- ._load_cold_agents_from_registry() `EXTRACTED`
- ._initialize_worker_pool() `EXTRACTED`
- .launch_batch() `EXTRACTED`
- .test_purge_expired_durable_untouched() `EXTRACTED`
- .test_purge_expired_removes_hot_agents() `EXTRACTED`
- .test_custom_fields() `EXTRACTED`
- .test_default_creation() `EXTRACTED`
- .test_durable_never_expires() `EXTRACTED`
- .test_hot_expires_after_ttl() `EXTRACTED`
- .test_hot_not_expired_within_ttl() `EXTRACTED`
- .test_to_dict_serializes_enums() `EXTRACTED`

### contains
- agent_models.py `EXTRACTED`

### imports
- [models/__init__.py](models-__init__.py.md) `EXTRACTED`
- opencode_swarm_service.py `EXTRACTED`
- agent_factory_service.py `EXTRACTED`
- worker_runtime_adapter.py `EXTRACTED`

### method
- .is_expired() `EXTRACTED`
- .to_dict() `EXTRACTED`

### references
- .spawn_from_learning() `EXTRACTED`
- ._launch_via_opencode() `EXTRACTED`
- .launch_worker() `EXTRACTED`
- .get_available_worker() `EXTRACTED`
- ._launch_via_native() `EXTRACTED`
- ._get_available_worker_unlocked() `EXTRACTED`
- ._launch_via_fabric() `EXTRACTED`

### uses
- [OpenCodeSwarmManager](OpenCodeSwarmManager.md) `INFERRED`
- WorkerRuntimeAdapter `INFERRED`
- [DurableAgentFactory](DurableAgentFactory.md) `INFERRED`
- [DurableAgentRouter](DurableAgentRouter.md) `INFERRED`
- [ChainRegistry](ChainRegistry.md) `INFERRED`
- TestDurableAgentFactory `INFERRED`
- [ConcurrencyRampController](ConcurrencyRampController.md) `INFERRED`
- TestChainRegistry `INFERRED`
- TestAgentSpec `INFERRED`
- TestWorkerPoolState `INFERRED`
- TestAdapterConstruction `INFERRED`
- TestLaunchWorker `INFERRED`
- TestSpawnChainEntry `INFERRED`
- TestWorkerPoolConfig `INFERRED`
- TestAgentType `INFERRED`
- TestWorkerRole `INFERRED`
- TestModeDetection `INFERRED`
- TestLaunchBatch `INFERRED`
- TestShutdown `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*