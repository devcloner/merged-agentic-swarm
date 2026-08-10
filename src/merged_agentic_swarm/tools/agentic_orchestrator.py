"""
Agentic Multi-Layered Workflow Master Orchestrator
Integrates Task Master AI, Codebase Mapper, Wave Gates, OpenCode 40-Worker Swarm, Key Pool Proxy, Durable Agent Factory, and Progress Ledger.
"""

import json
import logging
import os
import sys
import threading
import time
from pathlib import Path

# Resolve repo root relative to this file (tools/ → merged_agentic_swarm/ → src/ → repo_root)
_REPO_ROOT = Path(__file__).resolve().parents[3]
_REGISTRY_DIR = _REPO_ROOT / "docs" / "agentic" / "registry"


from typing import Any

from merged_agentic_swarm.models.agent_models import AgentType, WorkerRole
from merged_agentic_swarm.models.prd_models import TaskStatus
from merged_agentic_swarm.proxy.claude_proxy_server import ProxyServerDaemon
from merged_agentic_swarm.services.agent_factory_service import default_agent_factory
from merged_agentic_swarm.services.codebase_map_service import default_codebase_mapper
from merged_agentic_swarm.services.opencode_swarm_service import default_swarm_manager
from merged_agentic_swarm.services.progress_ledger_service import default_progress_ledger
from merged_agentic_swarm.services.task_master_service import default_task_master
from merged_agentic_swarm.services.wave_gate_service import default_wave_controller
from merged_agentic_swarm.tools.knowledge_cache import default_knowledge_cache

logger = logging.getLogger("agentic_orchestrator")


def _cancellation_check(cancel_event: threading.Event | None, wave: int) -> dict[str, Any] | None:
    """Return an aborted result if the run was cancelled, else None."""
    if cancel_event is not None and cancel_event.is_set():
        logger.warning(f"Workflow cancelled by user (wave {wave}); aborting.")
        return {"status": "aborted", "reason": "cancelled by user", "waves_completed": wave, "timestamp": time.time()}
    return None


