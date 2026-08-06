"""
Tests for services/report_service.py

Coverage: build_run_report (waves/epics/gates/token/timeline aggregation),
render_report_md (model timeline column), save_run_report (dual JSON+MD output),
and ProgressLedgerService.log_progress accepting a model arg (round-trips into
the report timeline).
"""

import json

from merged_agentic_swarm.services import report_service


def _write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def _write_jsonl(path, entries):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(e) + "\n" for e in entries), encoding="utf-8")
    return path


def _ledger(logs, snapshot=None):
    return {
        "logs": logs,
        "success_markers": [
            {"id": "MARKER-0001", "task_id": "EPIC-1", "verifier_name": "V", "timestamp": 1700000000.0}
        ],
        "task_master_snapshot": snapshot
        or {
            "title": "Test PRD",
            "epics": [{"id": "EPIC-1", "title": "Build core", "wave_id": 1, "status": "completed"}],
        },
    }


def _log(entry_id, task_id, wave_id, action, status, model=None, tokens=0, ts=1700000000.0):
    return {
        "entry_id": entry_id,
        "task_id": task_id,
        "subtask_id": None,
        "worker_id": "w1",
        "wave_id": wave_id,
        "action": action,
        "status": status,
        "timestamp": ts,
        "tokens_used": tokens,
        "model": model,
    }


class TestBuildRunReport:
    def test_empty_ledger(self, tmp_path):
        _write_json(tmp_path / "ledger.json", {"logs": [], "success_markers": [], "task_master_snapshot": {}})
        report = report_service.build_run_report(tmp_path, ledger_file=str(tmp_path / "ledger.json"))
        assert report["waves"] == {}
        assert report["timeline"] == []
        assert report["chain_registry_entries"] == 0
        assert report["knowledge_registry_entries"] == 0

    def test_missing_ledger_returns_empty_report(self, tmp_path):
        report = report_service.build_run_report(tmp_path, ledger_file=str(tmp_path / "missing.json"))
        assert report["waves"] == {}
        assert report["timeline"] == []

    def test_waves_tokens_and_gates_aggregated(self, tmp_path):
        logs = [
            _log("LOG-00001", "EPIC-1", 1, "testing", "completed", tokens=100),
            _log("LOG-00002", "EPIC-1", 1, "synth", "completed", tokens=50),
            _log("LOG-00003", "EPIC-2", 2, "synth", "failed", tokens=25),
        ]
        _write_json(tmp_path / "ledger.json", _ledger(logs))
        report = report_service.build_run_report(tmp_path, ledger_file=str(tmp_path / "ledger.json"))
        assert report["total_tokens_used"] == 175
        assert report["waves"]["1"]["tokens_used"] == 150
        assert report["gates"]["1"]["passed"] is True
        assert report["gates"]["2"]["passed"] is False

    def test_timeline_chronological_with_chain_and_model(self, tmp_path):
        logs = [
            _log("LOG-00001", "EPIC-1", 1, "testing", "completed", model="gemini-2.5-flash", ts=1700000001.0),
            _log("LOG-00002", "EPIC-1", 1, "synth", "completed", model="mistral-small", ts=1700000000.0),
        ]
        _write_json(tmp_path / "ledger.json", _ledger(logs))
        _write_jsonl(
            tmp_path / "docs/agentic/registry/chain.jsonl",
            [{"entry_id": "CHAIN-1", "agent_type": "cold_durable", "timestamp": 1700000000.5}],
        )
        report = report_service.build_run_report(tmp_path, ledger_file=str(tmp_path / "ledger.json"))
        assert [e["entry_id"] for e in report["timeline"]] == ["LOG-00002", "CHAIN-1", "LOG-00001"]
        steps = [e for e in report["timeline"] if e["kind"] == "step"]
        assert steps[0]["model"] == "mistral-small"
        assert steps[1]["model"] == "gemini-2.5-flash"

    def test_registry_counts(self, tmp_path):
        _write_json(tmp_path / "ledger.json", _ledger([]))
        _write_jsonl(tmp_path / "docs/agentic/registry/chain.jsonl", [{"entry_id": "C1"}])
        _write_jsonl(tmp_path / "docs/agentic/registry/knowledge.jsonl", [{"id": "K1"}, {"id": "K2"}])
        report = report_service.build_run_report(tmp_path, ledger_file=str(tmp_path / "ledger.json"))
        assert report["chain_registry_entries"] == 1
        assert report["knowledge_registry_entries"] == 2


