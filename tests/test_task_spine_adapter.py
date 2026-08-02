"""
Tests for services/task_spine_adapter.py

Real-behavior coverage: TaskSpineStore CRUD against a real JSON state file in
tmp_path (real fcntl locking, real atomic renames), TaskRecord schema, and the
CLI entry point via argparse. No mocks — files and locks are real.
"""
import json
import os

import pytest

from merged_agentic_swarm.services.task_spine_adapter import (
    DEFAULT_STATE_PATH,
    VALID_STATUSES,
    TaskRecord,
    TaskSpineStore,
    _make_parser,
    main,
)


class TestTaskRecord:
    def test_defaults_and_timestamps(self):
        r = TaskRecord(id="T-1", title="t", description="d")
        assert r.status == "pending"
        assert r.priority == "P2"
        assert r.created_at is not None and r.updated_at is not None

    def test_invalid_status_raises(self):
        with pytest.raises(ValueError):
            TaskRecord(id="T-1", title="t", description="d", status="bogus")

    def test_to_dict_roundtrip(self):
        r = TaskRecord(id="T-1", title="t", description="d", status="in_progress", worker_id="w1")
        d = r.to_dict()
        assert d["worker_id"] == "w1"
        r2 = TaskRecord.from_dict(d)
        assert r2.id == "T-1"
        assert r2.status == "in_progress"
        assert r2.owned_paths == []

    def test_from_dict_defaults(self):
        r = TaskRecord.from_dict({"id": "T-1", "title": "t", "description": "d"})
        assert r.status == "pending"
        assert r.owned_paths == []
        assert r.evidence_refs == []

    def test_valid_statuses_are_claimable_set(self):
        assert VALID_STATUSES == {"pending", "in_progress", "completed", "failed", "blocked"}


