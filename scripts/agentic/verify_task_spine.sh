#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────
# verify_task_spine.sh — End-to-end smoke test for the task spine.
#
# Creates a task, claims it, completes it with evidence, verifies
# persistence across a re-read, then cleans up.  All-or-nothing:
# exits 0 only when every step passes.
# ──────────────────────────────────────────────────────────────────────
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ADAPTER="$ROOT/services/task_spine_adapter.py"
LOCAL_STATE="${TASK_SPINE_STATE:-$HOME/.taskmaster/tasks/task_spine.json}"

# Colours
GREEN='\033[0;32m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

PASS=0
FAIL=0

banner()  { echo ""; echo -e "${CYAN}━━━ $* ━━━${NC}"; }
step_ok()   { PASS=$((PASS + 1)); echo -e "  ${GREEN}[PASS]${NC} $*"; }
step_fail() { FAIL=$((FAIL + 1)); echo -e "  ${RED}[FAIL]${NC} $*"; }

die() {
    echo ""
    echo -e "${RED}*** VERIFICATION ABORTED ***${NC}"
    echo "  $*"
    exit 2
}

# ── Sanity check ─────────────────────────────────────────────────────
banner "Pre-flight"
if [[ ! -f "$ADAPTER" ]]; then
    die "Task spine adapter not found at ${ADAPTER}"
fi
step_ok "Adapter file exists: ${ADAPTER}"

# Ensure state directory exists
mkdir -p "$(dirname "$LOCAL_STATE")"

# ── Helper: call adapter method via Python ───────────────────────────
# Returns the raw JSON response from the adapter (prints to stdout).
adapter_call() {
    local method="$1"
    shift
    local args=""
    for arg in "$@"; do
        if [[ -n "$args" ]]; then
            args="${args}, "
        fi
        args="${args}${arg}"
    done
    python3 -c "
import json, sys
sys.path.insert(0, '${ROOT}')
from services.task_spine_adapter import TaskSpineStore
a = TaskSpineStore('${LOCAL_STATE}')
result = a.${method}(${args})
print(json.dumps(result, indent=2))
"
}

# ── Helper: extract a value from the JSON response ───────────────────
# Usage:  val "$JSON" ".task.id"  or  val "$JSON" ".task.status"
val() {
    local json="$1"; local path="$2"
    echo "$json" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d${path})" 2>/dev/null || echo ""
}

# ── 1. Initialise the spine ──────────────────────────────────────────
banner "Step 0 — Initialise spine"
INIT_JSON=$(adapter_call "init") || die "Adapter init raised an error."
if echo "$INIT_JSON" | python3 -c "import json,sys; d=json.load(sys.stdin); exit(0 if d.get('ok') else 1)"; then
    step_ok "Spine initialised at ${LOCAL_STATE}"
else
    step_fail "Spine initialisation returned unexpected response."
fi

# ── 2. Create a test task ────────────────────────────────────────────
banner "Step 1 — Create test task"

CREATE_JSON=$(adapter_call "create" \
    "'verify-smoke-test'" \
    "'Auto-generated verification task — safe to delete'" \
    "'P1'") || die "Adapter create raised an error."

TASK_ID=$(val "$CREATE_JSON" "['task']['id']")
CREATE_OK=$(val "$CREATE_JSON" "['ok']")

if [[ "${CREATE_OK}" == "True" && -n "${TASK_ID:-}" ]]; then
    step_ok "Task created with ID: ${TASK_ID}"
else
    step_fail "Task creation failed. Response: $(echo "$CREATE_JSON" | head -5)"
fi

# ── 3. Inspect the newly created task ────────────────────────────────
banner "Step 2 — Inspect created task"

INSPECT_JSON=$(adapter_call "inspect" "'${TASK_ID}'") || die "Adapter inspect raised an error."

INSPECT_STATUS=$(val "$INSPECT_JSON" "['task']['status']")
INSPECT_TITLE=$(val "$INSPECT_JSON" "['task']['title']")

if [[ "${INSPECT_STATUS}" == "pending" ]]; then
    step_ok "Task status is 'pending'."
else
    step_fail "Expected status 'pending', got '${INSPECT_STATUS}'."
fi

if [[ "${INSPECT_TITLE}" == "verify-smoke-test" ]]; then
    step_ok "Task title matches."
