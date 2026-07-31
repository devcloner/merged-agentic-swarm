# Operator Runbook — Merged Agentic Swarm OS

**Version:** 1.0.0
**Date:** 2026-07-31
**Audience:** Operator / DevOps engineer managing the autonomous development runtime.

---

## Quick Start

```bash
cd /home/ubuntu

# Run the complete smoke test workflow (all subsystems)
./scripts/agentic/run_smoke_workflow.sh

# Run only critical subsystems
./scripts/agentic/run_smoke_workflow.sh --only proxy,spine,worker1

# Skip non-critical steps
./scripts/agentic/run_smoke_workflow.sh --skip learning,durable

# Generate progress report from smoke results
./scripts/agentic/generate_progress_report.sh

# Stop all agentic worker processes
./scripts/agentic/stop_agentic_services.sh

# Forcibly stop (skip SIGTERM grace period)
./scripts/agentic/stop_agentic_services.sh --force
```

---

## Architecture Overview

```
+=====================================================================+
|                  MERGED AGENTIC SWARM OS (v2)                        |
+=====================================================================+
                                                                       |
.-----------+----------------------------------------------------------'
|           |
|  Layer 1: CLAUDE CODE CONTROL PLANE (supervisor)
|           |
|    +-----------+   +----------+   +-------------------+
|    |  Agent    |   |  Skills  |   |  Phase Gatekeeper |
|    |  Factory  |   |  (.md)   |   | (wave_gate)       |
|    +-----+-----+   +-----+----+   +---------+---------+
|          |               |                  |
|    Writes .claude/agents/*.md              |
|    Evaluates gate criteria                  |
|           |                                 |
.-----------+---------------------------------+-----------------------.
|           |                                 |                        |
|  Layer 2: TASK MASTER TASK SPINE            |                        |
|           |                                 |                        |
|    .taskmaster/tasks/tasks.json  <----------+  (single truth)       |
|    PRD -> epics -> subtasks -> completion tracking                   |
|    progress_ledger.json (continuous state log)                       |
|    spawn_chain_registry.json (who-spawned-who)                       |
|           |                                                          |
.-----------+----------------------------------------------------------.
|           |                                                          |
|  Layer 3: OPENCODE WORKER PLANE (40 workers, 7 roles)               |
|           |                                                          |
|    Pool groups: [4] [8] [16] [24] [40]  concurrency ramp            |
|    +- pool-01 (audit/analysis) ---+                                   |
|    +- pool-02 (refactor/docs)  ---+                                   |
|    +- pool-03 (test/fix)       ---+  round-robin assignment          |
|    +- pool-04 (integration)    ---+                                   |
|           |                                                          |
.-----------+----------------------------------------------------------.
|           |                                                          |
|  Layer 4: MULTI-PROVIDER PROXY FABRIC                                |
|           |                                                          |
|    +------------+   +----------+   +-----------+   +--------+       |
|    |  fcc-server |   |  opencode |   |  gemini   |   | groq   | ...   |
|    |  :8080      |   |  :8085   |   |  (direct) |   | (no k) |       |
|    +------+------+   +-----+----+   +-----+-----+   +---+----+       |
|           |                |              |              |
|    Circuit breaker, perma-ban, simulation fallback
|           |
.-----------+----------------------------------------------------------.
|           |
|  Layer 5: LEARNING & RECOVERY FABRIC
|           |
|    Hot path:  anomaly -> knowledge_cache -> micro-specialist (300s)
|    Cold path: validated -> knowledge.jsonl -> agent spec -> .claude/agents/
|    Dedup: by ID, by content hash, cross-run persistence
|           |
'-----------+----------------------------------------------------------'
```

### Data Flow (read direction)

