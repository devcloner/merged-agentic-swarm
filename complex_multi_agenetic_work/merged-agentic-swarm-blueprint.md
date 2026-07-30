# Merged Agentic Swarm Blueprint

This document merges two approaches into one operating system for high-concurrency agentic development:

1. The user's executable swarm pack: `opencode-swarm.json`, `claude-code-proxy.json`, `task-master-mcp.json`, `taskmaster-mcp-bridge.ts`, `master-architect-prompt.md`, and the bootstrap scripts.[cite:55][cite:56][cite:57][cite:58][cite:59][cite:61]
2. The stronger control-plane method: Claude Code as the durable agent factory, Task Master as the mandatory task spine, a provider-aware proxy fabric, gated wave execution, and a durable knowledge-box promotion loop.[cite:16]

The result is a hybrid architecture that keeps the user's concrete swarm topology and rate-limit handling, while fixing the weak points around provider flexibility, task discipline, durable learning, progress tracking, and obstacle recovery.[cite:55][cite:57][cite:59][cite:61]

## Core Position

The merged system should be run with **Claude Code as the agent authoring and supervisory control plane**, **Task Master as the shared source of truth for work state**, **OpenCode as the scalable worker execution plane**, and a **Claude-compatible proxy** that can either pool Anthropic keys or route presented Claude model names to other providers and local servers.[cite:55][cite:57][cite:59][cite:61]

This is the best merged stance because the user's pack already solves parallelism and runtime packaging well, but it under-specifies durable agent creation, provider abstraction, task-governed execution, and long-term learning promotion.[cite:55][cite:57][cite:58][cite:59]

## Why This Merged Design Wins

| Capability | User's swarm pack | Control-plane method | Merged result |
|---|---|---|---|
| Drop-in runtime shape | Strong; concrete JSON and scripts.[cite:55][cite:56] | Moderate; more architectural than executable. | Keep the pack structure. |
| Claude Code usage | Mostly editing tools for workers.[cite:55] | Primary agent factory and skills runtime. | Claude Code writes and governs agents. |
| Task Master usage | Present, but partly idealized package/tool names and looser governance.[cite:57][cite:61] | Mandatory parse, expand, next, status, and task-id discipline.[cite:16] | Task Master becomes the real spine. |
| Parallel execution | Strong 40-worker pool model.[cite:55] | Strong gating, weaker immediate topology. | Use the pool topology behind wave gates. |
| Learning loop | Good anomaly-triggered micro-spawn idea.[cite:55] | Better durable promotion into standing agents. | Use both hot and cold learning paths. |
| Proxy model fabric | Anthropic key-pool and retry logic only.[cite:59] | Multi-provider Claude-compatible routing. | Support both key pooling and backend routing. |
| Auditability | Some logs and task files.[cite:59][cite:61] | Better registries, chain logs, and explicit promotion lifecycle. | Add registries and chain files. |

## High-Level Operating Model

### Layer 1: Claude Code Control Plane

Claude Code is responsible for:

- Creating and updating durable agent definitions.
- Hosting the supervisory prompts and reusable skills.
- Calling Task Master through MCP or CLI.
- Deciding whether new learning becomes a temporary micro-agent or a durable specialist.
- Maintaining the progress report, blocker list, and phase-gate decisions.

Claude Code is the right place for this because the user explicitly wants Claude Code to be used for agent creation and integration, while also having access to OpenCode and a proxy that can present itself as Claude while routing elsewhere.[cite:31][cite:32][file:55]

### Layer 2: Task Master Task Spine

Task Master owns the project work state:

- PRD ingestion and parsing.
- Task creation and dependency graphing.
- Complexity analysis and expansion.
- Status transitions.
- Linking discoveries, blockers, and promoted learning to work items.

No implementation agent should edit code unless it has a Task Master task id or a Task Master-generated subtask id.[cite:16][cite:61]

### Layer 3: OpenCode Worker Plane

OpenCode runs the heavy parallel worker pools:

- Domain workers.
- Type-hardening workers.
- Test engineers.
- Security and accessibility auditors.

