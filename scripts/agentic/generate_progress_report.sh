#!/usr/bin/env bash
# =============================================================================
# Progress Report Generator — Merged Agentic Swarm OS
# =============================================================================
# Collects all evidence from the smoke test run and all audit artifacts to
# produce a single authoritative progress document.
#
# Usage:
#   ./scripts/agentic/generate_progress_report.sh
#
# Output:
#   docs/agentic/PROGRESS_REPORT.md  (overwritten each run)
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
LOCAL_DATE="$(date '+%Y-%m-%d %H:%M:%S %Z')"

RESULTS_FILE="$REPO_ROOT/config/runtime/smoke-test-results.json"
AUDIT_DIR="$REPO_ROOT/docs/agentic/audit"
REGISTRY_DIR="$REPO_ROOT/docs/agentic/registry"
OUTPUT_FILE="$REPO_ROOT/docs/agentic/PROGRESS_REPORT.md"

TASKS_FILE="$REPO_ROOT/.taskmaster/tasks/tasks.json"
PROGRESS_LEDGER="$REPO_ROOT/.taskmaster/tasks/progress_ledger.json"
SPAWN_CHAIN="$REPO_ROOT/.taskmaster/tasks/spawn_chain_registry.json"
PROMOTED_IDS="$REPO_ROOT/.taskmaster/promoted_learning_ids.json"
KNOWLEDGE_CACHE="$REPO_ROOT/.opencode/knowledge_cache.json"
AGENTS_DIR="$REPO_ROOT/.claude/agents"

# -------------------------------------------------------------------------
# Helper: read a JSON field safely
# -------------------------------------------------------------------------
json_field() {
    local file="$1"
    local query="$2"
    local default="${3:-}"
    if [[ -f "$file" ]]; then
        jq -r "$query // \"$default\"" "$file" 2>/dev/null || echo "$default"
    else
        echo "$default"
    fi
}

# -------------------------------------------------------------------------
# Helper: count lines in a JSONL file
# -------------------------------------------------------------------------
count_jsonl() {
    local file="$1"
    if [[ -f "$file" ]]; then
        wc -l < "$file"
    else
        echo "0"
    fi
}

# -------------------------------------------------------------------------
# Helper: count files in a directory (or 0 if missing)
# -------------------------------------------------------------------------
count_files() {
    local dir="$1"
    if [[ -d "$dir" ]]; then
        find "$dir" -maxdepth 1 -type f | wc -l
    else
        echo "0"
    fi
}

# -------------------------------------------------------------------------
# Collect data from smoke-test-results.json
# -------------------------------------------------------------------------
collect_smoke_results() {
    if [[ -f "$RESULTS_FILE" ]]; then
        cat "$RESULTS_FILE"
    else
        echo '{"verdict":"unknown","counts":{"total":0,"passed":0,"failed":0,"skipped":0,"critical_failed":0},"passed":[],"failed":[],"skipped":[],"steps":[]}'
    fi
}

# -------------------------------------------------------------------------
# Determine proxy status from environment-facts.json
# -------------------------------------------------------------------------
proxy_status() {
    local env_file="$AUDIT_DIR/environment-facts.json"
    if [[ -f "$env_file" ]]; then
        local fcc_status
        fcc_status=$(json_field "$env_file" '.proxy.fcc_server.status' "UNKNOWN")
        local node_status
        node_status=$(json_field "$env_file" '.proxy.node_proxy.status' "UNKNOWN")

        if [[ "$fcc_status" == "VERIFIED_USED" ]]; then
            echo "USED — fcc-server port 8080 (${node_status:-UNKNOWN} node proxy on 8085)"
        else
            echo "NOT USED"
        fi
    else
        echo "UNKNOWN (no environment facts)"
    fi
}

# -------------------------------------------------------------------------
# Determine OpenCode status from environment-facts.json
# -------------------------------------------------------------------------
opencode_status() {
    local env_file="$AUDIT_DIR/environment-facts.json"
    if [[ -f "$env_file" ]]; then
        local status
        status=$(json_field "$env_file" '.opencode.status' "UNKNOWN")
        local workers
        workers=$(json_field "$env_file" '.opencode.worker_processes_running' "0")
        echo "$status (${workers:-0} workers running)"
    else
        echo "UNKNOWN"
    fi
}

