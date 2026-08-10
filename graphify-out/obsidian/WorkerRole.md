---
source_file: "src/merged_agentic_swarm/models/agent_models.py"
type: "code"
community: "WorkerRole"
location: "L11"
tags:
  - graphify/code
  - graphify/INFERRED
  - community/WorkerRole
---

# WorkerRole

## Connections
- [[dot-_get_available_worker_unlocked()]] - `references` [EXTRACTED]
- [[dot-_get_pool_id()]] - `references` [EXTRACTED]
- [[dot-_initialize_worker_pool()]] - `calls` [EXTRACTED]
- [[dot-_load_cold_agents_from_registry()]] - `calls` [EXTRACTED]
- [[dot-_run_opencode_worker()]] - `references` [EXTRACTED]
- [[dot-execute_subtask_batch_parallel()]] - `references` [EXTRACTED]
- [[dot-execute_subtask_with_worker()]] - `references` [EXTRACTED]
- [[dot-get_available_worker()]] - `references` [EXTRACTED]
- [[dot-launch_batch()]] - `references` [EXTRACTED]
- [[ChainRegistry]] - `uses` [INFERRED]
- [[ConcurrencyRampController]] - `uses` [INFERRED]
- [[DurableAgentFactory]] - `uses` [INFERRED]
- [[DurableAgentRouter]] - `uses` [INFERRED]
- [[Enum]] - `inherits` [EXTRACTED]
- [[MultiLayeredAgenticOrchestrator]] - `uses` [INFERRED]
- [[OpenCodeSwarmManager]] - `uses` [INFERRED]
- [[TestAdapterConstruction]] - `uses` [INFERRED]
- [[TestAgentSpec]] - `uses` [INFERRED]
- [[TestAgentType]] - `uses` [INFERRED]
- [[TestChainRegistry]] - `uses` [INFERRED]
- [[TestConcurrencyRampController]] - `uses` [INFERRED]
- [[TestDurableAgentFactory]] - `uses` [INFERRED]
- [[TestDurableAgentRouter]] - `uses` [INFERRED]
- [[TestExecuteSubtaskDecisionLogic]] - `uses` [INFERRED]
- [[TestLaunchBatch]] - `uses` [INFERRED]
- [[TestLaunchWorker]] - `uses` [INFERRED]
- [[TestModeDetection]] - `uses` [INFERRED]
- [[TestOpenCodeSwarmManager]] - `uses` [INFERRED]
- [[TestShutdown]] - `uses` [INFERRED]
- [[TestSpawnChainEntry]] - `uses` [INFERRED]
- [[TestTargetRepoRoot]] - `uses` [INFERRED]
- [[TestWorkerPoolConfig]] - `uses` [INFERRED]
- [[TestWorkerPoolState]] - `uses` [INFERRED]
- [[TestWorkerRole]] - `uses` [INFERRED]
- [[WorkerRuntimeAdapter]] - `uses` [INFERRED]
- [[agent_factory_service.py]] - `imports` [EXTRACTED]
- [[agent_models.py]] - `contains` [EXTRACTED]
- [[agentic_orchestrator.py]] - `imports` [EXTRACTED]
- [[models__init__.py]] - `imports` [EXTRACTED]
- [[opencode_swarm_service.py]] - `imports` [EXTRACTED]
- [[str]] - `inherits` [EXTRACTED]
- [[worker_runtime_adapter.py]] - `imports` [EXTRACTED]

#graphify/code #graphify/INFERRED #community/WorkerRole