```
Operator
  |
  v
run_smoke_workflow.sh  ---> discover_environment.sh  ---> environment-facts.json
  |                            (Layer 1 audit)              (docs/agentic/audit/)
  v
verify_proxy.sh         ---> curl :8085/health        ---> smoke-test-results.json
  |                            (Layer 4 health)             (config/runtime/)
  v
start_task_spine.sh     ---> agentic_cli.py run        ---> tasks.json, progress_ledger.json
  |                            (Layer 2 bootstrap)          (.taskmaster/tasks/)
  v
start_worker_runtime.sh ---> opencode swarm spawn      ---> /tmp/agentic-worker-*.pid
  |                            (Layer 3 launch)             (worker PID tracking)
  v
verify_worker_runtime.sh --> check worker outputs       ---> applied file changes on disk
  |
  v
run_learning_loop_test.sh -> knowledge_cache promote   ---> knowledge.jsonl, agents.jsonl
  |
  v
load_durable_agents.sh   --> .claude/agents/*.md read  ---> active agent specs loaded
  |
  v
generate_progress_report.sh --> PROGRESS_REPORT.md      ---> docs/agentic/PROGRESS_REPORT.md
```

---

## Component Descriptions

### Orchestration Scripts

| Script | Purpose | Path |
|--------|---------|------|
| `run_smoke_workflow.sh` | Master smoke test pipeline — runs all subsystems in order | `scripts/agentic/` |
| `discover_environment.sh` | Baseline discovery: OS, runtimes, ports, providers | `scripts/agentic/` |
| `verify_proxy.sh` | Proxy health check at specified tier (all, api, auth) | `scripts/agentic/` |
| `start_task_spine.sh` | Initialize and launch Task Master state | `scripts/agentic/` |
| `verify_task_spine.sh` | Confirm Task Master initialized correctly | `scripts/agentic/` |
| `start_worker_runtime.sh` | Launch OpenCode worker pool (configurable count) | `scripts/agentic/` |
| `verify_worker_runtime.sh` | Confirm workers producing valid output | `scripts/agentic/` |
| `run_learning_loop_test.sh` | Exercise hot->cold promotion pathway | `scripts/agentic/` |
| `load_durable_agents.sh` | Load persisted agent specs into runtime | `scripts/agentic/` |
| `generate_progress_report.sh` | Assemble all evidence into PROGRESS_REPORT.md | `scripts/agentic/` |
| `stop_agentic_services.sh` | Gracefully stop all tracked worker processes | `scripts/agentic/` |

### Python Services

| Service | Module | Purpose |
|---------|--------|---------|
| Orchestrator CLI | `tools/agentic_cli.py` | Main entry point (`run`, `status`, `config`, `promote`) |
| Orchestrator Engine | `tools/agentic_orchestrator.py` | Full workflow execution, phase gating |
| Knowledge Cache | `tools/knowledge_cache.py` | Hot-path learning with TTL, dedup, promotion |
| Multi-Provider Fabric | `providers/multi_provider_fabric.py` | AI model dispatch with circuit-breaking |
| Key Pool | `providers/key_pool.py` | API key lifecycle management |
| Task Master Service | `services/task_master_service.py` | PRD parsing, task state machine |
| OpenCode Swarm Service | `services/opencode_swarm_service.py` | Worker pool execution, concurrency ramp |
| Agent Factory Service | `services/agent_factory_service.py` | HOT/COLD agent spawning from learnings |
| Wave Gate Service | `services/wave_gate_service.py` | Gated phase control, ownership enforcement |
| Progress Ledger Service | `services/progress_ledger_service.py` | Continuous state logging |
| Codebase Map Service | `services/codebase_map_service.py` | AST scanning, spec gap detection |
| Claude Proxy Server | `proxy/claude_proxy_server.py` | API proxy on port 8085 |

### Key State Paths

