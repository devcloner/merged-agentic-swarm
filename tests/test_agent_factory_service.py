"""
Tests for services/agent_factory_service.py

Coverage: ChainRegistry (load, save, register_spawn), DurableAgentFactory
(purge_expired, spawn_from_learning, _write_agent_spec_file, sync_agent_specs).
"""

import os
import time

import pytest

from merged_agentic_swarm.models.agent_models import AgentSpec, AgentType, WorkerRole


@pytest.fixture
def isolated_agents_registry(temp_dir):
    """Return a temp path for the durable cold-path agents.jsonl registry."""
    return os.path.join(temp_dir, "agents.jsonl")


class TestChainRegistry:
    def test_default_registry(self, temp_dir):
        from merged_agentic_swarm.services.agent_factory_service import ChainRegistry

        reg_file = os.path.join(temp_dir, "chain.json")
        reg = ChainRegistry(registry_file=reg_file)
        assert reg.entries == []

    def test_register_spawn(self, temp_dir):
        from merged_agentic_swarm.services.agent_factory_service import ChainRegistry

        reg_file = os.path.join(temp_dir, "chain.json")
        reg = ChainRegistry(registry_file=reg_file)
        entry = reg.register_spawn(
            source_learning_id="LEARN-001",
            spawned_agent_id="agent-test-001",
            agent_type=AgentType.COLD_DURABLE,
            trigger_reason="Test trigger",
        )
        assert entry.entry_id.startswith("CHAIN-")
        assert len(reg.entries) == 1

    def test_persists_across_loads(self, temp_dir):
        from merged_agentic_swarm.services.agent_factory_service import ChainRegistry

        reg_file = os.path.join(temp_dir, "chain.json")
        reg1 = ChainRegistry(registry_file=reg_file)
        reg1.register_spawn("L-001", "a-001", AgentType.HOT_MICRO_SPECIALIST, "test")

        reg2 = ChainRegistry(registry_file=reg_file)
        assert len(reg2.entries) == 1

    def test_register_spawn_with_parent(self, temp_dir):
        from merged_agentic_swarm.services.agent_factory_service import ChainRegistry

        reg_file = os.path.join(temp_dir, "chain.json")
        reg = ChainRegistry(registry_file=reg_file)
        parent = reg.register_spawn("L-001", "a-001", AgentType.COLD_DURABLE, "parent")
        child = reg.register_spawn(
            "L-002",
            "a-002",
            AgentType.HOT_MICRO_SPECIALIST,
            "child",
            parent_entry_id=parent.entry_id,
        )
        assert child.parent_entry_id == parent.entry_id

    def test_load_corrupted_file(self, temp_dir):
        from merged_agentic_swarm.services.agent_factory_service import ChainRegistry

        reg_file = os.path.join(temp_dir, "chain.json")
        with open(reg_file, "w") as f:
            f.write("not valid json")
        reg = ChainRegistry(registry_file=reg_file)
        assert reg.entries == []  # graceful fallback

    def test_register_spawn_entry_ids_unique_within_batch(self, temp_dir):
        """#18: entry_ids in one promotion batch must never collide."""
        from merged_agentic_swarm.services.agent_factory_service import ChainRegistry

        reg_file = os.path.join(temp_dir, "chain.json")
        reg = ChainRegistry(registry_file=reg_file)
        ids = [
            reg.register_spawn(f"L-{i:03d}", f"a-{i:03d}", AgentType.COLD_DURABLE, f"batch {i}").entry_id
            for i in range(5)
        ]
        assert len(ids) == len(set(ids)), f"duplicate entry_ids in one batch: {ids}"
        assert all(reg.entries[i].entry_id == ids[i] for i in range(5))

    def test_register_spawn_entry_ids_unique_across_instances(self, temp_dir):
        """#18: separate registry instances sharing a file must not reuse entry_ids."""
        from merged_agentic_swarm.services.agent_factory_service import ChainRegistry

        reg_file = os.path.join(temp_dir, "chain.json")
        reg1 = ChainRegistry(registry_file=reg_file)
        reg2 = ChainRegistry(registry_file=reg_file)
        id1 = reg1.register_spawn("L-1", "a-1", AgentType.COLD_DURABLE, "proc 1").entry_id
        id2 = reg2.register_spawn("L-2", "a-2", AgentType.COLD_DURABLE, "proc 2").entry_id
        assert id1 != id2
        assert id1.startswith("CHAIN-")
        assert id2.startswith("CHAIN-")


