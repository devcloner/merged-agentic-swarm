# Worker Runtime Verification Report

**Generated**: 2026-07-31  
**Verifier**: Production Integration Engineer  
**Method**: Live worker ramp at 1, 2, and 4 concurrency levels via `native_subagent` mode

---

## Summary

| Metric | Result |
|:-------|:-------|
| OpenCode binary | **INSTALLED** v1.18.10 at `~/.local/bin/opencode` |
| OpenCode service | **RUNNING** as web IDE on port 9200 |
| Runtime adapter | `worker_runtime_adapter.py` — 3 modes |
| Auto-detection | ✅ Correctly identifies `opencode` as available |
| Ramp execution mode | **native_subagent** (Mistral-backed fabric) |
| Model tier | `claude-3-7-sonnet` routed through Mistral |
| Concurrency ramp | 1 → 2 → 4, all levels PASS |
| Ownership collisions | 0 observed (task-isolated ramp) |

---

## Runtime Discovery

The `WorkerRuntimeAdapter` (`src/merged_agentic_swarm/services/worker_runtime_adapter.py`) is the unified
launcher for swarm workers. It supports three execution modes:

| Mode | Mechanism | Notes |
|:-----|:----------|:------|
| `opencode` | Spawns `opencode serve --port <N>` subprocesses, one per worker, dispatches via HTTP | Highest-fidelity worker isolation |
| `native_subagent` | Runs tasks inline through `MultiProviderFabric.dispatch_request()` in the same process | No per-task process overhead |
| `direct_fabric` | Bare fabric dispatch, no worker subprocess at all | Semantically identical to `native_subagent` |

Mode selection is by explicit argument or auto-detection. Priority order is
`opencode` > `native_subagent` > `direct_fabric`.

### Auto-detection fix

Detection was previously broken for two independent reasons, both now fixed:

1. **Binary path bug** — the default `OPENCODE_BIN` pointed at `~/.opencode/bin/opencode`, but the
   binary is actually installed (via npm) at `~/.local/bin/opencode`. `_resolve_opencode_bin()` now
   probes a candidate list that includes `~/.local/bin/opencode`, `/usr/local/bin/opencode`,
   `/usr/bin/opencode`, and `shutil.which("opencode")`, returning the first executable match.
2. **`--help` goes to stderr** — `_opencode_available()` only inspected `stdout`, so the
   version banner (emitted on stderr) never matched. It now checks `result.stdout + result.stderr`.

Verified live: `detect_mode()` returns `opencode`, resolved binary
`/home/ubuntu/.local/bin/opencode`.

---

## OpenCode Status

| Item | Value |
|:-----|:------|
| Binary path | `/home/ubuntu/.local/bin/opencode` (symlink → `../lib/node_modules/opencode-ai/bin/opencode.exe`) |
| Version | **1.18.10** |
| Service | `opencode` listening on `127.0.0.1:9200` (web IDE) |
| Headless `serve` command | Present (`opencode serve --port <N>`) but **NOT used for execution** in this verification |

OpenCode is confirmed installed and running as the interactive web IDE. The `serve` command exists
and is wired into `_launch_via_opencode()`, but execution in this verification ran through the
`native_subagent` fallback path.

---

## Ramp Test Results

Controlled worker ramp executed in `native_subagent` mode against the Mistral-backed
multi-provider fabric. Each concurrency level was fully tested before advancing to the next
(1 → 2 → 4).

### Level 1: Single worker

| Field | Value |
|:------|:------|
| Workers | 1 |
| Status | **COMPLETED** |
| Time | 0.56s |
| Model tier | `claude-3-7-sonnet` → Mistral |

**Result**: ✅ PASS

### Level 2: Two workers

| Field | Value |
|:------|:------|
| Workers | 2 |
| Status | **BOTH COMPLETED** |
| Times | 0.46s – 0.65s |
| Collisions | 0 |
| Model tier | `claude-3-7-sonnet` → Mistral |

**Result**: ✅ PASS — no collisions, distinct workers

### Level 4: Four workers

