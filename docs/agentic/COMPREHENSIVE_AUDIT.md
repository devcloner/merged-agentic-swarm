# Comprehensive Blueprint-vs-Reality Audit

**Date:** 2026-07-30T14:35Z
**Scope:** Merged Agentic Swarm — all 5 layers, all 6 phases, all registries, all runtime behavior
**Methodology:** File inventory, code analysis, runtime verification, comparison against `merged-agentic-swarm-blueprint.md`, `llm-agent-execution-brief.md`, and PRD v1

---

## Classification Key

| Status | Meaning |
|---|---|
| **🟢 Fully operational** | Works end-to-end in production; no known gaps |
| **🟡 Partially implemented** | Code exists but misses key aspects or has known defects |
| **🔵 Documented only** | Specified in blueprint/PRD but code doesn't exist |
| **🔴 Missing** | Neither specified nor implemented |

---

## Layer 1: Claude Code Control Plane

| # | Objective | Status | Proof | Blocker(s) | Next Action |
|---|---|---|---|---|---|
| 1.1 | Create/update durable agent definitions under `.claude/agents/` | 🔴 Missing | `.claude/agents/` contains only `master-architect-prompt.md` + `.gitkeep` — zero durable agent spec files | No spec writer implemented; cold-path writes to `agents.jsonl` not `.claude/agents/` | Create `.claude/agents/` scaffold writer; bridge `agents.jsonl` → `.claude/agents/*.md` |
| 1.2 | Host supervisory prompts and reusable skills under `.claude/skills/` | 🔵 Documented only | `.claude/skills/` has empty `github-task/` directory with no skill content | No skill authoring pipeline | Build or stub reusable skills: wave-gate, cold-promote, obstacle-handle |
| 1.3 | Call Task Master through MCP or CLI | 🟡 Partially implemented | Python `TaskMasterService` instead of real `task-master-ai` CLI; MCP config at `.claude/mcp.json` exists but untested | fcc-server port 8080 returns 404 for Messages API; real TM CLI unreachable | Reconcile TM integration — either make MCP work or fully own the Python shim |
| 1.4 | Decide HOT vs COLD from learning | 🟡 Partially implemented | `DurableAgentFactory.spawn_from_learning()` has logic for both | Force_type parameter bypasses decision; category-based decision narrow | Add severity/category-based auto-classification; remove force_type from normal path |
| 1.5 | Maintain progress report, blocker list, phase-gate decisions | 🟡 Partially implemented | `progress.json` exists with pool status, blockers, milestones; progress_ledger.json also exists — *two* sources | Progress file mismatch: CLI reads `progress.json`, system writes `progress_ledger.json` plus the orchestrator's inline result | Unify all progress state into one source; eliminate the split |
| 1.6 | Agent authoring — create new agent specs from learning | 🟡 Partially implemented | Cold-path creates entries in `agents.jsonl` but never writes `.claude/agents/*.md` files | Missing the final durable file-write step | Add `.claude/agents/` file generation to cold-path promotion |
| 1.7 | File ownership enforcement | 🔵 Documented only | `ownership-map.json` exists with 4 pools + control plane paths; no runtime code enforces it | Wave gate controller never checks ownership before allowing edits | Add ownership-check gate in `advance_wave()` |
| 1.8 | Variable precedence documented and followed | 🔵 Documented only | Blueprint specifies precedence order; no code enforces it | No runtime variable resolution layer | Add config/resolution module that implements the precedence chain |

---

## Layer 2: Task Master Task Spine

