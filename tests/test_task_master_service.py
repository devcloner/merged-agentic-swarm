"""
Tests for services/task_master_service.py

Coverage: TaskMasterService — load_state, save_state, _estimate_turns,
optimize_and_parse_prd, update_task_status, get_tasks_for_wave.
"""
import json
import os

from models.prd_models import TaskStatus


class TestTaskMasterService:
    def test_empty_state(self, temp_dir):
        from services.task_master_service import TaskMasterService
        state = os.path.join(temp_dir, "tasks.json")
        tm = TaskMasterService(state_file_path=state)
        assert tm.current_analysis is None

    def test_load_existing_state(self, temp_dir):
        from services.task_master_service import TaskMasterService
        state = os.path.join(temp_dir, "tasks.json")
        data = {
            "title": "Test PRD",
            "summary": "Summary",
            "epics": [
                {
                    "id": "EPIC-01", "title": "Test Epic",
                    "description": "Desc", "wave_id": 0,
                    "status": "pending", "priority": "P1",
                    "subtasks": [
                        {"id": "ST-01", "title": "Task 1",
                         "description": "Desc", "status": "pending",
                         "estimated_turns": 1}
                    ],
                    "dependencies": [],
                    "acceptance_criteria": [],
                }
            ],
            "spec_gaps": [],
            "total_estimated_turns": 1,
        }
        with open(state, "w") as f:
            json.dump(data, f)
        tm = TaskMasterService(state_file_path=state)
        assert tm.current_analysis is not None
        assert len(tm.current_analysis.epics) == 1
        assert tm.current_analysis.epics[0].id == "EPIC-01"

    def test_load_corrupted_state(self, temp_dir):
        from services.task_master_service import TaskMasterService
        state = os.path.join(temp_dir, "tasks.json")
        with open(state, "w") as f:
            f.write("not json")
        tm = TaskMasterService(state_file_path=state)
        assert tm.current_analysis is None

    def test_estimate_turns_simple(self, temp_dir):
        from services.task_master_service import TaskMasterService
        tm = TaskMasterService(state_file_path=os.path.join(temp_dir, "tasks.json"))
        turns = tm._estimate_turns("Simple task")
        assert turns == 1

    def test_estimate_turns_complex(self, temp_dir):
        from services.task_master_service import TaskMasterService
        tm = TaskMasterService(state_file_path=os.path.join(temp_dir, "tasks.json"))
        turns = tm._estimate_turns("Multi-provider concurrent full integration")
        assert turns == 5  # baseline 1 + 5 indicators, capped at 5

    def test_estimate_turns_capped(self, temp_dir):
        from services.task_master_service import TaskMasterService
        tm = TaskMasterService(state_file_path=os.path.join(temp_dir, "tasks.json"))
        turns = tm._estimate_turns("multi-provider concurrent distributed comprehensive robust")
        assert turns == 5  # capped at 5

    def test_optimize_and_parse_prd(self, temp_dir):
        """Verify PRD parsing creates expected epics and structure."""
        from services.task_master_service import TaskMasterService
        tm = TaskMasterService(state_file_path=os.path.join(temp_dir, "tasks.json"))
        result = tm.optimize_and_parse_prd("Test PRD content", title="Test")
        assert len(result.epics) == 6
        assert result.title == "Test"
        assert result.total_estimated_turns > 0

    def test_optimize_and_parse_prd_persists(self, temp_dir):
        from services.task_master_service import TaskMasterService
        state = os.path.join(temp_dir, "tasks.json")
        tm = TaskMasterService(state_file_path=state)
        tm.optimize_and_parse_prd("Content", title="Persist Test")
        assert os.path.exists(state)

    def test_update_task_status_epic(self, temp_dir):
        from services.task_master_service import TaskMasterService
        tm = TaskMasterService(state_file_path=os.path.join(temp_dir, "tasks.json"))
        tm.optimize_and_parse_prd("Content", title="Status Test")
        tm.update_task_status("EPIC-01", TaskStatus.COMPLETED)
        assert tm.current_analysis.epics[1].status == TaskStatus.COMPLETED

    def test_update_task_status_subtask(self, temp_dir):
        from services.task_master_service import TaskMasterService
        tm = TaskMasterService(state_file_path=os.path.join(temp_dir, "tasks.json"))
        tm.optimize_and_parse_prd("Content", title="Subtask Status")
        subtask_id = tm.current_analysis.epics[0].subtasks[0].id
        tm.update_task_status(subtask_id, TaskStatus.COMPLETED)
        st = tm.current_analysis.epics[0].subtasks[0]
        assert st.status == TaskStatus.COMPLETED
        assert st.completed_at is not None

    def test_update_task_status_with_error(self, temp_dir):
        from services.task_master_service import TaskMasterService
        tm = TaskMasterService(state_file_path=os.path.join(temp_dir, "tasks.json"))
        tm.optimize_and_parse_prd("Content", title="Error Test")
        tm.update_task_status("EPIC-00", TaskStatus.FAILED, error_message="Broke")
        assert tm.current_analysis.epics[0].status == TaskStatus.FAILED

    def test_update_task_status_no_analysis(self, temp_dir):
        from services.task_master_service import TaskMasterService
        tm = TaskMasterService(state_file_path=os.path.join(temp_dir, "tasks.json"))
        # Should not crash when current_analysis is None
        tm.update_task_status("EPIC-01", TaskStatus.COMPLETED)

    def test_get_tasks_for_wave(self, temp_dir):
        from services.task_master_service import TaskMasterService
        tm = TaskMasterService(state_file_path=os.path.join(temp_dir, "tasks.json"))
        tm.optimize_and_parse_prd("Content", title="Wave Test")
        wave0 = tm.get_tasks_for_wave(0)
        assert len(wave0) == 1
        assert wave0[0].id == "EPIC-00"

    def test_get_tasks_for_wave_no_analysis(self, temp_dir):
        from services.task_master_service import TaskMasterService
        tm = TaskMasterService(state_file_path=os.path.join(temp_dir, "tasks.json"))
        assert tm.get_tasks_for_wave(0) == []

    def test_prd_analysis_includes_fabric_preview(self, temp_dir):
        from services.task_master_service import TaskMasterService
        tm = TaskMasterService(state_file_path=os.path.join(temp_dir, "tasks.json"))
        result = tm.optimize_and_parse_prd("Content")
        assert result.summary is not None
        # Each epic should have estimated_turns
        for epic in result.epics:
            for st in epic.subtasks:
                assert st.estimated_turns >= 1
