---
type: community
cohesion: 0.17
members: 12
---

# TestRun

**Cohesion:** 0.17 - loosely connected
**Members:** 12 nodes

## Members
- [[32 GET apirunstatus reports runs started by POST apirun.]] - rationale - tests/test_webapp.py
- [[32 POST apirun{id}cancel signals the workflow's cancel_event.]] - rationale - tests/test_webapp.py
- [[dot-test_run_cancel_marks_cancelling()]] - code - tests/test_webapp.py
- [[dot-test_run_cancel_unknown_404()]] - code - tests/test_webapp.py
- [[dot-test_run_learning_profile_forwards_none_ramp()]] - code - tests/test_webapp.py
- [[dot-test_run_missing_prd_400()]] - code - tests/test_webapp.py
- [[dot-test_run_missing_profile_400()]] - code - tests/test_webapp.py
- [[dot-test_run_starts_workflow_in_background()]] - code - tests/test_webapp.py
- [[dot-test_run_status_lists_and_details_runs()]] - code - tests/test_webapp.py
- [[dot-test_run_status_unknown_404()]] - code - tests/test_webapp.py
- [[dot-test_run_unknown_profile_404()]] - code - tests/test_webapp.py
- [[TestRun]] - code - tests/test_webapp.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/TestRun
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_MultiLayeredAgenticOrchestrator]]
- 1 edge to [[_COMMUNITY_test_webapp.py]]

## Top bridge nodes
- [[TestRun]] - degree 11, connects to 2 communities