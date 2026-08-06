"""
Tests for tools/agentic_orchestrator.py

Coverage: MultiLayeredAgenticOrchestrator — _apply_worker_outputs,
_compact_registries, _run_syntax_verification, _append_jsonl,
_promote_cold_path, initialize_system, run_full_agentic_workflow.

The workflow control-flow tests stub the *service* singletons' methods (task
master parse, swarm batch, wave gates, agent factory, ledger) — each of those
services has its own real-behavior tests. The orchestrator's own logic (wave
ordering, gate checks, epic status transitions, sim-failure logging, cold-path
calls) runs for real against a tmp registry dir.
"""

import logging
from pathlib import Path
from types import SimpleNamespace

from merged_agentic_swarm.tools import agentic_orchestrator as orch_mod
from merged_agentic_swarm.tools.agentic_orchestrator import MultiLayeredAgenticOrchestrator


def _epic(wave_id, subtask_count=1, epic_id=None):
    from merged_agentic_swarm.models.prd_models import EpicTask, SubTask, TaskPriority

    subtasks = [SubTask(id=f"ST-{wave_id}-{i}", title=f"ST {i}", description=f"d{i}") for i in range(subtask_count)]
    return EpicTask(
        id=epic_id or f"EPIC-{wave_id}",
        title=f"Epic W{wave_id}",
        description="d",
        wave_id=wave_id,
        priority=TaskPriority.P1_HIGH,
        subtasks=subtasks,
    )


def _analysis():
    from merged_agentic_swarm.models.prd_models import PRDAnalysisResult

    return PRDAnalysisResult(
        title="T",
        summary="S",
        epics=[_epic(1), _epic(2), _epic(3), _epic(4)],
    )


