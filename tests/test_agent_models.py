"""
Tests for models/agent_models.py

Coverage: AgentSpec, WorkerPoolConfig, SpawnChainEntry, WorkerPoolState,
WorkerRole, AgentType enums.
"""
import time
from models.agent_models import (
    AgentSpec, AgentType, WorkerRole, WorkerPoolConfig,
    SpawnChainEntry, WorkerPoolState,
)


class TestWorkerRole:
    def test_values(self):
        assert WorkerRole.MASTER_ARCHITECT.value == "master_architect"
        assert WorkerRole.CODEBASE_MAPPER.value == "codebase_mapper"
        assert WorkerRole.SPEC_GAP_CLOSER.value == "spec_gap_closer"
        assert WorkerRole.CORE_ENGINEER.value == "core_engineer"
        assert WorkerRole.REFACTOR_SPECIALIST.value == "refactor_specialist"
        assert WorkerRole.UNIT_TESTER.value == "unit_tester"
        assert WorkerRole.SECURITY_VERIFIER.value == "security_verifier"
        assert WorkerRole.HOT_MICRO_SPECIALIST.value == "hot_micro_specialist"
        assert WorkerRole.COLD_DURABLE.value == "cold_durable"


class TestAgentType:
    def test_values(self):
        assert AgentType.SWARM_WORKER.value == "swarm_worker"
        assert AgentType.HOT_MICRO_SPECIALIST.value == "hot_micro_specialist"
        assert AgentType.COLD_DURABLE.value == "cold_durable"


class TestAgentSpec:
    def test_default_creation(self):
        spec = AgentSpec(
            id="agent-001",
            name="Test Agent",
            role=WorkerRole.CORE_ENGINEER,
            agent_type=AgentType.SWARM_WORKER,
            system_prompt="You are a test agent.",
        )
        assert spec.id == "agent-001"
        assert spec.name == "Test Agent"
        assert spec.role == WorkerRole.CORE_ENGINEER
        assert spec.agent_type == AgentType.SWARM_WORKER
        assert spec.model_alias == "claude-3-7-sonnet"
        assert spec.max_concurrency == 1
        assert spec.ttl_sec is None
        assert spec.validated_learnings_applied == []
        assert spec.parent_agent_id is None
        assert spec.created_at > 0

    def test_durable_never_expires(self):
        spec = AgentSpec(
            id="cold-001", name="Durable",
            role=WorkerRole.COLD_DURABLE,
            agent_type=AgentType.COLD_DURABLE,
            system_prompt="Durable agent",
            ttl_sec=None,
        )
        assert not spec.is_expired, "Durable (ttl=None) should never expire"

    def test_hot_expires_after_ttl(self):
        spec = AgentSpec(
            id="hot-001", name="Hot",
            role=WorkerRole.HOT_MICRO_SPECIALIST,
            agent_type=AgentType.HOT_MICRO_SPECIALIST,
            system_prompt="Hot agent",
            ttl_sec=0.01,  # 10 ms
            created_at=time.time() - 1,  # created 1 second ago
        )
        assert spec.is_expired, "Agent with TTL 0.01s created 1s ago should be expired"

    def test_hot_not_expired_within_ttl(self):
        spec = AgentSpec(
            id="hot-002", name="Fresh",
            role=WorkerRole.HOT_MICRO_SPECIALIST,
            agent_type=AgentType.HOT_MICRO_SPECIALIST,
            system_prompt="Fresh hot agent",
            ttl_sec=300.0,
        )
        assert not spec.is_expired, "Freshly created agent should not be expired"

    def test_to_dict_serializes_enums(self):
        spec = AgentSpec(
            id="d-001", name="Dict",
            role=WorkerRole.MASTER_ARCHITECT,
            agent_type=AgentType.COLD_DURABLE,
            system_prompt="test",
        )
        d = spec.to_dict()
        assert d["role"] == "master_architect"
        assert d["agent_type"] == "cold_durable"
        assert d["id"] == "d-001"

    def test_custom_fields(self):
        spec = AgentSpec(
            id="custom", name="Custom",
            role=WorkerRole.UNIT_TESTER,
            agent_type=AgentType.SWARM_WORKER,
            system_prompt="test",
            model_alias="claude-3-5-sonnet",
            max_concurrency=4,
            validated_learnings_applied=["LEARN-001"],
            parent_agent_id="parent-001",
        )
        assert spec.model_alias == "claude-3-5-sonnet"
        assert spec.max_concurrency == 4
        assert "LEARN-001" in spec.validated_learnings_applied
        assert spec.parent_agent_id == "parent-001"


