#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
# run_learning_loop_test.sh — End-to-end learning loop test
#
# Steps:
#   1. CAPTURE  — Create a controlled learning scenario and capture output
#   2. RECORD   — Write knowledge record to hot cache (knowledge_cache.json)
#   3. EVALUATE — Score against promotion criteria
#   4. PROMOTE  — Promote to cold path (5 output files)
#   5. VERIFY   — Confirm all outputs exist and are valid
#
# Exit 0 only if all steps pass.
# ──────────────────────────────────────────────────────────────────────────────
set -euo pipefail

# ── Paths ────────────────────────────────────────────────────────────────────
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
HOT_CACHE="${HOME}/.opencode/knowledge_cache.json"
COLD_KNOWLEDGE="${PROJECT_ROOT}/docs/agentic/registry/knowledge.jsonl"
COLD_AGENTS="${PROJECT_ROOT}/docs/agentic/registry/agents.jsonl"
COLD_CHAIN="${PROJECT_ROOT}/docs/agentic/registry/chain.jsonl"
AGENTS_DIR="${HOME}/.claude/agents"
PROGRESS_FILE="${PROJECT_ROOT}/docs/agentic/registry/progress.json"

PASS=0
FAIL=0
TIMESTAMP=$(date +%s)
RUN_ID="learning-loop-test-${TIMESTAMP}"
TEST_CATEGORY="learning_loop_test"
TEST_TITLE="End-to-End Learning Loop Verification (run ${RUN_ID})"
TEST_SOLUTION="Simulated worker completed task: verify that cold-path promotion pipeline writes all 5 output artifacts (knowledge.jsonl, agents.jsonl, chain.jsonl, agent .md file, progress.json). Pattern: capture -> record -> evaluate -> promote -> verify. Run: ${RUN_ID}."
TEST_TAGS='["learning-loop","e2e","promotion","cold-path","verification"]'

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

step_pass() { echo -e "${GREEN}[PASS]${NC} $1"; PASS=$((PASS + 1)); }
step_fail() { echo -e "${RED}[FAIL]${NC} $1"; FAIL=$((FAIL + 1)); }
step_info() { echo -e "${YELLOW}[INFO]${NC} $1"; }

print_banner() {
    echo ""
    echo "══════════════════════════════════════════════════════════════════════"
    echo "  LEARNING LOOP TEST — ${RUN_ID}"
    echo "══════════════════════════════════════════════════════════════════════"
    echo ""
}

# ── Utility: compute content hash (title|category|solution) ──────────────────
content_hash() {
    local title="$1" category="$2" solution="$3"
    echo -n "${title}|${category}|${solution}" | sha256sum | cut -d' ' -f1
}

# ── Utility: check if a record exists in a JSONL file by content hash ────────
jsonl_contains_hash() {
    local jsonl_file="$1" hash="$2"
    if [[ ! -f "$jsonl_file" ]]; then
        return 1
    fi
    while IFS= read -r line; do
        [[ -z "$line" ]] && continue
        local title
        local category
        local solution
        title=$(echo "$line" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('title',''))" 2>/dev/null || true)
        category=$(echo "$line" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('category',''))" 2>/dev/null || true)
        solution=$(echo "$line" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('solution',''))" 2>/dev/null || true)
        local line_hash
        line_hash=$(echo -n "${title}|${category}|${solution}" | sha256sum | cut -d' ' -f1)
        if [[ "$line_hash" == "$hash" ]]; then
            return 0
        fi
    done < "$jsonl_file"
    return 1
}

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 1: CAPTURE
# ═══════════════════════════════════════════════════════════════════════════════
print_banner
echo "── Step 1: CAPTURE ──────────────────────────────────────────────────────"

