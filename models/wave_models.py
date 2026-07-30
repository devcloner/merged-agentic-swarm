"""
Wave Gates Data Models
"""
import time
from enum import Enum
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field, asdict

class WavePhase(int, Enum):
    WAVE_0_MAPPING_SPEC = 0
    WAVE_1_FOUNDATIONS = 1
    WAVE_2_CORE_FEATURES = 2
    WAVE_3_INTEGRATION_VERIFICATION = 3

class WaveStatus(str, Enum):
    LOCKED = "locked"
    IN_PROGRESS = "in_progress"
    PASSED = "passed"
    FAILED = "failed"

@dataclass
class WaveGateCriteria:
    wave_id: int
    name: str
    required_tasks_completed: bool = True
    spec_gaps_closed: bool = True
    zero_syntax_errors: bool = True
    tests_passing: bool = True
    security_audited: bool = False
    custom_checks: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class WaveExecutionState:
    wave_id: int
    name: str
    status: WaveStatus = WaveStatus.LOCKED
    tasks_assigned: List[str] = field(default_factory=list)
    tasks_completed: List[str] = field(default_factory=list)
    gate_criteria: WaveGateCriteria = field(default_factory=lambda: WaveGateCriteria(0, "Default Gate"))
    started_at: Optional[float] = None
    passed_at: Optional[float] = None
    failure_reason: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d['status'] = self.status.value if isinstance(self.status, Enum) else self.status
        d['gate_criteria'] = self.gate_criteria.to_dict() if hasattr(self.gate_criteria, 'to_dict') else self.gate_criteria
        return d
