"""
Tests for models/ledger_models.py

Coverage: SuccessMarker, ObstaclePlaybookEntry, ProgressLogEntry,
TaskMasterStateSnapshot.
"""
from models.ledger_models import (
    ObstaclePlaybookEntry,
    ProgressLogEntry,
    SuccessMarker,
    TaskMasterStateSnapshot,
)


class TestSuccessMarker:
    def test_default_creation(self):
        sm = SuccessMarker(id="MARKER-001", task_id="TASK-01", verifier_name="TestVerifier")
        assert sm.id == "MARKER-001"
        assert sm.exit_code == 0
        assert sm.command_executed is None
        assert sm.output_summary == ""
        assert sm.timestamp > 0

    def test_to_dict(self):
        sm = SuccessMarker(
            id="MARKER-002", task_id="TASK-01",
            verifier_name="SyntaxCheck",
            command_executed="python3 -c \"compile(...)\"",
            exit_code=0, output_summary="OK",
        )
        d = sm.to_dict()
        assert d["exit_code"] == 0
        assert "command_executed" in d


class TestObstaclePlaybookEntry:
    def test_default_creation(self):
        entry = ObstaclePlaybookEntry(
            id="PLAYBOOK-01",
            error_pattern=r"429|quota",
            category="rate_limit",
            description="Rate limit hit",
            auto_remediation_strategy="rotate_key_pool",
        )
        assert entry.trigger_count == 0
        assert entry.created_at > 0

    def test_to_dict(self):
        entry = ObstaclePlaybookEntry(
            id="PLAYBOOK-02", error_pattern=r"Error",
            category="general", description="Generic",
            auto_remediation_strategy="retry",
            trigger_count=3,
        )
        d = entry.to_dict()
        assert d["trigger_count"] == 3


class TestProgressLogEntry:
    def test_default_creation(self):
        log = ProgressLogEntry(
            entry_id="LOG-001", task_id="TASK-01",
            subtask_id=None, worker_id="w1",
            wave_id=1, action="testing", status="completed",
        )
        assert log.tokens_used == 0
        assert log.learning_generated is None
        assert log.details == {}

    def test_to_dict(self):
        log = ProgressLogEntry(
            entry_id="LOG-002", task_id="TASK-01",
            subtask_id="ST-01", worker_id="w2",
            wave_id=2, action="spawn", status="completed",
            tokens_used=500, learning_generated="LEARN-001",
            details={"files_applied": 3},
        )
        d = log.to_dict()
        assert d["tokens_used"] == 500
        assert d["details"]["files_applied"] == 3


class TestTaskMasterStateSnapshot:
    def test_default_creation(self):
        snap = TaskMasterStateSnapshot(
            session_id="SESS-001", prd_title="Test",
            total_epics=6, completed_epics=2,
            current_wave=1, progress_percentage=33.3,
        )
        assert snap.last_updated > 0
        assert snap.progress_percentage == 33.3

    def test_to_dict(self):
        snap = TaskMasterStateSnapshot(
            session_id="SESS-001", prd_title="Test",
            total_epics=6, completed_epics=2,
            current_wave=1, progress_percentage=33.3,
        )
        d = snap.to_dict()
        assert d["total_epics"] == 6
        assert d["completed_epics"] == 2