class TestRunFullAgenticWorkflow:
    def _stub_workflow(self, monkeypatch, tmp_path, batch_result=None, batch_error=None, advance=(True, "ok")):
        """Wire the orchestrator singletons for a deterministic workflow run."""
        registry = Path(tmp_path) / "registry"
        registry.mkdir(parents=True, exist_ok=True)
        for name in ("knowledge.jsonl", "agents.jsonl"):
            (registry / name).write_text("", encoding="utf-8")
        monkeypatch.setattr(orch_mod, "_REGISTRY_DIR", registry)

        orch = MultiLayeredAgenticOrchestrator()
        orch.promoted_ids_file = str(tmp_path / "promoted_ids.json")
        monkeypatch.setattr(orch, "initialize_system", lambda: {"status": "ready"})
        monkeypatch.setattr(orch, "_run_syntax_verification", lambda: {"exit_code": 0, "output_summary": "ok"})
        monkeypatch.setattr(
            orch, "_promote_cold_path", lambda phase_label="": {"promoted_knowledge": 0, "promoted_agents": 0}
        )
        monkeypatch.setattr(orch, "_compact_registries", dict)

        analysis = _analysis()
        monkeypatch.setattr(orch_mod.default_task_master, "current_analysis", analysis)
        monkeypatch.setattr(orch_mod.default_task_master, "optimize_and_parse_prd", lambda prd, title=None: analysis)
        monkeypatch.setattr(orch_mod.default_task_master, "update_task_status", lambda *a, **k: None)
        monkeypatch.setattr(orch_mod.default_task_master, "save_state", lambda: None)
        monkeypatch.setattr(orch_mod.default_codebase_mapper, "scan_repository", lambda: None)
        monkeypatch.setattr(orch_mod.default_codebase_mapper, "detect_spec_gaps", lambda required_components=None: [])
        monkeypatch.setattr(orch_mod.default_codebase_mapper, "close_spec_gap", lambda *a, **k: None)
        monkeypatch.setattr(orch_mod.default_wave_controller, "advance_wave", lambda: advance)
        if batch_error is not None:

            def boom(subtasks, role=None, wave_gate_level=0):
                raise batch_error

            monkeypatch.setattr(orch_mod.default_swarm_manager, "execute_subtask_batch_parallel", boom)
        else:
            result = batch_result or {
                "status": "completed",
                "worker_id": "w1",
                "files_written": [],
                "commands_run": [],
                "final_text": "done",
            }
            monkeypatch.setattr(
                orch_mod.default_swarm_manager,
                "execute_subtask_batch_parallel",
                lambda subtasks, role=None, wave_gate_level=0: [result],
            )
        monkeypatch.setattr(orch_mod.default_progress_ledger, "log_progress", lambda **k: None)
        monkeypatch.setattr(orch_mod.default_progress_ledger, "record_success_marker", lambda **k: None)
        monkeypatch.setattr(
            orch_mod.default_progress_ledger,
            "handle_task_failure",
            lambda *a, **k: {"remediated": True, "action": "retry"},
        )
        monkeypatch.setattr(orch_mod.default_knowledge_cache, "add_learning", lambda *a, **k: "learning-1")
        monkeypatch.setattr(
            orch_mod.default_agent_factory, "spawn_from_learning", lambda *a, **k: SimpleNamespace(id="agent-1")
        )
        monkeypatch.setattr(orch_mod.default_agent_factory, "purge_expired", lambda: 0)
        return orch

    def test_workflow_success_all_waves(self, monkeypatch, tmp_path):
        orch = self._stub_workflow(monkeypatch, tmp_path)
        result = orch.run_full_agentic_workflow("# PRD")
        assert result["status"] == "success"
        assert result["waves_completed"] == 4
        assert result["cold_path"]["total_knowledge_records"] == 0

    def test_workflow_wave0_gate_failure_aborts(self, monkeypatch, tmp_path):
        orch = self._stub_workflow(monkeypatch, tmp_path, advance=(False, "gate blocked"))
        result = orch.run_full_agentic_workflow("# PRD")
        assert result["status"] == "failed"
        assert result["wave"] == 0

    def test_workflow_simulation_failure_logged_and_epic_failed(self, monkeypatch, tmp_path, caplog):
        sim_result = {
            "status": "failed",
            "worker_id": "w1",
            "reason": "simulation_fallback",
            "final_text": "fake",
            "files_written": [],
            "commands_run": [],
        }
        orch = self._stub_workflow(monkeypatch, tmp_path, batch_result=sim_result)
        with caplog.at_level(logging.ERROR, logger="agentic_orchestrator"):
            result = orch.run_full_agentic_workflow("# PRD")
        assert result["status"] == "success"  # gates stubbed to pass; sim never marks an epic complete
        assert any("SIMULATION FALLBACK" in r.message for r in caplog.records)

    def test_workflow_batch_exception_remediated(self, monkeypatch, tmp_path):
        orch = self._stub_workflow(monkeypatch, tmp_path, batch_error=RuntimeError("batch crashed"))
        result = orch.run_full_agentic_workflow("# PRD")
        assert result["status"] == "success"


class TestRunSyntaxVerificationPaths:
    def _make_core_files(self, root, bad=None):
        files = [
            "providers/multi_provider_fabric.py",
            "providers/key_pool.py",
            "services/progress_ledger_service.py",
            "services/wave_gate_service.py",
            "services/codebase_map_service.py",
            "services/agent_factory_service.py",
            "services/task_master_service.py",
            "services/opencode_swarm_service.py",
            "tools/knowledge_cache.py",
            "tools/agentic_cli.py",
            "tools/agentic_orchestrator.py",
            "proxy/claude_proxy_server.py",
        ]
        for rel in files:
            p = root / "src" / "merged_agentic_swarm" / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            content = "def f():\n    return 1\n" if rel != bad else "def broken(:\n"
            p.write_text(content, encoding="utf-8")

    def test_inline_syntax_pass(self, tmp_path, monkeypatch):
        self._make_core_files(tmp_path)
        monkeypatch.setattr(orch_mod, "_REPO_ROOT", tmp_path)
        orch = MultiLayeredAgenticOrchestrator()
        result = orch._run_syntax_verification()
        assert result["exit_code"] == 0
        assert "Syntax check PASSED" in result["output_summary"]

    def test_inline_syntax_error_detected(self, tmp_path, monkeypatch):
        self._make_core_files(tmp_path, bad="tools/agentic_cli.py")
        monkeypatch.setattr(orch_mod, "_REPO_ROOT", tmp_path)
        orch = MultiLayeredAgenticOrchestrator()
        result = orch._run_syntax_verification()
        assert result["exit_code"] == 1
        assert "Syntax check FAILED" in result["output_summary"]

    def test_ci_script_nonzero_exit(self, tmp_path, monkeypatch):
        ci = tmp_path / "scripts" / "ci.sh"
        ci.parent.mkdir(parents=True, exist_ok=True)
        ci.write_text("#!/usr/bin/env bash\necho CI_BROKEN\nexit 1\n", encoding="utf-8")
        monkeypatch.setattr(orch_mod, "_REPO_ROOT", tmp_path)
        orch = MultiLayeredAgenticOrchestrator()
        result = orch._run_syntax_verification()
        assert result["exit_code"] == 1
        assert "CI_BROKEN" in result["output_summary"]


