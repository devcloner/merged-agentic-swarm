"""
OpenCode Swarm Pack Coordinator (40-Worker Pool Manager)
Allocates worker pools across roles, manages parallel execution, and coordinates master architect oversight.
"""
import os
import sys
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from typing import Dict, Any, List, Optional
from models.agent_models import WorkerRole, AgentSpec, AgentType, WorkerPoolConfig, WorkerPoolState
from models.prd_models import SubTask, TaskStatus
from providers.multi_provider_fabric import default_fabric

logger = logging.getLogger("opencode_swarm")

# Pool ID mapping from WorkerRole value to pool health key
_POOL_ID_MAP: Dict[str, str] = {
    WorkerRole.CORE_ENGINEER.value: "domain_module",
    WorkerRole.REFACTOR_SPECIALIST.value: "type_hardening",
    WorkerRole.UNIT_TESTER.value: "test_engineering",
    WorkerRole.SECURITY_VERIFIER.value: "security_a11y",
}

class ConcurrencyRampController:
    """Controls worker concurrency ramp-up across wave gates."""

    ramp_sequence = [4, 8, 16, 24, 40]

    def get_current_max_workers(self, wave_gate_level: int) -> int:
        """Map wave gate level to max workers.

        Gate 0 -> 4, gate 1 -> 8, gate 2 -> 16, gate 3 -> 24, after all gates -> 40.
        """
        if wave_gate_level < 0:
            return self.ramp_sequence[0]
        if wave_gate_level < len(self.ramp_sequence):
            return self.ramp_sequence[wave_gate_level]
        return self.ramp_sequence[-1]

    def get_ramp_sequence(self) -> list[int]:
        """Return the full ramp sequence."""
        return list(self.ramp_sequence)


class OpenCodeSwarmManager:
    def __init__(self, config: Optional[WorkerPoolConfig] = None):
        self.config = config or WorkerPoolConfig()
        self.state = WorkerPoolState()
        self.workers: Dict[str, AgentSpec] = {}
        self.ramp_controller = ConcurrencyRampController()
        self._round_robin_index: Dict[str, int] = {}  # role → next worker index (FIX-12)
        self._initialize_worker_pool()

    def _initialize_worker_pool(self):
        """Initializes the 40 worker specs across role allocations."""
        worker_id_counter = 1
        for role_name, count in self.config.role_allocations.items():
            role_enum = WorkerRole(role_name)
            self.state.workers_by_role[role_name] = []
            for _ in range(count):
                wid = f"opencode-worker-{worker_id_counter:02d}"
                spec = AgentSpec(
                    id=wid,
                    name=f"Swarm Worker ({role_name})",
                    role=role_enum,
                    agent_type=AgentType.SWARM_WORKER,
                    system_prompt=f"You are OpenCode Swarm Worker specializing as {role_name}. Deliver minimal, zero-defect code."
                )
                self.workers[wid] = spec
                self.state.workers_by_role[role_name].append(wid)
                worker_id_counter += 1

        logger.info(f"Initialized OpenCode Swarm pool with {len(self.workers)} workers across 7 roles.")

    def get_available_worker(self, role: WorkerRole) -> Optional[AgentSpec]:
        """Gets an available worker matching the specified role using round-robin (FIX-12)."""
        worker_ids = self.state.workers_by_role.get(role.value, [])
        if worker_ids:
            idx = self._round_robin_index.get(role.value, 0)
            self._round_robin_index[role.value] = (idx + 1) % len(worker_ids)
            return self.workers.get(worker_ids[idx])
        # Fallback to any core engineer worker
        fallback_ids = self.state.workers_by_role.get(WorkerRole.CORE_ENGINEER.value, [])
        if fallback_ids:
            idx = self._round_robin_index.get("core_engineer_fallback", 0)
            self._round_robin_index["core_engineer_fallback"] = (idx + 1) % len(fallback_ids)
            return self.workers.get(fallback_ids[idx])
        return list(self.workers.values())[0] if self.workers else None

    def _get_pool_id(self, role: WorkerRole) -> str:
        """Map a WorkerRole to a pool-health bucket key."""
        return _POOL_ID_MAP.get(role.value, "general")

    def execute_subtask_with_worker(self, subtask: SubTask, role: WorkerRole) -> Dict[str, Any]:
        """Dispatches a single subtask to a worker in the pool."""
        pool_id = self._get_pool_id(role)
        worker = self.get_available_worker(role)
        if not worker:
            self.state.record_pool_failure(pool_id)
            return {"status": "error", "message": "No available worker in pool"}

        subtask.assigned_worker_id = worker.id
        subtask.status = TaskStatus.IN_PROGRESS

        start_time = time.time()
        logger.info(f"Worker {worker.id} ({role.value}) started subtask: {subtask.title}")

        prompt = f"""Task Title: {subtask.title}
Task Description: {subtask.description}
Role: {role.value}

Execute this task and produce required code or verification artifacts.
"""
        try:
            response = default_fabric.dispatch_request(
                model_alias=worker.model_alias,
                messages=[{"role": "user", "content": prompt}],
                system_prompt=worker.system_prompt
            )
        except Exception as e:
            execution_time = time.time() - start_time
            subtask.status = TaskStatus.FAILED
            subtask.error_message = str(e)
            is_rate_limit = "rate" in str(e).lower() or "429" in str(e)
            self.state.record_pool_failure(pool_id, is_rate_limit=is_rate_limit)
            self.state.failed_tasks += 1
            logger.warning(f"Worker {worker.id} ({role.value}) failed subtask: {subtask.title} — {e}")
            return {
                "status": "failed",
                "subtask_id": subtask.id,
                "worker_id": worker.id,
                "role": role.value,
                "execution_time_sec": round(execution_time, 2),
                "error": str(e),
            }

        execution_time = time.time() - start_time
        subtask.status = TaskStatus.COMPLETED
        subtask.completed_at = time.time()

        self.state.completed_tasks += 1
        self.state.record_pool_success(pool_id)
        return {
            "status": "completed",
            "subtask_id": subtask.id,
            "worker_id": worker.id,
            "role": role.value,
            "execution_time_sec": round(execution_time, 2),
            "response": response
        }

    def execute_subtask_batch_parallel(self, subtasks: List[SubTask], role: WorkerRole = WorkerRole.CORE_ENGINEER, wave_gate_level: int = 0) -> List[Dict[str, Any]]:
        """Executes a batch of subtasks in parallel using ThreadPoolExecutor up to max pool capacity."""
        results = []
        max_workers = self.ramp_controller.get_current_max_workers(wave_gate_level)
        with ThreadPoolExecutor(max_workers=min(max_workers, self.config.max_total_workers)) as executor:
            future_to_subtask = {
                executor.submit(self.execute_subtask_with_worker, st, role): st
                for st in subtasks
            }
            for future in as_completed(future_to_subtask):
                try:
                    res = future.result()
                    results.append(res)
                except Exception as e:
                    st = future_to_subtask[future]
                    st.status = TaskStatus.FAILED
                    st.error_message = str(e)
                    self.state.failed_tasks += 1
                    results.append({"status": "failed", "subtask_id": st.id, "error": str(e)})

        return results

# Global Singleton
default_swarm_manager = OpenCodeSwarmManager()
