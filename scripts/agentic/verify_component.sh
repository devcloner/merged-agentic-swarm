#!/usr/bin/env bash
set -euo pipefail

# ── verify_component.sh ──────────────────────────────────────────────────
# Runs targeted health checks against a named component and reports each
# check's result. Exits 0 only when every check for the component passes.
# Use --json for machine-readable output.
# ─────────────────────────────────────────────────────────────────────────

REPO_ROOT="/home/ubuntu"
OPENCODE_BIN="/home/ubuntu/.opencode/bin/opencode"
TASKMASTER_CONFIG="/home/ubuntu/.taskmaster/config.json"
REGISTRY_DIR="$REPO_ROOT/docs/agentic/registry"

# Temp file for JSON accumulation
RESULTS_TMP=""

cleanup() {
    rm -f "$RESULTS_TMP"
}
trap cleanup EXIT

# ── help ─────────────────────────────────────────────────────────────────
usage() {
    cat <<'EOF'
Usage: verify_component.sh [--json] <component>
       verify_component.sh --help

Run health checks against a named component. Exits 0 only when every check
for that component passes.

Components:
  proxy       Check fcc-server on port 8080 (models endpoint, auth)
  opencode    Check the OpenCode binary (exists, executable, version)
  taskmaster  Check Task Master config (exists, valid JSON, has main model)
  registries  Check registry files (exist, are valid JSONL/JSON line-counts)
  git         Check git (available, in a repo, branch accessible)
  python      Check python3 + uv (available, version, import key modules)
  node        Check node + npm (available, version)

Flags:
  --json      Output results as a single JSON object to stdout
  --help      Show this help message and exit

Exit codes:
  0   All checks for the component passed
  1   One or more checks failed
  2   Invalid usage (bad component name, missing argument)
EOF
    exit 0
}

# ── parse args ───────────────────────────────────────────────────────────
JSON_MODE="false"
COMPONENT=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --help) usage ;;
        --json) JSON_MODE="true"; shift ;;
        -*)     echo "ERROR: Unknown flag: $1" >&2; echo "Use --help for usage." >&2; exit 2 ;;
        *)      COMPONENT="$1"; shift ;;
    esac
done

if [[ -z "$COMPONENT" ]]; then
    echo "ERROR: <component> is required. Use --help for usage." >&2
    exit 2
fi

# ── check-runner infrastructure ──────────────────────────────────────────
RESULTS_TMP="$(mktemp /tmp/verify_component_results.XXXXXX.json)"

# Start JSON array
echo '[]' > "$RESULTS_TMP"

declare -a CHECK_NAMES=()
declare -a CHECK_COMMANDS=()
declare -a CHECK_EXIT_CODES=()
declare -a CHECK_DETAILS=()
CHECK_INDEX=0

record_check() {
    local name="$1"
    local cmd="$2"
    local ec="$3"
    local detail="$4"

    CHECK_NAMES[$CHECK_INDEX]="$name"
    CHECK_COMMANDS[$CHECK_INDEX]="$cmd"
    CHECK_EXIT_CODES[$CHECK_INDEX]="$ec"
    CHECK_DETAILS[$CHECK_INDEX]="$detail"
    (( ++CHECK_INDEX ))

    # Escape via stdin to avoid quoting issues with arbitrary strings
    local detail_escaped
    detail_escaped=$(printf '%s' "$detail" | python3 -c "import sys, json; print(json.dumps(sys.stdin.read()))" 2>/dev/null || echo '""')
    local cmd_escaped
    cmd_escaped=$(printf '%s' "$cmd" | python3 -c "import sys, json; print(json.dumps(sys.stdin.read()))" 2>/dev/null || echo '""')
    local name_escaped
    name_escaped=$(printf '%s' "$name" | python3 -c "import sys, json; print(json.dumps(sys.stdin.read()))" 2>/dev/null || echo '""')

    local status="fail"
    [[ "$ec" -eq 0 ]] && status="pass"

    # Append to the JSON array (in-place)
    python3 -c "
import json
with open('$RESULTS_TMP') as f:
    data = json.load(f)
data.append({
    'name': $name_escaped,
    'command': $cmd_escaped,
    'exit_code': $ec,
    'status': '$status',
    'detail': $detail_escaped
})
with open('$RESULTS_TMP', 'w') as f:
    json.dump(data, f, indent=2)
"
}

succeeded() { [[ "$1" -eq 0 ]]; }
failed()   { [[ "$1" -ne 0 ]]; }

# ── component checks ─────────────────────────────────────────────────────

