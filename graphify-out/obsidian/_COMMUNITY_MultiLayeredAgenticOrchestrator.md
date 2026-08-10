---
type: community
cohesion: 0.09
members: 37
---

# MultiLayeredAgenticOrchestrator

**Cohesion:** 0.09 - loosely connected
**Members:** 37 nodes

## Members
- [[dot-__init__()_24]] - code - src/merged_agentic_swarm/tools/agentic_orchestrator.py
- [[dot-_abort_on_gate_failure()]] - code - src/merged_agentic_swarm/tools/agentic_orchestrator.py
- [[dot-_append_jsonl()]] - code - src/merged_agentic_swarm/tools/agentic_orchestrator.py
- [[dot-_apply_worker_outputs()]] - code - src/merged_agentic_swarm/tools/agentic_orchestrator.py
- [[dot-_compact_registries()]] - code - src/merged_agentic_swarm/tools/agentic_orchestrator.py
- [[dot-_load_promoted_ids()]] - code - src/merged_agentic_swarm/tools/agentic_orchestrator.py
- [[dot-_make_core_files()]] - code - tests/test_agentic_orchestrator.py
- [[dot-_promote_cold_path()]] - code - src/merged_agentic_swarm/tools/agentic_orchestrator.py
- [[dot-_run_syntax_verification()]] - code - src/merged_agentic_swarm/tools/agentic_orchestrator.py
- [[dot-_save_promoted_ids()]] - code - src/merged_agentic_swarm/tools/agentic_orchestrator.py
- [[dot-initialize_system()]] - code - src/merged_agentic_swarm/tools/agentic_orchestrator.py
- [[dot-run_full_agentic_workflow()]] - code - src/merged_agentic_swarm/tools/agentic_orchestrator.py
- [[dot-test_ci_script_nonzero_exit()]] - code - tests/test_agentic_orchestrator.py
- [[dot-test_event_set_returns_aborted()]] - code - tests/test_agentic_orchestrator.py
- [[dot-test_event_unset_or_none_returns_none()]] - code - tests/test_agentic_orchestrator.py
- [[dot-test_inline_syntax_error_detected()]] - code - tests/test_agentic_orchestrator.py
- [[dot-test_inline_syntax_pass()]] - code - tests/test_agentic_orchestrator.py
- [[dot-test_load_invalid_json_warns()]] - code - tests/test_agentic_orchestrator.py
- [[dot-test_save_to_path_under_file_warns()]] - code - tests/test_agentic_orchestrator.py
- [[Any_22]] - code
- [[Append a JSON line to a JSONL registry.]] - rationale - src/merged_agentic_swarm/tools/agentic_orchestrator.py
- [[Apply worker outputs to disk and count files written. Primary path agentic-…]] - rationale - src/merged_agentic_swarm/tools/agentic_orchestrator.py
- [[Cold-path normalize hot cache entries → knowledge.jsonl → validated →…]] - rationale - src/merged_agentic_swarm/tools/agentic_orchestrator.py
- [[Deduplicate cold-path registries by content hash (knowledge) and ID…]] - rationale - src/merged_agentic_swarm/tools/agentic_orchestrator.py
- [[Event_1]] - code
- [[Initializes Key Pool Proxy server and verifies service readiness.]] - rationale - src/merged_agentic_swarm/tools/agentic_orchestrator.py
- [[Load previously promoted learning IDs so cold-path dedup survives restarts.]] - rationale - src/merged_agentic_swarm/tools/agentic_orchestrator.py
- [[MultiLayeredAgenticOrchestrator]] - code - src/merged_agentic_swarm/tools/agentic_orchestrator.py
- [[Persist promoted learning IDs for the next run.]] - rationale - src/merged_agentic_swarm/tools/agentic_orchestrator.py
- [[Return an abort result when a gate fails and gates are enforced.…]] - rationale - src/merged_agentic_swarm/tools/agentic_orchestrator.py
- [[Return an aborted result if the run was cancelled, else None.]] - rationale - src/merged_agentic_swarm/tools/agentic_orchestrator.py
- [[Run actual syntax + import verification instead of hardcoded unittest (FIX-10).…]] - rationale - src/merged_agentic_swarm/tools/agentic_orchestrator.py
- [[Runs the complete self-healing 6-step agent-to-agent workflow.…]] - rationale - src/merged_agentic_swarm/tools/agentic_orchestrator.py
- [[TestCancellationCheck]] - code - tests/test_agentic_orchestrator.py
- [[TestPromotedIdsBranches]] - code - tests/test_agentic_orchestrator.py
- [[TestRunSyntaxVerificationPaths]] - code - tests/test_agentic_orchestrator.py
- [[_cancellation_check()]] - code - src/merged_agentic_swarm/tools/agentic_orchestrator.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/MultiLayeredAgenticOrchestrator
SORT file.name ASC
```

## Connections to other communities
- 19 edges to [[_COMMUNITY_SubTask]]
- 9 edges to [[_COMMUNITY_PRDAnalysisResult]]
- 3 edges to [[_COMMUNITY_services__init__.py]]
- 2 edges to [[_COMMUNITY_WorkerRole]]
- 2 edges to [[_COMMUNITY_ProxyServerDaemon]]
- 2 edges to [[_COMMUNITY_handle_run]]
- 2 edges to [[_COMMUNITY_TestRunFullAgenticWorkflow]]
- 2 edges to [[_COMMUNITY_test_webapp.py]]
- 1 edge to [[_COMMUNITY_webapp.py]]
- 1 edge to [[_COMMUNITY__Stream]]
- 1 edge to [[_COMMUNITY_TestChains]]
- 1 edge to [[_COMMUNITY_TestLatencyTest]]
- 1 edge to [[_COMMUNITY_TestModelRoleUpdate]]
- 1 edge to [[_COMMUNITY_TestProfiles]]
- 1 edge to [[_COMMUNITY_TestReports]]
- 1 edge to [[_COMMUNITY_TestRun]]
- 1 edge to [[_COMMUNITY_TestRunPlan]]

## Top bridge nodes
- [[MultiLayeredAgenticOrchestrator]] - degree 52, connects to 17 communities
- [[TestRunSyntaxVerificationPaths]] - degree 10, connects to 2 communities
- [[TestCancellationCheck]] - degree 8, connects to 2 communities
- [[TestPromotedIdsBranches]] - degree 8, connects to 2 communities
- [[_cancellation_check()]] - degree 7, connects to 1 community