| Purpose | Path |
|--------|------|
| Task Master state | `.taskmaster/tasks/tasks.json` |
| Progress ledger | `.taskmaster/tasks/progress_ledger.json` |
| Spawn chain registry | `.taskmaster/tasks/spawn_chain_registry.json` |
| Promoted learning IDs | `.taskmaster/promoted_learning_ids.json` |
| Hot knowledge cache | `.opencode/knowledge_cache.json` |
| Ownership map | `.opencode/ownership-map.json` |
| Cold knowledge registry | `docs/agentic/registry/knowledge.jsonl` |
| Cold agent registry | `docs/agentic/registry/agents.jsonl` |
| Cold chain registry | `docs/agentic/registry/chain.jsonl` |
| Progress report (generated) | `docs/agentic/PROGRESS_REPORT.md` |
| Environment facts | `docs/agentic/audit/environment-facts.json` |
| Baseline audit | `docs/agentic/audit/BASELINE_AUDIT.md` |
| Smoke test results | `config/runtime/smoke-test-results.json` |
| Durable agent specs | `.claude/agents/*.md` |
| Worker PID files | `/tmp/agentic-worker-*.pid` |
| Smoke step logs | `/tmp/smoke-step-*.log` |
| PRD v2 | `docs/agentic/PRD_V2_EXECUTION_READY.md` |
| PRD v1 | `.taskmaster/docs/prd_agentic_codebase_optimization.md` |

### Port Map

| Port | Service | Role | Protected |
|------|---------|------|-----------|
| 8080 | fcc-server | Primary model proxy (200 models) | YES — never stop |
| 8085 | node proxy | Secondary API proxy | YES — never stop |
| 8000 | sub-agent-mcp | MCP agent server | YES — never stop |
| 4000 | liteLLM | (dead — not running) | No |
| 3000 | docker-proxy | Container networking | YES — never stop |

---

## Common Operations

### 1. Start: Full System Verification

```bash
./scripts/agentic/run_smoke_workflow.sh
```

This runs the entire pipeline: discover -> proxy -> spine -> workers -> learning -> durable -> report.
At the end, you will see a summary table and a machine-readable JSON file.

**Expected output:** `config/runtime/smoke-test-results.json` with `"verdict": "pass"`.

### 2. Start: Quick Critical-Only Check

```bash
./scripts/agentic/run_smoke_workflow.sh --only proxy,spine,worker1
```

Runs only the three critical subsystems. Use this before launching the full orchestrator if you trust the other subsystems.

### 3. Verify: Single Subsystem

```bash
# Proxy only
./scripts/agentic/run_smoke_workflow.sh --only proxy

# Workers only (non-critical, so failure is advisory)
./scripts/agentic/run_smoke_workflow.sh --only worker2 --skip worker2

# Actually run worker verification:
./scripts/agentic/run_smoke_workflow.sh --only worker2
```

### 4. Stop: All Worker Processes

```bash
# Graceful (SIGTERM, 5s wait, SIGKILL)
./scripts/agentic/stop_agentic_services.sh

# Force (SIGKILL immediately)
./scripts/agentic/stop_agentic_services.sh --force
```

**This script will NEVER kill:** fcc-server, sub-agent-mcp, docker-proxy, or any process not in our PID files.

### 5. Stop: Individual Worker

```bash
# Find the PID file
ls /tmp/agentic-worker-*.pid

# Kill that specific worker
kill -TERM $(cat /tmp/agentic-worker-pool01-01.pid)
rm /tmp/agentic-worker-pool01-01.pid
```

### 6. Debug: Inspect Smoke Results

```bash
# View machine-readable results
cat config/runtime/smoke-test-results.json | jq '.'

# View which steps failed
cat config/runtime/smoke-test-results.json | jq '.failed[]'

# View step-level details
cat config/runtime/smoke-test-results.json | jq '.steps[] | select(.status == "failed")'
```

### 7. Debug: Inspect Step Logs

```bash
# Each step writes a log
cat /tmp/smoke-step-proxy.log
cat /tmp/smoke-step-spine.log
cat /tmp/smoke-step-worker1.log
```

### 8. Generate: Progress Report

```bash
./scripts/agentic/generate_progress_report.sh
cat docs/agentic/PROGRESS_REPORT.md
```

### 9. Launch: Full Orchestrator (after smoke passes)

```bash
# Only if smoke verdict is "pass"
python3 tools/agentic_cli.py run
```

### 10. Promote: Cold-Path Learning (without full run)

```bash
python3 tools/agentic_cli.py promote
```

### 11. Runtime Status

