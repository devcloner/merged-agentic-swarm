#!/usr/bin/env bash
# graphify-obsidian-sync.sh — rsync graphify-out/obsidian/ into the Obsidian vault
# The obsidian-vault Syncthing folder then syncs to all devices.
# Run after `graphify update .` to keep vault knowledge current.
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SRC="${PROJECT_DIR}/graphify-out/obsidian"
DST="/home/ubuntu/obsidian-vault/graphify/merged-agentic-swarm"

if [ ! -d "$SRC" ]; then
    echo "graphify-obsidian-sync: source $SRC not found — run graphify first" >&2
    exit 1
fi

mkdir -p "$DST"
rsync -a --delete "$SRC"/ "$DST"/
echo "graphify-obsidian-sync: $(date -u +%Y-%m-%dT%H:%M:%SZ) — $SRC → $DST ($(ls "$DST" | wc -l) files)"
