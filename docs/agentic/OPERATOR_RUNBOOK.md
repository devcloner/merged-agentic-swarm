# Operator Runbook — Merged Agentic Swarm

Concise operator guide for the autonomous development runtime.

---

## Quick Start

```bash
cd /home/ubuntu/merged-agentic-swarm

# Full smoke test across all subsystems (exit 0 = all critical steps passed)
./scripts/agentic/run_smoke_workflow.sh

# Focused health checks
./scripts/agentic/verify_proxy.sh        # proxy health + all 3 model tiers
uv run python scripts/agentic/verify_learning_loop.py   # learning loop E2E

# Start the proxy (port 8089)
uv run python -m merged_agentic_swarm.proxy.claude_proxy_server

# Run the test suite (246 tests)
uv run pytest -v

# Full CI gate (lint + format + tests)
./scripts/ci.sh
```

---

## Service Map

| Service | Purpose | How to Start / Restart |
|---|---|---|
| Claude Proxy | LLM gateway for agents; routes model tiers | `uv run python -m merged_agentic_swarm.proxy.claude_proxy_server` (port **8089**) |
| CloudCLI | Claude Code / agent transport | `systemctl --user restart cloudcli.service` (port **8085**) |
| Task Spine | Task lifecycle (create/claim/update) | `uv run python scripts/agentic/task_spine_cli.py <cmd> ...` |
| Learning Loop | Durable knowledge cache + registry | `uv run python scripts/agentic/verify_learning_loop.py` (E2E) |

---

## Common Commands

```bash
# Verify proxy health and all 3 model tiers
./scripts/agentic/verify_proxy.sh

# Learning loop end-to-end test
uv run python scripts/agentic/verify_learning_loop.py

# Task management
uv run python scripts/agentic/task_spine_cli.py create "Task title" "Description"
uv run python scripts/agentic/task_spine_cli.py list
uv run python scripts/agentic/task_spine_cli.py claim <task-id> <worker-id>
uv run python scripts/agentic/task_spine_cli.py update <task-id> <status>
uv run python scripts/agentic/task_spine_cli.py inspect <task-id>

# Full smoke test (create or update workflow)
./scripts/agentic/run_smoke_workflow.sh

# Tests and CI
uv run pytest -v                    # 246 tests
./scripts/ci.sh                     # lint + format + test gate
```

---

## Troubleshooting

| Symptom | Cause / Fix |
|---|---|
| Port 8085 already in use | CloudCLI owns 8085. Use the proxy on **8089** instead (`uv run python -m merged_agentic_swarm.proxy.claude_proxy_server`). |
| OpenCode / agent auth failures | Fall back to **Mistral** as the backend provider for that tier. |
| 401 / auth rejected by proxy | Bad token. Check `ANTHROPIC_AUTH_TOKEN=freecc` is set in the environment and `~/env.txt` (key pools). |
| Proxy not answering health checks | Confirm it is up on 8089, then rerun `./scripts/agentic/verify_proxy.sh`. |
| Smoke test step fails | Rerun `./scripts/agentic/run_smoke_workflow.sh`; inspect `.opencode/proxy.log` and registry state. |

---

## File Locations

| What | Path |
|---|---|
| Proxy logs | `.opencode/proxy.log` |
| Task state | `.taskmaster/tasks/tasks.json` |
| Registries | `docs/agentic/registry/*.jsonl` (agents / chain / knowledge) |
| Key pools / secrets | `~/env.txt` |
| Smoke workflow | `scripts/agentic/run_smoke_workflow.sh` |
| Proxy health + tiers | `scripts/agentic/verify_proxy.sh` |
| Learning loop E2E | `scripts/agentic/verify_learning_loop.py` |
| Task CLI | `scripts/agentic/task_spine_cli.py` |
| CI gate | `scripts/ci.sh` |
