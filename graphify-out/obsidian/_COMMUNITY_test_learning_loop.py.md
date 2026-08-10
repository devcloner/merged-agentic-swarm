---
type: community
cohesion: 0.11
members: 22
---

# test_learning_loop.py

**Cohesion:** 0.11 - loosely connected
**Members:** 22 nodes

## Members
- [[dot-test_evaluate_detects_duplicate()]] - code - tests/test_learning_loop.py
- [[dot-test_evaluate_fails_weak_entry()]] - code - tests/test_learning_loop.py
- [[dot-test_evaluate_passes_strong_entry()]] - code - tests/test_learning_loop.py
- [[A strong, substantive entry should pass all promotion criteria.]] - rationale - tests/test_learning_loop.py
- [[A weak entry should fail promotion criteria.]] - rationale - tests/test_learning_loop.py
- [[Append a single JSON entry as a line to a JSONL file.]] - rationale - tests/test_learning_loop.py
- [[Create a cold-path agents.jsonl entry.]] - rationale - tests/test_learning_loop.py
- [[Create a cold-path chain.jsonl entry.]] - rationale - tests/test_learning_loop.py
- [[Create a cold-path knowledge.jsonl entry.]] - rationale - tests/test_learning_loop.py
- [[Evaluate whether a learning entry meets cold-path promotion criteria. Returns…]] - rationale - tests/test_learning_loop.py
- [[Should detect when an entry already exists in cold knowledge.]] - rationale - tests/test_learning_loop.py
- [[Step 3 EVALUATE — Score learning against promotion criteria.]] - rationale - tests/test_learning_loop.py
- [[Step LOAD — Simulate loading agents after a restart.]] - rationale - tests/test_learning_loop.py
- [[TestEvaluateStep]] - code - tests/test_learning_loop.py
- [[TestLoadAfterRestart]] - code - tests/test_learning_loop.py
- [[Tests for the full learning loop lifecycle capture - evaluate - promote -…]] - rationale - tests/test_learning_loop.py
- [[_append_jsonl()]] - code - tests/test_learning_loop.py
- [[_evaluate_promotion_criteria()]] - code - tests/test_learning_loop.py
- [[_make_agent_jsonl_entry()]] - code - tests/test_learning_loop.py
- [[_make_chain_jsonl_entry()]] - code - tests/test_learning_loop.py
- [[_make_knowledge_jsonl_entry()]] - code - tests/test_learning_loop.py
- [[test_learning_loop.py]] - code - tests/test_learning_loop.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/test_learning_looppy
SORT file.name ASC
```

## Connections to other communities
- 16 edges to [[_COMMUNITY__make_learning_entry]]
- 8 edges to [[_COMMUNITY__read_jsonl]]
- 3 edges to [[_COMMUNITY_KnowledgeCache]]
- 1 edge to [[_COMMUNITY_TestCaptureStep]]

## Top bridge nodes
- [[test_learning_loop.py]] - degree 20, connects to 4 communities
- [[_evaluate_promotion_criteria()]] - degree 10, connects to 2 communities
- [[TestLoadAfterRestart]] - degree 5, connects to 2 communities
- [[TestEvaluateStep]] - degree 6, connects to 1 community
- [[dot-test_evaluate_detects_duplicate()]] - degree 6, connects to 1 community