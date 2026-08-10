---
type: community
cohesion: 0.20
members: 12
---

# _evaluate_promotion_criteria

**Cohesion:** 0.20 - loosely connected
**Members:** 12 nodes

## Members
- [[dot-test_evaluate_detects_duplicate()]] - code - tests/test_learning_loop.py
- [[dot-test_evaluate_fails_weak_entry()]] - code - tests/test_learning_loop.py
- [[dot-test_evaluate_passes_strong_entry()]] - code - tests/test_learning_loop.py
- [[A strong, substantive entry should pass all promotion criteria.]] - rationale - tests/test_learning_loop.py
- [[A weak entry should fail promotion criteria.]] - rationale - tests/test_learning_loop.py
- [[Append a single JSON entry as a line to a JSONL file.]] - rationale - tests/test_learning_loop.py
- [[Evaluate whether a learning entry meets cold-path promotion criteria. Returns…]] - rationale - tests/test_learning_loop.py
- [[Should detect when an entry already exists in cold knowledge.]] - rationale - tests/test_learning_loop.py
- [[Step 3 EVALUATE — Score learning against promotion criteria.]] - rationale - tests/test_learning_loop.py
- [[TestEvaluateStep]] - code - tests/test_learning_loop.py
- [[_append_jsonl()]] - code - tests/test_learning_loop.py
- [[_evaluate_promotion_criteria()]] - code - tests/test_learning_loop.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/_evaluate_promotion_criteria
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY__make_learning_entry]]
- 4 edges to [[_COMMUNITY_test_learning_loop.py]]
- 2 edges to [[_COMMUNITY__read_jsonl]]
- 1 edge to [[_COMMUNITY_KnowledgeCache]]

## Top bridge nodes
- [[_evaluate_promotion_criteria()]] - degree 10, connects to 3 communities
- [[TestEvaluateStep]] - degree 6, connects to 2 communities
- [[dot-test_evaluate_detects_duplicate()]] - degree 6, connects to 2 communities
- [[_append_jsonl()]] - degree 4, connects to 2 communities
- [[dot-test_evaluate_fails_weak_entry()]] - degree 4, connects to 1 community