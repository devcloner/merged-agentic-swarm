#!/usr/bin/env bash
# =============================================================================
# run_smoke_workflow.sh — Safe end-to-end smoke verification
# =============================================================================
# Runs the complete smoke pipeline for the Merged Agentic Swarm OS:
#   1. discover  — print environment discovery (hostname, python, open ports)
#   2. config    — validate ANTHROPIC_BASE_URL / ANTHROPIC_AUTH_TOKEN
#   3. proxy     — run scripts/agentic/verify_proxy.sh (all tiers)
#   4. spine     — task spine: create / claim / complete a test task
#   5. worker1   — worker runtime: 1-worker dry run via native_subagent
#   6. learning  — learning loop cold-path promotion test
#   7. report    — generate summary report + results JSON
#
# Safe by design: read-only verification, append-only test records, and a
# single in-process LLM call (native_subagent). No destructive operations.
#
# Usage:
#   ./scripts/agentic/run_smoke_workflow.sh
#   ./scripts/agentic/run_smoke_workflow.sh --only proxy,spine
#   ./scripts/agentic/run_smoke_workflow.sh --skip learning
#
# Exit codes:
#   0 — all steps passed
#   1 — one or more steps failed
#   2 — pre-flight failure (missing sub-script or required tool)
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
export REPO_ROOT  # consumed by the inline worker harness
RESULTS_FILE="$REPO_ROOT/config/runtime/smoke-test-results.json"
PYTHON_BIN="${PYTHON_BIN:-python3}"
START_TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Operate from the repo root regardless of the caller's cwd.
cd "$REPO_ROOT"

# ── Colour + timestamp helpers ──────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

stamp() { date -u '+%Y-%m-%d %H:%M:%SZ'; }
pass()  { echo -e "  $(stamp) ${GREEN}${BOLD}PASS${NC} $*"; }
fail()  { echo -e "  $(stamp) ${RED}${BOLD}FAIL${NC} $*"; }
warn()  { echo -e "  $(stamp) ${YELLOW}${BOLD}WARN${NC} $*"; }
info()  { echo -e "  $(stamp) ${CYAN}INFO${NC}  $*"; }

# ── Argument parsing ────────────────────────────────────────────────────────
SKIP_PATTERN=""
ONLY_PATTERN=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --skip)  SKIP_PATTERN="${2:-}"; shift 2 ;;
    --only)  ONLY_PATTERN="${2:-}"; shift 2 ;;
    --help|-h)
      cat <<EOF
Usage: $0 [--skip <pattern>] [--only <pattern>]

  --skip <pattern>   Skip steps matching pattern (comma-separated)
  --only <pattern>   Only run steps matching pattern (comma-separated)

  Steps: discover, config, proxy, spine, worker1, learning, report
EOF
      exit 0
      ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done

