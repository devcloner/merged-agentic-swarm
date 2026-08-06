"""
Tests for tools/agentic_cli.py

Coverage: cmd_config, basic CLI parsing, cmd_run (success + PRD-missing +
exception paths), cmd_status (real progress.json / registry rendering),
cmd_promote, and argparse dispatch.

The orchestrator's run_full_agentic_workflow / _promote_cold_path methods are
patched at the method level — the CLI's own logic (arg handling, file I/O,
formatting, exit codes) is real. The orchestrator itself is covered by its own
real-behavior tests and the live agentic run.
"""

import json
import os
import sys

import pytest

from merged_agentic_swarm.tools import agentic_cli
from merged_agentic_swarm.tools.agentic_cli import cmd_config


def _write(tmp_path, rel, data):
    path = tmp_path / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data, encoding="utf-8")
    return path


def _args(**overrides):
    class Args:
        pass

    a = Args()
    a.prd = overrides.get("prd", None)
    a.title = overrides.get("title", "Test Title")
    a.verbose = overrides.get("verbose", False)
    a.progress = overrides.get("progress", None)
    a.ledger = overrides.get("ledger", None)
    a.out = overrides.get("out", None)
    a.profile = overrides.get("profile", None)
    return a


def _fake_saved(md_path="r.md", json_path="r.json"):
    """Fake save_run_report return, so auto-save never writes into the real repo."""
    return {"report": {"status": "success"}, "json_path": json_path, "md_path": md_path}


def _patch_auto_save(monkeypatch, saved=None):
    monkeypatch.setattr(
        "merged_agentic_swarm.services.report_service.save_run_report",
        lambda *a, **k: saved if saved is not None else _fake_saved(),
    )


def _main_with_args(argv):
    old = sys.argv
    sys.argv = ["agentic_cli", *argv]
    try:
        agentic_cli.main()
    finally:
        sys.argv = old


class TestCmdConfig:
    def test_cmd_config_output(self, capsys):
        """cmd_config should print key pool, routes, and swarm info without crashing."""
        cmd_config(None)  # None is fine since args not used in cmd_config
        captured = capsys.readouterr()
        assert "Key Pool" in captured.out
        assert "Route:" in captured.out or "Swarm:" in captured.out
        assert "CONFIGURATION STATE" in captured.out

    def test_cmd_config_routes_printed(self, capsys):
        """Verify model routes appear in config output."""
        cmd_config(None)
        captured = capsys.readouterr()
        assert "mistral" in captured.out

    def test_main_entry_points(self):
        """Verify argparse setup works for each subcommand."""
        import sys

        from merged_agentic_swarm.tools.agentic_cli import main

        # Test that unknown commands exit
        with pytest.raises(SystemExit):
            sys.argv = ["agentic_cli.py", "unknown"]
            main()


class TestCLIStringFunctions:
    """Test internal helper behaviors exposed through the CLI module."""

    def test_cmd_promote_without_orchestrator_state(self):
        """cmd_promote should not crash when called directly (uses fresh orchestrator)."""
        from merged_agentic_swarm.tools.agentic_cli import cmd_promote

        # We can't easily test this without mocking because it writes to real registry
        # Just verify it imports correctly
        assert callable(cmd_promote)

    def test_cmd_status_no_progress_file(self, capsys, temp_dir):
        """cmd_status should handle a missing progress ledger gracefully."""
        from merged_agentic_swarm.tools.agentic_cli import cmd_status

        # Create a mock args object
        class Args:
            progress = os.path.join(temp_dir, "nonexistent.json")

        cmd_status(Args())
        captured = capsys.readouterr()
        assert "No progress ledger found" in captured.out