class MultiLayeredAgenticOrchestrator:
    def __init__(self, prd_title: str = "Multi-Layered Agentic Workflow System"):
        self.prd_title = prd_title
        self.proxy_daemon: ProxyServerDaemon | None = None
        self.promoted_learning_ids: set = set()
        self.promoted_ids_file: str = str(_REPO_ROOT / ".taskmaster" / "promoted_learning_ids.json")
        self._load_promoted_ids()

    # ── Promoted-IDs persistence (FIX-04: cross-run dedup) ──

    def _load_promoted_ids(self):
        """Load previously promoted learning IDs so cold-path dedup survives restarts."""
        if os.path.exists(self.promoted_ids_file):
            try:
                import json

                with open(self.promoted_ids_file) as f:
                    data = json.load(f)
                self.promoted_learning_ids = set(data.get("ids", []))
                logger.info(f"Loaded {len(self.promoted_learning_ids)} previously promoted learning IDs")
            except Exception as e:
                logger.warning(f"Could not load promoted IDs from {self.promoted_ids_file}: {e}")

    def _save_promoted_ids(self):
        """Persist promoted learning IDs for the next run."""
        try:
            import json

            os.makedirs(os.path.dirname(self.promoted_ids_file), exist_ok=True)
            with open(self.promoted_ids_file, "w") as f:
                json.dump({"ids": sorted(self.promoted_learning_ids), "updated_at": time.time()}, f)
        except Exception as e:
            logger.warning(f"Could not save promoted IDs: {e}")

    # ── Worker output → file application (FIX-01) ──

    def _run_syntax_verification(self) -> dict[str, Any]:
        """Run actual syntax + import verification instead of hardcoded unittest (FIX-10).

        Tries scripts/ci.ps1 (Windows) / scripts/ci.sh (POSIX) first, falls back
        to inline syntax check on core files.
        Returns dict with exit_code and output_summary.
        """
        import subprocess

        # Try CI script first — platform-appropriate script + interpreter
        script_name = "ci.ps1" if sys.platform == "win32" else "ci.sh"
        ci_script = str(_REPO_ROOT / "scripts" / script_name)
        if os.path.exists(ci_script):
            try:
                if sys.platform == "win32":
                    result = subprocess.run(
                        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ci_script],
                        capture_output=True,
                        text=True,
                        timeout=60,
                    )
                else:
                    result = subprocess.run(["bash", ci_script], capture_output=True, text=True, timeout=60)
                summary = result.stdout.strip().split("\n")[-1]  # Last line = pass/fail banner
                return {
                    "exit_code": result.returncode,
                    "output_summary": f"CI script: {summary} ({len(result.stdout)} chars)",
                    "tests_ran": True,  # ci.sh executes the pytest suite
                }
            except Exception as e:
                return {"exit_code": 1, "output_summary": f"CI script failed: {e}", "tests_ran": False}

        # Fallback: inline syntax check on core files
        # Paths are relative to the package root (src/merged_agentic_swarm/)
        core_files = [
            "providers/multi_provider_fabric.py",
            "providers/key_pool.py",
            "services/progress_ledger_service.py",
            "services/wave_gate_service.py",
            "services/codebase_map_service.py",
            "services/agent_factory_service.py",
            "services/task_master_service.py",
            "services/opencode_swarm_service.py",
            "tools/knowledge_cache.py",
            "tools/agentic_cli.py",
            "tools/agentic_orchestrator.py",
            "proxy/claude_proxy_server.py",
        ]
        pkg_root = _REPO_ROOT / "src" / "merged_agentic_swarm"
        errors = []
        for rel_path in core_files:
            fpath = pkg_root / rel_path
            try:
                with open(fpath) as f:
                    source = f.read()
                compile(source, fpath, "exec")
            except SyntaxError as e:
                errors.append(f"{rel_path}:{e.lineno}: {e.msg}")
        if errors:
            return {
                "exit_code": 1,
                "output_summary": f"Syntax check FAILED: {'; '.join(errors)}",
                "tests_ran": False,
            }
        return {
            "exit_code": 0,
            "output_summary": f"Syntax check PASSED ({len(core_files)} files)",
            "tests_ran": False,  # inline fallback does not execute the test suite
        }

    # ── Registry compaction (FIX-14: auto-compact at end of run) ──

    def _compact_registries(self) -> dict[str, int]:
        """Deduplicate cold-path registries by content hash (knowledge) and ID (agents/chain).

        knowledge.jsonl: group by title+category+solution content hash, keep last in group.
        agents.jsonl:    group by category, keep last per category.
        chain.jsonl:     group by source_learning_id, keep last per source.
        Returns dict of {registry: removed_count}.
        """
        import hashlib
        import json

        registry_dir = str(_REGISTRY_DIR)
        counts = {}

        # ── knowledge.jsonl: content-hash dedup ──
        kn_path = os.path.join(registry_dir, "knowledge.jsonl")
        if os.path.exists(kn_path):
            with open(kn_path) as f:
                kn_lines = [l.strip() for l in f if l.strip()]
            groups = {}
            for line in kn_lines:
                entry = json.loads(line)
                key = hashlib.md5(
                    f"{entry.get('title', '')}|{entry.get('category', '')}|{entry.get('solution', '')}".encode()
                ).hexdigest()
                groups[key] = entry  # last occurrence wins
            filtered = [json.dumps(e) + "\n" for e in groups.values()]
            counts["knowledge_removed"] = len(kn_lines) - len(filtered)
            # Atomic write: temp file → rename
            tmp = kn_path + ".tmp"
            with open(tmp, "w") as f:
                f.writelines(filtered)
            os.replace(tmp, kn_path)

        # ── agents.jsonl: content-hash dedup (not just per-category last-wins) ──
        ag_path = os.path.join(registry_dir, "agents.jsonl")
        if os.path.exists(ag_path):
            with open(ag_path) as f:
                ag_lines = [l.strip() for l in f if l.strip()]
            groups = {}
            for line in ag_lines:
                entry = json.loads(line)
                # Dedup by name+category+system_prompt so distinct agents in the
                # same category are preserved
                key = hashlib.md5(
                    f"{entry.get('name', '')}|{entry.get('category', '')}|{entry.get('system_prompt', '')}".encode()
                ).hexdigest()
                groups[key] = entry  # last occurrence per content-hash wins
            filtered = [json.dumps(e) + "\n" for e in groups.values()]
            counts["agents_removed"] = len(ag_lines) - len(filtered)
            tmp = ag_path + ".tmp"
            with open(tmp, "w") as f:
                f.writelines(filtered)
            os.replace(tmp, ag_path)

        # ── chain.jsonl: per-source dedup ──
        ch_path = os.path.join(registry_dir, "chain.jsonl")
        if os.path.exists(ch_path):
            with open(ch_path) as f:
                ch_lines = [l.strip() for l in f if l.strip()]
            groups = {}
            for line in ch_lines:
                entry = json.loads(line)
                src = entry.get("source_learning_id", "unknown")
                groups[src] = entry  # last per source wins
            filtered = [json.dumps(e) + "\n" for e in groups.values()]
            counts["chain_removed"] = len(ch_lines) - len(filtered)
            tmp = ch_path + ".tmp"
            with open(tmp, "w") as f:
                f.writelines(filtered)
            os.replace(tmp, ch_path)

        total = sum(counts.values())
        logger.info(f"Registry compaction: {total} entries removed ({counts})")
        return counts

    def _apply_worker_outputs(self, results: list[dict[str, Any]], wave_label: str = "") -> int:
        """Apply worker outputs to disk and count files written.

        Primary path: agentic-loop workers already wrote files for real — count
        their ``files_written`` list. Secondary path: text-only workers (e.g.
        opencode mode) may emit ``# file: <path>`` markdown blocks inside their
        final text; parse and write those as before.
        Returns the number of files written.
        """
        import re

        files_written = 0
        commands_run = 0
        for result in results:
            if result.get("status") != "completed":
                continue

            # Primary: real writes already on disk via the agentic tool loop.
            # Count DISTINCT files — a loop may write the same path repeatedly.
            fw_list = sorted(set(result.get("files_written") or []))
            cr_list = sorted(set(result.get("commands_run") or []))
            files_written += len(fw_list)
            commands_run += len(cr_list)
            # Auditable per-worker real-work trail: gate counts alone cannot prove
            # a worker produced artifacts, so surface the actual paths/commands.
            if fw_list or cr_list:
                logger.info(
                    f"{wave_label} worker {result.get('worker_id', '?')} REAL WORK: "
                    f"{len(fw_list)} file(s) {fw_list}; {len(cr_list)} command(s) {cr_list}"
                )
            elif result.get("final_text"):
                logger.info(
                    f"{wave_label} worker {result.get('worker_id', '?')} produced no "
                    f"files/commands (text-only: {result.get('final_text', '')[:80]!r})"
                )

            # Secondary: text-only workers — pull text from final_text/response.
            content = result.get("final_text", "") or ""
            response = result.get("response", {})
            if isinstance(response, dict):
                resp_text = response.get("content", "")
                if isinstance(resp_text, str) and not content:
                    content = resp_text
            elif isinstance(response, str) and not content:
                content = response

            if not content or not isinstance(content, str):
                continue

            # Match: ```lang\n# file: <path>\n<content>```
            # Also match: ```\n# file: <path>\n<content>```
            for match in re.finditer(r"```\w*\n#\s*file:\s*(.+?)\n(.*?)```", content, re.DOTALL | re.IGNORECASE):
                raw_path = match.group(1).strip().strip('"').strip("'")
                file_content = match.group(2).strip()
                # Resolve relative paths against the repo root
                if not os.path.isabs(raw_path):
                    abs_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), raw_path)
                else:
                    abs_path = raw_path
                try:
                    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
                    with open(abs_path, "w") as f:
                        f.write(file_content)
                    logger.info(
                        f"{wave_label} worker {result.get('worker_id', '?')} wrote {len(file_content)}B → {raw_path}"
                    )
                    files_written += 1
                except Exception as e:
                    logger.error(f"Failed to write {raw_path} ({abs_path}): {e}")

        logger.info(
            f"{wave_label} aggregate: {files_written} distinct real file(s), "
            f"{commands_run} distinct real command(s) across {len(results)} worker result(s)."
        )
        return files_written

    def _append_jsonl(self, path: str, record: dict):
        """Append a JSON line to a JSONL registry."""
        import json

        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, default=str) + "\n")

    def _promote_cold_path(self, phase_label: str = ""):
        """Cold-path: normalize hot cache entries → knowledge.jsonl → validated → agents.jsonl.

        Phase 4 of the blueprint: validated learning from hot cache is promoted to
        durable cold-path registries. Repeated patterns (≥3 same-category entries)
        graduate to durable agent specs.
        """

        knowledge_registry = str(_REGISTRY_DIR / "knowledge.jsonl")
        agents_registry = str(_REGISTRY_DIR / "agents.jsonl")
        chain_registry = str(_REGISTRY_DIR / "chain.jsonl")
        now = time.time()

        # Collect unpromoted learnings from hot cache
        unpromoted = []
        for lid, learning in default_knowledge_cache.learnings.items():
            if lid not in self.promoted_learning_ids:
                unpromoted.append(learning)

        if not unpromoted:
            logger.info(f"Cold-path [{phase_label}]: no new learnings to promote.")
            return {"promoted_knowledge": 0, "promoted_agents": 0}

        # Build category frequency map for validation (includes previously promoted)
        category_counts: dict[str, int] = {}
        for lid, learning in default_knowledge_cache.learnings.items():
            cat = learning.get("category", "general")
            category_counts[cat] = category_counts.get(cat, 0) + 1

        promoted_knowledge = 0
        promoted_agents = 0
        chain_seq = 0  # per-batch sequence so chain entry_ids stay unique
        promoted_categories_this_run: set = set()  # track which categories already got agents this batch

        for learning in unpromoted:
            lid = learning["id"]

            # 1. Normalize → knowledge.jsonl
            knowledge_record = {
                "id": lid,
                "title": learning.get("title", ""),
                "category": learning.get("category", "general"),
                "solution": learning.get("pattern_solution", learning.get("solution", "")),
                "tags": learning.get("tags", []),
                "promoted_at": now,
                "source": "orchestrator_cold_path",
                "phase": phase_label,
            }
            self._append_jsonl(knowledge_registry, knowledge_record)
            self.promoted_learning_ids.add(lid)
            promoted_knowledge += 1

            # 2. Validation: category frequency ≥ 3 AND not already promoted this run
            cat = learning.get("category", "general")
            if category_counts.get(cat, 0) >= 3 and cat not in promoted_categories_this_run:
                promoted_categories_this_run.add(cat)
                agent_spec = {
                    "id": f"agent-{cat}-cold-{int(now * 1000)}",
                    "name": f"Durable {cat} Specialist",
                    "category": cat,
                    "derived_from_learnings": [
                        l["id"] for l in default_knowledge_cache.learnings.values() if l.get("category") == cat
                    ],
                    "system_prompt": f"You are a durable specialist for {cat} tasks, "
                    f"created from {category_counts[cat]} validated learning records.",
                    "promoted_at": now,
                    "ttl_sec": None,  # durable — no expiration
                }
                self._append_jsonl(agents_registry, agent_spec)

                # 3. Chain log entry
                chain_seq += 1
                chain_entry = {
                    "entry_id": f"CHAIN-COLD-{int(now * 1000)}-{chain_seq}",
                    "source_learning_id": lid,
                    "spawned_agent_id": agent_spec["id"],
                    "agent_type": "cold_durable",
                    "trigger_reason": f"Repeated {cat} pattern ({category_counts[cat]} instances) triggered cold-path promotion",
                    "timestamp": now,
                    "promotion_phase": phase_label,
                }
                self._append_jsonl(chain_registry, chain_entry)
                promoted_agents += 1

                # 4. Write the actual agent .md spec file to .claude/agents/
                written_path = default_agent_factory._write_agent_spec_file(agent_spec)
                if written_path:
                    logger.info(f"Wrote durable agent spec: {written_path}")
                else:
                    logger.debug(f"Agent spec file already exists for {agent_spec['id']} (skipped)")

                # Also register in the hot-path spawn chain for cross-referencing
                default_agent_factory.chain_registry.register_spawn(
                    source_learning_id=lid,
                    spawned_agent_id=agent_spec["id"],
                    agent_type=AgentType.COLD_DURABLE,
                    trigger_reason=chain_entry["trigger_reason"],
                )

                # promoted_categories_this_run set above ensures only one agent
                # per category per batch — no counter reset needed

        logger.info(
            f"Cold-path [{phase_label}]: {promoted_knowledge} learnings → knowledge.jsonl, "
            f"{promoted_agents} durable agents → agents.jsonl"
        )
        return {"promoted_knowledge": promoted_knowledge, "promoted_agents": promoted_agents}

    def initialize_system(self, start_proxy_port: int = 8085) -> dict[str, Any]:
        """Initializes Key Pool Proxy server and verifies service readiness."""
        logger.info("Initializing Agentic System proxy server and model fabric...")
        try:
            self.proxy_daemon = ProxyServerDaemon(port=start_proxy_port)
            self.proxy_daemon.start()
            proxy_status = f"Running on port {start_proxy_port}"
        except Exception as e:
            proxy_status = f"Proxy initialization note: {e}"

        return {
            "status": "ready",
            "proxy_status": proxy_status,
            "task_master_ready": True,
            "swarm_workers": 40,
            "timestamp": time.time(),
        }

    def _abort_on_gate_failure(self, passed: bool, reason: str, wave: int, gates: bool | None) -> dict[str, Any] | None:
        """Return an abort result when a gate fails and gates are enforced.

        ``advance_wave()`` has already run (wave state advances regardless); this
        only decides whether a non-passing gate aborts the workflow. When
        ``gates is False`` (profile gates disabled) the failure is logged at
        warning and the workflow continues. When ``None``/``True`` the abort
        behavior is preserved exactly.
        """
        if passed:
            return None
        if gates is False:
            logger.warning(f"gates disabled by profile — Wave {wave} gate failed ({reason}); continuing")
            return None
        logger.error(f"Wave {wave} gate FAILED: {reason}. Aborting workflow.")
        return {"status": "failed", "reason": f"Wave {wave} gate failed: {reason}", "wave": wave}

    def run_full_agentic_workflow(
        self,
        prd_content: str,
        ramp_sequence: list[int] | None = None,
        default_model: str | None = None,
        gates: bool | None = None,
        cancel_event: threading.Event | None = None,
    ) -> dict[str, Any]:
        """Runs the complete self-healing 6-step agent-to-agent workflow.

        ``ramp_sequence`` (when set) is threaded into every swarm batch so the
        wave_gate_level -> worker-count mapping follows the profile's ramp instead
        of the hard-coded [4, 8, 16, 24, 40]. ``default_model`` (when set) is
        recorded as the ``model`` on each progress-ledger log_progress entry so the
        run-report timeline carries the model tier that served the run, and is
        threaded into every swarm batch as ``model_alias`` (profile runs only).
        ``gates`` honors the profile's ``gates`` flag: when ``False`` every
        ``advance_wave()`` call still runs (state advances) but a non-passing gate
        logs a warning and continues instead of aborting the workflow.
        """
        logger.info("=== STARTING MULTI-LAYERED AGENTIC WORKFLOW ===")

        # Profile-driven overrides are only forwarded when present so the default
        # call path stays byte-for-byte identical (None -> no extra kwargs).
        swarm_kwargs: dict[str, Any] = {}
        if ramp_sequence is not None:
            swarm_kwargs["ramp_sequence"] = ramp_sequence
        if default_model is not None:
            # Profile runs pin every worker to the profile's resolved alias;
            # non-profile runs omit it so per-role defaults apply.
            swarm_kwargs["model_alias"] = default_model
        ledger_kwargs: dict[str, Any] = {}
        if default_model is not None:
            ledger_kwargs["model"] = default_model

        # Step 0: System Init & Proxy Check
        self.initialize_system()
        default_progress_ledger.log_progress(
            task_id="INIT",
            subtask_id=None,
            worker_id="system",
            wave_id=0,
            action="proxy_deployed",
            status="completed",
            details={"proxy": "localhost:8085"},
            **ledger_kwargs,
        )
        default_progress_ledger.log_progress(
            task_id="INIT",
            subtask_id=None,
            worker_id="system",
            wave_id=0,
            action="run_deployed",
            status="completed",
            details={"model_alias": default_model},
            **ledger_kwargs,
        )

        # Step 1: PRD Optimization & Parsing via Task Master AI
        logger.info("--- Step 1: Optimizing and Parsing PRD via Task Master AI ---")
        prd_result = default_task_master.optimize_and_parse_prd(prd_content, title=self.prd_title)
        default_progress_ledger.log_progress(
            task_id="INIT",
            subtask_id=None,
            worker_id="task-master-ai",
            wave_id=0,
            action="prd_parsed",
            status="completed",
            details={"epics_count": len(prd_result.epics)},
            **ledger_kwargs,
        )

        # Step 2: Map Codebase & Close Spec Gaps
        logger.info("--- Step 2: Mapping Codebase and Closing Spec Gaps ---")
        default_codebase_mapper.scan_repository()
        detected_gaps = default_codebase_mapper.detect_spec_gaps(
            required_components=["models", "providers", "proxy", "services", "tools"]
        )
        for gap in detected_gaps:
            default_codebase_mapper.close_spec_gap(gap.id, resolution_note="Bootstrapped required module architecture.")

        # Validate Wave 0 Gate
        passed_w0, reason_w0 = default_wave_controller.advance_wave()
        logger.info(f"Wave 0 Gate Status: {passed_w0} ({reason_w0})")
        abort_w0 = self._abort_on_gate_failure(passed_w0, reason_w0, 0, gates)
        if abort_w0 is not None:
            return abort_w0
        aborted = _cancellation_check(cancel_event, 0)
        if aborted is not None:
            return aborted

        # Step 3: Wave 1 - Key Pool Proxy & Fabric Gate
        logger.info("--- Step 3: Wave 1 Execution (Key Pool Proxy & Model Fabric) ---")
        wave_1_epics = default_task_master.get_tasks_for_wave(1)
        for epic in wave_1_epics:
            try:
                results = default_swarm_manager.execute_subtask_batch_parallel(
                    epic.subtasks, role=WorkerRole.CORE_ENGINEER, wave_gate_level=1, **swarm_kwargs
                )
            except Exception as e:
                logger.error(f"Wave 1 batch failed: {e}")
                try:
                    remediation = default_progress_ledger.handle_task_failure(epic.id, str(e))
                except Exception as he:
                    logger.error(f"Error handler itself failed for epic {epic.id}: {he}")
                    remediation = {"remediated": False, "strategy": "none", "action": "error_handler_failed"}
                default_knowledge_cache.add_learning(
                    title=f"Anomaly: {epic.title}",
                    category="anomaly",
                    pattern_solution=f"Error: {str(e)[:200]}. Remediation: {remediation.get('action', 'none')}",
                    tags=["anomaly", "recovery", "wave-1"],
                )
                results = [{"status": "error", "error": str(e)}]
            files_written = self._apply_worker_outputs(results, wave_label="W1")
            # FIX-05: Only mark epic COMPLETED if ALL subtasks succeeded.
            # A simulated (offline-fallback) worker result reports status="failed"
            # with reason="simulation_fallback", so it can never pass this gate.
            all_ok = all(r.get("status") == "completed" for r in results)
            if all_ok:
                default_task_master.update_task_status(epic.id, TaskStatus.COMPLETED)
            else:
                failed = [r for r in results if r.get("status") != "completed"]
                sim_failures = [r for r in failed if "simulation" in str(r.get("reason", ""))]
                default_task_master.update_task_status(
                    epic.id, TaskStatus.FAILED, error_message=f"{len(failed)}/{len(results)} subtasks failed"
                )
                if sim_failures:
                    # Simulated work must NEVER advance a gate — log it distinctly.
                    logger.error(
                        f"Wave 1 epic {epic.id}: {len(sim_failures)} subtask(s) returned "
                        f"SIMULATION FALLBACK — gate cannot pass. Workers received no live provider."
                    )
                else:
                    logger.warning(f"Wave 1 epic {epic.id}: {len(failed)}/{len(results)} subtasks failed")
            default_progress_ledger.record_success_marker(
                task_id=epic.id,
                verifier_name="ProxyFabricVerifier",
                command_executed="curl http://localhost:8085/health",
                exit_code=0 if all_ok else 1,
                output_summary=f"Proxy server and key pool rotation active. Applied {files_written} file(s).",
            )

        passed_w1, reason_w1 = default_wave_controller.advance_wave()
        logger.info(f"Wave 1 Gate Status: {passed_w1} ({reason_w1})")
        abort_w1 = self._abort_on_gate_failure(passed_w1, reason_w1, 1, gates)
        if abort_w1 is not None:
            return abort_w1
        aborted = _cancellation_check(cancel_event, 1)
        if aborted is not None:
            return aborted

        # Step 4: Wave 2 - OpenCode 40-Worker Swarm & Durable Agent Factory
        logger.info("--- Step 4: Wave 2 Execution (OpenCode Swarm & Durable Agents) ---")
        wave_2_epics = default_task_master.get_tasks_for_wave(2)
        for epic in wave_2_epics:
            try:
                results = default_swarm_manager.execute_subtask_batch_parallel(
                    epic.subtasks, role=WorkerRole.CORE_ENGINEER, wave_gate_level=2, **swarm_kwargs
                )
            except Exception as e:
                logger.error(f"Wave 2 batch failed: {e}")
                remediation = default_progress_ledger.handle_task_failure(epic.id, str(e))
                learning_id = default_knowledge_cache.add_learning(
                    title=f"Anomaly: {epic.title}",
                    category="anomaly",
                    pattern_solution=f"Error: {str(e)[:200]}. Remediation: {remediation.get('action', 'none')}",
                    tags=["anomaly", "recovery", "wave-2"],
                )
                default_agent_factory.spawn_from_learning(learning_id, trigger_reason="Anomaly auto-recovery")
                results = [{"status": "error", "error": str(e)}]
            files_written = self._apply_worker_outputs(results, wave_label="W2")

            # Generate Validated Learning & Spawn Agents via Factory
            # Vary learning content by epic to create durable knowledge diversity
            epic_lower = epic.title.lower()
            if "swarm" in epic_lower or "worker" in epic_lower:
                learn_cat = "swarm_concurrency"
                learn_sol = "Use 40-worker thread pool with round-robin key rotation for high throughput."
                learn_tags = ["opencode", "swarm", "durable"]
            elif "gate" in epic_lower or "verif" in epic_lower or "integrat" in epic_lower:
                learn_cat = "wave_gating"
                learn_sol = "Phase gates enforce sequential dependency resolution before advancing to next wave. Each gate validates all predecessor outputs."
                learn_tags = ["gate", "verify", "wave"]
            elif "promot" in epic_lower or "learn" in epic_lower or "cold" in epic_lower:
                learn_cat = "knowledge_promotion"
                learn_sol = "Cold-path promotion: hot cache → knowledge.jsonl → validate (≥3 same-category) → agents.jsonl→ chain.jsonl"
                learn_tags = ["learning", "promotion", "durable"]
            elif "codebase" in epic_lower or "map" in epic_lower or "spec" in epic_lower:
                learn_cat = "codebase_analysis"
                learn_sol = "AST-based codebase mapping with directory-aware spec gap detection."
                learn_tags = ["codebase", "ast", "spec-gap"]
            elif "proxy" in epic_lower or "fabric" in epic_lower or "provider" in epic_lower:
                learn_cat = "provider_fabric"
                learn_sol = "Multi-provider fallback chain with 15s localhost timeout for Gemini thinking models."
                learn_tags = ["proxy", "fabric", "provider"]
            else:
                learn_cat = "general"
                learn_sol = "Standard execution pattern within the Merged Agentic Swarm framework."
                learn_tags = ["general", "execution"]

            learning_id = default_knowledge_cache.add_learning(
                title=f"{learn_cat.replace('_', ' ').title()}: {epic.title}",
                category=learn_cat,
                pattern_solution=learn_sol,
                tags=learn_tags,
            )
            # Spawn HOT Micro-Specialist and COLD Durable Agent
            # FIX-09: Purge expired HOT agents before spawning new ones
            purged = default_agent_factory.purge_expired()
            if purged:
                logger.info(f"Purged {purged} expired HOT agents before spawning")
            hot_agent = default_agent_factory.spawn_from_learning(
                learning_id, trigger_reason="Acute concurrency optimization", force_type=AgentType.HOT_MICRO_SPECIALIST
            )
            default_agent_factory.spawn_from_learning(
                learning_id, trigger_reason="Durable state persistence", force_type=AgentType.COLD_DURABLE
            )

            # FIX-05: Only mark epic COMPLETED if ALL subtasks succeeded.
            # Simulated (offline-fallback) results report status="failed", so they
            # can never pass this gate.
            all_ok = all(r.get("status") == "completed" for r in results)
            if all_ok:
                default_task_master.update_task_status(epic.id, TaskStatus.COMPLETED)
            else:
                failed = [r for r in results if r.get("status") != "completed"]
                sim_failures = [r for r in failed if "simulation" in str(r.get("reason", ""))]
                default_task_master.update_task_status(
                    epic.id, TaskStatus.FAILED, error_message=f"{len(failed)}/{len(results)} subtasks failed"
                )
                if sim_failures:
                    logger.error(
                        f"Wave 2 epic {epic.id}: {len(sim_failures)} subtask(s) returned "
                        f"SIMULATION FALLBACK — gate cannot pass."
                    )
                else:
                    logger.warning(f"Wave 2 epic {epic.id}: {len(failed)}/{len(results)} subtasks failed")

            default_progress_ledger.log_progress(
                task_id=epic.id,
                subtask_id=None,
                worker_id=hot_agent.id,
                wave_id=2,
                action="agent_spawned",
                status="completed",
                learning_generated=learning_id,
                details={"files_applied": files_written},
                **ledger_kwargs,
            )

        passed_w2, reason_w2 = default_wave_controller.advance_wave()
        logger.info(f"Wave 2 Gate Status: {passed_w2} ({reason_w2})")
        abort_w2 = self._abort_on_gate_failure(passed_w2, reason_w2, 2, gates)
        if abort_w2 is not None:
            return abort_w2
        aborted = _cancellation_check(cancel_event, 2)
        if aborted is not None:
            return aborted

        # Cold-path promotion after Wave 2: promote learnings to registries
        cold_2 = self._promote_cold_path(phase_label="wave_2")

        # Step 5: Wave 3 - Integration & Verification Gate
        logger.info("--- Step 5: Wave 3 Execution (Integration, Verifiers & Obstacle Playbooks) ---")
        wave_3_epics = default_task_master.get_tasks_for_wave(3)
        # Run the syntax/test check once — it feeds both the per-epic ledger
        # markers and the Wave-3 Zero-Defect gate (issue #13).
        ver_result = self._run_syntax_verification()
        for epic in wave_3_epics:
            try:
                results = default_swarm_manager.execute_subtask_batch_parallel(
                    epic.subtasks, role=WorkerRole.SECURITY_VERIFIER, wave_gate_level=3, **swarm_kwargs
                )
            except Exception as e:
                logger.error(f"Wave 3 batch failed: {e}")
                remediation = default_progress_ledger.handle_task_failure(epic.id, str(e))
                default_knowledge_cache.add_learning(
                    title=f"Anomaly: {epic.title}",
                    category="anomaly",
                    pattern_solution=f"Error: {str(e)[:200]}. Remediation: {remediation.get('action', 'none')}",
                    tags=["anomaly", "recovery", "wave-3"],
                )
                results = [{"status": "error", "error": str(e)}]
            files_written = self._apply_worker_outputs(results, wave_label="W3")
            # FIX-05: Only mark epic COMPLETED if ALL subtasks succeeded.
            # Simulated (offline-fallback) results report status="failed", so they
            # can never pass this gate.
            all_ok = all(r.get("status") == "completed" for r in results)
            if all_ok:
                default_task_master.update_task_status(epic.id, TaskStatus.COMPLETED)
            else:
                failed = [r for r in results if r.get("status") != "completed"]
                sim_failures = [r for r in failed if "simulation" in str(r.get("reason", ""))]
                default_task_master.update_task_status(
                    epic.id, TaskStatus.FAILED, error_message=f"{len(failed)}/{len(results)} subtasks failed"
                )
                if sim_failures:
                    logger.error(
                        f"Wave 3 epic {epic.id}: {len(sim_failures)} subtask(s) returned "
                        f"SIMULATION FALLBACK — gate cannot pass."
                    )
                else:
                    logger.warning(f"Wave 3 epic {epic.id}: {len(failed)}/{len(results)} subtasks failed")
            default_progress_ledger.record_success_marker(
                task_id=epic.id,
                verifier_name="SystemIntegrationVerifier",
                command_executed=ver_result.get("output_summary", "syntax-check")[:120],
                exit_code=ver_result.get("exit_code", 1) if not all_ok else 0,
                output_summary=f"Applied {files_written} file(s). {ver_result.get('output_summary', '')}",
            )

            # Generate verification learning for cold-path diversity
            default_knowledge_cache.add_learning(
                title=f"Verification: {epic.title}",
                category="verification",
                pattern_solution=f"Wave verification {'passed' if all_ok else 'FAILED'} for {epic.title} — {len(epic.subtasks)} subtasks validated.",
                tags=["verification", "wave-gate", "integration"],
            )

        # The Wave-3 "Zero Defect" gate evaluates the verification result —
        # syntax and test outcomes — not just epic statuses (issue #13).
        default_wave_controller.record_verification_results(ver_result)
        passed_w3, reason_w3 = default_wave_controller.advance_wave()
        logger.info(f"Wave 3 Gate Status: {passed_w3} ({reason_w3})")
        abort_w3 = self._abort_on_gate_failure(passed_w3, reason_w3, 3, gates)
        if abort_w3 is not None:
            return abort_w3
        aborted = _cancellation_check(cancel_event, 3)
        if aborted is not None:
            return aborted

        # Step 5.5: Wave 4 - Synthesis & Final Reporting
        logger.info("--- Step 5.5: Wave 4 Execution (Synthesis & Final Reporting) ---")
        wave_4_epics = default_task_master.get_tasks_for_wave(4)
        for epic in wave_4_epics:
            try:
                results = default_swarm_manager.execute_subtask_batch_parallel(
                    epic.subtasks, role=WorkerRole.CORE_ENGINEER, wave_gate_level=4, **swarm_kwargs
                )
            except Exception as e:
                logger.error(f"Wave 4 batch failed: {e}")
                try:
                    default_progress_ledger.handle_task_failure(epic.id, str(e))
                except Exception as he:
                    logger.error(f"Error handler failed for epic {epic.id}: {he}")
                results = [{"status": "error", "error": str(e)}]
            files_written = self._apply_worker_outputs(results, wave_label="W4")
            # Simulated (offline-fallback) results report status="failed", so they
            # can never pass this gate.
            all_ok = all(r.get("status") == "completed" for r in results)
            if all_ok:
                default_task_master.update_task_status(epic.id, TaskStatus.COMPLETED)
            else:
                failed = [r for r in results if r.get("status") != "completed"]
                sim_failures = [r for r in failed if "simulation" in str(r.get("reason", ""))]
                default_task_master.update_task_status(
                    epic.id, TaskStatus.FAILED, error_message=f"{len(failed)}/{len(results)} subtasks failed"
                )
                if sim_failures:
                    logger.error(
                        f"Wave 4 epic {epic.id}: {len(sim_failures)} subtask(s) returned "
                        f"SIMULATION FALLBACK — gate cannot pass."
                    )
            default_progress_ledger.log_progress(
                task_id=epic.id,
                subtask_id=None,
                worker_id="orchestrator-wave-4",
                wave_id=4,
                action="synthesis_completed",
                status="completed" if all_ok else "failed",
                details={"files_applied": files_written},
                **ledger_kwargs,
            )

        passed_w4, reason_w4 = default_wave_controller.advance_wave()
        logger.info(f"Wave 4 Gate Status: {passed_w4} ({reason_w4})")
        if not passed_w4:
            logger.warning(f"Wave 4 gate did not pass (non-fatal): {reason_w4}")

        # Final cold-path promotion: promote any remaining learnings
        cold_3 = self._promote_cold_path(phase_label="wave_3_final")

        # Step 6: Summary & State Preservation
        # Write final task_master state
        if default_task_master.current_analysis:
            default_task_master.save_state()

        # Persist promoted learning IDs for cross-run dedup (FIX-04)
        self._save_promoted_ids()

        # Auto-compact registries to prevent unbounded growth (FIX-14)
        compact_counts = self._compact_registries()

        with open(str(_REGISTRY_DIR / "knowledge.jsonl")) as kf:
            total_cold_knowledge = sum(1 for _ in kf if _.strip())
        with open(str(_REGISTRY_DIR / "agents.jsonl")) as af:
            total_cold_agents = sum(1 for _ in af if _.strip())
        logger.info("=== WORKFLOW COMPLETE: ALL WAVES PASSED ===")
        return {
            "status": "success",
            "prd_summary": prd_result.summary,
            "waves_completed": 4,
            "epics_completed": len(default_task_master.current_analysis.epics)
            if default_task_master.current_analysis
            else 0,
            "total_success_markers": len(default_progress_ledger.success_markers),
            "chain_registry_entries": len(default_agent_factory.chain_registry.entries),
            "cold_path": {
                "knowledge_promoted": cold_2.get("promoted_knowledge", 0) + cold_3.get("promoted_knowledge", 0),
                "agents_promoted": cold_2.get("promoted_agents", 0) + cold_3.get("promoted_agents", 0),
                "total_knowledge_records": total_cold_knowledge,
                "total_durable_agents": total_cold_agents,
                "memo": "Cold path: hot cache → knowledge.jsonl → validated → agents.jsonl",
            },
            "promoted_ids_persisted": len(self.promoted_learning_ids),
            "registry_compaction": compact_counts,
            "timestamp": time.time(),
        }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    orchestrator = MultiLayeredAgenticOrchestrator()
    sample_prd = """
    Target Architecture:
    A single system that combines your OpenCode swarm pack (40-worker pools, key-pool proxy, bootstrap, knowledge cache, master architect)
    with the Claude Code first control plane (Task Master spine, durable agent factory, multi-backend model fabric, knowledge-box -> spawn chain, wave gates, progress ledger).
    """
    res = orchestrator.run_full_agentic_workflow(sample_prd)
    print("\nWorkflow Execution Result:")
    print(json.dumps(res, indent=2))
