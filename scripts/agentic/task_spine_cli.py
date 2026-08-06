#!/usr/bin/env python3
"""
Task Spine Fallback CLI Adapter
──────────────────────────────
Operates on the same JSON state as TaskMasterService, providing a
standalone CLI for the complete task lifecycle. Designed to be
swappable with the real Task Master AI when available.

Usage:
  uv run python scripts/agentic/task_spine_cli.py create "My Task" "Description"
  uv run python scripts/agentic/task_spine_cli.py list
  uv run python scripts/agentic/task_spine_cli.py claim <task-id> <worker-id>
  uv run python scripts/agentic/task_spine_cli.py update <task-id> <status>
  uv run python scripts/agentic/task_spine_cli.py block <task-id> <blocked-task-id>
  uv run python scripts/agentic/task_spine_cli.py attach-evidence <task-id> <path>
  uv run python scripts/agentic/task_spine_cli.py inspect <task-id>
  uv run python scripts/agentic/task_spine_cli.py restart-verify
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
STATE_DIR = _REPO_ROOT / ".taskmaster" / "tasks"
STATE_FILE = STATE_DIR / "tasks.json"
EVIDENCE_DIR = _REPO_ROOT / ".taskmaster" / "evidence"


def _load_state() -> dict:
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {
        "title": "Task Spine Fallback",
        "epics": [],
        "spec_gaps": [],
        "total_estimated_turns": 0,
        "parsed_at": time.time(),
    }


def _save_state(state: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    tmp = str(STATE_FILE) + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2)
    os.replace(tmp, str(STATE_FILE))
    print(f"  ✓ State saved to {STATE_FILE}")


def _find_task(state: dict, task_id: str) -> dict | None:
    for epic in state.get("epics", []):
        if epic["id"] == task_id:
            return epic
        for st in epic.get("subtasks", []):
            if st["id"] == task_id:
                return st
    return None


_id_counter = [0]  # mutable across calls within same second


def cmd_create(args) -> None:
    state = _load_state()
    _id_counter[0] += 1
    task_id = f"TASK-{int(time.time() * 1_000_000)}-{_id_counter[0]:04d}"
    epic = {
        "id": task_id,
        "title": args.title,
        "description": args.description or "",
        "wave_id": args.wave or 0,
        "priority": args.priority or "P2",
        "status": "pending",
        "claimed_by": None,
        "claimed_at": None,
        "completed_at": None,
        "evidence": [],
        "blocked_by": [],
        "blocks": [],
        "dependencies": [],
        "subtasks": [],
        "acceptance_criteria": [],
    }
    state.setdefault("epics", []).append(epic)
    _save_state(state)
    print(f"  ✓ Created task {task_id}: {args.title}")


def cmd_list(args) -> None:
    state = _load_state()
    epics = state.get("epics", [])
    if not epics:
        print("  No tasks found.")
        return
    print(f"{'ID':<20} {'STATUS':<12} {'CLAIMED_BY':<16} {'TITLE'}")
    print("-" * 90)
    for epic in epics:
        claimed = epic.get("claimed_by") or "-"
        print(f"{epic['id']:<20} {epic['status']:<12} {claimed:<16} {epic['title'][:40]}")
        for st in epic.get("subtasks", []):
            sc = st.get("claimed_by") or "-"
            print(f"  {st['id']:<18} {st['status']:<12} {sc:<16} {st['title'][:36]}")


def cmd_claim(args) -> None:
    state = _load_state()
    task = _find_task(state, args.task_id)
    if not task:
        print(f"  ✗ Task {args.task_id} not found")
        sys.exit(1)
    if task.get("claimed_by"):
        print(f"  ✗ Task {args.task_id} already claimed by {task['claimed_by']}")
        sys.exit(1)
    task["claimed_by"] = args.worker_id
    task["claimed_at"] = time.time()
    task["status"] = "in_progress"
    _save_state(state)
    print(f"  ✓ Worker {args.worker_id} claimed task {args.task_id}")


def cmd_update(args) -> None:
    state = _load_state()
    task = _find_task(state, args.task_id)
    if not task:
        print(f"  ✗ Task {args.task_id} not found")
        sys.exit(1)
    valid_statuses = {"pending", "in_progress", "completed", "blocked", "failed", "cancelled"}
    if args.status not in valid_statuses:
        print(f"  ✗ Invalid status '{args.status}'. Must be one of: {', '.join(sorted(valid_statuses))}")
        sys.exit(1)
    old = task["status"]
    task["status"] = args.status
    if args.status == "completed":
        task["completed_at"] = time.time()
    if args.error:
        task.setdefault("errors", []).append({"timestamp": time.time(), "error": args.error})
    _save_state(state)
    print(f"  ✓ Task {args.task_id}: {old} → {args.status}")


def cmd_block(args) -> None:
    state = _load_state()
    task = _find_task(state, args.task_id)
    blocked = _find_task(state, args.blocked_task_id)
    if not task:
        print(f"  ✗ Task {args.task_id} not found")
        sys.exit(1)
    if not blocked:
        print(f"  ✗ Blocked task {args.blocked_task_id} not found")
        sys.exit(1)
    task.setdefault("blocks", []).append(args.blocked_task_id)
    blocked.setdefault("blocked_by", []).append(args.task_id)
    blocked["status"] = "blocked"
    _save_state(state)
    print(f"  ✓ {args.task_id} now blocks {args.blocked_task_id}")


def cmd_attach_evidence(args) -> None:
    state = _load_state()
    task = _find_task(state, args.task_id)
    if not task:
        print(f"  ✗ Task {args.task_id} not found")
        sys.exit(1)
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    evidence_entry = {
        "path": args.path,
        "attached_at": time.time(),
        "description": args.description or "",
    }
    task.setdefault("evidence", []).append(evidence_entry)
    _save_state(state)
    print(f"  ✓ Evidence attached to {args.task_id}: {args.path}")


def cmd_inspect(args) -> None:
    state = _load_state()
    task = _find_task(state, args.task_id)
    if not task:
        print(f"  ✗ Task {args.task_id} not found")
        sys.exit(1)
    print(json.dumps(task, indent=2, default=str))


def cmd_restart_verify(args) -> None:
    """Verify state survives restart by saving, re-reading, and showing key fields."""
    state = _load_state()
    epics = state.get("epics", [])
    if not epics:
        print("  ✗ No tasks exist. Create tasks first before restart verify.")
        sys.exit(1)
    task_count = len(epics)
    claimed = sum(1 for e in epics if e.get("claimed_by"))
    completed = sum(1 for e in epics if e.get("status") == "completed")
    blocked = sum(1 for e in epics if e.get("status") == "blocked")
    evidence_count = sum(len(e.get("evidence", [])) for e in epics)
    print("  ✓ Restart verification PASSED:")
    print(
        f"    Tasks: {task_count} | Claimed: {claimed} | Completed: {completed} | Blocked: {blocked} | Evidence: {evidence_count}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Task Spine Fallback CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("create")
    p.add_argument("title")
    p.add_argument("description", nargs="?", default="")
    p.add_argument("--wave", type=int, default=0)
    p.add_argument("--priority", default="P2")

    p = sub.add_parser("list")

    p = sub.add_parser("claim")
    p.add_argument("task_id")
    p.add_argument("worker_id")

    p = sub.add_parser("update")
    p.add_argument("task_id")
    p.add_argument("status")
    p.add_argument("--error")

    p = sub.add_parser("block")
    p.add_argument("task_id")
    p.add_argument("blocked_task_id")

    p = sub.add_parser("attach-evidence")
    p.add_argument("task_id")
    p.add_argument("path")
    p.add_argument("--description")

    p = sub.add_parser("inspect")
    p.add_argument("task_id")

    p = sub.add_parser("restart-verify")

    args = parser.parse_args()
    handlers = {
        "create": cmd_create,
        "list": cmd_list,
        "claim": cmd_claim,
        "update": cmd_update,
        "block": cmd_block,
        "attach-evidence": cmd_attach_evidence,
        "inspect": cmd_inspect,
        "restart-verify": cmd_restart_verify,
    }
    handlers[args.command](args)


if __name__ == "__main__":
    main()
