# Baseline Audit — Agentic Orchestration System

**Generated**: 2026-07-31  
**Auditor**: Production Integration Engineer  
**Method**: Live discovery — every claim verified against the running environment

---

## Summary Verdict

| Subsystem | Status | Evidence |
|:----------|:-------|:---------|
| FCC Proxy (fcc-server) | ✅ **VERIFIED USED** — port 8080, auth `freecc`, serves 200+ models | `curl -s localhost:8080/v1/models` returns valid JSON |
| OpenCode binary | ✅ **INSTALLED** v1.18.10 at `.opencode/bin/opencode` | `opencode --version` = 1.18.10 |
| OpenCode swarm | ❌ **NOT USED** — 0 workers launched, empty `opencode-swarm.json` | `{"agents": {}}` |
| Task Master | ⚠️ **CONFIGURED ONLY** — `.taskmaster/` exists, config references `anthropic` provider, never invoked | No TM process, no TM-linked task execution |
| LiteLLM (port 4000) | ❌ **NOT RUNNING** — port 4000 returns HTTP 000 | `curl localhost:4000/v1/models` = connection refused |
| Port 8085 proxy | ✅ **RUNNING** — node process on 8085 | `ss -tlnp` shows node:354200 on :8085 |
| Registries | ⚠️ **STALE** — 39 KB, 8 agents, 6 chain entries, never exercise-tested | Files exist but no restart-reuse proof |
| Circuit breaker | ✅ **IMPLEMENTED** in `multi_provider_fabric.py` | Code verified |
| Claude Code subagents | ✅ **VERIFIED USED** — 12 native subagents delivered Spotify work | SESSIONS_REPORT.md |
| MCP sub-agent-mcp | ✅ **RUNNING** on port 8000 | `ss -tlnp` shows `sub-agent-mcp` on :8000 |

---

## Environment Discovery

### System
- **OS**: Ubuntu 24.04.4 LTS (Noble Numbat), kernel 6.17.0-1019-oracle
- **Arch**: aarch64 (ARM64)
- **User**: ubuntu, home `/home/ubuntu`
- **Shell**: /bin/bash
- **Disk**: 145G total, 59G used (41%)

### Runtimes
| Tool | Version | Path |
|:-----|:--------|:-----|
| Python | 3.12.3 | `/usr/bin/python3` |
| uv | 0.12.0 | managed |
| Node | 22.23.1 | managed |
| npm | 10.9.8 | managed |
| Git | 2.43.0 | `/usr/bin/git` |
| Docker | 29.6.2 | `/usr/bin/docker` |
| systemd | 255 | systemctl available |
| pm2 | NOT FOUND | — |

### Listening Ports
| Port | Process | Notes |
|:-----|:--------|:------|
| 8080 | `fcc-server` (PID 342617) | Main FCC proxy — Anthropic/OpenAI compatible |
| 8085 | `node` (PID 354200) | Separate node proxy |
| 8000 | `sub-agent-mcp` (PID 1482) | Claude Code MCP sub-agent runtime |
| 3000 | Docker proxy → container | Likely web UI |
| 22 | sshd | SSH access |
| 80, 443 | system | HTTP/S |
| 9000 | system | Unknown service |
| 11451, 51121, 54545, 1455 | Docker proxies | Container services |
| 8317 | Docker proxy (127.0.0.1) | Internal container comm |

### Port 4000 (LiteLLM) — CONFIRMED DEAD
```bash
curl -s -o /dev/null -w "HTTP %{http_code}" http://localhost:4000/v1/models
# HTTP 000 — connection refused
```
**LiteLLM is not running.** The `OPENAI_BASE_URL=http://localhost:4000/v1` environment variable points to nothing live.
The `progress.json` claim of "litellm-proxy (localhost:4000)" being CONFIRMED WORKING is **stale** — it was verified on 2026-07-30T13:45Z but the service has since stopped or was never persistent.