class TestDurableAgentFactory:
    def test_purge_expired_removes_hot_agents(self, temp_dir, isolated_knowledge_cache, isolated_chain_registry):
        from merged_agentic_swarm.services.agent_factory_service import DurableAgentFactory

        factory = DurableAgentFactory(chain_registry=isolated_chain_registry)

        # Manually add an expired HOT agent
        expired = AgentSpec(
            id="hot-expired",
            name="Expired HOT",
            role=WorkerRole.HOT_MICRO_SPECIALIST,
            agent_type=AgentType.HOT_MICRO_SPECIALIST,
            system_prompt="test",
            ttl_sec=0.001,  # 1ms TTL
            created_at=time.time() - 10,
        )
        factory.active_hot_specialists["hot-expired"] = expired
        time.sleep(0.01)
        count = factory.purge_expired()
        assert count == 1
        assert "hot-expired" not in factory.active_hot_specialists

    def test_purge_expired_durable_untouched(self, temp_dir, isolated_chain_registry):
        from merged_agentic_swarm.services.agent_factory_service import DurableAgentFactory

        factory = DurableAgentFactory(chain_registry=isolated_chain_registry)
        durable = AgentSpec(
            id="cold-permanent",
            name="Durable",
            role=WorkerRole.COLD_DURABLE,
            agent_type=AgentType.COLD_DURABLE,
            system_prompt="test",
            ttl_sec=None,  # no expiry
        )
        factory.active_cold_agents["cold-permanent"] = durable
        count = factory.purge_expired()
        assert count == 0
        assert "cold-permanent" in factory.active_cold_agents

    def test_spawn_from_learning_cold(self, temp_dir, isolated_knowledge_cache, isolated_chain_registry):
        import merged_agentic_swarm.services.agent_factory_service as afs_mod
        from merged_agentic_swarm.services.agent_factory_service import DurableAgentFactory

        orig_cache = afs_mod.default_knowledge_cache
        afs_mod.default_knowledge_cache = isolated_knowledge_cache
        try:
            factory = DurableAgentFactory(chain_registry=isolated_chain_registry)
            lid = isolated_knowledge_cache.add_learning("Swarm pattern", "swarm_concurrency", "Use 40 workers")
            spec = factory.spawn_from_learning(lid, trigger_reason="Test spawn")
            assert spec.agent_type == AgentType.COLD_DURABLE
            assert spec.ttl_sec is None
            assert lid in spec.validated_learnings_applied
            assert spec.id in factory.active_cold_agents
        finally:
            afs_mod.default_knowledge_cache = orig_cache

    def test_spawn_from_learning_hot(self, temp_dir, isolated_knowledge_cache, isolated_chain_registry):
        import merged_agentic_swarm.services.agent_factory_service as afs_mod
        from merged_agentic_swarm.services.agent_factory_service import DurableAgentFactory

        orig_cache = afs_mod.default_knowledge_cache
        afs_mod.default_knowledge_cache = isolated_knowledge_cache
        try:
            factory = DurableAgentFactory(chain_registry=isolated_chain_registry)
            lid = isolated_knowledge_cache.add_learning("Hot fix", "error_fix", "Quick patch")
            spec = factory.spawn_from_learning(lid, trigger_reason="Error recovery")
            assert spec.agent_type == AgentType.HOT_MICRO_SPECIALIST
            assert spec.ttl_sec == 300.0
            assert spec.id in factory.active_hot_specialists
        finally:
            afs_mod.default_knowledge_cache = orig_cache

    def test_spawn_from_learning_with_force_type(self, temp_dir, isolated_knowledge_cache, isolated_chain_registry):
        import merged_agentic_swarm.services.agent_factory_service as afs_mod
        from merged_agentic_swarm.services.agent_factory_service import DurableAgentFactory

        orig_cache = afs_mod.default_knowledge_cache
        afs_mod.default_knowledge_cache = isolated_knowledge_cache
        try:
            factory = DurableAgentFactory(chain_registry=isolated_chain_registry)
            lid = isolated_knowledge_cache.add_learning("Force test", "general", "Solution")
            spec = factory.spawn_from_learning(lid, trigger_reason="Forced", force_type=AgentType.COLD_DURABLE)
            assert spec.agent_type == AgentType.COLD_DURABLE
        finally:
            afs_mod.default_knowledge_cache = orig_cache

    def test_spawn_from_learning_registers_in_chain(self, temp_dir, isolated_knowledge_cache, isolated_chain_registry):
        import merged_agentic_swarm.services.agent_factory_service as afs_mod
        from merged_agentic_swarm.services.agent_factory_service import DurableAgentFactory

        orig_cache = afs_mod.default_knowledge_cache
        afs_mod.default_knowledge_cache = isolated_knowledge_cache
        try:
            factory = DurableAgentFactory(chain_registry=isolated_chain_registry)
            lid = isolated_knowledge_cache.add_learning("Chain test", "general", "Solution")
            factory.spawn_from_learning(lid, trigger_reason="Chain check")
            assert len(isolated_chain_registry.entries) == 1
        finally:
            afs_mod.default_knowledge_cache = orig_cache

    def test_spawn_cold_persists_to_agents_registry(
        self, isolated_knowledge_cache, isolated_chain_registry, isolated_agents_registry
    ):
        """#17: COLD_DURABLE spawns must be written to the durable agents.jsonl registry."""
        import json

        import merged_agentic_swarm.services.agent_factory_service as afs_mod
        from merged_agentic_swarm.services.agent_factory_service import DurableAgentFactory

        orig_cache = afs_mod.default_knowledge_cache
        afs_mod.default_knowledge_cache = isolated_knowledge_cache
        try:
            factory = DurableAgentFactory(
                chain_registry=isolated_chain_registry, agents_registry_file=isolated_agents_registry
            )
            lid = isolated_knowledge_cache.add_learning("Durable pattern", "swarm_concurrency", "40 workers")
            spec = factory.spawn_from_learning(lid, trigger_reason="Durable state persistence")
            assert spec.agent_type == AgentType.COLD_DURABLE

            assert os.path.exists(isolated_agents_registry)
            with open(isolated_agents_registry) as f:
                lines = [json.loads(l) for l in f if l.strip()]
            assert len(lines) == 1
            record = lines[0]
            assert record["id"] == spec.id
            assert record["ttl_sec"] is None  # durable
            assert record["role"] == "cold_durable"
            assert record["agent_type"] == "cold_durable"
            assert record["category"] == "swarm_concurrency"
            assert lid in record["derived_from_learnings"]
        finally:
            afs_mod.default_knowledge_cache = orig_cache

    def test_spawn_hot_not_persisted_to_agents_registry(
        self, isolated_knowledge_cache, isolated_chain_registry, isolated_agents_registry
    ):
        """#17: HOT micro-specialists are transient and must NOT hit agents.jsonl."""
        import merged_agentic_swarm.services.agent_factory_service as afs_mod
        from merged_agentic_swarm.services.agent_factory_service import DurableAgentFactory

        orig_cache = afs_mod.default_knowledge_cache
        afs_mod.default_knowledge_cache = isolated_knowledge_cache
        try:
            factory = DurableAgentFactory(
                chain_registry=isolated_chain_registry, agents_registry_file=isolated_agents_registry
            )
            lid = isolated_knowledge_cache.add_learning("Hot fix", "error_fix", "Quick patch")
            spec = factory.spawn_from_learning(lid, trigger_reason="Error recovery")
            assert spec.agent_type == AgentType.HOT_MICRO_SPECIALIST
            assert not os.path.exists(isolated_agents_registry) or os.path.getsize(isolated_agents_registry) == 0
        finally:
            afs_mod.default_knowledge_cache = orig_cache

    def test_cold_persist_is_idempotent(self, isolated_chain_registry, isolated_agents_registry):
        """#17: persisting an already-registered agent id must not duplicate the line."""
        from merged_agentic_swarm.services.agent_factory_service import DurableAgentFactory

        factory = DurableAgentFactory(
            chain_registry=isolated_chain_registry, agents_registry_file=isolated_agents_registry
        )
        record = {
            "id": "agent-cold_durable-999",
            "name": "Durable 999",
            "role": "cold_durable",
            "type": "cold_durable",
            "category": "general",
            "derived_from_learnings": ["LEARN-001"],
            "system_prompt": "prompt",
            "promoted_at": time.time(),
            "ttl_sec": None,
        }
        assert factory._persist_cold_agent(record) is not None
        assert factory._persist_cold_agent(record) is None  # skipped
        with open(isolated_agents_registry) as f:
            assert sum(1 for l in f if l.strip()) == 1

    def test_cold_agents_loaded_from_registry_on_restart(
        self, isolated_knowledge_cache, isolated_chain_registry, isolated_agents_registry
    ):
        """#17: a fresh factory discovers persisted COLD_DURABLE agents (restart survival)."""
        import merged_agentic_swarm.services.agent_factory_service as afs_mod
        from merged_agentic_swarm.services.agent_factory_service import DurableAgentFactory

        orig_cache = afs_mod.default_knowledge_cache
        afs_mod.default_knowledge_cache = isolated_knowledge_cache
        try:
            factory1 = DurableAgentFactory(
                chain_registry=isolated_chain_registry, agents_registry_file=isolated_agents_registry
            )
            lid = isolated_knowledge_cache.add_learning("Restart pattern", "wave_gating", "Gate everything")
            spec = factory1.spawn_from_learning(lid, trigger_reason="Durable")

            factory2 = DurableAgentFactory(
                chain_registry=isolated_chain_registry, agents_registry_file=isolated_agents_registry
            )
            assert spec.id in factory2.active_cold_agents
            assert factory2.active_cold_agents[spec.id].agent_type == AgentType.COLD_DURABLE
            assert factory2.active_cold_agents[spec.id].ttl_sec is None
        finally:
            afs_mod.default_knowledge_cache = orig_cache

    def test_write_agent_spec_file_creates_md(
        self, temp_dir, isolated_knowledge_cache, isolated_chain_registry, monkeypatch
    ):
        from merged_agentic_swarm.services.agent_factory_service import DurableAgentFactory

        # Point .claude/agents to temp dir
        monkeypatch.setattr("os.path.expanduser", lambda p: temp_dir)

        factory = DurableAgentFactory(chain_registry=isolated_chain_registry)
        agent_spec = {
            "id": "test-agent-001",
            "name": "Test Agent",
            "category": "test_category",
            "type": "cold_durable",
            "promoted_at": time.time(),
            "derived_from_learnings": ["LEARN-001"],
            "system_prompt": "You are a test agent.",
        }
        result = factory._write_agent_spec_file(agent_spec)
        assert result is not None
        assert result.endswith(".md")

        # Verify content
        with open(result) as f:
            content = f.read()
        assert "Test Agent" in content
        assert "test_category" in content
        assert "LEARN-001" in content

    def test_write_agent_spec_file_skips_existing(self, temp_dir, isolated_chain_registry, monkeypatch):
        from merged_agentic_swarm.services.agent_factory_service import DurableAgentFactory

        monkeypatch.setattr("os.path.expanduser", lambda p: temp_dir)

        factory = DurableAgentFactory(chain_registry=isolated_chain_registry)
        agent_spec = {
            "id": "existing-agent",
            "name": "Existing",
            "category": "test",
            "type": "cold_durable",
            "promoted_at": time.time(),
            "derived_from_learnings": [],
            "system_prompt": "prompt",
        }
        # First write should succeed
        result1 = factory._write_agent_spec_file(agent_spec)
        assert result1 is not None

        # Second write should skip
        result2 = factory._write_agent_spec_file(agent_spec)
        assert result2 is None

    def test_sync_agent_specs_missing_registry(self, isolated_chain_registry, monkeypatch, temp_dir):
        """sync_agent_specs should handle missing agents.jsonl gracefully."""
        from merged_agentic_swarm.services.agent_factory_service import DurableAgentFactory

        factory = DurableAgentFactory(chain_registry=isolated_chain_registry)

        # Mock os.path.exists so agents.jsonl looks missing to sync_agent_specs
        original_exists = os.path.exists

        def mock_exists(path):
            if path.endswith("agents.jsonl"):
                return False
            return original_exists(path)

        monkeypatch.setattr(os.path, "exists", mock_exists)

        count = factory.sync_agent_specs()
        assert count == 0
