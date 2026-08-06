# Merged Agentic Swarm

Multi-agent orchestration system with a 5-phase workflow, 40-worker OpenCode pools, a
provider-aware model fabric, and a cold-path knowledge learning loop.

`merged-agentic-swarm` decomposes a PRD into atomic tasks, maps the codebase, dispatches
waves of OpenCode workers, verifies the integration with an adversarial gate, and promotes
validated learnings into durable agent specs — so the system gets better across runs.

**Current version:** 1.6.0 · Python ≥3.14 · **Status:** active development

---

## Why this exists

Most "agent swarms" run a handful of agents once and forget the results. This one is built
around two ideas:

1. **Wave-scaled worker pools** — the orchestrator ramps from 4 → 40 OpenCode workers across
   phases, gated so unsafe progression is blocked before full concurrency.
2. **Cold-path learning** — every run's validated findings are promoted from the hot cache into
   durable registries (`knowledge.jsonl`, `agents.jsonl`, `chain.jsonl`), so future runs start
   from what previous runs already proved.

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│  agentic-cli run                                                  │
│                                                                  │
│  Step 0  System init + proxy check                                │
│  Step 1  PRD optimization & parsing (Task Master AI)              │
│  Step 2  Codebase map & spec-gap closure                          │
│  Step 3  Wave 1 — key-pool proxy + model fabric gate              │
│  Step 4  Wave 2 — OpenCode 40-worker swarm + durable agents       │
│  Step 5  Wave 3 — integration & verification gate                 │
│  Step 5.5 Wave 4 — synthesis & final reporting                    │
│  Step 6  Summary & state preservation                             │
│                                                                  │
│  cold-path learning loop: hot cache → knowledge/agents/chain      │
└──────────────────────────────────────────────────────────────────┘
```

### Key components

| Component | Path | Role |
|-----------|------|------|
| Orchestrator | `src/merged_agentic_swarm/tools/agentic_orchestrator.py` | 6-step run, wave gates, promotions |
| CLI | `src/merged_agentic_swarm/tools/agentic_cli.py` | `run` / `status` / `promote` / `config` |
| Model fabric | `src/merged_agentic_swarm/providers/multi_provider_fabric.py` | litellm-first cascade with fallbacks |
| Key pools | `src/merged_agentic_swarm/providers/key_pool.py` | rotating provider keys + cooldown |
| Fast fallback | `src/merged_agentic_swarm/fast_pool.py`, `fast_fallback.py` | tiered failover across local proxies |
| Streaming proxy | `src/merged_agentic_swarm/streaming_proxy.py` | SSE worker API |
| Latency tracker | `src/merged_agentic_swarm/latency_tracker.py` | TTFB / total / tokens-per-sec percentiles |
| CloudCLI client | `src/merged_agentic_swarm/services/cloudcli_service.py` | trigger remote agents via cloneclove.com (`CLOUDCLI_API_KEY`) |
| Wave gate | `src/merged_agentic_swarm/services/wave_gate_service.py` | blocks unsafe progression |
| Learning cache | `src/merged_agentic_swarm/tools/knowledge_cache.py` | hot-cache → cold-registry promotion |
| Worker pools | `opencode-swarm.json` | 4 pool definitions, ramp `[4,8,16,24,40]` |
| Providers | `docs/agentic/providers/` | provider registry + routing policy |

### Model fabric (routing)

The `multi_provider_fabric` cascades through providers in order, moving to the next when the
current is throttled or failing:

1. **litellm** (local `:4000`, 42-key rotating Gemini pool) — primary
2. **fcc-server** / routatic proxy — local fallbacks
3. **opencode-go** / aerolink — downstream pools

## Quickstart

```bash
# Install (requires Python 3.14+ and uv)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync

# Run the full orchestrator
uv run agentic-cli run

# Inspect state
uv run agentic-cli status      # completion %, phases, registry counts, blockers
uv run agentic-cli config      # key pools, routes, swarm state

# Force cold-path promotion of validated learnings
uv run agentic-cli promote

# Tests
uv run pytest -v --tb=short
```

### CLI reference

```
agentic-cli run        Run full orchestrator workflow (--verbose for detail)
agentic-cli status     Show system status (completion %, phases, blockers, registries)
agentic-cli promote    Force cold-path promotion without running the full orchestrator
agentic-cli config     Show configuration state (key pools, routes, swarm)
```

## Worker configuration (ultraswarm)

The swarm dispatches workers through the **ultraswarm** runner
(`ultraswarm.config.json`, same repo). Five CLIs are wired:

| Worker | Route | Tier mapping |
|--------|-------|--------------|
| `opencode` | litellm gemini (2.5-flash → 3.5 → 3.6) | fast → expert |
| `codex` | aerolink (`gpt-5.6-sol` / `gpt-5.6-terra`) | simple → expert |
| `agy` | antigravity gemini, worktree-aware (`--add-dir`) | all tiers |
| `pi` | litellm via openai provider | all tiers |
| `claude` | Claude Code CLI | all tiers |

`maxParallelWorkers: 12`, `LITELLM_PROXY_KEY` passed through worker env. Run
`uv run agentic-cli status` and check the WORKER ROSTER for live health.

## Learning loop

Each run promotes validated findings from the hot cache into three cold registries under
`docs/agentic/registry/`:

- **`knowledge.jsonl`** — proven solutions (78 entries)
- **`agents.jsonl`** — durable agent specs (22 entries)
- **`chain.jsonl`** — spawn chain entries (22 entries)

`agentic-cli status` reports the counts. Promotion requires evidence, a claim, and a task
link (see `opencode-swarm.json` → `promotion_policy`).

## Development

```bash
# CI (ruff + pytest + import-chain + syntax) — run before pushing
./scripts/ci.sh

# Formatter
uv run ruff check . --fix
uv run ruff format .

# Single test file
uv run pytest tests/test_agentic_cli.py -v
```

**Versioning:** every `main` commit changing production files bumps `pyproject.toml`
(PATCH for fixes, MINOR for features, MAJOR for breaking) and re-locks `uv.lock`.

## Documentation

- `docs/swarm_project_prd.md` — project PRD
- `docs/agentic/` — agent registry, providers, registry data
- `docs/stack-analysis-2026-08-06.md` — deep audit (49 verified findings, ranked priorities)
- `docs/agentic/PROXY_GUIDE.md` — the local proxy stack (fcc-server, routatic, litellm)

## Known issues

Tracked on the GitHub issues board. Current priorities (see
`docs/stack-analysis-2026-08-06.md` for full detail):

- **Security (user action):** rotate the opencode-go key + revoke the GitHub PAT from history
- **High:** litellm container env stale (keys 36–42 unset) → ~1/6 first-attempt 401s
- **High:** concurrency ramp hard-capped at 4 workers
- **High:** fcc-server admin custom-provider creation 500s (signature mismatch)

## License

Not yet licensed — contact the maintainer before reuse.

---

Built and maintained by [devcloner](https://github.com/devcloner).
