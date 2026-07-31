#!/usr/bin/env bash
# =============================================================================
# Master Smoke Workflow — Merged Agentic Swarm OS
# =============================================================================
# This is the MAIN operator command. It runs the complete smoke-test pipeline
# across all subsystems and produces a machine-readable results file.
#
# Usage:
#   ./scripts/agentic/run_smoke_workflow.sh
#   ./scripts/agentic/run_smoke_workflow.sh --skip non-critical
#   ./scripts/agentic/run_smoke_workflow.sh --only proxy,spine
#
# Exit codes:
#   0 — all critical steps passed
#   1 — one or more critical steps failed
#   2 — pre-flight check failed (missing scripts, config, etc.)
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
RESULTS_FILE="$REPO_ROOT/config/runtime/smoke-test-results.json"
TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
SUMMARY_ONLY=false
SKIP_PATTERN=""
ONLY_PATTERN=""

# ---------------------------------------------------------------------------
# Colour helpers
# ---------------------------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Colour

pass()  { echo -e "  ${GREEN}${BOLD}PASS${NC} $*"; }
fail()  { echo -e "  ${RED}${BOLD}FAIL${NC} $*"; }
warn()  { echo -e "  ${YELLOW}${BOLD}WARN${NC} $*"; }
info()  { echo -e "  ${CYAN}INFO${NC}  $*"; }
step_header() {
    echo ""
    echo -e "${BOLD}━━━ STEP $1/$2: $3 ━━━${NC}"
}

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------
while [[ $# -gt 0 ]]; do
    case "$1" in
        --skip)
            SKIP_PATTERN="${2:-}"
            shift 2
            ;;
        --only)
            ONLY_PATTERN="${2:-}"
            shift 2
            ;;
        --summary-only)
            SUMMARY_ONLY=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [--skip <pattern>] [--only <pattern>] [--summary-only]"
            echo ""
            echo "  --skip <pattern>     Skip steps matching pattern (comma-separated)"
            echo "  --only <pattern>     Only run steps matching pattern (comma-separated)"
            echo "  --summary-only       Print summary table only (no step output)"
            echo ""
            echo "  Known step names: discover, proxy, spine, worker1, worker2,"
            echo "                    learning, durable, report"
            exit 0
            ;;
        *)
            echo "Unknown argument: $1"
            exit 2
            ;;
    esac
done

# ---------------------------------------------------------------------------
# Step definitions — ordered array of descriptors
# ---------------------------------------------------------------------------
# Each entry: "step_key|critical|description|script_with_args"
STEPS=(
    "discover|critical|Discover environment|$SCRIPT_DIR/discover_environment.sh"
    "proxy|critical|Verify proxy (all tiers)|$SCRIPT_DIR/verify_proxy.sh --tier all"
    "spine|critical|Start and verify task spine|$SCRIPT_DIR/start_task_spine.sh && $SCRIPT_DIR/verify_task_spine.sh"
    "worker1|critical|Start and verify worker runtime (1 worker)|$SCRIPT_DIR/start_worker_runtime.sh --workers 1 && $SCRIPT_DIR/verify_worker_runtime.sh --workers 1"
    "worker2|non_critical|Verify worker runtime (2 workers)|$SCRIPT_DIR/verify_worker_runtime.sh --workers 2"
    "learning|non_critical|Run learning loop test|$SCRIPT_DIR/run_learning_loop_test.sh"
    "durable|non_critical|Load durable agents|$SCRIPT_DIR/load_durable_agents.sh"
    "report|non_critical|Generate progress report|$SCRIPT_DIR/generate_progress_report.sh"
)

TOTAL_STEPS=${#STEPS[@]}

# ---------------------------------------------------------------------------
# Trackers
# ---------------------------------------------------------------------------
passed_steps=()
failed_steps=()
skipped_steps=()
step_results_json=""

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
should_run_step() {
    local key="$1"

    # --only filter
    if [[ -n "$ONLY_PATTERN" ]]; then
        local IFS=','
        local found=false
        for pat in $ONLY_PATTERN; do
            [[ "$key" == "$pat" ]] && found=true && break
        done
        $found || return 1
    fi

    # --skip filter
    if [[ -n "$SKIP_PATTERN" ]]; then
        local IFS=','
        for pat in $SKIP_PATTERN; do
            [[ "$key" == "$pat" ]] && return 1
        done
    fi

    return 0
}

is_critical_step() {
    local key="$1"
    case "$key" in
        discover|proxy|spine|worker1) return 0 ;;
        *) return 1 ;;
    esac
}