# -------------------------------------------------------------------------
# Determine Task Master status from environment-facts.json
# -------------------------------------------------------------------------
taskmaster_status() {
    local env_file="$AUDIT_DIR/environment-facts.json"
    if [[ -f "$env_file" ]]; then
        local status
        status=$(json_field "$env_file" '.task_master.status' "UNKNOWN")
        echo "$status"
    else
        echo "UNKNOWN"
    fi
}

# -------------------------------------------------------------------------
# Determine if multi-provider fabric is wired
# -------------------------------------------------------------------------
fabric_status() {
    local working=0
    local dead=0
    local unknown=0
    local env_file="$AUDIT_DIR/environment-facts.json"

    if [[ -f "$env_file" ]]; then
        while IFS='=' read -r key val; do
            case "$val" in
                *WORKING*) working=$((working + 1)) ;;
                *DEAD*)    dead=$((dead + 1)) ;;
                *NO_KEY*)  dead=$((dead + 1)) ;;
            esac
        done < <(jq -r '.providers | to_entries[] | "\(.key)=\(.value.result)"' "$env_file" 2>/dev/null)
    fi
    echo "$working working / $dead unavailable"
}

# -------------------------------------------------------------------------
# Count durable agents
# -------------------------------------------------------------------------
durable_agent_count() {
    count_files "$AGENTS_DIR"
}

# -------------------------------------------------------------------------
# Count promoted learnings
# -------------------------------------------------------------------------
promoted_count() {
    if [[ -f "$PROMOTED_IDS" ]]; then
        jq '. | length' "$PROMOTED_IDS" 2>/dev/null || echo "0"
    else
        echo "0"
    fi
}

# -------------------------------------------------------------------------
# Phase and completion estimate
# -------------------------------------------------------------------------
phase_info() {
    # Read from tasks.json if it exists
    if [[ -f "$TASKS_FILE" ]]; then
        local total
        total=$(json_field "$TASKS_FILE" '.tasks | length' "0")
        local completed
        completed=$(jq '[.tasks[] | select(.status == "completed")] | length' "$TASKS_FILE" 2>/dev/null || echo "0")

        local pct=0
        if [[ "$total" -gt 0 ]]; then
            pct=$(( completed * 100 / total ))
        fi

        if [[ $completed -gt 0 ]] && [[ $completed -lt $total ]]; then
            echo "Phase 3 — Worker Pool Execution | ${pct}% complete ($completed/$total tasks)"
        elif [[ $completed -eq $total ]] && [[ $total -gt 0 ]]; then
            echo "Phase 5 — Complete | 100% complete ($total/$total tasks)"
        elif [[ -f "$RESULTS_FILE" ]]; then
            echo "Phase 2 — Verification & Integration | 25% complete (smoke test run)"
        else
            echo "Phase 0 — Baseline Audit | 5% complete (environment discovered)"
        fi
    else
        echo "Phase 0 — Pre-initialization | 0% complete"
    fi
}

