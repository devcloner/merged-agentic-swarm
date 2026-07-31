# Worker Runtime Verification Report

**Generated**: 2026-07-31  
**Verifier**: Production Integration Engineer  
**Method**: Live worker dispatch at 1, 2, and 4 concurrency levels

---

## Summary

| Metric | Result |
|:-------|:-------|
| OpenCode binary | **INSTALLED** v1.18.10 (NOT USED as swarm server) |
| Worker runtime mode | **DIRECT FABRIC DISPATCH** |
| Worker pool size | 40 workers across 7 roles |
| Live provider | ✅ gemini (via multi-provider fabric) |
| Concurrency ramp | 1→2→4 all pass |

---

## Architecture

The worker runtime dispatches tasks through the existing `OpenCodeSwarmManager` which routes through `MultiProviderFabric.dispatch_request()`. The fabric tries providers in order:

1. `fcc-proxy` (localhost:8080) — HTTP 404 (Anthropic format, not OpenAI)
2. `opencode` (api.opencode.ai) — JSON parse error
3. `gemini` (generativelanguage.googleapis.com) — **WORKING**
4. `groq` — 403
5. `alibabacloud` — timeout
6. `digitalocean` — 403
7. `simulation` — fallback

The **gemini** provider is the active live route. It processes ~1 request/sec with latencies of 1.5–3s.

---

## Concurrency Ramp Results

### Test 1: Single Worker
| Field | Value |
|:------|:------|
| Worker ID | `opencode-worker-10` |
| Role | `core_engineer` |
| Status | `completed` |
| Time | 3.96s |
| Live provider | ✅ Yes |
| Simulation fallback | ❌ No |

**Result**: ✅ PASS

### Test 2: Two Workers (Isolated Paths)
| Field | Value |
|:------|:------|
| Workers | `opencode-worker-10`, `opencode-worker-11` |
| Task A | `VFY-W2-A` — math_utils.py, 2.24s |
| Task B | `VFY-W2-B` — string_utils.py, 2.47s |
| Total time | 2.47s |
| Collisions | 0 |
| Both live | ✅ Yes |
| Status | Both `completed` |

**Result**: ✅ PASS — no ownership violations, distinct workers

### Test 3: Four Workers (Batch)
| Field | Value |
|:------|:------|
| Workers | `opencode-worker-10` through `13` |
| Wave gate | Level 1 (max 8 concurrent) |
| Completed | 4/4 |
| Failed | 0 |
| Total time | 2.87s |
| Live provider | ✅ All 4 live |
| Unique workers | 4 |

**Result**: ✅ PASS — all completed, all live, correct ramp

---

## OpenCode Binary Assessment

### Installed
- **Path**: `/home/ubuntu/.opencode/bin/opencode`
- **Version**: 1.18.10
- **Type**: ELF 64-bit ARM aarch64 (178MB)
- **Commands**: `run`, `serve`, `acp`, `agent`, `providers`, `mcp`, etc.

### Why Not Used as Swarm Server
- `opencode serve` would start an interactive TUI server — not suitable for headless worker dispatch
- `opencode run "message"` executes a single prompt — could work but adds process-launch overhead per task
- The existing `MultiProviderFabric.dispatch_request()` already provides multi-provider routing with fallback
- Direct fabric dispatch avoids the overhead of spawning an OpenCode subprocess per worker task

### Fallback Path
- **Claude Code native subagents**: Available via `sub-agent-mcp` on port 8000
- Can serve as a fallback if the fabric dispatch fails
- Not tested in this verification run (fabric dispatch was working)

---

## Acceptance Tests Summary

| Test | Workers | Completed | Failed | Live | Collisions | Result |
|:-----|:--------|:----------|:-------|:-----|:-----------|:-------|
| Single | 1 | 1 | 0 | ✅ | 0 | ✅ PASS |
| Isolated | 2 | 2 | 0 | ✅ | 0 | ✅ PASS |
| Batch-4 | 4 | 4 | 0 | ✅ | 0 | ✅ PASS |

---

## Feature Gaps

| Feature | Status | Notes |
|:--------|:-------|:------|
| OpenCode swarm server mode | NOT USED | Binary exists but not suitable for this dispatch pattern |
| 40-worker full pool | NOT TESTED | Only verified 1→2→4 ramp |
| Worker process persistence | NOT IMPLEMENTED | Workers exist only within ThreadPoolExecutor scope |
| PID file tracking | NOT TESTED | Scripts exist but not exercised in this run |
| Claude Code subagent fallback | AVAILABLE | Not exercised (fabric dispatch was working) |

---

## Verdict

**WORKER RUNTIME = VERIFIED USED (direct fabric dispatch mode)**

The swarm manager dispatches worker tasks through the multi-provider fabric with live provider routing. 1, 2, and 4 worker configurations all complete successfully with no collisions. The OpenCode binary is installed but not used as a swarm server — direct fabric dispatch is the working pattern.
