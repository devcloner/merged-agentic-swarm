"""
Agent, Worker Pool, and Spawn Chain Data Models
"""

import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class WorkerRole(str, Enum):
    MASTER_ARCHITECT = "master_architect"
    CODEBASE_MAPPER = "codebase_mapper"
    SPEC_GAP_CLOSER = "spec_gap_closer"
    CORE_ENGINEER = "core_engineer"
    REFACTOR_SPECIALIST = "refactor_specialist"
    UNIT_TESTER = "unit_tester"
    SECURITY_VERIFIER = "security_verifier"
    HOT_MICRO_SPECIALIST = "hot_micro_specialist"
    COLD_DURABLE = "cold_durable"


class AgentType(str, Enum):
    SWARM_WORKER = "swarm_worker"
    HOT_MICRO_SPECIALIST = "hot_micro_specialist"
    COLD_DURABLE = "cold_durable"


@dataclass
class AgentSpec:
    id: str
    name: str
    role: WorkerRole
    agent_type: AgentType
    system_prompt: str
    model_alias: str = "claude-3-7-sonnet"
    max_concurrency: int = 1
    ttl_sec: float | None = None  # None = durable (no expiry); HOT specialists get 300s
    validated_learnings_applied: list[str] = field(default_factory=list)
    memory_context: dict[str, Any] = field(default_factory=dict)
    parent_agent_id: str | None = None
    created_at: float = field(default_factory=time.time)

    @property
    def is_expired(self) -> bool:
        """Return True if this agent has a TTL and has exceeded it."""
        if self.ttl_sec is None:
            return False  # durable — never expires
        return (time.time() - self.created_at) > self.ttl_sec

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["role"] = self.role.value if isinstance(self.role, Enum) else self.role
        d["agent_type"] = self.agent_type.value if isinstance(self.agent_type, Enum) else self.agent_type
        return d


@dataclass
class WorkerPoolConfig:
    pool_name: str = "opencode-swarm-40"
    max_total_workers: int = 40
    role_allocations: dict[str, int] = field(
        default_factory=lambda: {
            WorkerRole.MASTER_ARCHITECT.value: 1,
            WorkerRole.CODEBASE_MAPPER.value: 4,
            WorkerRole.SPEC_GAP_CLOSER.value: 4,
            WorkerRole.CORE_ENGINEER.value: 18,
            WorkerRole.REFACTOR_SPECIALIST.value: 4,
            WorkerRole.UNIT_TESTER.value: 5,
            WorkerRole.SECURITY_VERIFIER.value: 4,
        }
    )


@dataclass
class SpawnChainEntry:
    entry_id: str
    source_learning_id: str
    spawned_agent_id: str
    agent_type: AgentType
    trigger_reason: str
    parent_entry_id: str | None = None
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["agent_type"] = self.agent_type.value if isinstance(self.agent_type, Enum) else self.agent_type
        return d


@dataclass
class WorkerPoolState:
    active_workers: int = 0
    total_assigned: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    workers_by_role: dict[str, list[str]] = field(default_factory=dict)
    pool_health: dict[str, dict] = field(default_factory=dict)

    def record_pool_success(self, pool_id: str) -> None:
        """Increment the completed counter for the given pool."""
        if pool_id not in self.pool_health:
            self.pool_health[pool_id] = {"active": 0, "completed": 0, "failed": 0, "rate_limited": 0}
        self.pool_health[pool_id]["completed"] += 1

    def record_pool_failure(self, pool_id: str, is_rate_limit: bool = False) -> None:
        """Increment the failed or rate_limited counter for the given pool."""
        if pool_id not in self.pool_health:
            self.pool_health[pool_id] = {"active": 0, "completed": 0, "failed": 0, "rate_limited": 0}
        if is_rate_limit:
            self.pool_health[pool_id]["rate_limited"] += 1
        else:
            self.pool_health[pool_id]["failed"] += 1

    def get_pool_summary(self) -> dict[str, dict]:
        """Return a copy of the pool_health dict."""
        return dict(self.pool_health)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
