"""
Tests for models/wave_models.py

Coverage: WavePhase, WaveStatus, WaveGateCriteria, WaveExecutionState.
"""
from models.wave_models import WaveExecutionState, WaveGateCriteria, WavePhase, WaveStatus


class TestWavePhase:
    def test_values(self):
        assert WavePhase.WAVE_0_MAPPING_SPEC.value == 0
        assert WavePhase.WAVE_1_FOUNDATIONS.value == 1
        assert WavePhase.WAVE_2_CORE_FEATURES.value == 2
        assert WavePhase.WAVE_3_INTEGRATION_VERIFICATION.value == 3

    def test_ordering(self):
        assert WavePhase.WAVE_0_MAPPING_SPEC < WavePhase.WAVE_3_INTEGRATION_VERIFICATION


class TestWaveStatus:
    def test_values(self):
        assert WaveStatus.LOCKED.value == "locked"
        assert WaveStatus.IN_PROGRESS.value == "in_progress"
        assert WaveStatus.PASSED.value == "passed"
        assert WaveStatus.FAILED.value == "failed"


class TestWaveGateCriteria:
    def test_default_creation(self):
        criteria = WaveGateCriteria(wave_id=0, name="Default Gate")
        assert criteria.wave_id == 0
        assert criteria.required_tasks_completed is True
        assert criteria.spec_gaps_closed is True
        assert criteria.zero_syntax_errors is True
        assert criteria.tests_passing is True
        assert criteria.security_audited is False
        assert criteria.custom_checks == []

    def test_to_dict(self):
        criteria = WaveGateCriteria(wave_id=1, name="Test Gate", tests_passing=False)
        d = criteria.to_dict()
        assert d["wave_id"] == 1
        assert d["tests_passing"] is False

    def test_custom_checks(self):
        criteria = WaveGateCriteria(
            wave_id=2, name="Custom",
            custom_checks=["check_ownership", "check_security"]
        )
        assert len(criteria.custom_checks) == 2


class TestWaveExecutionState:
    def test_default_creation(self):
        state = WaveExecutionState(wave_id=0, name="Wave 0")
        assert state.status == WaveStatus.LOCKED
        assert state.tasks_assigned == []
        assert state.started_at is None
        assert state.passed_at is None
        assert state.failure_reason is None

    def test_advance_to_in_progress(self):
        state = WaveExecutionState(wave_id=1, name="Wave 1")
        state.status = WaveStatus.IN_PROGRESS
        import time
        state.started_at = time.time()
        assert state.status == WaveStatus.IN_PROGRESS
        assert state.started_at > 0

    def test_to_dict(self):
        state = WaveExecutionState(
            wave_id=2, name="Wave 2",
            status=WaveStatus.PASSED,
            tasks_assigned=["T1", "T2"],
            tasks_completed=["T1"],
        )
        d = state.to_dict()
        assert d["status"] == "passed"
        assert d["gate_criteria"]["wave_id"] == 0

    def test_failure(self):
        state = WaveExecutionState(wave_id=0, name="Wave 0", status=WaveStatus.FAILED, failure_reason="Something broke")
        assert state.failure_reason == "Something broke"
