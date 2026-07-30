# Merged Agentic Swarm — Operator Runbook

**Version:** 1.0.0
**Date:** 2026-07-30

---

## Quick Start

```bash
cd /home/ubuntu

# 1. Check system status
python3 tools/agentic_cli.py status

# 2. Check configuration
python3 tools/agentic_cli.py config

# 3. Run full orchestrator
python3 tools/agentic_cli.py run

# 4. Force cold-path promotion (without full orchestrator run)
python3 tools/agentic_cli.py promote

# 5. Run CI checks
bash scripts/ci.sh
```

---

## System Architecture

| Component | Path | Purpose |
|---|---|---|
| Orchestrator CLI | `tools/agentic_cli.py` | Main entry point |
| Orchestrator engine | `tools/agentic_orchestrator.py` | Workflow execution |
| Multi-provider fabric | `providers/multi_provider_fabric.py` | AI model dispatch |
| Key pool | `providers/key_pool.py` | API key management |
| Task Master | `services/task_master_service.py` | PRD parsing, task state |
| Swarm manager | `services/opencode_swarm_service.py` | Worker pool execution |
| Agent factory | `services/agent_factory_service.py` | HOT/COLD agent spawning |
| Wave gates | `services/wave_gate_service.py` | Gated phase control |
| Progress ledger | `services/progress_ledger_service.py` | Continuous logging |
| Codebase mapper | `services/codebase_map_service.py` | AST scanning, spec gaps |
| Knowledge cache | `tools/knowledge_cache.py` | Hot-path learning |
| Proxy server | `proxy/claude_proxy_server.py` | API proxy (port 8085) |

---

## Key State Paths

| Purpose | Path |
|---|---|
| Task Master state | `.taskmaster/tasks/tasks.json` |
| Progress ledger | `.taskmaster/tasks/progress_ledger.json` |
| Spawn chain | `.taskmaster/tasks/spawn_chain_registry.json` |
| Promoted IDs | `.taskmaster/promoted_learning_ids.json` |
| Hot knowledge cache | `.opencode/knowledge_cache.json` |
| Ownership map | `.opencode/ownership-map.json` |
| Cold knowledge registry | `docs/agentic/registry/knowledge.jsonl` |
| Cold agent registry | `docs/agentic/registry/agents.jsonl` |
| Cold chain registry | `docs/agentic/registry/chain.jsonl` |
| Progress report | `docs/agentic/registry/progress.json` |
| Provider registry | `docs/agentic/providers/PROVIDER_REGISTRY.json` |
| Agent specs | `.claude/agents/*.md` |
| PRD | `.taskmaster/docs/prd_agentic_codebase_optimization.md` |
| PRD v2 | `docs/agentic/PRD_V2_EXECUTION_READY.md` |

---

## CLI Reference

```
Usage: python3 tools/agentic_cli.py <command>

Commands:
  run            Run full orchestrator workflow
  status         Show system status
  promote        Force cold-path promotion
  config         Show configuration state

Run Options:
  --prd PATH     Custom PRD path (default: .taskmaster/docs/...)
  --title TEXT   PRD title (default: "Merged Agentic Swarm OS")
  --verbose, -v  Print full result JSON
```

---

## Health Checks

```bash
# Proxy health
curl http://localhost:8085/health
curl http://localhost:8085/status

# LiteLLM proxy (if running)
curl http://localhost:4000/health

# Registry writability
echo '{"test": true}' >> docs/agentic/registry/knowledge.jsonl

# CI suite
bash scripts/ci.sh
```

---

## Recovery Procedures

### If registry becomes corrupted:
```bash
# Each registry is append-only JSONL — remove last line if partially written
# knowledge.jsonl, agents.jsonl, chain.jsonl
# Last complete line should be the last entry
```

### If promoted_learning_ids.json is lost:
```bash
# The run will re-promote all hot-cache learnings — acceptable but creates duplicates
# Run compaction afterwards to clean up
```

### If orchestrator crashes mid-wave:
```bash
# State is preserved in tasks.json and progress_ledger.json
# Simply re-run: python3 tools/agentic_cli.py run
# Note: re-run will restart from Step 0 (idempotent for completed steps)
```

### If proxy fails:
```bash
# Fabric falls back to offline simulation automatically
# Check proxy: curl http://localhost:8085/health
# Restart if needed
```

---

## Maintenance Tasks

### Registry Compaction
```bash
# Run once per session or when duplicates accumulate:
# 1. Dedup knowledge.jsonl — keep last by ID
# 2. Dedup agents.jsonl — keep last by category  
# 3. Dedup chain.jsonl — keep last by source_learning_id
```

### Hot Cache Cleanup
```bash
# Knowledge cache has max_learnings=200 cap
# Oldest entries evicted automatically when limit reached
# TTL support available per entry
```

### CI Pipeline
```bash
# 3 stages: syntax check → CLI smoke test → import chain test
bash scripts/ci.sh
```
