# KnowledgeCache

> God node · 34 connections · `src/merged_agentic_swarm/tools/knowledge_cache.py`

**Community:** [KnowledgeCache](KnowledgeCache.md)

## Connections by Relation

### calls
- .test_full_lifecycle() `INFERRED`
- isolated_knowledge_cache() `INFERRED`
- .test_compacts_duplicates_on_load() `EXTRACTED`
- .test_ttl_expiry() `EXTRACTED`
- .test_add_and_get_learning() `EXTRACTED`
- .test_add_learning_different_content_same_title() `EXTRACTED`
- .test_add_learning_duplicate_content() `EXTRACTED`
- .test_add_learning_with_tags() `EXTRACTED`
- .test_cache_saves_symbols() `EXTRACTED`
- .test_empty_cache() `EXTRACTED`
- .test_max_learnings_evicts_oldest() `EXTRACTED`
- .test_persists_across_instances() `EXTRACTED`
- .test_search_learnings() `EXTRACTED`
- .test_search_learnings_empty_cache() `EXTRACTED`
- .test_search_learnings_matches_tags() `EXTRACTED`
- .test_record_dedup_identical_content() `INFERRED`
- .test_record_to_knowledge_cache() `INFERRED`

### contains
- knowledge_cache.py `EXTRACTED`

### imports
- tools/__init__.py `EXTRACTED`

### method
- .load_cache() `EXTRACTED`
- .save_cache() `EXTRACTED`
- .add_learning() `EXTRACTED`
- .get_learning() `EXTRACTED`
- .__init__() `EXTRACTED`
- .search_learnings() `EXTRACTED`

### uses
- TestKnowledgeCache `INFERRED`
- TestPromoteStep `INFERRED`
- TestDedup `INFERRED`
- TestEvaluateStep `INFERRED`
- [TestCaptureStep](TestCaptureStep.md) `INFERRED`
- TestFullLifecycle `INFERRED`
- TestLoadAfterRestart `INFERRED`
- TestRecordStep `INFERRED`
- TestRouteAndReuse `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*