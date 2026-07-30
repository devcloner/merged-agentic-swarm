"""
PRD and Task Master Data Models
"""
import time
from enum import Enum
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field, asdict

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    SPEC_GAP = "spec_gap"
    VERIFYING = "verifying"
    COMPLETED = "completed"
    FAILED = "failed"

class TaskPriority(str, Enum):
    P0_CRITICAL = "P0"
    P1_HIGH = "P1"
    P2_MEDIUM = "P2"
    P3_LOW = "P3"

@dataclass
class SubTask:
    id: str
    title: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    assigned_worker_id: Optional[str] = None
    input_artifacts: List[str] = field(default_factory=list)
    output_artifacts: List[str] = field(default_factory=list)
    error_message: Optional[str] = None
    estimated_turns: int = 1  # complexity estimate for Phase 1 analysis
    created_at: float = field(default_factory=time.time)
    completed_at: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d['status'] = self.status.value if isinstance(self.status, Enum) else self.status
        return d

@dataclass
class EpicTask:
    id: str
    title: str
    description: str
    wave_id: int
    priority: TaskPriority = TaskPriority.P1_HIGH
    status: TaskStatus = TaskStatus.PENDING
    subtasks: List[SubTask] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list) # IDs of prerequisite tasks
    acceptance_criteria: List[str] = field(default_factory=list)
    spec_gaps: List[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d['status'] = self.status.value if isinstance(self.status, Enum) else self.status
        d['priority'] = self.priority.value if isinstance(self.priority, Enum) else self.priority
        d['subtasks'] = [st.to_dict() if hasattr(st, 'to_dict') else st for st in self.subtasks]
        return d

@dataclass
class SpecGap:
    id: str
    epic_id: str
    missing_requirement: str
    affected_files: List[str]
    suggested_fix: str
    resolved: bool = False
    resolution_note: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class PRDDocument:
    raw_text: str
    title: str = "Unassigned PRD"
    version: str = "1.0.0"
    created_at: float = field(default_factory=time.time)

@dataclass
class PRDAnalysisResult:
    title: str
    summary: str
    epics: List[EpicTask] = field(default_factory=list)
    spec_gaps: List[SpecGap] = field(default_factory=list)
    total_estimated_turns: int = 0
    parsed_at: float = field(default_factory=time.time)
    fabric_response_preview: Optional[str] = None  # raw AI response (truncated)

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "title": self.title,
            "summary": self.summary,
            "epics": [epic.to_dict() for epic in self.epics],
            "spec_gaps": [gap.to_dict() for gap in self.spec_gaps],
            "total_estimated_turns": self.total_estimated_turns,
            "parsed_at": self.parsed_at
        }
        if self.fabric_response_preview:
            d["fabric_response_preview"] = self.fabric_response_preview
        return d
