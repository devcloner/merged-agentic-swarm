"""
OpenCode Swarm Pack Coordinator (40-Worker Pool Manager)
Allocates worker pools across roles, manages parallel execution, and coordinates master architect oversight.

Includes DurableAgentRouter — matches incoming tasks to promoted durable agents
based on category and keyword overlap, then routes to the best-matching agent.
"""
import json
import logging
import os
import re
import sys
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from typing import Any

from merged_agentic_swarm.models.agent_models import AgentSpec, AgentType, WorkerPoolConfig, WorkerPoolState, WorkerRole
from merged_agentic_swarm.models.prd_models import SubTask, TaskStatus
from merged_agentic_swarm.providers.multi_provider_fabric import default_fabric

logger = logging.getLogger("opencode_swarm")

# ── Durable Agent Router ─────────────────────────────────────────────────────
# Matches incoming subtasks to promoted durable agents via category + keyword
# overlap.  When a match scores above the threshold, the durable agent's
# system prompt and the agent file on disk are used instead of a generic worker.


class DurableAgentRouter:
    """Loads promoted durable agents from registry and disk, then matches
    incoming tasks to the best agent by category and keyword overlap."""

    # Minimum score for a match to be considered "routed"
    MIN_SCORE = 1.0
    # Weights for scoring components
    W_CATEGORY = 2.0   # exact category match
    W_KEYWORD = 1.0    # per keyword hit in title+description

    def __init__(self, agents_jsonl: str | None = None, agents_dir: str | None = None):
        self._repo_root = Path(__file__).resolve().parent.parent
        self._agents_jsonl = agents_jsonl or str(
            self._repo_root / "docs/agentic/registry/agents.jsonl"
        )
        self._agents_dir = agents_dir or str(self._repo_root / ".claude/agents")
        self._agents: list[dict[str, Any]] = []
        self._category_index: dict[str, list[dict[str, Any]]] = defaultdict(list)
        self._loaded = False

    # ── Loading ──────────────────────────────────────────────────────────

    def load(self) -> int:
        """Load all durable agents from agents.jsonl and .claude/agents/*.md.
        Returns the count of loaded agents."""
        self._agents.clear()
        self._category_index.clear()
        seen_ids: set[str] = set()

        # 1) From agents.jsonl registry (authoritative for promoted agents)
        if os.path.isfile(self._agents_jsonl):
            try:
                with open(self._agents_jsonl) as fh:
                    for line in fh:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            entry = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        aid = entry.get("id", "")
                        if aid and aid not in seen_ids:
                            seen_ids.add(aid)
                            self._agents.append(entry)
                            cat = entry.get("category", "uncategorized")
                            self._category_index[cat].append(entry)
            except OSError:
                pass

        # 2) From .claude/agents/*.md (frontmatter — supplementary)
        agents_dir_path = Path(self._agents_dir)
        if agents_dir_path.is_dir():
            for md_file in agents_dir_path.glob("*.md"):
                try:
                    fm = self._parse_frontmatter(md_file)
                    if fm and fm.get("name"):
                        aid = fm.get("name", "")
                        if aid not in seen_ids:
                            seen_ids.add(aid)
                            entry = {
                                "id": aid,
                                "name": fm.get("name", ""),
                                "category": fm.get("category", "uncategorized"),
                                "derived_from_learnings": [],
                                "system_prompt": fm.get("description", ""),
                                "promoted_at": fm.get("promoted_at"),
                                "source_file": str(md_file),
                                "body": self._read_body(md_file),
                            }
                            self._agents.append(entry)
                            self._category_index[entry["category"]].append(entry)
                except Exception:
                    continue

        self._loaded = True
        logger.info(f"DurableAgentRouter loaded {len(self._agents)} agents across "
                     f"{len(self._category_index)} categories.")
        return len(self._agents)

    def _parse_frontmatter(self, path: Path) -> dict[str, Any] | None:
        """Extract YAML-style frontmatter between --- markers."""
        text = path.read_text()
        if not text.startswith("---"):
            return None
        end = text.find("---", 3)
        if end == -1:
            return None
        fm_block = text[3:end].strip()
        result: dict[str, Any] = {}
        for line in fm_block.split("\n"):
            if ":" in line:
                key, _, val = line.partition(":")
                result[key.strip()] = val.strip()
        return result

    def _read_body(self, path: Path) -> str:
        """Read the body content after frontmatter."""
        text = path.read_text()
        if not text.startswith("---"):
            return text
        end = text.find("---", 3)
        if end == -1:
            return text
        return text[end + 3:].strip()

    # ── Keyword extraction ────────────────────────────────────────────────

    @staticmethod
    def _extract_keywords(text: str) -> set[str]:
        """Extract lowercase alphanumeric tokens, dropping very short/common words."""
        STOP = {"the", "a", "an", "is", "of", "in", "to", "for", "and", "or",
                "on", "at", "with", "by", "from", "be", "it", "we", "you", "not",
                "this", "that", "are", "was", "has", "have", "do", "does", "will",
                "can", "all", "as", "if", "no", "so", "but", "its", "just", "only",
                "also", "then", "than", "when", "what", "which", "how"}
        tokens = set()
        for word in re.findall(r"[a-z0-9_]{3,}", text.lower()):
            if word not in STOP:
                tokens.add(word)
        return tokens

    def _scan_agent_triggers(self, agent: dict[str, Any]) -> set[str]:
        """Collect trigger keywords from an agent's body (Trigger section) + system_prompt."""
        triggers: set[str] = set()
        body = agent.get("body", "")
        if body:
            # Extract the Trigger line
            for line in body.split("\n"):
                stripped = line.strip()
                if stripped.lower().startswith("activate when") or stripped.lower().startswith("trigger"):
                    triggers.update(self._extract_keywords(stripped))
            # Also scan entire body for keywords
            triggers.update(self._extract_keywords(body))
        # Add system_prompt keywords
        sp = agent.get("system_prompt", "")
        if sp:
            triggers.update(self._extract_keywords(sp))
        return triggers

    # ── Matching ───────────────────────────────────────────────────────────

    def find_matching_agent(self, task: SubTask) -> dict[str, Any] | None:
        """Find the best-matching durable agent for a subtask.

        Returns: agent dict with extra keys `_score` and `_reason`, or None.
        """
        if not self._loaded:
            self.load()

        task_text = f"{task.title} {task.description}"
        task_keywords = self._extract_keywords(task_text)
        task_cat = getattr(task, "category", None) or ""

        best_agent: dict[str, Any] | None = None
        best_score = 0.0

        for agent in self._agents:
            score = 0.0
            reasons: list[str] = []

            # Category match
            agent_cat = agent.get("category", "uncategorized")
            if task_cat and agent_cat == task_cat:
                score += self.W_CATEGORY
                reasons.append(f"category={agent_cat}")

            # Keyword overlap
            agent_triggers = self._scan_agent_triggers(agent)
            overlapping = task_keywords & agent_triggers
            if overlapping:
                score += self.W_KEYWORD * len(overlapping)
                reasons.append(f"keywords={','.join(sorted(list(overlapping)[:5]))}")

            if score > best_score:
                best_score = score
                best_agent = agent
                best_agent["_score"] = score
                best_agent["_reason"] = "; ".join(reasons) if reasons else "fallback"

        if best_agent and best_score >= self.MIN_SCORE:
            return best_agent
        return None

    def get_stats(self) -> dict[str, Any]:
        """Return router statistics for reporting."""
        return {
            "total_agents": len(self._agents),
            "categories": list(self._category_index.keys()),
            "category_counts": {k: len(v) for k, v in self._category_index.items()},
            "loaded": self._loaded,
        }


