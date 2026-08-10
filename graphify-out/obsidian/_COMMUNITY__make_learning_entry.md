---
type: community
cohesion: 0.18
members: 21
---

# _make_learning_entry

**Cohesion:** 0.18 - loosely connected
**Members:** 21 nodes

## Members
- [[dot-test_agent_md_file_survives_restart()]] - code - tests/test_learning_loop.py
- [[dot-test_dedup_via_content_hash()]] - code - tests/test_learning_loop.py
- [[dot-test_different_content_not_deduped()]] - code - tests/test_learning_loop.py
- [[dot-test_duplicate_learning_not_promoted()]] - code - tests/test_learning_loop.py
- [[dot-test_fresh_load_finds_promoted_agent()]] - code - tests/test_learning_loop.py
- [[dot-test_promote_agent_md_has_required_frontmatter()]] - code - tests/test_learning_loop.py
- [[dot-test_promote_agents_jsonl_has_correct_fields()]] - code - tests/test_learning_loop.py
- [[dot-test_promote_chain_jsonl_has_correct_fields()]] - code - tests/test_learning_loop.py
- [[dot-test_promote_knowledge_jsonl_has_correct_fields()]] - code - tests/test_learning_loop.py
- [[dot-test_promote_progress_json_updated()]] - code - tests/test_learning_loop.py
- [[dot-test_promote_writes_all_five_artifacts()]] - code - tests/test_learning_loop.py
- [[Create a learning entry dict matching the knowledge_cache schema.]] - rationale - tests/test_learning_loop.py
- [[Dedup identical learning should not produce duplicate agent.]] - rationale - tests/test_learning_loop.py
- [[Entries with different content should not collide.]] - rationale - tests/test_learning_loop.py
- [[Execute cold-path promotion write all 5 output files. Returns dict with paths…]] - rationale - tests/test_learning_loop.py
- [[Step 4 PROMOTE — Write all 5 cold-path artifacts.]] - rationale - tests/test_learning_loop.py
- [[TestDedup]] - code - tests/test_learning_loop.py
- [[TestPromoteStep]] - code - tests/test_learning_loop.py
- [[Verify that content-hash-based dedup catches semantically identical entries.]] - rationale - tests/test_learning_loop.py
- [[_make_learning_entry()]] - code - tests/test_learning_loop.py
- [[_promote_learning()]] - code - tests/test_learning_loop.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/_make_learning_entry
SORT file.name ASC
```

## Connections to other communities
- 16 edges to [[_COMMUNITY_test_learning_loop.py]]
- 13 edges to [[_COMMUNITY__read_jsonl]]
- 2 edges to [[_COMMUNITY_KnowledgeCache]]
- 2 edges to [[_COMMUNITY_TestCaptureStep]]

## Top bridge nodes
- [[_make_learning_entry()]] - degree 22, connects to 3 communities
- [[_promote_learning()]] - degree 21, connects to 2 communities
- [[TestPromoteStep]] - degree 9, connects to 2 communities
- [[TestDedup]] - degree 6, connects to 2 communities
- [[dot-test_fresh_load_finds_promoted_agent()]] - degree 4, connects to 2 communities