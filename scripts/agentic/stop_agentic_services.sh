#!/usr/bin/env bash
# =============================================================================
# Stop Agentic Services — Merged Agentic Swarm OS
# =============================================================================
# Gracefully stops all worker processes tracked by our PID files under
# /tmp/agentic-worker-*.pid. Does NOT touch fcc-server or other system
# services — only processes we spawned and recorded.
#
# Usage:
#   ./scripts/agentic/stop_agentic_services.sh
#   ./scripts/agentic/stop_agentic_services.sh --force   (skip SIGTERM, straight to SIGKILL)
# =============================================================================

set -euo pipefail

PID_DIR="/tmp"
PID_GLOB="agentic-worker-*.pid"
GRACE_SECONDS=5
FORCE=false

# -------------------------------------------------------------------------
# Argument parsing
# -------------------------------------------------------------------------
while [[ $# -gt 0 ]]; do
    case "$1" in
        --force|-f)
            FORCE=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [--force | -f]"
            echo ""
            echo "  Stops all agentic worker processes tracked by $PID_DIR/$PID_GLOB"
            echo ""
            echo "  --force, -f    Skip SIGTERM, send SIGKILL immediately"
            echo ""
            echo "  Protected processes (never touched):"
            echo "    - fcc-server (port 8080)"
            echo "    - routatic-proxy (port 3456)"
            echo "    - sub-agent-mcp (port 8000)"
            echo "    - docker-proxy"
            echo "    - Any PID not in our PID files"
            exit 0
            ;;
        *)
            echo "Unknown argument: $1"
            exit 2
            ;;
    esac
done

# -------------------------------------------------------------------------
# Protected process check — never kill these
# -------------------------------------------------------------------------
PROTECTED_COMMANDS=("fcc-server" "routatic-proxy" "sub-agent-mcp" "docker-proxy" "dockerd" "systemd" "sshd")

is_protected() {
    local pid="$1"
    local cmdline=""
    cmdline="$(cat "/proc/$pid/cmdline" 2>/dev/null | tr '\0' ' ' || echo "")"

    for protected in "${PROTECTED_COMMANDS[@]}"; do
        if echo "$cmdline" | grep -qi "$protected"; then
            return 0  # protected
        fi
    done
    return 1  # not protected
}

# -------------------------------------------------------------------------
# Kill a single process gracefully
# -------------------------------------------------------------------------
kill_worker() {
    local pid="$1"
    local pidfile="$2"

    # Validate PID is a positive integer
    if ! [[ "$pid" =~ ^[0-9]+$ ]]; then
        echo "  WARN: Invalid PID '$pid' in $pidfile — removing stale file"
        rm -f "$pidfile"
        return 1
    fi

    # Check if process exists
    if ! kill -0 "$pid" 2>/dev/null; then
        echo "  INFO: PID $pid is not running — removing stale PID file"
        rm -f "$pidfile"
        return 0
    fi

    # Protection check
    if is_protected "$pid"; then
        echo "  PROTECTED: PID $pid is a system service — will NOT kill"
        rm -f "$pidfile"
        echo "  Removed PID file $pidfile (process was not ours)"
        return 2
    fi

    # Get process name for display
    local proc_name
    proc_name="$(ps -p "$pid" -o comm= 2>/dev/null || echo "unknown")"

    if [[ "$FORCE" == true ]]; then
        echo "  FORCE: Sending SIGKILL to PID $pid ($proc_name)..."
        kill -9 "$pid" 2>/dev/null || true
        rm -f "$pidfile"
        echo "  Stopped: PID $pid ($proc_name)"
        return 0
    fi

    # Graceful shutdown: SIGTERM
    echo "  Sending SIGTERM to PID $pid ($proc_name)..."
    kill -TERM "$pid" 2>/dev/null || true

    # Wait up to GRACE_SECONDS for the process to exit
    local waited=0
    while kill -0 "$pid" 2>/dev/null && [[ $waited -lt $GRACE_SECONDS ]]; do
        sleep 1
        waited=$((waited + 1))
    done

    # If still running, SIGKILL
    if kill -0 "$pid" 2>/dev/null; then
        echo "  Process did not exit after ${GRACE_SECONDS}s — sending SIGKILL..."
        kill -9 "$pid" 2>/dev/null || true
        sleep 0.5
        if kill -0 "$pid" 2>/dev/null; then
            echo "  ERROR: Could not kill PID $pid ($proc_name)"
            return 1
        fi
    fi

    rm -f "$pidfile"
    echo "  Stopped: PID $pid ($proc_name) after ${waited}s"
    return 0
}

# -------------------------------------------------------------------------
# Main
# -------------------------------------------------------------------------
main() {
    echo ""
    echo "=== Stop Agentic Services ==="
    echo ""

    local pid_files
    pid_files=$(find "$PID_DIR" -maxdepth 1 -name "$PID_GLOB" -type f 2>/dev/null || true)

    if [[ -z "$pid_files" ]]; then
        echo "No PID files found matching $PID_DIR/$PID_GLOB"
        echo "No agentic worker processes to stop."
        echo ""
        exit 0
    fi

    local total=0
    local stopped=0
    local already_dead=0
    local protected_count=0
    local failed=0

    while IFS= read -r pidfile; do
        total=$((total + 1))
        local pid
        pid="$(cat "$pidfile" 2>/dev/null || echo "")"

        if [[ -z "$pid" ]]; then
            echo "WARN: Empty PID file: $pidfile — removing"
            rm -f "$pidfile"
            already_dead=$((already_dead + 1))
            continue
        fi

        local result
        kill_worker "$pid" "$pidfile"
        result=$?

        case $result in
            0) stopped=$((stopped + 1)) ;;
            1) failed=$((failed + 1)) ;;
            2) protected_count=$((protected_count + 1)) ;;
        esac
    done <<< "$pid_files"

    # Summary
    echo ""
    echo "────────────────────────────────────────────"
    printf "  %-30s %s\n" "PID files found:"      "$total"
    printf "  %-30s %s\n" "Workers stopped:"     "$stopped"
    printf "  %-30s %s\n" "Already dead:"        "$already_dead"
    printf "  %-30s %s\n" "Protected (skipped):" "$protected_count"
    printf "  %-30s %s\n" "Failed to stop:"      "$failed"
    echo "────────────────────────────────────────────"
    echo ""

    # Check for leftover PID files
    local remaining
    remaining=$(find "$PID_DIR" -maxdepth 1 -name "$PID_GLOB" -type f 2>/dev/null | wc -l)
    if [[ "$remaining" -gt 0 ]]; then
        echo "WARNING: $remaining PID file(s) remain — processes may still be running."
        echo "  Re-run with --force or inspect manually:"
        find "$PID_DIR" -maxdepth 1 -name "$PID_GLOB" -type f -exec echo "    {}" \;
    else
        echo "All agentic worker PID files removed. Services stopped."
    fi
    echo ""

    # Verify we didn't touch fcc-server
    if pgrep -f fcc-server > /dev/null 2>&1; then
        echo "OK: fcc-server is still running (untouched)."
    fi
}

main
