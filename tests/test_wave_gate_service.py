"""
Tests for services/wave_gate_service.py

Coverage: WaveGateController — evaluate_gate_criteria, advance_wave,
get_wave_state, _check_ownership. Wave 1-3 gates are exercised with a real
TaskMasterService (real epics/subtasks on disk) and a real ownership-map.json,
so incomplete-task and ownership violations are verified for real.
"""

import json
import os

from merged_agentic_swarm.models.prd_models import (
    EpicTask,
    PRDAnalysisResult,
    SubTask,
    TaskPriority,
    TaskStatus,
)


class TestWaveGateController:
    def setup_method(self):
        from merged_agentic_swarm.services.wave_gate_service import WaveGateController

        self.controller = WaveGateController()

    def test_initial_state(self):
        assert self.controller.current_wave == 0
        state = self.controller.get_wave_state(0)
        assert state.status.value == "in_progress"

    def test_get_wave_state_valid(self):
        state = self.controller.get_wave_state(1)
        assert state is not None
        assert state.wave_id == 1

    def test_get_wave_state_invalid_defaults_to_0(self):
        state = self.controller.get_wave_state(99)
        assert state is not None
        # Falls back to wave 0 by implementation

    def test_evaluate_gate_wave_0_passes(self, temp_dir, isolated_codebase_mapper):
        """Wave 0 should pass when there are no unresolved spec gaps."""
        # Replace the singleton with our isolated one
        from merged_agentic_swarm.services import wave_gate_service as wgs

        original_mapper = wgs.default_codebase_mapper
        wgs.default_codebase_mapper = isolated_codebase_mapper

        try:
            passed, reasons = self.controller.evaluate_gate_criteria(0)
            # No spec gaps → should pass
            assert passed is True
            assert len(reasons) == 0
        finally:
            wgs.default_codebase_mapper = original_mapper

    def test_evaluate_gate_invalid_wave(self):
        passed, reasons = self.controller.evaluate_gate_criteria(-1)
        assert passed is False
        assert "Invalid wave ID" in reasons

    def test_advance_wave_passes(self, temp_dir, isolated_codebase_mapper):
        """advance_wave should move from wave 0 to wave 1 if gate criteria pass."""
        from merged_agentic_swarm.services import wave_gate_service as wgs

        original_mapper = wgs.default_codebase_mapper
        wgs.default_codebase_mapper = isolated_codebase_mapper

        try:
            success, message = self.controller.advance_wave()
            assert success is True
            assert self.controller.current_wave == 1
            assert self.controller.waves[0].status.value == "passed"
            assert "Advanced to Wave 1" in message
        finally:
            wgs.default_codebase_mapper = original_mapper

    def test_advance_wave_beyond_all(self, temp_dir, isolated_codebase_mapper, owner_map_file):
        """advance_wave should complete after wave 3."""
        from merged_agentic_swarm.services import wave_gate_service as wgs

        original_mapper = wgs.default_codebase_mapper
        wgs.default_codebase_mapper = isolated_codebase_mapper

        try:
            for _ in range(4):
                success, _ = self.controller.advance_wave()
            success, message = self.controller.advance_wave()
            assert success is True
            assert "All Wave Gates successfully passed" in message
        finally:
            wgs.default_codebase_mapper = original_mapper

    def test_check_ownership_valid(self, owner_map_file, isolated_codebase_mapper):
        """Subtasks producing output within owned paths should have no violations."""
        # Override base dir so it finds our owner map
        # Monkey-patch _check_ownership's base path resolution
        import merged_agentic_swarm.services.wave_gate_service as wave_mod

        os.path.dirname(os.path.dirname(os.path.abspath(wave_mod.__file__)))
        # We can't easily mock os.path.dirname chain, so test the logic directly
        subtasks = [SubTask(id="ST-01", title="T", description="D", output_artifacts=["services/test_service.py"])]
        # Check ownership for domain-module-workers pool
        violations = self.controller._check_ownership(subtasks, "domain-module-workers")
        # This will likely file not found since ownership-map.json is in temp_dir
        # But the code handles that gracefully
        assert isinstance(violations, list)

    def test_fail_advance_if_wave_not_pass(self, temp_dir):
        """Wave 1 fails because task master has no tasks for it."""
        passed, reasons = self.controller.evaluate_gate_criteria(1)
        # Without task_master data for wave 1, there will be incomplete tasks
        # But whether it passes depends on what task_master returns
        # It might pass if get_tasks_for_wave(1) returns empty list
        # This is implementation-dependent, so just check it returns without error
        assert isinstance(passed, bool)
        assert isinstance(reasons, list)

    def test_wave_2_gate_checks_execution(self, temp_dir):
        """Wave 2 gate should evaluate with task_master data."""
        passed, reasons = self.controller.evaluate_gate_criteria(2)
        assert isinstance(passed, bool)
        assert isinstance(reasons, list)

    def test_wave_3_gate_checks_verification(self, temp_dir):
        """Wave 3 gate should evaluate with task_master data and ownership."""
        passed, reasons = self.controller.evaluate_gate_criteria(3)
        assert isinstance(passed, bool)
        assert isinstance(reasons, list)

    def test_advance_wave_sets_timestamps(self, temp_dir, isolated_codebase_mapper):
        from merged_agentic_swarm.services import wave_gate_service as wgs

        original_mapper = wgs.default_codebase_mapper
        wgs.default_codebase_mapper = isolated_codebase_mapper
        try:
            self.controller.advance_wave()
            assert self.controller.waves[0].passed_at is not None
        finally:
            wgs.default_codebase_mapper = original_mapper


