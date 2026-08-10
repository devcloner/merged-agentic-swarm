---
type: community
cohesion: 0.32
members: 8
---

# .handle_task_failure

**Cohesion:** 0.32 - loosely connected
**Members:** 8 nodes

## Members
- [[dot-handle_task_failure()]] - code - src/merged_agentic_swarm/services/progress_ledger_service.py
- [[dot-log_progress()]] - code - src/merged_agentic_swarm/services/progress_ledger_service.py
- [[dot-match_and_remediate()]] - code - src/merged_agentic_swarm/services/progress_ledger_service.py
- [[dot-record_success_marker()]] - code - src/merged_agentic_swarm/services/progress_ledger_service.py
- [[dot-save_ledger()]] - code - src/merged_agentic_swarm/services/progress_ledger_service.py
- [[Any_17]] - code
- [[Matches error against playbooks and applies self-healing strategy.]] - rationale - src/merged_agentic_swarm/services/progress_ledger_service.py
- [[Processes a task failure through self-healing playbooks.]] - rationale - src/merged_agentic_swarm/services/progress_ledger_service.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/handle_task_failure
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_ProgressLedgerService]]
- 2 edges to [[_COMMUNITY_ProgressLogEntry]]
- 1 edge to [[_COMMUNITY_ObstaclePlaybookEngine]]

## Top bridge nodes
- [[dot-log_progress()]] - degree 5, connects to 2 communities
- [[dot-record_success_marker()]] - degree 3, connects to 2 communities
- [[dot-handle_task_failure()]] - degree 5, connects to 1 community
- [[dot-match_and_remediate()]] - degree 4, connects to 1 community
- [[dot-save_ledger()]] - degree 3, connects to 1 community