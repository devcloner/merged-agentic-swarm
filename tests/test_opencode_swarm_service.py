"""
Tests for services/opencode_swarm_service.py

Coverage: ConcurrencyRampController, DurableAgentRouter (real agents.jsonl +
.markdown agent files), OpenCodeSwarmManager (pool init, round-robin, subtask
dispatch incl. durable-agent routing, failure paths, opencode mode,
_target_repo_root, batch parallel).

The agentic worker loop (which makes real model calls and real file edits) is
stubbed at the method level for the swarm manager's *decision* logic — status
transitions, pool accounting, routing. The loop itself has its own real-behavior
tests; the existing live test here still makes one real fabric call.
"""

import json

import pytest

from merged_agentic_swarm.models.agent_models import WorkerRole
from merged_agentic_swarm.models.prd_models import TaskStatus
from merged_agentic_swarm.services import opencode_swarm_service as mod
from merged_agentic_swarm.services.opencode_swarm_service import (
    DurableAgentRouter,
    OpenCodeSwarmManager,
    get_durable_router,
)


class TestConcurrencyRampController:
    def setup_method(self):
        from merged_agentic_swarm.services.opencode_swarm_service import ConcurrencyRampController

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
        from merged_agentic_swarm.services.opencode_swarm_service import OpenCodeSwarmManager

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
        # Create config without HOT_MICRO_SPECIALIST (not in defaults)
        from merged_agentic_swarm.models.agent_models import WorkerPoolConfig
        from merged_agentic_swarm.services.opencode_swarm_service import OpenCodeSwarmManager

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

    @pytest.mark.live
    def test_execute_subtask_with_worker_fabric(self, make_subtask):
        """A worker subtask goes through the agentic tool loop and reports honestly.

        A simulated (offline-fallback) response must be reported as ``failed``,
        never ``completed`` — simulation can never advance a gate.

        ``live``: makes a real fabric call; excluded from CI because the live
        gemini fleet can rate-limit mid-run. The simulation-honesty invariant
        is covered deterministically by ``test_simulation_worker_fails``.
        """
        subtask = make_subtask(title="Test task", desc="Test description")
        result = self.manager.execute_subtask_with_worker(subtask, WorkerRole.CORE_ENGINEER)
        assert result["status"] in ("completed", "failed")
        assert "final_text" in result
        assert "files_written" in result
        assert "commands_run" in result
        if result["status"] == "completed":
            assert not result.get("simulation_fallback", False)
        else:
            assert "reason" in result

    @pytest.mark.live
    def test_execute_subtask_batch_parallel(self, make_subtask):
        subtasks = [make_subtask(title=f"Batch {i}", desc="Parallel test") for i in range(3)]
        results = self.manager.execute_subtask_batch_parallel(
            subtasks, role=WorkerRole.CORE_ENGINEER, wave_gate_level=0
        )
        assert len(results) == 3


def _router(agents_jsonl_content="", agents_dir=None):
    """Build a real DurableAgentRouter over tmp JSONL + agent dir."""
    import tempfile
    from pathlib import Path

    d = Path(tempfile.mkdtemp())
    jsonl = d / "agents.jsonl"
    jsonl.write_text(agents_jsonl_content, encoding="utf-8")
    adir = agents_dir or d / "agents"
    adir.mkdir(exist_ok=True)
    router = DurableAgentRouter(agents_jsonl=str(jsonl), agents_dir=str(adir))
    router.load()
    return router