This preserves the user's excellent concurrency topology and lets Claude Code focus on orchestration, governance, and specialist authoring rather than being overloaded as a 40-process executor.[cite:55]

### Layer 4: Proxy Fabric

The proxy supports two operating modes:

1. **Anthropic key-pool mode**, which the user's current config already supports through weighted round-robin retries and request logging.[cite:59]
2. **Provider-routing mode**, where presented Claude model ids route to backends such as OpenRouter, Vertex AI, Azure OpenAI, or local OpenAI-compatible servers, which matches the user's stated requirement to use a Claude Code proxy that can run any model and present itself as major Claude models.[cite:32][cite:34]

### Layer 5: Learning and Recovery Fabric

The merged system has two learning paths:

- **Hot path:** anomaly events go to `.opencode/knowledge_cache.json`, triggering short-lived micro-specialists for acute incidents.[cite:55]
- **Cold path:** normalized knowledge-box records go into `docs/agentic/registry/knowledge.jsonl`; validated entries create durable new agent specs and chain links.

This split is important because not every runtime error deserves a permanent agent, but repeated patterns and important new reasoning should outlive one run.

## Final Directory Layout

```text
.
├── claude-code-proxy.json
├── opencode-swarm.json
├── task-master-mcp.json
├── taskmaster-mcp-bridge.ts
├── master-architect-prompt.md
├── setup-and-run.sh
├── .env
├── .claude/
│   ├── agents/
│   ├── skills/
│   └── commands/
├── .opencode/
│   ├── knowledge_cache.json
│   ├── ownership-map.json
│   └── proxy.log
├── .taskmaster/
│   ├── docs/
│   │   └── prd_agentic_codebase_optimization.txt
│   └── tasks/
│       └── tasks.json
└── docs/
    └── agentic/
        ├── RUNBOOK.md
        ├── AGENT_SPEC_CONTRACT.md
        ├── KNOWLEDGE_BOX_SCHEMA.md
        ├── WAVE_PLAN_40_AGENTS.md
        ├── providers/
        │   └── PROVIDER_REGISTRY.json
        └── registry/
            ├── agents.jsonl
            ├── knowledge.jsonl
            ├── chain.jsonl
            └── progress.json
```

This layout combines the user's real artifacts with the missing registries and Claude Code agent locations needed for durable operation.[cite:55][cite:56][cite:57][cite:59][cite:61]

## Detailed Execution Plan

### Phase 0: Wire the Control Plane

1. Start the proxy and verify it responds.
2. Initialize Task Master and confirm the task state path and PRD path are valid.
3. Ensure Claude Code has access to the Task Master MCP server config.
4. Create the durable registries and progress ledger.
5. Run a proxy smoke test, Task Master list/status test, and a write test to the progress ledger.

This phase exists to prevent the common failure mode in the user's current scripts where the swarm begins before the state model, cleanup behavior, and health checks are fully proven.[cite:56][cite:60]

### Phase 1: PRD Optimization and Parse Readiness

1. Ingest the existing PRD.
2. Rewrite it into Task Master-friendly structure.
3. Check missing acceptance criteria, constraints, deliverables, and test strategy.
4. Store the optimized PRD in `.taskmaster/docs/`.
5. Run Task Master parse and complexity analysis.
6. Expand tasks above a configurable threshold.

This gives the worker pools a clean and dependency-aware task graph instead of a vague instruction blob.[cite:16]

### Phase 2: Repository Mapping and Gap Analysis

1. Run the codebase map agents.
2. Build the dependency and entrypoint view.
3. Compare the codebase structure to the parsed task graph.
4. Mark contradictions, missing contracts, and high-risk zones.
5. Do not unlock Phase 3 until the gap report passes the gate.

This keeps the user's excellent AST/gap concept but makes it a hard prerequisite instead of a soft narrative step.[cite:55][cite:57]

### Phase 3: Controlled Worker Pool Ramp-Up

1. Start with a small concurrency cap, such as 4 or 8.
2. Confirm task completion, status sync, and file ownership behavior.
3. Expand to the full concurrency target only when the low-concurrency pilot is stable.
4. Assign pool workers by Task Master task ids and owned path globs.

