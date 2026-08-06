"""
Worker Runtime Adapter — Unified launcher for OpenCode swarm workers.

Supports three modes:
  - opencode:        Launch workers via the OpenCode CLI binary
  - native_subagent: Spawn subprocess workers with direct fabric dispatch
  - direct_fabric:   Bypass worker process, call the fabric directly

Auto-detection tries opencode first, falls back to native_subagent,
then falls back to direct_fabric.
"""

from __future__ import annotations

import json
import logging
import os
import subprocess
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from merged_agentic_swarm.models.agent_models import AgentSpec, AgentType, WorkerRole
from merged_agentic_swarm.providers.multi_provider_fabric import default_fabric

logger = logging.getLogger("worker_runtime_adapter")

OPENCODE_BIN = os.path.expanduser("~/.opencode/bin/opencode")

# Resolve the actual opencode binary from PATH or common locations
_OPENCODE_BIN_RESOLVED: str | None = None


def _resolve_opencode_bin() -> str | None:
    """Resolve the opencode binary from PATH or known locations."""
    global _OPENCODE_BIN_RESOLVED
    if _OPENCODE_BIN_RESOLVED is not None:
        return _OPENCODE_BIN_RESOLVED if _OPENCODE_BIN_RESOLVED else None

    candidates = [
        OPENCODE_BIN,
        os.path.expanduser("~/.local/bin/opencode"),
        "/usr/local/bin/opencode",
        "/usr/bin/opencode",
    ]
    # Also check PATH
    import shutil

    path_bin = shutil.which("opencode")
    if path_bin:
        candidates.insert(0, path_bin)

    for candidate in candidates:
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            _OPENCODE_BIN_RESOLVED = candidate
            return candidate
    _OPENCODE_BIN_RESOLVED = ""  # sentinel for "not found"
    return None


# ── Mode auto-detection ────────────────────────────────────────────────