```bash
python3 tools/agentic_cli.py status
python3 tools/agentic_cli.py config
```

### 12. CI Check

```bash
bash scripts/ci.sh
```

---

## Troubleshooting Guide

### Symptom: `verify_proxy.sh` fails with connection refused

```
Cause:  fcc-server or node proxy not running on expected port.
Check:  curl http://localhost:8080/health
        curl http://localhost:8085/health
Fix:    Restart the proxy service. If using fcc-server:
        ./cloudcli/cloudcli workspace proxy restart
```

### Symptom: `start_task_spine.sh` fails with "No PRD found"

```
Cause:  PRD file missing or path misconfigured.
Check:  ls .taskmaster/docs/prd_agentic_codebase_optimization.md
        ls docs/agentic/PRD_V2_EXECUTION_READY.md
Fix:    Ensure at least one PRD file exists. Copy PRD from docs/agentic/ if needed.
```

### Symptom: `verify_worker_runtime.sh` reports 0 running workers

```
Cause:  OpenCode not installed or swarm not configured.
Check:  ~/.opencode/bin/opencode --version
        cat .opencode/ownership-map.json
Fix:    Install OpenCode: follow https://github.com/anthropics/opencode
        Configure swarm: update .opencode/ownership-map.json
```

### Symptom: `run_learning_loop_test.sh` fails — no learnings promoted

```
Cause:  Knowledge cache is empty or promotion path broken.
Check:  cat .opencode/knowledge_cache.json | jq '.learnings | length'
        cat docs/agentic/registry/knowledge.jsonl | wc -l
Fix:    Run the orchestrator first to populate the knowledge cache:
        python3 tools/agentic_cli.py run
        Then retry the learning loop test.
```

### Symptom: `stop_agentic_services.sh` reports orphaned PID files

```
Cause:  Worker processes crashed without cleaning up PID files.
Check:  cat /tmp/agentic-worker-*.pid
        ps aux | grep opencode
Fix:    Run with --force to kill any remaining processes:
        ./scripts/agentic/stop_agentic_services.sh --force
```

### Symptom: Registry JSONL files appear corrupted

```
Cause:  Partial write from a crash mid-append.
Check:  tail -1 docs/agentic/registry/knowledge.jsonl | jq '.'
Fix:    Remove the last (incomplete) line. Registries are append-only JSONL
        so the last complete line should be the last valid entry.
```

### Symptom: `generate_progress_report.sh` shows all UNKNOWN

```
Cause:  No smoke test results file or environment facts available.
Check:  ls config/runtime/smoke-test-results.json
        ls docs/agentic/audit/environment-facts.json
Fix:    Run the smoke workflow first:
        ./scripts/agentic/run_smoke_workflow.sh
```

### Symptom: Promoted learnings duplicate on every run

```
Cause:  `promoted_learning_ids.json` was lost or corrupted.
Fix:    Run compaction to clean duplicates from JSONL registries.
        The system will re-promote on next run (idempotent but creates duplicates).
        Restore from backup or accept duplicates and compact afterwards.
```

---

## Log and Evidence Locations

```
All paths relative to /home/ubuntu/

Runtime logs:
  /tmp/smoke-step-*.log                  Per-step smoke test output
  /tmp/agentic-worker-*.pid              Worker PID files (one per worker)

Structured evidence:
  config/runtime/smoke-test-results.json Machine-readable smoke results
  docs/agentic/audit/environment-facts.json  Live environment discovery
  docs/agentic/audit/BASELINE_AUDIT.md       Manual audit report
  docs/agentic/PROGRESS_REPORT.md            Generated progress report

Registries (append-only):
  docs/agentic/registry/knowledge.jsonl  Cold learning records
  docs/agentic/registry/agents.jsonl     Cold agent definitions
  docs/agentic/registry/chain.jsonl      Promotion chain history
  docs/agentic/registry/progress.json    Progress summary

Task state:
  .taskmaster/tasks/tasks.json           Task definitions and status
  .taskmaster/tasks/progress_ledger.json Continuous progress log
  .taskmaster/tasks/spawn_chain_registry.json  Worker spawn lineage
  .taskmaster/promoted_learning_ids.json Duplicate prevention

Agent specs:
  .claude/agents/*.md                    Durable agent definitions

Python app logs:
  stdout/stderr from: python3 tools/agentic_cli.py run
```

