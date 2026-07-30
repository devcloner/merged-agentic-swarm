"""
Agent, Worker Pool, and Spawn Chain Data Models
"""
import time
from enum import Enum
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field, asdict

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
    validated_learnings_applied: List[str] = field(default_factory=list)
    memory_context: Dict[str, Any] = field(default_factory=dict)
    parent_agent_id: Optional[str] = None
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d['role'] = self.role.value if isinstance(self.role, Enum) else self.role
        d['agent_type'] = self.agent_type.value if isinstance(self.agent_type, Enum) else self.agent_type
        return d

@dataclass
class WorkerPoolConfig:
    pool_name: str = "opencode-swarm-40"
    max_total_workers: int = 40
    role_allocations: Dict[str, int] = field(default_factory=lambda: {
        WorkerRole.MASTER_ARCHITECT.value: 1,
        WorkerRole.CODEBASE_MAPPER.value: 4,
        WorkerRole.SPEC_GAP_CLOSER.value: 4,
        WorkerRole.CORE_ENGINEER.value: 18,
        WorkerRole.REFACTOR_SPECIALIST.value: 4,
        WorkerRole.UNIT_TESTER.value: 5,
        WorkerRole.SECURITY_VERIFIER.value: 4,
    })

@dataclass
class SpawnChainEntry:
    entry_id: str
    source_learning_id: str
    spawned_agent_id: str
    agent_type: AgentType
    trigger_reason: str
    parent_entry_id: Optional[str] = None
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d['agent_type'] = self.agent_type.value if isinstance(self.agent_type, Enum) else self.agent_type
        return d

@dataclass
class WorkerPoolState:
    active_workers: int = 0
    total_assigned: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    workers_by_role: Dict[str, List[str]] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