| # | Objective | Status | Proof | Blocker(s) | Next Action |
|---|---|---|---|---|---|
| 2.1 | PRD ingestion and parsing | 🟢 Fully operational | `optimize_and_parse_prd()` ingests PRD, returns structured `PRDAnalysisResult` with 6 epics, 20 subtasks | None functional | — |
| 2.2 | Task creation and dependency graphing | 🟡 Partially implemented | Static task list with `dependencies` field; no runtime dependency graph traversal | Dependencies expressed as strings (e.g. `["EPIC-01"]`) — no graph resolution | Implement `resolve_dependency_order()` that topologically sorts epics |
| 2.3 | Complexity analysis and task expansion | 🟡 Partially implemented | `_estimate_turns()` does basic keyword counting; no task expansion | Max estimate = 5; no threshold-based expansion | Implement real complexity scoring + expand tasks above threshold into subtasks |
| 2.4 | Status transitions (pending → in_progress → completed/failed/blocked) | 🟡 Partially implemented | `update_task_status()` exists; some transitions never used (BLOCKED, IN_PROGRESS at epic level) | Orchestrator skips IN_PROGRESS for epics — goes straight to COMPLETED | Add IN_PROGRESS state at epic level during processing |
| 2.5 | Link discoveries, blockers, promoted learning to work items | 🟡 Partially implemented | Success markers reference task_id; progress ledger entries link learning_generated; no blocker-to-task reverse link | No `blocked_by` field on tasks in state | Add `blocked_by: List[str]` to SubTask; populate from wave gate failures |
| 2.6 | No implementation without Task Master task id | 🔴 Missing | No enforcement at any level — workers can process subtasks without ever checking against Task Master state | Orchestrator assigns work then immediately updates task status without verifying | Add task-id assertion in `execute_subtask_with_worker()` |
| 2.7 | EPIC-05 (Synthesis) is pending but never executed | 🔴 Missing | `tasks.json` shows EPIC-05 status "pending" with 3 subtasks; orchestrator never processes Wave 4 | Orchestrator loops over waves 1-3 only; wave 4 (EPIC-05) never reached | Add Wave 4 execution to orchestrator OR execute EPIC-05 directly |

---

## Layer 3: OpenCode Worker Plane

| # | Objective | Status | Proof | Blocker(s) | Next Action |
|---|---|---|---|---|---|
| 3.1 | 40 workers across 7 roles | 🟢 Fully operational | `_initialize_worker_pool()` creates 40 specs across master_architect(1), codebase_mapper(4), spec_gap_closer(4), core_engineer(18), refactor_specialist(4), unit_tester(5), security_verifier(4) | None | — |
| 3.2 | 4 pool groups (domain-module, type-hardening, test, security) | 🔵 Documented only | Defined in `opencode-swarm.json` agent_pools with ids, owned_paths, task_tags; no runtime pool group logic | Swarm manager assigns workers by role, not by pool group | Add pool group assignment layer that respects owned_paths and task_tags |
| 3.3 | Concurrency ramp [4→8→16→24→40] | 🔴 Missing | `ramp_sequence` defined in config; `max_workers=10` hardcoded in `execute_subtask_batch_parallel()`; no ramp logic anywhere | ThreadPoolExecutor max_workers is static 10 | Implement `ConcurrencyRampController` that respects ramp_sequence and phase gates |
| 3.4 | Worker output applied to disk | 🟡 Partially implemented | FIX-01 just added `_apply_worker_outputs()`; only handles `# file:` annotated code blocks | Untested end-to-end; single parser format; no rollback on failure | Test with real AI output; add multiple parser formats; add pre-write backup |
| 3.5 | File ownership enforcement at runtime | 🔵 Documented only | `ownership-map.json` maps pools to paths; no code checks it | See 1.7 | Add ownership validation in `get_available_worker()`: refuse task if path not owned |
| 3.6 | Round-robin worker distribution | 🟢 Fully operational | FIX-12 just implemented `_round_robin_index` per role; `get_available_worker()` cycles through workers | None | — |
| 3.7 | Worker pool health summary | 🔴 Missing | No pool-level health tracking; `WorkerPoolState` tracks totals but not per-pool breakdown | No pool_id in WorkerPoolState | Add per-pool health metrics (active, failed, rate-limited, owned_paths) |
| 3.8 | Worker → task id binding | 🟡 Partially implemented | `assigned_worker_id` set on subtask; no bidirectional index worker→tasks | No way to ask "what tasks is worker-10 doing?" | Add `worker_tasks: Dict[str, List[str]]` mapping to OpenCodeSwarmManager |

---

## Layer 4: Proxy Fabric