else
    step_fail "Expected title 'verify-smoke-test', got '${INSPECT_TITLE}'."
fi

# ── 4. Claim the task ────────────────────────────────────────────────
banner "Step 3 — Claim task"

CLAIM_JSON=$(adapter_call "claim" "'${TASK_ID}'" "'verify-worker-01'") || die "Adapter claim raised an error."

CLAIM_STATUS=$(val "$CLAIM_JSON" "['task']['status']")
CLAIM_WORKER=$(val "$CLAIM_JSON" "['task']['worker_id']")

if [[ "${CLAIM_STATUS}" == "in_progress" ]]; then
    step_ok "Task status moved to 'in_progress'."
else
    step_fail "Expected status 'in_progress', got '${CLAIM_STATUS}'."
fi

if [[ "${CLAIM_WORKER}" == "verify-worker-01" ]]; then
    step_ok "Worker assigned correctly."
else
    step_fail "Expected worker 'verify-worker-01', got '${CLAIM_WORKER}'."
fi

# ── 5. Complete the task with evidence ───────────────────────────────
banner "Step 4 — Complete task with evidence"

# complete() takes evidence as a dict
COMPLETE_JSON=$(adapter_call "complete" "'${TASK_ID}'" "{'summary':'Smoke test passed all checks.','verdict':'pass','timestamp':'$(date -u +%Y-%m-%dT%H:%M:%SZ)'}") || die "Adapter complete raised an error."

COMPLETE_STATUS=$(val "$COMPLETE_JSON" "['task']['status']")

if [[ "${COMPLETE_STATUS}" == "completed" ]]; then
    step_ok "Task status moved to 'completed'."
else
    step_fail "Expected status 'completed', got '${COMPLETE_STATUS}'."
fi

# ── 6. Verify persistence — re-read from a fresh adapter instance ───
banner "Step 5 — Verify persistence (fresh load)"

PERSIST_JSON=$(python3 -c "
import json, sys
sys.path.insert(0, '${ROOT}')
from services.task_spine_adapter import TaskSpineStore
a2 = TaskSpineStore('${LOCAL_STATE}')
t = a2.inspect('${TASK_ID}')
print(json.dumps(t, indent=2))
") || die "Persistence re-read raised an error."

PERSIST_STATUS=$(val "$PERSIST_JSON" "['task']['status']")
PERSIST_WORKER=$(val "$PERSIST_JSON" "['task']['worker_id']")

if [[ "${PERSIST_STATUS}" == "completed" ]]; then
    step_ok "Persisted status is 'completed'."
else
    step_fail "Persistence check: expected 'completed', got '${PERSIST_STATUS}'."
fi

if [[ "${PERSIST_WORKER}" == "verify-worker-01" ]]; then
    step_ok "Persisted worker_id is correct."
else
    step_fail "Persistence check: expected worker 'verify-worker-01', got '${PERSIST_WORKER}'."
fi

# ── 7. List tasks to verify it appears ───────────────────────────────
banner "Step 6 — List completed tasks"

LIST_JSON=$(adapter_call "list_tasks" "'completed'") || die "Adapter list_tasks raised an error."
LIST_COUNT=$(echo "$LIST_JSON" | python3 -c "import json,sys; d=json.load(sys.stdin); tasks=d.get('tasks',[]); print(len(tasks))")

if [[ "${LIST_COUNT}" -ge 1 ]]; then
    step_ok "Completed task list contains ${LIST_COUNT} task(s), including ${TASK_ID}."
else
    step_fail "Completed task list returned ${LIST_COUNT} tasks (expected >=1)."
fi

# ── Summary ──────────────────────────────────────────────────────────
banner "Verification Summary"
TOTAL=$((PASS + FAIL))
echo -e "  Checks passed : ${GREEN}${PASS}${NC} / ${TOTAL}"
if [[ "${FAIL}" -gt 0 ]]; then
    echo -e "  Checks failed : ${RED}${FAIL}${NC} / ${TOTAL}"
fi

if [[ "${FAIL}" -eq 0 ]]; then
    echo ""
    echo -e "  ${GREEN}All verification steps passed. Task spine is operational.${NC}"
    exit 0
else
    echo ""
    echo -e "  ${RED}Some verification steps FAILED. Review output above.${NC}"
    exit 1
fi
