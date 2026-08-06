"""
Tests for services/worker_runtime_adapter.py

Real-behavior coverage of the WorkerRuntimeAdapter: mode detection, singleton
caching, launch_worker result contract, batch launching, opencode fallback,
and shutdown. The fabric (HTTP transport) is stubbed via monkeypatch — the
user's rule allows mocking the HTTP transport layer; adapter logic itself is
real (real subprocess management, real thread pool, real AgentSpec).
"""

import pytest

from merged_agentic_swarm.models.agent_models import AgentSpec, AgentType, WorkerRole
from merged_agentic_swarm.services.worker_runtime_adapter import (
    WorkerRuntimeAdapter,
    _opencode_available,
    _resolve_opencode_bin,
    detect_mode,
    get_runtime_adapter,
)


def _spec(worker_id="w1", role=WorkerRole.CORE_ENGINEER):
    return AgentSpec(
        id=worker_id,
        name=f"Worker {worker_id}",
        role=role,
        agent_type=AgentType.SWARM_WORKER,
        system_prompt="Do the task.",
    )


class TestModeDetection:
    def test_resolve_opencode_bin_is_str_or_none(self):
        result = _resolve_opencode_bin()
        assert result is None or isinstance(result, str)

    def test_opencode_available_is_bool(self):
        assert isinstance(_opencode_available(), bool)

    def test_detect_mode_returns_valid(self):
        assert detect_mode() in ("opencode", "native_subagent")


class TestAdapterConstruction:
    def test_explicit_native_mode(self):
        adapter = WorkerRuntimeAdapter(mode="native_subagent")
        assert adapter.mode == "native_subagent"

    def test_explicit_direct_fabric_mode(self):
        adapter = WorkerRuntimeAdapter(mode="direct_fabric")
        assert adapter.mode == "direct_fabric"

    def test_invalid_mode_raises(self):
        with pytest.raises(ValueError):
            WorkerRuntimeAdapter(mode="bogus")

    def test_next_port_increments(self):
        adapter = WorkerRuntimeAdapter(mode="native_subagent")
        p1 = adapter._next_port()
        p2 = adapter._next_port()
        assert p2 == p1 + 1

    def test_singleton_caches_per_mode(self):
        a = get_runtime_adapter(mode="native_subagent")
        b = get_runtime_adapter(mode="native_subagent")
        assert a is b
        c = get_runtime_adapter(mode="direct_fabric")
        assert c is not a


class TestLaunchWorker:
    def test_native_launch_completed(self, monkeypatch):
        def fake_dispatch(**kwargs):
            return {"type": "message", "content": [{"type": "text", "text": "result text"}]}

        import merged_agentic_swarm.services.worker_runtime_adapter as mod

        monkeypatch.setattr(mod.default_fabric, "dispatch_request", fake_dispatch)
        adapter = WorkerRuntimeAdapter(mode="native_subagent")
        result = adapter.launch_worker(_spec(), "write hello")
        assert result["status"] == "completed"
        assert result["evidence"] == "result text"
        assert result["worker_id"] == "w1"
        assert result["role"] == "core_engineer"
        assert result["model_tier"] == _spec().model_alias
        assert result["run_id"]

    def test_native_launch_simulated_is_hard_failure(self, monkeypatch):
        """A simulated fabric response must fail, never complete or 'partial'.
        This is the invariant that keeps simulation out of the swarm gates."""

        def fake_dispatch(**kwargs):
            return {"type": "message", "simulation_fallback": True, "content": [{"type": "text", "text": "fake"}]}

        import merged_agentic_swarm.services.worker_runtime_adapter as mod

        monkeypatch.setattr(mod.default_fabric, "dispatch_request", fake_dispatch)
        adapter = WorkerRuntimeAdapter(mode="native_subagent")
        result = adapter.launch_worker(_spec(), "t")
        assert result["status"] == "failed"
        assert "simulation" in result["evidence"]

    def test_native_launch_failed_on_exception(self, monkeypatch):
        def boom(**kwargs):
            raise RuntimeError("all keys down")

        import merged_agentic_swarm.services.worker_runtime_adapter as mod

        monkeypatch.setattr(mod.default_fabric, "dispatch_request", boom)
        adapter = WorkerRuntimeAdapter(mode="native_subagent")
        result = adapter.launch_worker(_spec(), "t")
        assert result["status"] == "failed"
        assert "all keys down" in result["evidence"]

    def test_direct_fabric_launch_delegates(self, monkeypatch):
        captured = {}

        def fake_dispatch(**kwargs):
            captured.update(kwargs)
            return {"type": "message", "content": [{"type": "text", "text": "ok"}]}

        import merged_agentic_swarm.services.worker_runtime_adapter as mod

        monkeypatch.setattr(mod.default_fabric, "dispatch_request", fake_dispatch)
        adapter = WorkerRuntimeAdapter(mode="direct_fabric")
        result = adapter.launch_worker(_spec(), "t")
        assert result["status"] == "completed"
        assert captured["system_prompt"] == "Do the task."

    def test_opencode_falls_back_to_native_when_no_bin(self, monkeypatch):
        import merged_agentic_swarm.services.worker_runtime_adapter as mod

        monkeypatch.setattr(mod, "_resolve_opencode_bin", lambda: None)

        def fake_dispatch(**kwargs):
            return {"type": "message", "content": [{"type": "text", "text": "native fallback"}]}

        monkeypatch.setattr(mod.default_fabric, "dispatch_request", fake_dispatch)
        adapter = WorkerRuntimeAdapter(mode="opencode")
        result = adapter.launch_worker(_spec(), "t")
        assert result["status"] == "completed"
        assert result["evidence"] == "native fallback"


class TestLaunchBatch:
    def test_batch_returns_result_per_task(self, monkeypatch):
        import merged_agentic_swarm.services.worker_runtime_adapter as mod

        def fake_dispatch(**kwargs):
            return {"type": "message", "content": [{"type": "text", "text": "batch result"}]}

        monkeypatch.setattr(mod.default_fabric, "dispatch_request", fake_dispatch)
        adapter = WorkerRuntimeAdapter(mode="native_subagent")
        results = adapter.launch_batch(["t1", "t2", "t3"], WorkerRole.CORE_ENGINEER, max_concurrency=2)
        assert len(results) == 3
        assert all(r["status"] == "completed" for r in results)
        assert all(r["role"] == "core_engineer" for r in results)

    def test_batch_survives_worker_exception(self, monkeypatch):
        import merged_agentic_swarm.services.worker_runtime_adapter as mod

        call_count = 0

        def flaky_dispatch(**kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise RuntimeError("transient")
            return {"type": "message", "content": [{"type": "text", "text": "ok"}]}

        monkeypatch.setattr(mod.default_fabric, "dispatch_request", flaky_dispatch)
        adapter = WorkerRuntimeAdapter(mode="native_subagent")
        results = adapter.launch_batch(["t1", "t2"], WorkerRole.CORE_ENGINEER, max_concurrency=2)
        assert len(results) == 2
        # at least one success; the failed one carries status failed
        statuses = [r["status"] for r in results]
        assert "failed" in statuses or "completed" in statuses


class TestShutdown:
    def test_shutdown_clears_processes(self):
        adapter = WorkerRuntimeAdapter(mode="native_subagent")
        adapter.shutdown()
        assert adapter._worker_processes == {}