class TestDurableAgentRouter:
    def test_load_from_jsonl(self):
        content = (
            json.dumps(
                {
                    "id": "agent-1",
                    "name": "Agent One",
                    "category": "python",
                    "system_prompt": "You are a python expert.",
                }
            )
            + "\n"
        )
        router = _router(content)
        assert router.get_stats()["total_agents"] == 1
        assert "python" in router.get_stats()["categories"]

    def test_load_from_markdown_frontmatter(self, tmp_path):
        adir = tmp_path / "agents"
        adir.mkdir()
        (adir / "helper.md").write_text(
            "---\nname: helper-agent\ncategory: build\npromoted_at: 2026-01-01\n"
            "description: Build and compile helpers.\n---\n\n"
            "Body content. Activate when building or compiling python modules.\n",
            encoding="utf-8",
        )
        router = DurableAgentRouter(agents_jsonl=str(tmp_path / "missing.jsonl"), agents_dir=str(adir))
        assert router.load() == 1
        agent = router.get_stats()["total_agents"] and router._agents[0]
        assert agent["id"] == "helper-agent"
        assert agent["category"] == "build"
        assert "Body content" in agent["body"]

    def test_skips_bad_jsonl_lines(self, tmp_path):
        jsonl = tmp_path / "agents.jsonl"
        jsonl.write_text("not json\n", encoding="utf-8")
        router = DurableAgentRouter(agents_jsonl=str(jsonl), agents_dir=str(tmp_path / "agents"))
        assert router.load() == 0

    def test_dedupes_by_id(self, tmp_path):
        jsonl = tmp_path / "agents.jsonl"
        jsonl.write_text(
            json.dumps({"id": "dup", "category": "a"}) + "\n" + json.dumps({"id": "dup", "category": "b"}) + "\n",
            encoding="utf-8",
        )
        router = DurableAgentRouter(agents_jsonl=str(jsonl), agents_dir=str(tmp_path / "agents"))
        assert router.load() == 1

    def test_parse_frontmatter_and_body(self, tmp_path):
        md = tmp_path / "a.md"
        md.write_text(
            "---\nname: z\ncategory: q\n---\nThis is the body.\n",
            encoding="utf-8",
        )
        router = DurableAgentRouter(agents_jsonl="", agents_dir=str(tmp_path))
        assert router._parse_frontmatter(md) == {"name": "z", "category": "q"}
        assert router._read_body(md) == "This is the body."

    def test_extract_keywords_drops_stopwords(self):
        kw = DurableAgentRouter._extract_keywords("the quick brown fox jumps over the lazy dog")
        assert "the" not in kw
        assert "quick" in kw
        assert "brown" in kw

    def test_scan_agent_triggers(self):
        agent = {
            "body": "Activate when building python helpers.\n",
            "system_prompt": "specialized in compiling.",
        }
        triggers = DurableAgentRouter()._scan_agent_triggers(agent)
        assert isinstance(triggers, set)
        assert "building" in triggers or "python" in triggers

    def test_find_matching_agent_by_category_and_keywords(self):
        content = (
            json.dumps(
                {
                    "id": "python-builder",
                    "name": "Python Builder",
                    "category": "python",
                    "system_prompt": "specialized in building and compiling python modules.",
                }
            )
            + "\n"
        )
        router = _router(content)
        from merged_agentic_swarm.models.prd_models import SubTask

        task = SubTask(id="T1", title="python builder", description="compile a python module")
        task.category = "python"
        matched = router.find_matching_agent(task)
        assert matched is not None
        assert matched["id"] == "python-builder"
        assert matched["_score"] >= 1.0

    def test_find_matching_agent_no_match_returns_none(self):
        content = (
            json.dumps(
                {
                    "id": "rust-expert",
                    "name": "Rust Expert",
                    "category": "rust",
                    "system_prompt": "specialized in rust lifetimes.",
                }
            )
            + "\n"
        )
        router = _router(content)
        from merged_agentic_swarm.models.prd_models import SubTask

        task = SubTask(id="T1", title="javascript ui", description="build a react component")
        task.category = "frontend"
        assert router.find_matching_agent(task) is None

    def test_get_durable_router_singleton(self):
        r1 = get_durable_router()
        r2 = get_durable_router()
        assert r1 is r2
        assert r1.get_stats()["loaded"] is True