The user's current `max_concurrency: 40` is useful, but it should be ramped rather than launched at full load immediately.[cite:55]

### Phase 4: Learning, Recovery, and Specialist Promotion

1. Watch runtime events and worker anomalies.
2. If a severe acute event occurs, spawn a temporary micro-specialist.
3. If a finding reflects a repeatable pattern, create a knowledge-box entry.
4. Validate the knowledge-box entry.
5. If promoted, generate a durable new agent definition via Claude Code and register it in the chain.

This is the merged answer to the user's requirement that an agent should create other agents based on learned knowledge and reasoned conclusions.[cite:55][cite:57]

### Phase 5: Synthesis, Docs, and Iterative Improvement

1. Generate updated PRD output, architecture docs, and migration notes.
2. Produce a current-state progress report.
3. Ask reflective questions based on unresolved blockers, repeated fixes, and model/provider performance.
4. Feed those answers back into Task Master or the agent registry.

This transforms the system from a one-run swarm into a reusable operating loop.

## Precedence and Variable Rules

The system should use explicit precedence so the agent does not lose control when many components interact.

### Global Precedence Order

1. **Human operator input**: explicit user instructions override everything else.
2. **Runtime safety constraints**: secrets, destructive actions, and hard environment limitations override other automation goals.
3. **Task Master state**: task ids, dependency order, and statuses govern what work is active.
4. **Phase gate rules**: no pool escalation if a gate is red.
5. **Agent-specific config**: local worker behavior, model tier, retries, and owned paths.
6. **Dynamic recovery rules**: obstacle handling, fallback provider routing, micro-agent spawn.

### Environment Variable Precedence

```text
CLI flag > exported shell env > .env > config file default > hardcoded fallback
```

### Key Variables

| Variable | Purpose | Precedence note |
|---|---|---|
| `REPO_ROOT` | Working repository root | Must match Task Master project root. |
| `PRD_INPUT_PATH` | Source PRD file | Overrides default PRD location if set. |
| `TASKMASTER_PROJECT_ROOT` | Task Master project root | Must be kept aligned with repo root.[cite:61] |
| `TASKMASTER_STATE_FILE` | Task ledger file | Prefer the `.taskmaster/tasks/` path pattern. |
| `ANTHROPIC_BASE_URL` | Claude-compatible proxy endpoint | Read at Claude Code process start.[cite:48] |
| `ANTHROPIC_API_KEY` | Proxy auth or direct Anthropic auth | May be synthetic if proxy injects keys. |
| `SWARM_MAX_CONCURRENCY` | Hard upper bound for worker count | Should be ramped, not blindly maxed. |
| `MODEL_TIER_MAIN` | Default general reasoning model | Routed by provider registry. |
| `MODEL_TIER_DEEP` | Deep review and complex planning model | Routed by provider registry. |
| `MODEL_TIER_FAST` | Cheap high-volume model | Routed by provider registry. |
| `PHASE_GATE_STRICT` | Whether to halt on red gate | Default should be true. |
| `HUMAN_GATE_REQUIRED` | Require human approval at key checkpoints | Recommended true in complex runs. |

## Merged Example Configs

### 1. `claude-code-proxy.json`

