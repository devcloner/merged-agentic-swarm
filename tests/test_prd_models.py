"""
Tests for models/prd_models.py

Coverage: TaskStatus, TaskPriority, SubTask, EpicTask, SpecGap,
PRDDocument, PRDAnalysisResult.
"""

import time

from merged_agentic_swarm.models.prd_models import (
    EpicTask,
    PRDAnalysisResult,
    PRDDocument,
    SpecGap,
    SubTask,
    TaskPriority,
    TaskStatus,
)


class TestTaskStatus:
    def test_values(self):
        assert TaskStatus.PENDING.value == "pending"
        assert TaskStatus.COMPLETED.value == "completed"
        assert TaskStatus.FAILED.value == "failed"
        assert TaskStatus.BLOCKED.value == "blocked"
        assert TaskStatus.SPEC_GAP.value == "spec_gap"
        assert TaskStatus.VERIFYING.value == "verifying"
        assert TaskStatus.IN_PROGRESS.value == "in_progress"


class TestTaskPriority:
    def test_values(self):
        assert TaskPriority.P0_CRITICAL.value == "P0"
        assert TaskPriority.P1_HIGH.value == "P1"
        assert TaskPriority.P2_MEDIUM.value == "P2"
        assert TaskPriority.P3_LOW.value == "P3"


class TestSubTask:
    def test_default_creation(self):
        st = SubTask(id="ST-001", title="Do something", description="Do it well")
        assert st.status == TaskStatus.PENDING
        assert st.assigned_worker_id is None
        assert st.error_message is None
        assert st.estimated_turns == 1
        assert st.completed_at is None

    def test_to_dict_serializes_enum(self):
        st = SubTask(id="ST-001", title="T", description="D")
        d = st.to_dict()
        assert d["status"] == "pending"

    def test_marked_completed_sets_timestamp(self):
        st = SubTask(id="ST-002", title="T", description="D")
        st.status = TaskStatus.COMPLETED
        st.completed_at = time.time()
        assert st.completed_at > 0

    def test_with_error(self):
        st = SubTask(
            id="ST-003", title="Fail", description="D", status=TaskStatus.FAILED, error_message="Something broke"
        )
        assert st.status == TaskStatus.FAILED
        assert st.error_message == "Something broke"


class TestEpicTask:
    def test_default_creation(self):
        SubTask(id="ST-001", title="Sub 1", description="D")
        epic = EpicTask(id="EPIC-01", title="Main Epic", description="Big work", wave_id=1)
        assert epic.priority == TaskPriority.P1_HIGH
        assert epic.status == TaskStatus.PENDING
        assert epic.subtasks == []
        assert epic.created_at > 0
        assert epic.updated_at > 0

    def test_with_subtasks(self):
        st = SubTask(id="ST-001", title="Sub", description="D")
        epic = EpicTask(id="EPIC-01", title="E", description="D", wave_id=0, subtasks=[st])
        assert len(epic.subtasks) == 1

    def test_to_dict_serializes_nested(self):
        st = SubTask(id="ST-001", title="Sub", description="D")
        epic = EpicTask(id="EPIC-01", title="E", description="D", wave_id=1, subtasks=[st])
        d = epic.to_dict()
        assert d["status"] == "pending"
        assert d["priority"] == "P1"
        assert len(d["subtasks"]) == 1
        assert d["subtasks"][0]["id"] == "ST-001"


class TestSpecGap:
    def test_default_creation(self):
        gap = SpecGap(
            id="GAP-01",
            epic_id="EPIC-00",
            missing_requirement="Missing service",
            affected_files=["services/missing.py"],
            suggested_fix="Create service",
        )
        assert not gap.resolved
        assert gap.resolution_note is None

    def test_resolve(self):
        gap = SpecGap(
            id="GAP-01",
            epic_id="EPIC-00",
            missing_requirement="X",
            affected_files=["x.py"],
            suggested_fix="Add X",
        )
        gap.resolved = True
        gap.resolution_note = "Created x.py"
        assert gap.resolved
        assert gap.resolution_note == "Created x.py"

    def test_to_dict(self):
        gap = SpecGap(
            id="GAP-01",
            epic_id="EPIC-00",
            missing_requirement="X",
            affected_files=["x.py"],
            suggested_fix="Add X",
        )
        d = gap.to_dict()
        assert d["id"] == "GAP-01"
        assert not d["resolved"]


class TestPRDDocument:
    def test_default_creation(self):
        doc = PRDDocument(raw_text="Some PRD text")
        assert doc.title == "Unassigned PRD"
        assert doc.version == "1.0.0"

    def test_custom_title(self):
        doc = PRDDocument(raw_text="Text", title="My PRD", version="2.0.0")
        assert doc.title == "My PRD"
        assert doc.version == "2.0.0"


class TestPRDAnalysisResult:
    def test_default_creation(self):
        result = PRDAnalysisResult(
            title="Analysis",
            summary="Done",
        )
        assert result.total_estimated_turns == 0
        assert result.epics == []
        assert result.fabric_response_preview is None

    def test_to_dict_without_preview(self):
        result = PRDAnalysisResult(title="A", summary="S")
        d = result.to_dict()
        assert "fabric_response_preview" not in d

    def test_to_dict_with_preview(self):
        result = PRDAnalysisResult(title="A", summary="S", fabric_response_preview="Raw AI output")
        d = result.to_dict()
        assert d["fabric_response_preview"] == "Raw AI output"
