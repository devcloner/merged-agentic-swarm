#!/usr/bin/env bash
# Merged Agentic Swarm — setup and run
# Adapted from blueprint §4 to match this environment's actual binaries.
set -euo pipefail

REPO_ROOT="${REPO_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}"
PRD_INPUT_PATH="${PRD_INPUT_PATH:-$REPO_ROOT/.taskmaster/docs/prd_agentic_codebase_optimization.md}"
SWARM_MAX_CONCURRENCY="${SWARM_MAX_CONCURRENCY:-40}"
HUMAN_GATE_REQUIRED="${HUMAN_GATE_REQUIRED:-true}"

cd "$REPO_ROOT"

# ── Phase 0: scaffold (idempotent) ──────────────────────────────────────────
mkdir -p .opencode .taskmaster/tasks .taskmaster/docs \
  docs/agentic/registry docs/agentic/providers \
  .claude/agents .claude/skills .claude/commands
: > .opencode/knowledge_cache.json
: > docs/agentic/registry/agents.jsonl
: > docs/agentic/registry/knowledge.jsonl
: > docs/agentic/registry/chain.jsonl

cleanup() {
  [[ -n "${PROXY_PID:-}" ]] && kill "$PROXY_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

echo "== Phase 0: starting Python proxy on port 8085 =="
python3 -m proxy.claude_proxy_server &
PROXY_PID=$!
sleep 2

# Health check
if curl -sf http://127.0.0.1:8085/health >/dev/null 2>&1; then
  echo "  Proxy health: OK"
else
  echo "  WARNING: proxy health check failed"
fi

echo "== Phase 0: verifying registries =="
for f in \
  docs/agentic/registry/knowledge.jsonl \
  docs/agentic/registry/agents.jsonl \
  docs/agentic/registry/chain.jsonl \
  docs/agentic/registry/progress.json; do
  if [[ -f "$f" ]]; then echo "  $f ✓"; else echo "  $f MISSING"; fi
done

if [[ ! -f "$PRD_INPUT_PATH" ]]; then
  echo "Missing PRD at $PRD_INPUT_PATH"
  exit 1
fi

echo "== Phase 1: parse PRD via Python task spine =="
python3 -m tools.agentic_cli parse-prd --file "$PRD_INPUT_PATH"
python3 -m tools.agentic_cli status

echo "== Phase 1 gate: human review =="
if [[ "$HUMAN_GATE_REQUIRED" == "true" ]]; then
  echo "  Review PRD parse output above before continuing."
  echo "  Check: task graph correctness, complexity estimates, spec gaps."
fi

echo ""
echo "── Setup complete. Run Phase 2+ with: ──"
echo "  python3 -m tools.agentic_cli map-codebase"
echo "  python3 -m tools.agentic_cli run-all"
echo ""
echo "Proxy PID: $PROXY_PID  (run 'kill $PROXY_PID' to stop)"
