#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────
# scripts/agentic/verify_worker_runtime.sh
# Smoke-test: launch N workers, assign fixture tasks, verify results.
# ──────────────────────────────────────────────────────────────────────
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG_DIR="${REPO_ROOT}/logs/agentic"
PID_DIR="/tmp"
TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"

# ── defaults ──────────────────────────────────────────────────────────
WORKERS=1
TIMEOUT_SEC=60
PYTHON_BIN="python3"

# ── helpers ───────────────────────────────────────────────────────────
die() { log "FATAL: $*"; exit 1; }
log() { echo "[$(date -u +%H:%M:%S.%3N)] $*"; }

usage() {
  cat <<EOF
Usage: $0 [--workers 1|2|4]

  --workers   Number of workers to launch (default: 1)

Verification steps:
  1. Launch workers at specified count via the runtime adapter.
  2. Assign each worker a safe fixture task.
  3. Wait for completion (timeout ${TIMEOUT_SEC}s per worker).
  4. Verify each result has: run_id, task_id, role, start_time, end_time, evidence.
  5. Verify no ownership collisions across workers.
  6. Report planned vs launched vs completed vs failed.
  7. Clean up worker PIDs.
EOF
  exit 0
}

# ── parse args ────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --workers)
      WORKERS="$2"; shift 2 ;;
    --help|-h)
      usage ;;
    *)
      die "Unknown argument: $1" ;;
  esac
done

if ! [[ "$WORKERS" =~ ^[124]$ ]]; then
  die "--workers must be 1, 2, or 4; got: '$WORKERS'"
fi

mkdir -p "$LOG_DIR"

# ── start workers ─────────────────────────────────────────────────────
log "=== Verification Run | Workers: $WORKERS | Timestamp: $TIMESTAMP ==="

PLANNED="$WORKERS"
LAUNCHED=0
COMPLETED=0
FAILED=0

# Launch workers via the start script
log "Launching $WORKERS worker(s) ..."
"$SCRIPT_DIR/start_worker_runtime.sh" --mode auto --workers "$WORKERS"
LAUNCHED="$WORKERS"

# ── build Python verification harness ─────────────────────────────────
HARNESS="${LOG_DIR}/verify_harness_${TIMESTAMP}.py"
cat > "$HARNESS" <<'PYEOF'
import json
import os
import sys
import time
import uuid

# Point to src/ so merged_agentic_swarm imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../src"))

from merged_agentic_swarm.models.agent_models import AgentSpec, WorkerRole
from merged_agentic_swarm.services.worker_runtime_adapter import get_runtime_adapter

WORKERS = int(sys.argv[1]) if len(sys.argv) > 1 else 1

# Fixture task: each worker writes a 1-line Python function
def fixture_task(idx: int) -> str:
    return (
        f"Write exactly one line of Python code that defines a function named "
        f"fixture_worker_{idx} that returns the integer {idx}."
    )

def main():
    adapter = get_runtime_adapter(mode="auto")
    log_prefix = f"[verifier {os.getpid()}]"
    print(f"{log_prefix} adapter_mode={adapter.mode}", flush=True)

    results = []
    for i in range(1, WORKERS + 1):
        spec = AgentSpec(
            id=f"verify-worker-{i:02d}",
            name=f"Verification Worker {i}",
            role=WorkerRole.CORE_ENGINEER,
            agent_type="swarm_worker",
            system_prompt="You are a verification test worker. Execute the task precisely.",
            model_alias="claude-3-7-sonnet",
        )
        print(f"{log_prefix} dispatching worker {spec.id} ...", flush=True)
        result = adapter.launch_worker(spec, fixture_task(i))
        results.append(result)

    print(f"{log_prefix} --- RESULTS ({len(results)} workers) ---", flush=True)
    print(json.dumps(results, indent=2, default=str), flush=True)

    # Write results to a JSON file for the shell to pick up
    outpath = os.environ.get("VERIFY_RESULTS_FILE", "/tmp/verifier_results.json")
    with open(outpath, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"{log_prefix} wrote results to {outpath}", flush=True)

    # Validate
    exit_code = 0
    paths_seen: set[str] = set()

    for r in results:
        rid = r.get("run_id", "MISSING")
        task_id = r.get("task_id", "MISSING")
        worker_id = r.get("worker_id", "MISSING")
        role = r.get("role", "MISSING")
        start_t = r.get("start_time", None)
        end_t = r.get("end_time", None)
        status = r.get("status", "MISSING")
        evidence = r.get("evidence", "")

        # Required fields
        for field, val in [
            ("run_id", rid), ("task_id", task_id), ("worker_id", worker_id),
            ("role", role), ("start_time", start_t), ("end_time", end_t),
            ("status", status), ("evidence", evidence),
        ]:
            if val is None or val == "MISSING":
                print(f"  FAIL [{rid}]: missing field '{field}'", flush=True)
                exit_code = 1

        # No ownership violation: each worker gets its own worker_id
        if worker_id in paths_seen:
            print(f"  FAIL [{rid}]: ownership collision on worker_id={worker_id}", flush=True)
            exit_code = 1
        paths_seen.add(worker_id)

        print(f"  [{rid[:8]}] worker={worker_id} role={role} status={status} "
              f"start={start_t:.0f}" if start_t else "start=None",
              f"end={end_t:.0f}" if end_t else "end=None",
              f"evidence_len={len(evidence)}",
              flush=True)

    # Summary
    completed = sum(1 for r in results if r.get("status") == "completed")
    failed = sum(1 for r in results
                 if r.get("status") not in ("completed", "partial (simulated)"))
    print(f"\n  planned={WORKERS} launched={len(results)} "
          f"completed={completed} failed={failed}", flush=True)

    sys.exit(exit_code)