---

## How to Add a New Worker Role

### Step 1: Define the role

Choose a unique role key (e.g., `security-auditor`) and define:
- **Pool assignment:** which pool group it belongs to
- **Owned paths:** which files/directories it is allowed to modify
- **Forbidden paths:** which files/directories it must never touch
- **Task types:** what kinds of subtasks it handles

### Step 2: Update the ownership map

Edit `.opencode/ownership-map.json` and add a new entry:

```json
{
  "role": "security-auditor",
  "pool_id": "pool-01",
  "count": 5,
  "owned_paths": ["tools/security/", "config/security/"],
  "forbidden_paths": [".taskmaster/", ".claude/", "docs/agentic/registry/"]
}
```

### Step 3: Update the PRD

Add the new role to the PRD's worker pool section in `docs/agentic/PRD_V2_EXECUTION_READY.md`.

### Step 4: Update the worker initialization

In `services/opencode_swarm_service.py`, add the new role to the `_initialize_worker_pool()` method:

```python
WorkerRole(
    role_key="security-auditor",
    pool_id="pool-01",
    count=5,
    owned_paths=["tools/security/", "config/security/"],
    forbidden_paths=[".taskmaster/", ".claude/"],
)
```

### Step 5: Add a verification step (optional)

Add a verification function to `verify_worker_runtime.sh` that checks the new role's output quality.

### Step 6: Update the smoke workflow (optional)

If the role is critical, add it as a new step in `run_smoke_workflow.sh`:

```bash
STEPS+=("security|cricital|Verify security auditor|$SCRIPT_DIR/verify_worker_runtime.sh --role security-auditor")
```

---

## How to Promote a Learning to a Durable Agent

### Overview

The learning-to-agent promotion pathway is a two-stage process:
1. **Hot path:** The knowledge cache records an anomaly or pattern (lives in memory)
2. **Cold path:** Validated learnings are promoted into durable agent specs on disk

### Manual Promotion (Operator-Triggered)

```bash
# 1. View current learnings in the hot cache
python3 -c "
from tools.knowledge_cache import default_knowledge_cache
for l in default_knowledge_cache.learnings:
    print(f'{l.learning_id}: {l.summary[:80]}')
"

# 2. Run the promotion command
python3 tools/agentic_cli.py promote

# 3. Verify the new agent spec was written
ls -la .claude/agents/
cat .claude/agents/specialist-*.md
```

### What Happens During Promotion

1. Knowledge records in the hot cache are validated against the quality threshold
2. Records that pass are written to `docs/agentic/registry/knowledge.jsonl`
3. An agent spec is generated and written to `.claude/agents/` as a markdown file
4. The promotion is recorded in `docs/agentic/registry/agents.jsonl` and `chain.jsonl`
5. The learning ID is recorded in `.taskmaster/promoted_learning_ids.json` to prevent duplicate promotion

### Automatic Promotion (During Orchestrator Run)

```bash
python3 tools/agentic_cli.py run
# Promotion happens automatically at Phase 5 (Learning & Recovery Fabric)
```

### Deduplication After Promotion

If duplicates accumulate (e.g., after `promoted_learning_ids.json` is lost), run compaction:

```bash
# Dedup knowledge.jsonl: keep last entry per learning_id
# Dedup agents.jsonl: keep last entry per category
# Dedup chain.jsonl: keep last entry per source_learning_id
```

### Verification

```bash
# Check what was promoted
ls .claude/agents/

# Check promotion records
cat docs/agentic/registry/agents.jsonl | jq '.'
cat docs/agentic/registry/chain.jsonl | jq '.'

# Count promoted learnings
cat .taskmaster/promoted_learning_ids.json | jq 'length'
```

---

## Recovery Procedures

### If registries become corrupted

