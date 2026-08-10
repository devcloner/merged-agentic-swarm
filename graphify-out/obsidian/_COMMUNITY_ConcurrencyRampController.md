---
type: community
cohesion: 0.12
members: 18
---

# ConcurrencyRampController

**Cohesion:** 0.12 - loosely connected
**Members:** 18 nodes

## Members
- [[dot-execute_subtask_batch_parallel()]] - code - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[dot-get_current_max_workers()]] - code - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[dot-get_ramp_sequence()]] - code - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[dot-setup_method()_16]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_get_current_max_workers_beyond_gates()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_get_current_max_workers_gate_0()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_get_current_max_workers_gate_1()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_get_current_max_workers_gate_2()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_get_current_max_workers_gate_3()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_get_current_max_workers_negative()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_get_ramp_sequence()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_ramp_sequence_length()]] - code - tests/test_opencode_swarm_service.py
- [[ConcurrencyRampController]] - code - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[Controls worker concurrency ramp-up across wave gates.]] - rationale - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[Executes a batch of subtasks in parallel using ThreadPoolExecutor up to max…]] - rationale - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[Map wave gate level to max workers. Gate 0 - 4, gate 1 - 8, gate 2 - 16,…]] - rationale - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[Return the full ramp sequence.]] - rationale - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[TestConcurrencyRampController]] - code - tests/test_opencode_swarm_service.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ConcurrencyRampController
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_WorkerRole]]
- 5 edges to [[_COMMUNITY_SubTask]]
- 5 edges to [[_COMMUNITY_OpenCodeSwarmManager]]
- 4 edges to [[_COMMUNITY_WorkerPoolConfig]]
- 3 edges to [[_COMMUNITY_DurableAgentRouter]]
- 1 edge to [[_COMMUNITY_AgentSpec]]
- 1 edge to [[_COMMUNITY_TestTargetRepoRoot]]

## Top bridge nodes
- [[ConcurrencyRampController]] - degree 18, connects to 7 communities
- [[TestConcurrencyRampController]] - degree 17, connects to 5 communities
- [[dot-execute_subtask_batch_parallel()]] - degree 6, connects to 4 communities