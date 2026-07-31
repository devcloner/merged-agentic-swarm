#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────
# start_task_spine.sh — Boot the task spine subsystem.
#
# Prefers the real Task Master AI CLI when available and properly
# configured (valid API key).  Falls back to a local JSON-file-based
# task spine adapter otherwise.
# ──────────────────────────────────────────────────────────────────────
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TM_CONFIG="${TM_CONFIG:-$HOME/.taskmaster/config.json}"
TM_STATE_DIR="${TM_STATE_DIR:-$HOME/.taskmaster/tasks}"
LOCAL_STATE="${LOCAL_STATE:-$TM_STATE_DIR/task_spine.json}"

# Colours
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

banner()  { echo -e "${CYAN}=== $* ===${NC}"; }
ok()      { echo -e "  ${GREEN}[PASS]${NC} $*"; }
warn()    { echo -e "  ${YELLOW}[WARN]${NC} $*"; }
fail()    { echo -e "  ${RED}[FAIL]${NC} $*"; }
info()    { echo -e "  ${CYAN}[INFO]${NC} $*"; }

# ── 1. Detect Task Master CLI ────────────────────────────────────────
banner "Task Spine Startup"

TM_BIN=""
TM_ACTIVE=false
SPINE_TYPE=""

if command -v task-master &>/dev/null; then
    TM_BIN="$(command -v task-master)"
elif [[ -x "$HOME/.local/bin/task-master" ]]; then
    TM_BIN="$HOME/.local/bin/task-master"
elif [[ -x "/usr/local/bin/task-master" ]]; then
    TM_BIN="/usr/local/bin/task-master"
fi

if [[ -n "${TM_BIN:-}" ]]; then
    TM_VER="$("$TM_BIN" --version 2>/dev/null || echo "unknown")"
    info "Task Master CLI found: ${TM_BIN} (${TM_VER})"
else
    warn "Task Master CLI not found on PATH or in known locations."
    TM_ACTIVE=false
fi

# ── 2. Inspect Task Master configuration ─────────────────────────────
API_KEY_VALID=false
if [[ -n "${TM_BIN:-}" ]] && [[ -f "$TM_CONFIG" ]]; then
    # Extract the main provider
    TM_PROVIDER=$(python3 -c "
import json, sys
try:
    with open('$TM_CONFIG') as f:
        cfg = json.load(f)
    print(cfg.get('models',{}).get('main',{}).get('provider','unknown'))
except Exception:
    print('parse_error')
" 2>/dev/null)
    info "Task Master config provider: ${TM_PROVIDER:-unknown}"

    # Check whether the relevant API key is a real key or a placeholder.
    # We treat keys matching these patterns as non-operational:
    #   - starts with "free"   (e.g. freecc…)
    #   - starts with "placeholder"
    #   - equals "YOUR_KEY_HERE"
    #   - is empty / unset
    case "${TM_PROVIDER:-unknown}" in
        anthropic)
            KEY_VAR="ANTHROPIC_API_KEY"
            ;;
        openai)
            KEY_VAR="OPENAI_API_KEY"
            ;;
        groq)
            KEY_VAR="GROQ_API_KEY"
            ;;
        openrouter)
            KEY_VAR="OPENROUTER_API_KEY"
            ;;
        gemini|google)
            KEY_VAR="GEMINI_API_KEY"
            ;;
        perplexity)
            KEY_VAR="PERPLEXITY_API_KEY"
            ;;
        *)
            KEY_VAR=""
            ;;
    esac

    if [[ -n "${KEY_VAR:-}" ]]; then
        KEY_VAL="${!KEY_VAR:-}"
        if [[ -z "${KEY_VAL:-}" ]]; then
            warn "${KEY_VAR} is not set in the environment."
        elif [[ "${KEY_VAL}" =~ ^free ]]; then
            warn "${KEY_VAR} looks like a free/placeholder key (starts with 'free')."
        elif [[ "${KEY_VAL}" =~ ^placeholder ]] || [[ "${KEY_VAL}" == "YOUR_KEY_HERE" ]]; then
            warn "${KEY_VAR} is a known placeholder string."
        elif [[ "${#KEY_VAL}" -gt 20 ]]; then
            KEY_MASK="${KEY_VAL:0:8}…${KEY_VAL:(-4)}"
            ok "API key present (${KEY_MASK})."
            API_KEY_VALID=true
        else
            warn "${KEY_VAL} is too short to be a real API key."
        fi
    fi
else
    if [[ -z "${TM_BIN:-}" ]]; then
        warn "Skipping config check — no Task Master CLI."
    elif [[ ! -f "$TM_CONFIG" ]]; then
        warn "Task Master config not found at ${TM_CONFIG}."
    fi
fi

# Also check ANTHROPIC_API_KEY directly since the config hardcodes it
if ! $API_KEY_VALID; then
    ANTHROPIC_KEY="${ANTHROPIC_API_KEY:-}"
    if [[ -n "${ANTHROPIC_KEY:-}" ]] && [[ "${ANTHROPIC_KEY}" =~ ^free ]]; then
        warn "ANTHROPIC_API_KEY appears to be a free/non-operational key — Task Master LLM calls may fail."
    fi
fi

# ── 3. Decide spine type ─────────────────────────────────────────────
if $API_KEY_VALID && [[ -n "${TM_BIN:-}" ]]; then
    SPINE_TYPE="TASK_MASTER"
    TM_ACTIVE=true
    ok "Using TASK_MASTER spine (real CLI + valid API key)."
else
    SPINE_TYPE="LOCAL_FALLBACK"
    warn "Activating LOCAL FALLBACK task spine."
fi

# ── 4. Initialise local fallback (always — it's harmless and ensures
#       the file exists even if we later switch to Task Master) ───────
mkdir -p "$TM_STATE_DIR"

if python3 "$ROOT/services/task_spine_adapter.py" --init 2>/dev/null; then
    ok "Local task spine adapter initialised at ${LOCAL_STATE}"
else
    # Try absolute import-free path as a fallback
    if python3 -c "
import json, os, sys
path = '${LOCAL_STATE}'
os.makedirs(os.path.dirname(path), exist_ok=True)
if not os.path.exists(path):
    with open(path, 'w') as f:
        json.dump({'tasks': {}, 'updated_at': 'init'}, f)
    print('Bootstrap created:', path)
else:
    print('Already exists:', path)
" 2>/dev/null; then
        ok "Local task spine bootstrapped via inline fallback."
    else
        fail "Could not initialise local task spine at ${LOCAL_STATE}."
        exit 1
    fi
fi

# ── 5. Report ────────────────────────────────────────────────────────
echo ""
banner "Task Spine Status"
echo -e "  Active spine type : ${GREEN}${SPINE_TYPE}${NC}"
echo -e "  State file        : ${LOCAL_STATE}"
if [[ -n "${TM_BIN:-}" ]]; then
    echo -e "  Task Master binary: ${TM_BIN}"
    echo -e "  Task Master config: ${TM_CONFIG}"
fi

# Export for downstream scripts
export TASK_SPINE_TYPE="$SPINE_TYPE"
export TASK_SPINE_STATE="$LOCAL_STATE"

exit 0