```json
{
  "server": {
    "host": "127.0.0.1",
    "port": 8080,
    "max_concurrent_connections": 100,
    "keep_alive_timeout_sec": 60
  },
  "load_balancing": {
    "strategy": "round_robin_weighted",
    "retry_on_status": [429, 500, 502, 503, 504],
    "max_retries": 8,
    "initial_backoff_ms": 250,
    "max_backoff_ms": 10000
  },
  "key_pool": [
    {
      "id": "anthropic-primary-01",
      "provider": "anthropic",
      "api_key_env": "ANTHROPIC_API_KEY_POOL_1",
      "weight": 10,
      "rate_limit_rpm": 4000
    },
    {
      "id": "anthropic-primary-02",
      "provider": "anthropic",
      "api_key_env": "ANTHROPIC_API_KEY_POOL_2",
      "weight": 10,
      "rate_limit_rpm": 4000
    },
    {
      "id": "anthropic-backup-03",
      "provider": "anthropic",
      "api_key_env": "ANTHROPIC_API_KEY_POOL_3",
      "weight": 5,
      "rate_limit_rpm": 2000
    }
  ],
  "presented_models": {
    "claude-opus-4": {
      "routing_tier": "deep",
      "backend": "openrouter",
      "backend_model": "anthropic/claude-opus-4"
    },
    "claude-sonnet-4": {
      "routing_tier": "main",
      "backend": "vertex",
      "backend_model": "claude-sonnet-4"
    },
    "claude-haiku": {
      "routing_tier": "fast",
      "backend": "local-openai-compatible",
      "backend_model": "qwen2.5-coder"
    }
  },
  "backends": {
    "openrouter": {
      "type": "openai_compatible",
      "base_url": "https://openrouter.ai/api/v1",
      "auth_env": "OPENROUTER_API_KEY"
    },
    "vertex": {
      "type": "anthropic_compatible",
      "base_url": "https://vertex-proxy.example/v1",
      "auth_env": "VERTEX_PROXY_KEY"
    },
    "local-openai-compatible": {
      "type": "openai_compatible",
      "base_url": "http://127.0.0.1:11434/v1",
      "auth_env": null
    }
  },
  "request_header_overrides": {
    "x-app-name": "Merged-Agentic-Swarm",
    "anthropic-beta": "prompt-caching-2024-07-25"
  },
  "logging": {
    "level": "info",
    "file": ".opencode/proxy.log",
    "log_metrics": true,
    "log_backend_route": true
  }
}
```

This keeps the user's working rate-limit strategy while adding the provider-routing layer they explicitly asked for.[cite:59][cite:32]

### 2. `task-master-mcp.json`

```json
{
  "mcpServers": {
    "task-master-ai": {
      "command": "npx",
      "args": ["-y", "task-master-ai"],
      "env": {
        "TASKMASTER_PROJECT_ROOT": ".",
        "TASKMASTER_STATE_FILE": ".taskmaster/tasks/tasks.json",
        "TASKMASTER_LOG_LEVEL": "info",
        "ANTHROPIC_BASE_URL": "http://127.0.0.1:8080",
        "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}"
      }
    }
  }
}
```

This adapts the user's Task Master MCP idea to a more realistic Task Master entrypoint pattern and a better state path layout.[cite:61][cite:16]

### 3. `opencode-swarm.json`

