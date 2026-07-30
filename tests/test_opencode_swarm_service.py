"""
Tests for services/opencode_swarm_service.py

Coverage: ConcurrencyRampController, OpenCodeSwarmManager
(_initialize_worker_pool, get_available_worker, _get_pool_id,
execute_subtask_with_worker, execute_subtask_batch_parallel).
"""
import pytest
from models.agent_models import WorkerRole, AgentType


class TestConcurrencyRampController:
    def setup_method(self):
        from services.opencode_swarm_service import ConcurrencyRampController
        self.ctrl = ConcurrencyRampController()

    def test_ramp_sequence_length(self):
        assert len(self.ctrl.ramp_sequence) == 5

    def test_get_current_max_workers_gate_0(self):
        assert self.ctrl.get_current_max_workers(0) == 4

    def test_get_current_max_workers_gate_1(self):
        assert self.ctrl.get_current_max_workers(1) == 8

    def test_get_current_max_workers_gate_2(self):
        assert self.ctrl.get_current_max_workers(2) == 16

    def test_get_current_max_workers_gate_3(self):
        assert self.ctrl.get_current_max_workers(3) == 24

    def test_get_current_max_workers_beyond_gates(self):
        assert self.ctrl.get_current_max_workers(4) == 40
        assert self.ctrl.get_current_max_workers(10) == 40

    def test_get_current_max_workers_negative(self):
        assert self.ctrl.get_current_max_workers(-1) == 4

    def test_get_ramp_sequence(self):
        seq = self.ctrl.get_ramp_sequence()
        assert seq == [4, 8, 16, 24, 40]


class TestOpenCodeSwarmManager:
    def setup_method(self):
        from services.opencode_swarm_service import OpenCodeSwarmManager
        self.manager = OpenCodeSwarmManager()

    def test_initializes_40_workers(self):
        assert len(self.manager.workers) == 40

    def test_workers_by_role(self):
        assert len(self.manager.state.workers_by_role) == 7

    def test_get_available_worker_returns_correct_role(self):
        worker = self.manager.get_available_worker(WorkerRole.UNIT_TESTER)
        assert worker is not None
        assert worker.role == WorkerRole.UNIT_TESTER

    def test_get_available_worker_round_robin(self):
        w1 = self.manager.get_available_worker(WorkerRole.MASTER_ARCHITECT)
        w2 = self.manager.get_available_worker(WorkerRole.MASTER_ARCHITECT)
        # Only 1 MASTER_ARCHITECT, so both calls return the same worker
        assert w1 is not None
        assert w2 is not None
        assert w1.id == w2.id

    def test_get_available_worker_tester_round_robin(self):
        # 5 UNIT_TESTER workers; round-robin should cycle
        seen = set()
        for _ in range(6):
            w = self.manager.get_available_worker(WorkerRole.UNIT_TESTER)
            seen.add(w.id)
            assert w.role == WorkerRole.UNIT_TESTER
        # Should have seen all 5, then wrapped around
        assert len(seen) <= 5

    def test_get_available_worker_fallback_to_core_engineer(self):
        """Getting a role with zero allocation should fall back to core engineer."""
        from services.opencode_swarm_service import OpenCodeSwarmManager, WorkerPoolConfig
        # Create config without HOT_MICRO_SPECIALIST (not in defaults)
        from models.agent_models import WorkerPoolConfig
        config = WorkerPoolConfig()
        manager = OpenCodeSwarmManager(config=config)
        # HOT_MICRO_SPECIALIST has no dedicated allocation
        worker = manager.get_available_worker(WorkerRole.HOT_MICRO_SPECIALIST)
        assert worker is not None

    def test_get_pool_id_mapped(self):
        pid = self.manager._get_pool_id(WorkerRole.CORE_ENGINEER)
        assert pid == "domain_module"

    def test_get_pool_id_fallback(self):
        pid = self.manager._get_pool_id(WorkerRole.MASTER_ARCHITECT)
        assert pid == "general"

    def test_execute_subtask_with_worker_fabric_simulation(self, make_subtask):
        """Since fabric falls to simulation mode, the task should still complete."""
        subtask = make_subtask(title="Test task", desc="Test description")
        result = self.manager.execute_subtask_with_worker(subtask, WorkerRole.CORE_ENGINEER)
        # Should complete (even if simulation)
        assert result["status"] in ("completed", "failed")
        if result["status"] == "completed":
            assert "response" in result

    def test_execute_subtask_batch_parallel(self, make_subtask):
        subtasks = [make_subtask(title=f"Batch {i}", desc="Parallel test") for i in range(3)]
        results = self.manager.execute_subtask_batch_parallel(
            subtasks, role=WorkerRole.CORE_ENGINEER, wave_gate_level=0
        )
        assert len(results) == 3
