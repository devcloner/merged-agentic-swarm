---
type: community
cohesion: 0.11
members: 30
---

# KnowledgeCache

**Cohesion:** 0.11 - loosely connected
**Members:** 30 nodes

## Members
- [[dot-__init__()_25]] - code - src/merged_agentic_swarm/tools/knowledge_cache.py
- [[dot-add_learning()]] - code - src/merged_agentic_swarm/tools/knowledge_cache.py
- [[dot-get_learning()]] - code - src/merged_agentic_swarm/tools/knowledge_cache.py
- [[dot-load_cache()]] - code - src/merged_agentic_swarm/tools/knowledge_cache.py
- [[dot-save_cache()]] - code - src/merged_agentic_swarm/tools/knowledge_cache.py
- [[dot-search_learnings()]] - code - src/merged_agentic_swarm/tools/knowledge_cache.py
- [[dot-test_add_and_get_learning()]] - code - tests/test_knowledge_cache.py
- [[dot-test_add_learning_different_content_same_title()]] - code - tests/test_knowledge_cache.py
- [[dot-test_add_learning_duplicate_content()]] - code - tests/test_knowledge_cache.py
- [[dot-test_add_learning_with_tags()]] - code - tests/test_knowledge_cache.py
- [[dot-test_cache_saves_symbols()]] - code - tests/test_knowledge_cache.py
- [[dot-test_compacts_duplicates_on_load()]] - code - tests/test_knowledge_cache.py
- [[dot-test_empty_cache()]] - code - tests/test_knowledge_cache.py
- [[dot-test_max_learnings_evicts_oldest()]] - code - tests/test_knowledge_cache.py
- [[dot-test_persists_across_instances()]] - code - tests/test_knowledge_cache.py
- [[dot-test_record_dedup_identical_content()]] - code - tests/test_learning_loop.py
- [[dot-test_record_to_knowledge_cache()]] - code - tests/test_learning_loop.py
- [[dot-test_search_learnings()]] - code - tests/test_knowledge_cache.py
- [[dot-test_search_learnings_empty_cache()]] - code - tests/test_knowledge_cache.py
- [[dot-test_search_learnings_matches_tags()]] - code - tests/test_knowledge_cache.py
- [[dot-test_ttl_expiry()]] - code - tests/test_knowledge_cache.py
- [[Any_23]] - code
- [[KnowledgeCache]] - code - src/merged_agentic_swarm/tools/knowledge_cache.py
- [[Learning with TTL should be expired and not returned.]] - rationale - tests/test_knowledge_cache.py
- [[Pre-populate cache file with duplicate entries, verify compaction on load.]] - rationale - tests/test_knowledge_cache.py
- [[Step 2 RECORD — Write to hot cache (knowledge_cache.json).]] - rationale - tests/test_learning_loop.py
- [[TestKnowledgeCache]] - code - tests/test_knowledge_cache.py
- [[TestRecordStep]] - code - tests/test_learning_loop.py
- [[Tests for toolsknowledge_cache.py Coverage KnowledgeCache — load_cache,…]] - rationale - tests/test_knowledge_cache.py
- [[test_knowledge_cache.py]] - code - tests/test_knowledge_cache.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/KnowledgeCache
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_WorkerRole]]
- 2 edges to [[_COMMUNITY__make_learning_entry]]
- 2 edges to [[_COMMUNITY__read_jsonl]]
- 2 edges to [[_COMMUNITY_test_learning_loop.py]]
- 1 edge to [[_COMMUNITY_TestTokenSavior]]
- 1 edge to [[_COMMUNITY_conftest.py]]
- 1 edge to [[_COMMUNITY_TestCaptureStep]]
- 1 edge to [[_COMMUNITY__evaluate_promotion_criteria]]
- 1 edge to [[_COMMUNITY__simulate_reuse]]

## Top bridge nodes
- [[KnowledgeCache]] - degree 34, connects to 9 communities
- [[TestRecordStep]] - degree 5, connects to 1 community
- [[test_knowledge_cache.py]] - degree 3, connects to 1 community