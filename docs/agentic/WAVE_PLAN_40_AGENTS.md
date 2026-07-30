# Ultra-Scale Workflow Plan: 40+ Agents

**Version:** 1.0.0
**Date:** 2026-07-30T14:35Z
**Workflow type:** Multi-phase pipeline with learning loop interleaving

---

## Workflow Structure

```
Phase 0: Registry Compaction ───────────────── (1 agent)
Phase 1: Gap Closure ───────────────────────── (2 agents)
Phase 2: Core Code Improvements ────────────── (5 agents)
Phase 3: Infrastructure Build ──────────────── (4 agents)
Phase 4: Learning Loop ─────────────────────── (3 agents)
Phase 5: Synthesis & Documentation ─────────── (3 agents)
Phase 6: Cold-Path Promotion ───────────────── (2 agents)
                                         ─────────
                  Total per cycle:       20 agents
                                         (40+ with verify/retry)
```

---

## Phase 0: Registry Compaction (P0)

**Goal:** Clean duplicated entries from all 3 cold-path registries.

**Agent 0.1 — Compact knowledge.jsonl**
- Read `docs/agentic/registry/knowledge.jsonl`
- Group by `id`, keep only the LAST occurrence of each ID
- Remove entries with empty/null `solution` field
- Write deduplicated result back
- Report: entries before → after

**Agent 0.2 — Compact agents.jsonl**
- Read `docs/agentic/registry/agents.jsonl`
- Group by `category`, keep last per category
- Remove agents where `derived_from_learnings` entries no longer exist in knowledge.jsonl
- Write deduplicated result back
- Report: entries before → after

**Agent 0.3 — Compact chain.jsonl**
- Read `docs/agentic/registry/chain.jsonl`
- Group by `source_learning_id`, keep last per source
- Remove entries referencing removed agents or learnings
- Write result back

---

## Phase 1: Gap Closure (P1)

**Goal:** Close the 2 unresolved spec gaps.

**Agent 1.1 — GAP-01: SSE streaming proxy support**
- File: `proxy/claude_proxy_server.py`
- Read current proxy implementation
- Verify streaming format compatibility
- Either implement or document why deferred
- Update GAP-01 status in tasks.json

**Agent 1.2 — GAP-02: Task Master format reconciliation**
- Files: `services/task_master_service.py`, `.taskmaster/tasks/tasks.json`
- Compare current Python service output format with real `task-master-ai` CLI format
- Document the divergence and compatibility strategy
- Update GAP-02 status

---

## Phase 2: Core Code Improvements (P0/P1)

**Goal:** Implement 5 critical code improvements.

**Agent 2.1 — Concurrency Ramp Controller**
- File: `services/opencode_swarm_service.py`
- Implement `ConcurrencyRampController` class
- Read `ramp_sequence` from config (hardcoded: `[4, 8, 16, 24, 40]`)
- Expose `get_current_max_workers(gate_level)` method
- Replace hardcoded `max_workers=10` in `execute_subtask_batch_parallel()`
- Add gate dependency: ramp only when wave gate passes
- Unit tests for ramp progression

**Agent 2.2 — Ownership Enforcement Gate**
- File: `services/wave_gate_service.py`
- In `evaluate_gate_criteria()`, add ownership check
- Read `ownership-map.json` pools and their `owned_paths`
- For each subtask in the wave, verify proposed output paths are within the pool's `owned_paths`
- Block wave advance if any subtask violates ownership boundaries
- Log violations to progress ledger