class TestRenderMarkdown:
    def test_timeline_model_column(self, tmp_path):
        logs = [
            _log("LOG-00001", "EPIC-1", 1, "testing", "completed", model="gemini-2.5-flash"),
            _log("LOG-00002", "EPIC-1", 1, "synth", "completed"),
        ]
        _write_json(tmp_path / "ledger.json", _ledger(logs))
        report = report_service.build_run_report(tmp_path, ledger_file=str(tmp_path / "ledger.json"))
        md = report_service.render_report_md(report)
        assert "## Timeline" in md
        assert "| Time (UTC) | wave | action | status | model | tokens |" in md
        assert "gemini-2.5-flash" in md
        # A step without a recorded model renders a dash in the model column
        assert "| 1 | synth | completed | - | 0 |" in md


class TestSaveRunReport:
    def test_writes_both_files(self, tmp_path):
        _write_json(tmp_path / "ledger.json", _ledger([_log("LOG-00001", "EPIC-1", 1, "testing", "completed")]))
        saved = report_service.save_run_report(tmp_path, ledger_file=str(tmp_path / "ledger.json"))
        assert saved["json_path"].exists()
        assert saved["md_path"].exists()
        assert saved["json_path"].parent == tmp_path / "reports"
        assert saved["md_path"].parent == tmp_path / "reports"
        parsed = json.loads(saved["json_path"].read_text(encoding="utf-8"))
        assert parsed["prd_title"] == "Test PRD"
        assert saved["md_path"].read_text(encoding="utf-8").startswith("# Run Report")

    def test_creates_custom_reports_dir(self, tmp_path):
        out = tmp_path / "custom"
        _write_json(tmp_path / "ledger.json", _ledger([]))
        saved = report_service.save_run_report(tmp_path, ledger_file=str(tmp_path / "ledger.json"), reports_dir=out)
        assert out.exists()
        assert saved["json_path"].parent == out


class TestLogProgressModelArg:
    def test_log_progress_accepts_model_and_roundtrips(self, tmp_path):
        from merged_agentic_swarm.services.progress_ledger_service import ProgressLedgerService

        ledger_file = str(tmp_path / "ledger.json")
        ledger = ProgressLedgerService(ledger_file=ledger_file)
        entry = ledger.log_progress(
            task_id="EPIC-1",
            subtask_id=None,
            worker_id="w1",
            wave_id=1,
            action="testing",
            status="completed",
            model="gemini-2.5-flash",
            tokens_used=42,
        )
        assert entry.model == "gemini-2.5-flash"
        reloaded = ProgressLedgerService(ledger_file=ledger_file)
        assert reloaded.log_entries[0].model == "gemini-2.5-flash"
        assert reloaded.log_entries[0].tokens_used == 42

    def test_log_progress_model_defaults_to_none(self, tmp_path):
        from merged_agentic_swarm.services.progress_ledger_service import ProgressLedgerService

        ledger = ProgressLedgerService(ledger_file=str(tmp_path / "ledger.json"))
        entry = ledger.log_progress("T-1", "ST-1", "w1", 1, "act", "completed")
        assert entry.model is None

    def test_log_progress_model_appears_in_report(self, tmp_path):
        from merged_agentic_swarm.services.progress_ledger_service import ProgressLedgerService

        ledger_file = str(tmp_path / "ledger.json")
        ledger = ProgressLedgerService(ledger_file=ledger_file)
        ledger.log_progress(
            task_id="EPIC-1",
            subtask_id=None,
            worker_id="w1",
            wave_id=1,
            action="testing",
            status="completed",
            model="gemini-2.5-flash",
        )
        report = report_service.build_run_report(tmp_path, ledger_file=ledger_file)
        steps = [e for e in report["timeline"] if e["kind"] == "step"]
        assert steps[0]["model"] == "gemini-2.5-flash"
        assert report["waves"]["1"]["models"] == ["gemini-2.5-flash"]