```json
{
  "$schema": "https://example.local/schemas/opencode-swarm.schema.json",
  "version": "3.0.0",
  "project": {
    "name": "Merged-Agentic-Codebase-Swarm",
    "description": "Claude Code governed, Task Master spine, OpenCode worker swarm, provider-aware proxy routing.",
    "root_dir": "./",
    "knowledge_graph_path": ".opencode/knowledge_cache.json",
    "task_master_state": ".taskmaster/tasks/tasks.json",
    "ownership_map": ".opencode/ownership-map.json",
    "progress_report": "docs/agentic/registry/progress.json"
  },
  "orchestrator": {
    "runner": "opencode-architect",
    "control_plane": "claude-code",
    "max_concurrency": 40,
    "ramp_sequence": [4, 8, 16, 24, 40],
    "proxy_endpoint": "http://127.0.0.1:8080/v1",
    "telemetry_enabled": true,
    "heartbeat_interval_ms": 1000,
    "retry_policy": {
      "max_retries": 5,
      "backoff_factor": 1.5,
      "jitter": true
    },
    "phase_gates": {
      "phase_1_required": true,
      "phase_2_required": true,
      "human_gate_before_full_concurrency": true
    }
  },
  "control_agents": [
    {
      "id": "cc-orchestrator",
      "runtime": "claude-code",
      "goal": "Own phases, gates, promotions, and progress reporting.",
      "model_tier": "deep"
    },
    {
      "id": "tm-operator",
      "runtime": "claude-code",
      "goal": "Ensure all work is mapped to Task Master ids and statuses.",
      "model_tier": "main"
    },
    {
      "id": "spawn-gate",
      "runtime": "claude-code",
      "goal": "Promote validated knowledge into durable agent specs and chain entries.",
      "model_tier": "main"
    },
    {
      "id": "budget-route-auditor",
      "runtime": "claude-code",
      "goal": "Track routing, cost, retries, and provider drift.",
      "model_tier": "fast"
    }
  ],
  "phase_1_agents": [
    {
      "id": "prd-decomposer",
      "runtime": "claude-code",
      "goal": "Parse and normalize PRD content into Task Master-friendly atomic tasks.",
      "task_master_required": true
    },
    {
      "id": "codebase-ast-mapper",
      "runtime": "opencode",
      "goal": "Map repo structure, imports, edges, and critical modules."
    },
    {
      "id": "spec-gap-detector",
      "runtime": "claude-code",
      "goal": "Compare Task Master tasks against mapped codebase reality and block unsafe progression."
    }
  ],
  "agent_pools": [
    {
      "pool_id": "domain-module-workers",
      "phase": 3,
      "instances": 10,
      "id_prefix": "domain-worker-",
      "runtime": "opencode",
      "model_tier": "main",
      "task_tags": ["domain", "feature", "api"],
      "owned_paths": ["src/api/**", "src/services/**", "src/features/**"]
    },
    {
      "pool_id": "ast-type-hardening-workers",
      "phase": 3,
      "instances": 10,
      "id_prefix": "type-hardening-",
      "runtime": "opencode",
      "model_tier": "fast",
      "task_tags": ["types", "imports", "lint"],
      "owned_paths": ["src/**/*.ts", "src/**/*.tsx"]
    },
    {
      "pool_id": "test-coverage-engineers",
      "phase": 3,
      "instances": 10,
      "id_prefix": "test-engineer-",
      "runtime": "opencode",
      "model_tier": "main",
      "task_tags": ["test", "integration", "perf"],
      "owned_paths": ["tests/**", "src/**/*.test.*", "src/**/*.spec.*"]
    },
    {
      "pool_id": "security-a11y-auditors",
      "phase": 3,
      "instances": 10,
      "id_prefix": "sec-a11y-auditor-",
      "runtime": "opencode",
      "model_tier": "deep",
      "task_tags": ["security", "a11y", "compliance"],
      "owned_paths": ["src/ui/**", "src/auth/**", "src/web/**"]
    }
  ],
  "dynamic_learning_loop": {
    "hot_cache": ".opencode/knowledge_cache.json",
    "cold_registry": "docs/agentic/registry/knowledge.jsonl",
    "chain_registry": "docs/agentic/registry/chain.jsonl",
    "micro_spawn_policy": {
      "max_lifespan_sec": 300,
      "severity_threshold": "HIGH"
    },
    "promotion_policy": {
      "require_evidence": true,
      "require_claim": true,
      "require_task_link": true,
      "write_durable_agent": true
    }
  }
}
```

This version preserves the user's pool structure but adds a proper split between control-plane agents, worker pools, path ownership, phase gates, progress reporting, and durable promotion.[cite:55]

### 4. `setup-and-run.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="${REPO_ROOT:-$(pwd)}"
PRD_INPUT_PATH="${PRD_INPUT_PATH:-$REPO_ROOT/.taskmaster/docs/prd_agentic_codebase_optimization.txt}"
SWARM_MAX_CONCURRENCY="${SWARM_MAX_CONCURRENCY:-40}"
HUMAN_GATE_REQUIRED="${HUMAN_GATE_REQUIRED:-true}"

cd "$REPO_ROOT"
mkdir -p .opencode .taskmaster/tasks .taskmaster/docs docs/agentic/registry docs/agentic/providers .claude/agents .claude/skills
: > .opencode/knowledge_cache.json
: > docs/agentic/registry/agents.jsonl
: > docs/agentic/registry/knowledge.jsonl
: > docs/agentic/registry/chain.jsonl