```bash
# Each registry is append-only JSONL. Remove the last line if partially written.
tail -1 docs/agentic/registry/knowledge.jsonl | jq '.'  # check validity
# If invalid: truncate to last valid line
```

### If promoted_learning_ids.json is lost

```bash
# Re-run promotion — will re-promote all hot-cache learnings
# (acceptable but creates duplicates; compact afterwards)
python3 tools/agentic_cli.py promote
```

### If orchestrator crashes mid-wave

```bash
# State preserved in tasks.json and progress_ledger.json
# Re-run is idempotent for completed steps
python3 tools/agentic_cli.py run
```

### If proxy fails

```bash
# Fabric falls back to offline simulation automatically
# Check proxy health:
curl http://localhost:8085/health
curl http://localhost:8080/health
# Restart if needed
```

### If worker pool stalls

```bash
# Stop all workers
./scripts/agentic/stop_agentic_services.sh

# Check for orphaned processes
ps aux | grep opencode

# Clean PID files
rm -f /tmp/agentic-worker-*.pid

# Restart
./scripts/agentic/run_smoke_workflow.sh --only spine,worker1
```

---

## Smoke Test Step Reference

| Step # | Key | Critical | Description | Sub-script |
|--------|-----|----------|-------------|------------|
| 1 | discover | YES | Environment discovery | `discover_environment.sh` |
| 2 | proxy | YES | Proxy health (all tiers) | `verify_proxy.sh --tier all` |
| 3 | spine | YES | Task spine bootstrap | `start_task_spine.sh` + `verify_task_spine.sh` |
| 4 | worker1 | YES | Single worker verification | `start_worker_runtime.sh --workers 1` + `verify_worker_runtime.sh --workers 1` |
| 5 | worker2 | NO | Concurrent worker verification | `verify_worker_runtime.sh --workers 2` |
| 6 | learning | NO | Learning loop test | `run_learning_loop_test.sh` |
| 7 | durable | NO | Durable agent load | `load_durable_agents.sh` |
| 8 | report | NO | Progress report generation | `generate_progress_report.sh` |

**Critical steps** (exit code 1 on failure): discover, proxy, spine, worker1
**Non-critical steps** (advisory failure only): worker2, learning, durable, report

---

## Smoke Test Results Schema

```json
{
  "workflow": "smoke-test",
  "version": "1.0.0",
  "started_at": "2026-07-31T...",
  "completed_at": "2026-07-31T...",
  "verdict": "pass|fail",
  "counts": {
    "total": 8,
    "passed": 7,
    "failed": 1,
    "skipped": 0,
    "critical_failed": 0
  },
  "passed": ["discover", "proxy", ...],
  "failed": ["worker2"],
  "skipped": [],
  "steps": [
    {"step": "discover", "status": "passed", "critical": true, "duration_sec": 2},
    {"step": "worker2", "status": "failed", "critical": false, "duration_sec": 5, "exit_code": 1}
  ]
}
```

---

## Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `OPENCODE_API_KEY` | OpenCode provider API key | (required for live testing) |
| `ANTHROPIC_API_KEY` | Anthropic provider API key | (required for Claude API) |
| `OPENROUTER_API_KEY` | OpenRouter provider API key | (optional fallback) |
| `GEMINI_API_KEY` | Gemini provider API key | (optional fallback) |
| `MISTRAL_API_KEY` | Mistral provider API key | (optional fallback) |
| `FCC_SERVER_URL` | fcc-server endpoint | `http://localhost:8080` |
| `FCC_SERVER_TOKEN` | fcc-server bearer token | `freecc` |

---

## CI Integration

The smoke workflow can be integrated into CI:

```bash
# In CI pipeline:
./scripts/agentic/run_smoke_workflow.sh --summary-only

# Parse results:
jq '.verdict' config/runtime/smoke-test-results.json

# Block on critical failures:
if [[ $(jq -r '.counts.critical_failed' config/runtime/smoke-test-results.json) -ne 0 ]]; then
    echo "Critical smoke test failures — aborting deploy"
    exit 1
fi
```