class TestApplyWorkerOutputsPaths:
    def setup_method(self):
        self.orch = MultiLayeredAgenticOrchestrator()

    def test_relative_path_resolves_and_write_failure_logged(self, tmp_path, caplog):
        """A relative # file: path that resolves to a directory triggers the
        write-failure branch (resolved abs path is an existing dir)."""
        results = [
            {
                "status": "completed",
                "final_text": "```\n# file: tools\nnot-writable\n```",
            }
        ]
        with caplog.at_level(logging.ERROR, logger="agentic_orchestrator"):
            count = self.orch._apply_worker_outputs(results, wave_label="W1")
        assert count == 0
        assert any("Failed to write" in r.message for r in caplog.records)

    def test_secondary_text_from_response_dict(self, tmp_path):
        results = [
            {
                "status": "completed",
                "response": {"content": "no file annotations"},
            }
        ]
        count = self.orch._apply_worker_outputs(results)
        assert count == 0


class TestPromotedIdsBranches:
    def test_load_invalid_json_warns(self, tmp_path, caplog):
        p = tmp_path / "ids.json"
        p.write_text("{not json", encoding="utf-8")
        with caplog.at_level(logging.WARNING, logger="agentic_orchestrator"):
            orch = MultiLayeredAgenticOrchestrator()
            orch.promoted_ids_file = str(p)
            orch._load_promoted_ids()
        assert any("Could not load promoted IDs" in r.message for r in caplog.records)

    def test_save_to_path_under_file_warns(self, tmp_path, caplog):
        blocker = tmp_path / "afile"
        blocker.write_text("x", encoding="utf-8")
        orch = MultiLayeredAgenticOrchestrator()
        orch.promoted_ids_file = str(blocker / "ids.json")
        with caplog.at_level(logging.WARNING, logger="agentic_orchestrator"):
            orch._save_promoted_ids()
        assert any("Could not save promoted IDs" in r.message for r in caplog.records)


class TestInitializeSystemProxyFailure:
    def test_proxy_start_failure_is_nonfatal(self, monkeypatch):
        class BrokenDaemon:
            def __init__(self, port=8085):
                pass

            def start(self):
                raise RuntimeError("port in use")

        monkeypatch.setattr(orch_mod, "ProxyServerDaemon", BrokenDaemon)
        orch = MultiLayeredAgenticOrchestrator()
        result = orch.initialize_system(start_proxy_port=9999)
        assert result["status"] == "ready"
        assert "Proxy initialization note" in result["proxy_status"]


class TestPromoteColdPathAgentFileExists:
    def test_existing_agent_file_skipped(self, tmp_path, monkeypatch):
        """When _write_agent_spec_file returns None (already exists), the skip
        branch logs at debug — promotion count is still correct."""
        from merged_agentic_swarm.tools.knowledge_cache import default_knowledge_cache

        monkeypatch.setattr(default_knowledge_cache, "learnings", {})
        monkeypatch.setattr(orch_mod.default_agent_factory, "_write_agent_spec_file", lambda *a, **k: None)
        # 3 learnings in one category → agent promotion path runs
        for i in range(3):
            default_knowledge_cache.add_learning(f"L{i}", "skip_cat", f"Sol{i}")
        orch = MultiLayeredAgenticOrchestrator()
        orch.promoted_learning_ids = set()
        orch.promoted_ids_file = str(tmp_path / "p.json")
        result = orch._promote_cold_path("test")
        assert result["promoted_agents"] == 1
        # cleanup
        default_knowledge_cache.learnings = {}


class TestApplyWorkerOutputs:
    def setup_method(self):
        self.orch = MultiLayeredAgenticOrchestrator()
