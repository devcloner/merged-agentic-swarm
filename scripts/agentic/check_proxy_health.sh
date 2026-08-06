#!/usr/bin/env bash
set -euo pipefail

# ── check_proxy_health.sh ─────────────────────────────────────────────
# Health-check the Claude-Shaped Key Pool Proxy (systemd unit claude-proxy,
# port 8089). If /health is unreachable or non-200, restart the unit once and
# log the event. Exit 0 when healthy, 1 when a restart was issued/failed.
#
# Intended to run from cron every 2 minutes (see idempotent install note in
# the comment below). Safe to re-run — a healthy proxy does nothing.
#
# Logs to: /tmp/claude-proxy-health.log
# ────────────────────────────────────────────────────────────────────────

readonly HEALTH_URL="http://127.0.0.1:8089/health"
readonly TIMEOUT_SEC="${HEALTH_TIMEOUT_SEC:-5}"
readonly LOG_FILE="/tmp/claude-proxy-health.log"
readonly SERVICE_NAME="claude-proxy"

log() {
    printf '%s %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >> "$LOG_FILE"
}

# ── Probe health ──────────────────────────────────────────────────────
http_code=$(curl -sS -o /dev/null -w '%{http_code}' \
    --connect-timeout "$TIMEOUT_SEC" --max-time "$TIMEOUT_SEC" \
    "$HEALTH_URL" 2>/dev/null) || http_code="000"

if [[ "$http_code" == "200" ]]; then
    exit 0
fi

# ── Unhealthy: restart once ───────────────────────────────────────────
log "health check failed (HTTP $http_code) — restarting ${SERVICE_NAME}"

if ! sudo -n systemctl restart "$SERVICE_NAME" 2>/dev/null; then
    log "restart failed (non-interactive sudo unavailable or unit error) — manual action required"
    exit 1
fi

# Confirm the unit comes back before declaring success.
sleep 3
retry_code=$(curl -sS -o /dev/null -w '%{http_code}' \
    --connect-timeout "$TIMEOUT_SEC" --max-time "$TIMEOUT_SEC" \
    "$HEALTH_URL" 2>/dev/null) || retry_code="000"

if [[ "$retry_code" == "200" ]]; then
    log "restart succeeded — proxy healthy again"
    exit 0
else
    log "restart issued but proxy still unhealthy (HTTP $retry_code)"
    exit 1
fi

# Cron install (idempotent — re-running this block is a no-op):
#   crontab -l | grep -q 'check_proxy_health.sh' \
#     || ( crontab -l; echo '*/2 * * * * /home/ubuntu/merged-agentic-swarm/scripts/agentic/check_proxy_health.sh' ) \
#     | crontab -