# -------------------------------------------------------------------------
# Subsystem evidence table builder
# -------------------------------------------------------------------------
generate_evidence_table() {
    local smoke_json
    smoke_json=$(collect_smoke_results)

    local proxy_ok="NOT CHECKED"
    local spine_ok="NOT CHECKED"
    local worker1_ok="NOT CHECKED"
    local worker2_ok="NOT CHECKED"
    local learning_ok="NOT CHECKED"
    local durable_ok="NOT CHECKED"
    local discover_ok="NOT CHECKED"
    local report_ok="NOT CHECKED"

    while IFS= read -r step; do
        local key status
        key=$(echo "$step" | jq -r '.step // ""')
        status=$(echo "$step" | jq -r '.status // "unknown"')
        case "$key" in
            discover) discover_ok="$status" ;;
            proxy)    proxy_ok="$status" ;;
            spine)    spine_ok="$status" ;;
            worker1)  worker1_ok="$status" ;;
            worker2)  worker2_ok="$status" ;;
            learning) learning_ok="$status" ;;
            durable)  durable_ok="$status" ;;
            report)   report_ok="$status" ;;
        esac
    done < <(echo "$smoke_json" | jq -c '.steps[]?' 2>/dev/null || true)

    local icon_pass="OK"
    local icon_fail="FAIL"
    local icon_skip="SKIP"
    local icon_unk="--"

    status_icon() {
        case "$1" in
            passed)  echo "$icon_pass" ;;
            failed)  echo "$icon_fail" ;;
            skipped) echo "$icon_skip" ;;
            *)       echo "$icon_unk" ;;
        esac
    }

    echo "| Subsystem | Status | Detail |"
    echo "|-----------|--------|--------|"
    echo "| Environment Discovery | $(status_icon "$discover_ok") | $(proxy_status) |"
    echo "| Proxy (fcc + node) | $(status_icon "$proxy_ok") | $(proxy_status) |"
    echo "| Task Spine | $(status_icon "$spine_ok") | $(taskmaster_status) |"
    echo "| Worker Runtime (1 worker) | $(status_icon "$worker1_ok") | $(opencode_status) |"
    echo "| Worker Runtime (2 workers) | $(status_icon "$worker2_ok") | $(opencode_status) |"
    echo "| Learning Loop | $(status_icon "$learning_ok") | $(count_jsonl "$REGISTRY_DIR/knowledge.jsonl") records in registry |"
    echo "| Durable Agents | $(status_icon "$durable_ok") | $(durable_agent_count) agent specs |"
    echo "| Progress Report | $(status_icon "$report_ok") | Generated $LOCAL_DATE |"
    echo "| Multi-Provider Fabric | $(status_icon "") | $(fabric_status) |"
    echo "| Registries (knowledge/agents/chain) | $(status_icon "") | $(count_jsonl "$REGISTRY_DIR/knowledge.jsonl") / $(count_jsonl "$REGISTRY_DIR/agents.jsonl") / $(count_jsonl "$REGISTRY_DIR/chain.jsonl") entries |"
    echo "| Promoted Learnings | $(status_icon "") | $(promoted_count) promoted |"
}

# -------------------------------------------------------------------------
# Generate remaining risks
# -------------------------------------------------------------------------
remaining_risks() {
    echo "- No runtime enforcement of variable precedence (FR-01.8)"
    echo "- PRD checkboxes not yet reflecting reality (FR-02.5)"
    echo "- Duplicate learning records possible if promoted_learning_ids.json lost"
    echo "- Worker pool scaling beyond 2 workers untested in smoke"
    echo "- Cross-provider circuit-breaking not yet live-tested beyond opencode"
    echo "- Orchestrator re-run restarts from Step 0 (idempotent, but time-consuming)"
}

# -------------------------------------------------------------------------
# Next command hint
# -------------------------------------------------------------------------
next_command() {
    local smoke_json
    smoke_json=$(collect_smoke_results)
    local verdict
    verdict=$(echo "$smoke_json" | jq -r '.verdict // "unknown"')

    if [[ "$verdict" == "pass" ]]; then
        echo "python3 tools/agentic_cli.py run"
        echo "# Full orchestrator is safe to launch — all critical subsystems verified."
    else
        echo "./scripts/agentic/run_smoke_workflow.sh --only \$(cat $RESULTS_FILE | jq -r '.failed[]' | tr '\n' ',')"
        echo "# Re-run only the failed steps before proceeding to full orchestrator."
    fi
}

