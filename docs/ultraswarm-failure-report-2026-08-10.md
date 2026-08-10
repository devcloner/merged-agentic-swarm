# Ultraswarm Run Failure Report — 2026-08-10

**Run ID**: `e89ab5b1-774f-4642-9ded-11118fa5d6b8`  
**Plan**: `.ultraswarm-plan.json`  
**Date**: 2026-08-10 20:56–21:26 UTC  
**Repo**: `devcloner/merged-agentic-swarm` @ commit `446e11e`

---

## Summary

3 tasks planned, **0 integrated**, 1 failed (exhausted), 2 blocked. Wall clock: 30m 5s.

## Preflight State

```
WORKER    INSTALLED  FUNCTIONAL  DETAIL
codex     ✓          ✓           verified · backend, logic, debugging, architecture
agy       ✓          ✗           UNUSABLE — error
opencode  ✓          ✗           UNUSABLE — error
pi        ✓          ✓           verified · general, full-stack, refactors
claude    ✓          ✓           verified · full-stack, refactors, architecture

3/5 workers usable. GATES: test. POLICY: maxParallelWorkers=16.
```

**Note**: `agy` and `opencode` are UNUSABLE (preflight smoke test failed). Only 3 workers available, severely limiting parallelism.

---

## Task Results

| Task | Worker | Status | Attempts | Duration | Model Used |
|------|--------|--------|----------|----------|------------|
| `chat-backend` | claude | **FAILED** | 3 exhausted | ~30m total | `claude-haiku-4-5` |
| `chatbox-ui` | pi | **BLOCKED** | 0 | — | `gemini-2.5-flash` (est.) |
| `expose-and-test` | codex | **BLOCKED** | 0 | — | `gpt-5.6-sol` (est.) |

---

## Root Cause Analysis

### 1. `chat-backend` — 3× timeout (exit code 143 = SIGTERM)

**Log entries** (from `~/.ultraswarm/logs/`):

```
170 → attempt.started  chat-backend {number:1, worker:"claude", model:"claude-haiku-4-5", pid:3059502, effort:"low"}
171 → attempt.finished chat-backend {attemptId:77, status:"failed", exitCode:143, durationMs:600782, errorKind:"timeout"}

172 → attempt.started  chat-backend {number:2, worker:"claude", model:"claude-haiku-4-5", pid:3091388, effort:"medium"}
173 → attempt.finished chat-backend {attemptId:78, status:"failed", exitCode:143, durationMs:600559, errorKind:"timeout"}

174 → attempt.started  chat-backend {number:3, worker:"claude", model:"claude-haiku-4-5", pid:3119285, effort:"high"}
175 → attempt.finished chat-backend {attemptId:79, status:"failed", exitCode:143, durationMs:600571, errorKind:"timeout"}
```

**Root cause**: The claude worker resolved to **claude-haiku-4-5** for ALL attempts, even at medium/high effort. Haiku 4.5 is a fast/light model — insufficient for a complexity-8 task requiring:

- Reading + understanding a ~900-line `webapp.py` file
- Adding SSE streaming chat endpoint (`/api/chat`)
- Adding 4 session management endpoints
- Wiring through multi-provider fabric
- Adding imports, handlers, routes
- Running ruff lint + format
- Verifying imports

The model spent all 10 minutes per attempt reading the file and building context, never reaching the write/verify phase.

**Why Haiku and not Opus/Sonnet?** The claude worker in ultraswarm is FCC's Claude Code CLI pointed at `ANTHROPIC_BASE_URL=http://127.0.0.1:8080` (fcc-server). The FCC model routing maps `claude` family models to `opencode_go/deepseek-v4-flash` — see GitLab issue #12. Opus/Fable are silently downgraded. So Haiku (the cheapest model) was used for all 3 tiers.

### 2. `chatbox-ui` + `expose-and-test` — BLOCKED

These had correct dependencies on `chat-backend`. Since it never merged, they never started. This is expected behavior.

---

## Secondary Issues

### Worker Pool Degradation
- `agy` (agy 1.1.11): UNUSABLE — preflight smoke test error. Last known good: unknown.
- `opencode` (opencode 1.18.15): UNUSABLE — preflight smoke test error. Likely related to opencode.json provider misconfiguration.

### Model Tier Misrouting
- FCC's `model_routing.py` maps all Claude models → `deepseek-v4-flash` via opencode_go provider (GitLab issue #12)
- The ultraswarm claude worker inherits this misrouting
- Result: complexity-8 task gets cheapest model regardless of tier escalation

### Worktree Cleanup
- Path: `/home/ubuntu/merged-agentic-swarm/.ultraswarm/worktrees/` — **empty** after run
- Worktrees auto-cleaned because no changes landed (all attempts timed out before writing)
- No partial output to recover

---

## Log Paths

| Resource | Path |
|----------|------|
| Run logs (JSON events) | `~/.ultraswarm/logs/` (query via `ultraswarm logs e89ab5b1`) |
| Plan file | `/home/ubuntu/merged-agentic-swarm/.ultraswarm-plan.json` |
| Worktree root | `/home/ubuntu/merged-agentic-swarm/.ultraswarm/worktrees/` (empty) |
| Worker stdout/stderr | Per-attempt, captured by ultraswarm runner (ephemeral) |
| FCC model routing | `/home/ubuntu/fcc-fork/src/free_claude_code/model_routing.py` |
| FCC logs | `/home/ubuntu/.fcc/logs/server.log` |
| Claude Code worker logs | `~/.claude/projects/-home-ubuntu/` (session transcripts) |
| GitLab issue #12 | `devcloner/merged-agentic-swarm` — "fcc-server: all claude families routed to deepseek-v4-flash" |

---

## Recommended Fixes

### Immediate (this session)
1. **Implement chatbox inline** — bypass ultraswarm for the chat-backend task. Use this Claude session (Opus 5) directly for the complex implementation.
2. **Split into smaller chunks** — `/api/chat` endpoint first, then session management, then UI, then tests.
3. **Fix opencode/agy preflight** — investigate why they fail smoke test so the full 5-worker pool is available.

### Medium-term
4. **Fix FCC model routing** (GitLab issue #12) — so ultraswarm claude worker can use Sonnet/Opus for complex tasks.
5. **Reduce claude worker timeout** — 10 minutes is too short for a complexity-8 task on Haiku. Either increase timeout or split tasks smaller.

### Long-term
6. **Add model-tier awareness to ultraswarm policy** — complexity-7+ tasks should require a minimum model tier (not Haiku).
