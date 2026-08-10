# Graph Report - merged-agentic-swarm  (2026-08-10)

## Corpus Check
- 207 files · ~199,767 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2839 nodes · 4968 edges · 217 communities (156 shown, 61 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 625 edges (avg confidence: 0.58)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `446e11e7`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- TaskSpineStore
- AgenticWorkerLoop
- LatencyTracker
- CloudCLIClient
- webapp.py
- _router_with_keys
- Ultraswarm Run Failure Report — 2026-08-10
- WorkerRole
- SubTask
- WaveExecutionState
- CodebaseMapService
- DurableAgentFactory
- LiteLLM Gateway
- ProxyChainHealth
- DurableAgentRouter
- resolve_model_alias_for_profile
- .run_full_agentic_workflow
- fast_pool.py
- Graphify
- FastFallbackRouter
- TaskMasterService
- TestClaudeProxyHandler
- KeyPoolManager
- test_streaming_proxy.py
- MultiLayeredAgenticOrchestrator
- OpenCodeSwarmManager
- conftest.py
- opencode.json
- HopResult
- test_agentic_cli.py
- TestResolveLitellmModelForRole
- KnowledgeCache
- test_swarm_profiles.py
- What You Must Do When Invoked
- What You Must Do When Invoked
- What You Must Do When Invoked
- TestWaveGateController
- TestTokenSavior
- TestWaveGatesWithRealState
- ProgressLogEntry
- MultiProviderFabric
- agentic_cli.py
- swarm_run.py
- run_smoke_workflow.sh
- test_health_check.py
- APIKeyInfo
- Request
- _evaluate_promotion_criteria
- _make_learning_entry
- TestDispatchRequest
- test_learning_loop.py
- PassthroughStreamingProxy
- ProgressLedgerService
- TestRunFullAgenticWorkflow
- FastFallbackConfig
- generate_progress_report.sh
- verify_component.sh
- AgentSpec
- ConcurrencyRampController
- _read_jsonl
- ProxyServerDaemon
- test_report_service.py
- graphify-out/graph.json
- Task Spine CLI
- multi_provider_fabric.py
- ClaudeProxyHandler
- _simulate_reuse
- TestFormatConversion
- task_spine_cli.py
- _record_failure
- CircuitBreaker
- .run_all
- _forward_transcription
- ObstaclePlaybookEngine
- test_multi_provider_fabric.py
- DurableAgentRouter
- Real task-master CLI
- WaveGateController
- create_app
- handle_chain_update
- TestRun
- test_webapp.py
- StreamingProxyConfig
- TestChains
- transcribe_all
- graphify export and benchmark reference
- Graphify CLI
- Incremental Update Process
- Merge
- Incremental Update Flow
- graphify reference: extra exports and benchmark
- graphify reference: extra exports and benchmark
- graphify reference: extra exports and benchmark
- dynamic_learning_loop
- project
- services/__init__.py
- start_task_spine.sh
- model_routing.py
- Any
- ingest
- Extraction Rules
- handle_latency_test
- orchestrator
- role_allocations
- run_learning_loop_test.sh
- start_proxy.sh
- verify_task_spine.sh
- handle_profile_update
- .handle_task_failure
- test_check_streaming_fcc_happy_path
- query, path, and explain reference
- knowledge.jsonl
- CI Script
- CI test job
- check_proxy_health.sh
- graphify-obsidian-sync.sh
- _ChunkStream
- _StallStream
- graphify reference: query, path, explain
- graphify reference: query, path, explain
- Answer
- graphify reference: query, path, explain
- opencode-swarm.json
- verify_worker_runtime.sh
- handle_run_status
- TestCaptureStep
- TestLatencyTest
- TestReports
- graphify.serve module
- graphify add command
- MultiLayeredAgenticOrchestrator
- promotion_policy
- package.json
- load_durable_agents.sh
- start_worker_runtime.sh
- stop_agentic_services.sh
- TestCmdProviders
- TestRunPlan
- graphify extract
- graphify reference: incremental update and cluster-only
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- Agent Markdown File
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- phase_gates
- retry_policy
- discover_environment.sh
- verify_proxy.sh
- TestModelRoleUpdate
- BFS/DFS Graph Traversal
- graphify Skill Spec
- GitHub clone and cross-repo merge reference
- commit hook and CLAUDE.md integration reference
- Agentic Codebase Optimization PRD (Canonical TXT)
- graphify reference: transcribe video and audio
- Add and Watch Reference
- graphify reference: GitHub clone and cross-repo merge
- graphify reference: transcribe video and audio
- graphify reference: GitHub clone and cross-repo merge
- graphify reference: transcribe video and audio
- Windows CI Job
- setup-and-run.sh Script
- graphify.js
- graphify reference: GitHub clone and cross-repo merge
- graphify reference: transcribe video and audio
- ci.sh
- setup-and-run.sh
- detect
- transcribe video and audio reference
- rules/graphify.md
- workflows/graphify.md
- graphify benchmark
- git diff HEAD~1
- .copilot/skills/graphify/references/extraction-spec.md
- GEMINI.md
- .gemini/skills/graphify/references/extraction-spec.md
- Merged Agentic Swarm Blueprint
- .opencode/skills/graphify/references/extraction-spec.md
- Ready-to-Say Swarm Prompts
- Spotify AI Analytics
- graphify export graphml
- graphify export svg
- Graphify Reference
- graphify claude
- Hooks Reference
- Query Reference
- Update Reference
- Agent Spec Contract
- Baseline Audit
- Learning Loop Verification Report
- Worker Runtime Verification Report
- Ultra-Scale Execution Completion Report
- Comprehensive Blueprint-vs-Reality Audit
- Phase 5 Improvement Recommendations
- Operator Runbook
- Execution-Ready PRD v2
- Progress Report
- Operator Runbook
- Ultra-Scale Workflow Plan: 40+ Agents
- Ultracode Fleet Manifest
- Stack Analysis 2026-08-06
- Merged Agentic Swarm PRD
- FCC Gateway
- CI security job
- Merged Agentic Swarm Blueprint
- task-master-mcp.json Spec
- graphify Skill
- Team Onboarding Guide
- merged-agentic-swarm
- Setup and Run Script

## God Nodes (most connected - your core abstractions)
1. `KeyPoolManager` - 61 edges
2. `SubTask` - 55 edges
3. `MultiLayeredAgenticOrchestrator` - 52 edges
4. `MultiProviderFabric` - 47 edges
5. `AgentSpec` - 46 edges
6. `WorkerRole` - 42 edges
7. `TaskMasterService` - 38 edges
8. `PRDAnalysisResult` - 34 edges
9. `KnowledgeCache` - 34 edges
10. `CodebaseMapService` - 33 edges

## Surprising Connections (you probably didn't know these)
- `_spawn_agentic_run()` --indirect_call--> `_runner()`  [INFERRED]
  src/merged_agentic_swarm/webapp.py → scripts/swarm_run.py
- `TestCircuitBreaker` --uses--> `FastFallbackConfig`  [INFERRED]
  tests/test_fast_fallback.py → src/merged_agentic_swarm/fast_fallback.py
- `TestDispatchBehavior` --uses--> `FastFallbackConfig`  [INFERRED]
  tests/test_fast_fallback.py → src/merged_agentic_swarm/fast_fallback.py
- `TestParallelProbe` --uses--> `FastFallbackConfig`  [INFERRED]
  tests/test_fast_fallback.py → src/merged_agentic_swarm/fast_fallback.py
- `TestAdaptiveSelection` --uses--> `FastFallbackRouter`  [INFERRED]
  tests/test_fast_fallback.py → src/merged_agentic_swarm/fast_fallback.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **System Verification Audit Suite** — docs_agentic_audit_baseline_audit, docs_agentic_audit_learning_loop_verification, docs_agentic_audit_worker_runtime_verification [EXTRACTED 1.00]
- **Agentic Swarm Architecture** — claude_code, task_master, opencode, claude_code_proxy [EXTRACTED 1.00]
- **Swarm Architecture Core Documentation** — merged_agentic_swarm_blueprint_md_operating_system, readme_md_overview, prompts_md_ready_prompts, sessions_report_md_audit [EXTRACTED 0.95]
- **Graphify Pipeline Steps** — agents_skills_graphify_skill_detect, agents_skills_graphify_skill_ast_extraction, agents_skills_graphify_skill_semantic_extraction, agents_skills_graphify_skill_graphify_out [EXTRACTED 1.00]
- **Graph Build Pipeline** — agents_skills_graphify_skill_build_from_json, agents_skills_graphify_skill_cluster, agents_skills_graphify_skill_score_all, agents_skills_graphify_skill_god_nodes, agents_skills_graphify_skill_surprising_connections, agents_skills_graphify_skill_suggest_questions, agents_skills_graphify_skill_generate, agents_skills_graphify_skill_to_json [EXTRACTED 1.00]
- **Graph Health Check** — agents_skills_graphify_skill_diagnose_extraction, agents_skills_graphify_skill_format_diagnostic_report [EXTRACTED 1.00]
- **Manifest Management** — agents_skills_graphify_skill_save_manifest, agents_skills_graphify_skill_stamped_manifest_files, agents_skills_graphify_skill_save_semantic_cache [EXTRACTED 1.00]
- **URL ingestion flow** — agents_skills_graphify_references_add_watch_ingest, agents_skills_graphify_references_add_watch_ytdlp, agents_skills_graphify_references_add_watch_oembed, agents_skills_graphify_references_add_watch_html2text, agents_skills_graphify_references_add_watch_claude_vision [EXTRACTED 0.90]
- **Graphify export commands** — agents_skills_graphify_references_exports_graphify_export_wiki, agents_skills_graphify_references_exports_graphify_export_neo4j, agents_skills_graphify_references_exports_graphify_export_falkordb, agents_skills_graphify_references_exports_graphify_export_svg, agents_skills_graphify_references_exports_graphify_export_graphml [EXTRACTED 1.00]
- **MCP server setup flow** — agents_skills_graphify_references_exports_graphify_serve, agents_skills_graphify_references_exports_graphify_out_graph_json, agents_skills_graphify_references_exports_mcp_server, agents_skills_graphify_references_exports_claude_desktop_config, agents_skills_graphify_references_exports_graphify_out_graphify_python [EXTRACTED 1.00]
- **Token reduction benchmark flow** — agents_skills_graphify_references_exports_graphify_benchmark, agents_skills_graphify_references_exports_graphify_out_graphify_detect [EXTRACTED 1.00]
- **Graphify CLI Workflow** — agents_skills_graphify_references_github_and_merge_clone, agents_skills_graphify_references_github_and_merge_extract, agents_skills_graphify_references_github_and_merge_merge_graphs, agents_skills_graphify_references_github_and_merge_query [EXTRACTED 0.95]
- **Graphify Auto-Integration** — agents_skills_graphify_references_hooks_hook, agents_skills_graphify_references_hooks_agents, agents_skills_graphify_references_hooks_agents_md, agents_skills_graphify_references_hooks_graph_report_md [EXTRACTED 0.90]
- **Video Transcription Flow** — _agents_skills_graphify_references_transcribe_detect, _agents_skills_graphify_references_transcribe_graphify_detect_json, _agents_skills_graphify_references_transcribe_transcribe_all, _agents_skills_graphify_references_transcribe_whisper, _agents_skills_graphify_references_transcribe_graphify_transcripts_json [EXTRACTED 1.00]
- **Incremental Update Pipeline** — agents_skills_graphify_references_update_detect_incremental, agents_skills_graphify_references_update_build_merge, agents_skills_graphify_references_update_save_manifest, agents_skills_graphify_references_update_graph_diff [EXTRACTED 0.95]
- **Cluster-Only Flow** — agents_skills_graphify_references_update_cluster_only_flow, agents_skills_graphify_references_update_build_merge [INFERRED 0.70]
- **Graphify add and watch flow** — claude_skills_graphify_references_add_watch_graphify_add, claude_skills_graphify_references_add_watch_watch_mode, graphify_ingest_ingest, graphify_watch_watch [INFERRED 0.75]
- **Graphify export steps flow** — claude_skills_graphify_references_exports_graphify_export_wiki, claude_skills_graphify_references_exports_graphify_export_neo4j, claude_skills_graphify_references_exports_graphify_export_falkordb, claude_skills_graphify_references_exports_graphify_export_svg, claude_skills_graphify_references_exports_graphify_export_graphml [EXTRACTED 1.00]
- **MCP server configuration** — claude_skills_graphify_references_exports_graphify_serve, claude_skills_graphify_references_exports_graphify_out_graph_json, claude_skills_graphify_references_exports_graphify_out_graphify_python, claude_skills_graphify_references_exports_claude_desktop_config [EXTRACTED 1.00]
- **Graph data artifacts** — claude_skills_graphify_references_exports_graphify_out_graph_json, claude_skills_graphify_references_exports_graphify_out_graphify_labels_json, claude_skills_graphify_references_exports_graphify_out_graphify_detect_json, claude_skills_graphify_references_exports_graphify_out_graphify_python [EXTRACTED 1.00]
- **Extraction Specification Components** — claude_skills_graphify_references_extraction_spec_extraction_rules, claude_skills_graphify_references_extraction_spec_confidence_scoring, claude_skills_graphify_references_extraction_spec_node_id_format, claude_skills_graphify_references_extraction_spec_source_file_rule, claude_skills_graphify_references_extraction_spec_hyperedge_guidance, claude_skills_graphify_references_extraction_spec_deep_mode, claude_skills_graphify_references_extraction_spec_json_schema [EXTRACTED 1.00]
- **Graphify Query Traversal Flow** — claude_skills_graphify_references_query_graphify_path, claude_skills_graphify_references_query_graphify_explain, claude_skills_graphify_references_query_networkx [EXTRACTED 1.00]
- **Graphify Self-Improvement Loop** — claude_skills_graphify_references_query_graphify_save_result, claude_skills_graphify_references_query_graphify_reflect, claude_skills_graphify_references_query_lessons [EXTRACTED 1.00]
- **Graphify Cross-Repo Merge Pipeline** — claude_skills_graphify_references_github_and_merge_graphify_clone, claude_skills_graphify_references_github_and_merge_graphify_extract, claude_skills_graphify_references_github_and_merge_graphify_merge_graphs, claude_skills_graphify_references_github_and_merge_graphify_out [EXTRACTED 1.00]
- **Incremental Update Flow** — claude_skills_graphify_references_update_detect_incremental, claude_skills_graphify_references_update_build_merge, claude_skills_graphify_references_update_save_manifest, claude_skills_graphify_references_update_graph_diff [EXTRACTED 1.00]
- **Export Formats Group** — graphify_export_wiki, graphify_export_neo4j, graphify_export_falkordb, graphify_export_svg, graphify_export_graphml, graphify_export_mcp [EXTRACTED 1.00]
- **Query Operations Group** — graphify_query, graphify_path, graphify_explain, graphify_save_result [EXTRACTED 1.00]
- **Integration Methods Group** — graphify_hook_install, graphify_claude_install, graphify_reflect [EXTRACTED 1.00]
- **Update Merge and Manifest Flow** — codex_skills_graphify_references_update_incremental_extraction, codex_skills_graphify_references_update_merge, codex_skills_graphify_references_update_manifest [INFERRED 0.80]
- **Core Agentic Swarm Components** — github_copilot_instructions_key_pool, github_copilot_instructions_task_master, github_copilot_instructions_wave_gate_controller, github_copilot_instructions_multi_layered_agentic_orchestrator [EXTRACTED 1.00]
- **Model Provider Endpoints** — github_copilot_instructions_fcc_gateway, github_copilot_instructions_cli_proxy_api, github_copilot_instructions_routatic_proxy [EXTRACTED 1.00]
- **CI Pipeline Steps** — github_workflows_arc_ci_actions_checkout, github_workflows_arc_ci_setup_uv, github_workflows_arc_ci_uv_sync, github_workflows_arc_ci_ci_script, github_workflows_arc_ci_docker [EXTRACTED 1.00]
- **Matrix runner import validation** — github_workflows_matrix_ci_cross_platform_check, github_workflows_matrix_ci_uv, github_workflows_matrix_ci_merged_agentic_swarm [EXTRACTED 1.00]
- **LiteLLM Gateway Model Set** — github_workflows_litellm_gateway, github_workflows_litellm_fast_flash, github_workflows_litellm_smart_auto, github_workflows_litellm_high_throughput [EXTRACTED 1.00]
- **OpenCode Workflow Shared Infrastructure** — github_workflows_opencode_review, github_workflows_opencode_scheduled, github_workflows_litellm_gateway, github_workflows_litellm_master_key, github_workflows_github_token [EXTRACTED 1.00]
- **OpenCode Provider Routing Modes** — github_workflows_opencode_fcc_proxy, github_workflows_opencode_claudeproxy, github_workflows_opencode_cloneclove, github_workflows_opencode_openrouter, github_workflows_opencode_anthropic [EXTRACTED 1.00]
- **Swarm Provider Pool** — github_workflows_swarm_run_litellm_proxy, github_workflows_swarm_run_gemini, github_workflows_swarm_run_cloudcli, github_workflows_swarm_run_nvidia_nim, github_workflows_swarm_run_mistral, github_workflows_swarm_run_opencode_api [EXTRACTED 1.00]
- **Model Discovery Gateways** — docs_vscode_copilot_kepler_model_discovery_fcc_server [EXTRACTED 1.00]
- **Model Fleet Consumers** — docs_vscode_copilot_kepler_model_discovery_vscode_copilot_chat, docs_vscode_copilot_kepler_model_discovery_kepler, docs_vscode_copilot_kepler_model_discovery_fcc_server [INFERRED 0.80]
- **Agent Spec Generation Flow** — docs_agentic_AGENT_SPEC_CONTRACT_cold_path_promotion, docs_agentic_AGENT_SPEC_CONTRACT_agents_jsonl, docs_agentic_AGENT_SPEC_CONTRACT_agent_md [EXTRACTED 1.00]
- **Knowledge Registry Integrity** — docs_agentic_knowledge_box_schema_knowledge_jsonl, docs_agentic_knowledge_box_schema_agents_jsonl, docs_agentic_knowledge_box_schema_chain_jsonl [EXTRACTED 1.00]
- **Durable Agent Routing Flow** — docs_agentic_audit_DURABLE_AGENT_ROUTING_VERIFICATION_execute_subtask_with_worker, docs_agentic_audit_DURABLE_AGENT_ROUTING_VERIFICATION_get_durable_router, docs_agentic_audit_DURABLE_AGENT_ROUTING_VERIFICATION_DurableAgentRouter, docs_agentic_audit_DURABLE_AGENT_ROUTING_VERIFICATION_find_matching_agent, docs_agentic_audit_DURABLE_AGENT_ROUTING_VERIFICATION_DurableRegexValidationSpecialist [EXTRACTED 1.00]
- **Proxy Verification Flow** — docs_agentic_audit_proxy_verification_verify_proxy_script, docs_agentic_audit_proxy_verification_claude_proxy_server, docs_agentic_audit_proxy_verification_multi_provider_fabric, docs_agentic_audit_proxy_verification_gemini_pool [EXTRACTED 0.95]
- **Task Spine Lifecycle** — docs_agentic_audit_task_spine_verification_task_spine_cli, docs_agentic_audit_task_spine_verification_task_master_service, docs_agentic_audit_task_spine_verification_tasks_json, docs_agentic_audit_task_spine_verification_evidence_directory [EXTRACTED 0.95]
- **State Path Reconciliation** — docs_agentic_registry_state_path_notes_task_master_cli, docs_agentic_registry_state_path_notes_task_master_service, docs_agentic_registry_state_path_notes_env, docs_agentic_registry_state_path_notes_blueprint [EXTRACTED 1.00]
- **Task Management Flow** — docs_agentic_registry_state_path_notes_task_master_service, docs_agentic_registry_state_path_notes_model_fabric, docs_agentic_registry_state_path_notes_python_proxy [EXTRACTED 1.00]
- **Graph Query Flow** — _agents_skills_graphify_references_query_traversal, _agents_skills_graphify_references_query_queryexpansion, _agents_skills_graphify_references_query_saveresult [EXTRACTED 1.00]

## Communities (217 total, 61 thin omitted)

### Community 0 - "TaskSpineStore"
Cohesion: 0.06
Nodes (23): _LockedScope, main(), _make_parser(), Any, ArgumentParser, Manages the local task spine JSON file with fcntl locking., Create the spine file if it does not exist. Idempotent., Create a new task. Idempotent on task_id. (+15 more)

### Community 1 - "AgenticWorkerLoop"
Cohesion: 0.06
Nodes (26): RuntimeError, AgenticWorkerLoop, _command_safety_error(), _extract_text(), Any, Agentic Worker Tool Loop Runs a real agentic loop over the multi-provider…, Return a refusal reason if ``command`` is unsafe, else None., Extract the assistant's text content from an Anthropic-shaped response. (+18 more)

### Community 2 - "LatencyTracker"
Cohesion: 0.05
Nodes (37): get_tracker(), LatencyTracker, _pct_stats(), percentile(), Per-request streaming latency tracking and provider health reporting. Tracks…, Record the first-byte (TTFB) moment. Idempotent per request., Time-to-first-byte in seconds, or None if no byte was received., Total request duration in seconds, or None if still in flight. (+29 more)

### Community 3 - "CloudCLIClient"
Cohesion: 0.07
Nodes (21): CloudCLIClient, CloudCLIConfig, CloudCLIError, Any, CloudCLI client — trigger remote AI agents via the cloneclove.com /api/agent…, Trigger a remote agent with streaming (SSE) and yield each event dict., Raised when CloudCLI returns a non-2xx response or is misconfigured., Minimal client for the CloudCLI agent API (``POST /api/agent``). (+13 more)

### Community 4 - "webapp.py"
Cohesion: 0.20
Nodes (13): _fabric_routes(), handle_reports_list(), handle_status(), _key_pool_snapshot(), _latest_report(), Agentic Swarm — Web UI Control Panel. A Starlette control panel (JSON API + a…, Provider -> {active, total, key_ids} — key_id list only, never values., MODEL_FABRIC_ROUTES as alias -> [{provider, model}] chains. (+5 more)

### Community 5 - "_router_with_keys"
Cohesion: 0.10
Nodes (26): _anthropic_response(), _mock_response(), patch, Tests for merged_agentic_swarm/fast_fallback.py Coverage: parallel probe first-…, Both wave probes fire concurrently; the first 2xx is returned., A failing primary overlaps the fallback's latency instead of serializing it., A losing in-flight probe (2xx after another probe won) must not corrupt state., With probe_stagger_ms, the primary's head-start lets it win even if slower. (+18 more)

### Community 6 - "Ultraswarm Run Failure Report — 2026-08-10"
Cohesion: 0.12
Nodes (16): 1. `chat-backend` — 3× timeout (exit code 143 = SIGTERM), 2. `chatbox-ui` + `expose-and-test` — BLOCKED, Immediate (this session), Log Paths, Long-term, Medium-term, Model Tier Misrouting, Preflight State (+8 more)

### Community 7 - "WorkerRole"
Cohesion: 0.06
Nodes (33): Run the agentic swarm orchestrator against spotify-ai project. Produces an…, Phase 5: Durable Learning Loop End-to-End Verification, AgentType, Enum, str, Agent, Worker Pool, and Spawn Chain Data Models, WorkerRole, Durable Agent Factory & Knowledge-Box -> Spawn Chain Registry Turns validated… (+25 more)

### Community 8 - "SubTask"
Cohesion: 0.09
Nodes (36): Models Package Initialization, EpicTask, PRDAnalysisResult, PRDDocument, Any, Enum, str, PRD and Task Master Data Models (+28 more)

### Community 9 - "WaveExecutionState"
Cohesion: 0.15
Nodes (13): int, Enum, str, Wave Gates Data Models, WaveExecutionState, WaveGateCriteria, WavePhase, WaveStatus (+5 more)

### Community 10 - "CodebaseMapService"
Cohesion: 0.08
Nodes (14): CodebaseMapService, Any, Scans workspace repository files and parses AST definitions., Parses Python file to extract top-level functions, classes, and imports., Cross-references required components against mapped codebase to find spec gaps.…, Load persisted codebase map state from disk., Persist codebase map state so restart doesn't require re-scan., Closes a specific spec gap after verifying fixes. (+6 more)

### Community 11 - "DurableAgentFactory"
Cohesion: 0.05
Nodes (25): ChainRegistry, DurableAgentFactory, Any, Remove and return count of expired HOT micro-specialists (FIX-09)., Resolve the durable cold-path agents registry (agents.jsonl). Prefers an…, Load durable agents from the cold-path agents.jsonl registry. Called once at…, Append a COLD_DURABLE agent record to the durable agents.jsonl registry.…, Write an agent spec .md file from a JSONL entry. Returns the file path, or None… (+17 more)

### Community 12 - "LiteLLM Gateway"
Cohesion: 0.07
Nodes (38): Claude Settings, Copilot Instructions, fcc-server, Kepler (GitKraken agent server), Model Fleet, OpenAI-Compatible Gateways, VSCode Copilot Chat, VSCode Settings (+30 more)

### Community 13 - "ProxyChainHealth"
Cohesion: 0.10
Nodes (38): HealthConfig, ProxyChainHealth, Runs reachability, streaming, and provider-status checks., Endpoints and request tuning for the health checks. Each field falls back to…, _patch_client(), check_opencode reports failure on HTTP 500 from upstream., check_opencode reports failure on connection errors., check_streaming reports unhealthy when no content_block_delta arrives. (+30 more)

### Community 14 - "DurableAgentRouter"
Cohesion: 0.08
Nodes (19): agents_registry_path(), Resolve the durable cold-path agents registry (agents.jsonl). Prefers an…, DurableAgentRouter, get_durable_router(), Any, Path, Extract YAML-style frontmatter between --- markers., Read the body content after frontmatter. (+11 more)

### Community 15 - "resolve_model_alias_for_profile"
Cohesion: 0.23
Nodes (11): load_profiles(), Swarm Profile Service Named, slash-command-style presets for pushing a large…, Load all swarm profiles (cached); fall back to the code-side dict when missing., Return the resolved profile dict for a name; raise KeyError for unknown names., Return the profile's model alias, or resolve via model_routing when absent.…, resolve_model_alias_for_profile(), resolve_profile(), handle_profiles() (+3 more)

### Community 16 - ".run_full_agentic_workflow"
Cohesion: 0.13
Nodes (11): _cancellation_check(), Any, Event, Deduplicate cold-path registries by content hash (knowledge) and ID…, Apply worker outputs to disk and count files written. Primary path: agentic-…, Return an aborted result if the run was cancelled, else None., Initializes Key Pool Proxy server and verifies service readiness., Return an abort result when a gate fails and gates are enforced.… (+3 more)

### Community 17 - "fast_pool.py"
Cohesion: 0.06
Nodes (41): Client, HTTPTransport, Limits, NetworkStream, _build_transport(), _CachedDNSBackend, close_thread_client(), _create_client() (+33 more)

### Community 18 - "Graphify"
Cohesion: 0.07
Nodes (34): AST extraction, build_from_json, check_semantic_cache, cluster, collect_files, detect, diagnose_extraction, exports (+26 more)

### Community 19 - "FastFallbackRouter"
Cohesion: 0.12
Nodes (18): dispatch_fast(), FastFallbackRouter, _ProbeContext, _ProbeResult, Any, Event, Fast Fallback Router — parallel-probe, minimal-latency fallback dispatch. Why…, Parallel-probe fallback router over the model fabric's route table.… (+10 more)

### Community 20 - "TaskMasterService"
Cohesion: 0.09
Nodes (10): Orchestrator wrapping the real Task Master AI spine. NOTE on state paths: -…, Updates task status in state and syncs to file., Saves Task Master state as the authoritative single source of truth., Rough complexity analysis: estimate turns based on task scope., TaskMasterService, Tests for services/task_master_service.py Coverage: TaskMasterService —…, Regression for #41: temp file must not be the fixed <target>.tmp., Concurrent save_state calls must never leave a torn JSON target. (+2 more)

### Community 21 - "TestClaudeProxyHandler"
Cohesion: 0.06
Nodes (15): #42: /status surfaces exhausted/cooldown/latency per provider., #35: a body over the JSON cap must be rejected before buffering., #35: a body under the cap still reaches normal processing (400 here)., #35: audio multipart bodies have their own (higher) cap., #33: FAST_FALLBACK_ENABLED routes through the hedged router., #33: without the flag the proxy keeps using the fabric dispatch path., POST /v1/messages should return a response (simulation fallback)., POST /v1/messages without an auth token → 401. (+7 more)

### Community 22 - "KeyPoolManager"
Cohesion: 0.10
Nodes (9): KeyPoolManager, Any, When every key is still cooling down, get_key returns None so the fabric…, Even with many keys, none may be reused while every one is cooling down., A key still cooling down must not be picked while another is active., #42: summary reports exhausted count, next cooldown expiry, avg latency., Getting a key from a provider that doesn't exist should not raise., TestKeyPoolManager (+1 more)

### Community 23 - "test_streaming_proxy.py"
Cohesion: 0.17
Nodes (30): asyncio, make_proxy(), make_request(), post(), Tests for ``merged_agentic_swarm.streaming_proxy``. Covers the zero-buffering…, Send one proxied request and return the proxy's Response., Each upstream network chunk must reach the client with identical boundaries —…, Proves no-buffering: the first chunk is yielded the instant the upstream writes… (+22 more)

### Community 24 - "MultiLayeredAgenticOrchestrator"
Cohesion: 0.12
Nodes (7): MultiLayeredAgenticOrchestrator, Append a JSON line to a JSONL registry., Cold-path: normalize hot cache entries → knowledge.jsonl → validated →…, Load previously promoted learning IDs so cold-path dedup survives restarts., When _write_agent_spec_file returns None (already exists), the skip branch logs…, Two categories promoted in one batch must produce distinct chain entry_ids…, TestRunSyntaxVerificationPaths

### Community 25 - "OpenCodeSwarmManager"
Cohesion: 0.07
Nodes (22): live, OpenCodeSwarmManager, Initializes the 40 worker specs across role allocations., Gets an available worker matching the specified role using round-robin…, Internal: must be called while holding self._worker_lock., Map a WorkerRole to a pool-health bucket key., make_subtask(), Factory fixture that returns a function to create SubTask instances. (+14 more)

### Community 26 - "conftest.py"
Cohesion: 0.09
Nodes (30): isolated_agent_factory(), isolated_chain_registry(), isolated_codebase_mapper(), isolated_fabric(), isolated_key_pool(), isolated_knowledge_cache(), isolated_progress_ledger(), isolated_swarm_manager() (+22 more)

### Community 27 - "opencode.json"
Cohesion: 0.08
Nodes (29): Claude Code, Claude Code Proxy, Deep Agentic Swarm Supervisor Brief, Merged Agentic Swarm Blueprint, Knowledge Box, limit, name, limit (+21 more)

### Community 28 - "HopResult"
Cohesion: 0.11
Nodes (28): Namespace, _build_parser(), HopResult, main(), _print_header(), _print_human(), Any, ArgumentParser (+20 more)

### Community 29 - "test_agentic_cli.py"
Cohesion: 0.07
Nodes (21): _args(), _fake_saved(), _ledger_json(), _ledger_log(), _main_with_args(), _patch_auto_save(), Tests for tools/agentic_cli.py Coverage: cmd_config, basic CLI parsing, cmd_run…, `run --profile review` resolves the profile's waves as the ramp and the tier-… (+13 more)

### Community 30 - "TestResolveLitellmModelForRole"
Cohesion: 0.07
Nodes (8): Tests for services/model_routing.py Coverage: role -> litellm alias resolution,…, The on-disk registry must parse and carry a consistent role_routing section., Live resolution should match the tier aliases in the registry file., reload_registry() clears the cache so an updated registry file is seen., TestLitellmModelForFabricRoute, TestRegistryFile, TestReloadRegistry, TestResolveLitellmModelForRole

### Community 31 - "KnowledgeCache"
Cohesion: 0.11
Nodes (8): KnowledgeCache, Any, Tests for tools/knowledge_cache.py Coverage: KnowledgeCache — load_cache,…, Learning with TTL should be expired and not returned., Pre-populate cache file with duplicate entries, verify compaction on load., TestKnowledgeCache, Step 2: RECORD — Write to hot cache (knowledge_cache.json)., TestRecordStep

### Community 32 - "test_swarm_profiles.py"
Cohesion: 0.08
Nodes (11): _fresh_cache(), fixture, Tests for services/swarm_profiles.py Coverage: load_profiles reads the JSON and…, The on-disk profiles file must parse and carry the documented fields., Each test starts (and ends) with an empty profile cache., A fallback load must not poison later loads once the real file returns., TestListProfiles, TestLoadProfiles (+3 more)

### Community 33 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 34 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 35 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 36 - "TestWaveGateController"
Cohesion: 0.08
Nodes (10): Subtasks producing output within owned paths should have no violations., #36: absent ownership map is an optional gate — warn and pass., Map exists but the requested pool is absent — keep the hard-fail., Wave 1 fails because task master has no tasks for it., Wave 2 gate should evaluate with task_master data., Wave 3 gate should evaluate with task_master data and ownership., Wave 0 should pass when there are no unresolved spec gaps., advance_wave should move from wave 0 to wave 1 if gate criteria pass. (+2 more)

### Community 37 - "TestTokenSavior"
Cohesion: 0.10
Nodes (7): Token Savior & Context Compactor Optimizes context window consumption via…, Removes blank lines and excessive indentation spaces to save tokens., Filters noisy bash logs and retains error tracebacks + summary lines., Compresses assistant prose (Caveman mode) by removing pleasantries, hedging,…, TokenSavior, Tests for tools/token_savior.py Coverage: TokenSavior — compact_code_snippet,…, TestTokenSavior

### Community 38 - "TestWaveGatesWithRealState"
Cohesion: 0.20
Nodes (7): _ownership_map(), Tests for services/wave_gate_service.py Coverage: WaveGateController —…, Attach real epics (wave 1) with subtasks carrying output artifacts., Attach real wave-3 epics whose subtasks output src/ artifacts., Wave 3 must not pass on statuses alone — verification must have run., Inline syntax fallback (no tests_ran) must not satisfy tests_passing., TestWaveGatesWithRealState

### Community 39 - "ProgressLogEntry"
Cohesion: 0.18
Nodes (10): ObstaclePlaybookEntry, ProgressLogEntry, Any, SuccessMarker, TaskMasterStateSnapshot, Tests for models/ledger_models.py Coverage: SuccessMarker,…, TestObstaclePlaybookEntry, TestProgressLogEntry (+2 more)

### Community 40 - "MultiProviderFabric"
Cohesion: 0.12
Nodes (14): _load_fabric_routes_overlay(), MultiProviderFabric, Any, Load the per-alias route overlay (cached); {} when missing or unreadable., Flatten Anthropic content blocks (or plain text) into a single text string., Convert normalized messages (Anthropic-shaped) to OpenAI Chat Completions…, Normalize a content value into a list of Anthropic content blocks., Convert normalized messages to Anthropic Messages API format. Used for… (+6 more)

### Community 41 - "agentic_cli.py"
Cohesion: 0.06
Nodes (52): _build_epics(), _build_gates(), build_run_report(), _build_timeline(), _build_waves(), _format_ts(), Any, Path (+44 more)

### Community 42 - "swarm_run.py"
Cohesion: 0.29
Nodes (21): CompletedProcess, build_tasks(), discover_modules(), fetch_issues(), _issue_risk(), latest_run_id(), main(), make_docs_task() (+13 more)

### Community 43 - "run_smoke_workflow.sh"
Cohesion: 0.17
Nodes (15): fail(), info(), main(), pass(), preflight(), print_summary(), refresh_progress_report(), run_step() (+7 more)

### Community 44 - "test_health_check.py"
Cohesion: 0.10
Nodes (19): _make_sse_response(), Response, Return a 200 httpx.Response whose .stream yields SSE events., from_env returns defaults when no env vars are set., from_env picks up env overrides for string fields., from_env casts numeric env vars to int/float., from_env surfaces ValueError for non-numeric env values (no silent fallback)., --json flag emits machine-readable JSON for all checks. (+11 more)

### Community 45 - "APIKeyInfo"
Cohesion: 0.11
Nodes (9): APIKeyInfo, Loads API keys from env file, environment variables, and local key files., Hot-reload keys from all sources, preserving runtime stats for persistent keys.…, Gets an active API key using round-robin / least-used strategy., Internal: must be called while holding self._lock., Avoid leaking the secret value in logs/debug output., Gather (provider, secret_value, key_id) candidates from all key sources.…, Tests for providers/key_pool.py Coverage: APIKeyInfo, KeyPoolManager… (+1 more)

### Community 46 - "Request"
Cohesion: 0.16
Nodes (17): HTMLResponse, JSONResponse, _clean_expired_sessions(), handle_chat(), handle_chat_session(), handle_chat_sessions(), handle_dashboard(), handle_report_detail() (+9 more)

### Community 47 - "_evaluate_promotion_criteria"
Cohesion: 0.20
Nodes (9): _append_jsonl(), _evaluate_promotion_criteria(), Step 3: EVALUATE — Score learning against promotion criteria., A strong, substantive entry should pass all promotion criteria., A weak entry should fail promotion criteria., Should detect when an entry already exists in cold knowledge., Append a single JSON entry as a line to a JSONL file., Evaluate whether a learning entry meets cold-path promotion criteria. Returns… (+1 more)

### Community 48 - "_make_learning_entry"
Cohesion: 0.18
Nodes (10): _make_learning_entry(), _promote_learning(), Execute cold-path promotion: write all 5 output files. Returns dict with paths…, Create a learning entry dict matching the knowledge_cache schema., Step 4: PROMOTE — Write all 5 cold-path artifacts., Dedup: identical learning should not produce duplicate agent., Verify that content-hash-based dedup catches semantically identical entries., Entries with different content should not collide. (+2 more)

### Community 49 - "TestDispatchRequest"
Cohesion: 0.13
Nodes (11): patch, Block all real providers so dispatch falls to simulation., Without any working providers, should fall through to simulation., Test that content blocks (list) are flattened correctly before dispatch., Test a successful API call returns formatted Anthropic response., A 2xx with a non-dict JSON body must cascade, not crash on .get()., A 2xx with an empty/non-JSON body must cascade, not raise JSONDecodeError., 4xx/5xx from dispatch() must be caught by HTTPStatusError handling. (+3 more)

### Community 50 - "test_learning_loop.py"
Cohesion: 0.20
Nodes (9): _make_agent_jsonl_entry(), _make_chain_jsonl_entry(), _make_knowledge_jsonl_entry(), Tests for the full learning loop lifecycle: capture -> evaluate -> promote ->…, Create a cold-path knowledge.jsonl entry., Create a cold-path agents.jsonl entry., Step: LOAD — Simulate loading agents after a restart., Create a cold-path chain.jsonl entry. (+1 more)

### Community 51 - "PassthroughStreamingProxy"
Cohesion: 0.15
Nodes (12): Route, PassthroughStreamingProxy, AsyncClient, Request, Response, Zero-buffering SSE passthrough proxy. Accepts Anthropic Messages API streaming…, Return the shared httpx client, creating it if needed., Close the underlying httpx client and release connections. (+4 more)

### Community 52 - "ProgressLedgerService"
Cohesion: 0.17
Nodes (5): ProgressLedgerService, Regression for #41: temp file must not be the fixed <target>.tmp., Concurrent save_ledger calls must never leave a torn JSON target., TestProgressLedgerService, TestLogProgressModelArg

### Community 53 - "TestRunFullAgenticWorkflow"
Cohesion: 0.16
Nodes (8): gates=False keeps advance_wave() running (state advances) but a non-passing…, A run emits proxy_deployed (after init) and run_deployed (pre-wave)…, Each wave threads its wave number as wave_gate_level so the swarm executes at…, A provided ramp_sequence reaches every swarm batch, default_model is recorded…, Without a profile, the swarm batch gets no ramp_sequence kwarg and the ledger…, #32: a set cancel_event makes the workflow return an aborted result., Wire the orchestrator singletons for a deterministic workflow run., TestRunFullAgenticWorkflow

### Community 54 - "FastFallbackConfig"
Cohesion: 0.11
Nodes (11): dict, FastFallbackConfig, Build a config from ``FAST_FALLBACK_*`` environment variables., Tunables for the fast-fallback router (dataclass defaults + env overrides)., A fallback with strong latency history outranks a slow primary., No latency history → static verified-first order is untouched., A perma-banned provider does not appear in the candidate list., dispatch_fast reaches the default router and returns an Anthropic-shaped… (+3 more)

### Community 55 - "generate_progress_report.sh"
Cohesion: 0.12
Nodes (5): count_files(), durable_agent_count(), generate_evidence_table(), generate_report(), generate_progress_report.sh script

### Community 56 - "verify_component.sh"
Cohesion: 0.22
Nodes (15): CHECK_COMMANDS, CHECK_DETAILS, CHECK_EXIT_CODES, check_git(), CHECK_NAMES, check_node(), check_opencode(), check_proxy() (+7 more)

### Community 57 - "AgentSpec"
Cohesion: 0.07
Nodes (22): AgentSpec, Any, Increment the completed counter for the given pool., Increment the failed or rate_limited counter for the given pool., Return a copy of the pool_health dict., Return True if this agent has a TTL and has exceeded it., SpawnChainEntry, WorkerPoolConfig (+14 more)

### Community 58 - "ConcurrencyRampController"
Cohesion: 0.09
Nodes (9): ConcurrencyRampController, Controls worker concurrency ramp-up across wave gates., Map wave gate level to max workers. Gate 0 -> 4, gate 1 -> 8, gate 2 -> 16,…, Return the full ramp sequence., Resolve the working repo the swarm writes into. ``SWARM_TARGET_REPO`` env var…, Executes a batch of subtasks in parallel using ThreadPoolExecutor up to max…, When SWARM_TARGET_REPO is unset and no sibling target repo exists,…, TestConcurrencyRampController (+1 more)

### Community 59 - "_read_jsonl"
Cohesion: 0.24
Nodes (10): _load_agents_from_registry(), Verify all 5 cold-path artifacts exist and are valid. Returns list of failures., Simulate loading agents after restart: read agents.jsonl and .md files., End-to-end: capture -> record -> evaluate -> promote -> verify -> load -> route…, Run the complete lifecycle and verify every step., Read all JSONL entries from a file, returning a list of dicts., Promote multiple different learnings and verify they are all loadable., _read_jsonl() (+2 more)

### Community 60 - "ProxyServerDaemon"
Cohesion: 0.12
Nodes (11): HTTPServer, ProxyServerDaemon, Threaded HTTP server to handle concurrent requests., ThreadedHTTPServer, Proxy Package Initialization, fixture, ProxyServerDaemon should start and stop without error., Calling start() twice should not create a second server. (+3 more)

### Community 61 - "test_report_service.py"
Cohesion: 0.26
Nodes (8): _ledger(), _log(), Tests for services/report_service.py Coverage: build_run_report…, TestBuildRunReport, TestRenderMarkdown, TestSaveRunReport, _write_json(), _write_jsonl()

### Community 62 - "graphify-out/graph.json"
Cohesion: 0.17
Nodes (16): FalkorDB instance, graphify export falkordb, graphify export neo4j, graphify export wiki, Neo4j instance, claude_desktop_config.json, graphify export falkordb, graphify export graphml (+8 more)

### Community 63 - "Task Spine CLI"
Cohesion: 0.14
Nodes (16): Check Proxy Health Script, Claude Proxy Server, Claude Proxy Systemd Service, Fast Pool, Gemini Pool, Generate LiteLLM Config, LiteLLM Proxy, Model Fabric Routes (+8 more)

### Community 64 - "multi_provider_fabric.py"
Cohesion: 0.17
Nodes (11): Providers Package Initialization, KeyStatus, Enum, str, API Key Pool Manager & Key Rotator Supports multi-provider key rotation, quota…, _load_bans(), Multi-Backend Model Fabric Routes requests across providers with priority…, Load persisted perma-bans into _permanently_dead, dropping expired entries. (+3 more)

### Community 65 - "ClaudeProxyHandler"
Cohesion: 0.21
Nodes (7): BaseHTTPRequestHandler, ClaudeProxyHandler, _proxy_dispatch(), Any, Reject an oversized body. Close the connection since the unread bytes would…, Enforce the inbound proxy token (ANTHROPIC_AUTH_TOKEN, default 'freecc').…, Route a request through the hedged fast-fallback router when enabled. Both…

### Community 66 - "_simulate_reuse"
Cohesion: 0.40
Nodes (4): Simulate routing a task to a promoted agent and getting a response., Step: ROUTE & REUSE — Routing tasks to promoted agents., _simulate_reuse(), TestRouteAndReuse

### Community 67 - "TestFormatConversion"
Cohesion: 0.13
Nodes (3): format_anthropic_to_openai converts normalized tool_calls to OpenAI shape., format_anthropic_to_anthropic builds tool_use + tool_result blocks for…, TestFormatConversion

### Community 68 - "task_spine_cli.py"
Cohesion: 0.43
Nodes (13): cmd_attach_evidence(), cmd_block(), cmd_claim(), cmd_create(), cmd_inspect(), cmd_list(), cmd_restart_verify(), cmd_update() (+5 more)

### Community 69 - "_record_failure"
Cohesion: 0.18
Nodes (8): _persist_bans(), Atomically write the perma-ban map to disk. Caller must hold _fabric_lock., Record a provider failure — perma-ban on 401 auth errors, circuit-break on…, Record a provider success — reset circuit breaker and update last-working cache., _record_failure(), _record_success(), Provider should be retried after perma-ban duration expires., TestCircuitBreaker

### Community 70 - "CircuitBreaker"
Cohesion: 0.14
Nodes (8): CircuitBreaker, AsyncBaseTransport, Simple fail-fast circuit breaker. Tracks consecutive failures. After…, True when the circuit is open (requests should be rejected)., Current consecutive failure count., Reset the failure counter after a successful request., Increment the failure counter; open circuit if threshold reached., test_circuit_breaker_unit_transitions()

### Community 71 - ".run_all"
Cohesion: 0.21
Nodes (7): Probe routatic-proxy /health and surface circuit-breaker metrics., Probe the FCC gateway /health endpoint., Check upstream OpenCode API reachability (models endpoint)., Stream a tiny /v1/messages request and time first token + total. ``endpoint``…, Monitor provider/circuit-breaker status via routatic + FCC models list., Run every check; returns results in a stable order., _truncate()

### Community 72 - "_forward_transcription"
Cohesion: 0.11
Nodes (12): _forward_transcription(), _parse_multipart(), Forward a transcription request to the configured Whisper backend., Return (file_bytes, file_name, model_name) from a multipart body., _FakeResp, _multipart_body(), Tests for proxy/claude_proxy_server.py Coverage: ClaudeProxyHandler (do_GET,…, Multipart audio POST → forwarded to Whisper backend → JSON response. (+4 more)

### Community 73 - "ObstaclePlaybookEngine"
Cohesion: 0.17
Nodes (3): ObstaclePlaybookEngine, Tests for services/progress_ledger_service.py Coverage: ObstaclePlaybookEngine…, TestObstaclePlaybookEngine

### Community 74 - "test_multi_provider_fabric.py"
Cohesion: 0.09
Nodes (12): _isolated_bans_path(), fixture, Tests for providers/multi_provider_fabric.py Coverage:…, #40: 401 perma-bans persist to disk and are honored across reloads., Redirect the persisted-bans path so tests never write into the repo., Role routing maps worker roles to litellm aliases, so every fabric tier must…, Worker-tier aliases route through the litellm gateway FIRST (42-key Gemini…, Malformed overlay routes are dropped at load, never crashing dispatch (issue… (+4 more)

### Community 75 - "DurableAgentRouter"
Cohesion: 0.20
Nodes (11): DurableAgentRouter, Durable Regex Validation Specialist, _extract_keywords(text), _scan_agent_triggers(agent), Durable Agents, agents.jsonl registry, .claude/agents/*.md, execute_subtask_with_worker (+3 more)

### Community 76 - "Real task-master CLI"
Cohesion: 0.20
Nodes (12): Anthropic Messages API, Blueprint expectation, .env TASKMASTER_STATE_FILE, EpicTask/SubTask schema, fcc-server proxy, Model fabric (multi_provider_fabric.py), PERPLEXITY_API_KEY, Python proxy (port 8085) (+4 more)

### Community 77 - "WaveGateController"
Cohesion: 0.21
Nodes (7): Any, Record the Wave-3 verification outcome for the Zero-Defect gate. Accepts the…, Evaluates whether all criteria for a wave gate are met., Evaluate Wave 3's Zero-Defect verification criteria. Uses the results recorded…, Attempts to pass the current wave gate and advance to the next wave., Verify each subtask's output paths against the ownership map for pool_id.…, WaveGateController

### Community 78 - "create_app"
Cohesion: 0.18
Nodes (12): create_app(), _fetch_litellm_aliases(), handle_models(), main(), AsyncBaseTransport, AsyncClient, Starlette, Live litellm /v1/models aliases; on failure (aliases=[], note). (+4 more)

### Community 79 - "handle_chain_update"
Cohesion: 0.29
Nodes (8): _fabric_chains(), handle_chain_update(), handle_chains(), _load_fabric_overlay(), fabric-routes.json as {"routes": {alias: [route, …]}}; {} when absent., Merged fabric chain view: code MODEL_FABRIC_ROUTES overlaid per alias., Upsert one chain alias into fabric-routes.json atomically., _write_fabric_overlay()

### Community 80 - "TestRun"
Cohesion: 0.17
Nodes (3): #32: GET /api/run/status reports runs started by POST /api/run., #32: POST /api/run/{id}/cancel signals the workflow's cancel_event., TestRun

### Community 81 - "test_webapp.py"
Cohesion: 0.10
Nodes (7): merged-agentic-swarm — Agentic orchestration system with multi-provider fabric…, Tests for merged_agentic_swarm.webapp — the control-panel JSON API + dashboard.…, Async byte stream over fixed chunks for the mocked litellm SSE response., _Stream, TestModels, TestProfiles, TestStatus

### Community 82 - "StreamingProxyConfig"
Cohesion: 0.22
Nodes (9): create_streaming_proxy_app(), Starlette, Zero-buffering streaming passthrough proxy for Anthropic Messages API. Accepts…, Return a standalone Starlette ASGI application., Create a configured streaming proxy Starlette app in one call., Configuration for the zero-buffering streaming proxy., StreamingProxyConfig, test_config_defaults() (+1 more)

### Community 83 - "TestChains"
Cohesion: 0.18
Nodes (7): _fresh_caches(), fixture, Start each test with empty disk caches so patches don't leak across tests., Point webapp at a throwaway fabric-routes.json (never the real file)., Point swarm_profiles at a throwaway registry seeded with the on-disk profiles., TestChains, tmp_profiles_file()

### Community 84 - "transcribe_all"
Cohesion: 0.33
Nodes (10): .graphify_transcripts.json, transcribe_all, Whisper, .graphify_detect.json, .graphify_python, .graphify_transcripts.json, GRAPHIFY_WHISPER_MODEL, GRAPHIFY_WHISPER_PROMPT (+2 more)

### Community 85 - "graphify export and benchmark reference"
Cohesion: 0.20
Nodes (10): graphify export and benchmark reference, graphify benchmark, .graphify_detect.json file, Token Reduction Benchmark, FalkorDB Export Step, GraphML Export Step, MCP Server Export Step, Neo4j Export Step (+2 more)

### Community 86 - "Graphify CLI"
Cohesion: 0.27
Nodes (10): Clone Command, Extract Command, Graph JSON File, Merge Graphs Command, Query Command, Agents Command, AGENTS.md File, GRAPH_REPORT.md File (+2 more)

### Community 87 - "Incremental Update Process"
Cohesion: 0.22
Nodes (10): build_from_json, build_merge, Cluster-Only Process, detect_incremental, graph_diff, graphify CLI, Incremental Update Process, save_manifest (+2 more)

### Community 88 - "Merge"
Cohesion: 0.20
Nodes (10): build_from_json, build_merge, Cluster Only, detect_incremental, graph_diff, Incremental Extraction, Manifest, Merge (+2 more)

### Community 89 - "Incremental Update Flow"
Cohesion: 0.36
Nodes (9): build_from_json, build_merge, Cluster-Only Flow, detect_incremental, graph_diff, Incremental Update Flow, save_manifest, _stamped_manifest_files (+1 more)

### Community 90 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 91 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 92 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 93 - "dynamic_learning_loop"
Cohesion: 0.22
Nodes (9): dynamic_learning_loop, agent_registry, chain_registry, cold_registry, hot_cache, micro_spawn_policy, progress_report, max_lifespan_sec (+1 more)

### Community 94 - "project"
Cohesion: 0.22
Nodes (9): project, description, knowledge_graph_path, name, ownership_map, progress_report, provider_registry, root_dir (+1 more)

### Community 95 - "services/__init__.py"
Cohesion: 0.33
Nodes (3): Progress Ledger, Success Markers, and Obstacle Playbooks Models, Services Package Initialization, Progress Ledger, Success Markers, and Self-Healing Obstacle Playbook Engine…

### Community 96 - "start_task_spine.sh"
Cohesion: 0.36
Nodes (8): banner(), fail(), info(), ok(), start_task_spine.sh script, TASK_SPINE_STATE, TASK_SPINE_TYPE, warn()

### Community 97 - "model_routing.py"
Cohesion: 0.17
Nodes (15): litellm_model_for_fabric_route(), _load_registry(), Any, Model Role Routing Resolves a worker role (deep / main / fast tier, or a…, Return the first litellm model in the fabric route list for a model alias., Load the provider registry (cached); return {} when missing/unreadable., Clear the cached registry and reload it from disk. Called after the provider…, Return the litellm virtual Gemini alias for a worker role. Resolution order: 1.… (+7 more)

### Community 99 - "ingest"
Cohesion: 0.25
Nodes (8): Claude Vision, graph, html2text, ingest, oEmbed, update, watch, yt-dlp

### Community 100 - "Extraction Rules"
Cohesion: 0.64
Nodes (8): Confidence Scoring, Deep Mode, Extraction Rules, Extraction Subagent Prompt, Hyperedge Guidance, JSON Schema, Node ID Format, Source File Rule

### Community 101 - "handle_latency_test"
Cohesion: 0.33
Nodes (6): Exception, handle_latency_test(), _latency_error(), ok:false payload — short error, never the key., Stream one chat/completions request; report TTFB and total wall time., _run_latency_test()

### Community 102 - "orchestrator"
Cohesion: 0.25
Nodes (8): orchestrator, control_plane, heartbeat_interval_ms, max_concurrency, proxy_endpoint, ramp_sequence, runner, telemetry_enabled

### Community 103 - "role_allocations"
Cohesion: 0.25
Nodes (8): role_allocations, codebase_mapper, core_engineer, master_architect, refactor_specialist, security_verifier, spec_gap_closer, unit_tester

### Community 104 - "run_learning_loop_test.sh"
Cohesion: 0.39
Nodes (5): print_banner(), run_learning_loop_test.sh script, step_fail(), step_info(), step_pass()

### Community 105 - "start_proxy.sh"
Cohesion: 0.32
Nodes (7): check_proxy(), FCC_PORT, FCC_PROCESS_NAME, ROUTATIC_PORT, ROUTATIC_PROCESS_NAME, start_proxy.sh script, usage()

### Community 106 - "verify_task_spine.sh"
Cohesion: 0.39
Nodes (5): banner(), die(), verify_task_spine.sh script, step_fail(), step_ok()

### Community 107 - "handle_profile_update"
Cohesion: 0.67
Nodes (3): handle_profile_update(), Persist profiles to disk atomically and invalidate the load cache., _write_profiles()

### Community 108 - ".handle_task_failure"
Cohesion: 0.32
Nodes (3): Any, Processes a task failure through self-healing playbooks., Matches error against playbooks and applies self-healing strategy.

### Community 109 - "test_check_streaming_fcc_happy_path"
Cohesion: 0.25
Nodes (8): Build a single SSE data line for an Anthropic streaming content-block-delta., check_streaming through FCC endpoint measures TTFB and total latency., check_streaming targets routatic-proxy when endpoint='routatic'., stream' subcommand runs only the streaming check., _sse_event(), test_check_streaming_fcc_happy_path(), test_check_streaming_routatic_endpoint(), test_main_stream_subcommand()

### Community 110 - "query, path, and explain reference"
Cohesion: 0.33
Nodes (7): graphify extraction subagent prompt, query, path, and explain reference, Explain Node, Find Shortest Path, Query Graph, Reflect on Lessons, Save Result to Graph

### Community 111 - "knowledge.jsonl"
Cohesion: 0.29
Nodes (7): agents.jsonl, anomaly_detection, chain.jsonl, Knowledge Box Schema, knowledge.jsonl, manual, orchestrator_cold_path

### Community 112 - "CI Script"
Cohesion: 0.33
Nodes (7): CI Script, pyproject.toml, actions/checkout, CI Script, Docker, astral-sh/setup-uv, uv sync

### Community 113 - "CI test job"
Cohesion: 0.33
Nodes (7): Ruff lint and format check, Import-chain smoke script, CI test job, uv dependency sync, Cross-platform check job, merged_agentic_swarm import check, uv dependency sync (matrix)

### Community 114 - "check_proxy_health.sh"
Cohesion: 0.33
Nodes (6): HEALTH_URL, log(), LOG_FILE, SERVICE_NAME, check_proxy_health.sh script, TIMEOUT_SEC

### Community 116 - "_ChunkStream"
Cohesion: 0.29
Nodes (4): _ChunkStream, Async byte stream over a fixed list of chunks. Optionally raises ``exc`` after…, Build an upstream ``httpx.Response`` that streams ``chunks`` as SSE., _sse_response()

### Community 117 - "_StallStream"
Cohesion: 0.29
Nodes (4): drain(), Consume (or close) a StreamingResponse so upstream streams are torn down., Async byte stream that never yields (simulates a stalled upstream)., _StallStream

### Community 118 - "graphify reference: query, path, explain"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 119 - "graphify reference: query, path, explain"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 120 - "Answer"
Cohesion: 0.33
Nodes (5): Answer, KeyPoolManager, Outcome, Q: What is KeyPoolManager?, What is KeyPoolManager?

### Community 121 - "graphify reference: query, path, explain"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 122 - "opencode-swarm.json"
Cohesion: 0.33
Nodes (5): agent_pools, control_agents, phase_1_agents, $schema, version

### Community 123 - "verify_worker_runtime.sh"
Cohesion: 0.60
Nodes (5): die(), log(), verify_worker_runtime.sh script, usage(), VERIFY_RESULTS_FILE

### Community 124 - "handle_run_status"
Cohesion: 0.29
Nodes (7): handle_run_status(), Registry entry for a background workflow run., Start a real agentic workflow on a background daemon thread (returns now).…, Report live status for a run (or all runs when no ``run_id`` is given)., RunHandle, _serialize_run(), _spawn_agentic_run()

### Community 126 - "TestCaptureStep"
Cohesion: 0.33
Nodes (4): Step 1: CAPTURE — Create a controlled learning scenario., A captured learning scenario produces a properly structured entry., A generic/non-specific entry should be identifiable as weak., TestCaptureStep

### Community 130 - "graphify.serve module"
Cohesion: 0.50
Nodes (5): Claude Desktop config, graph.json file, .graphify_python file, graphify.serve module, MCP server

### Community 131 - "graphify add command"
Cohesion: 0.40
Nodes (5): graphify Skill, graphify add command, watch mode, ingest function, watch module

### Community 132 - "MultiLayeredAgenticOrchestrator"
Cohesion: 0.40
Nodes (5): KeyPool, MultiLayeredAgenticOrchestrator, TaskMaster, Ultraswarm Workers, WaveGateController

### Community 133 - "promotion_policy"
Cohesion: 0.40
Nodes (5): promotion_policy, require_claim, require_evidence, require_task_link, write_durable_agent

### Community 134 - "package.json"
Cohesion: 0.40
Nodes (4): name, private, scripts, test

### Community 136 - "start_worker_runtime.sh"
Cohesion: 0.70
Nodes (4): die(), log(), start_worker_runtime.sh script, usage()

### Community 137 - "stop_agentic_services.sh"
Cohesion: 0.70
Nodes (4): is_protected(), kill_worker(), main(), stop_agentic_services.sh script

### Community 144 - "graphify extract"
Cohesion: 0.50
Nodes (4): graphify clone, graphify extract, graphify merge-graphs, graphify-out directory

### Community 145 - "graphify reference: incremental update and cluster-only"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

### Community 146 - "graphify reference: add a URL and watch a folder"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 147 - "graphify reference: commit hook and native CLAUDE.md integration"
Cohesion: 0.50
Nodes (3): For git commit hook, For native CLAUDE.md integration, graphify reference: commit hook and native CLAUDE.md integration

### Community 148 - "graphify reference: incremental update and cluster-only"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

### Community 149 - "Agent Markdown File"
Cohesion: 0.50
Nodes (4): Agent Markdown File, agents.jsonl, Cold-Path Promotion, TTL (Time-to-Live)

### Community 150 - "graphify reference: add a URL and watch a folder"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 151 - "graphify reference: commit hook and native CLAUDE.md integration"
Cohesion: 0.50
Nodes (3): For git commit hook, For native CLAUDE.md integration, graphify reference: commit hook and native CLAUDE.md integration

### Community 152 - "graphify reference: incremental update and cluster-only"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

### Community 153 - "graphify reference: add a URL and watch a folder"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 154 - "graphify reference: commit hook and native CLAUDE.md integration"
Cohesion: 0.50
Nodes (3): For git commit hook, For native CLAUDE.md integration, graphify reference: commit hook and native CLAUDE.md integration

### Community 155 - "graphify reference: incremental update and cluster-only"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

### Community 156 - "phase_gates"
Cohesion: 0.50
Nodes (4): phase_gates, human_gate_before_full_concurrency, phase_1_required, phase_2_required

### Community 157 - "retry_policy"
Cohesion: 0.50
Nodes (4): retry_policy, backoff_factor, jitter, max_retries

### Community 158 - "discover_environment.sh"
Cohesion: 0.83
Nodes (3): critical_fail(), discover_environment.sh script, usage()

### Community 159 - "verify_proxy.sh"
Cohesion: 0.67
Nodes (3): check(), verify_proxy.sh script, TIERS

### Community 163 - "BFS/DFS Graph Traversal"
Cohesion: 0.67
Nodes (3): Constrained Query Expansion, Save-Result Feedback Loop, BFS/DFS Graph Traversal

### Community 164 - "graphify Skill Spec"
Cohesion: 0.67
Nodes (3): graphify Skill Spec, graphify Agent Rules, Claude Principles & Instructions

### Community 165 - "GitHub clone and cross-repo merge reference"
Cohesion: 0.67
Nodes (3): GitHub clone and cross-repo merge reference, Clone GitHub Repo, Merge Graphs

### Community 166 - "commit hook and CLAUDE.md integration reference"
Cohesion: 0.67
Nodes (3): commit hook and CLAUDE.md integration reference, Install CLAUDE.md Integration, Install Git Hook

### Community 167 - "Agentic Codebase Optimization PRD (Canonical TXT)"
Cohesion: 1.00
Nodes (3): Agentic Codebase Optimization PRD (Canonical TXT), Agentic Swarm Target Architecture, EPIC-00..05 Wave Plan

### Community 169 - "Add and Watch Reference"
Cohesion: 1.00
Nodes (3): Add and Watch Reference, ingest function, watch module

### Community 174 - "Windows CI Job"
Cohesion: 0.67
Nodes (3): Pytest, Ruff, Windows CI Job

### Community 175 - "setup-and-run.sh Script"
Cohesion: 0.67
Nodes (3): claude-code-proxy.json Spec, opencode-swarm.json Spec, setup-and-run.sh Script

## Ambiguous Edges - Review These
- `graphify export neo4j` → `.graphify_python`  [AMBIGUOUS]
  .claude/skills/graphify/references/exports.md · relation: references
- `graphify export falkordb` → `.graphify_python`  [AMBIGUOUS]
  .claude/skills/graphify/references/exports.md · relation: references

## Knowledge Gaps
- **392 isolated node(s):** `$schema`, `version`, `name`, `description`, `root_dir` (+387 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **61 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `graphify export neo4j` and `.graphify_python`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `graphify export falkordb` and `.graphify_python`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `create_app()` connect `create_app` to `model_routing.py`, `webapp.py`, `handle_latency_test`, `handle_profile_update`, `Request`, `handle_chain_update`, `resolve_model_alias_for_profile`, `PassthroughStreamingProxy`, `handle_run_status`?**
  _High betweenness centrality (0.093) - this node is a cross-community bridge._
- **Why does `PassthroughStreamingProxy` connect `PassthroughStreamingProxy` to `CircuitBreaker`, `StreamingProxyConfig`, `_ChunkStream`, `_StallStream`, `test_streaming_proxy.py`?**
  _High betweenness centrality (0.087) - this node is a cross-community bridge._
- **Why does `MultiLayeredAgenticOrchestrator` connect `MultiLayeredAgenticOrchestrator` to `TestLatencyTest`, `TestModelRoleUpdate`, `TestReports`, `webapp.py`, `WorkerRole`, `SubTask`, `agentic_cli.py`, `TestRunPlan`, `.run_full_agentic_workflow`, `handle_run_status`, `test_webapp.py`, `TestChains`, `TestRun`, `TestRunFullAgenticWorkflow`, `ProxyServerDaemon`?**
  _High betweenness centrality (0.078) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `KeyPoolManager` (e.g. with `isolated_key_pool()` and `TestCLIStringFunctions`) actually correct?**
  _`KeyPoolManager` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 29 inferred relationships involving `SubTask` (e.g. with `ConcurrencyRampController` and `DurableAgentRouter`) actually correct?**
  _`SubTask` has 29 INFERRED edges - model-reasoned connections that need verification._