class TestWorkerPoolConfig:
    def test_default_allocations(self):
        cfg = WorkerPoolConfig()
        assert cfg.pool_name == "opencode-swarm-40"
        assert cfg.max_total_workers == 40
        assert cfg.role_allocations[WorkerRole.CORE_ENGINEER.value] == 18
        assert cfg.role_allocations[WorkerRole.UNIT_TESTER.value] == 5
        total = sum(cfg.role_allocations.values())
        assert total == 40

    def test_custom_config(self):
        cfg = WorkerPoolConfig(
            pool_name="mini-swarm",
            max_total_workers=5,
            role_allocations={WorkerRole.CORE_ENGINEER.value: 3, WorkerRole.UNIT_TESTER.value: 2},
        )
        assert cfg.max_total_workers == 5
        assert sum(cfg.role_allocations.values()) == 5


class TestSpawnChainEntry:
    def test_default_creation(self):
        entry = SpawnChainEntry(
            entry_id="CHAIN-0001",
            source_learning_id="LEARN-0001",
            spawned_agent_id="agent-cold-001",
            agent_type=AgentType.COLD_DURABLE,
            trigger_reason="Validation threshold reached",
        )
        assert entry.entry_id == "CHAIN-0001"
        assert entry.parent_entry_id is None
        assert entry.timestamp > 0

    def test_to_dict(self):
        entry = SpawnChainEntry(
            entry_id="CHAIN-0002",
            source_learning_id="LEARN-0002",
            spawned_agent_id="agent-hot-001",
            agent_type=AgentType.HOT_MICRO_SPECIALIST,
            trigger_reason="Acute fix",
            parent_entry_id="CHAIN-0001",
        )
        d = entry.to_dict()
        assert d["agent_type"] == "hot_micro_specialist"
        assert d["parent_entry_id"] == "CHAIN-0001"


class TestWorkerPoolState:
    def test_default_state(self):
        state = WorkerPoolState()
        assert state.active_workers == 0
        assert state.total_assigned == 0
        assert state.completed_tasks == 0
        assert state.failed_tasks == 0

    def test_record_pool_success(self):
        state = WorkerPoolState()
        state.record_pool_success("domain_module")
        assert state.pool_health["domain_module"]["completed"] == 1

    def test_record_pool_failure(self):
        state = WorkerPoolState()
        state.record_pool_failure("domain_module")
        assert state.pool_health["domain_module"]["failed"] == 1

    def test_record_rate_limit(self):
        state = WorkerPoolState()
        state.record_pool_failure("domain_module", is_rate_limit=True)
        assert state.pool_health["domain_module"]["rate_limited"] == 1
        assert state.pool_health["domain_module"]["failed"] == 0

    def test_get_pool_summary_returns_copy(self):
        state = WorkerPoolState()
        state.record_pool_success("test_pool")
        summary = state.get_pool_summary()
        assert "test_pool" in summary
        assert summary["test_pool"]["completed"] == 1

    def test_to_dict(self):
        state = WorkerPoolState()
        state.completed_tasks = 5
        state.failed_tasks = 1
        d = state.to_dict()
        assert d["completed_tasks"] == 5
        assert d["failed_tasks"] == 1
