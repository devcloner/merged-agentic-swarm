---
type: community
cohesion: 0.33
members: 6
---

# TestCaptureStep

**Cohesion:** 0.33 - loosely connected
**Members:** 6 nodes

## Members
- [[dot-test_capture_produces_valid_entry()]] - code - tests/test_learning_loop.py
- [[dot-test_capture_requires_specific_claim()]] - code - tests/test_learning_loop.py
- [[A captured learning scenario produces a properly structured entry.]] - rationale - tests/test_learning_loop.py
- [[A genericnon-specific entry should be identifiable as weak.]] - rationale - tests/test_learning_loop.py
- [[Step 1 CAPTURE — Create a controlled learning scenario.]] - rationale - tests/test_learning_loop.py
- [[TestCaptureStep]] - code - tests/test_learning_loop.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/TestCaptureStep
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY__make_learning_entry]]
- 1 edge to [[_COMMUNITY_KnowledgeCache]]
- 1 edge to [[_COMMUNITY_test_learning_loop.py]]

## Top bridge nodes
- [[TestCaptureStep]] - degree 5, connects to 2 communities
- [[dot-test_capture_produces_valid_entry()]] - degree 3, connects to 1 community
- [[dot-test_capture_requires_specific_claim()]] - degree 3, connects to 1 community