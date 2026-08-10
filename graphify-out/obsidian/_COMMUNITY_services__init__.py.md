---
type: community
cohesion: 0.09
members: 37
---

# services/__init__.py

**Cohesion:** 0.09 - loosely connected
**Members:** 37 nodes

## Members
- [[Force cold-path promotion without running full orchestrator.]] - rationale - src/merged_agentic_swarm/tools/agentic_cli.py
- [[List named swarm profiles or resolve one into a runnable orchestrator plan.]] - rationale - src/merged_agentic_swarm/tools/agentic_cli.py
- [[Load all swarm profiles (cached); fall back to the code-side dict when missing.]] - rationale - src/merged_agentic_swarm/services/swarm_profiles.py
- [[Merged Agentic Swarm — CLI Entry Point Provides run, status, promote, config,…]] - rationale - src/merged_agentic_swarm/tools/agentic_cli.py
- [[Model Role Routing Resolves a worker role (deep  main  fast tier, or a…]] - rationale - src/merged_agentic_swarm/services/model_routing.py
- [[Render a live progress-ledger snapshot (logs + success markers + task-master…]] - rationale - src/merged_agentic_swarm/tools/agentic_cli.py
- [[Render an older progress.json snapshot (kept so ``--progress`` still works on…]] - rationale - src/merged_agentic_swarm/tools/agentic_cli.py
- [[Resolve the live progress ledger path (default source for ``cmd_status``).]] - rationale - src/merged_agentic_swarm/tools/agentic_cli.py
- [[Return {name, description} entries for every known profile, name-sorted.]] - rationale - src/merged_agentic_swarm/services/swarm_profiles.py
- [[Return the first litellm model in the fabric route list for a model alias.]] - rationale - src/merged_agentic_swarm/services/model_routing.py
- [[Return the litellm virtual Gemini alias for a worker role. Resolution order 1.…]] - rationale - src/merged_agentic_swarm/services/model_routing.py
- [[Return the profile's model alias, or resolve via model_routing when absent.…]] - rationale - src/merged_agentic_swarm/services/swarm_profiles.py
- [[Return the resolved profile dict for a name; raise KeyError for unknown names.]] - rationale - src/merged_agentic_swarm/services/swarm_profiles.py
- [[Run the full orchestrator workflow.]] - rationale - src/merged_agentic_swarm/tools/agentic_cli.py
- [[Services Package Initialization]] - rationale - src/merged_agentic_swarm/services/__init__.py
- [[Show a provider + proxy inventory key pools, fabric routes, registry backends.]] - rationale - src/merged_agentic_swarm/tools/agentic_cli.py
- [[Show current system status from the live progress ledger.]] - rationale - src/merged_agentic_swarm/tools/agentic_cli.py
- [[Swarm Profile Service Named, slash-command-style presets for pushing a large…]] - rationale - src/merged_agentic_swarm/services/swarm_profiles.py
- [[_progress_ledger_path()]] - code - src/merged_agentic_swarm/tools/agentic_cli.py
- [[_render_ledger_status()]] - code - src/merged_agentic_swarm/tools/agentic_cli.py
- [[_render_legacy_snapshot()]] - code - src/merged_agentic_swarm/tools/agentic_cli.py
- [[agentic_cli.py]] - code - src/merged_agentic_swarm/tools/agentic_cli.py
- [[cmd_promote()]] - code - src/merged_agentic_swarm/tools/agentic_cli.py
- [[cmd_providers()]] - code - src/merged_agentic_swarm/tools/agentic_cli.py
- [[cmd_run()]] - code - src/merged_agentic_swarm/tools/agentic_cli.py
- [[cmd_status()]] - code - src/merged_agentic_swarm/tools/agentic_cli.py
- [[cmd_swarm()]] - code - src/merged_agentic_swarm/tools/agentic_cli.py
- [[list_profiles()]] - code - src/merged_agentic_swarm/services/swarm_profiles.py
- [[litellm_model_for_fabric_route()]] - code - src/merged_agentic_swarm/services/model_routing.py
- [[load_profiles()]] - code - src/merged_agentic_swarm/services/swarm_profiles.py
- [[main()_6]] - code - src/merged_agentic_swarm/tools/agentic_cli.py
- [[model_routing.py]] - code - src/merged_agentic_swarm/services/model_routing.py
- [[resolve_litellm_model_for_role()]] - code - src/merged_agentic_swarm/services/model_routing.py
- [[resolve_model_alias_for_profile()]] - code - src/merged_agentic_swarm/services/swarm_profiles.py
- [[resolve_profile()]] - code - src/merged_agentic_swarm/services/swarm_profiles.py
- [[services__init__.py]] - code - src/merged_agentic_swarm/services/__init__.py
- [[swarm_profiles.py]] - code - src/merged_agentic_swarm/services/swarm_profiles.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/services/__init__py
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_webapp.py]]
- 6 edges to [[_COMMUNITY_report_service.py]]
- 5 edges to [[_COMMUNITY__load_registry]]
- 4 edges to [[_COMMUNITY_WorkerRole]]
- 4 edges to [[_COMMUNITY_CloudCLIClient]]
- 3 edges to [[_COMMUNITY_SubTask]]
- 3 edges to [[_COMMUNITY_test_agentic_cli.py]]
- 3 edges to [[_COMMUNITY_cmd_config]]
- 3 edges to [[_COMMUNITY_MultiLayeredAgenticOrchestrator]]
- 2 edges to [[_COMMUNITY_OpenCodeSwarmManager]]
- 2 edges to [[_COMMUNITY_test_webapp.py]]
- 2 edges to [[_COMMUNITY_handle_run]]
- 2 edges to [[_COMMUNITY_TestCLIStringFunctions]]
- 1 edge to [[_COMMUNITY_WorkerPoolConfig]]
- 1 edge to [[_COMMUNITY_ChainRegistry]]
- 1 edge to [[_COMMUNITY_DurableAgentFactory]]
- 1 edge to [[_COMMUNITY_CodebaseMapService]]
- 1 edge to [[_COMMUNITY_ProgressLogEntry]]
- 1 edge to [[_COMMUNITY_ObstaclePlaybookEngine]]
- 1 edge to [[_COMMUNITY_ProgressLedgerService]]
- 1 edge to [[_COMMUNITY_TaskMasterService]]
- 1 edge to [[_COMMUNITY_WaveGateController]]
- 1 edge to [[_COMMUNITY_test_report_service.py]]
- 1 edge to [[_COMMUNITY_TestResolveLitellmModelForRole]]
- 1 edge to [[_COMMUNITY_DurableAgentRouter]]
- 1 edge to [[_COMMUNITY_test_swarm_profiles.py]]

## Top bridge nodes
- [[services__init__.py]] - degree 32, connects to 16 communities
- [[agentic_cli.py]] - degree 21, connects to 5 communities
- [[model_routing.py]] - degree 11, connects to 5 communities
- [[resolve_model_alias_for_profile()]] - degree 11, connects to 3 communities
- [[main()_6]] - degree 10, connects to 3 communities