### Proxy (Port 8080) — VERIFIED WORKING
```bash
curl -s http://localhost:8080/v1/models -H "Authorization: Bearer freecc"
# Returns: {"object":"list","data":[...200+ models...]}
```
The FCC proxy serves models including:
- `anthropic/opencode_go/deepseek-v4-flash`
- `anthropic/opencode_go/deepseek-v4-pro`
- `anthropic/opencode/deepseek-v4-flash`
- `anthropic/nvidia_nim/*`
- `anthropic/groq/*`
- And 200+ more provider/model combinations

**Auth**: Bearer token `freecc` (configured via `ANTHROPIC_AUTH_TOKEN`)

### Proxy (Port 8085) — RUNNING
Node process on port 8085. Not tested for API compatibility.

---

## OpenCode Status

### Binary
- **Path**: `/home/ubuntu/.opencode/bin/opencode`
- **Version**: 1.18.10
- **Type**: ELF 64-bit ARM aarch64 executable (178MB, not stripped)
- **Help**: Working — `opencode --help` shows full command list including `run`, `serve`, `acp`, `agent`, `providers`

### Swarm Configuration
- **`opencode.json`**: `{"$schema": "https://opencode.ai/config.json", "plugin": []}` — minimal, no plugins
- **`opencode-swarm.json`**: `{"agents": {}}` — **EMPTY**. No agents configured.
- **`.opencode/bin/`**: Contains only the `opencode` binary — no worker scripts, no runtime configs

### OpenCode Worker Status
- **Running processes**: 0 OpenCode worker processes detected
- **Swarm agents**: 0 configured, 0 launched, 0 completed
- **Verdict**: OpenCode binary is installed but **never used as a worker runtime**

---

## Task Master Status

### Installation
- **Config**: `/home/ubuntu/.taskmaster/config.json` — exists, well-formed JSON
- **State**: `/home/ubuntu/.taskmaster/tasks/` — contains `tasks.json`, `progress_ledger.json`, `spawn_chain_registry.json`
- **Reports**: `/home/ubuntu/.taskmaster/reports/` — directory exists

### Configuration Analysis
```json
{
  "models": {
    "main": {"provider": "anthropic", "modelId": "claude-sonnet-4-20250514"},
    "research": {"provider": "perplexity", "modelId": "sonar"},
    "fallback": {"provider": "anthropic", "modelId": "claude-3-7-sonnet-20250219"}
  }
}
```
- **Provider**: `anthropic` — requires a valid Anthropic API key
- **API key status**: `ANTHROPIC_API_KEY=freecc` — this is the FCC proxy auth token, NOT a real Anthropic API key
- **Perplexity**: `research` tier uses `perplexity` provider — no Perplexity API key found in environment

### Task Master Invocation Status
- **CLI commands**: 0 Task Master commands issued
- **MCP tools**: 0 Task Master MCP tools invoked
- **Task execution**: 0 tasks created/claimed/completed through Task Master
- **Verdict**: **CONFIGURED ONLY** — config files exist but Task Master was never invoked with real credentials

---

## Registry Status

### knowledge.jsonl
- **Entries**: 39 lines
- **Status**: Stale — last promotion timestamp 1785423023 (2026-07-29)
- **Content**: Mostly duplicate `swarm_concurrency` entries (LEARN-0001 through LEARN-0006 same title)
- **Issue**: No TTL, no pruning, append-only growth

### agents.jsonl
- **Entries**: 8 lines
- **Status**: Stale
- **Content**: 3 agent definitions from cold-path promotion, all `swarm_concurrency` category
- **Issue**: Agents reference system prompts but no actual `.claude/agents/*.md` files written

### chain.jsonl
- **Entries**: 6 lines
- **Status**: Stale
- **Content**: Cold-path promotion lineage records
- **Issue**: Forward-only — spawn chains not cross-referenced back