class TestCmdRun:
    def test_run_missing_prd_exits(self, tmp_path, capsys):
        missing = str(tmp_path / "nope.md")
        with pytest.raises(SystemExit) as exc:
            agentic_cli.cmd_run(_args(prd=missing))
        assert exc.value.code == 1
        assert "PRD file not found" in capsys.readouterr().out

    def test_run_success_prints_result(self, tmp_path, capsys, monkeypatch):
        prd = _write(tmp_path, "prd.md", "# PRD\n\nBuild a thing.\n")

        def fake_run(self, prd):
            assert prd == "# PRD\n\nBuild a thing.\n"
            return {
                "status": "completed",
                "waves_completed": 4,
                "epics_completed": 2,
                "total_success_markers": 5,
                "chain_registry_entries": 3,
                "cold_path": {"total_knowledge_records": 2, "total_durable_agents": 1},
            }

        monkeypatch.setattr(
            "merged_agentic_swarm.tools.agentic_orchestrator.MultiLayeredAgenticOrchestrator.run_full_agentic_workflow",
            fake_run,
        )
        _patch_auto_save(monkeypatch)
        result = agentic_cli.cmd_run(_args(prd=str(prd)))
        out = capsys.readouterr().out
        assert result["status"] == "completed"
        assert "Status:          completed" in out
        assert "Waves completed: 4" in out
        assert "Cold-path:       2 knowledge, 1 agents promoted" in out

    def test_run_verbose_prints_full_json(self, tmp_path, capsys, monkeypatch):
        prd = _write(tmp_path, "prd.md", "# PRD\n")

        def fake_run(self, prd):
            return {"status": "completed", "cold_path": {}}

        monkeypatch.setattr(
            "merged_agentic_swarm.tools.agentic_orchestrator.MultiLayeredAgenticOrchestrator.run_full_agentic_workflow",
            fake_run,
        )
        _patch_auto_save(monkeypatch)
        agentic_cli.cmd_run(_args(prd=str(prd), verbose=True))
        out = capsys.readouterr().out
        assert "Full result:" in out
        assert '"status": "completed"' in out

    def test_run_exception_exits(self, tmp_path, capsys, monkeypatch):
        prd = _write(tmp_path, "prd.md", "# PRD\n")

        def boom(self, prd):
            raise RuntimeError("fabric exploded")

        monkeypatch.setattr(
            "merged_agentic_swarm.tools.agentic_orchestrator.MultiLayeredAgenticOrchestrator.run_full_agentic_workflow",
            boom,
        )
        with pytest.raises(SystemExit) as exc:
            agentic_cli.cmd_run(_args(prd=str(prd)))
        assert exc.value.code == 1
        assert "ERROR: Workflow failed" in capsys.readouterr().out

    def test_run_profile_resolves_and_passes_ramp_and_model(self, tmp_path, capsys, monkeypatch):
        """`run --profile review` resolves the profile's waves as the ramp and the
        tier-resolved model alias, then forwards both to the orchestrator."""
        from merged_agentic_swarm.services import resolve_model_alias_for_profile

        prd = _write(tmp_path, "prd.md", "# PRD\n")
        captured = {}

        def fake_run(self, prd, **kwargs):
            captured.update(kwargs)
            return {"status": "completed", "waves_completed": 4, "cold_path": {}}

        monkeypatch.setattr(
            "merged_agentic_swarm.tools.agentic_orchestrator.MultiLayeredAgenticOrchestrator.run_full_agentic_workflow",
            fake_run,
        )
        _patch_auto_save(monkeypatch)
        result = agentic_cli.cmd_run(_args(prd=str(prd), profile="review"))
        out = capsys.readouterr().out
        assert result["status"] == "completed"
        assert captured["ramp_sequence"] == [4, 8]
        assert captured["default_model"] == resolve_model_alias_for_profile("review")
        assert "Using swarm profile: review" in out
        assert "[4, 8]" in out
        assert captured["default_model"] in out

    def test_run_unknown_profile_exits(self, tmp_path, capsys):
        prd = _write(tmp_path, "prd.md", "# PRD\n")
        with pytest.raises(SystemExit) as exc:
            agentic_cli.cmd_run(_args(prd=str(prd), profile="no-such-profile"))
        assert exc.value.code == 1
        assert "Unknown swarm profile" in capsys.readouterr().out

    def test_run_profile_through_main(self, tmp_path, capsys, monkeypatch):
        """argparse wires `run --profile patch` into cmd_run with profile resolved."""
        prd = _write(tmp_path, "prd.md", "# PRD\n")
        captured = {}

        def fake_run(self, prd, **kwargs):
            captured.update(kwargs)
            return {"status": "completed", "waves_completed": 4, "cold_path": {}}

        monkeypatch.setattr(
            "merged_agentic_swarm.tools.agentic_orchestrator.MultiLayeredAgenticOrchestrator.run_full_agentic_workflow",
            fake_run,
        )
        _patch_auto_save(monkeypatch)
        _main_with_args(["run", "--prd", str(prd), "--profile", "patch"])
        assert captured["ramp_sequence"] == [4]
        out = capsys.readouterr().out
        assert "Using swarm profile: patch" in out


