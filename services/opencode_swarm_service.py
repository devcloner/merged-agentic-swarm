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

class OpenCodeSwarmManager:
    def __init__(self, config: Optional[WorkerPoolConfig] = None):
        self.config = config or WorkerPoolConfig()
        self.state = WorkerPoolState()
        self.workers: Dict[str, AgentSpec] = {}
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
        """Gets an available worker matching the specified role."""
        worker_ids = self.state.workers_by_role.get(role.value, [])
        if worker_ids:
            # Pick first worker (round-robin simulation)
            return self.workers.get(worker_ids[0])
        # Fallback to any core engineer worker
        fallback_ids = self.state.workers_by_role.get(WorkerRole.CORE_ENGINEER.value, [])
        if fallback_ids:
            return self.workers.get(fallback_ids[0])
        return list(self.workers.values())[0] if self.workers else None

    def execute_subtask_with_worker(self, subtask: SubTask, role: WorkerRole) -> Dict[str, Any]:
        """Dispatches a single subtask to a worker in the pool."""
        worker = self.get_available_worker(role)
        if not worker:
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
        response = default_fabric.dispatch_request(
            model_alias=worker.model_alias,
            messages=[{"role": "user", "content": prompt}],
            system_prompt=worker.system_prompt
        )

        execution_time = time.time() - start_time
        subtask.status = TaskStatus.COMPLETED
        subtask.completed_at = time.time()

        self.state.completed_tasks += 1
        return {
            "status": "completed",
            "subtask_id": subtask.id,
            "worker_id": worker.id,
            "role": role.value,
            "execution_time_sec": round(execution_time, 2),
            "response": response
        }

    def execute_subtask_batch_parallel(self, subtasks: List[SubTask], role: WorkerRole = WorkerRole.CORE_ENGINEER, max_workers: int = 10) -> List[Dict[str, Any]]:
        """Executes a batch of subtasks in parallel using ThreadPoolExecutor up to max pool capacity."""
        results = []
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
