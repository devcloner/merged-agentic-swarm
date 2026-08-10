---
type: community
cohesion: 0.08
members: 46
---

# AgentSpec

**Cohesion:** 0.08 - loosely connected
**Members:** 46 nodes

## Members
- [[dot-_launch_via_fabric()]] - code - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[dot-_launch_via_native()]] - code - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[dot-_launch_via_opencode()]] - code - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[dot-_next_port()]] - code - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[dot-is_expired()]] - code - src/merged_agentic_swarm/models/agent_models.py
- [[dot-launch_batch()]] - code - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[dot-launch_worker()]] - code - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[dot-shutdown()]] - code - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[dot-test_batch_returns_result_per_task()]] - code - tests/test_worker_runtime_adapter.py
- [[dot-test_batch_survives_worker_exception()]] - code - tests/test_worker_runtime_adapter.py
- [[dot-test_custom_fields()]] - code - tests/test_agent_models.py
- [[dot-test_default_creation()]] - code - tests/test_agent_models.py
- [[dot-test_direct_fabric_launch_delegates()]] - code - tests/test_worker_runtime_adapter.py
- [[dot-test_durable_never_expires()]] - code - tests/test_agent_models.py
- [[dot-test_explicit_direct_fabric_mode()]] - code - tests/test_worker_runtime_adapter.py
- [[dot-test_explicit_native_mode()]] - code - tests/test_worker_runtime_adapter.py
- [[dot-test_hot_expires_after_ttl()]] - code - tests/test_agent_models.py
- [[dot-test_hot_not_expired_within_ttl()]] - code - tests/test_agent_models.py
- [[dot-test_invalid_mode_raises()]] - code - tests/test_worker_runtime_adapter.py
- [[dot-test_native_launch_completed()]] - code - tests/test_worker_runtime_adapter.py
- [[dot-test_native_launch_failed_on_exception()]] - code - tests/test_worker_runtime_adapter.py
- [[dot-test_native_launch_simulated_is_hard_failure()]] - code - tests/test_worker_runtime_adapter.py
- [[dot-test_next_port_increments()]] - code - tests/test_worker_runtime_adapter.py
- [[dot-test_opencode_falls_back_to_native_when_no_bin()]] - code - tests/test_worker_runtime_adapter.py
- [[dot-test_shutdown_clears_processes()]] - code - tests/test_worker_runtime_adapter.py
- [[dot-test_singleton_caches_per_mode()]] - code - tests/test_worker_runtime_adapter.py
- [[dot-test_to_dict_serializes_enums()]] - code - tests/test_agent_models.py
- [[A simulated fabric response must fail, never complete or 'partial'. This is the…]] - rationale - tests/test_worker_runtime_adapter.py
- [[AgentSpec]] - code - src/merged_agentic_swarm/models/agent_models.py
- [[Any_21]] - code
- [[Launch a batch of tasks for a given role, up to max_concurrency.]] - rationale - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[Launch a single worker with a task and return a result dict. Result keys…]] - rationale - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[Launch a task via direct fabric dispatch. Identical to native_subagent in…]] - rationale - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[Launch a task via native subagent fallback. Calls the multi-provider fabric…]] - rationale - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[Launch a task via the OpenCode CLI. Spawns `opencode serve --port N` as a…]] - rationale - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[Return (or create) the global WorkerRuntimeAdapter singleton.]] - rationale - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[Return True if this agent has a TTL and has exceeded it.]] - rationale - src/merged_agentic_swarm/models/agent_models.py
- [[Terminate all opencode worker processes.]] - rationale - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[TestAdapterConstruction]] - code - tests/test_worker_runtime_adapter.py
- [[TestAgentSpec]] - code - tests/test_agent_models.py
- [[TestLaunchBatch]] - code - tests/test_worker_runtime_adapter.py
- [[TestLaunchWorker]] - code - tests/test_worker_runtime_adapter.py
- [[Unified adapter that launches workers in the selected execution mode. Modes…]] - rationale - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[WorkerRuntimeAdapter]] - code - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[_spec()]] - code - tests/test_worker_runtime_adapter.py
- [[get_runtime_adapter()]] - code - src/merged_agentic_swarm/services/worker_runtime_adapter.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/AgentSpec
SORT file.name ASC
```

## Connections to other communities
- 37 edges to [[_COMMUNITY_WorkerRole]]
- 6 edges to [[_COMMUNITY_DurableAgentFactory]]
- 4 edges to [[_COMMUNITY_OpenCodeSwarmManager]]
- 3 edges to [[_COMMUNITY_WorkerPoolState]]
- 3 edges to [[_COMMUNITY_DurableAgentRouter]]
- 2 edges to [[_COMMUNITY_ChainRegistry]]
- 1 edge to [[_COMMUNITY_PRDAnalysisResult]]
- 1 edge to [[_COMMUNITY_ConcurrencyRampController]]

## Top bridge nodes
- [[AgentSpec]] - degree 46, connects to 8 communities
- [[TestAgentSpec]] - degree 13, connects to 2 communities
- [[get_runtime_adapter()]] - degree 6, connects to 2 communities
- [[WorkerRuntimeAdapter]] - degree 32, connects to 1 community
- [[TestAdapterConstruction]] - degree 10, connects to 1 community