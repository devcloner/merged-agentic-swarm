# AgentSpec

> 35 nodes · cohesion 0.11

## Key Concepts

- **WorkerRole** (42 connections) — `src/merged_agentic_swarm/models/agent_models.py`
- **AgentType** (31 connections) — `src/merged_agentic_swarm/models/agent_models.py`
- **opencode_swarm_service.py** (23 connections) — `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- **agentic_orchestrator.py** (21 connections) — `src/merged_agentic_swarm/tools/agentic_orchestrator.py`
- **agent_models.py** (17 connections) — `src/merged_agentic_swarm/models/agent_models.py`
- **agent_factory_service.py** (15 connections) — `src/merged_agentic_swarm/services/agent_factory_service.py`
- **worker_runtime_adapter.py** (12 connections) — `src/merged_agentic_swarm/services/worker_runtime_adapter.py`
- **test_worker_runtime_adapter.py** (9 connections) — `tests/test_worker_runtime_adapter.py`
- **knowledge_cache.py** (8 connections) — `src/merged_agentic_swarm/tools/knowledge_cache.py`
- **TestModeDetection** (8 connections) — `tests/test_worker_runtime_adapter.py`
- **TestShutdown** (6 connections) — `tests/test_worker_runtime_adapter.py`
- **run_spotify_ai_workflow.py** (5 connections) — `scripts/agentic/run_spotify_ai_workflow.py`
- **detect_mode()** (5 connections) — `src/merged_agentic_swarm/services/worker_runtime_adapter.py`
- **_opencode_available()** (5 connections) — `src/merged_agentic_swarm/services/worker_runtime_adapter.py`
- **_resolve_opencode_bin()** (5 connections) — `src/merged_agentic_swarm/services/worker_runtime_adapter.py`
- **verify_learning_loop.py** (4 connections) — `scripts/agentic/verify_learning_loop.py`
- **Enum** (3 connections)
- **str** (2 connections)
- **.__init__()** (2 connections) — `src/merged_agentic_swarm/services/worker_runtime_adapter.py`
- **.test_detect_mode_returns_valid()** (2 connections) — `tests/test_worker_runtime_adapter.py`
- **.test_opencode_available_is_bool()** (2 connections) — `tests/test_worker_runtime_adapter.py`
- **.test_resolve_opencode_bin_is_str_or_none()** (2 connections) — `tests/test_worker_runtime_adapter.py`
- **Run the agentic swarm orchestrator against spotify-ai project. Produces an…** (1 connections) — `scripts/agentic/run_spotify_ai_workflow.py`
- **run_git()** (1 connections) — `scripts/agentic/run_spotify_ai_workflow.py`
- **Phase 5: Durable Learning Loop End-to-End Verification** (1 connections) — `scripts/agentic/verify_learning_loop.py`
- *... and 10 more nodes in this community*

## Relationships

- [OpenCodeSwarmManager](OpenCodeSwarmManager.md) (29 shared connections)
- [WorkerPoolConfig](WorkerPoolConfig.md) (17 shared connections)
- [WorkerRole](WorkerRole.md) (10 shared connections)
- [SubTask](SubTask.md) (9 shared connections)
- [DurableAgentRouter](DurableAgentRouter.md) (9 shared connections)
- [swarm_run.py](swarm_run.py.md) (8 shared connections)
- [CodebaseMapService](CodebaseMapService.md) (8 shared connections)
- [ChainRegistry](ChainRegistry.md) (6 shared connections)
- [ProxyChainHealth](ProxyChainHealth.md) (4 shared connections)
- [PassthroughStreamingProxy](PassthroughStreamingProxy.md) (4 shared connections)
- [test_streaming_proxy.py](test_streaming_proxy.py.md) (2 shared connections)
- [services/__init__.py](services-__init__.py.md) (2 shared connections)

## Source Files

- `scripts/agentic/run_spotify_ai_workflow.py`
- `scripts/agentic/verify_learning_loop.py`
- `src/merged_agentic_swarm/models/agent_models.py`
- `src/merged_agentic_swarm/services/agent_factory_service.py`
- `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- `src/merged_agentic_swarm/services/worker_runtime_adapter.py`
- `src/merged_agentic_swarm/tools/agentic_orchestrator.py`
- `src/merged_agentic_swarm/tools/knowledge_cache.py`
- `tests/test_worker_runtime_adapter.py`

## Audit Trail

- EXTRACTED: 189 (78%)
- INFERRED: 53 (22%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*