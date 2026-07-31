#!/usr/bin/env bash
set -euo pipefail

# ── start_proxy.sh ───────────────────────────────────────────────────────────
# Check whether the FCC proxy (fcc-server) is running on port 8080.
# Idempotent — exits 0 when already running, 1 when not running.
#
# Usage:
#   scripts/agentic/start_proxy.sh [--help]
# ──────────────────────────────────────────────────────────────────────────────

readonly PORT=8080
readonly PROCESS_NAME="fcc-server"

# ── Usage ────────────────────────────────────────────────────────────────────
usage() {
    cat <<EOF
Usage: $(basename "$0") [--help]

Check whether the FCC proxy ($PROCESS_NAME) is running on port $PORT.
If running: prints PID, port, and status, then exits 0.
If not running: prints instructions and exits 1.

Options:
  --help    Show this help and exit.
EOF
}

if [[ $# -gt 0 ]]; then
    case "$1" in
        --help)
            usage
            exit 0
            ;;
        *)
            echo "ERROR: Unknown option: $1" >&2
            usage >&2
            exit 2
            ;;
    esac
fi

# ── Check for fcc-server on port 8080 ────────────────────────────────────────
check_proxy() {
    # ss -tlnp: show listening TCP sockets with process info.
    # Match port 8080 and optionally filter for the process name.
    local ss_output
    ss_output=$(ss -tlnp "sport = :$PORT" 2>/dev/null) || true

    if [[ -z "$ss_output" ]]; then
        return 1
    fi

    # Extract the PID from the ss output.
    # Typical ss -tlnp line:
    #   LISTEN 0 128 0.0.0.0:8080 0.0.0.0:* users:(("node",pid=12345,fd=18))
    local pid
    pid=$(echo "$ss_output" | grep -oP 'pid=\K[0-9]+' | head -n 1) || true

    if [[ -z "$pid" ]]; then
        # Something is listening but we could not extract a PID (maybe root-owned).
        echo ""
        echo "=== FCC Proxy Status ==="
        echo "  Port   : $PORT"
        echo "  Status : LISTENING (PID unknown — process may be owned by another user)"
        echo "  Process: $PROCESS_NAME (assumed)"
        echo ""
        echo "Proxy appears to be running but PID could not be read."
        echo "Run with sudo if you need the PID:  sudo ss -tlnp \"sport = :$PORT\""
        echo ""
        return 0
    fi

    # Confirm the process name matches (best-effort).
    local proc_name
    proc_name=$(ps -p "$pid" -o comm= 2>/dev/null || echo "unknown")

    echo ""
    echo "=== FCC Proxy Status ==="
    echo "  PID     : $pid"
    echo "  Port    : $PORT"
    echo "  Process : $proc_name"
    echo "  Status  : RUNNING"
    echo ""
    echo "FCC proxy is already running. No action needed."
    echo ""

    return 0
}

# ── Main ──────────────────────────────────────────────────────────────────────
if check_proxy; then
    exit 0
fi

# ── Not running — print status and instructions ──────────────────────────────
echo ""
echo "=== FCC Proxy Status ==="
echo "  Port    : $PORT"
echo "  Process : $PROCESS_NAME"
echo "  Status  : NOT RUNNING"
echo ""

echo "fcc-server not running. It must be started manually or by system service."
echo ""
echo "── Start instructions ─────────────────────────────────────────────────────"
echo ""

# Check common service managers
if command -v systemctl &>/dev/null; then
    echo "systemd (if installed as a system service):"
    echo "    sudo systemctl start fcc-server"
    echo "    sudo systemctl status fcc-server"
    echo ""
    echo "Enable at boot:"
    echo "    sudo systemctl enable fcc-server"
    echo ""
fi

# Check for PM2
if command -v pm2 &>/dev/null; then
    echo "PM2 (if managed via PM2):"
    echo "    pm2 start fcc-server"
    echo "    pm2 list"
    echo "    pm2 logs fcc-server"
    echo ""
fi

# Generic manual start
echo "Manual start (substitute with the actual binary/entrypoint):"
echo "    cd <project-root>"
echo "    nohup <fcc-server-binary> &>/var/log/fcc-server.log &"
echo ""

# Check for a Docker container
if command -v docker &>/dev/null; then
    echo "Docker (if containerised):"
    echo "    docker ps -a --filter name=fcc-server"
    echo "    docker start fcc-server"
    echo ""
fi

exit 1
