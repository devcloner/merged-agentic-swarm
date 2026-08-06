"""
Tests for services/agentic_worker_loop.py

Coverage: real tool execution (write_file/read_file/list_dir/run_command) against
a tmp workdir, the agentic loop's control flow (completion, tool round-trip,
simulation failure, iteration bound), and the command safety denylist.

The HTTP transport layer is mocked via a fake fabric; tool execution itself is
REAL (files on disk, real subprocesses).
"""

import os
from unittest.mock import MagicMock

from merged_agentic_swarm.services.agentic_worker_loop import (
    WORKER_TOOLS,
    AgenticWorkerLoop,
    _command_safety_error,
    _extract_text,
)


class TestCommandSafety:
    def test_denylist_global_destructive(self):
        for cmd in ("sudo rm -rf /", "rm -rf /", "rm -fr /", "rm -rf ~", "git push origin main"):
            assert _command_safety_error(cmd) is not None, cmd

    def test_sudo_token(self):
        assert _command_safety_error("sudo apt install curl") is not None

    def test_allowed_commands(self):
        for cmd in ("echo hello", "git status", "uv run pytest tests/ -q", "python hello.py"):
            assert _command_safety_error(cmd) is None, cmd

    def test_empty_and_parse_failures(self):
        assert _command_safety_error("") is not None
        assert _command_safety_error('echo "unterminated') is not None

    def test_run_command_tool_hints_uv(self):
        """The run_command schema must steer models to the uv toolchain —
        bare ``python`` exits 127 on this host (only uv manages the interpreter)."""
        run_cmd = next(t for t in WORKER_TOOLS if t["function"]["name"] == "run_command")
        description = run_cmd["function"]["description"]
        param_desc = run_cmd["function"]["parameters"]["properties"]["command"]["description"]
        assert "uv run python" in description
        assert "uv run python" in param_desc


class TestRealToolExecution:
    """Tools execute for real against a tmp workdir."""

    def test_write_and_read_file(self, tmp_path):
        loop = AgenticWorkerLoop(workdir=str(tmp_path))
        out, err = loop._tool_write_file({"path": "src/a.py", "content": "x = 1\n"}, str(tmp_path))
        assert err is None, err
        assert os.path.exists(tmp_path / "src" / "a.py")
        out, err = loop._tool_read_file({"path": "src/a.py"}, str(tmp_path))
        assert err is None
        assert "x = 1" in out

    def test_write_file_creates_parents(self, tmp_path):
        loop = AgenticWorkerLoop(workdir=str(tmp_path))
        _, err = loop._tool_write_file({"path": "deep/nested/dir/f.py", "content": "pass"}, str(tmp_path))
        assert err is None
        assert (tmp_path / "deep" / "nested" / "dir" / "f.py").exists()

    def test_path_escape_refused(self, tmp_path):
        loop = AgenticWorkerLoop(workdir=str(tmp_path))
        _, err = loop._tool_write_file({"path": "../evil.py", "content": "print('bad')"}, str(tmp_path))
        assert err is not None
        assert "escapes" in err
        assert not (tmp_path.parent / "evil.py").exists()

    def test_list_dir(self, tmp_path):
        loop = AgenticWorkerLoop(workdir=str(tmp_path))
        (tmp_path / "alpha.txt").write_text("a")
        (tmp_path / "beta.txt").write_text("b")
        out, err = loop._tool_list_dir({"path": ""}, str(tmp_path))
        assert err is None
        assert "alpha.txt" in out and "beta.txt" in out

    def test_run_command_real_subprocess(self, tmp_path):
        loop = AgenticWorkerLoop(workdir=str(tmp_path), command_timeout=30)
        (tmp_path / "hi.py").write_text("print('hello-real')\n")
        out, err = loop._tool_run_command({"command": "uv run python hi.py"}, str(tmp_path))
        assert err is None, err
        assert "hello-real" in out
        assert "[exit code: 0]" in out

    def test_run_command_captures_failure(self, tmp_path):
        loop = AgenticWorkerLoop(workdir=str(tmp_path), command_timeout=30)
        out, err = loop._tool_run_command({"command": "false"}, str(tmp_path))
        assert err is None  # non-zero exit is reported, not an exception
        assert "[exit code: 1]" in out

    def test_run_command_refuses_denylist(self, tmp_path):
        loop = AgenticWorkerLoop(workdir=str(tmp_path))
        _, err = loop._tool_run_command({"command": "rm -rf /"}, str(tmp_path))
        assert err is not None
        assert "refused" in err

    def test_run_command_respects_timeout(self, tmp_path):
        loop = AgenticWorkerLoop(workdir=str(tmp_path), command_timeout=2)
        _, err = loop._tool_run_command({"command": "sleep 10"}, str(tmp_path))
        assert err is not None
        assert "timed out" in err


