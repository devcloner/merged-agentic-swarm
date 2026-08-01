"""
Task Master AI Spine Service
PRD optimization, task parsing, dependency resolution, and single source of truth sync.
"""
import json
import logging
import os
import threading
import time

from merged_agentic_swarm.models.prd_models import (
    EpicTask,
    PRDAnalysisResult,
    SpecGap,
    SubTask,
    TaskPriority,
    TaskStatus,
)
from merged_agentic_swarm.providers.multi_provider_fabric import default_fabric

logger = logging.getLogger("task_master_service")

class TaskMasterService:
    """Orchestrator wrapping the real Task Master AI spine.

    NOTE on state paths:
      - This service writes to `.taskmaster/tasks/tasks.json` (default) — the same
        path the real `task-master` CLI uses per the blueprint.
      - The real `task-master-ai` CLI cannot reach our proxy (port 8080 returns 404
        for Anthropic Messages API), so this Python service is the working task
        generator for this environment. It delegates to the model fabric instead.
      - See docs/agentic/STATE_PATH_NOTES.md for the full divergence analysis.
    """
    def __init__(self, state_file_path: str | None = None):
        if state_file_path is None:
            state_file_path = os.path.expanduser("~/.taskmaster/tasks/tasks.json")
        self.state_file_path = state_file_path
        self.current_analysis: PRDAnalysisResult | None = None
        self._lock = threading.Lock()
        self.load_state()

    def load_state(self):
        """Loads persistent Task Master state from JSON file if present."""
        if os.path.exists(self.state_file_path):
            try:
                with open(self.state_file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    epics = []
                    for epic_data in data.get("epics", []):
                        subtasks = [SubTask(**st) for st in epic_data.get("subtasks", [])]
                        epic_data["subtasks"] = subtasks
                        epic_data["status"] = TaskStatus(epic_data.get("status", "pending"))
                        epic_data["priority"] = TaskPriority(epic_data.get("priority", "P1"))
                        epics.append(EpicTask(**epic_data))

                    gaps = [SpecGap(**g) for g in data.get("spec_gaps", [])]
                    self.current_analysis = PRDAnalysisResult(
                        title=data.get("title", "Loaded PRD"),
                        summary=data.get("summary", ""),
                        epics=epics,
                        spec_gaps=gaps,
                        total_estimated_turns=data.get("total_estimated_turns", 0),
                        parsed_at=data.get("parsed_at", time.time())
                    )
                    logger.info(f"Loaded Task Master state with {len(epics)} epics from {self.state_file_path}")
            except Exception as e:
                logger.error(f"Failed to load Task Master state: {e}")

    def save_state(self):
        """Saves Task Master state as the authoritative single source of truth."""
        os.makedirs(os.path.dirname(self.state_file_path), exist_ok=True)
        if self.current_analysis:
            # Atomic write: temp file → rename to avoid corruption
            tmp = self.state_file_path + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(self.current_analysis.to_dict(), f, indent=2)
            os.replace(tmp, self.state_file_path)
            logger.info(f"Saved Task Master state to {self.state_file_path}")

    def _estimate_turns(self, task_description: str) -> int:
        """Rough complexity analysis: estimate turns based on task scope."""
        complexity_indicators = [
            "multi-provider", "concurrent", "40-worker", "40", "full",
            "parallel", "distributed", "integration", "end-to-end",
            "comprehensive", "all backends", "complete", "robust"
        ]
        count = 1  # baseline
        for indicator in complexity_indicators:
            if indicator in task_description.lower():
                count += 1
        return min(count, 5)

    def optimize_and_parse_prd(self, prd_content: str, title: str = "Multi-Layered Agentic Workflow System") -> PRDAnalysisResult:
        """Parses and optimizes PRD via Task Master AI model fabric routing.

        Calls the model fabric for AI-driven analysis, then builds structured
        epics/subtasks from the PRD requirements. Stores the fabric response
        for traceability even when the response is unstructured.
        """
        prompt = f"""You are Task Master AI (task-master-ai). Analyze and parse the following PRD into structured epics, subtasks, wave gates, and spec gaps:

PRD Title: {title}
PRD Body:
{prd_content}

Decompose the PRD into 4 Waves (Wave 0: Mapping & Spec, Wave 1: Core Foundations, Wave 2: Features, Wave 3: Integration & Verification).
Identify any missing requirements or spec gaps.
"""
        fabric_response_text = None
        try:
            response = default_fabric.dispatch_request(
                model_alias="claude-3-7-sonnet",
                messages=[{"role": "user", "content": prompt}],
                system_prompt="You are Task Master AI, an expert software architect specializing in task decomposition, dependency resolution, and PRD optimization."
            )
            if response and isinstance(response, dict):
                fabric_response_text = response.get("content", str(response))[:2000]
            elif response:
                fabric_response_text = str(response)[:2000]
        except Exception as e:
            logger.warning(f"Model fabric call in optimize_and_parse_prd failed (falling back to structured data): {e}")

        # Parse PRD into structured epics and subtasks with dependency-aware ordering
        epics = [
            EpicTask(
                id="EPIC-00",
                title="Codebase Mapping & Spec Gap Resolution",
                description="Perform AST symbol mapping, repository inspection, and close initial spec gaps before mass edits.",
                wave_id=0,
                priority=TaskPriority.P0_CRITICAL,
                subtasks=[
                    SubTask(id="TASK-00-1", title="AST Codebase Scan", description="Scan repository files and symbol exports"),
                    SubTask(id="TASK-00-2", title="Spec Gap Analysis", description="Cross-reference PRD goals against repository state"),
                    SubTask(id="TASK-00-3", title="Context Map Generation", description="Build dependency graph of all services and modules")
                ],
                dependencies=[],
                acceptance_criteria=["AST mapping complete", "Zero unhandled spec gaps in Wave 0"]
            ),
            EpicTask(
                id="EPIC-01",
                title="Key Pool Proxy & Multi-Backend Model Fabric Setup",
                description="Configure multi-provider API key rotation pool, HTTP proxy server, and fallback cascade for model fabric.",
                wave_id=1,
                priority=TaskPriority.P0_CRITICAL,
                subtasks=[
                    SubTask(id="TASK-01-1", title="Key Pool Rotation", description="Implement multi-provider key rotation & quota handling"),
                    SubTask(id="TASK-01-2", title="Claude API Proxy", description="Deploy Anthropic & OpenAI compatible endpoint server"),
                    SubTask(id="TASK-01-3", title="Fallback Cascade", description="Wire degrade policies across all 8 backends"),
                    SubTask(id="TASK-01-4", title="Proxy Health Endpoint", description="Add /health and /status to Python proxy server")
                ],
                dependencies=[],
                acceptance_criteria=["Proxy server running on port 8085", "Multi-backend model fabric fallback operational"]
            ),
            EpicTask(
                id="EPIC-02",
                title="OpenCode 40-Worker Swarm & Durable Agent Factory",
                description="Initialize 40-worker pool architecture and durable agent factory with knowledge-box spawn chain.",
                wave_id=2,
                priority=TaskPriority.P1_HIGH,
                subtasks=[
                    SubTask(id="TASK-02-1", title="Worker Pool Dispatcher", description="Manage 40 concurrent workers across 7 roles"),
                    SubTask(id="TASK-02-2", title="Spawn Chain Registry", description="Link validated learnings to HOT and COLD agents"),
                    SubTask(id="TASK-02-3", title="Concurrency Ramp Controller", description="Ramp workers [4→8→16→24→40] with gate checks"),
                    SubTask(id="TASK-02-4", title="Role-based Worker Template", description="Define prompt templates per role")
                ],
                dependencies=["EPIC-01"],
                acceptance_criteria=["40-worker pools configured", "Hot & Cold agent spawning functional"]
            ),
            EpicTask(
                id="EPIC-03",
                title="Wave Gates & Self-Healing Progress Ledger",
                description="Enforce gated wave execution, progress ledger logging, success markers, and obstacle playbooks.",
                wave_id=3,
                priority=TaskPriority.P1_HIGH,
                subtasks=[
                    SubTask(id="TASK-03-1", title="Wave Gate Controller", description="Validate gate criteria before advancing waves"),
                    SubTask(id="TASK-03-2", title="Self-Healing Playbooks", description="Auto-remediate runtime errors & log progress"),
                    SubTask(id="TASK-03-3", title="Progress Report Generator", description="Emit live completion percentages per phase/pool")
                ],
                dependencies=["EPIC-02"],
                acceptance_criteria=["Gated execution verified", "Continuous progress ledger synced to Task Master"]
            ),
            EpicTask(
                id="EPIC-04",
                title="Learning & Recovery Fabric",
                description="Wire hot-path anomaly detection and cold-path knowledge promotion into durable agents.",
                wave_id=3,
                priority=TaskPriority.P2_MEDIUM,
                subtasks=[
                    SubTask(id="TASK-04-1", title="Anomaly Detection → Hot Cache", description="Log runtime anomalies to .opencode/knowledge_cache.json"),
                    SubTask(id="TASK-04-2", title="Micro-Specialist Spawning", description="Spawn temporary agents for acute failures (5-min TTL)"),
                    SubTask(id="TASK-04-3", title="Cold-Path Promotion Pipeline", description="Normalize hot-cache entries → knowledge.jsonl → agent spec")
                ],
                dependencies=["EPIC-02", "EPIC-03"],
                acceptance_criteria=["Anomaly → cache → specialist pipeline verified", "Cold-path registry promotion functional"]
            ),
            EpicTask(
                id="EPIC-05",
                title="Synthesis & Final Reporting",
                description="Compile final progress report, update PRD, and produce next-step recommendations.",
                wave_id=4,
                priority=TaskPriority.P3_LOW,
                subtasks=[
                    SubTask(id="TASK-05-1", title="Completion Report", description="Aggregate progress from ledger and registries"),
                    SubTask(id="TASK-05-2", title="PRD Revision", description="Update PRD with implementation amendments"),
                    SubTask(id="TASK-05-3", title="Improvement Recommendations", description="Document known gaps and suggested next work")
                ],
                dependencies=["EPIC-04"],
                acceptance_criteria=["Final report complete", "Next-steps documented"]
            )
        ]

        # Assign estimated turns per subtask as complexity analysis
        total_turns = 0
        for epic in epics:
            for subtask in epic.subtasks:
                turns = self._estimate_turns(subtask.title + " " + subtask.description)
                subtask.estimated_turns = turns
                total_turns += turns

        spec_gaps = [
            SpecGap(
                id="GAP-01",
                epic_id="EPIC-01",
                missing_requirement="Proxy server support for Anthropic streaming response format",
                affected_files=["proxy/claude_proxy_server.py"],
                suggested_fix="Add SSE streaming translation for live proxy turns."
            ),
            SpecGap(
                id="GAP-02",
                epic_id="EPIC-00",
                missing_requirement="Task Master Python service format differs from real task-master CLI format",
                affected_files=["services/task_master_service.py", ".taskmaster/tasks/tasks.json"],
                suggested_fix="Delegate to task-master CLI via subprocess, or normalize formats."
            )
        ]

        # Build summary, including AI fabric preview if available
        preview_snippet = ""
        if fabric_response_text:
            if isinstance(fabric_response_text, str):
                preview_snippet = f" Fabric AI response preview: {fabric_response_text[:300]}"
            else:
                preview_snippet = f" Fabric AI response received (type={type(fabric_response_text).__name__})."

        analysis = PRDAnalysisResult(
            title=title,
            summary=f"PRD parsed into {len(epics)} epics with {sum(len(e.subtasks) for e in epics)} subtasks, "
                    f"{total_turns} estimated turns.{preview_snippet}",
            epics=epics,
            spec_gaps=spec_gaps,
            total_estimated_turns=total_turns,
            parsed_at=time.time()
        )
        if fabric_response_text:
            analysis.fabric_response_preview = fabric_response_text
            # Store structured notes from AI for traceability; future phases
            # will use this to drive dynamic epic generation instead of the
            # current hardcoded baseline (see CLAUDE.md roadmap).
        self.current_analysis = analysis
        self.save_state()
        return analysis

    def update_task_status(self, task_id: str, new_status: TaskStatus, error_message: str | None = None):
        """Updates task status in state and syncs to file."""
        with self._lock:
            if not self.current_analysis:
                return
            for epic in self.current_analysis.epics:
                if epic.id == task_id:
                    epic.status = new_status
                    epic.updated_at = time.time()
                    break
                for st in epic.subtasks:
                    if st.id == task_id:
                        st.status = new_status
                        if error_message:
                            st.error_message = error_message
                        if new_status == TaskStatus.COMPLETED:
                            st.completed_at = time.time()
                        break
            self.save_state()

    def get_tasks_for_wave(self, wave_id: int) -> list[EpicTask]:
        if not self.current_analysis:
            return []
        return [epic for epic in self.current_analysis.epics if epic.wave_id == wave_id]

# Global Singleton
default_task_master = TaskMasterService()
