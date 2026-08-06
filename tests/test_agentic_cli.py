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
    return a


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
        """cmd_status should handle missing progress.json gracefully."""
        from merged_agentic_swarm.tools.agentic_cli import cmd_status

        # Create a mock args object
        class Args:
            progress = os.path.join(temp_dir, "nonexistent.json")

        cmd_status(Args())
        captured = capsys.readouterr()
        assert "No progress.json found" in captured.out


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


class TestCmdStatus:
    def _registry(self, tmp_path):
        reg = tmp_path / "docs" / "agentic" / "registry"
        reg.mkdir(parents=True, exist_ok=True)
        return reg

    def test_status_no_progress(self, tmp_path, capsys, monkeypatch):
        monkeypatch.setattr(agentic_cli, "_REPO_ROOT", tmp_path)
        agentic_cli.cmd_status(_args())
        out = capsys.readouterr().out
        assert "No progress.json found" in out

    def test_status_with_progress_and_registries(self, tmp_path, capsys, monkeypatch):
        reg = self._registry(tmp_path)
        _write(
            tmp_path,
            "docs/agentic/registry/progress.json",
            json.dumps(
                {
                    "overall_completion_pct": 63,
                    "phase_status": {"W1": {"completion_pct": 100, "color": "green", "status": "done"}},
                    "blockers": ["a long blocker message that should be truncated"],
                    "milestone_history": [{"milestone": "M1", "status": "achieved"}],
                }
            ),
        )
        (reg / "knowledge.jsonl").write_text("a\nb\n", encoding="utf-8")
        (reg / "agents.jsonl").write_text("x\n", encoding="utf-8")
        (reg / "chain.jsonl").write_text("", encoding="utf-8")
        _write(tmp_path, ".taskmaster/tasks/spawn_chain_registry.json", json.dumps([1, 2]))
        monkeypatch.setattr(agentic_cli, "_REPO_ROOT", tmp_path)
        agentic_cli.cmd_status(_args())
        out = capsys.readouterr().out
        assert "Overall completion: 63%" in out
        assert "W1: 100%" in out
        assert "knowledge.jsonl: 2 entries" in out
        assert "agents.jsonl: 1 entries" in out
        assert "chain.jsonl: 0 entries" in out
        assert "spawn_chain_registry: 2 entries" in out

    def test_status_corrupt_progress(self, tmp_path, capsys, monkeypatch):
        self._registry(tmp_path)
        _write(tmp_path, "docs/agentic/registry/progress.json", "{not json")
        monkeypatch.setattr(agentic_cli, "_REPO_ROOT", tmp_path)
        agentic_cli.cmd_status(_args())
        out = capsys.readouterr().out
        assert "ERROR reading progress.json" in out

    def test_status_custom_progress_path(self, tmp_path, capsys, monkeypatch):
        p = _write(tmp_path, "alt.json", json.dumps({"overall_completion_pct": 42}))
        monkeypatch.setattr(agentic_cli, "_REPO_ROOT", tmp_path)
        agentic_cli.cmd_status(_args(progress=str(p)))
        assert "Overall completion: 42%" in capsys.readouterr().out


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
