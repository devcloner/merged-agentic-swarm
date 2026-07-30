"""
Tests for services/progress_ledger_service.py

Coverage: ObstaclePlaybookEngine (match_and_remediate),
ProgressLedgerService (load, save, log_progress, record_success_marker,
handle_task_failure).
"""
import os
import time
import json
import pytest


class TestObstaclePlaybookEngine:
    def setup_method(self):
        from services.progress_ledger_service import ObstaclePlaybookEngine
        self.engine = ObstaclePlaybookEngine()

    def test_match_rate_limit(self):
        result = self.engine.match_and_remediate("429 Too Many Requests", "TASK-01")
        assert result["remediated"] is True
        assert result["strategy"] == "rotate_key_pool"

    def test_match_rate_limit_case_insensitive(self):
        result = self.engine.match_and_remediate("RATE LIMIT exceeded", "TASK-01")
        assert result["remediated"] is True

    def test_match_import_error(self):
        result = self.engine.match_and_remediate("ModuleNotFoundError: No module named 'xyz'", "TASK-01")
        assert result["remediated"] is True
        assert result["strategy"] == "inject_fallback_stub"

    def test_match_syntax_error(self):
        result = self.engine.match_and_remediate("SyntaxError: invalid syntax", "TASK-01")
        assert result["remediated"] is True
        assert result["strategy"] == "spawn_hot_specialist"

    def test_match_type_error(self):
        result = self.engine.match_and_remediate("TypeError: 'NoneType' object is not subscriptable", "TASK-01")
        assert result["remediated"] is True
        assert result["strategy"] == "refactor_interface"

    def test_no_match(self):
        result = self.engine.match_and_remediate("Something completely different", "TASK-01")
        assert result["remediated"] is False

    def test_trigger_count_increments(self):
        self.engine.match_and_remediate("429 error", "TASK-01")
        for entry in self.engine.playbooks:
            if entry.category == "rate_limit":
                assert entry.trigger_count >= 1
                break


class TestProgressLedgerService:
    def test_empty_ledger(self, temp_dir):
        from services.progress_ledger_service import ProgressLedgerService
        ledger_file = os.path.join(temp_dir, "ledger.json")
        ledger = ProgressLedgerService(ledger_file=ledger_file)
        assert ledger.log_entries == []
        assert ledger.success_markers == []

    def test_log_progress(self, temp_dir):
        from services.progress_ledger_service import ProgressLedgerService
        ledger_file = os.path.join(temp_dir, "ledger.json")
        ledger = ProgressLedgerService(ledger_file=ledger_file)
        entry = ledger.log_progress(
            task_id="TASK-01", subtask_id="ST-01", worker_id="w1",
            wave_id=1, action="testing", status="completed",
            tokens_used=100, learning_generated="LEARN-001",
            details={"key": "value"},
        )
        assert entry.entry_id.startswith("LOG-")
        assert len(ledger.log_entries) == 1

    def test_log_progress_persists(self, temp_dir):
        from services.progress_ledger_service import ProgressLedgerService
        ledger_file = os.path.join(temp_dir, "ledger.json")
        ledger1 = ProgressLedgerService(ledger_file=ledger_file)
        ledger1.log_progress("T-01", "ST-01", "w1", 1, "act", "completed")

        ledger2 = ProgressLedgerService(ledger_file=ledger_file)
        assert len(ledger2.log_entries) == 1

    def test_record_success_marker(self, temp_dir):
        from services.progress_ledger_service import ProgressLedgerService
        ledger_file = os.path.join(temp_dir, "ledger.json")
        ledger = ProgressLedgerService(ledger_file=ledger_file)
        marker = ledger.record_success_marker(
            task_id="TASK-01",
            verifier_name="TestVerifier",
            command="test command",
            exit_code=0,
            output_summary="All good",
        )
        assert marker.id.startswith("MARKER-")
        assert marker.command_executed == "test command"

    def test_record_success_with_command_executed(self, temp_dir):
        from services.progress_ledger_service import ProgressLedgerService
        ledger_file = os.path.join(temp_dir, "ledger.json")
        ledger = ProgressLedgerService(ledger_file=ledger_file)
        marker = ledger.record_success_marker(
            task_id="T-01",
            verifier_name="V",
            command_executed="custom_cmd",
            exit_code=0,
            output_summary="OK",
        )
        assert marker.command_executed == "custom_cmd"

    def test_handle_task_failure(self, temp_dir):
        from services.progress_ledger_service import ProgressLedgerService
        ledger_file = os.path.join(temp_dir, "ledger.json")
        ledger = ProgressLedgerService(ledger_file=ledger_file)
        result = ledger.handle_task_failure("TASK-01", "429: rate limited")
        assert result["remediated"] is True
        # Should also log the failure
        assert len(ledger.log_entries) == 1

    def test_load_corrupted_ledger(self, temp_dir):
        from services.progress_ledger_service import ProgressLedgerService
        ledger_file = os.path.join(temp_dir, "ledger.json")
        with open(ledger_file, "w") as f:
            f.write("not valid json")
        ledger = ProgressLedgerService(ledger_file=ledger_file)
        assert ledger.log_entries == []

    def test_save_and_load_success_markers(self, temp_dir):
        from services.progress_ledger_service import ProgressLedgerService
        ledger_file = os.path.join(temp_dir, "ledger.json")
        ledger1 = ProgressLedgerService(ledger_file=ledger_file)
        ledger1.record_success_marker("T-01", "V1", exit_code=0)

        ledger2 = ProgressLedgerService(ledger_file=ledger_file)
        assert len(ledger2.success_markers) == 1
