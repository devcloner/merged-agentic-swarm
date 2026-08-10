---
type: community
cohesion: 0.08
members: 31
---

# OpenCodeSwarmManager

**Cohesion:** 0.08 - loosely connected
**Members:** 31 nodes

## Members
- [[dot-__init__()_14]] - code - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[dot-_get_available_worker_unlocked()]] - code - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[dot-_get_pool_id()]] - code - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[dot-_initialize_worker_pool()]] - code - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[dot-get_available_worker()]] - code - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[dot-setup_method()_17]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_batch_parallel_custom_ramp_clamped_and_bounded()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_batch_parallel_omits_alias_when_none()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_batch_parallel_threads_explicit_model_alias()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_batch_parallel_uses_custom_ramp()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_batch_parallel_uses_ramp_concurrency()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_get_available_worker_fallback_to_core_engineer()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_get_available_worker_returns_correct_role()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_get_available_worker_round_robin()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_get_available_worker_tester_round_robin()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_get_pool_id_fallback()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_get_pool_id_mapped()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_initializes_40_workers()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_workers_by_role()]] - code - tests/test_opencode_swarm_service.py
- [[A custom ramp past the configured cap is clamped to max_total_workers; levels…]] - rationale - tests/test_opencode_swarm_service.py
- [[A provided ramp_sequence overrides the default wave_gate_level mapping.]] - rationale - tests/test_opencode_swarm_service.py
- [[An explicit model_alias on the batch is threaded into every worker.]] - rationale - tests/test_opencode_swarm_service.py
- [[Gets an available worker matching the specified role using round-robin…]] - rationale - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[Getting a role with zero allocation should fall back to core engineer.]] - rationale - tests/test_opencode_swarm_service.py
- [[Initializes the 40 worker specs across role allocations.]] - rationale - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[Internal must be called while holding self._worker_lock.]] - rationale - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[Map a WorkerRole to a pool-health bucket key.]] - rationale - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[OpenCodeSwarmManager]] - code - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[TestOpenCodeSwarmManager]] - code - tests/test_opencode_swarm_service.py
- [[Wave N batch executes at rampN concurrency, not the 4-worker default.]] - rationale - tests/test_opencode_swarm_service.py
- [[With model_alias=None the worker receives no alias kwarg — each worker resolves…]] - rationale - tests/test_opencode_swarm_service.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/OpenCodeSwarmManager
SORT file.name ASC
```

## Connections to other communities
- 14 edges to [[_COMMUNITY_WorkerRole]]
- 9 edges to [[_COMMUNITY_TestExecuteSubtaskDecisionLogic]]
- 6 edges to [[_COMMUNITY_DurableAgentRouter]]
- 4 edges to [[_COMMUNITY_AgentSpec]]
- 4 edges to [[_COMMUNITY_ConcurrencyRampController]]
- 2 edges to [[_COMMUNITY_WorkerPoolState]]
- 2 edges to [[_COMMUNITY_PRDAnalysisResult]]
- 2 edges to [[_COMMUNITY_SubTask]]
- 2 edges to [[_COMMUNITY_TestTargetRepoRoot]]
- 1 edge to [[_COMMUNITY_services__init__.py]]
- 1 edge to [[_COMMUNITY_conftest.py]]

## Top bridge nodes
- [[OpenCodeSwarmManager]] - degree 32, connects to 11 communities
- [[TestOpenCodeSwarmManager]] - degree 24, connects to 6 communities
- [[dot-get_available_worker()]] - degree 6, connects to 3 communities
- [[dot-__init__()_14]] - degree 5, connects to 3 communities
- [[dot-_get_available_worker_unlocked()]] - degree 5, connects to 2 communities