class TestCmdStatus:
    def _registry(self, tmp_path):
        reg = tmp_path / "docs" / "agentic" / "registry"
        reg.mkdir(parents=True, exist_ok=True)
        return reg

    def _ledger(self, n_logs=3, n_markers=2, wave_ids=(1, 2, 4)):
        logs = [
            {
                "entry_id": f"LOG-{i + 1:05d}",
                "task_id": f"EPIC-{i}",
                "subtask_id": None,
                "worker_id": f"orchestrator-wave-{i % 4}",
                "wave_id": wave_ids[i] if i < len(wave_ids) else 0,
                "action": "synthesis_completed" if i % 2 else "testing",
                "status": "completed",
                "timestamp": 1700000000 + i,
            }
            for i in range(n_logs)
        ]
        markers = [
            {
                "id": f"MARKER-{i + 1:04d}",
                "task_id": "TASK-01",
                "verifier_name": "V",
                "command_executed": "cmd",
                "exit_code": 0,
                "output_summary": "ok",
                "timestamp": 1700000000 + i,
            }
            for i in range(n_markers)
        ]
        return {"logs": logs, "success_markers": markers, "task_master_snapshot": {"title": "Test PRD"}}

    def test_status_no_progress(self, tmp_path, capsys, monkeypatch):
        monkeypatch.setattr(agentic_cli, "_REPO_ROOT", tmp_path)
        monkeypatch.setattr(agentic_cli, "_progress_ledger_path", lambda: str(tmp_path / "none.json"))
        agentic_cli.cmd_status(_args())
        out = capsys.readouterr().out
        assert "No progress ledger found" in out

    def test_status_with_ledger_and_registries(self, tmp_path, capsys, monkeypatch):
        reg = self._registry(tmp_path)
        ledger_path = _write(tmp_path, "ledger.json", json.dumps(self._ledger()))
        (reg / "knowledge.jsonl").write_text("a\nb\n", encoding="utf-8")
        (reg / "agents.jsonl").write_text("x\n", encoding="utf-8")
        (reg / "chain.jsonl").write_text("", encoding="utf-8")
        _write(tmp_path, ".taskmaster/tasks/spawn_chain_registry.json", json.dumps([1, 2]))
        monkeypatch.setattr(agentic_cli, "_REPO_ROOT", tmp_path)
        monkeypatch.setattr(agentic_cli, "_progress_ledger_path", lambda: str(ledger_path))
        agentic_cli.cmd_status(_args())
        out = capsys.readouterr().out
        assert "3 log entries, 2 success markers" in out
        assert "completed=3, failed=0" in out
        assert "Test PRD" in out
        assert "knowledge.jsonl: 2 entries" in out
        assert "agents.jsonl: 1 entries" in out
        assert "chain.jsonl: 0 entries" in out
        assert "spawn_chain_registry: 2 entries" in out

    def test_status_corrupt_ledger(self, tmp_path, capsys, monkeypatch):
        self._registry(tmp_path)
        bad = _write(tmp_path, "ledger.json", "{not json")
        monkeypatch.setattr(agentic_cli, "_REPO_ROOT", tmp_path)
        monkeypatch.setattr(agentic_cli, "_progress_ledger_path", lambda: str(bad))
        agentic_cli.cmd_status(_args())
        out = capsys.readouterr().out
        assert "ERROR reading progress ledger" in out

    def test_status_custom_progress_path(self, tmp_path, capsys, monkeypatch):
        p = _write(tmp_path, "alt.json", json.dumps(self._ledger(n_logs=1, n_markers=1, wave_ids=(3,))))
        monkeypatch.setattr(agentic_cli, "_REPO_ROOT", tmp_path)
        agentic_cli.cmd_status(_args(progress=str(p)))
        out = capsys.readouterr().out
        assert "1 log entries, 1 success markers" in out
        assert "Waves covered:     3" in out

    def test_status_legacy_snapshot_still_renders(self, tmp_path, capsys, monkeypatch):
        """Old progress.json snapshots passed via --progress keep working."""
        p = _write(
            tmp_path,
            "legacy.json",
            json.dumps(
                {
                    "overall_completion_pct": 63,
                    "phase_status": {"W1": {"completion_pct": 100, "color": "green", "status": "done"}},
                    "blockers": ["a long blocker message that should be truncated"],
                    "milestone_history": [{"milestone": "M1", "status": "achieved"}],
                }
            ),
        )
        monkeypatch.setattr(agentic_cli, "_REPO_ROOT", tmp_path)
        agentic_cli.cmd_status(_args(progress=str(p)))
        out = capsys.readouterr().out
        assert "Overall completion: 63%" in out
        assert "W1: 100%" in out
        assert "Milestones (1):" in out

    def test_status_defaults_to_real_ledger(self):
        """#19: cmd_status must point at the live ProgressLedgerService ledger."""
        from merged_agentic_swarm.services.progress_ledger_service import default_progress_ledger

        assert agentic_cli._progress_ledger_path() == default_progress_ledger.ledger_file
        assert agentic_cli._progress_ledger_path().endswith("progress_ledger.json")