class _FakeFabric:
    """Scripted fabric: serves a queue of responses, records requests."""

    def __init__(self, responses):
        self._responses = list(responses)
        self.requests = []

    def dispatch_request(self, **kwargs):
        self.requests.append(kwargs)
        if not self._responses:
            return {"type": "message", "content": [{"type": "text", "text": ""}]}
        return self._responses.pop(0)


def _text_response(text):
    return {"type": "message", "role": "assistant", "content": [{"type": "text", "text": text}]}


def _tool_response(name, **kwargs):
    return {
        "type": "message",
        "role": "assistant",
        "content": [{"type": "text", "text": ""}],
        "tool_calls": [{"id": f"call-{name}", "name": name, "input": kwargs}],
    }


class TestLoopControlFlow:
    def test_completes_on_final_text(self, tmp_path):
        """No tool_calls in the response → completed with the model's summary."""
        fabric = _FakeFabric([_text_response("done, no tools needed")])
        loop = AgenticWorkerLoop(fabric=fabric, workdir=str(tmp_path))
        result = loop.execute({"title": "T", "description": "D"})
        assert result["status"] == "completed"
        assert result["final_text"] == "done, no tools needed"
        assert result["files_written"] == []

    def test_executes_tool_call_then_completes(self, tmp_path):
        """Tool call is executed for real, result fed back, then completes."""
        fabric = _FakeFabric(
            [
                _tool_response("write_file", path="greet.py", content="print('hello')\n"),
                _text_response("wrote the file"),
            ]
        )
        loop = AgenticWorkerLoop(fabric=fabric, workdir=str(tmp_path))
        result = loop.execute({"title": "T", "description": "create greet.py"})
        assert result["status"] == "completed"
        assert result["files_written"] == ["greet.py"]
        assert (tmp_path / "greet.py").read_text() == "print('hello')\n"
        # Second dispatch must carry the assistant tool_calls + tool result messages.
        second = fabric.requests[1]
        assert second["tools"] == WORKER_TOOLS
        roles = [m["role"] for m in second["messages"]]
        assert "assistant" in roles and "tool" in roles

    def test_simulation_is_failure(self, tmp_path):
        fabric = _FakeFabric([{"type": "message", "simulation_fallback": True, "content": []}])
        loop = AgenticWorkerLoop(fabric=fabric, workdir=str(tmp_path))
        result = loop.execute({"title": "T", "description": "D"})
        assert result["status"] == "failed"
        assert result["reason"] == "simulation_fallback"
        assert result.get("simulation_fallback") is True

    def test_iteration_bound_keeps_partial_work(self, tmp_path):
        """Hitting max_iterations completes with real partial work kept."""
        fabric = _FakeFabric(
            [
                _tool_response("write_file", path="a.txt", content="1\n"),
                _tool_response("write_file", path="b.txt", content="2\n"),
            ]
        )
        loop = AgenticWorkerLoop(fabric=fabric, workdir=str(tmp_path), max_iterations=2)
        result = loop.execute({"title": "T", "description": "D"})
        assert result["status"] == "completed"
        assert result["iterations_exhausted"] is True
        assert result["iterations"] == 2
        assert (tmp_path / "a.txt").exists() and (tmp_path / "b.txt").exists()

    def test_dispatch_error_fails(self, tmp_path):
        fabric = MagicMock()
        fabric.dispatch_request.side_effect = RuntimeError("boom")
        loop = AgenticWorkerLoop(fabric=fabric, workdir=str(tmp_path))
        result = loop.execute({"title": "T", "description": "D"})
        assert result["status"] == "failed"
        assert "boom" in result["reason"]


class TestExtractText:
    def test_plain_string(self):
        assert _extract_text({"content": "hi"}) == "hi"

    def test_text_blocks(self):
        resp = {"content": [{"type": "text", "text": "a"}, {"type": "text", "text": "b"}]}
        assert _extract_text(resp) == "a\nb"

    def test_tool_use_blocks_ignored(self):
        resp = {"content": [{"type": "tool_use", "name": "x", "input": {}}, {"type": "text", "text": "ok"}]}
        assert _extract_text(resp) == "ok"
