---
type: community
cohesion: 0.10
members: 37
---

# WorkerRole

**Cohesion:** 0.10 - loosely connected
**Members:** 37 nodes

## Members
- [[dot-__init__()_21]] - code - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[dot-test_detect_mode_returns_valid()]] - code - tests/test_worker_runtime_adapter.py
- [[dot-test_opencode_available_is_bool()]] - code - tests/test_worker_runtime_adapter.py
- [[dot-test_resolve_opencode_bin_is_str_or_none()]] - code - tests/test_worker_runtime_adapter.py
- [[Agent, Worker Pool, and Spawn Chain Data Models]] - rationale - src/merged_agentic_swarm/models/agent_models.py
- [[AgentType]] - code - src/merged_agentic_swarm/models/agent_models.py
- [[Agentic Multi-Layered Workflow Master Orchestrator Integrates Task Master AI,…]] - rationale - src/merged_agentic_swarm/tools/agentic_orchestrator.py
- [[Auto-detect the best available runtime mode. Priority opencode …]] - rationale - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[Durable Agent Factory & Knowledge-Box - Spawn Chain Registry Turns validated…]] - rationale - src/merged_agentic_swarm/services/agent_factory_service.py
- [[Enum]] - code
- [[Knowledge Cache Service Persistent cache for validated learnings, obstacle…]] - rationale - src/merged_agentic_swarm/tools/knowledge_cache.py
- [[OpenCode Swarm Pack Coordinator (40-Worker Pool Manager) Allocates worker pools…]] - rationale - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[Phase 5 Durable Learning Loop End-to-End Verification]] - rationale - scripts/agentic/verify_learning_loop.py
- [[Resolve the durable cold-path agents registry (agents.jsonl). Prefers an…]] - rationale - src/merged_agentic_swarm/services/agent_factory_service.py
- [[Resolve the opencode binary from PATH or known locations.]] - rationale - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[Return True if the OpenCode binary exists and responds to --help.]] - rationale - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[Run the agentic swarm orchestrator against spotify-ai project. Produces an…]] - rationale - scripts/agentic/run_spotify_ai_workflow.py
- [[TestModeDetection]] - code - tests/test_worker_runtime_adapter.py
- [[TestShutdown]] - code - tests/test_worker_runtime_adapter.py
- [[Tests for servicesworker_runtime_adapter.py Real-behavior coverage of the…]] - rationale - tests/test_worker_runtime_adapter.py
- [[Worker Runtime Adapter — Unified launcher for OpenCode swarm workers. Supports…]] - rationale - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[WorkerRole]] - code - src/merged_agentic_swarm/models/agent_models.py
- [[_opencode_available()]] - code - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[_resolve_opencode_bin()]] - code - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[agent_factory_service.py]] - code - src/merged_agentic_swarm/services/agent_factory_service.py
- [[agent_models.py]] - code - src/merged_agentic_swarm/models/agent_models.py
- [[agentic_orchestrator.py]] - code - src/merged_agentic_swarm/tools/agentic_orchestrator.py
- [[agents_registry_path()]] - code - src/merged_agentic_swarm/services/agent_factory_service.py
- [[detect_mode()]] - code - src/merged_agentic_swarm/services/worker_runtime_adapter.py
- [[knowledge_cache.py]] - code - src/merged_agentic_swarm/tools/knowledge_cache.py
- [[opencode_swarm_service.py]] - code - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[run_git()]] - code - scripts/agentic/run_spotify_ai_workflow.py
- [[run_spotify_ai_workflow.py]] - code - scripts/agentic/run_spotify_ai_workflow.py
- [[str]] - code
- [[test_worker_runtime_adapter.py]] - code - tests/test_worker_runtime_adapter.py
- [[verify_learning_loop.py]] - code - scripts/agentic/verify_learning_loop.py
- [[worker_runtime_adapter.py]] - code - src/merged_agentic_swarm/services/worker_runtime_adapter.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/WorkerRole
SORT file.name ASC
```

## Connections to other communities
- 29 edges to [[_COMMUNITY_AgentSpec]]
- 18 edges to [[_COMMUNITY_WorkerPoolConfig]]
- 11 edges to [[_COMMUNITY_SubTask]]
- 9 edges to [[_COMMUNITY_DurableAgentRouter]]
- 8 edges to [[_COMMUNITY_ChainRegistry]]
- 8 edges to [[_COMMUNITY_DurableAgentFactory]]
- 7 edges to [[_COMMUNITY_OpenCodeSwarmManager]]
- 5 edges to [[_COMMUNITY_ConcurrencyRampController]]
- 5 edges to [[_COMMUNITY_MultiLayeredAgenticOrchestrator]]
- 4 edges to [[_COMMUNITY_services__init__.py]]
- 2 edges to [[_COMMUNITY_dot-get_available_worker]]
- 2 edges to [[_COMMUNITY_KnowledgeCache]]
- 1 edge to [[_COMMUNITY_TestTargetRepoRoot]]
- 1 edge to [[_COMMUNITY_multi_provider_fabric.py]]
- 1 edge to [[_COMMUNITY_claude_proxy_server.py]]
- 1 edge to [[_COMMUNITY_ProxyServerDaemon]]
- 1 edge to [[_COMMUNITY_AgenticWorkerLoop]]
- 1 edge to [[_COMMUNITY_ProgressLogEntry]]
- 1 edge to [[_COMMUNITY_TestTokenSavior]]
- 1 edge to [[_COMMUNITY_test_webapp.py]]

## Top bridge nodes
- [[WorkerRole]] - degree 42, connects to 11 communities
- [[AgentType]] - degree 31, connects to 9 communities
- [[opencode_swarm_service.py]] - degree 23, connects to 8 communities
- [[agentic_orchestrator.py]] - degree 21, connects to 6 communities
- [[agent_models.py]] - degree 17, connects to 5 communities