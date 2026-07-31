#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
# load_durable_agents.sh — Scan and validate durable agent definitions
#
# Scans .claude/agents/ for *.md agent definition files and
# docs/agentic/registry/agents.jsonl for agent records.
#
# Output:
#   - Agent ID, name, category, source file, status
#   - System prompt summary (first 100 chars) for each active agent
#   - Validation of markdown frontmatter (name, description)
#
# Exit: 0 if at least one valid agent found, 1 if none found (clean failure).
# ──────────────────────────────────────────────────────────────────────────────
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
AGENTS_DIR="${HOME}/.claude/agents"
AGENTS_JSONL="${PROJECT_ROOT}/docs/agentic/registry/agents.jsonl"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m'

VALID_COUNT=0
INVALID_COUNT=0
TOTAL_FOUND=0

# ── Parse markdown frontmatter from agent .md files ──
parse_agent_md() {
    local md_file="$1"
    local agent_id=""
    local agent_name=""
    local agent_category=""
    local agent_type=""
    local system_prompt=""
    local has_name=false
    local has_description=false

    agent_id=$(grep -oP 'ID:\s*\K.*' "$md_file" | head -1 | sed 's/^\*\* //;s/\*\*$//' | xargs || true)
    agent_name=$(grep -oP '(?<=# Agent: ).*' "$md_file" | head -1 | xargs || true)
    agent_category=$(grep -oP 'Category:\s*\K.*' "$md_file" | head -1 | sed 's/^\*\* //;s/\*\*$//' | xargs || true)
    agent_type=$(grep -oP 'Type:\s*\K.*' "$md_file" | head -1 | xargs || true)

    # Extract system prompt (between "## System Prompt" and next "##" or EOF)
    system_prompt=$(sed -n '/^## System Prompt/,/^## /{//!p;}' "$md_file" | head -5 | tr '\n' ' ' | xargs || true)

    # Validate required frontmatter
    if [[ -n "$agent_name" ]]; then
        has_name=true
    fi
    if grep -qP 'System Prompt|Description' "$md_file"; then
        has_description=true
    fi

    # Determine status
    local status="inactive"
    if $has_name && $has_description; then
        status="active"
    fi

    # Print result as a structured line
    echo "${agent_id:-unknown}|${agent_name:-unnamed}|${agent_category:-uncategorized}|${md_file}|${status}|${system_prompt:0:100}"
}

# ── Parse JSONL agent records ──
parse_agent_jsonl() {
    local jsonl_file="$1"
    if [[ ! -f "$jsonl_file" ]]; then
        return
    fi
    python3 -c "
import json, sys

with open('$jsonl_file') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
            agent_id = entry.get('id', '')
            name = entry.get('name', '')
            category = entry.get('category', '')
            sp = entry.get('system_prompt', '')
            sp_summary = sp[:100] if sp else ''
            # JSONL records are registry-only (no .md file linked here)
            print(f'{agent_id}|{name}|{category}|{jsonl_file}|jsonl_registry|{sp_summary}')
        except json.JSONDecodeError:
            print(f'PARSE_ERROR|PARSE_ERROR|PARSE_ERROR|{jsonl_file}|invalid|')
" 2>/dev/null || true
}

print_banner() {
    echo ""
    echo "══════════════════════════════════════════════════════════════════════"
    echo "  DURABLE AGENT SCAN"
    echo "══════════════════════════════════════════════════════════════════════"
    echo ""
}

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
print_banner

# ── Scan .md agent definition files ──
echo -e "${CYAN}── Agent Definition Files (.claude/agents/) ──${NC}"
echo ""

if [[ -d "$AGENTS_DIR" ]]; then
    shopt -s nullglob
    md_files=("$AGENTS_DIR"/*.md)
    shopt -u nullglob

    if [[ ${#md_files[@]} -gt 0 ]]; then
        for md_file in "${md_files[@]}"; do
            TOTAL_FOUND=$((TOTAL_FOUND + 1))
            IFS='|' read -r agent_id agent_name agent_category source_file status sp_summary <<< "$(parse_agent_md "$md_file")"

            # Determine validity
            if [[ "$status" == "active" ]]; then
                VALID_COUNT=$((VALID_COUNT + 1))
                icon="${GREEN}✓${NC}"
            else
                INVALID_COUNT=$((INVALID_COUNT + 1))
                icon="${RED}✗${NC}"
            fi

            echo "  $icon [${status}] ${agent_name}"
            echo "      ID:       ${agent_id}"
            echo "      Category: ${agent_category}"
            echo "      Source:   ${source_file}"
            if [[ -n "$sp_summary" ]] && [[ "$status" == "active" ]]; then
                echo "      Prompt:   ${sp_summary}..."
            fi
            echo ""
        done
    else
        echo -e "  ${YELLOW}No .md agent files found in ${AGENTS_DIR}${NC}"
        echo ""
    fi
else
    echo -e "  ${YELLOW}Agents directory does not exist: ${AGENTS_DIR}${NC}"
    echo ""
fi

# ── Scan agents.jsonl registry ──
echo -e "${CYAN}── Agent Registry (agents.jsonl) ──${NC}"
echo ""

if [[ -f "$AGENTS_JSONL" ]]; then
    while IFS='|' read -r agent_id agent_name agent_category source_file status sp_summary; do
        [[ -z "$agent_id" ]] && continue
        TOTAL_FOUND=$((TOTAL_FOUND + 1))

        # Check if this JSONL entry has a corresponding .md file
        local md_path="${AGENTS_DIR}/${agent_id}.md"
        if [[ -f "$md_path" ]]; then
            icon="${GREEN}✓${NC}"
            status="active (has .md file)"
            VALID_COUNT=$((VALID_COUNT + 1))
        else
            icon="${YELLOW}○${NC}"
            status="jsonl_only (no .md file)"
        fi

        echo "  $icon ${agent_name}"
        echo "      ID:       ${agent_id}"
        echo "      Category: ${agent_category}"
        echo "      Source:   ${source_file}"
        echo "      Status:   ${status}"
        if [[ -n "$sp_summary" ]]; then
            echo "      Prompt:   ${sp_summary}..."
        fi
        echo ""
    done < <(parse_agent_jsonl "$AGENTS_JSONL")
else
    echo -e "  ${YELLOW}Agent registry not found: ${AGENTS_JSONL}${NC}"
    echo ""
fi

# ── Summary ──
echo "══════════════════════════════════════════════════════════════════════"
echo "  SUMMARY"
echo "══════════════════════════════════════════════════════════════════════"
echo ""
echo "  Total agents found:  ${TOTAL_FOUND}"
echo "  Valid / active:      ${VALID_COUNT}"
echo "  Invalid / inactive:  ${INVALID_COUNT}"
echo ""

if [[ $VALID_COUNT -gt 0 ]]; then
    echo -e "  ${GREEN}At least one valid agent found.${NC}"
    echo ""
    exit 0
else
    echo -e "  ${RED}No valid agents found.${NC}"
    echo ""
    exit 1
fi
