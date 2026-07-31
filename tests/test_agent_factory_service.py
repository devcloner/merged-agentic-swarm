"""
Tests for services/agent_factory_service.py

Coverage: ChainRegistry (load, save, register_spawn), DurableAgentFactory
(purge_expired, spawn_from_learning, _write_agent_spec_file, sync_agent_specs).
"""
import os
import time

from merged_agentic_swarm.models.agent_models import AgentSpec, AgentType, WorkerRole


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
            "L-002", "a-002", AgentType.HOT_MICRO_SPECIALIST, "child",
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


class TestDurableAgentFactory:
    def test_purge_expired_removes_hot_agents(self, temp_dir, isolated_knowledge_cache, isolated_chain_registry):
        from merged_agentic_swarm.services.agent_factory_service import DurableAgentFactory
        factory = DurableAgentFactory(chain_registry=isolated_chain_registry)

        # Manually add an expired HOT agent
        expired = AgentSpec(
            id="hot-expired", name="Expired HOT",
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
            id="cold-permanent", name="Durable",
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
            spec = factory.spawn_from_learning(lid, trigger_reason="Forced",
                                                force_type=AgentType.COLD_DURABLE)
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

    def test_write_agent_spec_file_creates_md(self, temp_dir, isolated_knowledge_cache, isolated_chain_registry, monkeypatch):
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