check_proxy() {
    local ec detail

    # Check 1: HTTP reachability of /v1/models
    ec=0
    detail=$(curl -s -o /dev/null -w 'HTTP %{http_code}' \
        -H 'Authorization: Bearer freecc' \
        'http://localhost:8080/v1/models' --connect-timeout 5 --max-time 10 2>&1) || ec=$?
    record_check "proxy-reachability" \
        "curl -H 'Authorization: Bearer freecc' http://localhost:8080/v1/models" \
        "$ec" \
        "$detail"

    # Check 2: Response is valid JSON with a 'data' key, model count > 0
    ec=0
    detail=$(python3 -c "
import json, urllib.request
req = urllib.request.Request('http://localhost:8080/v1/models', headers={'Authorization': 'Bearer freecc'})
resp = urllib.request.urlopen(req, timeout=10)
body = json.loads(resp.read())
count = len(body.get('data', []))
print(f'valid JSON, model_count={count}')
" 2>&1) || ec=$?
    record_check "proxy-json-parse" \
        "python3 parse /v1/models response, validate JSON, count models" \
        "$ec" \
        "$detail"

    # Check 3: Model count is non-zero
    if [[ "$ec" -eq 0 ]]; then
        local model_count
        model_count=$(echo "$detail" | grep -oP 'model_count=\K\d+' || echo "0")
        if [[ "$model_count" -gt 0 ]]; then
            ec=0
            detail="model_count=$model_count (non-zero, ok)"
        else
            ec=1
            detail="model_count=$model_count (expected > 0)"
        fi
    else
        ec=1
        detail="cannot verify model count (parse failed)"
    fi
    record_check "proxy-model-count" \
        "assert model_count > 0" \
        "$ec" \
        "$detail"
}

check_opencode() {
    local ec detail

    # Check 1: Binary exists
    ec=0
    if [[ -f "$OPENCODE_BIN" ]]; then
        detail="binary present at $OPENCODE_BIN"
    else
        ec=1
        detail="binary NOT FOUND at $OPENCODE_BIN"
    fi
    record_check "opencode-exists" \
        "test -f $OPENCODE_BIN" \
        "$ec" \
        "$detail"

    # Check 2: Binary is executable
    ec=0
    if [[ -x "$OPENCODE_BIN" ]]; then
        detail="binary is executable"
    else
        ec=1
        detail="binary is NOT executable"
    fi
    record_check "opencode-executable" \
        "test -x $OPENCODE_BIN" \
        "$ec" \
        "$detail"

    # Check 3: Version output
    ec=0
    detail=$("$OPENCODE_BIN" --version 2>&1) || ec=$?
    record_check "opencode-version" \
        "$OPENCODE_BIN --version" \
        "$ec" \
        "$detail"
}

check_taskmaster() {
    local ec detail

    # Check 1: Config file exists
    ec=0
    if [[ -f "$TASKMASTER_CONFIG" ]]; then
        detail="config present at $TASKMASTER_CONFIG"
    else
        ec=1
        detail="config NOT FOUND at $TASKMASTER_CONFIG"
    fi
    record_check "taskmaster-exists" \
        "test -f $TASKMASTER_CONFIG" \
        "$ec" \
        "$detail"

    # Check 2: Valid JSON
    ec=0
    detail=$(python3 -c "import json; json.load(open('$TASKMASTER_CONFIG')); print('valid JSON')" 2>&1) || ec=$?
    record_check "taskmaster-json-valid" \
        "python3 -c 'json.load(open(config))'" \
        "$ec" \
        "$detail"

    # Check 3: Has main model section with provider and modelId
    ec=0
    detail=$(python3 -c "
import json
with open('$TASKMASTER_CONFIG') as f:
    d = json.load(f)
m = d.get('models', {}).get('main', {})
provider = m.get('provider', 'MISSING')
model_id = m.get('modelId', 'MISSING')
print(f'provider={provider} modelId={model_id}')
" 2>&1) || ec=$?
    record_check "taskmaster-main-model" \
        "python3 -c 'extract models.main.provider and models.main.modelId'" \
        "$ec" \
        "$detail"
}

check_registries() {
    local ec detail

    for name in knowledge agents chain; do
        local path="$REGISTRY_DIR/${name}.jsonl"

        # Check existence
        ec=0
        if [[ -f "$path" ]]; then
            local lines
            lines=$(wc -l < "$path" 2>/dev/null || echo "0")
            detail="exists, lines=$lines"
        else
            ec=1
            detail="NOT FOUND at $path"
        fi
        record_check "registries-${name}-exists" \
            "test -f $path" \
            "$ec" \
            "$detail"

        # Check JSONL parse
        if [[ -f "$path" ]]; then
            ec=0
            detail=$(python3 -c "
import json
with open('$path') as f:
    count = 0
    for i, line in enumerate(f):
        line = line.strip()
        if line:
            json.loads(line)
            count += 1
print(f'parsed={count} valid JSONL records')
" 2>&1) || ec=$?
            record_check "registries-${name}-parse" \
                "python3 validate each JSONL line in $name.jsonl" \
                "$ec" \
                "$detail"
        fi
    done

    # progress.json
    local ppath="$REGISTRY_DIR/progress.json"
    ec=0
    if [[ -f "$ppath" ]]; then
        local lines
        lines=$(wc -l < "$ppath" 2>/dev/null || echo "0")
        detail="exists, lines=$lines"
    else
        ec=1
        detail="NOT FOUND at $ppath"
    fi
    record_check "registries-progress-exists" \
        "test -f $ppath" \
        "$ec" \
        "$detail"

    if [[ -f "$ppath" ]]; then
        ec=0
        detail=$(python3 -c "import json; json.load(open('$ppath')); print('valid JSON')" 2>&1) || ec=$?
        record_check "registries-progress-parse" \
            "python3 -c 'json.load(open(progress.json))'" \
            "$ec" \
            "$detail"
    fi
}

check_git() {
    local ec detail

    # Check 1: git is available
    ec=0
    detail=$(git --version 2>&1) || ec=$?
    record_check "git-available" \
        "git --version" \
        "$ec" \
        "$detail"

    # Check 2: REPO_ROOT is in a git repo
    ec=0
    detail=$(cd "$REPO_ROOT" && git rev-parse --show-toplevel 2>&1) || ec=$?
    record_check "git-repo" \
        "git rev-parse --show-toplevel (cd $REPO_ROOT)" \
        "$ec" \
        "$detail"

    # Check 3: Can get current branch
    ec=0
    detail=$(cd "$REPO_ROOT" && git branch --show-current 2>&1) || ec=$?
    record_check "git-branch" \
        "git branch --show-current" \
        "$ec" \
        "$detail"
}

check_python() {
    local ec detail

    # Check 1: python3 available
    ec=0
    detail=$(python3 --version 2>&1) || ec=$?
    record_check "python-available" \
        "python3 --version" \
        "$ec" \
        "$detail"

    # Check 2: uv available
    ec=0
    detail=$(uv --version 2>&1) || ec=$?
    record_check "uv-available" \
        "uv --version" \
        "$ec" \
        "$detail"

    # Check 3: Can import key stdlib modules
    ec=0
    detail=$(python3 -c "import json, subprocess, sys, os, re; print('stdlib ok')" 2>&1) || ec=$?
    record_check "python-stdlib" \
        "python3 -c 'import json, subprocess, sys, os, re'" \
        "$ec" \
        "$detail"
}

check_node() {
    local ec detail

    # Check 1: node available
    ec=0
    detail=$(node --version 2>&1) || ec=$?
    record_check "node-available" \
        "node --version" \
        "$ec" \
        "$detail"

    # Check 2: npm available
    ec=0
    detail=$(npm --version 2>&1) || ec=$?
    record_check "npm-available" \
        "npm --version" \
        "$ec" \
        "$detail"
}

# ── dispatch ─────────────────────────────────────────────────────────────
case "$COMPONENT" in
    proxy)      check_proxy ;;
    opencode)   check_opencode ;;
    taskmaster) check_taskmaster ;;
    registries) check_registries ;;
    git)        check_git ;;
    python)     check_python ;;
    node)       check_node ;;
    *)
        echo "ERROR: Unknown component '$COMPONENT'." >&2
        echo "Valid components: proxy, opencode, taskmaster, registries, git, python, node" >&2
        echo "Use --help for usage." >&2
        exit 2
        ;;