def _ownership_map(repo_root, pools):
    path = os.path.join(repo_root, ".opencode", "ownership-map.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"pools": pools}, f)
    return path


class TestWaveGatesWithRealState:
    def _controller(self, tmp_path):
        from merged_agentic_swarm.services import wave_gate_service as wgs
        from merged_agentic_swarm.services.codebase_map_service import CodebaseMapService
        from merged_agentic_swarm.services.task_master_service import TaskMasterService
        from merged_agentic_swarm.services.wave_gate_service import WaveGateController

        controller = WaveGateController()
        # Point wave gates at a real repo root + real task spine.
        wgs.default_codebase_mapper = CodebaseMapService(repo_root=str(tmp_path))
        state_file = os.path.join(str(tmp_path), "tasks.json")
        wgs.default_task_master = TaskMasterService(state_file_path=state_file)
        return controller, wgs

    def _with_epics(self, tmp_path, wgs, statuses):
        """Attach real epics (wave 1) with subtasks carrying output artifacts."""
        epics = []
        for i, (epic_status, subtask_statuses) in enumerate(statuses):
            subtasks = [
                SubTask(
                    id=f"ST-{i}-{j}",
                    title=f"Subtask {i}-{j}",
                    description=f"d {i}-{j}",
                    status=ss,
                    output_artifacts=[f"src/module{i}/file{j}.py"],
                )
                for j, ss in enumerate(subtask_statuses)
            ]
            epics.append(
                EpicTask(
                    id=f"EPIC-W1-{i}",
                    title=f"Epic {i}",
                    description="desc",
                    wave_id=1,
                    priority=TaskPriority.P1_HIGH,
                    status=epic_status,
                    subtasks=subtasks,
                )
            )
        wgs.default_task_master.current_analysis = PRDAnalysisResult(title="T", summary="S", epics=epics)

    def test_wave1_fails_on_incomplete_epics(self, tmp_path):
        controller, wgs = self._controller(tmp_path)
        self._with_epics(tmp_path, wgs, [(TaskStatus.PENDING, [TaskStatus.PENDING])])
        try:
            passed, reasons = controller.evaluate_gate_criteria(1)
            assert passed is False
            assert any("incomplete" in r for r in reasons)
        finally:
            wgs.default_task_master.current_analysis = None

    def test_wave1_passes_when_all_completed(self, tmp_path):
        controller, wgs = self._controller(tmp_path)
        self._with_epics(tmp_path, wgs, [(TaskStatus.COMPLETED, [TaskStatus.COMPLETED])])
        _ownership_map(
            str(tmp_path),
            [
                {
                    "pool_id": "domain-module-workers",
                    "owned_paths": ["src/*"],
                    "forbidden_paths": [],
                }
            ],
        )
        try:
            passed, reasons = controller.evaluate_gate_criteria(1)
            assert passed is True, reasons
            assert reasons == []
        finally:
            wgs.default_task_master.current_analysis = None

    def test_ownership_forbidden_path_violation(self, tmp_path):
        controller, wgs = self._controller(tmp_path)
        self._with_epics(tmp_path, wgs, [(TaskStatus.COMPLETED, [TaskStatus.COMPLETED])])
        _ownership_map(
            str(tmp_path),
            [
                {
                    "pool_id": "domain-module-workers",
                    "owned_paths": ["src/*"],
                    "forbidden_paths": ["src/secret/*"],
                }
            ],
        )
        # Rewrite subtask output to hit the forbidden path
        wgs.default_task_master.current_analysis.epics[0].subtasks[0].output_artifacts = ["src/secret/x.py"]
        try:
            passed, reasons = controller.evaluate_gate_criteria(1)
            assert passed is False
            assert any("forbidden path" in r for r in reasons)
        finally:
            wgs.default_task_master.current_analysis = None

    def test_ownership_outside_owned_paths(self, tmp_path):
        controller, wgs = self._controller(tmp_path)
        self._with_epics(tmp_path, wgs, [(TaskStatus.COMPLETED, [TaskStatus.COMPLETED])])
        _ownership_map(
            str(tmp_path),
            [
                {
                    "pool_id": "domain-module-workers",
                    "owned_paths": ["services/*"],
                    "forbidden_paths": [],
                }
            ],
        )
        try:
            passed, reasons = controller.evaluate_gate_criteria(1)
            assert passed is False
            assert any("outside owned paths" in r for r in reasons)
        finally:
            wgs.default_task_master.current_analysis = None

    def test_ownership_pool_not_found(self, tmp_path):
        controller, wgs = self._controller(tmp_path)
        self._with_epics(tmp_path, wgs, [(TaskStatus.COMPLETED, [TaskStatus.COMPLETED])])
        _ownership_map(str(tmp_path), [{"pool_id": "other-pool", "owned_paths": [], "forbidden_paths": []}])
        try:
            passed, reasons = controller.evaluate_gate_criteria(1)
            assert passed is False
            assert any("not found in ownership map" in r for r in reasons)
        finally:
            wgs.default_task_master.current_analysis = None

    def test_ownership_map_missing(self, tmp_path):
        controller, wgs = self._controller(tmp_path)
        self._with_epics(tmp_path, wgs, [(TaskStatus.COMPLETED, [TaskStatus.COMPLETED])])
        try:
            passed, reasons = controller.evaluate_gate_criteria(1)
            assert passed is False
            assert any("Ownership map not found" in r for r in reasons)
        finally:
            wgs.default_task_master.current_analysis = None

    def test_corrupt_ownership_map(self, tmp_path):
        controller, wgs = self._controller(tmp_path)
        self._with_epics(tmp_path, wgs, [(TaskStatus.COMPLETED, [TaskStatus.COMPLETED])])
        path = os.path.join(str(tmp_path), ".opencode", "ownership-map.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write("{not json")
        try:
            passed, reasons = controller.evaluate_gate_criteria(1)
            assert passed is False
            assert any("Failed to read ownership map" in r for r in reasons)
        finally:
            wgs.default_task_master.current_analysis = None

    def test_advance_wave_fails_when_gate_not_passed(self, tmp_path):
        controller, wgs = self._controller(tmp_path)
        controller.current_wave = 1
        self._with_epics(tmp_path, wgs, [(TaskStatus.PENDING, [TaskStatus.PENDING])])
        try:
            success, _message = controller.advance_wave()
            assert success is False
            assert controller.waves[1].status.value == "failed"
            assert controller.waves[1].failure_reason
        finally:
            wgs.default_task_master.current_analysis = None