class TestCmdPromote:
    def test_promote_success(self, tmp_path, capsys, monkeypatch):
        reg = tmp_path / "docs" / "agentic" / "registry"
        reg.mkdir(parents=True, exist_ok=True)
        (reg / "knowledge.jsonl").write_text("k\n", encoding="utf-8")
        (reg / "agents.jsonl").write_text("", encoding="utf-8")
        (reg / "chain.jsonl").write_text("c\n", encoding="utf-8")
        monkeypatch.setattr(agentic_cli, "_REPO_ROOT", tmp_path)
        monkeypatch.setattr(
            "merged_agentic_swarm.tools.agentic_orchestrator.MultiLayeredAgenticOrchestrator._promote_cold_path",
            lambda self, phase_label=None: {"promoted_knowledge": 3, "promoted_agents": 1},
        )
        agentic_cli.cmd_promote(_args())
        out = capsys.readouterr().out
        assert "Promoted: 3 knowledge, 1 agents" in out
        assert "knowledge.jsonl: 1 entries" in out

    def test_promote_exception_exits(self, tmp_path, capsys, monkeypatch):
        monkeypatch.setattr(agentic_cli, "_REPO_ROOT", tmp_path)
        monkeypatch.setattr(
            "merged_agentic_swarm.tools.agentic_orchestrator.MultiLayeredAgenticOrchestrator._promote_cold_path",
            lambda self, phase_label=None: (_ for _ in ()).throw(RuntimeError("promote boom")),
        )
        with pytest.raises(SystemExit) as exc:
            agentic_cli.cmd_promote(_args())
        assert exc.value.code == 1
        assert "ERROR: Promotion failed" in capsys.readouterr().out


class TestMain:
    def test_no_command_prints_help_and_exits(self, capsys):
        with pytest.raises(SystemExit) as exc:
            _main_with_args([])
        assert exc.value.code == 1
        out = capsys.readouterr().out
        assert "usage" in out.lower()

    def test_run_missing_prd_exits_through_main(self, tmp_path, capsys):
        with pytest.raises(SystemExit) as exc:
            _main_with_args(["run", "--prd", str(tmp_path / "gone.md")])
        assert exc.value.code == 1

    def test_config_routes_through_main(self, capsys):
        _main_with_args(["config"])
        out = capsys.readouterr().out
        assert "Key Pool" in out


def _ledger_json(logs, snapshot=None):
    return {
        "logs": logs,
        "success_markers": [
            {"id": "MARKER-0001", "task_id": "EPIC-1", "verifier_name": "V", "timestamp": 1700000000.0}
        ],
        "task_master_snapshot": snapshot or {"title": "Test PRD", "epics": []},
    }