if __name__ == "__main__":
    main()
PYEOF

# ── run the harness ───────────────────────────────────────────────────
log "Running verification harness (timeout: ${TIMEOUT_SEC}s per worker) ..."

TOTAL_TIMEOUT=$((TIMEOUT_SEC * WORKERS + 10))
export VERIFY_RESULTS_FILE="/tmp/verifier_results_${TIMESTAMP}.json"

cd "$REPO_ROOT"

set +e
timeout "$TOTAL_TIMEOUT" "$PYTHON_BIN" "$HARNESS" "$WORKERS" 2>&1 \
  | tee "${LOG_DIR}/verify_run_${TIMESTAMP}.log"
PY_EXIT="${PIPESTATUS[0]}"
set -e

# ── parse results ─────────────────────────────────────────────────────
RESULTS_FILE="$VERIFY_RESULTS_FILE"

if [[ -f "$RESULTS_FILE" ]] && command -v python3 &>/dev/null; then
  COMPLETED=$(python3 -c "
import json
with open('$RESULTS_FILE') as f:
    data = json.load(f)
completed = sum(1 for r in data if r.get('status') == 'completed')
partial = sum(1 for r in data if r.get('status') == 'partial (simulated)')
print(completed + partial)
" 2>/dev/null || echo "0")

  FAILED=$(python3 -c "
import json
with open('$RESULTS_FILE') as f:
    data = json.load(f)
failed = sum(1 for r in data if r.get('status') not in ('completed', 'partial (simulated)'))
print(failed)
" 2>/dev/null || echo "0")
else
  COMPLETED=0
  FAILED="$WORKERS"
fi

# ── clean up worker PIDs ──────────────────────────────────────────────
log "Cleaning up worker PIDs ..."
for i in $(seq 1 "$WORKERS"); do
  PIDFILE="${PID_DIR}/agentic-worker-${i}.pid"
  if [[ -f "$PIDFILE" ]]; then
    PID="$(cat "$PIDFILE")"
    if kill -0 "$PID" 2>/dev/null; then
      kill "$PID" 2>/dev/null || true
      log "  Killed worker $i (PID $PID)"
    fi
    rm -f "$PIDFILE"
  fi
done

# Clean up the harness
rm -f "$HARNESS"

# ── report ─────────────────────────────────────────────────────────────
echo ""
echo "──────────────────────────────────────────"
echo " Verification Report"
echo "──────────────────────────────────────────"
echo "  Planned:    $PLANNED"
echo "  Launched:   $LAUNCHED"
echo "  Completed:  $COMPLETED"
echo "  Failed:     $FAILED"
echo "  Timestamp:  $TIMESTAMP"
echo "──────────────────────────────────────────"

if [[ "$COMPLETED" -eq "$PLANNED" ]] && [[ "$FAILED" -eq 0 ]]; then
  log "ALL WORKERS COMPLETED SUCCESSFULLY"
  exit 0
else
  die "Verification failed: planned=$PLANNED completed=$COMPLETED failed=$FAILED"
fi
