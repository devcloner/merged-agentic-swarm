# CodebaseMapService

> 40 nodes · cohesion 0.08

## Key Concepts

- **DurableAgentRouter** (30 connections) — `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- **TestDurableAgentRouter** (19 connections) — `tests/test_opencode_swarm_service.py`
- **.execute_subtask_with_worker()** (12 connections) — `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- **.find_matching_agent()** (8 connections) — `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- **.load()** (7 connections) — `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- **._run_opencode_worker()** (7 connections) — `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- **Any** (7 connections)
- **get_durable_router()** (6 connections) — `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- **._extract_keywords()** (5 connections) — `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- **._parse_frontmatter()** (5 connections) — `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- **._scan_agent_triggers()** (5 connections) — `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- **._read_body()** (4 connections) — `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- **._get_pool_id()** (4 connections) — `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- **Path** (4 connections)
- **.get_stats()** (3 connections) — `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- **.__init__()** (3 connections) — `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- **.test_default_router_discovers_config_path_agent()** (3 connections) — `tests/test_opencode_swarm_service.py`
- **.test_find_matching_agent_by_category_and_keywords()** (3 connections) — `tests/test_opencode_swarm_service.py`
- **.test_find_matching_agent_no_match_returns_none()** (3 connections) — `tests/test_opencode_swarm_service.py`
- **.test_dedupes_by_id()** (2 connections) — `tests/test_opencode_swarm_service.py`
- **.test_extract_keywords_drops_stopwords()** (2 connections) — `tests/test_opencode_swarm_service.py`
- **.test_get_durable_router_singleton()** (2 connections) — `tests/test_opencode_swarm_service.py`
- **.test_load_from_jsonl()** (2 connections) — `tests/test_opencode_swarm_service.py`
- **.test_load_from_markdown_frontmatter()** (2 connections) — `tests/test_opencode_swarm_service.py`
- **.test_parse_frontmatter_and_body()** (2 connections) — `tests/test_opencode_swarm_service.py`
- *... and 15 more nodes in this community*

## Relationships

- [SubTask](SubTask.md) (12 shared connections)
- [AgentSpec](AgentSpec.md) (8 shared connections)
- [test_streaming_proxy.py](test_streaming_proxy.py.md) (6 shared connections)
- [OpenCodeSwarmManager](OpenCodeSwarmManager.md) (3 shared connections)
- [WorkerPoolConfig](WorkerPoolConfig.md) (3 shared connections)
- [ChainRegistry](ChainRegistry.md) (3 shared connections)
- [WorkerRole](WorkerRole.md) (2 shared connections)
- [promotion_policy](promotion_policy.md) (2 shared connections)
- [DurableAgentRouter](DurableAgentRouter.md) (1 shared connections)
- [PassthroughStreamingProxy](PassthroughStreamingProxy.md) (1 shared connections)

## Source Files

- `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- `tests/test_opencode_swarm_service.py`

## Audit Trail

- EXTRACTED: 148 (89%)
- INFERRED: 19 (11%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*