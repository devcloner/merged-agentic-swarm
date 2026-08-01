"""
Agentic Worker Tool Loop

Runs a real agentic loop over the multi-provider fabric with filesystem and
command-execution tools. Each iteration dispatches to the fabric with tool
schemas; if the model emits tool calls they are executed FOR REAL (file writes
to the working repo, scoped subprocesses), and the results are fed back for the
next iteration. Simulated (offline-fallback) responses are a hard failure —
they can never be recorded as completed work.

This replaces the old single-shot worker dispatch that produced no artifacts.
"""
from __future__ import annotations

import logging
import os
import shlex
import subprocess
from typing import Any

from merged_agentic_swarm.providers.multi_provider_fabric import default_fabric

logger = logging.getLogger("agentic_worker_loop")

# ── Tools exposed to workers (OpenAI function-call schemas; the fabric
#    converts them per provider family) ───────────────────────────────────────

WRITE_FILE_TOOL: dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Create or overwrite a file inside the working repository. Parent directories are created automatically.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Repository-relative file path, e.g. src/hello.py"},
                "content": {"type": "string", "description": "Full file contents to write"},
            },
            "required": ["path", "content"],
        },
    },
}

READ_FILE_TOOL: dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "Read a file from the working repository and return its contents (truncated to 8000 chars).",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Repository-relative file path to read"},
            },
            "required": ["path"],
        },
    },
}

LIST_DIR_TOOL: dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "list_dir",
        "description": "List the entries of a directory in the working repository (truncated to 8000 chars).",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Repository-relative directory path; use '' for the repo root"},
            },
            "required": ["path"],
        },
    },
}

RUN_COMMAND_TOOL: dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "run_command",
        "description": "Run a shell command inside the working repository (cwd = repo root) with a 60s timeout. Use for tests, linters, and git status. Destructive host-wide commands (sudo, git push, rm -rf on root paths) are refused.",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "The shell command to run, e.g. 'python hello.py'"},
            },
            "required": ["command"],
        },
    },
}

WORKER_TOOLS: list[dict[str, Any]] = [WRITE_FILE_TOOL, READ_FILE_TOOL, LIST_DIR_TOOL, RUN_COMMAND_TOOL]

# ── Command safety boundary ──────────────────────────────────────────────────
# run_command executes real subprocesses scoped to the working repo. This small
# denylist refuses commands whose side effects reach beyond the repo. The
# timeout is the second boundary. In-repo destructive ops are handled through
# write_file instead of the shell.

_REFUSED_TOKENS: set[str] = {"sudo", "mkfs"}
_REFUSED_PHRASES: tuple[str, ...] = (
    "rm -rf /",
    "rm -fr /",
    "rm -rf ~",
    "rm -fr ~",
    "git push",
    "git fetch",
    "git pull",
    "shutdown",
    "reboot",
)


def _command_safety_error(command: str) -> str | None:
    """Return a refusal reason if ``command`` is unsafe, else None."""
    try:
        tokens = shlex.split(command)
    except ValueError:
        return "command could not be parsed"
    if not tokens:
        return "empty command"
    lowered = [t.lower() for t in tokens]
    if _REFUSED_TOKENS.intersection(lowered):
        return "sudo/mkfs are not allowed"
    joined = " ".join(lowered)
    for phrase in _REFUSED_PHRASES:
        if phrase in joined:
            return f"forbidden destructive command: {phrase}"
    return None


def _extract_text(response: dict[str, Any]) -> str:
    """Extract the assistant's text content from an Anthropic-shaped response."""
    content = response.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(parts)
    return ""


