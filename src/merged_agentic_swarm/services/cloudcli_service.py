"""CloudCLI client — trigger remote AI agents via the cloneclove.com /api/agent endpoint.

CloudCLI clones a GitHub repo (or targets an existing project path) and runs a
Claude, Cursor, Codex, or OpenCode agent against it, optionally creating a
branch and pull request. Unlike the chat-completions providers in the fabric,
this is an agent-triggering API authenticated with an ``X-API-Key`` header; the
key is read from the ``CLOUDCLI_API_KEY`` env var and is never hardcoded.
"""

from __future__ import annotations

import json
import logging
import os
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any

import httpx

logger = logging.getLogger("cloudcli")

DEFAULT_BASE_URL = "https://cloneclove.com"
DEFAULT_TIMEOUT = 600.0
PROVIDERS = ("claude", "cursor", "codex", "opencode")


class CloudCLIError(RuntimeError):
    """Raised when CloudCLI returns a non-2xx response or is misconfigured."""


@dataclass
class CloudCLIConfig:
    base_url: str = DEFAULT_BASE_URL
    timeout: float = DEFAULT_TIMEOUT

    @classmethod
    def from_env(cls) -> CloudCLIConfig:
        env = os.environ.get
        return cls(
            base_url=env("CLOUDCLI_BASE_URL", DEFAULT_BASE_URL),
            timeout=float(env("CLOUDCLI_TIMEOUT", str(DEFAULT_TIMEOUT))),
        )


class CloudCLIClient:
    """Minimal client for the CloudCLI agent API (``POST /api/agent``)."""

    def __init__(self, api_key: str | None = None, config: CloudCLIConfig | None = None) -> None:
        self.api_key = api_key or os.environ.get("CLOUDCLI_API_KEY", "")
        self.config = config or CloudCLIConfig.from_env()
        self._headers = {"Content-Type": "application/json", "X-API-Key": self.api_key}

    def trigger_agent(
        self,
        message: str,
        *,
        github_url: str | None = None,
        project_path: str | None = None,
        provider: str = "claude",
        model: str | None = None,
        effort: str | None = None,
        cleanup: bool = True,
        github_token: str | None = None,
        branch_name: str | None = None,
        create_branch: bool = False,
        create_pr: bool = False,
    ) -> dict[str, Any]:
        """Trigger a remote agent (non-streaming) and return the JSON response."""
        if not self.api_key:
            raise CloudCLIError("CLOUDCLI_API_KEY is not set")
        payload = self._build_payload(
            message=message,
            github_url=github_url,
            project_path=project_path,
            provider=provider,
            model=model,
            effort=effort,
            cleanup=cleanup,
            github_token=github_token,
            branch_name=branch_name,
            create_branch=create_branch,
            create_pr=create_pr,
        )
        with httpx.Client(base_url=self.config.base_url, headers=self._headers, timeout=self.config.timeout) as client:
            resp = client.post("/api/agent", json=payload)
            if resp.status_code >= 400:
                raise CloudCLIError(f"CloudCLI returned {resp.status_code}: {resp.text[:200]}")
            return resp.json()

    def stream_agent(
        self,
        message: str,
        *,
        github_url: str | None = None,
        project_path: str | None = None,
        provider: str = "claude",
        model: str | None = None,
        effort: str | None = None,
        cleanup: bool = True,
        github_token: str | None = None,
        branch_name: str | None = None,
        create_branch: bool = False,
        create_pr: bool = False,
    ) -> Iterator[dict[str, Any]]:
        """Trigger a remote agent with streaming (SSE) and yield each event dict."""
        if not self.api_key:
            raise CloudCLIError("CLOUDCLI_API_KEY is not set")
        payload = self._build_payload(
            message=message,
            github_url=github_url,
            project_path=project_path,
            provider=provider,
            model=model,
            effort=effort,
            cleanup=cleanup,
            github_token=github_token,
            branch_name=branch_name,
            create_branch=create_branch,
            create_pr=create_pr,
            stream=True,
        )
        with (
            httpx.Client(base_url=self.config.base_url, headers=self._headers, timeout=self.config.timeout) as client,
            client.stream("POST", "/api/agent", json=payload) as resp,
        ):
            if resp.status_code >= 400:
                raise CloudCLIError(f"CloudCLI returned {resp.status_code}: {resp.read()[:200]}")
            for line in resp.iter_lines():
                if not line.startswith("data:"):
                    continue
                data = line[len("data:") :].strip()
                if not data:
                    continue
                try:
                    yield json.loads(data)
                except json.JSONDecodeError:
                    logger.warning("Skipping non-JSON SSE line: %s", data[:80])

    @staticmethod
    def _build_payload(
        *,
        message: str,
        github_url: str | None,
        project_path: str | None,
        provider: str,
        model: str | None,
        effort: str | None,
        cleanup: bool,
        github_token: str | None,
        branch_name: str | None,
        create_branch: bool,
        create_pr: bool,
        stream: bool = False,
    ) -> dict[str, Any]:
        if not message.strip():
            raise ValueError("message is required")
        if not github_url and not project_path:
            raise ValueError("Provide github_url or project_path")
        if provider not in PROVIDERS:
            raise ValueError(f"provider must be one of {PROVIDERS}")

        payload: dict[str, Any] = {
            "message": message,
            "provider": provider,
            "stream": stream,
            "cleanup": cleanup,
        }
        if github_url:
            payload["githubUrl"] = github_url
        if project_path:
            payload["projectPath"] = project_path
        if model:
            payload["model"] = model
        if effort:
            payload["effort"] = effort
        if github_token:
            payload["githubToken"] = github_token
        if branch_name:
            payload["branchName"] = branch_name
            payload["createBranch"] = True
        if create_branch:
            payload["createBranch"] = True
        if create_pr:
            payload["createPR"] = True
        return payload