### progress.json
- **Claims**: 100% completion, all phases GREEN
- **Reality**: `pool_status` shows 0/0/0/0 across all pools — zero actual work
- **Blockers documented**: 7 blockers, including opencode 403, gemini timeout, groq 403, etc.
- **Critical gap noted**: "Worker output never applied to codebase" (CG-01) — acknowledged but not fixed

---

## Provider & API Key Status

### Keys with values (from env.txt)
| Provider | Key Present | Tested Live | Result |
|:---------|:-----------|:------------|:-------|
| opencode | ✅ `sk-ziIQQ...` | ✅ | Working via FCC proxy port 8080 |
| openrouter | ✅ `sk-or-v1-...` | ❌ | Not tested |
| mistral | ✅ `qLWSa1...` | ❌ | Not tested |
| nvidia_nim | ✅ `nvapi-o9...` | ❌ | Not tested |
| gemini | ⚠️ 42 keys loaded | ❌ | Direct API times out |
| groq | ❌ Empty | ❌ | 403 — account/api key issue |
| deepseek | ❌ Empty | — | No key |

### Key Pool
- **46 keys** loaded across 5 providers (gemini: 42, mistral: 1, nvidia_nim: 1, opencode: 1, openrouter: 1)
- **Circuit breakers**: Clean (0 tripped)
- **Permanently dead**: 0 providers

---

## Git Status
- **Branch**: main
- **Remote**: None configured — local commits only
- **Pending changes**: 26 modified files, 13 untracked directories/files
- **Last commits**: Documentation, prompt variants, test suite (224 tests)

---

## Critical Port Mismatch

| Source | Claims Proxy Port | Actual Proxy Port | Match? |
|:-------|:-----------------|:------------------|:-------|
| `.env` MODEL_TIER_MAIN | routes via fabric (port 4000 litellm) | 8080 (fcc-server) | ❌ |
| `progress.json` live_ai_verification | "litellm-proxy (localhost:4000)" | 8080 | ❌ |
| `opencode_swarm_service.py` fabric routes | localhost:4000 first | 8080 | ❌ |
| `providers/multi_provider_fabric.py` | localhost:4000 (litellm) | 8080 | ❌ |
| Actual running proxy | — | 8080 | ✅ |

**The fabric routing table targets port 4000 (litellm) first, which is dead. It then falls through opencode → gemini → groq → alibabacloud → digitalocean before hitting simulation fallback.**

---

## Live Fire Test Results (2026-07-31)

A live integration test was run against the actual environment:

1. **Single subtask**: ✅ Completed in 0.85s via opencode provider (`api.opencode.ai`)
2. **Batch parallel (3 tasks)**: ✅ All 3 completed in 2.05s via ThreadPoolExecutor
3. **Multi-role dispatch**: ✅ All 3 roles completed successfully

**Conclusion**: The FCC proxy (port 8080) + opencode provider works. The swarm manager code is functional. What's missing is:
- No workers persist across sessions
- No task state is durable
- No learning loop is exercised
- No OpenCode swarm process is launched
- The first-hop route (litellm:4000) is dead weight

---

## Remediation Plan

1. **Fix fabric routing**: Add FCC proxy (port 8080) as first route, remove dead litellm route
2. **Launch OpenCode workers**: Use `opencode serve` or `opencode run` with actual task payloads
3. **Wire Task Master**: Either configure real Anthropic API key OR implement local task-spine fallback
4. **Exercise learning loop**: Promote → write agent file → restart → load → route → verify
5. **Ramp concurrency**: 1 → 2 → 4 workers with gate checks at each level
6. **Generate evidence**: Every claim backed by command output, exit code, and timestamp

---

## Blockers

1. **No git remote** — commits cannot be pushed, no off-machine backup
2. **Task Master API keys** — `anthropic` provider requires real API key, not `freecc` proxy token
3. **No process supervisor** — pm2 not installed, systemd user unit path unclear
4. **Port 4000 permanently dead** — litellm not installed/configured to run as service