# -------------------------------------------------------------------------
# Main report generation
# -------------------------------------------------------------------------
generate_report() {
    mkdir -p "$(dirname "$OUTPUT_FILE")"

    cat > "$OUTPUT_FILE" << 'REPORT_HEADER'
# Merged Agentic Swarm OS — Progress Report

REPORT_HEADER

    cat >> "$OUTPUT_FILE" << REPORT_META
**Generated:** $LOCAL_DATE ($TIMESTAMP)
**Report version:** 1.0.0
**Repository:** $REPO_ROOT
**Branch:** $(cd "$REPO_ROOT" && git branch --show-current 2>/dev/null || echo "unknown")

---

## 1. Current Phase & Completion

$(phase_info)

---

## 2. Worker Pool Status

| Metric | Count |
|--------|-------|
| Planned workers (target) | 40 |
| Launched workers (configured) | $(json_field "$AUDIT_DIR/environment-facts.json" '.opencode.swarm_agents_configured' "0") |
| Running workers (live) | $(json_field "$AUDIT_DIR/environment-facts.json" '.opencode.worker_processes_running' "0") |
| Completed tasks | $(json_field "$TASKS_FILE" '[.tasks[] | select(.status == "completed")] | length' "0") |
| Total tasks | $(json_field "$TASKS_FILE" '.tasks | length' "0") |

---

## 3. Subsystem Status

- **OpenCode status:** $(opencode_status)
- **Task Master status:** $(taskmaster_status)
- **Proxy status:** $(proxy_status)
- **Selected endpoint:** $(json_field "$AUDIT_DIR/environment-facts.json" '.proxy.fcc_server.status // "UNKNOWN"' "UNKNOWN") (fcc-server:8080)

---

## 4. Checks Summary

| Result | Count |
|--------|-------|
| Completed | $(json_field "$RESULTS_FILE" '.counts.passed' "0") |
| Failed | $(json_field "$RESULTS_FILE" '.counts.failed' "0") |
| Blocked/Skipped | $(json_field "$RESULTS_FILE" '.counts.skipped' "0") |
| Critical failures | $(json_field "$RESULTS_FILE" '.counts.critical_failed' "0") |

**Failed steps:** $(json_field "$RESULTS_FILE" '.failed | join(", ")' "none")

---

## 5. Durable Agents

$(durable_agent_count) durable agent spec(s) in \`.claude/agents/\`:
$(if [[ -d "$AGENTS_DIR" ]]; then ls "$AGENTS_DIR" 2>/dev/null | sed 's/^/- /'; else echo "- (none)"; fi)

---

## 6. Learning Records

| Registry | Entries |
|----------|---------|
| knowledge.jsonl | $(count_jsonl "$REGISTRY_DIR/knowledge.jsonl") |
| agents.jsonl | $(count_jsonl "$REGISTRY_DIR/agents.jsonl") |
| chain.jsonl | $(count_jsonl "$REGISTRY_DIR/chain.jsonl") |
| Promoted learnings | $(promoted_count) |

---

## 7. Provider Fabric Status

$(fabric_status)

---

## 8. Final Evidence Table

$(generate_evidence_table)

---

## 9. Next Command

\`\`\`bash
$(next_command)
\`\`\`

---

## 10. Remaining Risks

$(remaining_risks)

---

## 11. Audit Trail

REPORT_META

    # Append audit files content summary
    if [[ -d "$AUDIT_DIR" ]]; then
        echo "Audit files in \`$AUDIT_DIR\`:" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        for f in "$AUDIT_DIR"/*; do
            if [[ -f "$f" ]]; then
                local fname
                fname=$(basename "$f")
                local fsize
                fsize=$(wc -c < "$f")
                local flines
                flines=$(wc -l < "$f")
                echo "- \`$fname\` ($fsize bytes, $flines lines)" >> "$OUTPUT_FILE"
            fi
        done
        echo "" >> "$OUTPUT_FILE"
    else
        echo "(No audit directory found)" >> "$OUTPUT_FILE"
    fi

    # Append smoke results JSON summary
    if [[ -f "$RESULTS_FILE" ]]; then
        echo "### Smoke Test Results (raw)" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        echo '```json' >> "$OUTPUT_FILE"
        jq '.' "$RESULTS_FILE" 2>/dev/null >> "$OUTPUT_FILE" || echo "(invalid JSON)" >> "$OUTPUT_FILE"
        echo '```' >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
    fi

    echo "Report generated: $OUTPUT_FILE"
}

# -------------------------------------------------------------------------
# Entry point
# -------------------------------------------------------------------------
generate_report