# ── Step definitions — key|description (function = step_<key>) ─────────────
STEPS=(
  "discover|Environment discovery (hostname, python, open ports)"
  "config|Config validation (ANTHROPIC_BASE_URL, ANTHROPIC_AUTH_TOKEN)"
  "proxy|Proxy verification (verify_proxy.sh)"
  "spine|Task spine (create/claim/complete test task)"
  "worker1|Worker runtime (1-worker native_subagent dry run)"
  "learning|Learning loop promotion"
  "report|Summary report"
)
TOTAL_STEPS=${#STEPS[@]}

# ── Trackers ───────────────────────────────────────────────────────────────
passed_steps=()
failed_steps=()
skipped_steps=()
step_results_json=""

# ── Filtering ──────────────────────────────────────────────────────────────
should_run_step() {
  local key="$1"
  if [[ -n "$ONLY_PATTERN" ]]; then
    local IFS=',' found=false pat
    for pat in $ONLY_PATTERN; do
      [[ "$key" == "$pat" ]] && found=true && break
    done
    $found || return 1
  fi
  if [[ -n "$SKIP_PATTERN" ]]; then
    local IFS=',' pat
    for pat in $SKIP_PATTERN; do
      [[ "$key" == "$pat" ]] && return 1
    done
  fi
  return 0
}

# ── Pre-flight ─────────────────────────────────────────────────────────────
preflight() {
  echo -e "${BOLD}=== Merged Agentic Swarm — Smoke Workflow ===${NC}"
  echo "Started: $START_TS"
  echo "Repo root: $REPO_ROOT"
  echo "Results: $RESULTS_FILE"
  echo ""
  local missing=0 script
  for script in verify_proxy.sh verify_task_spine.sh run_learning_loop_test.sh; do
    if [[ ! -x "$SCRIPT_DIR/$script" ]]; then
      fail "Required sub-script missing: scripts/agentic/$script"
      missing=1
    fi
  done
  if [[ $missing -eq 1 ]]; then
    echo ""
    fail "Pre-flight: required sub-scripts missing. Aborting."
    exit 2
  fi
}

# ── Run one step, print PASS/FAIL ──────────────────────────────────────────
run_step() {
  local num="$1" key="$2" desc="$3" fn="$4"
  echo ""
  echo -e "${BOLD}━━━ STEP $num/$TOTAL_STEPS: $desc ━━━${NC}   [$(stamp)]"

  if ! should_run_step "$key"; then
    warn "SKIPPED (filtered)"
    skipped_steps+=("$key")
    step_results_json+="$(printf '{"step":"%s","status":"skipped","critical":true},' "$key")"
    return 0
  fi

  local start_s end_s duration exit_code=0
  start_s="$(date +%s)"
  "$fn" || exit_code=$?
  end_s="$(date +%s)"
  duration=$((end_s - start_s))

  if [[ $exit_code -eq 0 ]]; then
    pass "$desc (${duration}s)"
    passed_steps+=("$key")
    step_results_json+="$(printf '{"step":"%s","status":"passed","critical":true,"duration_sec":%d},' "$key" "$duration")"
  else
    fail "$desc (${duration}s) — exit code $exit_code"
    failed_steps+=("$key")
    step_results_json+="$(printf '{"step":"%s","status":"failed","critical":true,"duration_sec":%d,"exit_code":%d},' "$key" "$duration" "$exit_code")"
  fi

  # The summary report is generated after the report step is recorded so the
  # table and results JSON reflect its own outcome.
  if [[ "$key" == "report" ]]; then
    print_summary
    if [[ $exit_code -eq 0 ]]; then
      if write_results_json; then
        info "Machine-readable results written to: $RESULTS_FILE"
      else
        warn "failed to write $RESULTS_FILE"
      fi
      refresh_progress_report
    fi
  fi
  return 0
}

# ── 1. Environment discovery ───────────────────────────────────────────────
step_discover() {
  local hostname_ok=1 python_ok=1 hname="" pyver="" ports=""
  hname="$(hostname 2>/dev/null)" || { hostname_ok=0; hname="unknown"; }
  pyver="$("$PYTHON_BIN" --version 2>&1)" || { python_ok=0; pyver="not-found"; }

  info "hostname : ${hname}"
  info "python   : ${pyver}"
  info "os       : $(uname -srm 2>/dev/null || echo unknown)"
  if command -v ss >/dev/null 2>&1; then
    ports="$(ss -tlnp 2>/dev/null | awk 'NR>1 {n=split($4,a,":"); print a[n]}' | sort -n -u | tr '\n' ' ')"
  fi
  info "open ports: ${ports:-<none found / ss unavailable>}"
  [[ $hostname_ok -eq 1 && $python_ok -eq 1 ]]
}

# ── 2. Config validation ───────────────────────────────────────────────────
step_config() {
  local base_url="${ANTHROPIC_BASE_URL:-}"
  local auth_token="${ANTHROPIC_AUTH_TOKEN:-}"

  [[ -z "$base_url" ]] && fail "ANTHROPIC_BASE_URL is unset or empty"
  [[ -z "$auth_token" ]] && fail "ANTHROPIC_AUTH_TOKEN is unset or empty"
  [[ -z "$base_url" || -z "$auth_token" ]] && return 1

  local redacted=""
  if [[ "${#auth_token}" -gt 6 ]]; then
    redacted="${auth_token:0:3}…${auth_token: -3}"
  else
    redacted="******"
  fi
  info "ANTHROPIC_BASE_URL   = $base_url"
  info "ANTHROPIC_AUTH_TOKEN = $redacted (length ${#auth_token})"
  return 0
}

# ── 3. Proxy verification ──────────────────────────────────────────────────
step_proxy() {
  "$SCRIPT_DIR/verify_proxy.sh"
}

# ── 4. Task spine: create / claim / complete ───────────────────────────────
step_spine() {
  "$SCRIPT_DIR/verify_task_spine.sh"
}

# ── 5. Worker runtime: 1-worker dry run via native_subagent ────────────────
step_worker1() {
  timeout 120 "$PYTHON_BIN" - <<'PY'
import json
import os
import sys

sys.path.insert(0, os.path.join(os.environ["REPO_ROOT"], "src"))

from merged_agentic_swarm.models.agent_models import AgentSpec, WorkerRole
from merged_agentic_swarm.services.worker_runtime_adapter import get_runtime_adapter

adapter = get_runtime_adapter(mode="native_subagent")
spec = AgentSpec(
    id="smoke-worker-01",
    name="Smoke Worker 1",
    role=WorkerRole.CORE_ENGINEER,
    agent_type="swarm_worker",
    system_prompt="You are a verification test worker. Answer very briefly.",
    model_alias="claude-3-7-sonnet",
)
task = (
    "Write exactly one line of Python that defines a function named "
    "fixture_worker_1 returning the integer 1."
)

print(f"[worker1] adapter_mode={adapter.mode}")
print(f"[worker1] dispatching {spec.id} ...", flush=True)
result = adapter.launch_worker(spec, task)

summary = {k: v for k, v in result.items() if k != "evidence"}
print(f"[worker1] result: {json.dumps(summary, default=str)}", flush=True)

required = ["run_id", "task_id", "worker_id", "role", "start_time", "end_time", "status", "evidence"]
missing = [f for f in required if f not in result or result[f] is None]
status = result.get("status", "MISSING")
ok_status = status in ("completed", "partial (simulated)")
all_fields = not missing

print(
    f"[worker1] status={status} "
    f"required_fields={'ok' if all_fields else 'MISSING: ' + ','.join(missing)}",
    flush=True,
)

if all_fields and ok_status:
    print("[worker1] dry run PASSED")
    sys.exit(0)
else:
    print("[worker1] dry run FAILED")
    sys.exit(1)
PY
}

# ── 6. Learning loop promotion ─────────────────────────────────────────────
step_learning() {
  "$SCRIPT_DIR/run_learning_loop_test.sh"
}

# ── Summary report ─────────────────────────────────────────────────────────
print_summary() {
  echo ""
  echo -e "${BOLD}════════════════════════════════════════════════════════════════${NC}"
  echo -e "${BOLD}                    SMOKE TEST SUMMARY                          ${NC}"
  echo -e "${BOLD}════════════════════════════════════════════════════════════════${NC}"
  echo ""
  local total=$(( ${#passed_steps[@]} + ${#failed_steps[@]} + ${#skipped_steps[@]} ))
  printf "  %-30s %s\n" "Total steps:" "${total}"
  printf "  %-30s %s\n" "Passed:"      "${#passed_steps[@]}"
  printf "  %-30s %s\n" "Failed:"      "${#failed_steps[@]}"
  printf "  %-30s %s\n" "Skipped:"     "${#skipped_steps[@]}"
  echo ""
  printf "  %-4s %-12s %-10s %-48s\n" "#" "KEY" "RESULT" "DESCRIPTION"
  printf "  %-4s %-12s %-10s %-48s\n" "---" "------------" "----------" "------------------------------------------------"
  local i=1 entry key desc result colour pk fk
  for entry in "${STEPS[@]}"; do
    IFS='|' read -r key desc <<< "$entry"
    result="SKIPPED"
    for pk in "${passed_steps[@]}"; do [[ "$pk" == "$key" ]] && result="PASS" && break; done
    for fk in "${failed_steps[@]}"; do [[ "$fk" == "$key" ]] && result="FAIL" && break; done
    colour="$YELLOW"
    [[ "$result" == "PASS" ]] && colour="$GREEN"
    [[ "$result" == "FAIL" ]] && colour="$RED"
    printf "  %-4s ${colour}%-12s %-10s${NC} %-48s\n" "$i" "$key" "$result" "$desc"
    i=$((i + 1))
  done
  echo ""
  if [[ ${#failed_steps[@]} -eq 0 ]]; then
    echo -e "  ${GREEN}${BOLD}VERDICT: ALL STEPS PASSED${NC}"
  else
    echo -e "  ${RED}${BOLD}VERDICT: ${#failed_steps[@]} STEP(S) FAILED: ${failed_steps[*]}${NC}"
  fi
  echo ""
}

# ── Machine-readable results ───────────────────────────────────────────────
json_array() {
  local -n arr="$1"
  if [[ ${#arr[@]} -eq 0 ]]; then
    echo "[]"
  else
    printf '%s\n' "${arr[@]}" | jq -R . | jq -s .
  fi
}

write_results_json() {
  local end_ts verdict total steps_json
  end_ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  steps_json="[${step_results_json%,}]"
  verdict="pass"
  [[ ${#failed_steps[@]} -gt 0 ]] && verdict="fail"
  total=$(( ${#passed_steps[@]} + ${#failed_steps[@]} + ${#skipped_steps[@]} ))

  mkdir -p "$(dirname "$RESULTS_FILE")"
  cat > "$RESULTS_FILE" <<JSONEOF
{
  "workflow": "smoke-test",
  "version": "2.0.0",
  "started_at": "$START_TS",
  "completed_at": "$end_ts",
  "verdict": "$verdict",
  "counts": {
    "total": $total,
    "passed": ${#passed_steps[@]},
    "failed": ${#failed_steps[@]},
    "skipped": ${#skipped_steps[@]},
    "critical_failed": ${#failed_steps[@]}
  },
  "passed": $(json_array passed_steps),
  "failed": $(json_array failed_steps),
  "skipped": $(json_array skipped_steps),
  "steps": $steps_json,
  "results_file": "$RESULTS_FILE"
}
JSONEOF
}

# ── 7. Summary report step ─────────────────────────────────────────────────
step_report() {
  # Lightweight check: the report target must be writable. The summary table,
  # results JSON, and progress report refresh run in run_step after this step
  # is recorded so its own outcome is included.
  local dir
  dir="$(dirname "$RESULTS_FILE")"
  if ! mkdir -p "$dir" 2>/dev/null; then
    fail "report directory not writable: $dir"
    return 1
  fi
  if [[ ! -w "$dir" ]]; then
    fail "report directory not writable: $dir"
    return 1
  fi
  info "report target writable: $RESULTS_FILE"
  return 0
}

# Best-effort refresh of the ecosystem progress report (never fails the step).
refresh_progress_report() {
  if [[ -x "$SCRIPT_DIR/generate_progress_report.sh" ]]; then
    if "$SCRIPT_DIR/generate_progress_report.sh" >/tmp/smoke-progress-report.log 2>&1; then
      info "Progress report regenerated: $REPO_ROOT/docs/agentic/PROGRESS_REPORT.md"
    else
      warn "generate_progress_report.sh failed — see /tmp/smoke-progress-report.log"
    fi
  fi
}

# ── Main ───────────────────────────────────────────────────────────────────
main() {
  preflight

  local i=1 entry key desc
  for entry in "${STEPS[@]}"; do
    IFS='|' read -r key desc <<< "$entry"
    run_step "$i" "$key" "$desc" "step_${key}"
    i=$((i + 1))
  done

  echo ""
  echo -e "${BOLD}Workflow finished: $(stamp)${NC}"
  if [[ ${#failed_steps[@]} -eq 0 ]]; then
    exit 0
  else
    exit 1
  fi
}

main