def _ledger_log(entry_id, task_id, wave_id, action, status, model=None, tokens=0):
    return {
        "entry_id": entry_id,
        "task_id": task_id,
        "subtask_id": None,
        "worker_id": "w1",
        "wave_id": wave_id,
        "action": action,
        "status": status,
        "timestamp": 1700000000.0,
        "tokens_used": tokens,
        "model": model,
    }


class TestCmdProviders:
    def _setup(self, tmp_path, monkeypatch):
        from merged_agentic_swarm.providers.key_pool import KeyPoolManager

        env = tmp_path / "env.txt"
        env.write_text("GEMINI_API_KEY=test-gemini-key\nGROQ_API_KEY=test-groq-key\n", encoding="utf-8")
        monkeypatch.setattr(
            "merged_agentic_swarm.providers.key_pool.default_key_pool", KeyPoolManager(env_file_path=str(env))
        )
        monkeypatch.setattr(
            "merged_agentic_swarm.providers.multi_provider_fabric.MODEL_FABRIC_ROUTES",
            {"claude-3-7-sonnet": [{"provider": "gemini", "model": "gemini-2.5-flash", "url": "https://x"}]},
        )
        reg = tmp_path / "docs" / "agentic" / "providers"
        reg.mkdir(parents=True, exist_ok=True)
        (reg / "PROVIDER_REGISTRY.json").write_text(
            json.dumps(
                {
                    "backends": {
                        "litellm": {
                            "base_url": "http://localhost:4000/v1/chat/completions",
                            "auth_env": "LITELLM_PROXY_KEY",
                            "status": "available",
                        }
                    }
                }
            ),
            encoding="utf-8",
        )
        monkeypatch.setattr(agentic_cli, "_REPO_ROOT", tmp_path)

    def test_providers_renders_key_names_env_names_and_routes(self, tmp_path, capsys, monkeypatch):
        self._setup(tmp_path, monkeypatch)
        agentic_cli.cmd_providers(None)
        out = capsys.readouterr().out
        assert "gemini-1" in out
        assert "groq-main" in out
        assert "LITELLM_PROXY_KEY" in out
        assert "gemini-2.5-flash" in out

    def test_providers_never_leaks_key_values(self, tmp_path, capsys, monkeypatch):
        self._setup(tmp_path, monkeypatch)
        agentic_cli.cmd_providers(None)
        out = capsys.readouterr().out
        assert "test-gemini-key" not in out
        assert "test-groq-key" not in out

    def test_providers_through_main(self, tmp_path, capsys, monkeypatch):
        self._setup(tmp_path, monkeypatch)
        _main_with_args(["providers"])
        out = capsys.readouterr().out
        assert "PROVIDER & PROXY INVENTORY" in out


class TestCmdReport:
    def _write_ledger(self, tmp_path, model="gemini-2.5-flash"):
        return _write(
            tmp_path,
            "ledger.json",
            json.dumps(_ledger_json([_ledger_log("LOG-00001", "EPIC-1", 1, "testing", "completed", model=model)])),
        )

    def test_report_writes_both_files_with_model_timeline(self, tmp_path, capsys, monkeypatch):
        ledger = self._write_ledger(tmp_path)
        monkeypatch.setattr(agentic_cli, "_REPO_ROOT", tmp_path)
        out_dir = tmp_path / "reports"
        saved = agentic_cli.cmd_report(_args(ledger=str(ledger), out=str(out_dir)))
        out = capsys.readouterr().out
        assert "RUN REPORT" in out
        assert "gemini-2.5-flash" in out
        assert saved["json_path"].exists() and saved["md_path"].exists()
        parsed = json.loads(saved["json_path"].read_text(encoding="utf-8"))
        assert parsed["timeline"][0]["model"] == "gemini-2.5-flash"
        assert "## Timeline" in saved["md_path"].read_text(encoding="utf-8")

    def test_report_missing_ledger_writes_empty_report(self, tmp_path, capsys, monkeypatch):
        monkeypatch.setattr(agentic_cli, "_REPO_ROOT", tmp_path)
        out_dir = tmp_path / "reports"
        saved = agentic_cli.cmd_report(_args(ledger=str(tmp_path / "missing.json"), out=str(out_dir)))
        assert saved["json_path"].exists() and saved["md_path"].exists()

    def test_report_through_main(self, tmp_path, capsys, monkeypatch):
        ledger = self._write_ledger(tmp_path, model=None)
        monkeypatch.setattr(agentic_cli, "_REPO_ROOT", tmp_path)
        _main_with_args(["report", "--ledger", str(ledger), "--out", str(tmp_path / "reports")])
        out = capsys.readouterr().out
        assert "RUN REPORT" in out
        assert "## Timeline" in out


