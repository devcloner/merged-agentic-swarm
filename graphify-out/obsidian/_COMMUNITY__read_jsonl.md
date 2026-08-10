---
type: community
cohesion: 0.24
members: 12
---

# _read_jsonl

**Cohesion:** 0.24 - loosely connected
**Members:** 12 nodes

## Members
- [[dot-test_full_lifecycle()]] - code - tests/test_learning_loop.py
- [[dot-test_multiple_promotions_in_sequence()]] - code - tests/test_learning_loop.py
- [[End-to-end capture - record - evaluate - promote - verify - load - route…]] - rationale - tests/test_learning_loop.py
- [[Promote multiple different learnings and verify they are all loadable.]] - rationale - tests/test_learning_loop.py
- [[Read all JSONL entries from a file, returning a list of dicts.]] - rationale - tests/test_learning_loop.py
- [[Run the complete lifecycle and verify every step.]] - rationale - tests/test_learning_loop.py
- [[Simulate loading agents after restart read agents.jsonl and .md files.]] - rationale - tests/test_learning_loop.py
- [[TestFullLifecycle]] - code - tests/test_learning_loop.py
- [[Verify all 5 cold-path artifacts exist and are valid. Returns list of failures.]] - rationale - tests/test_learning_loop.py
- [[_load_agents_from_registry()]] - code - tests/test_learning_loop.py
- [[_read_jsonl()_1]] - code - tests/test_learning_loop.py
- [[_verify_promotion()]] - code - tests/test_learning_loop.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/_read_jsonl
SORT file.name ASC
```

## Connections to other communities
- 9 edges to [[_COMMUNITY__make_learning_entry]]
- 4 edges to [[_COMMUNITY_test_learning_loop.py]]
- 3 edges to [[_COMMUNITY__simulate_reuse]]
- 2 edges to [[_COMMUNITY_KnowledgeCache]]
- 2 edges to [[_COMMUNITY__evaluate_promotion_criteria]]

## Top bridge nodes
- [[dot-test_full_lifecycle()]] - degree 10, connects to 4 communities
- [[_read_jsonl()_1]] - degree 10, connects to 3 communities
- [[_load_agents_from_registry()]] - degree 8, connects to 3 communities
- [[_verify_promotion()]] - degree 6, connects to 2 communities
- [[TestFullLifecycle]] - degree 5, connects to 2 communities