**Agent 2.3 — .claude/agents/ Spec Writer**
- File: `services/agent_factory_service.py`
- After cold-path creates an entry in `agents.jsonl`, write a corresponding `.claude/agents/{agent_id}.md`
- Format per AGENT_SPEC_CONTRACT: name, id, category, type, system_prompt, owned_tasks, TTL
- Create dedicated `_write_agent_spec_file(agent_spec: dict)` method
- Handle existing files via `if exists, skip` (don't overwrite)

**Agent 2.4 — Anomaly → Hot Path Wiring**
- File: `tools/agentic_orchestrator.py`
- In the main workflow loop, catch exceptions from `execute_subtask_batch_parallel`
- For each failed subtask, call `default_progress_ledger.handle_task_failure(error, task_id)`
- Then call `default_knowledge_cache.add_learning()` with error details
- Then call `default_agent_factory.spawn_from_learning()` for HIGH severity
- Log the full remediation chain

**Agent 2.5 — Pool-Level Health Tracking**
- File: `services/opencode_swarm_service.py`
- Extend `WorkerPoolState` with pool-level breakdown
- Add `pool_health: Dict[str, Dict]` tracking active/failed/rate-limited per pool
- Update counters in `execute_subtask_with_worker()` on success/failure
- Expose `get_pool_summary()` method

---

## Phase 3: Infrastructure Build (P1)

**Goal:** Create the reusable infrastructure for durable operation.

**Agent 3.1 — Operational Documentation Suite**
- Create `docs/agentic/RUNBOOK.md` — how to start, run, stop, recover
- Create `docs/agentic/AGENT_SPEC_CONTRACT.md` — agent file format contract
- Create `docs/agentic/KNOWLEDGE_BOX_SCHEMA.md` — knowledge entry schema
- All three must match actual registry formats exactly
- Include example entries from the current registries

**Agent 3.2 — Base Commands for .claude/commands/**
- Create status command showing registry counts, pool health, phase state
- Create promote command for manual cold-path promotion
- Create dedup command for registry compaction
- Each command is a brief markdown file with description + invocation

**Agent 3.3 — Reusable Skills for .claude/skills/**
- Create `wave-gate-check` skill: template for evaluating gate criteria
- Create `cold-promote` skill: template for promoting a learning batch
- Create `obstacle-handle` skill: template for error → playbook → remediation
- Each skill is a markdown file with trigger, steps, output template

**Agent 3.4 — Variable Precedence Module**
- Create `config/resolver.py` module
- Implement precedence chain: CLI flag > shell env > .env > config default > hardcoded
- Expose `resolve(key, default=None)` function
- Wire into key_pool and fabric initialization

---

## Phase 4: Learning Loop Activation (P1/P2)

**Goal:** Wire the interwoven learning loop.

**Agent 4.1 — Content-Based Learning Classification**
- File: `tools/knowledge_cache.py`
- Add `classify_content(title, description) -> str` method
- Use keyword analysis to auto-assign category (expand beyond 6 fixed categories)
- Generate diverse solution text based on input content (not generic template)
- Add `solution_hash` field for content-level dedup

**Agent 4.2 — Cross-Registry Referential Integrity**
- Verify all `derived_from_learnings` refs in agents.jsonl exist in knowledge.jsonl
- Verify all `source_learning_id` refs in chain.jsonl exist in knowledge.jsonl
- Verify all `spawned_agent_id` refs in chain.jsonl exist in agents.jsonl
- Remove or flag orphaned references
- On each cold-path run, check integrity before writing

**Agent 4.3 — Auto-Compaction at End of Each Run**
- File: `tools/agentic_orchestrator.py`
- After `_promote_cold_path()` completes, auto-compact all 3 registries
- Use simple dedup-by-ID strategy
- Log entries removed vs kept

---

## Phase 5: Synthesis & Documentation (P0)

**Goal:** Execute EPIC-05, close the synthesis loop.

**Agent 5.1 — EPIC-05 TASK-05-1: Completion Report**
- Aggregate data from all sources:
  - progress.json (overall %, phase status)
  - tasks.json (epics completed/pending)
  - spawn_chain_registry.json (entry count)
  - knowledge_cache (hot cache size)
  - knowledge.jsonl, agents.jsonl, chain.jsonl (registry sizes)
- Generate structured completion report at `docs/agentic/completion_report.json`
- Include: files created/modified, learning captured, agents promoted, blockers remaining

**Agent 5.2 — EPIC-05 TASK-05-2: PRD Revision**
- Update `PRD_V2_EXECUTION_READY.md` with completion status
- Mark completed FR items as DONE
- Add new findings and improvements

**Agent 5.3 — EPIC-05 TASK-05-3: Improvement Recommendations**
- Write `docs/agentic/IMPROVEMENT_RECOMMENDATIONS.md`
- Capture: unresolved blockers, repeated fix patterns, provider performance data
- Recommend next wave of work

---

## Phase 6: Cold-Path Promotion (P0)

**Goal:** Promote any new learnings from this workflow run.

**Agent 6.1 — Identify Promoteable Patterns**
- Scan hot cache for learnings not yet in promoted_learning_ids
- Group by category
- For categories with ≥3 learnings not yet promoted, flag for promotion

**Agent 6.2 — Execute Promotion**
- Run cold-path promotion for flagged learnings
- Write `.claude/agents/` spec files
- Update chain registries
- Save promoted_learning_ids.json

---

## Verification Gates

Between each phase, check:
1. All agents in phase completed successfully
2. Registry state is consistent after writes
3. No syntax errors introduced
4. Promoted_learning_ids saved

## Learning Loop Integration Points

- **Phase 2** (code improvements) → each improvement creates learning entry
- **Phase 4** (learning loop) → classifications feed into cold-path
- **Phase 6** (promotion) → learnings become durable agents