class TestCmdRunAutoSave:
    def test_run_auto_saves_report_on_success(self, tmp_path, capsys, monkeypatch):
        prd = _write(tmp_path, "prd.md", "# PRD\n")

        def fake_run(self, prd):
            return {"status": "success", "waves_completed": 4}

        monkeypatch.setattr(
            "merged_agentic_swarm.tools.agentic_orchestrator.MultiLayeredAgenticOrchestrator.run_full_agentic_workflow",
            fake_run,
        )
        _patch_auto_save(monkeypatch, _fake_saved(md_path="reports/fake.md", json_path="reports/fake.json"))
        agentic_cli.cmd_run(_args(prd=str(prd)))
        out = capsys.readouterr().out
        assert "Report:          reports/fake.md" in out
        assert "Report JSON:     reports/fake.json" in out

    def test_run_does_not_autosave_on_failure(self, tmp_path, capsys, monkeypatch):
        prd = _write(tmp_path, "prd.md", "# PRD\n")

        def fake_run(self, prd):
            return {"status": "failed", "reason": "gate"}

        monkeypatch.setattr(
            "merged_agentic_swarm.tools.agentic_orchestrator.MultiLayeredAgenticOrchestrator.run_full_agentic_workflow",
            fake_run,
        )
        agentic_cli.cmd_run(_args(prd=str(prd)))
        out = capsys.readouterr().out
        assert "Report:" not in out


class TestCmdSwarm:
    """Coverage for the swarm subcommand: --list, --profile, and error paths."""

    def setup_method(self):
        from merged_agentic_swarm.services import swarm_profiles

        swarm_profiles._profiles_cache = None

    def _swarm_args(self, profile=None, list_profiles=False):
        class Args:
            pass

        a = Args()
        a.profile = profile
        a.list_profiles = list_profiles
        return a

    def test_swarm_list_through_main(self, capsys):
        _main_with_args(["swarm", "--list"])
        out = capsys.readouterr().out
        assert "SWARM PROFILES" in out
        assert "build" in out
        assert "learning" in out
        assert "gemini-batch" in out  # deep-tier default alias for build
        assert "fast-flash" in out  # fast-tier default alias for review/patch

    def test_swarm_profile_through_main(self, capsys):
        _main_with_args(["swarm", "--profile", "build"])
        out = capsys.readouterr().out
        assert "SWARM PROFILE: build" in out
        assert "[4, 8, 16, 24, 40]" in out
        assert "gemini-batch" in out
        assert "agentic-cli run" in out

    def test_swarm_learning_profile_reports_no_runnable_waves(self, capsys):
        _main_with_args(["swarm", "--profile", "learning"])
        out = capsys.readouterr().out
        assert "SWARM PROFILE: learning" in out
        assert "no worker waves" in out

    def test_swarm_unknown_profile_errors_clearly(self, capsys):
        with pytest.raises(SystemExit) as exc:
            _main_with_args(["swarm", "--profile", "no-such-profile"])
        assert exc.value.code == 1
        assert "Unknown swarm profile" in capsys.readouterr().out

    def test_swarm_without_args_errors(self, capsys):
        with pytest.raises(SystemExit) as exc:
            _main_with_args(["swarm"])
        assert exc.value.code == 1
        assert "specify --profile" in capsys.readouterr().out

    def test_swarm_handler_returns_resolved_profile(self, capsys):
        profile = agentic_cli.cmd_swarm(self._swarm_args(profile="patch"))
        out = capsys.readouterr().out
        assert profile["waves"] == [4]
        assert profile["default_tier"] == "fast"
        assert "Quick targeted patch" in out
        assert "fast-flash" in out
        assert "Gates:         False" in out
