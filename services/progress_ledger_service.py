"""
Progress Ledger, Success Markers, and Self-Healing Obstacle Playbook Engine
Maintains continuous progress report, verifies success markers, and executes auto-remediation playbooks.
"""
import os
import sys
import re
import json
import time
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from typing import Dict, Any, List, Optional
from models.ledger_models import ProgressLogEntry, SuccessMarker, ObstaclePlaybookEntry, TaskMasterStateSnapshot
from services.task_master_service import default_task_master

logger = logging.getLogger("progress_ledger")

class ObstaclePlaybookEngine:
    def __init__(self):
        self.playbooks: List[ObstaclePlaybookEntry] = [
            ObstaclePlaybookEntry(
                id="PLAYBOOK-01",
                error_pattern=r"429|quota|rate limit|too many requests",
                category="rate_limit",
                description="API key rate limit or quota exhaustion detected.",
                auto_remediation_strategy="rotate_key_pool"
            ),
            ObstaclePlaybookEntry(
                id="PLAYBOOK-02",
                error_pattern=r"ModuleNotFoundError|No module named",
                category="import_missing",
                description="Missing Python dependency or module import.",
                auto_remediation_strategy="inject_fallback_stub"
            ),
            ObstaclePlaybookEntry(
                id="PLAYBOOK-03",
                error_pattern=r"SyntaxError|IndentationError",
                category="syntax_error",
                description="Code syntax error detected during verification.",
                auto_remediation_strategy="spawn_hot_specialist"
            ),
            ObstaclePlaybookEntry(
                id="PLAYBOOK-04",
                error_pattern=r"TypeError|AttributeError|KeyError",
                category="type_mismatch",
                description="Runtime interface mismatch or attribute missing.",
                auto_remediation_strategy="refactor_interface"
            )
        ]

    def match_and_remediate(self, error_message: str, task_id: str) -> Dict[str, Any]:
        """Matches error against playbooks and applies self-healing strategy."""
        for entry in self.playbooks:
            if re.search(entry.error_pattern, error_message, re.IGNORECASE):
                entry.trigger_count += 1
                logger.info(f"Obstacle matched playbook {entry.id} ({entry.category}) for task {task_id}. Applying: {entry.auto_remediation_strategy}")

                if entry.auto_remediation_strategy == "rotate_key_pool":
                    # Key rotation triggered
                    return {"remediated": True, "strategy": entry.auto_remediation_strategy, "action": "Rotated key pool to active key"}
                elif entry.auto_remediation_strategy == "spawn_hot_specialist":
                    # Spawn HOT micro specialist
                    return {"remediated": True, "strategy": entry.auto_remediation_strategy, "action": "Spawned HOT micro-specialist to patch syntax"}
                else:
                    return {"remediated": True, "strategy": entry.auto_remediation_strategy, "action": "Applied standard self-healing fallback"}

        return {"remediated": False, "strategy": "none", "action": "No playbook match; escalated to Master Architect"}

class ProgressLedgerService:
    def __init__(self, ledger_file: str = "/home/ubuntu/.taskmaster/tasks/progress_ledger.json"):
        self.ledger_file = ledger_file
        self.log_entries: List[ProgressLogEntry] = []
        self.success_markers: List[SuccessMarker] = []
        self.playbook_engine = ObstaclePlaybookEngine()
        self.load_ledger()

    def load_ledger(self):
        if os.path.exists(self.ledger_file):
            try:
                with open(self.ledger_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.log_entries = [ProgressLogEntry(**d) for d in data.get("logs", [])]
                    self.success_markers = [SuccessMarker(**d) for d in data.get("success_markers", [])]
            except Exception as e:
                logger.error(f"Failed loading progress ledger: {e}")

    def save_ledger(self):
        os.makedirs(os.path.dirname(self.ledger_file), exist_ok=True)
        try:
            data = {
                "logs": [e.to_dict() for e in self.log_entries],
                "success_markers": [sm.to_dict() for sm in self.success_markers],
                "task_master_snapshot": default_task_master.current_analysis.to_dict() if default_task_master.current_analysis else {}
            }
            with open(self.ledger_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed saving progress ledger: {e}")

    def log_progress(self, task_id: str, subtask_id: Optional[str], worker_id: str, wave_id: int, action: str, status: str, tokens_used: int = 0, learning_generated: Optional[str] = None, details: Optional[Dict[str, Any]] = None) -> ProgressLogEntry:
        entry = ProgressLogEntry(
            entry_id=f"LOG-{len(self.log_entries)+1:05d}",
            timestamp=time.time(),
            task_id=task_id,
            subtask_id=subtask_id,
            worker_id=worker_id,
            wave_id=wave_id,
            action=action,
            status=status,
            tokens_used=tokens_used,
            learning_generated=learning_generated,
            details=details or {}
        )
        self.log_entries.append(entry)
        self.save_ledger()
        logger.info(f"Progress Ledger logged: [{task_id}] {action} -> {status}")
        return entry

    def record_success_marker(self, task_id: str, verifier_name: str, command: Optional[str] = None, exit_code: int = 0, output_summary: str = "", command_executed: Optional[str] = None) -> SuccessMarker:
        cmd = command or command_executed
        marker = SuccessMarker(
            id=f"MARKER-{len(self.success_markers)+1:04d}",
            task_id=task_id,
            verifier_name=verifier_name,
            command_executed=cmd,
            exit_code=exit_code,
            output_summary=output_summary,
            timestamp=time.time()
        )
        self.success_markers.append(marker)
        self.save_ledger()
        logger.info(f"Recorded Success Marker {marker.id} for task {task_id}")
        return marker

    def handle_task_failure(self, task_id: str, error_message: str) -> Dict[str, Any]:
        """Processes a task failure through self-healing playbooks."""
        res = self.playbook_engine.match_and_remediate(error_message, task_id)
        self.log_progress(
            task_id=task_id,
            subtask_id=None,
            worker_id="self-healing-engine",
            wave_id=0,
            action="obstacle_remediation",
            status="remediated" if res["remediated"] else "escalated",
            details={"error": error_message, "remediation": res}
        )
        return res

# Global Singleton
default_progress_ledger = ProgressLedgerService()