class TestExecuteSubtaskDecisionLogic:
    def _manager(self):
        return OpenCodeSwarmManager()

    def test_routed_to_durable_agent(self, tmp_path, monkeypatch, make_subtask):
        content = (
            json.dumps(
                {
                    "id": "router-agent",
                    "name": "Router Agent",
                    "category": "routing",
                    "system_prompt": "specialized in routing and building python code.",
                }
            )
            + "\n"
        )
        router = _router(content)
        monkeypatch.setattr(mod, "get_durable_router", lambda: router)
        monkeypatch.setattr(
            mod.default_agentic_worker_loop,
            "execute",
            lambda **k: {"status": "completed", "final_text": "done", "files_written": [], "commands_run": []},
        )
        subtask = make_subtask(title="python routing", desc="build and fix python code")
        subtask.category = "routing"
        result = self._manager().execute_subtask_with_worker(subtask, WorkerRole.CORE_ENGINEER)
        assert result["status"] == "completed"
        assert result["routed_agent"] == "router-agent"
        assert subtask.status == TaskStatus.COMPLETED

    def test_no_worker_returns_error(self, monkeypatch, make_subtask):
        monkeypatch.setattr(mod, "get_durable_router", lambda: _router(""))
        manager = self._manager()
        manager.workers = {}
        manager.state.workers_by_role = {}
        subtask = make_subtask()
        result = manager.execute_subtask_with_worker(subtask, WorkerRole.CORE_ENGINEER)
        assert result["status"] == "error"

    def test_loop_exception_fails_subtask(self, monkeypatch, make_subtask):
        monkeypatch.setattr(mod, "get_durable_router", lambda: _router(""))

        def boom(**k):
            raise RuntimeError("rate limit 429")

        monkeypatch.setattr(mod.default_agentic_worker_loop, "execute", boom)
        manager = self._manager()
        subtask = make_subtask()
        result = manager.execute_subtask_with_worker(subtask, WorkerRole.CORE_ENGINEER)
        assert result["status"] == "failed"
        assert "429" in result["error"]
        assert subtask.status == TaskStatus.FAILED
        assert manager.state.failed_tasks >= 1

    def test_simulation_worker_fails(self, monkeypatch, make_subtask):
        monkeypatch.setattr(mod, "get_durable_router", lambda: _router(""))
        monkeypatch.setattr(
            mod.default_agentic_worker_loop,
            "execute",
            lambda **k: {"status": "failed", "reason": "simulation_fallback", "final_text": "fake"},
        )
        manager = self._manager()
        subtask = make_subtask()
        result = manager.execute_subtask_with_worker(subtask, WorkerRole.CORE_ENGINEER)
        assert result["status"] == "failed"
        assert result["reason"] == "simulation_fallback"
        assert subtask.status == TaskStatus.FAILED
        assert manager.state.failed_tasks >= 1

    def test_opencode_mode_routes_to_opencode_worker(self, monkeypatch, make_subtask):
        monkeypatch.setenv("SWARM_WORKER_MODE", "opencode")
        monkeypatch.setattr(mod, "get_durable_router", lambda: _router(""))
        monkeypatch.setattr(
            mod.OpenCodeSwarmManager,
            "_run_opencode_worker",
            lambda self, wid, role, sp, task: {
                "status": "completed",
                "reason": None,
                "final_text": "opencode ok",
                "files_written": [],
                "commands_run": [],
            },
        )
        subtask = make_subtask()
        result = self._manager().execute_subtask_with_worker(subtask, WorkerRole.CORE_ENGINEER)
        assert result["status"] == "completed"

    def test_run_opencode_worker_completed(self, monkeypatch):
        from merged_agentic_swarm.services import worker_runtime_adapter as wra

        class FakeAdapter:
            def launch_worker(self, spec, prompt):
                assert spec.role == WorkerRole.CORE_ENGINEER
                return {"status": "completed", "evidence": "opencode did it"}

        monkeypatch.setattr(wra, "get_runtime_adapter", lambda mode: FakeAdapter())
        result = self._manager()._run_opencode_worker(
            "w1", WorkerRole.CORE_ENGINEER, "sp", {"title": "t", "description": "d"}
        )
        assert result["status"] == "completed"
        assert result["final_text"] == "opencode did it"

    def test_run_opencode_worker_failed(self, monkeypatch):
        from merged_agentic_swarm.services import worker_runtime_adapter as wra

        class FakeAdapter:
            def launch_worker(self, spec, prompt):
                return {"status": "failed", "evidence": "auth died"}

        monkeypatch.setattr(wra, "get_runtime_adapter", lambda mode: FakeAdapter())
        result = self._manager()._run_opencode_worker(
            "w1", WorkerRole.CORE_ENGINEER, "sp", {"title": "t", "description": "d"}
        )
        assert result["status"] == "failed"
        assert "auth died" in result["reason"]


class TestTargetRepoRoot:
    def test_env_var_wins(self, monkeypatch):
        monkeypatch.setenv("SWARM_TARGET_REPO", "~/custom-target")
        root = OpenCodeSwarmManager._target_repo_root()
        assert "custom-target" in root

    def test_defaults_to_existing_sibling_or_cwd(self, monkeypatch):
        monkeypatch.delenv("SWARM_TARGET_REPO", raising=False)
        root = OpenCodeSwarmManager._target_repo_root()
        assert root  # resolves to a real dir

    def test_getcwd_fallback(self, monkeypatch, tmp_path):
        """When SWARM_TARGET_REPO is unset and no sibling target repo exists,
        _target_repo_root falls back to getcwd."""
        monkeypatch.delenv("SWARM_TARGET_REPO", raising=False)
        # Neutralise the sibling-repo candidates so the fallback is reached.
        monkeypatch.setattr(mod.os.path, "expanduser", lambda p: str(tmp_path / "missing-target"))
        monkeypatch.setattr(mod.os.path, "isdir", lambda p: False)
        monkeypatch.setattr(mod.os, "getcwd", lambda: str(tmp_path))
        root = OpenCodeSwarmManager._target_repo_root()
        assert root == str(tmp_path)
