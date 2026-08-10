---
type: community
cohesion: 0.20
members: 10
---

# test_learning_loop.py

**Cohesion:** 0.20 - loosely connected
**Members:** 10 nodes

## Members
- [[Create a cold-path agents.jsonl entry.]] - rationale - tests/test_learning_loop.py
- [[Create a cold-path chain.jsonl entry.]] - rationale - tests/test_learning_loop.py
- [[Create a cold-path knowledge.jsonl entry.]] - rationale - tests/test_learning_loop.py
- [[Step LOAD — Simulate loading agents after a restart.]] - rationale - tests/test_learning_loop.py
- [[TestLoadAfterRestart]] - code - tests/test_learning_loop.py
- [[Tests for the full learning loop lifecycle capture - evaluate - promote -…]] - rationale - tests/test_learning_loop.py
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
- 9 edges to [[_COMMUNITY__make_learning_entry]]
- 4 edges to [[_COMMUNITY__evaluate_promotion_criteria]]
- 4 edges to [[_COMMUNITY__read_jsonl]]
- 2 edges to [[_COMMUNITY_KnowledgeCache]]
- 2 edges to [[_COMMUNITY__simulate_reuse]]
- 1 edge to [[_COMMUNITY_TestCaptureStep]]

## Top bridge nodes
- [[test_learning_loop.py]] - degree 20, connects to 6 communities
- [[TestLoadAfterRestart]] - degree 5, connects to 2 communities
- [[_make_knowledge_jsonl_entry()]] - degree 4, connects to 2 communities
- [[_make_agent_jsonl_entry()]] - degree 3, connects to 1 community
- [[_make_chain_jsonl_entry()]] - degree 3, connects to 1 community