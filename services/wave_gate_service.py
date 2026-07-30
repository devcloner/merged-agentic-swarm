"""
Wave Gates Controller Service
Enforces gated phase boundaries (Wave 0 to Wave 3) with pre-condition and post-condition verification.
"""
import os
import sys
import time
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from typing import Dict, Any, List, Optional, Tuple
from models.wave_models import WavePhase, WaveStatus, WaveGateCriteria, WaveExecutionState
from services.task_master_service import default_task_master
from services.codebase_map_service import default_codebase_mapper

logger = logging.getLogger("wave_gate")

class WaveGateController:
    def __init__(self):
        self.waves: Dict[int, WaveExecutionState] = {
            0: WaveExecutionState(
                wave_id=0,
                name="Wave 0: Codebase Mapping & Spec Gap Gate",
                gate_criteria=WaveGateCriteria(0, "Codebase Mapped & Gaps Closed", spec_gaps_closed=True)
            ),
            1: WaveExecutionState(
                wave_id=1,
                name="Wave 1: Key Pool Proxy & Fabric Gate",
                gate_criteria=WaveGateCriteria(1, "Proxy & Fabric Operational", required_tasks_completed=True)
            ),
            2: WaveExecutionState(
                wave_id=2,
                name="Wave 2: Swarm & Agent Factory Feature Gate",
                gate_criteria=WaveGateCriteria(2, "Swarm Work Completed", required_tasks_completed=True)
            ),
            3: WaveExecutionState(
                wave_id=3,
                name="Wave 3: Integration & Verification Gate",
                gate_criteria=WaveGateCriteria(3, "Full Verification & Zero Defect", zero_syntax_errors=True, tests_passing=True)
            ),
        }
        self.current_wave: int = 0
        self.waves[0].status = WaveStatus.IN_PROGRESS
        self.waves[0].started_at = time.time()

    def get_wave_state(self, wave_id: int) -> WaveExecutionState:
        return self.waves.get(wave_id, self.waves[0])

    def evaluate_gate_criteria(self, wave_id: int) -> Tuple[bool, List[str]]:
        """Evaluates whether all criteria for a wave gate are met."""
        state = self.waves.get(wave_id)
        if not state:
            return False, ["Invalid wave ID"]

        reasons = []

        if wave_id == 0:
            # Wave 0 gate: Codebase scan done, spec gaps closed
            gaps = default_codebase_mapper.spec_gaps
            unresolved = [g for g in gaps if not g.resolved]
            if unresolved:
                reasons.append(f"{len(unresolved)} unresolved spec gaps remaining in Wave 0.")

        elif wave_id in (1, 2, 3):
            # Check Task Master tasks for this wave
            wave_tasks = default_task_master.get_tasks_for_wave(wave_id)
            incomplete = [t for t in wave_tasks if t.status.value != "completed"]
            if incomplete:
                reasons.append(f"{len(incomplete)} epic tasks still incomplete in Wave {wave_id}.")

        passed = len(reasons) == 0
        return passed, reasons

    def advance_wave(self) -> Tuple[bool, str]:
        """Attempts to pass the current wave gate and advance to the next wave."""
        passed, reasons = self.evaluate_gate_criteria(self.current_wave)
        curr_state = self.waves[self.current_wave]

        if not passed:
            curr_state.status = WaveStatus.FAILED
            curr_state.failure_reason = "; ".join(reasons)
            logger.warning(f"Gate verification failed for Wave {self.current_wave}: {curr_state.failure_reason}")
            return False, curr_state.failure_reason

        # Mark current wave as passed
        curr_state.status = WaveStatus.PASSED
        curr_state.passed_at = time.time()
        logger.info(f"Gate PASSED for {curr_state.name}")

        # Advance to next wave if available
        if self.current_wave < 3:
            self.current_wave += 1
            next_state = self.waves[self.current_wave]
            next_state.status = WaveStatus.IN_PROGRESS
            next_state.started_at = time.time()
            logger.info(f"Advanced to {next_state.name}")
            return True, f"Advanced to Wave {self.current_wave}"
        else:
            return True, "All Wave Gates successfully passed!"

# Global Singleton
default_wave_controller = WaveGateController()
