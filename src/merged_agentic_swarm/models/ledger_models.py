"""
Progress Ledger, Success Markers, and Obstacle Playbooks Models
"""

import time
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class SuccessMarker:
    id: str
    task_id: str
    verifier_name: str
    command_executed: str | None = None
    exit_code: int = 0
    output_summary: str = ""
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ObstaclePlaybookEntry:
    id: str
    error_pattern: str
    category: str
    description: str
    auto_remediation_strategy: str
    trigger_count: int = 0
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ProgressLogEntry:
    entry_id: str
    task_id: str
    subtask_id: str | None
    worker_id: str
    wave_id: int
    action: str
    status: str
    model: str | None = None  # which model/alias served this step (None = not recorded)
    timestamp: float = field(default_factory=time.time)
    tokens_used: int = 0
    learning_generated: str | None = None
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class TaskMasterStateSnapshot:
    session_id: str
    prd_title: str
    total_epics: int
    completed_epics: int
    current_wave: int
    progress_percentage: float
    last_updated: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
