# Graph Report - merged-agentic-swarm  (2026-08-09)

## Corpus Check
- 173 files · ~191,587 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2502 nodes · 4725 edges · 150 communities (130 shown, 20 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 645 edges (avg confidence: 0.59)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2394907f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- TaskSpineStore
- AgenticWorkerLoop
- Merged Agentic Swarm Blueprint (Root)
- LatencyTracker
- CloudCLIClient
- multi_provider_fabric.py
- SubTask
- OpenCodeSwarmManager
- webapp.py
- models/__init__.py
- _router_with_keys
- CodebaseMapService
- DurableAgentRouter
- DurableAgentFactory
- WorkerRole
- ProxyChainHealth
- AgentSpec
- .run_full_agentic_workflow
- FastFallbackRouter
- TaskMasterService
- TestClaudeProxyHandler
- WorkerPoolConfig
- KeyPoolManager
- cmd_config
- test_streaming_proxy.py
- conftest.py
- HopResult
- KnowledgeCache
- services/__init__.py
- _args
- TestResolveLitellmModelForRole
- MultiProviderFabric
- ProgressLogEntry
- _record_failure
- test_swarm_profiles.py
- ConcurrencyRampController
- litellm
- TestTokenSavior
- test_multi_provider_fabric.py
- TestWaveGatesWithRealState
- TestWaveGateController
- Graphify Knowledge Graph Pipeline
- swarm_run.py
- FastFallbackConfig
- run_smoke_workflow.sh
- test_health_check.py
- ChainRegistry
- report_service.py
- _make_learning_entry
- TestDispatchRequest
- PassthroughStreamingProxy
- TestRunFullAgenticWorkflow
- generate_progress_report.sh
- verify_component.sh
- ProgressLedgerService
- ProxyServerDaemon
- test_report_service.py
- Graphify Pipeline
- ClaudeProxyHandler
- APIKeyInfo
- _main_with_args
- MultiLayeredAgenticOrchestrator
- TestFormatConversion
- task_spine_cli.py
- .get_available_worker
- CircuitBreaker
- .run_all
- _forward_transcription
- Merged Agentic Swarm OS PRD v2
- _parse_multipart
- test_agentic_cli.py
- _evaluate_promotion_criteria
- _read_jsonl
- TestRun
- Ultracode Swarm Audit Fleet Manifest
- test_webapp.py
- StreamingProxyConfig
- Merged Agentic Swarm OS Progress Report
- Operator Runbook
- test_learning_loop.py
- ObstaclePlaybookEngine
- Merged Agentic Swarm
- dynamic_learning_loop
- project
- start_task_spine.sh
- Whisper Transcription
- Merged Agentic Swarm PRD
- _run_latency_test
- orchestrator
- role_allocations
- run_learning_loop_test.sh
- start_proxy.sh
- verify_task_spine.sh
- TaskStatus
- .load_keys
- .handle_task_failure
- test_check_streaming_fcc_happy_path
- OpenCode Routing Modes
- WorkerRuntimeAdapter (3 modes)
- check_proxy_health.sh
- _ChunkStream
- _StallStream
- Cross-Repo Graph Merge
- BFS/DFS Query Traversal
- Native Task Spine CLI Fallback
- opencode-swarm.json
- verify_worker_runtime.sh
- _DNSCache
- handle_run
- _simulate_reuse
- TestCaptureStep
- TestChains
- TestLatencyTest
- TestReports
- promotion_policy
- package.json
- load_durable_agents.sh
- start_worker_runtime.sh
- stop_agentic_services.sh
- _FakeClient
- Any
- TestCmdProviders
- _load_registry
- TestRunPlan
- Neo4j Export
- CI Lint and Test
- phase_gates
- retry_policy
- discover_environment.sh
- verify_proxy.sh
- TestTargetRepoRoot
- TestModelRoleUpdate
- TestCLIStringFunctions
- Post-Commit Auto-Rebuild Hook
- ci.sh
- setup-and-run.sh
- .get_summary
- Reflect Work Memory
- Windows Native CI Workflow
- Graphify Usage Rules (AGENTS.md)
- Architecture Principles
- merged-agentic-swarm
- TestBanPersistence
- test_claude_proxy_server.py
- TestLitellmPresenceInRoutes
- TestMalformedOverlayRoutes
- graphify reference: incremental update and cluster-only
- Q: What is KeyPoolManager?
- graphify reference: transcribe video and audio

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
- `Graphify Knowledge Graph Pipeline (mirror)` --semantically_similar_to--> `Graphify Knowledge Graph Pipeline`  [INFERRED] [semantically similar]
  .claude/skills/graphify/SKILL.md → .agents/skills/graphify/SKILL.md
- `Extraction JSON Schema (mirror)` --semantically_similar_to--> `Extraction JSON Schema`  [INFERRED] [semantically similar]
  .claude/skills/graphify/references/extraction-spec.md → .agents/skills/graphify/references/extraction-spec.md
- `BFS/DFS Graph Traversal (mirror)` --semantically_similar_to--> `BFS/DFS Graph Traversal`  [INFERRED] [semantically similar]
  .claude/skills/graphify/references/query.md → .agents/skills/graphify/references/query.md
- `Neo4j Export (mirror)` --semantically_similar_to--> `Neo4j Export`  [INFERRED] [semantically similar]
  .claude/skills/graphify/references/exports.md → .codex/skills/graphify/references/exports.md
- `Whisper Transcription (mirror)` --semantically_similar_to--> `Whisper Transcription`  [INFERRED] [semantically similar]
  .claude/skills/graphify/references/transcribe.md → .codex/skills/graphify/references/transcribe.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Extraction Subagent Contract** — _agents_skills_graphify_references_extraction_spec_extractionschema, _agents_skills_graphify_references_extraction_spec_nodeid, _agents_skills_graphify_references_extraction_spec_confidencerubric [EXTRACTED 1.00]
- **Graph Query Flow** — _agents_skills_graphify_references_query_traversal, _agents_skills_graphify_references_query_queryexpansion, _agents_skills_graphify_references_query_saveresult [EXTRACTED 1.00]
- **Graphify Extraction Pipeline** — _codex_skills_graphify_skill_ast_extraction, _codex_skills_graphify_skill_semantic_extraction, _codex_skills_graphify_references_extractionspec_extractionschema, _codex_skills_graphify_skill_communitydetection [INFERRED 0.85]
- **OpenCode CI Fleet** — _github_workflows_opencodereview_opencodereview, _github_workflows_opencodescheduled_maintenance, _github_workflows_opencode_routing, _github_workflows_opencode_litellmgateway [INFERRED 0.85]
- **uv-based CI Gate** — _github_workflows_arcci_arcci, _github_workflows_ci_linttest, _github_workflows_matrixci_multirunner [INFERRED 0.75]
- **Merged Agentic Swarm Operating Layers** — merged_agentic_swarm_blueprin_claude_code_control_plane, merged_agentic_swarm_blueprin_task_master_spine, merged_agentic_swarm_blueprin_opencode_worker_plane, merged_agentic_swarm_blueprin_proxy_fabric, merged_agentic_swarm_blueprin_hot_cold_learning [EXTRACTED 1.00]
- **Cold-Path Promotion Pipeline** — readme_cold_path_learning, prompts_cold_path_promotion_prompt, docs_agentic_completion_report_registry_compaction [INFERRED 0.85]
- **Wave-Gated Ramp-Up** — merged_agentic_swarm_blueprin_wave_gates, readme_wave_ramp, docs_agentic_completion_report_wave_gates_verified, _taskmaster_docs_prd_agentic_codebase_optimization_epic_wave_plan [INFERRED 0.85]
- **Cold-Path Learning Promotion Pipeline** — docs_agentic_knowledge_box_schema_knowledge_registry, docs_agentic_prd_v2_execution_ready_cold_path_pipeline, docs_agentic_audit_learning_loop_verification_promotion_pipeline, docs_agentic_audit_learning_loop_verification_durable_agent_factory [INFERRED 0.85]
- **Multi-Provider Gateway Stack on Host** — docs_agentic_audit_baseline_audit_fcc_proxy, docs_agentic_audit_proxy_verification_claude_proxy_service, docs_vscode_copilot_kepler_model_discovery_litellm_gateway, docs_fleet_manifests_2026_08_07_ultracode_swarm_audit_routatic_proxy, docs_agentic_audit_proxy_verification_gemini_pool [INFERRED 0.75]
- **Worker Execution Plane and Concurrency Ramp** — docs_agentic_prd_v2_execution_ready_worker_plane, docs_agentic_prd_v2_execution_ready_concurrency_ramp_controller, docs_agentic_audit_worker_runtime_verification_worker_runtime_adapter, docs_agentic_audit_worker_runtime_verification_concurrency_ramp, docs_agentic_audit_worker_runtime_verification_native_subagent [INFERRED 0.75]

## Communities (150 total, 20 thin omitted)

### Community 0 - "TaskSpineStore"
Cohesion: 0.06
Nodes (23): _LockedScope, main(), _make_parser(), Any, ArgumentParser, Manages the local task spine JSON file with fcntl locking., Create the spine file if it does not exist. Idempotent., Create a new task. Idempotent on task_id. (+15 more)

### Community 1 - "AgenticWorkerLoop"
Cohesion: 0.06
Nodes (26): RuntimeError, AgenticWorkerLoop, _command_safety_error(), _extract_text(), Any, Agentic Worker Tool Loop Runs a real agentic loop over the multi-provider…, Return a refusal reason if ``command`` is unsafe, else None., Extract the assistant's text content from an Anthropic-shaped response. (+18 more)

### Community 2 - "Merged Agentic Swarm Blueprint (Root)"
Cohesion: 0.05
Nodes (54): Agentic Codebase Optimization PRD (Markdown), Agentic Codebase Optimization PRD (Canonical TXT), Agentic Swarm Target Architecture, EPIC-00..05 Wave Plan, PRD Template, Semver Versioning Policy, LLM Agent Execution Brief, First Principles Rules (+46 more)

### Community 3 - "LatencyTracker"
Cohesion: 0.05
Nodes (37): get_tracker(), LatencyTracker, _pct_stats(), percentile(), Per-request streaming latency tracking and provider health reporting. Tracks…, Record the first-byte (TTFB) moment. Idempotent per request., Time-to-first-byte in seconds, or None if no byte was received., Total request duration in seconds, or None if still in flight. (+29 more)

### Community 4 - "CloudCLIClient"
Cohesion: 0.07
Nodes (21): CloudCLIClient, CloudCLIConfig, CloudCLIError, Any, CloudCLI client — trigger remote AI agents via the cloneclove.com /api/agent…, Trigger a remote agent with streaming (SSE) and yield each event dict., Raised when CloudCLI returns a non-2xx response or is misconfigured., Minimal client for the CloudCLI agent API (``POST /api/agent``). (+13 more)

### Community 5 - "multi_provider_fabric.py"
Cohesion: 0.09
Nodes (31): Client, HTTPTransport, Limits, Fast Fallback Router — parallel-probe, minimal-latency fallback dispatch. Why…, _build_transport(), close_thread_client(), _create_client(), dispatch() (+23 more)

### Community 6 - "SubTask"
Cohesion: 0.15
Nodes (19): EpicTask, PRDAnalysisResult, SubTask, TaskPriority, Loads persistent Task Master state from JSON file if present., _analysis(), _epic(), Tests for tools/agentic_orchestrator.py Coverage:… (+11 more)

### Community 7 - "OpenCodeSwarmManager"
Cohesion: 0.08
Nodes (18): live, OpenCodeSwarmManager, make_subtask(), Factory fixture that returns a function to create SubTask instances., Tests for services/opencode_swarm_service.py Coverage:…, A worker subtask goes through the agentic tool loop and reports honestly. A…, Wave N batch executes at ramp[N] concurrency, not the 4-worker default., A provided ramp_sequence overrides the default wave_gate_level mapping. (+10 more)

### Community 8 - "webapp.py"
Cohesion: 0.09
Nodes (47): HTMLResponse, JSONResponse, create_app(), _fabric_chains(), _fabric_routes(), handle_chain_update(), handle_chains(), handle_dashboard() (+39 more)

### Community 9 - "models/__init__.py"
Cohesion: 0.08
Nodes (23): int, Models Package Initialization, Any, Enum, str, Wave Gates Data Models, WaveExecutionState, WaveGateCriteria (+15 more)

### Community 10 - "_router_with_keys"
Cohesion: 0.09
Nodes (28): _anthropic_response(), _mock_response(), patch, Tests for merged_agentic_swarm/fast_fallback.py Coverage: parallel probe first-…, Both wave probes fire concurrently; the first 2xx is returned., A failing primary overlaps the fallback's latency instead of serializing it., A losing in-flight probe (2xx after another probe won) must not corrupt state., With probe_stagger_ms, the primary's head-start lets it win even if slower. (+20 more)

### Community 11 - "CodebaseMapService"
Cohesion: 0.08
Nodes (14): CodebaseMapService, Any, Scans workspace repository files and parses AST definitions., Parses Python file to extract top-level functions, classes, and imports., Cross-references required components against mapped codebase to find spec gaps.…, Load persisted codebase map state from disk., Persist codebase map state so restart doesn't require re-scan., Closes a specific spec gap after verifying fixes. (+6 more)

### Community 12 - "DurableAgentRouter"
Cohesion: 0.08
Nodes (18): DurableAgentRouter, get_durable_router(), Any, Path, Extract YAML-style frontmatter between --- markers., Read the body content after frontmatter., Extract lowercase alphanumeric tokens, dropping very short/common words., Collect trigger keywords from an agent's body (Trigger section) + system_prompt. (+10 more)

### Community 13 - "DurableAgentFactory"
Cohesion: 0.08
Nodes (16): DurableAgentFactory, Any, Remove and return count of expired HOT micro-specialists (FIX-09)., Resolve the durable cold-path agents registry (agents.jsonl). Prefers an…, Load durable agents from the cold-path agents.jsonl registry. Called once at…, Append a COLD_DURABLE agent record to the durable agents.jsonl registry.…, Write an agent spec .md file from a JSONL entry. Returns the file path, or None…, Read agents.jsonl and write spec files for every entry. Returns the count of… (+8 more)

### Community 14 - "WorkerRole"
Cohesion: 0.10
Nodes (23): Run the agentic swarm orchestrator against spotify-ai project. Produces an…, Phase 5: Durable Learning Loop End-to-End Verification, AgentType, Enum, str, Agent, Worker Pool, and Spawn Chain Data Models, WorkerRole, agents_registry_path() (+15 more)

### Community 15 - "ProxyChainHealth"
Cohesion: 0.10
Nodes (38): HealthConfig, ProxyChainHealth, Runs reachability, streaming, and provider-status checks., Endpoints and request tuning for the health checks. Each field falls back to…, _patch_client(), check_opencode reports failure on HTTP 500 from upstream., check_opencode reports failure on connection errors., check_streaming reports unhealthy when no content_block_delta arrives. (+30 more)

### Community 16 - "AgentSpec"
Cohesion: 0.08
Nodes (20): AgentSpec, Return True if this agent has a TTL and has exceeded it., get_runtime_adapter(), Any, Unified adapter that launches workers in the selected execution mode. Modes:…, Return the resolved opencode binary, or None if unavailable., Launch a single worker with a task and return a result dict. Result keys:…, Launch a batch of tasks for a given role, up to max_concurrency. (+12 more)

### Community 17 - ".run_full_agentic_workflow"
Cohesion: 0.13
Nodes (11): _cancellation_check(), Any, Event, Deduplicate cold-path registries by content hash (knowledge) and ID…, Apply worker outputs to disk and count files written. Primary path: agentic-…, Return an aborted result if the run was cancelled, else None., Initializes Key Pool Proxy server and verifies service readiness., Return an abort result when a gate fails and gates are enforced.… (+3 more)

### Community 18 - "FastFallbackRouter"
Cohesion: 0.12
Nodes (17): dispatch_fast(), FastFallbackRouter, _ProbeContext, _ProbeResult, Any, Event, Parallel-probe fallback router over the model fabric's route table.…, Dispatch a request across providers with parallel fallback probing. Returns an… (+9 more)

### Community 19 - "TaskMasterService"
Cohesion: 0.10
Nodes (11): Parses and optimizes PRD via Task Master AI model fabric routing. Calls the…, Orchestrator wrapping the real Task Master AI spine. NOTE on state paths: -…, Updates task status in state and syncs to file., Saves Task Master state as the authoritative single source of truth., Rough complexity analysis: estimate turns based on task scope., TaskMasterService, Tests for services/task_master_service.py Coverage: TaskMasterService —…, Regression for #41: temp file must not be the fixed <target>.tmp. (+3 more)

### Community 20 - "TestClaudeProxyHandler"
Cohesion: 0.06
Nodes (15): #42: /status surfaces exhausted/cooldown/latency per provider., #35: a body over the JSON cap must be rejected before buffering., #35: a body under the cap still reaches normal processing (400 here)., #35: audio multipart bodies have their own (higher) cap., #33: FAST_FALLBACK_ENABLED routes through the hedged router., #33: without the flag the proxy keeps using the fabric dispatch path., POST /v1/messages should return a response (simulation fallback)., POST /v1/messages without an auth token → 401. (+7 more)

### Community 21 - "WorkerPoolConfig"
Cohesion: 0.10
Nodes (14): Any, Increment the completed counter for the given pool., Increment the failed or rate_limited counter for the given pool., Return a copy of the pool_health dict., SpawnChainEntry, WorkerPoolConfig, WorkerPoolState, Initializes the 40 worker specs across role allocations. (+6 more)

### Community 22 - "KeyPoolManager"
Cohesion: 0.11
Nodes (8): KeyPoolManager, When every key is still cooling down, get_key returns None so the fabric…, Even with many keys, none may be reused while every one is cooling down., A key still cooling down must not be picked while another is active., #42: summary reports exhausted count, next cooldown expiry, avg latency., Getting a key from a provider that doesn't exist should not raise., TestKeyPoolManager, TestKeyPoolReload

### Community 23 - "cmd_config"
Cohesion: 0.25
Nodes (6): cmd_config(), Show configuration state., cmd_config should print key pool, routes, and swarm info without crashing., Verify model routes appear in config output., Verify argparse setup works for each subcommand., TestCmdConfig

### Community 24 - "test_streaming_proxy.py"
Cohesion: 0.17
Nodes (30): asyncio, make_proxy(), make_request(), post(), Tests for ``merged_agentic_swarm.streaming_proxy``. Covers the zero-buffering…, Send one proxied request and return the proxy's Response., Each upstream network chunk must reach the client with identical boundaries —…, Proves no-buffering: the first chunk is yielded the instant the upstream writes… (+22 more)

### Community 25 - "conftest.py"
Cohesion: 0.09
Nodes (30): isolated_agent_factory(), isolated_chain_registry(), isolated_codebase_mapper(), isolated_fabric(), isolated_key_pool(), isolated_knowledge_cache(), isolated_progress_ledger(), isolated_swarm_manager() (+22 more)

### Community 26 - "HopResult"
Cohesion: 0.11
Nodes (28): Namespace, _build_parser(), HopResult, main(), _print_header(), _print_human(), Any, ArgumentParser (+20 more)

### Community 27 - "KnowledgeCache"
Cohesion: 0.11
Nodes (8): KnowledgeCache, Any, Tests for tools/knowledge_cache.py Coverage: KnowledgeCache — load_cache,…, Learning with TTL should be expired and not returned., Pre-populate cache file with duplicate entries, verify compaction on load., TestKnowledgeCache, Step 2: RECORD — Write to hot cache (knowledge_cache.json)., TestRecordStep

### Community 28 - "services/__init__.py"
Cohesion: 0.09
Nodes (33): Services Package Initialization, litellm_model_for_fabric_route(), Model Role Routing Resolves a worker role (deep / main / fast tier, or a…, Return the first litellm model in the fabric route list for a model alias., Return the litellm virtual Gemini alias for a worker role. Resolution order: 1.…, resolve_litellm_model_for_role(), list_profiles(), load_profiles() (+25 more)

### Community 29 - "_args"
Cohesion: 0.14
Nodes (12): _args(), _fake_saved(), _patch_auto_save(), `run --profile review` resolves the profile's waves as the ramp and the tier-…, argparse wires `run --profile patch` into cmd_run with profile resolved., Old progress.json snapshots passed via --progress keep working., #19: cmd_status must point at the live ProgressLedgerService ledger., Fake save_run_report return, so auto-save never writes into the real repo. (+4 more)

### Community 30 - "TestResolveLitellmModelForRole"
Cohesion: 0.07
Nodes (8): Tests for services/model_routing.py Coverage: role -> litellm alias resolution,…, The on-disk registry must parse and carry a consistent role_routing section., Live resolution should match the tier aliases in the registry file., reload_registry() clears the cache so an updated registry file is seen., TestLitellmModelForFabricRoute, TestRegistryFile, TestReloadRegistry, TestResolveLitellmModelForRole

### Community 31 - "MultiProviderFabric"
Cohesion: 0.15
Nodes (13): _load_fabric_routes_overlay(), MultiProviderFabric, Any, Load the per-alias route overlay (cached); {} when missing or unreadable., Flatten Anthropic content blocks (or plain text) into a single text string., Convert normalized messages (Anthropic-shaped) to OpenAI Chat Completions…, Normalize a content value into a list of Anthropic content blocks., Convert normalized messages to Anthropic Messages API format. Used for… (+5 more)

### Community 32 - "ProgressLogEntry"
Cohesion: 0.16
Nodes (12): ObstaclePlaybookEntry, ProgressLogEntry, Any, Progress Ledger, Success Markers, and Obstacle Playbooks Models, SuccessMarker, TaskMasterStateSnapshot, Progress Ledger, Success Markers, and Self-Healing Obstacle Playbook Engine…, Tests for models/ledger_models.py Coverage: SuccessMarker,… (+4 more)

### Community 33 - "_record_failure"
Cohesion: 0.18
Nodes (8): _persist_bans(), Atomically write the perma-ban map to disk. Caller must hold _fabric_lock., Record a provider failure — perma-ban on 401 auth errors, circuit-break on…, Record a provider success — reset circuit breaker and update last-working cache., _record_failure(), _record_success(), Provider should be retried after perma-ban duration expires., TestCircuitBreaker

### Community 34 - "test_swarm_profiles.py"
Cohesion: 0.08
Nodes (11): _fresh_cache(), fixture, Tests for services/swarm_profiles.py Coverage: load_profiles reads the JSON and…, The on-disk profiles file must parse and carry the documented fields., Each test starts (and ends) with an empty profile cache., A fallback load must not poison later loads once the real file returns., TestListProfiles, TestLoadProfiles (+3 more)

### Community 35 - "ConcurrencyRampController"
Cohesion: 0.12
Nodes (6): ConcurrencyRampController, Controls worker concurrency ramp-up across wave gates., Map wave gate level to max workers. Gate 0 -> 4, gate 1 -> 8, gate 2 -> 16,…, Return the full ramp sequence., Executes a batch of subtasks in parallel using ThreadPoolExecutor up to max…, TestConcurrencyRampController

### Community 36 - "litellm"
Cohesion: 0.10
Nodes (23): limit, name, limit, name, context, output, models, name (+15 more)

### Community 37 - "TestTokenSavior"
Cohesion: 0.09
Nodes (8): Tools Package Initialization, Token Savior & Context Compactor Optimizes context window consumption via…, Removes blank lines and excessive indentation spaces to save tokens., Filters noisy bash logs and retains error tracebacks + summary lines., Compresses assistant prose (Caveman mode) by removing pleasantries, hedging,…, TokenSavior, Tests for tools/token_savior.py Coverage: TokenSavior — compact_code_snippet,…, TestTokenSavior

### Community 38 - "test_multi_provider_fabric.py"
Cohesion: 0.15
Nodes (6): _isolated_bans_path(), fixture, Tests for providers/multi_provider_fabric.py Coverage:…, Redirect the persisted-bans path so tests never write into the repo., TestFabricRouteOverlay, TestRouteBuilding

### Community 39 - "TestWaveGatesWithRealState"
Cohesion: 0.20
Nodes (7): _ownership_map(), Tests for services/wave_gate_service.py Coverage: WaveGateController —…, Attach real epics (wave 1) with subtasks carrying output artifacts., Attach real wave-3 epics whose subtasks output src/ artifacts., Wave 3 must not pass on statuses alone — verification must have run., Inline syntax fallback (no tests_ran) must not satisfy tests_passing., TestWaveGatesWithRealState

### Community 40 - "TestWaveGateController"
Cohesion: 0.08
Nodes (10): Subtasks producing output within owned paths should have no violations., #36: absent ownership map is an optional gate — warn and pass., Map exists but the requested pool is absent — keep the hard-fail., Wave 1 fails because task master has no tasks for it., Wave 2 gate should evaluate with task_master data., Wave 3 gate should evaluate with task_master data and ownership., Wave 0 should pass when there are no unresolved spec gaps., advance_wave should move from wave 0 to wave 1 if gate criteria pass. (+2 more)

### Community 41 - "Graphify Knowledge Graph Pipeline"
Cohesion: 0.13
Nodes (22): URL Ingest (/graphify add), Folder Watch (--watch), Graphify MCP Server, Confidence Rubric, Extraction JSON Schema, Deterministic Node ID Rules, Constrained Query Expansion, Save-Result Feedback Loop (+14 more)

### Community 42 - "swarm_run.py"
Cohesion: 0.29
Nodes (21): CompletedProcess, build_tasks(), discover_modules(), fetch_issues(), _issue_risk(), latest_run_id(), main(), make_docs_task() (+13 more)

### Community 43 - "FastFallbackConfig"
Cohesion: 0.14
Nodes (9): dict, FastFallbackConfig, Build a config from ``FAST_FALLBACK_*`` environment variables., Tunables for the fast-fallback router (dataclass defaults + env overrides)., A fallback with strong latency history outranks a slow primary., No latency history → static verified-first order is untouched., A perma-banned provider does not appear in the candidate list., TestAdaptiveSelection (+1 more)

### Community 44 - "run_smoke_workflow.sh"
Cohesion: 0.17
Nodes (15): fail(), info(), main(), pass(), preflight(), print_summary(), refresh_progress_report(), run_step() (+7 more)

### Community 45 - "test_health_check.py"
Cohesion: 0.10
Nodes (19): _make_sse_response(), Response, Return a 200 httpx.Response whose .stream yields SSE events., from_env returns defaults when no env vars are set., from_env picks up env overrides for string fields., from_env casts numeric env vars to int/float., from_env surfaces ValueError for non-numeric env values (no silent fallback)., --json flag emits machine-readable JSON for all checks. (+11 more)

### Community 46 - "ChainRegistry"
Cohesion: 0.13
Nodes (9): ChainRegistry, Generate a collision-proof spawn-chain entry_id (sequence + timestamp suffix).…, isolated_agents_registry(), fixture, Tests for services/agent_factory_service.py Coverage: ChainRegistry (load,…, Return a temp path for the durable cold-path agents.jsonl registry., #18: entry_ids in one promotion batch must never collide., #18: separate registry instances sharing a file must not reuse entry_ids. (+1 more)

### Community 47 - "report_service.py"
Cohesion: 0.17
Nodes (22): _build_epics(), _build_gates(), build_run_report(), _build_timeline(), _build_waves(), _format_ts(), Any, Path (+14 more)

### Community 48 - "_make_learning_entry"
Cohesion: 0.18
Nodes (10): _make_learning_entry(), _promote_learning(), Execute cold-path promotion: write all 5 output files. Returns dict with paths…, Create a learning entry dict matching the knowledge_cache schema., Step 4: PROMOTE — Write all 5 cold-path artifacts., Dedup: identical learning should not produce duplicate agent., Verify that content-hash-based dedup catches semantically identical entries., Entries with different content should not collide. (+2 more)

### Community 49 - "TestDispatchRequest"
Cohesion: 0.13
Nodes (11): patch, Block all real providers so dispatch falls to simulation., Without any working providers, should fall through to simulation., Test that content blocks (list) are flattened correctly before dispatch., Test a successful API call returns formatted Anthropic response., A 2xx with a non-dict JSON body must cascade, not crash on .get()., A 2xx with an empty/non-JSON body must cascade, not raise JSONDecodeError., 4xx/5xx from dispatch() must be caught by HTTPStatusError handling. (+3 more)

### Community 50 - "PassthroughStreamingProxy"
Cohesion: 0.15
Nodes (12): Route, PassthroughStreamingProxy, AsyncClient, Request, Response, Zero-buffering SSE passthrough proxy. Accepts Anthropic Messages API streaming…, Return the shared httpx client, creating it if needed., Close the underlying httpx client and release connections. (+4 more)

### Community 51 - "TestRunFullAgenticWorkflow"
Cohesion: 0.16
Nodes (8): gates=False keeps advance_wave() running (state advances) but a non-passing…, A run emits proxy_deployed (after init) and run_deployed (pre-wave)…, Each wave threads its wave number as wave_gate_level so the swarm executes at…, A provided ramp_sequence reaches every swarm batch, default_model is recorded…, Without a profile, the swarm batch gets no ramp_sequence kwarg and the ledger…, #32: a set cancel_event makes the workflow return an aborted result., Wire the orchestrator singletons for a deterministic workflow run., TestRunFullAgenticWorkflow

### Community 52 - "generate_progress_report.sh"
Cohesion: 0.12
Nodes (5): count_files(), durable_agent_count(), generate_evidence_table(), generate_report(), generate_progress_report.sh script

### Community 53 - "verify_component.sh"
Cohesion: 0.22
Nodes (15): CHECK_COMMANDS, CHECK_DETAILS, CHECK_EXIT_CODES, check_git(), CHECK_NAMES, check_node(), check_opencode(), check_proxy() (+7 more)

### Community 54 - "ProgressLedgerService"
Cohesion: 0.17
Nodes (5): ProgressLedgerService, Regression for #41: temp file must not be the fixed <target>.tmp., Concurrent save_ledger calls must never leave a torn JSON target., TestProgressLedgerService, TestLogProgressModelArg

### Community 55 - "ProxyServerDaemon"
Cohesion: 0.13
Nodes (10): HTTPServer, ProxyServerDaemon, Threaded HTTP server to handle concurrent requests., ThreadedHTTPServer, fixture, ProxyServerDaemon should start and stop without error., Calling start() twice should not create a second server., Start a server on random port for each test. (+2 more)

### Community 56 - "test_report_service.py"
Cohesion: 0.26
Nodes (8): _ledger(), _log(), Tests for services/report_service.py Coverage: build_run_report…, TestBuildRunReport, TestRenderMarkdown, TestSaveRunReport, _write_json(), _write_jsonl()

### Community 57 - "Graphify Pipeline"
Cohesion: 0.16
Nodes (16): Graphify Add URL Ingest, Graphify Watch Mode, Token Reduction Benchmark, Post-Commit Hook, build_merge, Cluster-Only Flow, Graph Diff, Incremental Update Flow (+8 more)

### Community 58 - "ClaudeProxyHandler"
Cohesion: 0.21
Nodes (7): BaseHTTPRequestHandler, ClaudeProxyHandler, _proxy_dispatch(), Any, Reject an oversized body. Close the connection since the unread bytes would…, Enforce the inbound proxy token (ANTHROPIC_AUTH_TOKEN, default 'freecc').…, Route a request through the hedged fast-fallback router when enabled. Both…

### Community 59 - "APIKeyInfo"
Cohesion: 0.13
Nodes (11): Providers Package Initialization, APIKeyInfo, KeyStatus, Enum, str, API Key Pool Manager & Key Rotator Supports multi-provider key rotation, quota…, Gets an active API key using round-robin / least-used strategy., Internal: must be called while holding self._lock. (+3 more)

### Community 60 - "_main_with_args"
Cohesion: 0.20
Nodes (4): _main_with_args(), Coverage for the swarm subcommand: --list, --profile, and error paths., TestCmdSwarm, TestMain

### Community 61 - "MultiLayeredAgenticOrchestrator"
Cohesion: 0.12
Nodes (7): MultiLayeredAgenticOrchestrator, Append a JSON line to a JSONL registry., Cold-path: normalize hot cache entries → knowledge.jsonl → validated →…, Load previously promoted learning IDs so cold-path dedup survives restarts., When _write_agent_spec_file returns None (already exists), the skip branch logs…, Two categories promoted in one batch must produce distinct chain entry_ids…, TestRunSyntaxVerificationPaths

### Community 62 - "TestFormatConversion"
Cohesion: 0.13
Nodes (3): format_anthropic_to_openai converts normalized tool_calls to OpenAI shape., format_anthropic_to_anthropic builds tool_use + tool_result blocks for…, TestFormatConversion

### Community 63 - "task_spine_cli.py"
Cohesion: 0.43
Nodes (13): cmd_attach_evidence(), cmd_block(), cmd_claim(), cmd_create(), cmd_inspect(), cmd_list(), cmd_restart_verify(), cmd_update() (+5 more)

### Community 65 - "CircuitBreaker"
Cohesion: 0.14
Nodes (8): CircuitBreaker, AsyncBaseTransport, Simple fail-fast circuit breaker. Tracks consecutive failures. After…, True when the circuit is open (requests should be rejected)., Current consecutive failure count., Reset the failure counter after a successful request., Increment the failure counter; open circuit if threshold reached., test_circuit_breaker_unit_transitions()

### Community 66 - ".run_all"
Cohesion: 0.21
Nodes (7): Probe routatic-proxy /health and surface circuit-breaker metrics., Probe the FCC gateway /health endpoint., Check upstream OpenCode API reachability (models endpoint)., Stream a tiny /v1/messages request and time first token + total. ``endpoint``…, Monitor provider/circuit-breaker status via routatic + FCC models list., Run every check; returns results in a stable order., _truncate()

### Community 67 - "_forward_transcription"
Cohesion: 0.22
Nodes (5): _forward_transcription(), Forward a transcription request to the configured Whisper backend., _FakeResp, Multipart audio POST → forwarded to Whisper backend → JSON response., TestForwardTranscription

### Community 68 - "Merged Agentic Swarm OS PRD v2"
Cohesion: 0.21
Nodes (12): Knowledge Registry Dedup Rules, Knowledge Box Schema, Knowledge Registry (knowledge.jsonl), Cold-Path Pipeline (knowledge.jsonl -> agents.jsonl -> chain.jsonl), Learning & Recovery Fabric (Layer 5), Merged Agentic Swarm OS PRD v2, Orchestrator CLI (tools/agentic_cli.py), Merged Agentic Swarm Operator Runbook (+4 more)

### Community 69 - "_parse_multipart"
Cohesion: 0.23
Nodes (6): _parse_multipart(), Return (file_bytes, file_name, model_name) from a multipart body., _multipart_body(), Multipart POST without a file field → 400., Backend connection failure → 503 with unavailable message., TestParseMultipart

### Community 70 - "test_agentic_cli.py"
Cohesion: 0.23
Nodes (5): _ledger_json(), _ledger_log(), Tests for tools/agentic_cli.py Coverage: cmd_config, basic CLI parsing, cmd_run…, TestCmdPromote, TestCmdReport

### Community 71 - "_evaluate_promotion_criteria"
Cohesion: 0.20
Nodes (9): _append_jsonl(), _evaluate_promotion_criteria(), Step 3: EVALUATE — Score learning against promotion criteria., A strong, substantive entry should pass all promotion criteria., A weak entry should fail promotion criteria., Should detect when an entry already exists in cold knowledge., Append a single JSON entry as a line to a JSONL file., Evaluate whether a learning entry meets cold-path promotion criteria. Returns… (+1 more)

### Community 72 - "_read_jsonl"
Cohesion: 0.24
Nodes (10): _load_agents_from_registry(), Verify all 5 cold-path artifacts exist and are valid. Returns list of failures., Simulate loading agents after restart: read agents.jsonl and .md files., End-to-end: capture -> record -> evaluate -> promote -> verify -> load -> route…, Run the complete lifecycle and verify every step., Read all JSONL entries from a file, returning a list of dicts., Promote multiple different learnings and verify they are all loadable., _read_jsonl() (+2 more)

### Community 73 - "TestRun"
Cohesion: 0.17
Nodes (3): #32: GET /api/run/status reports runs started by POST /api/run., #32: POST /api/run/{id}/cancel signals the workflow's cancel_event., TestRun

### Community 74 - "Ultracode Swarm Audit Fleet Manifest"
Cohesion: 0.18
Nodes (11): FCC Proxy (port 8080, verified), LiteLLM port 4000 confirmed dead, Test Coverage Analysis (66% combined), FCC Server (port 8080, healthy), Registry Integrity Issues (dup IDs, orphan chain), Routatic Proxy (port 3456, 300 models), Ultracode Swarm Audit Fleet Manifest, fcc-server (port 8080, Anthropic-shaped) (+3 more)

### Community 75 - "test_webapp.py"
Cohesion: 0.10
Nodes (7): merged-agentic-swarm — Agentic orchestration system with multi-provider fabric…, Tests for merged_agentic_swarm.webapp — the control-panel JSON API + dashboard.…, Async byte stream over fixed chunks for the mocked litellm SSE response., _Stream, TestModels, TestProfiles, TestStatus

### Community 76 - "StreamingProxyConfig"
Cohesion: 0.22
Nodes (9): create_streaming_proxy_app(), Starlette, Zero-buffering streaming passthrough proxy for Anthropic Messages API. Accepts…, Return a standalone Starlette ASGI application., Create a configured streaming proxy Starlette app in one call., Configuration for the zero-buffering streaming proxy., StreamingProxyConfig, test_config_defaults() (+1 more)

### Community 77 - "Merged Agentic Swarm OS Progress Report"
Cohesion: 0.24
Nodes (10): Baseline Audit of Agentic Orchestration, Critical Port Mismatch (fabric routes 4000 vs actual 8080), Inbound Auth Gate, Gemini Key Pool (42 keys), Proxy Verification Report, Multi-Provider Proxy Fabric (Layer 4), Merged Agentic Swarm OS Progress Report, Worker Pool Status (0 launched) (+2 more)

### Community 78 - "Operator Runbook"
Cohesion: 0.22
Nodes (10): DurableAgentFactory, Learning Loop Verification Report, Cold-Path Promotion Pipeline (capture -> promote -> restart), claude-proxy systemd service (port 8089), Claude Proxy (port 8089), Learning Loop, Operator Runbook, Smoke Workflow (run_smoke_workflow.sh) (+2 more)

### Community 79 - "test_learning_loop.py"
Cohesion: 0.20
Nodes (9): _make_agent_jsonl_entry(), _make_chain_jsonl_entry(), _make_knowledge_jsonl_entry(), Tests for the full learning loop lifecycle: capture -> evaluate -> promote ->…, Create a cold-path knowledge.jsonl entry., Create a cold-path agents.jsonl entry., Step: LOAD — Simulate loading agents after a restart., Create a cold-path chain.jsonl entry. (+1 more)

### Community 80 - "ObstaclePlaybookEngine"
Cohesion: 0.17
Nodes (3): ObstaclePlaybookEngine, Tests for services/progress_ledger_service.py Coverage: ObstaclePlaybookEngine…, TestObstaclePlaybookEngine

### Community 81 - "Merged Agentic Swarm"
Cohesion: 0.33
Nodes (9): KeyPool, Merged Agentic Swarm, MultiLayeredAgenticOrchestrator, Python 3.14 Floor (PEP 758), TaskMaster, Semver Bump Rule, WaveGateController, Swarm Run Workflow (+1 more)

### Community 82 - "dynamic_learning_loop"
Cohesion: 0.22
Nodes (9): dynamic_learning_loop, agent_registry, chain_registry, cold_registry, hot_cache, micro_spawn_policy, progress_report, max_lifespan_sec (+1 more)

### Community 83 - "project"
Cohesion: 0.22
Nodes (9): project, description, knowledge_graph_path, name, ownership_map, progress_report, provider_registry, root_dir (+1 more)

### Community 84 - "start_task_spine.sh"
Cohesion: 0.36
Nodes (8): banner(), fail(), info(), ok(), start_task_spine.sh script, TASK_SPINE_STATE, TASK_SPINE_TYPE, warn()

### Community 85 - "Whisper Transcription"
Cohesion: 0.25
Nodes (8): Whisper Transcription (mirror), Confidence Rubric, Extraction JSON Schema, Node ID Format Rule, Whisper Domain Hint Prompt, Whisper Transcription, Honesty Rules, Semantic Extraction

### Community 86 - "Merged Agentic Swarm PRD"
Cohesion: 0.25
Nodes (8): Durable Agent Routing Hook Verification, Claude Code Control Plane (Layer 1), Task Master Task Spine (Layer 2), Agentic Worker Loop, Core Orchestrator, Durable Agent Router, Merged Agentic Swarm PRD, Task Master Service

### Community 87 - "_run_latency_test"
Cohesion: 0.25
Nodes (8): Exception, _fetch_litellm_aliases(), _latency_error(), AsyncClient, Live litellm /v1/models aliases; on failure (aliases=[], note)., ok:false payload — short error, never the key., Stream one chat/completions request; report TTFB and total wall time., _run_latency_test()

### Community 88 - "orchestrator"
Cohesion: 0.25
Nodes (8): orchestrator, control_plane, heartbeat_interval_ms, max_concurrency, proxy_endpoint, ramp_sequence, runner, telemetry_enabled

### Community 89 - "role_allocations"
Cohesion: 0.25
Nodes (8): role_allocations, codebase_mapper, core_engineer, master_architect, refactor_specialist, security_verifier, spec_gap_closer, unit_tester

### Community 90 - "run_learning_loop_test.sh"
Cohesion: 0.39
Nodes (5): print_banner(), run_learning_loop_test.sh script, step_fail(), step_info(), step_pass()

### Community 91 - "start_proxy.sh"
Cohesion: 0.32
Nodes (7): check_proxy(), FCC_PORT, FCC_PROCESS_NAME, ROUTATIC_PORT, ROUTATIC_PROCESS_NAME, start_proxy.sh script, usage()

### Community 92 - "verify_task_spine.sh"
Cohesion: 0.39
Nodes (5): banner(), die(), verify_task_spine.sh script, step_fail(), step_ok()

### Community 93 - "TaskStatus"
Cohesion: 0.16
Nodes (13): PRDDocument, Enum, str, PRD and Task Master Data Models, SpecGap, TaskStatus, Codebase Mapper & Spec Gap Closer Service Maps repository structure, AST…, Task Master AI Spine Service PRD optimization, task parsing, dependency… (+5 more)

### Community 94 - ".load_keys"
Cohesion: 0.25
Nodes (3): Loads API keys from env file, environment variables, and local key files., Hot-reload keys from all sources, preserving runtime stats for persistent keys.…, Gather (provider, secret_value, key_id) candidates from all key sources.…

### Community 95 - ".handle_task_failure"
Cohesion: 0.32
Nodes (3): Any, Processes a task failure through self-healing playbooks., Matches error against playbooks and applies self-healing strategy.

### Community 96 - "test_check_streaming_fcc_happy_path"
Cohesion: 0.25
Nodes (8): Build a single SSE data line for an Anthropic streaming content-block-delta., check_streaming through FCC endpoint measures TTFB and total latency., check_streaming targets routatic-proxy when endpoint='routatic'., stream' subcommand runs only the streaming check., _sse_event(), test_check_streaming_fcc_happy_path(), test_check_streaming_routatic_endpoint(), test_main_stream_subcommand()

### Community 97 - "OpenCode Routing Modes"
Cohesion: 0.52
Nodes (7): Local Model Discovery Endpoints, Cloneclove Agent Path, LiteLLM Gateway Config, Provider Reachability Check, OpenCode Routing Modes, OpenCode PR Review, OpenCode Scheduled Maintenance

### Community 98 - "WorkerRuntimeAdapter (3 modes)"
Cohesion: 0.33
Nodes (7): Concurrency Ramp 1 -> 2 -> 4, native_subagent execution mode, WorkerRuntimeAdapter (3 modes), Worker Runtime Verification Report, ConcurrencyRampController, OpenCode Worker Plane (Layer 3, 40 workers), Concurrency Ramp Hard-Capped at 4 Workers (finding #21)

### Community 99 - "check_proxy_health.sh"
Cohesion: 0.33
Nodes (6): HEALTH_URL, log(), LOG_FILE, SERVICE_NAME, check_proxy_health.sh script, TIMEOUT_SEC

### Community 100 - "_ChunkStream"
Cohesion: 0.29
Nodes (4): _ChunkStream, Async byte stream over a fixed list of chunks. Optionally raises ``exc`` after…, Build an upstream ``httpx.Response`` that streams ``chunks`` as SSE., _sse_response()

### Community 101 - "_StallStream"
Cohesion: 0.29
Nodes (4): drain(), Consume (or close) a StreamingResponse so upstream streams are torn down., Async byte stream that never yields (simulates a stalled upstream)., _StallStream

### Community 102 - "Cross-Repo Graph Merge"
Cohesion: 0.33
Nodes (6): GitHub Clone, Cross-Repo Graph Merge, Cross-Repo Graph Merge (mirror), Cross-Repo Merge, CLAUDE.md Integration, Query Fast Path

### Community 103 - "BFS/DFS Query Traversal"
Cohesion: 0.47
Nodes (6): MCP Server Export, Graphify Explain Command, NetworkX, Graphify Path Command, BFS/DFS Query Traversal, Constrained Query Expansion

### Community 104 - "Native Task Spine CLI Fallback"
Cohesion: 0.33
Nodes (6): Native Task Spine CLI Fallback, Task Spine Verification Report, Task Spine CLI, Task Master State Path Reconciliation Notes, Task Master CLI Divergence (Anthropic-wire incompatibility), Task State Path Reconciliation (task_master_state.json -> tasks.json)

### Community 105 - "opencode-swarm.json"
Cohesion: 0.33
Nodes (5): agent_pools, control_agents, phase_1_agents, $schema, version

### Community 106 - "verify_worker_runtime.sh"
Cohesion: 0.60
Nodes (5): die(), log(), verify_worker_runtime.sh script, usage(), VERIFY_RESULTS_FILE

### Community 107 - "_DNSCache"
Cohesion: 0.13
Nodes (10): NetworkStream, _CachedDNSBackend, _DNSCache, Any, Drop one entry (used to invalidate a stale cached IP)., Resolve hostname to IP, consulting the in-process DNS cache first. Returns the…, httpcore sync backend that connects to a cached IP for each hostname.…, Lightweight TTL-bounded DNS cache to avoid repeated gethostbyname calls. All… (+2 more)

### Community 108 - "handle_run"
Cohesion: 0.33
Nodes (6): handle_run(), Registry entry for a background workflow run., Start a real agentic workflow on a background daemon thread (returns now).…, Start a real agentic workflow in a background daemon thread; return now., RunHandle, _spawn_agentic_run()

### Community 109 - "_simulate_reuse"
Cohesion: 0.40
Nodes (4): Simulate routing a task to a promoted agent and getting a response., Step: ROUTE & REUSE — Routing tasks to promoted agents., _simulate_reuse(), TestRouteAndReuse

### Community 110 - "TestCaptureStep"
Cohesion: 0.33
Nodes (4): Step 1: CAPTURE — Create a controlled learning scenario., A captured learning scenario produces a properly structured entry., A generic/non-specific entry should be identifiable as weak., TestCaptureStep

### Community 111 - "TestChains"
Cohesion: 0.18
Nodes (7): _fresh_caches(), fixture, Start each test with empty disk caches so patches don't leak across tests., Point webapp at a throwaway fabric-routes.json (never the real file)., Point swarm_profiles at a throwaway registry seeded with the on-disk profiles., TestChains, tmp_profiles_file()

### Community 114 - "promotion_policy"
Cohesion: 0.40
Nodes (5): promotion_policy, require_claim, require_evidence, require_task_link, write_durable_agent

### Community 115 - "package.json"
Cohesion: 0.40
Nodes (4): name, private, scripts, test

### Community 117 - "start_worker_runtime.sh"
Cohesion: 0.70
Nodes (4): die(), log(), start_worker_runtime.sh script, usage()

### Community 118 - "stop_agentic_services.sh"
Cohesion: 0.70
Nodes (4): is_protected(), kill_worker(), main(), stop_agentic_services.sh script

### Community 119 - "_FakeClient"
Cohesion: 0.21
Nodes (7): _FakeClient, _install_fake(), Response, Records the per-request timeout passed to post() without network I/O., test_dispatch_localhost_uses_local_connect_timeout(), test_dispatch_remote_keeps_configured_connect_timeout(), Timeout

### Community 122 - "_load_registry"
Cohesion: 0.25
Nodes (9): _load_registry(), Any, Load the provider registry (cached); return {} when missing/unreadable., Clear the cached registry and reload it from disk. Called after the provider…, reload_registry(), Persist one role -> alias mapping into PROVIDER_REGISTRY.json atomically. The…, Tier + registered-role -> litellm alias via model_routing resolution., _role_mapping() (+1 more)

### Community 124 - "Neo4j Export"
Cohesion: 0.50
Nodes (4): Neo4j Export (mirror), FalkorDB Export, Neo4j Export, SVG and GraphML Exports

### Community 125 - "CI Lint and Test"
Cohesion: 0.67
Nodes (4): ARC Kubernetes CI, CI Lint and Test, Secret Scan Job, Multi-Runner Parallel Check

### Community 126 - "phase_gates"
Cohesion: 0.50
Nodes (4): phase_gates, human_gate_before_full_concurrency, phase_1_required, phase_2_required

### Community 127 - "retry_policy"
Cohesion: 0.50
Nodes (4): retry_policy, backoff_factor, jitter, max_retries

### Community 128 - "discover_environment.sh"
Cohesion: 0.83
Nodes (3): critical_fail(), discover_environment.sh script, usage()

### Community 129 - "verify_proxy.sh"
Cohesion: 0.67
Nodes (3): check(), verify_proxy.sh script, TIERS

### Community 130 - "TestTargetRepoRoot"
Cohesion: 0.38
Nodes (3): Resolve the working repo the swarm writes into. ``SWARM_TARGET_REPO`` env var…, When SWARM_TARGET_REPO is unset and no sibling target repo exists,…, TestTargetRepoRoot

### Community 132 - "TestCLIStringFunctions"
Cohesion: 0.33
Nodes (4): cmd_status should handle a missing progress ledger gracefully., Test internal helper behaviors exposed through the CLI module., cmd_promote should not crash when called directly (uses fresh orchestrator)., TestCLIStringFunctions

### Community 133 - "Post-Commit Auto-Rebuild Hook"
Cohesion: 0.67
Nodes (3): AGENTS.md Native Integration, Post-Commit Auto-Rebuild Hook, Post-Commit Auto-Rebuild Hook (mirror)

### Community 145 - "TestLitellmPresenceInRoutes"
Cohesion: 0.40
Nodes (3): Role routing maps worker roles to litellm aliases, so every fabric tier must…, Worker-tier aliases route through the litellm gateway FIRST (42-key Gemini…, TestLitellmPresenceInRoutes

### Community 147 - "graphify reference: incremental update and cluster-only"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

### Community 148 - "Q: What is KeyPoolManager?"
Cohesion: 0.50
Nodes (3): Answer, Outcome, Q: What is KeyPoolManager?

## Knowledge Gaps
- **134 isolated node(s):** `$schema`, `version`, `name`, `description`, `root_dir` (+129 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PassthroughStreamingProxy` connect `PassthroughStreamingProxy` to `CircuitBreaker`, `_ChunkStream`, `_StallStream`, `StreamingProxyConfig`, `test_streaming_proxy.py`?**
  _High betweenness centrality (0.121) - this node is a cross-community bridge._
- **Why does `create_app()` connect `webapp.py` to `PassthroughStreamingProxy`, `handle_run`, `_run_latency_test`?**
  _High betweenness centrality (0.121) - this node is a cross-community bridge._
- **Why does `MultiLayeredAgenticOrchestrator` connect `MultiLayeredAgenticOrchestrator` to `TestModelRoleUpdate`, `SubTask`, `webapp.py`, `TestRun`, `test_webapp.py`, `handle_run`, `WorkerRole`, `TestChains`, `TestLatencyTest`, `.run_full_agentic_workflow`, `TestReports`, `TestRunFullAgenticWorkflow`, `ProxyServerDaemon`, `TestRunPlan`, `services/__init__.py`, `TaskStatus`?**
  _High betweenness centrality (0.099) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `KeyPoolManager` (e.g. with `isolated_key_pool()` and `TestCLIStringFunctions`) actually correct?**
  _`KeyPoolManager` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 29 inferred relationships involving `SubTask` (e.g. with `ConcurrencyRampController` and `DurableAgentRouter`) actually correct?**
  _`SubTask` has 29 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `MultiLayeredAgenticOrchestrator` (e.g. with `AgentType` and `WorkerRole`) actually correct?**
  _`MultiLayeredAgenticOrchestrator` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `MultiProviderFabric` (e.g. with `FastFallbackConfig` and `FastFallbackRouter`) actually correct?**
  _`MultiProviderFabric` has 19 INFERRED edges - model-reasoned connections that need verification._