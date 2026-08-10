---
source_file: "src/merged_agentic_swarm/models/agent_models.py"
type: "code"
community: "AgentSpec"
location: "L30"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/AgentSpec
---

# AgentSpec

## Connections
- [[dot-_get_available_worker_unlocked()]] - `references` [EXTRACTED]
- [[dot-_initialize_worker_pool()]] - `calls` [EXTRACTED]
- [[dot-_launch_via_fabric()]] - `references` [EXTRACTED]
- [[dot-_launch_via_native()]] - `references` [EXTRACTED]
- [[dot-_launch_via_opencode()]] - `references` [EXTRACTED]
- [[dot-_load_cold_agents_from_registry()]] - `calls` [EXTRACTED]
- [[dot-_run_opencode_worker()]] - `calls` [EXTRACTED]
- [[dot-get_available_worker()]] - `references` [EXTRACTED]
- [[dot-is_expired()]] - `method` [EXTRACTED]
- [[dot-launch_batch()]] - `calls` [EXTRACTED]
- [[dot-launch_worker()]] - `references` [EXTRACTED]
- [[dot-spawn_from_learning()]] - `references` [EXTRACTED]
- [[dot-test_custom_fields()]] - `calls` [EXTRACTED]
- [[dot-test_default_creation()]] - `calls` [EXTRACTED]
- [[dot-test_durable_never_expires()]] - `calls` [EXTRACTED]
- [[dot-test_hot_expires_after_ttl()]] - `calls` [EXTRACTED]
- [[dot-test_hot_not_expired_within_ttl()]] - `calls` [EXTRACTED]
- [[dot-test_purge_expired_durable_untouched()]] - `calls` [EXTRACTED]
- [[dot-test_purge_expired_removes_hot_agents()]] - `calls` [EXTRACTED]
- [[dot-test_to_dict_serializes_enums()]] - `calls` [EXTRACTED]
- [[dot-to_dict()]] - `method` [EXTRACTED]
- [[ChainRegistry]] - `uses` [INFERRED]
- [[ConcurrencyRampController]] - `uses` [INFERRED]
- [[DurableAgentFactory]] - `uses` [INFERRED]
- [[DurableAgentRouter]] - `uses` [INFERRED]
- [[OpenCodeSwarmManager]] - `uses` [INFERRED]
- [[TestAdapterConstruction]] - `uses` [INFERRED]
- [[TestAgentSpec]] - `uses` [INFERRED]
- [[TestAgentType]] - `uses` [INFERRED]
- [[TestChainRegistry]] - `uses` [INFERRED]
- [[TestDurableAgentFactory]] - `uses` [INFERRED]
- [[TestLaunchBatch]] - `uses` [INFERRED]
- [[TestLaunchWorker]] - `uses` [INFERRED]
- [[TestModeDetection]] - `uses` [INFERRED]
- [[TestShutdown]] - `uses` [INFERRED]
- [[TestSpawnChainEntry]] - `uses` [INFERRED]
- [[TestWorkerPoolConfig]] - `uses` [INFERRED]
- [[TestWorkerPoolState]] - `uses` [INFERRED]
- [[TestWorkerRole]] - `uses` [INFERRED]
- [[WorkerRuntimeAdapter]] - `uses` [INFERRED]
- [[_spec()]] - `calls` [EXTRACTED]
- [[agent_factory_service.py]] - `imports` [EXTRACTED]
- [[agent_models.py]] - `contains` [EXTRACTED]
- [[models__init__.py]] - `imports` [EXTRACTED]
- [[opencode_swarm_service.py]] - `imports` [EXTRACTED]
- [[worker_runtime_adapter.py]] - `imports` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/AgentSpec