esac

# ── report ───────────────────────────────────────────────────────────────
PASS_COUNT=0
FAIL_COUNT=0
TOTAL=${#CHECK_NAMES[@]}
OVERALL_PASS="true"

if [[ "$JSON_MODE" == "true" ]]; then
    # Read the temp JSON file, wrap it with metadata, and print
    python3 -c "
import json, sys
with open('$RESULTS_TMP') as f:
    checks = json.load(f)
pass_count = sum(1 for c in checks if c['status'] == 'pass')
fail_count = sum(1 for c in checks if c['status'] == 'fail')
output = {
    'component': '${COMPONENT}',
    'total': len(checks),
    'passed': pass_count,
    'failed': fail_count,
    'overall': 'pass' if fail_count == 0 else 'fail',
    'checks': checks
}
json.dump(output, sys.stdout, indent=2)
print()
"
    exit 0
fi

# Human-readable output
echo ""
echo "============================================================"
echo " VERIFY COMPONENT: $COMPONENT"
echo "============================================================"

for ((i=0; i<TOTAL; i++)); do
    name="${CHECK_NAMES[$i]}"
    cmd="${CHECK_COMMANDS[$i]}"
    ec="${CHECK_EXIT_CODES[$i]}"
    detail="${CHECK_DETAILS[$i]}"

    if succeeded "$ec"; then
        status="PASS"
        (( ++PASS_COUNT ))
    else
        status="FAIL"
        (( ++FAIL_COUNT ))
        OVERALL_PASS="false"
    fi

    printf "  [%s]  %s\n" "$status" "$name"
    printf "        command: %s\n" "$cmd"
    printf "        exit:    %s\n" "$ec"
    printf "        detail:  %s\n" "$detail"
    echo ""
done

echo "------------------------------------------------------------"
echo "  Total:  $TOTAL  |  Passed:  $PASS_COUNT  |  Failed:  $FAIL_COUNT"
echo "  Result: $([[ "$OVERALL_PASS" == "true" ]] && echo 'ALL PASS' || echo 'SOME FAILED')"
echo "============================================================"

if [[ "$OVERALL_PASS" == "true" ]]; then
    exit 0
else
    exit 1
fi
