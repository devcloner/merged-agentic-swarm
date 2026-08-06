#!/usr/bin/env python3
"""
Local Task Spine Fallback Adapter

Thread-safe, idempotent CRUD for the local JSON task spine.
Used as the fallback when the real Task Master AI spine
(Anthropic API) is unreachable.

Persistence: .taskmaster/tasks/task_spine.json
Locking: fcntl.flock (blocking, per-process; no-op on non-POSIX)
Atomicity: write to temp file then os.rename
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

try:
    import fcntl
except ImportError:
    # Non-POSIX (e.g. Windows): advisory file locking is unavailable; the store
    # still works via atomic rename, just without cross-process mutual exclusion.
    fcntl = None

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_STATE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".taskmaster", "tasks", "task_spine.json")
)

VALID_STATUSES = {"pending", "in_progress", "completed", "failed", "blocked"}


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------


@dataclass
class TaskRecord:
    id: str
    title: str
    description: str
    status: str = "pending"
    priority: str = "P2"
    worker_id: str | None = None
    owned_paths: list[str] = field(default_factory=list)
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    created_at: str | None = None
    updated_at: str | None = None
    blocked_by: list[str] = field(default_factory=list)
    blocks: list[str] = field(default_factory=list)

    def __post_init__(self):
        now = datetime.now(UTC).isoformat()
        if self.created_at is None:
            self.created_at = now
        if self.updated_at is None:
            self.updated_at = now
        if self.status not in VALID_STATUSES:
            raise ValueError(f"Invalid status '{self.status}'; must be one of {VALID_STATUSES}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "worker_id": self.worker_id,
            "owned_paths": self.owned_paths,
            "evidence_refs": self.evidence_refs,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "blocked_by": self.blocked_by,
            "blocks": self.blocks,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> TaskRecord:
        return cls(
            id=d["id"],
            title=d["title"],
            description=d["description"],
            status=d.get("status", "pending"),
            priority=d.get("priority", "P2"),
            worker_id=d.get("worker_id"),
            owned_paths=d.get("owned_paths", []),
            evidence_refs=d.get("evidence_refs", []),
            created_at=d.get("created_at"),
            updated_at=d.get("updated_at"),
            blocked_by=d.get("blocked_by", []),
            blocks=d.get("blocks", []),
        )


# ---------------------------------------------------------------------------
# Persistence (thread-safe + atomic)
# ---------------------------------------------------------------------------


class TaskSpineStore:
    """Manages the local task spine JSON file with fcntl locking."""

    def __init__(self, state_path: str = DEFAULT_STATE_PATH):
        self.state_path = os.path.abspath(state_path)
        self._lock_fd: int | None = None

    # ---- helpers -----------------------------------------------------------

    def _ensure_dir(self) -> None:
        os.makedirs(os.path.dirname(self.state_path), exist_ok=True)

    def _acquire_lock(self) -> None:
        self._ensure_dir()
        lock_path = self.state_path + ".lock"
        self._lock_fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o644)
        if fcntl is not None:
            fcntl.flock(self._lock_fd, fcntl.LOCK_EX)

    def _release_lock(self) -> None:
        if self._lock_fd is not None:
            if fcntl is not None:
                fcntl.flock(self._lock_fd, fcntl.LOCK_UN)
            os.close(self._lock_fd)
            self._lock_fd = None
            # best-effort cleanup of lock file
            try:
                os.unlink(self.state_path + ".lock")
            except OSError:
                pass

    def _read_raw(self) -> dict[str, Any]:
        if not os.path.exists(self.state_path):
            return {"tasks": {}}
        with open(self.state_path, "r", encoding="utf-8") as fh:
            return json.load(fh)

    def _write_atomic(self, data: dict[str, Any]) -> None:
        self._ensure_dir()
        dirname = os.path.dirname(self.state_path)
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=dirname,
            prefix=".task_spine_",
            suffix=".tmp",
            delete=False,
        ) as tf:
            json.dump(data, tf, indent=2)
            tmp_name = tf.name
        os.rename(tmp_name, self.state_path)

    # ---- public CRUD -------------------------------------------------------

    def init(self) -> dict[str, Any]:
        """Create the spine file if it does not exist. Idempotent."""
        self._ensure_dir()
        with self._locked():
            if not os.path.exists(self.state_path):
                self._write_atomic({"tasks": {}, "updated_at": datetime.now(UTC).isoformat()})
            return {"ok": True, "state_path": self.state_path, "exists": True}

    def create(self, title: str, description: str, priority: str = "P2", task_id: str | None = None) -> dict[str, Any]:
        """Create a new task.  Idempotent on task_id."""
        with self._locked():
            data = self._read_raw()
            tid = task_id or f"TASK-{uuid.uuid4().hex[:8].upper()}"
            if tid in data["tasks"]:
                return {"ok": True, "task": data["tasks"][tid], "created": False, "message": "already exists"}
            task = TaskRecord(id=tid, title=title, description=description, priority=priority)
            data["tasks"][tid] = task.to_dict()
            data["updated_at"] = datetime.now(UTC).isoformat()
            self._write_atomic(data)
            return {"ok": True, "task": task.to_dict(), "created": True}

    def claim(self, task_id: str, worker_id: str, owned_paths: list[str] | None = None) -> dict[str, Any]:
        """Claim a pending task for a worker. Sets status→in_progress."""
        with self._locked():
            data = self._read_raw()
            if task_id not in data["tasks"]:
                return {"ok": False, "error": f"Task '{task_id}' not found"}
            task = TaskRecord.from_dict(data["tasks"][task_id])
            if task.status not in ("pending", "failed", "blocked"):
                return {"ok": False, "error": f"Task '{task_id}' is '{task.status}', not claimable"}
            if task.status == "blocked" and task.blocked_by:
                unresolved = [
                    b for b in task.blocked_by if b in data["tasks"] and data["tasks"][b].get("status") != "completed"
                ]
                if unresolved:
                    return {"ok": False, "error": f"Task '{task_id}' is blocked by unresovled tasks: {unresolved}"}
            task.status = "in_progress"
            task.worker_id = worker_id
            task.updated_at = datetime.now(UTC).isoformat()
            if owned_paths:
                task.owned_paths = owned_paths
            data["tasks"][task_id] = task.to_dict()
            data["updated_at"] = datetime.now(UTC).isoformat()
            self._write_atomic(data)
            return {"ok": True, "task": task.to_dict()}

    def complete(self, task_id: str, evidence: dict[str, Any] | None = None) -> dict[str, Any]:
        """Mark a task as completed with optional evidence."""
        with self._locked():
            data = self._read_raw()
            if task_id not in data["tasks"]:
                return {"ok": False, "error": f"Task '{task_id}' not found"}
            task = TaskRecord.from_dict(data["tasks"][task_id])
            if evidence:
                task.evidence_refs.append(evidence)
            task.status = "completed"
            task.updated_at = datetime.now(UTC).isoformat()
            data["tasks"][task_id] = task.to_dict()
            data["updated_at"] = datetime.now(UTC).isoformat()
            self._write_atomic(data)
            return {"ok": True, "task": task.to_dict()}

    def fail(self, task_id: str, error_message: str) -> dict[str, Any]:
        """Mark a task as failed with an error message stored in evidence."""
        with self._locked():
            data = self._read_raw()
            if task_id not in data["tasks"]:
                return {"ok": False, "error": f"Task '{task_id}' not found"}
            task = TaskRecord.from_dict(data["tasks"][task_id])
            task.status = "failed"
            task.evidence_refs.append({"error": error_message, "at": datetime.now(UTC).isoformat()})
            task.updated_at = datetime.now(UTC).isoformat()
            data["tasks"][task_id] = task.to_dict()
            data["updated_at"] = datetime.now(UTC).isoformat()
            self._write_atomic(data)
            return {"ok": True, "task": task.to_dict()}

    def block(self, task_id: str, blocked_by: list[str] | None = None) -> dict[str, Any]:
        """Mark a task as blocked, optionally recording blocker ids."""
        with self._locked():
            data = self._read_raw()
            if task_id not in data["tasks"]:
                return {"ok": False, "error": f"Task '{task_id}' not found"}
            task = TaskRecord.from_dict(data["tasks"][task_id])
            task.status = "blocked"
            if blocked_by:
                task.blocked_by = list(set(task.blocked_by) | set(blocked_by))
                # Also update blocking tasks' blocks list
                for bid in blocked_by:
                    if bid in data["tasks"]:
                        bt = TaskRecord.from_dict(data["tasks"][bid])
                        bt.updated_at = datetime.now(UTC).isoformat()
                        if task_id not in bt.blocks:
                            bt.blocks.append(task_id)
                            data["tasks"][bid] = bt.to_dict()
            task.updated_at = datetime.now(UTC).isoformat()
            data["tasks"][task_id] = task.to_dict()
            data["updated_at"] = datetime.now(UTC).isoformat()
            self._write_atomic(data)
            return {"ok": True, "task": task.to_dict()}

    def update(self, task_id: str, **fields) -> dict[str, Any]:
        """Generic update: set arbitrary fields on a task."""
        allowed = {"title", "description", "priority", "worker_id", "owned_paths", "blocked_by", "blocks"}
        with self._locked():
            data = self._read_raw()
            if task_id not in data["tasks"]:
                return {"ok": False, "error": f"Task '{task_id}' not found"}
            task = TaskRecord.from_dict(data["tasks"][task_id])
            for k, v in fields.items():
                if k in allowed and hasattr(task, k):
                    setattr(task, k, v)
            task.updated_at = datetime.now(UTC).isoformat()
            data["tasks"][task_id] = task.to_dict()
            data["updated_at"] = datetime.now(UTC).isoformat()
            self._write_atomic(data)
            return {"ok": True, "task": task.to_dict()}

    def list_tasks(self, status: str | None = None) -> dict[str, Any]:
        """List tasks, optionally filtered by status."""
        with self._locked():
            data = self._read_raw()
            tasks = list(data["tasks"].values())
            if status:
                tasks = [t for t in tasks if t.get("status") == status]
            tasks.sort(key=lambda t: t.get("created_at", ""))
            return {"ok": True, "count": len(tasks), "tasks": tasks}

    def inspect(self, task_id: str) -> dict[str, Any]:
        """Return full detail for a single task."""
        with self._locked():
            data = self._read_raw()
            if task_id not in data["tasks"]:
                return {"ok": False, "error": f"Task '{task_id}' not found"}
            return {"ok": True, "task": data["tasks"][task_id]}

    def attach_evidence(self, task_id: str, evidence: dict[str, Any]) -> dict[str, Any]:
        """Append an evidence record to a task without changing its status."""
        with self._locked():
            data = self._read_raw()
            if task_id not in data["tasks"]:
                return {"ok": False, "error": f"Task '{task_id}' not found"}
            task = TaskRecord.from_dict(data["tasks"][task_id])
            task.evidence_refs.append(evidence)
            task.updated_at = datetime.now(UTC).isoformat()
            data["tasks"][task_id] = task.to_dict()
            data["updated_at"] = datetime.now(UTC).isoformat()
            self._write_atomic(data)
            return {"ok": True, "task": task.to_dict()}

    # ---- context manager ---------------------------------------------------

    class _LockedScope:
        def __init__(self, store: TaskSpineStore):
            self.store = store

        def __enter__(self):
            self.store._acquire_lock()
            return self.store

        def __exit__(self, *args):
            self.store._release_lock()

    def _locked(self) -> _LockedScope:
        return self._LockedScope(self)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _make_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Local Task Spine Fallback Adapter", prog="task_spine_adapter")
    p.add_argument("--state-path", default=DEFAULT_STATE_PATH, help="Path to task_spine.json")

    cmds = p.add_argument_group("Commands")
    cmds.add_argument("--init", action="store_true", help="Create state file if missing")
    cmds.add_argument("--create", action="store_true", help="Create a new task")
    cmds.add_argument("--claim", action="store_true", help="Claim a task for a worker")
    cmds.add_argument("--complete", action="store_true", help="Mark a task completed")
    cmds.add_argument("--fail", action="store_true", help="Mark a task failed")
    cmds.add_argument("--block", action="store_true", help="Mark a task blocked")
    cmds.add_argument("--list", action="store_true", help="List tasks")
    cmds.add_argument("--inspect", action="store_true", help="Inspect a single task")
    cmds.add_argument("--attach-evidence", action="store_true", help="Attach evidence to a task")

    opts = p.add_argument_group("Options")
    opts.add_argument("--task-id", help="Task identifier")
    opts.add_argument("--title", help="Task title (--create)")
    opts.add_argument("--description", help="Task description (--create)")
    opts.add_argument("--priority", default="P2", help="Task priority (--create)")
    opts.add_argument("--worker-id", help="Worker identifier (--claim)")
    opts.add_argument("--evidence", help="JSON evidence string (--complete, --attach-evidence)")
    opts.add_argument("--error-message", help="Error message (--fail)")
    opts.add_argument("--status", help="Filter by status (--list)")
    opts.add_argument("--blocked-by", help="Comma-separated blocker task IDs (--block)")

    return p


def main() -> None:
    parser = _make_parser()
    args = parser.parse_args()

    store = TaskSpineStore(state_path=os.path.abspath(args.state_path))
    result: dict[str, Any] = {"ok": False, "error": "No command given"}

    try:
        if args.init:
            result = store.init()
        elif args.create:
            if not args.title:
                result = {"ok": False, "error": "--title is required for --create"}
            else:
                result = store.create(
                    title=args.title,
                    description=args.description or "",
                    priority=args.priority,
                    task_id=args.task_id,
                )
        elif args.claim:
            if not args.task_id or not args.worker_id:
                result = {"ok": False, "error": "--task-id and --worker-id are required for --claim"}
            else:
                result = store.claim(task_id=args.task_id, worker_id=args.worker_id)
        elif args.complete:
            if not args.task_id:
                result = {"ok": False, "error": "--task-id is required for --complete"}
            else:
                evidence = None
                if args.evidence:
                    try:
                        evidence = json.loads(args.evidence)
                    except json.JSONDecodeError as e:
                        result = {"ok": False, "error": f"Invalid --evidence JSON: {e}"}
                        print(json.dumps(result))
                        sys.exit(1)
                result = store.complete(task_id=args.task_id, evidence=evidence)
        elif args.fail:
            if not args.task_id or not args.error_message:
                result = {"ok": False, "error": "--task-id and --error-message are required for --fail"}
            else:
                result = store.fail(task_id=args.task_id, error_message=args.error_message)
        elif args.block:
            if not args.task_id:
                result = {"ok": False, "error": "--task-id is required for --block"}
            else:
                blocked_by = None
                if args.blocked_by:
                    blocked_by = [b.strip() for b in args.blocked_by.split(",") if b.strip()]
                result = store.block(task_id=args.task_id, blocked_by=blocked_by)
        elif args.list:
            result = store.list_tasks(status=args.status)
        elif args.inspect:
            if not args.task_id:
                result = {"ok": False, "error": "--task-id is required for --inspect"}
            else:
                result = store.inspect(task_id=args.task_id)
        elif args.attach_evidence:
            if not args.task_id or not args.evidence:
                result = {"ok": False, "error": "--task-id and --evidence are required for --attach-evidence"}
            else:
                try:
                    evidence = json.loads(args.evidence)
                except json.JSONDecodeError as e:
                    result = {"ok": False, "error": f"Invalid --evidence JSON: {e}"}
                    print(json.dumps(result))
                    sys.exit(1)
                result = store.attach_evidence(task_id=args.task_id, evidence=evidence)
        else:
            result = {
                "ok": False,
                "error": "No command specified. Use --init, --create, --claim, --complete, --fail, --block, --list, --inspect, or --attach-evidence.",
            }

    except Exception as exc:
        result = {"ok": False, "error": str(exc)}

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
