---
type: community
cohesion: 0.06
members: 52
---

# MultiLayeredAgenticOrchestrator

**Cohesion:** 0.06 - loosely connected
**Members:** 52 nodes

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
- [[dot-setup_method()_1]] - code - tests/test_agentic_orchestrator.py
- [[dot-test_chain_entry_ids_unique_within_batch()]] - code - tests/test_agentic_orchestrator.py
- [[dot-test_ci_script_nonzero_exit()]] - code - tests/test_agentic_orchestrator.py
- [[dot-test_event_set_returns_aborted()]] - code - tests/test_agentic_orchestrator.py
- [[dot-test_event_unset_or_none_returns_none()]] - code - tests/test_agentic_orchestrator.py
- [[dot-test_existing_agent_file_skipped()]] - code - tests/test_agentic_orchestrator.py
- [[dot-test_inline_syntax_error_detected()]] - code - tests/test_agentic_orchestrator.py
- [[dot-test_inline_syntax_pass()]] - code - tests/test_agentic_orchestrator.py
- [[dot-test_load_invalid_json_warns()]] - code - tests/test_agentic_orchestrator.py
- [[dot-test_relative_path_resolves_and_write_failure_logged()]] - code - tests/test_agentic_orchestrator.py
- [[dot-test_save_to_path_under_file_warns()]] - code - tests/test_agentic_orchestrator.py
- [[dot-test_secondary_text_from_response_dict()]] - code - tests/test_agentic_orchestrator.py
- [[A relative  file path that resolves to a directory triggers the write-failure…]] - rationale - tests/test_agentic_orchestrator.py
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
- [[TestApplyWorkerOutputsPaths]] - code - tests/test_agentic_orchestrator.py
- [[TestCancellationCheck]] - code - tests/test_agentic_orchestrator.py
- [[TestPromoteColdPathAgentFileExists]] - code - tests/test_agentic_orchestrator.py
- [[TestPromoteColdPathChainEntryIds]] - code - tests/test_agentic_orchestrator.py
- [[TestPromotedIdsBranches]] - code - tests/test_agentic_orchestrator.py
- [[TestRunSyntaxVerificationPaths]] - code - tests/test_agentic_orchestrator.py
- [[Tests for toolsagentic_orchestrator.py Coverage…]] - rationale - tests/test_agentic_orchestrator.py
- [[Two categories promoted in one batch must produce distinct chain entry_ids…]] - rationale - tests/test_agentic_orchestrator.py
- [[When _write_agent_spec_file returns None (already exists), the skip branch logs…]] - rationale - tests/test_agentic_orchestrator.py
- [[_analysis()]] - code - tests/test_agentic_orchestrator.py
- [[_cancellation_check()]] - code - src/merged_agentic_swarm/tools/agentic_orchestrator.py
- [[_epic()]] - code - tests/test_agentic_orchestrator.py
- [[test_agentic_orchestrator.py]] - code - tests/test_agentic_orchestrator.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/MultiLayeredAgenticOrchestrator
SORT file.name ASC
```

## Connections to other communities
- 34 edges to [[_COMMUNITY_SubTask]]
- 5 edges to [[_COMMUNITY_WorkerRole]]
- 4 edges to [[_COMMUNITY_TestRunFullAgenticWorkflow]]
- 3 edges to [[_COMMUNITY_services__init__.py]]
- 2 edges to [[_COMMUNITY_ProxyServerDaemon]]
- 2 edges to [[_COMMUNITY_handle_run]]
- 2 edges to [[_COMMUNITY_test_webapp.py]]
- 1 edge to [[_COMMUNITY_TestTokenSavior]]
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
- [[MultiLayeredAgenticOrchestrator]] - degree 52, connects to 16 communities
- [[test_agentic_orchestrator.py]] - degree 14, connects to 4 communities
- [[_analysis()]] - degree 4, connects to 2 communities
- [[TestRunSyntaxVerificationPaths]] - degree 10, connects to 1 community
- [[TestApplyWorkerOutputsPaths]] - degree 9, connects to 1 community