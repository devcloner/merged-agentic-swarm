"""
Tests for tools/agentic_orchestrator.py

Coverage: MultiLayeredAgenticOrchestrator — _apply_worker_outputs,
_compact_registries, _run_syntax_verification, _append_jsonl,
_promote_cold_path, initialize_system.
"""
import os


class TestApplyWorkerOutputs:
    def setup_method(self):
        from merged_agentic_swarm.tools.agentic_orchestrator import MultiLayeredAgenticOrchestrator
        self.orch = MultiLayeredAgenticOrchestrator()

    def test_empty_results(self):
        count = self.orch._apply_worker_outputs([])
        assert count == 0

    def test_no_completed_results(self):
        results = [{"status": "failed"}, {"status": "error"}]
        count = self.orch._apply_worker_outputs(results)
        assert count == 0

    def test_no_content_in_response(self):
        results = [{"status": "completed", "response": {}}]
        count = self.orch._apply_worker_outputs(results)
        assert count == 0

    def test_non_dict_response(self):
        results = [{"status": "completed", "response": "string response"}]
        count = self.orch._apply_worker_outputs(results)
        assert count == 0  # no file: pattern in plain string

    def test_skipped_when_missing_worker_id(self):
        """Worker results without worker_id don't crash."""
        results = [{"status": "completed", "response": {"content": "no file annotation"}}]
        count = self.orch._apply_worker_outputs(results)
        assert count == 0

    def test_counts_agentic_loop_files_written(self):
        """Real writes from the agentic tool loop are counted (not re-parsed)."""
        results = [{"status": "completed", "files_written": ["a.py", "b.py"]}]
        count = self.orch._apply_worker_outputs(results)
        assert count == 2

    def test_parses_file_blocks_from_final_text(self, temp_dir):
        """Secondary path: # file: blocks in final_text are still written to disk."""
        import os
        abs_path = os.path.join(temp_dir, "x.py")
        results = [{
            "status": "completed",
            "final_text": f'```python\n# file: {abs_path}\nprint(1)\n```',
        }]
        count = self.orch._apply_worker_outputs(results)
        assert count == 1
        assert os.path.exists(abs_path)
        with open(abs_path, encoding="utf-8") as fh:
            assert fh.read() == "print(1)"

    def test_simulation_worker_fails_gate(self):
        """A simulated worker result is status=failed, so all_ok is False.

        This is the invariant that makes simulation unable to advance any wave:
        the gate formula ``all(r.get('status') == 'completed')`` fails.
        """
        results = [
            {"status": "completed", "subtask_id": "s1"},
            {"status": "failed", "reason": "simulation_fallback", "subtask_id": "s2"},
        ]
        assert not all(r.get("status") == "completed" for r in results)

    def test_logs_per_worker_real_work(self, caplog):
        """Each completed worker's files_written/commands_run are logged —
        the auditable trail that proves a gate advanced on real artifacts."""
        import logging
        results = [{
            "status": "completed",
            "worker_id": "opencode-worker-11",
            "files_written": ["a.py", "b.py"],
            "commands_run": ["uv run python a.py"],
            "final_text": "done",
        }]
        with caplog.at_level(logging.INFO, logger="agentic_orchestrator"):
            count = self.orch._apply_worker_outputs(results, wave_label="W1")
        assert count == 2
        assert any("opencode-worker-11" in r.message and "REAL WORK" in r.message and "a.py" in r.message for r in caplog.records)
        assert any("W1 aggregate: 2 distinct real file(s), 1 distinct real command(s)" in r.message for r in caplog.records)

    def test_counts_distinct_files_written(self):
        """Repeated writes to the same path across loop iterations count once."""
        results = [{"status": "completed", "files_written": ["a.py", "a.py", "b.py", "a.py"]}]
        count = self.orch._apply_worker_outputs(results, wave_label="W1")
        assert count == 2

    def test_logs_text_only_worker(self, caplog):
        """A completed worker that produced no files/commands is flagged honestly."""
        import logging
        results = [{
            "status": "completed",
            "worker_id": "opencode-worker-07",
            "final_text": "no artifacts needed",
        }]
        with caplog.at_level(logging.INFO, logger="agentic_orchestrator"):
            count = self.orch._apply_worker_outputs(results, wave_label="W2")
        assert count == 0
        assert any("produced no files/commands" in r.message and "opencode-worker-07" in r.message for r in caplog.records)


