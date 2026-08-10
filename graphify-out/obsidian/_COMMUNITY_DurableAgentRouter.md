---
type: community
cohesion: 0.08
members: 40
---

# DurableAgentRouter

**Cohesion:** 0.08 - loosely connected
**Members:** 40 nodes

## Members
- [[31 a cold agent at the user-config path must be routed by a default…]] - rationale - tests/test_opencode_swarm_service.py
- [[dot-__init__()_13]] - code - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[dot-_extract_keywords()]] - code - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[dot-_get_pool_id()]] - code - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[dot-_parse_frontmatter()]] - code - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[dot-_read_body()]] - code - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[dot-_run_opencode_worker()]] - code - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[dot-_scan_agent_triggers()]] - code - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[dot-execute_subtask_with_worker()]] - code - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[dot-find_matching_agent()]] - code - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[dot-get_stats()]] - code - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[dot-load()]] - code - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[dot-test_dedupes_by_id()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_default_router_discovers_config_path_agent()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_extract_keywords_drops_stopwords()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_find_matching_agent_by_category_and_keywords()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_find_matching_agent_no_match_returns_none()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_get_durable_router_singleton()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_load_from_jsonl()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_load_from_markdown_frontmatter()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_parse_frontmatter_and_body()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_scan_agent_triggers()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_skips_bad_jsonl_lines()]] - code - tests/test_opencode_swarm_service.py
- [[Any_16]] - code
- [[Collect trigger keywords from an agent's body (Trigger section) + system_prompt.]] - rationale - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[Dispatches a single subtask — first checks for a matching durable agent, then…]] - rationale - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[DurableAgentRouter]] - code - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[Extract YAML-style frontmatter between --- markers.]] - rationale - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[Extract lowercase alphanumeric tokens, dropping very shortcommon words.]] - rationale - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[Find the best-matching durable agent for a subtask. Returns agent dict with…]] - rationale - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[Lazy-initialised singleton for the durable agent router.]] - rationale - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[Load all durable agents from agents.jsonl and .claudeagents.md. Returns the…]] - rationale - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[Loads promoted durable agents from registry and disk, then matches incoming…]] - rationale - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[Map a WorkerRole to a pool-health bucket key.]] - rationale - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[Path_1]] - code
- [[Read the body content after frontmatter.]] - rationale - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[Return router statistics for reporting.]] - rationale - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[Run a subtask via the opencode worker launcher (SWARM_WORKER_MODE=opencode).…]] - rationale - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[TestDurableAgentRouter]] - code - tests/test_opencode_swarm_service.py
- [[get_durable_router()]] - code - src/merged_agentic_swarm/services/opencode_swarm_service.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/DurableAgentRouter
SORT file.name ASC
```

## Connections to other communities
- 11 edges to [[_COMMUNITY_OpenCodeSwarmManager]]
- 9 edges to [[_COMMUNITY_WorkerRole]]
- 8 edges to [[_COMMUNITY_SubTask]]
- 3 edges to [[_COMMUNITY_AgentSpec]]
- 3 edges to [[_COMMUNITY_WorkerPoolConfig]]
- 3 edges to [[_COMMUNITY_ConcurrencyRampController]]
- 2 edges to [[_COMMUNITY_TestTargetRepoRoot]]
- 1 edge to [[_COMMUNITY_services__init__.py]]
- 1 edge to [[_COMMUNITY_dot-get_available_worker]]

## Top bridge nodes
- [[DurableAgentRouter]] - degree 30, connects to 7 communities
- [[dot-execute_subtask_with_worker()]] - degree 12, connects to 6 communities
- [[TestDurableAgentRouter]] - degree 19, connects to 5 communities
- [[dot-_run_opencode_worker()]] - degree 7, connects to 3 communities
- [[dot-_get_pool_id()]] - degree 4, connects to 2 communities