class AgenticWorkerLoop:
    """Executes a subtask with real tools through the multi-provider fabric."""

    def __init__(
        self,
        fabric: Any = None,
        workdir: str | None = None,
        max_iterations: int = 12,
        command_timeout: int = 60,
    ) -> None:
        self.fabric = fabric or default_fabric
        self.workdir = os.path.abspath(workdir or os.getcwd())
        self.max_iterations = max_iterations
        self.command_timeout = command_timeout

    # ── Public API ──────────────────────────────────────────────────────

    def execute(
        self,
        subtask: dict[str, Any],
        system_prompt: str | None = None,
        model_alias: str = "claude-3-5-sonnet",
        workdir: str | None = None,
    ) -> dict[str, Any]:
        """Run the agentic loop for one subtask and return a result dict.

        Result keys:
          status            "completed" (real work) | "failed"
          reason            failure reason when status == "failed"
          final_text        the model's final plain-text summary
          files_written     repo-relative paths actually written to disk
          commands_run      shell commands actually executed
          iterations        number of loop iterations used
          iterations_exhausted  True when the iteration bound was reached
          simulation_fallback  True when the response was synthetic
        """
        target_workdir = os.path.abspath(workdir or self.workdir)
        os.makedirs(target_workdir, exist_ok=True)

        title = subtask.get("title", "") if isinstance(subtask, dict) else ""
        desc = subtask.get("description", "") or subtask.get("task", "")
        task_text = title + (("\n" + desc) if desc else "")

        system_prompt = system_prompt or (
            "You are an autonomous software engineer executing one task inside a working "
            "repository. Use the provided tools (write_file, read_file, list_dir, "
            "run_command) to do REAL work: write real code, run real commands, and produce "
            "real artifacts on disk. When the task is complete, reply with a short plain-text "
            "summary and do NOT call any more tools."
        )

        messages: list[dict[str, Any]] = [{"role": "user", "content": task_text}]
        files_written: list[str] = []
        commands_run: list[str] = []
        final_text = ""

        for iteration in range(1, self.max_iterations + 1):
            try:
                response = self.fabric.dispatch_request(
                    model_alias=model_alias,
                    messages=messages,
                    system_prompt=system_prompt,
                    tools=WORKER_TOOLS,
                )
            except Exception as exc:  # provider cascade failure (e.g. all keys exhausted)
                logger.error("Worker dispatch raised %s: %s", type(exc).__name__, exc)
                return {
                    "status": "failed",
                    "reason": f"dispatch error: {type(exc).__name__}: {exc}",
                    "final_text": final_text,
                    "files_written": files_written,
                    "commands_run": commands_run,
                    "iterations": iteration,
                }

            if response.get("simulation_fallback"):
                # A simulated response is a hard failure — never a completion.
                logger.error(
                    "Worker received simulation_fallback (all live providers down); "
                    "marking subtask failed."
                )
                return {
                    "status": "failed",
                    "reason": "simulation_fallback",
                    "final_text": _extract_text(response),
                    "files_written": files_written,
                    "commands_run": commands_run,
                    "iterations": iteration,
                    "simulation_fallback": True,
                }

            tool_calls = response.get("tool_calls") or []
            if not tool_calls:
                final_text = _extract_text(response)
                return {
                    "status": "completed",
                    "final_text": final_text,
                    "files_written": files_written,
                    "commands_run": commands_run,
                    "iterations": iteration,
                }

            # Append the assistant tool-call message, then execute each call for real.
            messages.append({
                "role": "assistant",
                "content": _extract_text(response),
                "tool_calls": tool_calls,
            })
            for tool_call in tool_calls:
                name = tool_call.get("name", "")
                args = tool_call.get("input", {}) or {}
                result_text, error = self._run_tool(name, args, target_workdir)
                if error is not None:
                    result_text = f"Error: {error}"
                else:
                    if name == "write_file":
                        files_written.append(args.get("path", ""))
                    elif name == "run_command":
                        commands_run.append(args.get("command", ""))
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.get("id", ""),
                    "content": result_text,
                })

        # Iteration bound hit — real partial work is kept and reported honestly.
        return {
            "status": "completed",
            "final_text": final_text,
            "files_written": files_written,
            "commands_run": commands_run,
            "iterations": self.max_iterations,
            "iterations_exhausted": True,
        }

    # ── Tool execution (all real) ───────────────────────────────────────

    def _run_tool(self, name: str, args: dict[str, Any], workdir: str) -> tuple[str, str | None]:
        """Execute one tool call for real. Returns (result_text, error_or_None)."""
        if name == "write_file":
            return self._tool_write_file(args, workdir)
        if name == "read_file":
            return self._tool_read_file(args, workdir)
        if name == "list_dir":
            return self._tool_list_dir(args, workdir)
        if name == "run_command":
            return self._tool_run_command(args, workdir)
        return f"Unknown tool: {name}", None

    @staticmethod
    def _resolve_in_workdir(workdir: str, rel_path: str) -> str:
        """Resolve a repo-relative path, refusing escapes outside ``workdir``."""
        if not rel_path:
            raise ValueError("path is required")
        base = os.path.realpath(workdir)
        target = os.path.realpath(os.path.join(base, rel_path))
        if target != base and not target.startswith(base + os.sep):
            raise ValueError(f"path escapes working directory: {rel_path!r}")
        return target

    def _tool_write_file(self, args: dict[str, Any], workdir: str) -> tuple[str, str | None]:
        path = args.get("path", "")
        content = args.get("content", "")
        try:
            target = self._resolve_in_workdir(workdir, path)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, "w", encoding="utf-8") as fh:
                fh.write(content)
            return f"Wrote {len(content)} bytes to {path}", None
        except Exception as exc:
            return "", f"{type(exc).__name__}: {exc}"

    def _tool_read_file(self, args: dict[str, Any], workdir: str) -> tuple[str, str | None]:
        path = args.get("path", "")
        try:
            target = self._resolve_in_workdir(workdir, path)
            with open(target, "r", encoding="utf-8") as fh:
                data = fh.read()
            return data[:8000], None
        except Exception as exc:
            return "", f"{type(exc).__name__}: {exc}"

    def _tool_list_dir(self, args: dict[str, Any], workdir: str) -> tuple[str, str | None]:
        path = args.get("path", "") or "."
        try:
            # Empty path means the repo root — resolve directly, skipping the
            # "path is required" guard that applies to file read/write.
            target = os.path.realpath(workdir) if path == "." else self._resolve_in_workdir(workdir, path)
            if not os.path.isdir(target):
                return "", f"not a directory: {path}"
            entries = sorted(os.listdir(target))
            return "\n".join(entries)[:8000], None
        except Exception as exc:
            return "", f"{type(exc).__name__}: {exc}"

    def _tool_run_command(self, args: dict[str, Any], workdir: str) -> tuple[str, str | None]:
        command = args.get("command", "")
        safety_error = _command_safety_error(command)
        if safety_error:
            return "", f"command refused: {safety_error}"
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=workdir,
                capture_output=True,
                text=True,
                timeout=self.command_timeout,
            )
            output = result.stdout[-8000:]
            if result.stderr:
                output += "\n[stderr]\n" + result.stderr[-2000:]
            output += f"\n[exit code: {result.returncode}]"
            return output, None
        except subprocess.TimeoutExpired:
            return "", f"command timed out after {self.command_timeout}s"
        except Exception as exc:
            return "", f"{type(exc).__name__}: {exc}"


# ── Global singleton ─────────────────────────────────────────────────────────

default_agentic_worker_loop = AgenticWorkerLoop()