cleanup() {
  [[ -n "${PROXY_PID:-}" ]] && kill "$PROXY_PID" 2>/dev/null || true
  [[ -n "${BRIDGE_PID:-}" ]] && kill "$BRIDGE_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

echo "== Phase 0: starting proxy =="
npx claude-code-proxy --config claude-code-proxy.json &
PROXY_PID=$!
sleep 2

echo "== Phase 0: initializing Task Master =="
npx -y task-master-ai init || true
npx ts-node taskmaster-mcp-bridge.ts &
BRIDGE_PID=$!

if [[ ! -f "$PRD_INPUT_PATH" ]]; then
  echo "Missing PRD at $PRD_INPUT_PATH"
  exit 1
fi

echo "== Phase 1: parse and inspect PRD =="
npx -y task-master-ai parse-prd "$PRD_INPUT_PATH" || true
npx -y task-master-ai list || true

echo "== Phase 1 gate: waiting for Claude Code supervisor approval =="
if [[ "$HUMAN_GATE_REQUIRED" == "true" ]]; then
  echo "Review PRD parse, complexity, and gap report before full ramp."
fi

echo "== Phase 2+: launch swarm with controlled ramp-up =="
npx opencode-swarm run --config opencode-swarm.json --max-concurrency "$SWARM_MAX_CONCURRENCY"
```

This script fixes the duplicate-launcher problem, establishes cleanup before the blocking run, creates the registries, and makes PRD path and concurrency explicit variables.[cite:56][cite:60]

### 5. `docs/agentic/providers/PROVIDER_REGISTRY.json`

```json
{
  "version": 1,
  "tiers": {
    "deep": ["claude-opus-4"],
    "main": ["claude-sonnet-4"],
    "fast": ["claude-haiku"]
  },
  "policy": {
    "default_tier_by_role": {
      "architect": "deep",
      "tm-operator": "main",
      "spawn-gate": "main",
      "bulk-refactor": "main",
      "type-fix": "fast",
      "test-writer": "main",
      "security-review": "deep"
    },
    "fallback_order": ["main", "fast", "deep"],
    "degrade_on_rate_limit": true,
    "degrade_on_budget_pressure": true
  }
}
```

This gives the swarm a policy layer for model selection rather than hardcoding one model across every role as in the current pack.[cite:55]

## Feature Highlights and Reasoned Advantages

### 1. Real task-governed execution

The merged design makes Task Master the execution spine rather than a decorative attachment. That improves clarity, resumability, dependency control, and auditability because every worker action maps to a specific task record.[cite:61][cite:16]

### 2. Better use of Claude Code

Claude Code becomes more than an edit tool. It becomes the place where long-lived intelligence is created, refined, and chained. That aligns better with the user's stated goal to use Claude Code for agent creation and integrated orchestration.[cite:31]

### 3. Practical multi-provider abstraction

The current proxy solves one bottleneck: Anthropic key rate limits.[cite:59] The merged proxy solves the broader operator problem: use the same Claude-facing control flow while swapping backends, fallback paths, or cheaper tiers when the environment changes.[cite:32][cite:34]

### 4. Better obstacle recovery without losing progress

The merged system keeps progress through:

- Task Master statuses.
- Progress ledger snapshots.
- File ownership maps.
- Micro-specialists for local acute failures.
- Durable promotions for recurring knowledge.

This is better than either approach alone because it handles both immediate fixes and strategic learning.

### 5. Safer high concurrency

The user already has a good 40-agent topology.[cite:55] The merged design simply makes it safer by requiring gates, staged ramp-up, and ownership rules before the full load begins.

## Markers of Success

The system should explicitly report success markers so the operator and supervising agents know whether the workflow is healthy.

### Control-plane success

- Proxy healthy and routing logs visible.
- Task Master initialized and returning task state.
- Claude Code can access Task Master tools.
- Registries and progress ledger writable.

### PRD success

- PRD parsed without critical structural failures.
- Complexity analysis completed.
- Tasks expanded where complexity is high.
- Gap detector marks readiness for worker phase.

### Worker-phase success

- Every active worker has a task id.
- No unowned file edits.
- Retry counts remain within threshold.
- Test pass rate is stable or improving.
- Security and accessibility reviews produce actionable findings rather than generic summaries.

### Learning-loop success

- Anomalies are logged.
- At least some anomalies are normalized into knowledge boxes.
- At least one knowledge-box entry is promoted into a durable agent.
- Chain log shows parent-child relationships.

### Final synthesis success

- PRD V2 or equivalent updated specification exists.
- Docs are generated.
- Progress report shows completion percentages by phase and pool.
- Outstanding blockers and next steps are explicit.

## Progress Report Model

The workflow should continuously update a machine-readable progress ledger.

Example: `docs/agentic/registry/progress.json`

```json
{
  "run_id": "2026-07-29T07:00:00Z",
  "overall_completion_pct": 38,
  "phase_status": {
    "phase_0": { "status": "done", "completion_pct": 100 },
    "phase_1": { "status": "done", "completion_pct": 100 },
    "phase_2": { "status": "in_progress", "completion_pct": 70 },
    "phase_3": { "status": "in_progress", "completion_pct": 25 },
    "phase_4": { "status": "not_started", "completion_pct": 0 }
  },
  "pool_status": {
    "domain-module-workers": { "assigned": 12, "done": 4, "blocked": 1 },
    "ast-type-hardening-workers": { "assigned": 10, "done": 6, "blocked": 0 },
    "test-coverage-engineers": { "assigned": 8, "done": 2, "blocked": 1 },
    "security-a11y-auditors": { "assigned": 6, "done": 1, "blocked": 0 }
  },
  "blockers": [
    "Task 14.2 waiting for schema clarification.",
    "Rate-limit spikes observed on backup key pool."
  ],
  "recent_promotions": [
    "kb-20260729-001 -> agent-perf-hotspot-mapper"
  ],
  "next_recommended_actions": [
    "Finish Phase 2 gate validation.",
    "Resolve Task 14.2 ambiguity before full ramp to 40."
  ]
}
```

This gives the system a live self-reporting model rather than vague claims of progress.

## Obstacle Handling Rules

The agent should be explicitly instructed to preserve progress while adapting around obstacles.

### If the proxy fails

- Retry local endpoint health checks.
- Fall back to a backup provider path if available.
- Mark the impacted pool as degraded rather than globally failed.
- Preserve Task Master state and progress report.

### If Task Master tools fail

- Retry with direct CLI.
- If MCP is down, use the CLI path temporarily.
- Log a recovery note and continue in a restricted mode until TM sync is restored.

### If a pool thrashes or conflicts appear

- Lower concurrency.
- Tighten ownership map.
- Convert high-conflict tasks into smaller expanded subtasks.

### If a worker repeatedly fails

- Mark the task blocked.
- Spawn a micro-specialist if the failure is local and acute.
- Promote to durable specialist only if the pattern recurs or has strategic importance.

### If the PRD is too vague

- Pause implementation.
- Create clarification tasks in Task Master.
- Ask deep clarification questions and rewrite the PRD before resuming.

## Where to Begin

1. Verify binaries and actual package names in the target server environment.
2. Implement the merged proxy config.
3. Convert the bootstrap script into the single merged script.
4. Add the provider registry and progress ledger.
5. Rewrite the architect prompt to enforce Task Master discipline, phase gates, promotions, and ownership rules.
6. Run Phase 0 and Phase 1 only.
7. Review the parse/gap outputs.
8. Ramp worker concurrency gradually.

This order matters because it reduces blast radius while still preserving the user's desire for a serious, highly autonomous, high-throughput operation.

## End-State Usage

Once fully implemented, this merged system becomes a reusable autonomous development runtime that can:

- Ingest and optimize PRDs.
- Generate and govern structured work.
- Perform large-scale parallel implementation and analysis.
- Learn from its own mistakes and discoveries.
- Turn repeated reasoning into reusable specialist agents.
- Produce clear progress reports, docs, and updated project intelligence.

That is the overall goal: not just a one-time swarm, but a compounding agentic operating environment.