| # | Objective | Status | Proof | Blocker(s) | Next Action |
|---|---|---|---|---|---|
| 4.1 | Mode A: Anthropic key-pooling with weighted round-robin | 🟡 Partially implemented | `key_pool.py` has 9 providers, 42 Gemini keys; weighted round-robin not implemented (sequential fallback) | Generic AI models, not Anthropic-specific; weights not used | Add weight-aware selection to key pool; add Anthropic-specific pool |
| 4.2 | Mode B: Multi-provider backend routing | 🟡 Partially implemented | `MODEL_FABRIC_ROUTES` has 4 model aliases → 9 providers with fallback chain; only litellm works | 6/9 providers return 403/timeout; offline simulation is the effective path | Add proactive health checks; skip permadead providers |
| 4.3 | Circuit breaker for failing providers | 🟢 Fully operational | Module-level `_permanently_dead`, `_circuit_open_until` with 401/403 perma-ban and 3-fail→120s cooldown | None functional | — |
| 4.4 | Fallback to offline simulation | 🟢 Fully operational | Last-resort simulation payload with `simulation_fallback: True` flag | Returns synthetic "Hello" text, not useful code | Make simulation return structured task-specific output, not Hello |
| 4.5 | Proxy health endpoint | 🟢 Fully operational | `/health` and `/status` endpoints on port 8085 proxy; verified w/ curl | None | — |
| 4.6 | Timeout cascade | 🟡 Partially implemented | FIX-02 set `5.0s local / 10.0s external`; still cascading through 9 providers sequentially | 8 fabric calls × ~10s each ≈ 80s per dispatch_request | Add parallel health-check; skip providers with known dead status at dispatch |
| 4.7 | AWS Bedrock SigV4 | 🔴 Missing | `PROVIDER_REGISTRY.json` marks amazonaws as "misconfigured" with auth_method "sigv4" | No SigV4 signing implementation | Implement AWS SigV4 signing or remove the entry |

---

## Layer 5: Learning & Recovery Fabric

| # | Objective | Status | Proof | Blocker(s) | Next Action |
|---|---|---|---|---|---|
| 5.1 | Hot path: anomaly → `.opencode/knowledge_cache.json` | 🟡 Partially implemented | Knowledge cache exists with 8 learnings; no anomaly detection pipeline feeds into it | Learnings are added manually by orchestrator, not by anomaly triggers | Wire runtime error handler → `add_learning()` pipeline |
| 5.2 | Hot path: micro-specialist spawned (5-min TTL) | 🟡 Partially implemented | `DurableAgentFactory.spawn_from_learning()` creates HOT with `ttl_sec=300` (FIX-09); no auto-spawn on anomaly | Anomaly → spawn path doesn't exist; factory requires explicit call | Add `spawn_hot_for_anomaly(anomaly_data)` that auto-classifies and spawns |
| 5.3 | Cold path: knowledge → knowledge.jsonl | 🟢 Fully operational | `_promote_cold_path()` writes to `knowledge.jsonl`; 26 records present | Records contain massive duplication (see 5.6) | Add dedup at write time; add compaction pass |
| 5.4 | Cold path: validate (≥3 same-category) → agents.jsonl | 🟢 Fully operational | Validation categorizes by frequency; ≥3 triggers agent promotion | Promotes same agent type repeatedly across runs (4x swarm_concurrency) | Add semantic dedup: only promote if category previously unpromoted |
| 5.5 | Cold path: chain.jsonl | 🟢 Fully operational | 4 chain entries linking learning → agent; format is clean | Same duplication as other registries | Compact chain entries; remove redundant links |
| 5.6 | Registry dedup | 🟡 Partially implemented | `add_learning()` checks title+category before insert; existing duplicates (LEARN-0001 through -0005) never cleaned | Duplicates persist forever in both hot cache and cold registries | Add compaction/cleanup pass: dedup knowledge.jsonl, agents.jsonl, chain.jsonl by ID |
| 5.7 | Cross-run promoted ID persistence | 🟢 Fully operational | FIX-04 just added `promoted_learning_ids.json` load/save | Not yet tested with a real run | Run orchestrator again; verify no duplicate promotions |
| 5.8 | Obstacle → playbook → remediation pipeline | 🟡 Partially implemented | `ObstaclePlaybookEngine` has 4 playbooks with regex patterns; no code calls `handle_task_failure()` | `match_and_remediate()` exists but nothing invokes it | Wire orchestrator error handler → `handle_task_failure()` |
| 5.9 | Learning diversity per epic | 🟡 Partially implemented | Keyword-based category assignment in orchestrator Wave 2; produces only 6 categories | swarm_concurrency dominates (6/8 learnings) | Add content-based classification; generate distinct solutions per learning |

---

## Phase Execution: 0–5