def _opencode_available() -> bool:
    """Return True if the OpenCode binary exists and responds to --help."""
    bin_path = _resolve_opencode_bin()
    if not bin_path:
        return False
    try:
        result = subprocess.run(
            [bin_path, "--help"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        # OpenCode sends help output to stderr
        output = (result.stdout + result.stderr).lower()
        return result.returncode == 0 and "opencode" in output
    except Exception:
        return False


def detect_mode() -> str:
    """Auto-detect the best available runtime mode.

    Priority: opencode > native_subagent > direct_fabric
    """
    if _opencode_available():
        return "opencode"
    # native_subagent is always available (just runs Python)
    return "native_subagent"


# ── Worker runtime adapter ─────────────────────────────────────────────


class WorkerRuntimeAdapter:
    """Unified adapter that launches workers in the selected execution mode.

    Modes:
      opencode        — spawns opencode serve subprocesses, one per worker
      native_subagent — runs tasks inline via multi_provider_fabric (same process)
      direct_fabric   — bare fabric dispatch, no worker subprocess at all
    """

    OPENCODE_BIN: str = OPENCODE_BIN  # default (may be overridden)
    DEFAULT_PORT_BASE: int = 9200

    @classmethod
    def _get_opencode_bin(cls) -> str | None:
        """Return the resolved opencode binary, or None if unavailable."""
        return _resolve_opencode_bin()

    def __init__(self, mode: str = "auto") -> None:
        if mode == "auto":
            mode = detect_mode()
        if mode not in ("opencode", "native_subagent", "direct_fabric"):
            raise ValueError(f"Invalid mode '{mode}'. Must be one of: opencode, native_subagent, direct_fabric, auto")
        self.mode: str = mode
        self._worker_processes: dict[str, subprocess.Popen[str]] = {}
        self._lock = threading.Lock()
        self._port_counter: int = self.DEFAULT_PORT_BASE

        reason = (
            "OpenCode binary found and executable"
            if mode == "opencode"
            else "subprocess worker fallback"
            if mode == "native_subagent"
            else "direct fabric dispatch (no subprocess)"
        )
        logger.info(
            "WorkerRuntimeAdapter initialised | mode=%s | reason=%s",
            self.mode,
            reason,
        )

    def _next_port(self) -> int:
        with self._lock:
            port = self._port_counter
            self._port_counter += 1
            return port

    # ── launch_worker ────────────────────────────────────────────────

    def launch_worker(
        self,
        worker_spec: AgentSpec,
        task: str,
    ) -> dict[str, Any]:
        """Launch a single worker with a task and return a result dict.

        Result keys:
          run_id, task_id, worker_id, role, model_tier, start_time,
          end_time, status, evidence
        """
        run_id = str(uuid.uuid4())
        start_time = time.time()

        logger.info(
            "Launching worker | run_id=%s | worker_id=%s | role=%s | mode=%s",
            run_id,
            worker_spec.id,
            worker_spec.role.value,
            self.mode,
        )

        evidence: str
        status: str

        if self.mode == "opencode":
            status, evidence = self._launch_via_opencode(worker_spec, task)
        elif self.mode == "native_subagent":
            status, evidence = self._launch_via_native(worker_spec, task)
        else:
            status, evidence = self._launch_via_fabric(worker_spec, task)

        end_time = time.time()

        result: dict[str, Any] = {
            "run_id": run_id,
            "task_id": worker_spec.id,
            "worker_id": worker_spec.id,
            "role": worker_spec.role.value,
            "model_tier": worker_spec.model_alias,
            "start_time": start_time,
            "end_time": end_time,
            "status": status,
            "evidence": evidence,
        }
        logger.info("Worker finished | result=%s", json.dumps(result, default=str))
        return result

    # ── launch_batch ─────────────────────────────────────────────────

    def launch_batch(
        self,
        tasks: list[str],
        role: WorkerRole,
        max_concurrency: int = 4,
    ) -> list[dict[str, Any]]:
        """Launch a batch of tasks for a given role, up to max_concurrency."""
        results: list[dict[str, Any]] = []
        max_w = max(1, min(max_concurrency, len(tasks)))

        with ThreadPoolExecutor(max_workers=max_w) as executor:
            futures = {
                executor.submit(
                    self.launch_worker,
                    AgentSpec(
                        id=f"batch-worker-{role.value}-{i:02d}",
                        name=f"Batch Worker {role.value}",
                        role=role,
                        agent_type=AgentType.SWARM_WORKER,
                        system_prompt=f"Execute the given task as a {role.value} specialist.",
                    ),
                    task,
                ): i
                for i, task in enumerate(tasks)
            }
            for future in as_completed(futures):
                try:
                    results.append(future.result())
                except Exception as exc:
                    results.append(
                        {
                            "run_id": str(uuid.uuid4()),
                            "task_id": f"batch-task-{futures[future]:02d}",
                            "worker_id": "batch-error",
                            "role": role.value,
                            "model_tier": "claude-3-7-sonnet",
                            "start_time": time.time(),
                            "end_time": time.time(),
                            "status": "failed",
                            "evidence": str(exc),
                        }
                    )

        return results

    # ── Internal launchers ───────────────────────────────────────────

    def _launch_via_opencode(self, worker_spec: AgentSpec, task: str) -> tuple[str, str]:
        """Launch a task via the OpenCode CLI.

        Spawns `opencode serve --port <N>` as a short-lived worker,
        sends the task via stdin / HTTP, and captures the result.
        If the serve subprocess fails, falls back to native.
        """
        opencode_bin = self._get_opencode_bin()
        if not opencode_bin:
            return self._launch_via_native(worker_spec, task)

        port = self._next_port()
        cmd = [
            opencode_bin,
            "serve",
            "--port",
            str(port),
            "--print-logs",
        ]
        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self._worker_processes[worker_spec.id] = proc

            # Give opencode serve a moment to start
            time.sleep(1.5)

            # Attempt an HTTP call to the opencode endpoint
            import urllib.error
            import urllib.request

            payload = json.dumps(
                {
                    "prompt": task,
                    "system": worker_spec.system_prompt,
                }
            ).encode("utf-8")

            req = urllib.request.Request(
                f"http://127.0.0.1:{port}/v1/agent",
                data=payload,
                headers={
                    "Content-Type": "application/json",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = resp.read().decode("utf-8")

            # Try to terminate gracefully
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()

            return "completed", body[:2000]

        except Exception as exc:
            logger.debug("OpenCode worker failed, falling back to native: %s", exc)
            # Fallback to native if opencode fails
            return self._launch_via_native(worker_spec, task)

    def _launch_via_native(self, worker_spec: AgentSpec, task: str) -> tuple[str, str]:
        """Launch a task via native subagent fallback.

        Calls the multi-provider fabric directly with the worker's
        model alias and system prompt, returning the fabric response.
        """
        try:
            response = default_fabric.dispatch_request(
                model_alias=worker_spec.model_alias,
                messages=[{"role": "user", "content": task}],
                system_prompt=worker_spec.system_prompt,
            )
            content_blocks = response.get("content", [])
            if isinstance(content_blocks, list) and len(content_blocks) > 0:
                evidence = content_blocks[0].get("text", str(response))
            else:
                evidence = str(response)
            if response.get("simulation_fallback", False):
                # Simulation is a hard failure, never a completion: it is
                # fabricated work and must not pass any swarm gate.
                return "failed", "simulation_fallback: " + evidence[:2000]
            return "completed", evidence[:2000]
        except Exception as exc:
            return "failed", str(exc)

    def _launch_via_fabric(self, worker_spec: AgentSpec, task: str) -> tuple[str, str]:
        """Launch a task via direct fabric dispatch.

        Identical to native_subagent in implementation — the
        distinction is semantic (no subprocess overhead expected).
        """
        return self._launch_via_native(worker_spec, task)

    # ── Helper ────────────────────────────────────────────────────────

    def shutdown(self) -> None:
        """Terminate all opencode worker processes."""
        for wid, proc in list(self._worker_processes.items()):
            try:
                proc.terminate()
                proc.wait(timeout=5)
            except Exception:
                proc.kill()
            logger.debug("Shut down worker process %s", wid)
        self._worker_processes.clear()


# ── Global singleton ──────────────────────────────────────────────────

_default_adapter: WorkerRuntimeAdapter | None = None


def get_runtime_adapter(mode: str = "auto") -> WorkerRuntimeAdapter:
    """Return (or create) the global WorkerRuntimeAdapter singleton."""
    global _default_adapter
    if _default_adapter is None or _default_adapter.mode != mode:
        _default_adapter = WorkerRuntimeAdapter(mode=mode)
    return _default_adapter