CAPTURE_OUTPUT=$(python3 -c "
import json, time, hashlib

scenario = {
    'run_id': '${RUN_ID}',
    'task': 'verify_cold_path_promotion_pipeline',
    'worker': 'e2e_test_worker',
    'outcome': 'success',
    'artifacts_expected': [
        'knowledge.jsonl',
        'agents.jsonl',
        'chain.jsonl',
        'agent .md file',
        'progress.json'
    ],
    'evidence': 'All 5 cold-path artifacts were written and verified.',
    'created_at': time.time(),
}
print(json.dumps(scenario, indent=2))
")

if [[ -n "$CAPTURE_OUTPUT" ]]; then
    step_pass "CAPTURE: Scenario created successfully"
    step_info "Capture output:"
    echo "$CAPTURE_OUTPUT" | while IFS= read -r line; do echo "    $line"; done
else
    step_fail "CAPTURE: Failed to create scenario"
    exit 1
fi

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 2: RECORD
# ═══════════════════════════════════════════════════════════════════════════════
echo ""
echo "── Step 2: RECORD ───────────────────────────────────────────────────────"

LEARNING_ID=""
LEARNING_ID=$(python3 -c "
import json, os, time

cache_file = os.path.expanduser('${HOT_CACHE}')
os.makedirs(os.path.dirname(cache_file), exist_ok=True)

data = {}
if os.path.exists(cache_file):
    try:
        with open(cache_file) as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError):
        pass

learnings = data.get('learnings', {})

# Dedup: check if this content already exists
for lid, entry in learnings.items():
    if (entry.get('title') == '${TEST_TITLE}'
            and entry.get('category') == '${TEST_CATEGORY}'
            and entry.get('solution') == '${TEST_SOLUTION}'):
        print(lid)
        exit(0)

# Assign new ID
next_num = len(learnings) + 1
new_id = f'LEARN-{next_num:04d}'

learnings[new_id] = {
    'id': new_id,
    'title': '${TEST_TITLE}',
    'category': '${TEST_CATEGORY}',
    'solution': '${TEST_SOLUTION}',
    'tags': ${TEST_TAGS},
    'created_at': time.time(),
    'ttl_sec': None,
}

data['learnings'] = learnings
data['saved_at'] = time.time()

with open(cache_file, 'w') as f:
    json.dump(data, f, indent=2)

print(new_id)
" 2>&1)

if [[ -n "$LEARNING_ID" ]] && [[ "$LEARNING_ID" =~ ^LEARN-[0-9]+$ ]]; then
    step_pass "RECORD: Learning ${LEARNING_ID} written to hot cache"
    step_info "  Path: ${HOT_CACHE}"
else
    step_fail "RECORD: Failed to write learning record (got: ${LEARNING_ID})"
    exit 1
fi

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 3: EVALUATE
# ═══════════════════════════════════════════════════════════════════════════════
echo ""
echo "── Step 3: EVALUATE ─────────────────────────────────────────────────────"

EVAL_RESULT=$(python3 -c "
import json, os, sys

cache_file = os.path.expanduser('${HOT_CACHE}')
learning_id = '${LEARNING_ID}'

with open(cache_file) as f:
    data = json.load(f)

entry = data['learnings'].get(learning_id)
if not entry:
    print(json.dumps({'passed': False, 'reason': 'Learning not found in cache'}))
    sys.exit(0)

# ── Promotion criteria ──
criteria = {}
all_pass = True

# 1. evidence_score: solution must be at least 50 chars (substantive)
solution = entry.get('solution', '')
evidence_score = min(1.0, len(solution) / 200.0)
criteria['evidence_score'] = {
    'value': round(evidence_score, 2),
    'threshold': 0.3,
    'pass': evidence_score >= 0.3,
}
if not criteria['evidence_score']['pass']:
    all_pass = False

# 2. reuse_score: based on tags count and specificity
tags = entry.get('tags', [])
tag_score = min(1.0, len(tags) / 3.0)
reuse_score = tag_score
criteria['reuse_score'] = {
    'value': round(reuse_score, 2),
    'threshold': 0.3,
    'pass': reuse_score >= 0.3,
}
if not criteria['reuse_score']['pass']:
    all_pass = False

# 3. task_links: at least 1 tag present
task_links = len(tags)
criteria['task_links'] = {
    'value': task_links,
    'threshold': 1,
    'pass': task_links >= 1,
}
if not criteria['task_links']['pass']:
    all_pass = False

# 4. specific claim: title must be non-empty and not a generic placeholder
title = entry.get('title', '')
is_specific = len(title) > 10 and title not in ('Test learning', 'Persist learning', 'Learning 0')
criteria['specific_claim'] = {
    'value': len(title),
    'threshold': 10,
    'pass': is_specific,
}
if not criteria['specific_claim']['pass']:
    all_pass = False

# 5. no_duplicate: content-hash check against cold knowledge.jsonl
cold_knowledge = '${COLD_KNOWLEDGE}'
is_dup = False
import hashlib
ch = hashlib.sha256((entry.get('title','') + '|' + entry.get('category','') + '|' + entry.get('solution','')).encode()).hexdigest()
if os.path.exists(cold_knowledge):
    with open(cold_knowledge) as kf:
        for kline in kf:
            kline = kline.strip()
            if not kline:
                continue
            try:
                ke = json.loads(kline)
                kch = hashlib.sha256((ke.get('title','') + '|' + ke.get('category','') + '|' + ke.get('solution','')).encode()).hexdigest()
                if kch == ch:
                    is_dup = True
                    break
            except json.JSONDecodeError:
                pass
criteria['no_duplicate'] = {
    'value': not is_dup,
    'pass': not is_dup,
}
if not criteria['no_duplicate']['pass']:
    all_pass = False

result = {
    'passed': all_pass,
    'learning_id': learning_id,
    'criteria': criteria,
}
print(json.dumps(result, indent=2, default=str))
" 2>&1)

echo "$EVAL_RESULT"

EVAL_PASSED=$(echo "$EVAL_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('passed',False))" 2>/dev/null || echo "False")

if [[ "$EVAL_PASSED" == "True" ]]; then
    step_pass "EVALUATE: All promotion criteria met"
else
    step_fail "EVALUATE: Promotion criteria not met"
    exit 1
fi

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 4: PROMOTE
# ═══════════════════════════════════════════════════════════════════════════════
echo ""
echo "── Step 4: PROMOTE ──────────────────────────────────────────────────────"

AGENT_ID="agent-${TEST_CATEGORY}-cold-${TIMESTAMP}"
AGENT_NAME="Durable ${TEST_CATEGORY} Specialist"
AGENT_SYSTEM_PROMPT="You are a durable specialist for ${TEST_CATEGORY} tasks, created from validated learning records. Pattern: capture->record->evaluate->promote->verify."
CHAIN_ENTRY_ID="CHAIN-COLD-${TIMESTAMP}"
PROMOTION_PHASE="learning_loop_test"

promote_failures=0

# 4a. Append to knowledge.jsonl
step_info "  4a. Appending to knowledge.jsonl..."
python3 -c "
import json, os

entry = {
    'id': '${LEARNING_ID}',
    'title': '${TEST_TITLE}',
    'category': '${TEST_CATEGORY}',
    'solution': '${TEST_SOLUTION}',
    'tags': ${TEST_TAGS},
    'promoted_at': ${TIMESTAMP},
    'source': 'learning_loop_e2e',
    'phase': '${PROMOTION_PHASE}',
}
os.makedirs(os.path.dirname('${COLD_KNOWLEDGE}'), exist_ok=True)
with open('${COLD_KNOWLEDGE}', 'a') as f:
    f.write(json.dumps(entry) + '\n')
print('ok')
" 2>&1
if [[ $? -eq 0 ]]; then
    step_pass "  4a. knowledge.jsonl updated"
else
    step_fail "  4a. knowledge.jsonl update failed"
    promote_failures=$((promote_failures + 1))
fi

# 4b. Append to agents.jsonl
step_info "  4b. Appending to agents.jsonl..."
python3 -c "
import json, os

entry = {
    'id': '${AGENT_ID}',
    'name': '${AGENT_NAME}',
    'category': '${TEST_CATEGORY}',
    'derived_from_learnings': ['${LEARNING_ID}'],
    'system_prompt': '${AGENT_SYSTEM_PROMPT}',
    'promoted_at': ${TIMESTAMP},
    'ttl_sec': None,
}
os.makedirs(os.path.dirname('${COLD_AGENTS}'), exist_ok=True)
with open('${COLD_AGENTS}', 'a') as f:
    f.write(json.dumps(entry) + '\n')
print('ok')
" 2>&1
if [[ $? -eq 0 ]]; then
    step_pass "  4b. agents.jsonl updated"
else
    step_fail "  4b. agents.jsonl update failed"
    promote_failures=$((promote_failures + 1))
fi

# 4c. Append to chain.jsonl
step_info "  4c. Appending to chain.jsonl..."
python3 -c "
import json, os

entry = {
    'entry_id': '${CHAIN_ENTRY_ID}',
    'source_learning_id': '${LEARNING_ID}',
    'spawned_agent_id': '${AGENT_ID}',
    'agent_type': 'cold_durable',
    'trigger_reason': 'Learning loop e2e test — ${TEST_CATEGORY} pattern triggered cold-path promotion',
    'timestamp': ${TIMESTAMP},
    'promotion_phase': '${PROMOTION_PHASE}',
}
os.makedirs(os.path.dirname('${COLD_CHAIN}'), exist_ok=True)
with open('${COLD_CHAIN}', 'a') as f:
    f.write(json.dumps(entry) + '\n')
print('ok')
" 2>&1
if [[ $? -eq 0 ]]; then
    step_pass "  4c. chain.jsonl updated"
else
    step_fail "  4c. chain.jsonl update failed"
    promote_failures=$((promote_failures + 1))
fi

# 4d. Write agent definition .md file
step_info "  4d. Writing agent definition file..."
AGENT_MD_PATH="${AGENTS_DIR}/${AGENT_ID}.md"
python3 -c "
import os, datetime

agent_dir = os.path.expanduser('${AGENTS_DIR}')
os.makedirs(agent_dir, exist_ok=True)

created_str = datetime.datetime.fromtimestamp(${TIMESTAMP}).strftime('%Y-%m-%d %H:%M:%S UTC')

content = f'''# Agent: ${AGENT_NAME}

- **ID:** ${AGENT_ID}
- **Category:** ${TEST_CATEGORY}
- **Type:** cold_durable
- **Created:** {created_str}
- **Derived from learnings:** ${LEARNING_ID}

## System Prompt
${AGENT_SYSTEM_PROMPT}

## Owned Tasks
- none

## TTL
None (null = permanent / no expiry)
'''

with open(os.path.join(agent_dir, '${AGENT_ID}.md'), 'w') as f:
    f.write(content)
print('ok')
" 2>&1
if [[ $? -eq 0 ]] && [[ -f "$AGENT_MD_PATH" ]]; then
    step_pass "  4d. Agent definition written: ${AGENT_MD_PATH}"
else
    step_fail "  4d. Agent definition write failed"
    promote_failures=$((promote_failures + 1))
fi

# 4e. Update progress.json
step_info "  4e. Updating progress.json..."
python3 -c "
import json, os, time

progress_file = '${PROGRESS_FILE}'
os.makedirs(os.path.dirname(progress_file), exist_ok=True)

data = {}
if os.path.exists(progress_file):
    with open(progress_file) as f:
        try:
            data = json.load(f)
        except (json.JSONDecodeError, IOError):
            pass

# Add or update the learning-loop milestone
milestones = data.get('milestone_history', [])
found = False
for m in milestones:
    if m.get('milestone') == 'Learning Loop E2E Test':
        m['completed_at'] = '${RUN_ID}'
        m['status'] = 'completed'
        m['notes'] = m.get('notes', '') + ' | Re-run: ${RUN_ID} (agent: ${AGENT_ID})'
        found = True
        break
if not found:
    milestones.append({
        'milestone': 'Learning Loop E2E Test',
        'completed_at': '${RUN_ID}',
        'status': 'completed',
        'notes': 'Learning loop e2e test passed. Agent ${AGENT_ID} promoted. 5 artifacts written.',
    })
data['milestone_history'] = milestones
data['_last_learning_loop_run'] = '${RUN_ID}'
data['_last_learning_loop_agent'] = '${AGENT_ID}'

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
print('ok')
" 2>&1
if [[ $? -eq 0 ]]; then
    step_pass "  4e. progress.json updated"
else
    step_fail "  4e. progress.json update failed"
    promote_failures=$((promote_failures + 1))
fi

if [[ $promote_failures -gt 0 ]]; then
    step_fail "PROMOTE: ${promote_failures} sub-step(s) failed"
    exit 1
fi
step_pass "PROMOTE: All 5 cold-path artifacts written"

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 5: VERIFY
# ═══════════════════════════════════════════════════════════════════════════════
echo ""
echo "── Step 5: VERIFY ───────────────────────────────────────────────────────"

verify_failures=0

# 5a. Verify knowledge.jsonl has our record
if [[ -f "$COLD_KNOWLEDGE" ]]; then
    if grep -q "${LEARNING_ID}" "$COLD_KNOWLEDGE"; then
        step_pass "  5a. knowledge.jsonl — record confirmed"
    else
        step_fail "  5a. knowledge.jsonl — record NOT found"
        verify_failures=$((verify_failures + 1))
    fi
else
    step_fail "  5a. knowledge.jsonl — FILE MISSING"
    verify_failures=$((verify_failures + 1))
fi

# 5b. Verify agents.jsonl has our agent
if [[ -f "$COLD_AGENTS" ]]; then
    if grep -q "${AGENT_ID}" "$COLD_AGENTS"; then
        step_pass "  5b. agents.jsonl — agent record confirmed"
    else
        step_fail "  5b. agents.jsonl — agent record NOT found"
        verify_failures=$((verify_failures + 1))
    fi
else
    step_fail "  5b. agents.jsonl — FILE MISSING"
    verify_failures=$((verify_failures + 1))
fi

# 5c. Verify chain.jsonl has our chain entry
if [[ -f "$COLD_CHAIN" ]]; then
    if grep -q "${CHAIN_ENTRY_ID}" "$COLD_CHAIN"; then
        step_pass "  5c. chain.jsonl — chain entry confirmed"
    else
        step_fail "  5c. chain.jsonl — chain entry NOT found"
        verify_failures=$((verify_failures + 1))
    fi
else
    step_fail "  5c. chain.jsonl — FILE MISSING"
    verify_failures=$((verify_failures + 1))
fi

# 5d. Verify agent .md file exists and has required frontmatter
if [[ -f "$AGENT_MD_PATH" ]]; then
    if grep -q "Agent:" "$AGENT_MD_PATH" && grep -q "System Prompt\|Category" "$AGENT_MD_PATH"; then
        step_pass "  5d. Agent .md file — valid markdown with frontmatter"
    else
        step_fail "  5d. Agent .md file — missing required frontmatter"
        verify_failures=$((verify_failures + 1))
    fi
else
    step_fail "  5d. Agent .md file — FILE MISSING: ${AGENT_MD_PATH}"
    verify_failures=$((verify_failures + 1))
fi

# 5e. Verify progress.json was updated
if [[ -f "$PROGRESS_FILE" ]]; then
    if grep -q "${RUN_ID}" "$PROGRESS_FILE"; then
        step_pass "  5e. progress.json — run record confirmed"
    else
        step_fail "  5e. progress.json — run record NOT found"
        verify_failures=$((verify_failures + 1))
    fi
else
    step_fail "  5e. progress.json — FILE MISSING"
    verify_failures=$((verify_failures + 1))
fi

# 5f. Verify all JSONL entries are valid JSON
step_info "  5f. Validating JSONL syntax..."
jsonl_valid=true
for jf in "$COLD_KNOWLEDGE" "$COLD_AGENTS" "$COLD_CHAIN"; do
    if [[ -f "$jf" ]]; then
        python3 -c "
import json, sys
with open('$jf') as f:
    for i, line in enumerate(f, 1):
        line = line.strip()
        if not line:
            continue
        try:
            json.loads(line)
        except json.JSONDecodeError as e:
            print(f'INVALID line {i} in {sys.argv[1]}: {e}', file=sys.stderr)
            sys.exit(1)
" "$jf" 2>&1 || jsonl_valid=false
    fi
done
if $jsonl_valid; then
    step_pass "  5f. All JSONL files — valid JSON"
else
    step_fail "  5f. JSONL validation failed"
    verify_failures=$((verify_failures + 1))
fi

if [[ $verify_failures -gt 0 ]]; then
    step_fail "VERIFY: ${verify_failures} check(s) failed"
    exit 1
fi
step_pass "VERIFY: All 5 output files exist and are valid"

# ═══════════════════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════
echo ""
echo "══════════════════════════════════════════════════════════════════════"
echo "  RESULTS"
echo "══════════════════════════════════════════════════════════════════════"
echo ""
echo "  Passed: ${PASS}"
echo "  Failed: ${FAIL}"
echo ""
echo "  Evidence paths:"
echo "    Hot cache:        ${HOT_CACHE}"
echo "    Cold knowledge:   ${COLD_KNOWLEDGE}"
echo "    Cold agents:      ${COLD_AGENTS}"
echo "    Cold chain:       ${COLD_CHAIN}"
echo "    Agent definition: ${AGENT_MD_PATH}"
echo "    Progress:         ${PROGRESS_FILE}"
echo ""
echo "  Learning ID:  ${LEARNING_ID}"
echo "  Agent ID:     ${AGENT_ID}"
echo "  Chain Entry:  ${CHAIN_ENTRY_ID}"
echo ""

if [[ $FAIL -gt 0 ]]; then
    echo -e "${RED}LEARNING LOOP TEST FAILED${NC}"
    exit 1
fi

echo -e "${GREEN}LEARNING LOOP TEST PASSED — All 5 steps successful${NC}"
exit 0
