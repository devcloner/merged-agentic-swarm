---
type: community
cohesion: 0.17
members: 23
---

# report_service.py

**Cohesion:** 0.17 - loosely connected
**Members:** 23 nodes

## Members
- [[Any_18]] - code
- [[Build a run report and persist it as both JSON and Markdown. Returns…]] - rationale - src/merged_agentic_swarm/services/report_service.py
- [[Build a run-report dict from the live progress ledger + cold-path registries.]] - rationale - src/merged_agentic_swarm/services/report_service.py
- [[Chronological event list (ledger steps + chain spawns) with model per step.]] - rationale - src/merged_agentic_swarm/services/report_service.py
- [[Derive per-wave gate passfail from ledger log statuses. The orchestrator…]] - rationale - src/merged_agentic_swarm/services/report_service.py
- [[Generate and persist a run report, rendering a readable timeline.]] - rationale - src/merged_agentic_swarm/tools/agentic_cli.py
- [[Group ledger logs by wave, tallying statuses, tokens, and distinct models.]] - rationale - src/merged_agentic_swarm/services/report_service.py
- [[Path_2]] - code
- [[Per-epic status from the ledger snapshot plus log-derived status tallies.]] - rationale - src/merged_agentic_swarm/services/report_service.py
- [[Render a run-report dict as human-readable Markdown (with model timeline).]] - rationale - src/merged_agentic_swarm/services/report_service.py
- [[Run Report Service Builds and persists orchestration run reports (JSON +…]] - rationale - src/merged_agentic_swarm/services/report_service.py
- [[_build_epics()]] - code - src/merged_agentic_swarm/services/report_service.py
- [[_build_gates()]] - code - src/merged_agentic_swarm/services/report_service.py
- [[_build_timeline()]] - code - src/merged_agentic_swarm/services/report_service.py
- [[_build_waves()]] - code - src/merged_agentic_swarm/services/report_service.py
- [[_format_ts()]] - code - src/merged_agentic_swarm/services/report_service.py
- [[_read_json()]] - code - src/merged_agentic_swarm/services/report_service.py
- [[_read_jsonl()]] - code - src/merged_agentic_swarm/services/report_service.py
- [[build_run_report()]] - code - src/merged_agentic_swarm/services/report_service.py
- [[cmd_report()]] - code - src/merged_agentic_swarm/tools/agentic_cli.py
- [[render_report_md()]] - code - src/merged_agentic_swarm/services/report_service.py
- [[report_service.py]] - code - src/merged_agentic_swarm/services/report_service.py
- [[save_run_report()]] - code - src/merged_agentic_swarm/services/report_service.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/report_servicepy
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_services__init__.py]]

## Top bridge nodes
- [[report_service.py]] - degree 12, connects to 1 community
- [[save_run_report()]] - degree 9, connects to 1 community
- [[render_report_md()]] - degree 7, connects to 1 community
- [[cmd_report()]] - degree 5, connects to 1 community