"""
Wave Gates Controller Service
Enforces gated phase boundaries (Wave 0 to Wave 3) with pre-condition and post-condition verification.
"""

import fnmatch
import json
import logging
import os
import time

from merged_agentic_swarm.models.prd_models import SubTask
from merged_agentic_swarm.models.wave_models import WaveExecutionState, WaveGateCriteria, WaveStatus
from merged_agentic_swarm.services.codebase_map_service import default_codebase_mapper
from merged_agentic_swarm.services.task_master_service import default_task_master

logger = logging.getLogger("wave_gate")


class WaveGateController:
    def __init__(self):
        self.waves: dict[int, WaveExecutionState] = {
            0: WaveExecutionState(
                wave_id=0,
                name="Wave 0: Codebase Mapping & Spec Gap Gate",
                gate_criteria=WaveGateCriteria(0, "Codebase Mapped & Gaps Closed", spec_gaps_closed=True),
            ),
            1: WaveExecutionState(
                wave_id=1,
                name="Wave 1: Key Pool Proxy & Fabric Gate",
                gate_criteria=WaveGateCriteria(1, "Proxy & Fabric Operational", required_tasks_completed=True),
            ),
            2: WaveExecutionState(
                wave_id=2,
                name="Wave 2: Swarm & Agent Factory Feature Gate",
                gate_criteria=WaveGateCriteria(2, "Swarm Work Completed", required_tasks_completed=True),
            ),
            3: WaveExecutionState(
                wave_id=3,
                name="Wave 3: Integration & Verification Gate",
                gate_criteria=WaveGateCriteria(
                    3, "Full Verification & Zero Defect", zero_syntax_errors=True, tests_passing=True
                ),
            ),
            4: WaveExecutionState(
                wave_id=4,
                name="Wave 4: Synthesis & Final Reporting Gate",
                gate_criteria=WaveGateCriteria(4, "Synthesis & Reporting Complete", required_tasks_completed=True),
            ),
        }
        self._max_wave = 4
        self.current_wave: int = 0
        self.waves[0].status = WaveStatus.IN_PROGRESS
        self.waves[0].started_at = time.time()

    def get_wave_state(self, wave_id: int) -> WaveExecutionState:
        return self.waves.get(wave_id, self.waves[0])

    def _check_ownership(self, subtasks: list[SubTask], pool_id: str) -> list[str]:
        """Verify each subtask's output paths against the ownership map for pool_id.

        Checks that every output_artifact falls within the pool's owned_paths
        and does not match any forbidden_paths. Returns a list of violation
        descriptions (empty = all valid).
        """
        # Locate ownership-map.json — use codebase mapper's repo root so tests can isolate
        base = default_codebase_mapper.repo_root
        candidates = [
            os.path.join(base, ".opencode", "ownership-map.json"),
            os.path.join(base, "docs", "agentic", "registry", "ownership-map.json"),
        ]
        ownership_map = None
        for path in candidates:
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        ownership_map = json.load(f)
                except Exception as exc:
                    return [f"Failed to read ownership map at {path}: {exc}"]
                break

        if ownership_map is None:
            return ["Ownership map not found (checked .opencode/ and docs/agentic/registry/)"]

        # Find the pool config
        pool_config = None
        for pool in ownership_map.get("pools", []):
            if pool.get("pool_id") == pool_id:
                pool_config = pool
                break

        if pool_config is None:
            return [f"Pool '{pool_id}' not found in ownership map"]

        owned_paths = pool_config.get("owned_paths", [])
        forbidden_paths = pool_config.get("forbidden_paths", [])

        violations: list[str] = []
        for subtask in subtasks:
            for output_path in subtask.output_artifacts:
                # Check forbidden paths first
                for pattern in forbidden_paths:
                    if fnmatch.fnmatch(output_path, pattern):
                        violations.append(
                            f"Subtask '{subtask.id}' output '{output_path}' matches "
                            f"forbidden path '{pattern}' for pool '{pool_id}'"
                        )

                # Check that output falls within owned paths (if pool has any defined)
                if owned_paths and not any(fnmatch.fnmatch(output_path, p) for p in owned_paths):
                    violations.append(
                        f"Subtask '{subtask.id}' output '{output_path}' is outside owned paths for pool '{pool_id}'"
                    )

        return violations

    def evaluate_gate_criteria(self, wave_id: int) -> tuple[bool, list[str]]:
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

            # Ownership enforcement: verify subtask output paths against ownership map
            wave_pool_map = {
                1: "domain-module-workers",
                2: "ast-type-hardening-workers",
                3: "security-a11y-auditors",
            }
            pool_id = wave_pool_map.get(wave_id)
            if pool_id:
                subtasks = []
                for epic in wave_tasks:
                    subtasks.extend(epic.subtasks)
                violations = self._check_ownership(subtasks, pool_id)
                reasons.extend(violations)

        passed = len(reasons) == 0
        return passed, reasons

    def advance_wave(self) -> tuple[bool, str]:
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
        if self.current_wave < self._max_wave:
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
