#!/usr/bin/env bash
# verify_proxy.sh — Authenticated proxy verification
# Tests each configured model tier against the live proxy endpoint.
# Supports FCC (port 8080, default) and routatic-proxy (port 3456).
set -euo pipefail

PROXY_HOST="${PROXY_HOST:-127.0.0.1}"
PROXY_PORT="${PROXY_PORT:-8080}"
PROXY_URL="http://${PROXY_HOST}:${PROXY_PORT}"
AUTH_TOKEN="${ANTHROPIC_AUTH_TOKEN:-freecc}"
TIMEOUT_SEC=30
NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Detect proxy type from port for display
case "$PROXY_PORT" in
    3456) PROXY_TYPE="routatic-proxy" ;;
    8080) PROXY_TYPE="fcc-proxy" ;;
    *)    PROXY_TYPE="unknown" ;;
esac

declare -A TIERS=(
    ["deep"]="claude-3-opus"
    ["main"]="claude-3-7-sonnet"
    ["fast"]="claude-3-5-haiku"
)

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
PASS=0; FAIL=0

check() {
    local label="$1" url="$2" expected="$3"
    local code=$(curl -s -o /tmp/vp_resp.txt -w "%{http_code}" --max-time "$TIMEOUT_SEC" "$url")
    if [ "$code" = "$expected" ]; then
        echo -e "  ${GREEN}PASS${NC} $label (HTTP $code)"
        PASS=$((PASS + 1))
    else
        echo -e "  ${RED}FAIL${NC} $label (expected $expected, got $code)"
        FAIL=$((FAIL + 1))
    fi
}

echo "============================================================"
echo " PROXY VERIFICATION  |  $NOW"
echo " Type    : $PROXY_TYPE"
echo " Endpoint: $PROXY_URL"
echo " Auth:     x-api-key (${AUTH_TOKEN:0:3}...)"
echo "============================================================"

echo; echo "── 1. Health ──"
check "/health" "$PROXY_URL/health" "200"

echo; echo "── 2. Tier Tests ──"
for TIER in deep main fast; do
    MODEL="${TIERS[$TIER]}"
    START=$(date +%s%3N)
    HTTP=$(curl -s -o /tmp/vp_tier.txt -w "%{http_code}" --max-time "$TIMEOUT_SEC" \
        -H "Content-Type: application/json" -H "x-api-key: $AUTH_TOKEN" \
        -H "anthropic-version: 2023-06-01" \
        -d "{\"model\":\"$MODEL\",\"max_tokens\":10,\"messages\":[{\"role\":\"user\",\"content\":\"Say OK\"}]}" \
        "$PROXY_URL/v1/messages")
    END=$(date +%s%3N)
    LAT=$((END - START))
    if [ "$HTTP" = "200" ]; then
        BACKEND=$(python3 -c "import json; d=json.load(open('/tmp/vp_tier.txt')); print(d.get('model','?'))" 2>/dev/null || echo "?")
        echo -e "  ${GREEN}PASS${NC} tier=$TIER alias=$MODEL backend=$BACKEND latency=${LAT}ms"
        PASS=$((PASS + 1))
    else
        echo -e "  ${RED}FAIL${NC} tier=$TIER alias=$MODEL HTTP=$HTTP"
        FAIL=$((FAIL + 1))
    fi
done

echo; echo "── 3. Invalid Auth ──"
HTTP=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 \
    -H "Content-Type: application/json" -H "x-api-key: bad-token-xyz" \
    -H "anthropic-version: 2023-06-01" \
    -d '{"model":"claude-3-5-haiku","max_tokens":5,"messages":[{"role":"user","content":"Hi"}]}' \
    "$PROXY_URL/v1/messages")
if [ "$HTTP" = "401" ] || [ "$HTTP" = "403" ]; then
    echo -e "  ${GREEN}PASS${NC} Invalid auth rejected (HTTP $HTTP)"
    PASS=$((PASS + 1))
else
    echo -e "  ${RED}FAIL${NC} Invalid auth returned $HTTP (expected 401/403)"
    FAIL=$((FAIL + 1))
fi

echo; echo "── 4. Unavailable Model ──"
HTTP=$(curl -s -o /dev/null -w "%{http_code}" --max-time 15 \
    -H "Content-Type: application/json" -H "x-api-key: $AUTH_TOKEN" \
    -H "anthropic-version: 2023-06-01" \
    -d '{"model":"no-such-model-zzz","max_tokens":5,"messages":[{"role":"user","content":"Hi"}]}' \
    "$PROXY_URL/v1/messages")
if [ "$HTTP" != "200" ]; then
    echo -e "  ${GREEN}PASS${NC} Unknown model rejected (HTTP $HTTP)"
    PASS=$((PASS + 1))
else
    echo -e "  ${YELLOW}WARN${NC} Unknown model returned 200 (backend may ignore model name)"
fi

echo; echo "============================================================"
echo " RESULT: $PASS passed, $FAIL failed  |  $NOW"
if [ "$FAIL" -gt 0 ]; then echo " STATUS: FAILED"; exit 1; else echo " STATUS: SUCCESS"; fi