class TestTaskSpineStore:
    def _store(self, tmp_path):
        return TaskSpineStore(state_path=str(tmp_path / "spine.json"))

    def test_init_creates_file(self, tmp_path):
        store = self._store(tmp_path)
        result = store.init()
        assert result["ok"] is True
        assert os.path.exists(tmp_path / "spine.json")
        # idempotent
        result2 = store.init()
        assert result2["ok"] is True

    def test_create_and_inspect(self, tmp_path):
        store = self._store(tmp_path)
        store.init()
        created = store.create("My task", "A description", priority="P1")
        assert created["created"] is True
        tid = created["task"]["id"]
        assert tid.startswith("TASK-")
        inspected = store.inspect(tid)
        assert inspected["task"]["title"] == "My task"
        assert inspected["task"]["priority"] == "P1"

    def test_create_idempotent_on_task_id(self, tmp_path):
        store = self._store(tmp_path)
        store.init()
        r1 = store.create("t", "d", task_id="FIXED-1")
        r2 = store.create("t", "d", task_id="FIXED-1")
        assert r1["created"] is True
        assert r2["created"] is False
        assert r2["message"] == "already exists"

    def test_claim_pending(self, tmp_path):
        store = self._store(tmp_path)
        store.init()
        tid = store.create("t", "d", task_id="C1")["task"]["id"]
        claimed = store.claim(tid, worker_id="worker-9", owned_paths=["a.py"])
        assert claimed["ok"] is True
        assert claimed["task"]["status"] == "in_progress"
        assert claimed["task"]["worker_id"] == "worker-9"
        assert claimed["task"]["owned_paths"] == ["a.py"]

    def test_claim_missing_task(self, tmp_path):
        store = self._store(tmp_path)
        store.init()
        result = store.claim("NOPE", "w1")
        assert result["ok"] is False
        assert "not found" in result["error"]

    def test_claim_non_claimable_status(self, tmp_path):
        store = self._store(tmp_path)
        store.init()
        tid = store.create("t", "d", task_id="CC")["task"]["id"]
        store.complete(tid)
        result = store.claim(tid, "w1")
        assert result["ok"] is False
        assert "not claimable" in result["error"]

    def test_claim_blocked_by_unresolved(self, tmp_path):
        store = self._store(tmp_path)
        store.init()
        blocker = store.create("blocker", "d", task_id="BLK")["task"]["id"]
        tid = store.create("t", "d", task_id="DEP")["task"]["id"]
        store.block(tid, blocked_by=[blocker])
        result = store.claim(tid, "w1")
        assert result["ok"] is False
        assert "blocked" in result["error"]

    def test_claim_blocked_resolved_ok(self, tmp_path):
        store = self._store(tmp_path)
        store.init()
        blocker = store.create("blocker", "d", task_id="BLK2")["task"]["id"]
        tid = store.create("t", "d", task_id="DEP2")["task"]["id"]
        store.block(tid, blocked_by=[blocker])
        store.complete(blocker)
        result = store.claim(tid, "w1")
        assert result["ok"] is True
        assert result["task"]["status"] == "in_progress"

    def test_complete_with_evidence(self, tmp_path):
        store = self._store(tmp_path)
        store.init()
        tid = store.create("t", "d", task_id="CP")["task"]["id"]
        done = store.complete(tid, evidence={"verifier": "x", "exit_code": 0})
        assert done["ok"] is True
        assert done["task"]["status"] == "completed"
        assert done["task"]["evidence_refs"][0]["verifier"] == "x"

    def test_complete_missing(self, tmp_path):
        store = self._store(tmp_path)
        store.init()
        assert store.complete("NOPE")["ok"] is False

    def test_fail_stores_error(self, tmp_path):
        store = self._store(tmp_path)
        store.init()
        tid = store.create("t", "d", task_id="FL")["task"]["id"]
        result = store.fail(tid, "boom")
        assert result["task"]["status"] == "failed"
        assert result["task"]["evidence_refs"][0]["error"] == "boom"

    def test_block_records_blocks_both_ways(self, tmp_path):
        store = self._store(tmp_path)
        store.init()
        b = store.create("b", "d", task_id="B1")["task"]["id"]
        a = store.create("a", "d", task_id="A1")["task"]["id"]
        store.block(a, blocked_by=[b])
        assert store.inspect(a)["task"]["status"] == "blocked"
        assert b in store.inspect(a)["task"]["blocked_by"]
        assert a in store.inspect(b)["task"]["blocks"]

    def test_block_missing(self, tmp_path):
        store = self._store(tmp_path)
        store.init()
        assert store.block("NOPE")["ok"] is False

    def test_update_allowed_fields(self, tmp_path):
        store = self._store(tmp_path)
        store.init()
        tid = store.create("t", "d", task_id="UP")["task"]["id"]
        result = store.update(tid, priority="P0", worker_id="w9")
        assert result["task"]["priority"] == "P0"
        assert result["task"]["worker_id"] == "w9"
        # disallowed field is ignored
        result2 = store.update(tid, title="new title", status="completed")
        assert result2["task"]["title"] == "new title"
        assert result2["task"]["status"] == "pending"

    def test_update_missing(self, tmp_path):
        store = self._store(tmp_path)
        store.init()
        assert store.update("NOPE", title="x")["ok"] is False

    def test_list_tasks_filter(self, tmp_path):
        store = self._store(tmp_path)
        store.init()
        store.create("a", "d", task_id="L1")
        store.create("b", "d", task_id="L2")
        store.complete("L1")
        all_tasks = store.list_tasks()
        assert all_tasks["count"] == 2
        done = store.list_tasks(status="completed")
        assert done["count"] == 1
        assert done["tasks"][0]["id"] == "L1"

    def test_attach_evidence_preserves_status(self, tmp_path):
        store = self._store(tmp_path)
        store.init()
        tid = store.create("t", "d", task_id="AE")["task"]["id"]
        result = store.attach_evidence(tid, {"note": "observed"})
        assert result["ok"] is True
        assert result["task"]["status"] == "pending"
        assert result["task"]["evidence_refs"][0]["note"] == "observed"

    def test_attach_evidence_missing(self, tmp_path):
        store = self._store(tmp_path)
        store.init()
        assert store.attach_evidence("NOPE", {"x": 1})["ok"] is False

    def test_missing_file_lists_empty(self, tmp_path):
        store = self._store(tmp_path)
        result = store.list_tasks()
        assert result["ok"] is True
        assert result["count"] == 0

    def test_state_file_is_valid_json_after_ops(self, tmp_path):
        store = self._store(tmp_path)
        store.init()
        store.create("a", "d", task_id="J1")
        store.create("b", "d", task_id="J2")
        store.claim("J1", "w1")
        store.complete("J1")
        with open(tmp_path / "spine.json", encoding="utf-8") as fh:
            data = json.load(fh)
        assert set(data["tasks"].keys()) == {"J1", "J2"}
        assert data["tasks"]["J1"]["status"] == "completed"

    def test_default_state_path_is_absolute(self):
        assert os.path.isabs(DEFAULT_STATE_PATH)