# ---------------------------------------------------------------------------
# Pre-flight checks
# ---------------------------------------------------------------------------
preflight() {
    echo -e "${BOLD}=== Merged Agentic Swarm — Smoke Workflow ===${NC}"
    echo "Started: $TIMESTAMP"
    echo "Repo root: $REPO_ROOT"
    echo ""

    # Ensure results directory exists
    mkdir -p "$(dirname "$RESULTS_FILE")"

    # Ensure all referenced scripts exist (warn, don't fail, for sub-scripts)
    local missing=0
    for entry in "${STEPS[@]}"; do
        local key critical desc cmd
        IFS='|' read -r key critical desc cmd <<< "$entry"
        # For compound commands, check the first script only
        local first_script="${cmd%% *}"
        if [[ "$first_script" == "$SCRIPT_DIR"/* ]]; then
            if [[ ! -x "$first_script" ]]; then
                warn "Script not found or not executable: $first_script (step: $key)"
                missing=1
            fi
        fi
    done

    if [[ $missing -eq 1 ]]; then
        warn "Some sub-scripts are missing. Those steps will produce FAIL results."
        warn "This is expected on first setup — create the sub-scripts first."
    fi

    echo ""
}

# ---------------------------------------------------------------------------
# Execute one step
# ---------------------------------------------------------------------------
run_step() {
    local step_num="$1"
    local key="$2"
    local critical="$3"
    local description="$4"
    local cmd="$5"

    step_header "$step_num" "$TOTAL_STEPS" "$description"

    if ! should_run_step "$key"; then
        warn "SKIPPED (filtered)"
        skipped_steps+=("$key")
        step_results_json+="$(printf '{"step":"%s","status":"skipped","critical":%s},"' \
            "$key" "$(is_critical_step "$key" && echo true || echo false)")"
        return 0
    fi

    local start_ts
    start_ts="$(date +%s)"

    # Run the step — capture stdout/stderr but also tee so operator sees output
    local exit_code=0
    local log_file="/tmp/smoke-step-${key}.log"

    if [[ "$SUMMARY_ONLY" == true ]]; then
        bash -c "$cmd" > "$log_file" 2>&1 || exit_code=$?
    else
        bash -c "$cmd" 2>&1 | tee "$log_file" || exit_code=$?
    fi

    local end_ts
    end_ts="$(date +%s)"
    local duration=$((end_ts - start_ts))

    if [[ $exit_code -eq 0 ]]; then
        pass "$description (${duration}s)"
        passed_steps+=("$key")
        step_results_json+="$(printf '{"step":"%s","status":"passed","critical":%s,"duration_sec":%d},' \
            "$key" "$(is_critical_step "$key" && echo true || echo false)" "$duration")"
    else
        fail "$description (${duration}s) — exit code: $exit_code"
        failed_steps+=("$key")
        step_results_json+="$(printf '{"step":"%s","status":"failed","critical":%s,"duration_sec":%d,"exit_code":%d},' \
            "$key" "$(is_critical_step "$key" && echo true || echo false)" "$duration" "$exit_code")"
        info "See full log: $log_file"
    fi
}

# ---------------------------------------------------------------------------
# Print summary table
# ---------------------------------------------------------------------------
print_summary() {
    echo ""
    echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}                    SMOKE TEST SUMMARY                         ${NC}"
    echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
    echo ""

    # Summary counts
    local total_run=$(( ${#passed_steps[@]} + ${#failed_steps[@]} ))
    local total_passed=${#passed_steps[@]}
    local total_failed=${#failed_steps[@]}
    local total_skipped=${#skipped_steps[@]}

    # Count critical failures
    local critical_failed=0
    for key in "${failed_steps[@]}"; do
        if is_critical_step "$key"; then
            critical_failed=$((critical_failed + 1))
        fi
    done

    printf "  %-30s %s\n" "Total steps:"        "$TOTAL_STEPS"
    printf "  %-30s %s\n" "Passed:"             "$total_passed"
    printf "  %-30s %s\n" "Failed:"             "$total_failed"
    printf "  %-30s %s\n" "Skipped:"            "$total_skipped"
    printf "  %-30s %s\n" "Critical failures:"  "$critical_failed"
    echo ""

    # Per-step table
    printf "  %-4s %-12s %-10s %-35s\n" "#" "KEY" "RESULT" "DESCRIPTION"
    printf "  %-4s %-12s %-10s %-35s\n" "---" "------------" "----------" "-----------------------------------"
    local i=1
    for entry in "${STEPS[@]}"; do
        local key critical desc cmd
        IFS='|' read -r key critical desc cmd <<< "$entry"

        local result="SKIPPED"
        for pk in "${passed_steps[@]}"; do [[ "$pk" == "$key" ]] && result="PASS" && break; done
        for fk in "${failed_steps[@]}"; do [[ "$fk" == "$key" ]] && result="FAIL" && break; done

        local colour=""
        case "$result" in
            PASS)    colour="$GREEN" ;;
            FAIL)    colour="$RED" ;;
            SKIPPED) colour="$YELLOW" ;;
        esac
        printf "  %-4s ${colour}%-12s %-10s${NC} %-35s\n" \
            "$i" "$key" "$result" "$desc"
        i=$((i + 1))
    done
    echo ""

    # Verdict
    if [[ $critical_failed -eq 0 ]]; then
        echo -e "  ${GREEN}${BOLD}VERDICT: ALL CRITICAL STEPS PASSED${NC}"
    else
        echo -e "  ${RED}${BOLD}VERDICT: $critical_failed CRITICAL STEP(S) FAILED${NC}"
    fi
    echo ""

    # Next command hint
    if [[ $critical_failed -eq 0 ]]; then
        echo -e "  Next: ${BOLD}./scripts/agentic/generate_progress_report.sh${NC}"
        echo -e "        ${BOLD}python3 tools/agentic_cli.py run${NC} (full orchestrator)"
    else
        echo -e "  Next: ${BOLD}cat /tmp/smoke-step-<key>.log${NC}   (inspect failures)"
        echo -e "        ${BOLD}./scripts/agentic/run_smoke_workflow.sh --only <step>${NC} (retry single step)"
    fi
    echo ""
    echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
}

# ---------------------------------------------------------------------------
# Write machine-readable results
# ---------------------------------------------------------------------------
write_results_json() {
    local end_ts
    end_ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

    # Build step results array (strip trailing comma)
    local steps_json="[${step_results_json%,}]"

    # Determine overall verdict
    local critical_failed=0
    for key in "${failed_steps[@]}"; do
        is_critical_step "$key" && critical_failed=$((critical_failed + 1))
    done

    local verdict="pass"
    [[ $critical_failed -gt 0 ]] && verdict="fail"

    cat > "$RESULTS_FILE" << JSONEOF
{
  "workflow": "smoke-test",
  "version": "1.0.0",
  "started_at": "$TIMESTAMP",
  "completed_at": "$end_ts",
  "verdict": "$verdict",
  "counts": {
    "total": $TOTAL_STEPS,
    "passed": ${#passed_steps[@]},
    "failed": ${#failed_steps[@]},
    "skipped": ${#skipped_steps[@]},
    "critical_failed": $critical_failed
  },
  "passed": $(printf '%s\n' "${passed_steps[@]}" | jq -R . | jq -s .),
  "failed": $(printf '%s\n' "${failed_steps[@]}" | jq -R . | jq -s .),
  "skipped": $(printf '%s\n' "${skipped_steps[@]}" | jq -R . | jq -s .),
  "steps": $steps_json,
  "results_file": "$RESULTS_FILE"
}
JSONEOF
    echo ""
    info "Machine-readable results written to: $RESULTS_FILE"
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
main() {
    preflight

    local i=1
    for entry in "${STEPS[@]}"; do
        local key critical desc cmd
        IFS='|' read -r key critical desc cmd <<< "$entry"
        run_step "$i" "$key" "$critical" "$desc" "$cmd"
        i=$((i + 1))
    done

    print_summary
    write_results_json

    # Final exit code
    local critical_failed=0
    for key in "${failed_steps[@]}"; do
        is_critical_step "$key" && critical_failed=$((critical_failed + 1))
    done
    [[ $critical_failed -eq 0 ]] && exit 0 || exit 1
}

main