# Global singleton router
_durable_router: DurableAgentRouter | None = None


def get_durable_router() -> DurableAgentRouter:
    """Lazy-initialised singleton for the durable agent router."""
    global _durable_router
    if _durable_router is None:
        _durable_router = DurableAgentRouter()
        _durable_router.load()
    return _durable_router

# Pool ID mapping from WorkerRole value to pool health key
_POOL_ID_MAP: dict[str, str] = {
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
    def __init__(self, config: WorkerPoolConfig | None = None):
        self.config = config or WorkerPoolConfig()
        self.state = WorkerPoolState()
        self.workers: dict[str, AgentSpec] = {}
        self.ramp_controller = ConcurrencyRampController()
        self._round_robin_index: dict[str, int] = {}  # role → next worker index (FIX-12)
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

    def get_available_worker(self, role: WorkerRole) -> AgentSpec | None:
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

    def execute_subtask_with_worker(self, subtask: SubTask, role: WorkerRole) -> dict[str, Any]:
        """Dispatches a single subtask — first checks for a matching durable agent,
        then falls back to the generic worker pool."""
        pool_id = self._get_pool_id(role)
        routed_agent_id: str | None = None
        routed_agent_score: float = 0.0

        # ── Durable-agent routing hook (FIX-13) ──────────────────────────
        system_prompt = None
        try:
            router = get_durable_router()
            matched = router.find_matching_agent(subtask)
            if matched:
                routed_agent_id = matched.get("id", "")
                routed_agent_score = matched.get("_score", 0.0)
                system_prompt = matched.get("system_prompt", "")
                # If the agent has a body (from .md file), prepend it
                body = matched.get("body", "")
                if body:
                    system_prompt = f"{system_prompt}\n\n---\n{body}"
                logger.info(
                    "Routed subtask '%s' → durable agent %s (score=%.1f, %s)",
                    subtask.title, routed_agent_id, routed_agent_score,
                    matched.get("_reason", "unknown"),
                )
        except Exception:
            pass  # Router failure must not block dispatch

        if not system_prompt:
            worker = self.get_available_worker(role)
            if not worker:
                self.state.record_pool_failure(pool_id)
                return {"status": "error", "message": "No available worker in pool"}
            system_prompt = worker.system_prompt
            worker_id = worker.id
        else:
            worker_id = f"durable-agent:{routed_agent_id or 'unknown'}"

        subtask.assigned_worker_id = worker_id
        subtask.status = TaskStatus.IN_PROGRESS

        start_time = time.time()
        logger.info(f"Worker {worker_id} ({role.value}) started subtask: {subtask.title}")

        prompt = f"""Task Title: {subtask.title}
Task Description: {subtask.description}
Role: {role.value}

Execute this task and produce required code or verification artifacts.
"""
        try:
            response = default_fabric.dispatch_request(
                model_alias=WorkerRole.CORE_ENGINEER.value,  # routed agent uses default tier
                messages=[{"role": "user", "content": prompt}],
                system_prompt=system_prompt,
            )
        except Exception as e:
            execution_time = time.time() - start_time
            subtask.status = TaskStatus.FAILED
            subtask.error_message = str(e)
            is_rate_limit = "rate" in str(e).lower() or "429" in str(e)
            self.state.record_pool_failure(pool_id, is_rate_limit=is_rate_limit)
            self.state.failed_tasks += 1
            logger.warning(f"Worker {worker_id} ({role.value}) failed subtask: {subtask.title} — {e}")
            return {
                "status": "failed",
                "subtask_id": subtask.id,
                "worker_id": worker_id,
                "role": role.value,
                "execution_time_sec": round(execution_time, 2),
                "error": str(e),
            }

        execution_time = time.time() - start_time
        subtask.status = TaskStatus.COMPLETED
        subtask.completed_at = time.time()

        self.state.completed_tasks += 1
        self.state.record_pool_success(pool_id)
        result = {
            "status": "completed",
            "subtask_id": subtask.id,
            "worker_id": worker_id,
            "role": role.value,
            "execution_time_sec": round(execution_time, 2),
            "response": response,
        }
        if routed_agent_id:
            result["routed_agent"] = routed_agent_id
            result["routed_agent_score"] = routed_agent_score
        return result

    def execute_subtask_batch_parallel(self, subtasks: list[SubTask], role: WorkerRole = WorkerRole.CORE_ENGINEER, wave_gate_level: int = 0) -> list[dict[str, Any]]:
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