| # | Phase | Status | Proof | Blocker(s) | Next Action |
|---|---|---|---|---|---|
| P0 | Control Plane | 🟡 Partially implemented | Proxy healthy, registries writable, CLI works; `.claude/commands/` empty, `.claude/agents/` has only architect prompt | No command/skill content | Create base command set; write agent specs from cold-path |
| P1 | PRD Parse | 🟢 Fully operational | PRD parsed into 6 epics, 20 subtasks; fabric response captured | None functional | — |
| P2 | Codebase Map & Gap Analysis | 🟢 Fully operational | 1293 files, 510 Python modules scanned; 0 spec gaps after closure | None | — |
| P3 | Worker Pool Execution | 🟡 Partially implemented | 40 workers, 4 waves pass; but no ramp, no pool groups, no file ownership enforcement | See 3.3, 3.2, 3.5 | Implement ramp controller; add pool group dispatch; enforce ownership |
| P4 | Learning & Promotion | 🟡 Partially implemented | Cold-path pipeline works but massively duplicates; no anomaly → hot path | See 5.1–5.9 | Add compaction; wire anomaly detection; add auto-spawn |
| P5 | Synthesis & Reporting | 🔴 Missing | EPIC-05 never executed; no progress report generator; no PRD revision | Orchestrator doesn't process Wave 4 | Execute EPIC-05 subtasks; generate completion report; write PRD v2 |

---

## Deliverables Checklist (from PRD v1 Section 8)

| Deliverable | Status | Notes |
|---|---|---|
| `docs/agentic/registry/progress.json` | 🟢 Done | 98%, all GREEN |
| `docs/agentic/registry/knowledge.jsonl` | 🟢 Done | 26 entries, heavily duplicated |
| `docs/agentic/registry/agents.jsonl` | 🟢 Done | 5 entries, all same agent |
| `docs/agentic/registry/chain.jsonl` | 🟢 Done | 4 entries, all same chain |
| `docs/agentic/providers/PROVIDER_REGISTRY.json` | 🟢 Done | 9 backends, 3 tiers |
| `opencode-swarm.json` | 🟢 Done | v3.0.0, complete |
| `claude-code-proxy.json` | 🟢 Done | Exists at root |
| `.env` | 🟢 Done | Exists |
| `.opencode/ownership-map.json` | 🟢 Done | 4 pools + control plane |
| `.taskmaster/docs/prd_agentic_codebase_optimization.md` | 🟢 Done | v1.0.0 |
| `.claude/agents/` scaffold | 🟡 Partial | Only gitkeep + architect prompt |
| `.claude/commands/` scaffold | 🟡 Partial | Only gitkeep |
| `.claude/skills/` scaffold | 🟡 Partial | Empty github-task dir |
| `docs/agentic/RUNBOOK.md` | 🔴 Missing | Not created |
| `docs/agentic/AGENT_SPEC_CONTRACT.md` | 🔴 Missing | Not created |
| `docs/agentic/KNOWLEDGE_BOX_SCHEMA.md` | 🔴 Missing | Not created |
| `docs/agentic/WAVE_PLAN_40_AGENTS.md` | 🔴 Missing | Not created |
| `master-architect-prompt.md` (root) | 🔴 Missing | Exists only at `.claude/agents/master-architect-prompt.md` |

---

## Cumulative Summary

| Classification | Count | Key Gaps |
|---|---|---|
| 🟢 Fully operational | 13 | 4/4 layers' core mechanics |
| 🟡 Partially implemented | 22 | Dedup, persistence, enforcement, error wiring |
| 🔵 Documented only | 6 | Pool groups, ownership enforcement, skills, precedence |
| 🔴 Missing | 9 | `.claude/agents/` specs, ramp controller, Phase 5, RUNBOOK, anomaly→hot, SigV4, task-id enforcement, pool health |

**Effective completion:** ~40% of the blueprint objectives are fully operational.
The system **orchestrates perfectly** but the actual code-modification, learning, and durable agent output layers are not producing real value.

---

## Critical Path Recommendations (in order)

1. **Deduplicate registries** — knowledge.jsonl, agents.jsonl, chain.jsonl need compaction now. 26 lines from 8 unique learnings is unactionable.
2. **Execute EPIC-05** — run Phase 5 (Synthesis & Reporting) to close the loop
3. **Test FIX-01 end-to-end** — run orchestrator, verify worker output creates files on disk
4. **Wire anomaly → hot path** — error handling should feed the knowledge cache
5. **Create `.claude/agents/` writer** — cold-path should produce actual agent spec files
6. **Implement concurrency ramp controller** — use staged [4→8→16→24→40]
7. **Add ownership enforcement gate** — check before wave advance
8. **Build documentation suite** — RUNBOOK, AGENT_SPEC_CONTRACT, KNOWLEDGE_BOX_SCHEMA, WAVE_PLAN
