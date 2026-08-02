#!/usr/bin/env bash
set -euo pipefail

# ── start_proxy.sh ───────────────────────────────────────────────────
# Check whether a proxy (FCC on 8080 or routatic-proxy on 3456) is running.
# Idempotent — exits 0 when already running, 1 when not running.
#
# Usage:
#   scripts/agentic/start_proxy.sh [--help]
#   scripts/agentic/start_proxy.sh [--routatic|--fcc]
# ──────────────────────────────────────────────────────────────────────

readonly FCC_PORT=8080
readonly FCC_PROCESS_NAME="fcc-server"
readonly ROUTATIC_PORT=3456
readonly ROUTATIC_PROCESS_NAME="routatic-proxy"

PROXY_TYPE="both"

# ── Usage ────────────────────────────────────────────────────────────
usage() {
    cat <<EOF
Usage: $(basename "$0") [--help] [--routatic|--fcc]

Check whether a proxy is running on the configured port.
If running: prints PID, port, and status, then exits 0.
If not running: prints instructions and exits 1.

Options:
  --help       Show this help and exit.
  --fcc        Check only FCC proxy (port $FCC_PORT).
  --routatic   Check only routatic-proxy (port $ROUTATIC_PORT).
EOF
}

if [[ $# -gt 0 ]]; then
    case "$1" in
        --help)
            usage
            exit 0
            ;;
        --fcc)
            PROXY_TYPE="fcc"
            shift
            ;;
        --routatic)
            PROXY_TYPE="routatic"
            shift
            ;;
        *)
            echo "ERROR: Unknown option: $1" >&2
            usage >&2
            exit 2
            ;;
    esac
fi

# ── Check for a proxy on a given port ──────────────────────────────
check_proxy() {
    local PORT="$1"
    local PROCESS_NAME="$2"
    local LABEL="$3"

    local ss_output
    ss_output=$(ss -tlnp "sport = :$PORT" 2>/dev/null) || true

    if [[ -z "$ss_output" ]]; then
        return 1
    fi

    local pid
    pid=$(echo "$ss_output" | grep -oP 'pid=\K[0-9]+' | head -n 1) || true

    if [[ -z "$pid" ]]; then
        echo ""
        echo "=== $LABEL Status ==="
        echo "  Port   : $PORT"
        echo "  Status : LISTENING (PID unknown — process may be owned by another user)"
        echo "  Process: $PROCESS_NAME (assumed)"
        echo ""
        echo "Proxy appears to be running but PID could not be read."
        echo "Run with sudo if you need the PID:  sudo ss -tlnp \"sport = :$PORT\""
        echo ""
        return 0
    fi

    local proc_name
    proc_name=$(ps -p "$pid" -o comm= 2>/dev/null || echo "unknown")

    echo ""
    echo "=== $LABEL Status ==="
    echo "  PID     : $pid"
    echo "  Port    : $PORT"
    echo "  Process : $proc_name"
    echo "  Status  : RUNNING"
    echo ""
    echo "$LABEL is already running. No action needed."
    echo ""

    return 0
}

# ── Main ──────────────────────────────────────────────────────────────
case "$PROXY_TYPE" in
    fcc)
        if check_proxy "$FCC_PORT" "$FCC_PROCESS_NAME" "FCC Proxy"; then
            exit 0
        fi
        echo ""
        echo "=== FCC Proxy Status ==="
        echo "  Port    : $FCC_PORT"
        echo "  Process : $FCC_PROCESS_NAME"
        echo "  Status  : NOT RUNNING"
        echo ""
        echo "fcc-server not running. It must be started manually or by system service."
        exit 1
        ;;
    routatic)
        if check_proxy "$ROUTATIC_PORT" "$ROUTATIC_PROCESS_NAME" "Routatic Proxy"; then
            exit 0
        fi
        echo ""
        echo "=== Routatic Proxy Status ==="
        echo "  Port    : $ROUTATIC_PORT"
        echo "  Process : $ROUTATIC_PROCESS_NAME"
        echo "  Status  : NOT RUNNING"
        echo ""
        echo "routatic-proxy not running. Start it with:"
        echo "  source ~/.local/bin/start-routatic-proxy.sh"
        exit 1
        ;;
    both)
        FCC_RUNNING=false
        ROUTATIC_RUNNING=false

        if check_proxy "$FCC_PORT" "$FCC_PROCESS_NAME" "FCC Proxy" >/dev/null 2>&1; then
            FCC_RUNNING=true
        fi
        if check_proxy "$ROUTATIC_PORT" "$ROUTATIC_PROCESS_NAME" "Routatic Proxy" >/dev/null 2>&1; then
            ROUTATIC_RUNNING=true
        fi

        if $FCC_RUNNING && $ROUTATIC_RUNNING; then
            echo "Both proxies are running (FCC:$FCC_PORT, Routatic:$ROUTATIC_PORT)."
            exit 0
        fi

        echo ""
        echo "=== Proxy Status ==="
        if ! $FCC_RUNNING; then
            echo "  FCC Proxy (port $FCC_PORT): NOT RUNNING"
        fi
        if ! $ROUTATIC_RUNNING; then
            echo "  Routatic Proxy (port $ROUTATIC_PORT): NOT RUNNING"
        fi
        echo ""

        if ! $FCC_RUNNING; then
            echo "fcc-server not running. It must be started manually or by system service."
        fi
        if ! $ROUTATIC_RUNNING; then
            echo "routatic-proxy not running. Start it with:"
            echo "  source ~/.local/bin/start-routatic-proxy.sh"
        fi
        exit 1
        ;;
esac