class TestCLI:
    def test_parser_has_commands(self):
        parser = _make_parser()
        args = parser.parse_args(["--init", "--state-path", "/tmp/x.json"])
        assert args.init is True
        assert args.state_path == "/tmp/x.json"

    def test_main_init_creates_file(self, tmp_path, capsys):
        state = str(tmp_path / "cli.json")
        result = self._run_cli(capsys, state, "--init")
        assert result["ok"] is True
        assert os.path.exists(state)

    def test_main_create_requires_title(self, tmp_path, capsys):
        state = str(tmp_path / "cli2.json")
        import sys
        old = sys.argv
        sys.argv = ["task_spine_adapter", "--create", "--state-path", state]
        try:
            main()
        finally:
            sys.argv = old
        out = capsys.readouterr().out
        assert "--title is required" in out

    def _run_cli(self, capsys, state, *extra):
        """Run main() with argv and return the parsed JSON of its output."""
        import sys
        argv = ["task_spine_adapter", "--state-path", state, *extra]
        old = sys.argv
        sys.argv = argv
        try:
            main()
        finally:
            sys.argv = old
        return json.loads(capsys.readouterr().out)

    def test_main_create_claim_flow(self, tmp_path, capsys):
        state = str(tmp_path / "cli3.json")
        self._run_cli(capsys, state, "--init")
        created = self._run_cli(capsys, state, "--create", "--title", "CLI task", "--description", "d")
        tid = created["task"]["id"]
        claimed = self._run_cli(capsys, state, "--claim", "--task-id", tid, "--worker-id", "cli-worker")
        assert claimed["task"]["status"] == "in_progress"
        assert claimed["task"]["worker_id"] == "cli-worker"

    def test_main_fail_and_complete(self, tmp_path, capsys):
        state = str(tmp_path / "cli4.json")
        self._run_cli(capsys, state, "--init")
        self._run_cli(capsys, state, "--create", "--title", "t", "--task-id", "C5")
        failed = self._run_cli(capsys, state, "--fail", "--task-id", "C5", "--error-message", "oops")
        assert failed["task"]["status"] == "failed"
        done = self._run_cli(capsys, state, "--complete", "--task-id", "C5")
        assert done["task"]["status"] == "completed"

    def test_main_list_and_inspect(self, tmp_path, capsys):
        state = str(tmp_path / "cli5.json")
        self._run_cli(capsys, state, "--init")
        self._run_cli(capsys, state, "--create", "--title", "t", "--task-id", "L9")
        listing = self._run_cli(capsys, state, "--list")
        assert listing["count"] == 1
        inspected = self._run_cli(capsys, state, "--inspect", "--task-id", "L9")
        assert inspected["task"]["id"] == "L9"
        missing = self._run_cli(capsys, state, "--inspect", "--task-id", "NOPE")
        assert missing["ok"] is False

    def test_main_block_and_attach_evidence(self, tmp_path, capsys):
        state = str(tmp_path / "cli6.json")
        self._run_cli(capsys, state, "--init")
        self._run_cli(capsys, state, "--create", "--title", "b", "--task-id", "B9")
        self._run_cli(capsys, state, "--create", "--title", "a", "--task-id", "A9")
        blocked = self._run_cli(capsys, state, "--block", "--task-id", "A9", "--blocked-by", "B9")
        assert blocked["task"]["status"] == "blocked"
        ev = self._run_cli(capsys, state, "--attach-evidence", "--task-id", "A9", "--evidence", '{"k":"v"}')
        assert ev["task"]["evidence_refs"][0]["k"] == "v"

    def test_main_invalid_evidence_exits(self, tmp_path, capsys):
        state = str(tmp_path / "cli7.json")
        import sys
        old = sys.argv
        try:
            sys.argv = ["task_spine_adapter", "--init", "--state-path", state]
            main()
            sys.argv = ["task_spine_adapter", "--create", "--state-path", state, "--title", "t", "--task-id", "E9"]
            main()
            capsys.readouterr()
            sys.argv = ["task_spine_adapter", "--complete", "--state-path", state, "--task-id", "E9", "--evidence", "not-json"]
            with pytest.raises(SystemExit):
                main()
            out = capsys.readouterr().out
            assert "Invalid --evidence" in out
        finally:
            sys.argv = old

    def test_main_no_command(self, tmp_path, capsys):
        state = str(tmp_path / "cli8.json")
        import sys
        old = sys.argv
        try:
            sys.argv = ["task_spine_adapter", "--state-path", state]
            main()
            out = capsys.readouterr().out
            assert "No command specified" in out
        finally:
            sys.argv = old