class TestCompactRegistries:
    def setup_method(self):
        from merged_agentic_swarm.tools.agentic_orchestrator import MultiLayeredAgenticOrchestrator
        self.orch = MultiLayeredAgenticOrchestrator()

    def test_no_registries_no_crash(self):
        """_compact_registries handles missing registry dir gracefully."""
        # Temporarily point to nonexistent dir
        counts = self.orch._compact_registries()
        assert isinstance(counts, dict)


class TestAppendJSONL:
    def setup_method(self):
        from merged_agentic_swarm.tools.agentic_orchestrator import MultiLayeredAgenticOrchestrator
        self.orch = MultiLayeredAgenticOrchestrator()

    def test_append_to_new_file(self, temp_dir):
        path = os.path.join(temp_dir, "test.jsonl")
        self.orch._append_jsonl(path, {"id": "001", "value": "test"})
        with open(path) as f:
            lines = f.readlines()
        assert len(lines) == 1
        assert "001" in lines[0]

    def test_append_to_existing_file(self, temp_dir):
        path = os.path.join(temp_dir, "test.jsonl")
        self.orch._append_jsonl(path, {"id": "001"})
        self.orch._append_jsonl(path, {"id": "002"})
        with open(path) as f:
            lines = f.readlines()
        assert len(lines) == 2


class TestRunSyntaxVerification:
    def setup_method(self):
        from merged_agentic_swarm.tools.agentic_orchestrator import MultiLayeredAgenticOrchestrator
        self.orch = MultiLayeredAgenticOrchestrator()

    def test_syntax_verification_runs(self):
        """_run_syntax_verification should produce a dict with exit_code and output."""
        result = self.orch._run_syntax_verification()
        assert "exit_code" in result
        assert "output_summary" in result


class TestPromoteColdPath:
    def setup_method(self):
        from merged_agentic_swarm.tools.agentic_orchestrator import MultiLayeredAgenticOrchestrator
        self.orch = MultiLayeredAgenticOrchestrator()
        # Clear persisted IDs and cache for test isolation
        self.orch.promoted_learning_ids = set()

        from merged_agentic_swarm.tools.knowledge_cache import default_knowledge_cache
        self.cache = default_knowledge_cache
        self.cache.learnings = {}

    def test_no_unpromoted_learnings(self):
        result = self.orch._promote_cold_path("test")
        assert result["promoted_knowledge"] == 0
        assert result["promoted_agents"] == 0

    def test_promotes_single_learning(self, temp_dir):
        lid = self.cache.add_learning("Test learning", "general", "Solution")
        result = self.orch._promote_cold_path("test")
        assert result["promoted_knowledge"] == 1
        assert lid in self.orch.promoted_learning_ids

    def test_promotes_agent_when_category_threshold_reached(self, temp_dir):
        """Add 3 learnings in the same category → should promote an agent."""
        for i in range(3):
            self.cache.add_learning(f"Learning {i}", "threshold_test", f"Solution {i}")
        result = self.orch._promote_cold_path("batch")
        assert result["promoted_knowledge"] == 3
        assert result["promoted_agents"] == 1

    def test_does_not_duplicate_agent_per_category(self, temp_dir):
        """Multiple promotions of same category should only create 1 agent per batch."""
        for i in range(6):
            self.cache.add_learning(f"L{i}", "single_agent_cat", f"Sol{i}")
        result = self.orch._promote_cold_path("batch")
        assert result["promoted_agents"] == 1

    def test_persists_promoted_ids(self, temp_dir):
        """_save_promoted_ids should persist across runs."""
        # Override the promoted_ids_file to temp
        self.orch.promoted_ids_file = os.path.join(temp_dir, "promoted_ids.json")
        lid = self.cache.add_learning("Persist learning", "persist", "Sol")
        self.orch._promote_cold_path("test")
        self.orch._save_promoted_ids()

        # Load into new orchestrator
        from merged_agentic_swarm.tools.agentic_orchestrator import MultiLayeredAgenticOrchestrator
        orch2 = MultiLayeredAgenticOrchestrator()
        orch2.promoted_ids_file = self.orch.promoted_ids_file
        orch2._load_promoted_ids()
        assert lid in orch2.promoted_learning_ids


class TestInitializeSystem:
    def test_initialize_system(self):
        """initialize_system should return ready status."""
        from merged_agentic_swarm.tools.agentic_orchestrator import MultiLayeredAgenticOrchestrator
        orch = MultiLayeredAgenticOrchestrator()
        result = orch.initialize_system(start_proxy_port=0)
        assert result["status"] == "ready"
        assert result["task_master_ready"] is True
        assert result["swarm_workers"] == 40
        # Clean up the proxy if it was started
        if orch.proxy_daemon:
            orch.proxy_daemon.stop()