| Field | Value |
|:------|:------|
| Workers | 4 |
| Status | **ALL 4 COMPLETED** |
| Times | 0.59s – 0.66s |
| Collisions | 0 |
| Model tier | `claude-3-7-sonnet` → Mistral |

**Result**: ✅ PASS — full ramp, no failures, no collisions

### Ramp summary

| Level | Workers | Completed | Failed | Collisions | Time range | Result |
|:------|:--------|:----------|:-------|:-----------|:-----------|:-------|
| 1 | 1 | 1 | 0 | 0 | 0.56s | ✅ PASS |
| 2 | 2 | 2 | 0 | 0 | 0.46–0.65s | ✅ PASS |
| 4 | 4 | 4 | 0 | 0 | 0.59–0.66s | ✅ PASS |

---

## Worker Output Format

Every worker returns a uniform result dict, verified against the actual adapter output:

| Key | Type | Description |
|:----|:-----|:------------|
| `run_id` | str | Unique UUID per worker invocation |
| `task_id` | str | Task identifier the worker executed |
| `worker_id` | str | Worker identifier (role-scoped in batch mode) |
| `role` | str | `WorkerRole.value` (e.g. `core_engineer`) |
| `model_tier` | str | Model alias, `claude-3-7-sonnet` |
| `start_time` | float | Epoch seconds at launch |
| `end_time` | float | Epoch seconds at completion |
| `status` | str | `completed` / `failed` / `partial (simulated)` |
| `evidence` | str | Fabric response text (truncated to 2000 chars) |

All workers in this ramp reported `model_tier=claude-3-7-sonnet`, routed through Mistral,
with `status=completed` and no `simulation_fallback`.

---

## Collision Detection

- **No edit collisions were observed** across any ramp level (0 at 2 workers, 0 at 4 workers).
- **Caveat**: the ramp was **task-isolated** — each worker owned a distinct task with no
  shared file targets. This verifies concurrent dispatch correctness (no cross-talk, distinct
  worker IDs, distinct runs) but does **not** exercise file-level ownership enforcement.
- **Ownership enforcement is NOT yet verified** for the concurrent-write-to-same-file case.
  File-level conflict resolution remains unverified and is flagged as a residual gap below.

---

## Fallback Decision

| Path | Status | Reason |
|:-----|:-------|:-------|
| `opencode serve` execution | NOT USED | `serve` exists and is wired in, but headless dispatch was not exercised this run |
| `native_subagent` | **USED** | Ramp executed through this mode (Mistral-backed fabric, same-process inline dispatch) |
| `direct_fabric` | AVAILABLE | Identical implementation to `native_subagent`; not separately exercised |

`WorkerRuntimeAdapter.detect_mode()` returns `opencode` (the binary is available and verified), but
the controlled ramp ran in `native_subagent` mode. This is the documented fallback path that
guarantees execution even when headless OpenCode dispatch is unavailable.

---

## Controlled Scaling Policy

1. **Stepwise ramp** — concurrency advances strictly 1 → 2 → 4; each level must pass fully
   before the next is attempted. No jumping directly to peak concurrency.
2. **Max concurrency guard** — `launch_batch()` caps at `min(max_concurrency, len(tasks))`,
   never exceeding the configured bound.
3. **No collision tolerance** — a level only advances if all workers complete with zero
   collisions. Any collision fails the level and blocks further scaling.
4. **Worker isolation** — tasks are dispatched to distinct worker IDs so runs are attributable
   per worker; verified at all three ramp levels.
5. **Gap to close before full-scale (40-worker) deployment** — verify file-level ownership
   enforcement under concurrent writes to shared files, and exercise `opencode serve`
   headless dispatch as the primary path.

---

## Verdict

**WORKER RUNTIME = VERIFIED at 1→2→4 ramp (native_subagent / Mistral-backed fabric)**

OpenCode v1.18.10 is installed and auto-detected correctly after the path/stderr fix; the
runtime adapter supports 3 modes; all ramp levels complete with zero collisions and a
consistent result schema. OpenCode `serve` was available but not used for execution — the
`native_subagent` fallback carried the ramp. File-level ownership enforcement under concurrent
writes remains the one unverified dimension.
