"""
Tests for services/cloudcli_service.py

Coverage: CloudCLIClient — trigger_agent (payload shape, JSON parse, HTTP error),
stream_agent (SSE parsing, skipping malformed lines), _build_payload validation
(api key, provider, message, github_url/project_path), env-var fallbacks.
HTTP transport is stubbed at the httpx.Client level; the environment is stubbed
so tests never read real CLOUDCLI_* variables.
"""

import pytest

from merged_agentic_swarm.services import cloudcli_service as mod
from merged_agentic_swarm.services.cloudcli_service import CloudCLIClient, CloudCLIError


@pytest.fixture(autouse=True)
def _env(monkeypatch):
    fake = {}
    monkeypatch.setattr(mod.os, "environ", fake)
    return fake


class _FakeClient:
    """Context-managed httpx.Client stand-in; records calls and returns a fake response."""

    def __init__(self, response, lines=()):
        self.response = response
        self.lines = list(lines)
        self.calls = []

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def post(self, url, json=None):
        self.calls.append(("post", url, json))
        return self.response

    def stream(self, method, url, json=None):
        self.calls.append(("stream", method, url, json))
        return self.response


class _FakeResp:
    def __init__(self, status_code=200, json_data=None, text="", lines=()):
        self.status_code = status_code
        self._json = json_data
        self.text = text
        self.lines = list(lines)

    def json(self):
        return self._json

    def iter_lines(self):
        return iter(self.lines)

    def read(self):
        return self.text.encode()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def _install_fake_client(monkeypatch, response, lines=()):
    fake = _FakeClient(response, lines)

    class _Ctx:
        def __init__(self, *args, **kwargs):
            pass

        def __enter__(self):
            return fake

        def __exit__(self, *exc):
            return False

    monkeypatch.setattr(mod.httpx, "Client", _Ctx)
    return fake


def _client(api_key="ck-test-key", env=None, config=None):
    if env:
        mod.os.environ.update(env)
    return CloudCLIClient(api_key=api_key, config=config)


class TestTriggerAgent:
    def test_sends_payload_and_parses_json(self, monkeypatch):
        resp = _FakeResp(200, json_data={"success": True, "sessionId": "abc123"})
        fake = _install_fake_client(monkeypatch, resp)
        client = _client()

        out = client.trigger_agent("Add tests", github_url="https://github.com/user/repo", provider="claude")

        assert out["success"] is True
        (method, url, payload) = fake.calls[0]
        assert method == "post"
        assert url == "/api/agent"
        assert payload["message"] == "Add tests"
        assert payload["githubUrl"] == "https://github.com/user/repo"
        assert payload["provider"] == "claude"
        assert payload["stream"] is False
        assert payload["cleanup"] is True

    def test_branch_and_pr_flags(self, monkeypatch):
        fake = _install_fake_client(monkeypatch, _FakeResp(200, json_data={"success": True}))
        client = _client()
        client.trigger_agent("m", project_path="/tmp/p", branch_name="feature/x", create_pr=True)
        (_, _, payload) = fake.calls[0]
        assert payload["projectPath"] == "/tmp/p"
        assert payload["branchName"] == "feature/x"
        assert payload["createBranch"] is True
        assert payload["createPR"] is True

    def test_http_error_raises(self, monkeypatch):
        _install_fake_client(monkeypatch, _FakeResp(401, text="bad key"))
        client = _client()
        with pytest.raises(CloudCLIError, match="401"):
            client.trigger_agent("m", project_path="/tmp/p")


class TestStreamAgent:
    def test_yields_sse_events(self, monkeypatch):
        lines = [
            'data: {"type":"status","message":"Repository cloned"}',
            'data: {"type":"content","content":"Done!"}',
            'data: {"type":"done"}',
        ]
        fake = _install_fake_client(monkeypatch, _FakeResp(200, json_data={}, lines=lines))
        client = _client()

        events = list(client.stream_agent("m", project_path="/tmp/p"))

        assert [e["type"] for e in events] == ["status", "content", "done"]
        (verb, _method, _url, payload) = fake.calls[0]
        assert verb == "stream"
        assert payload["stream"] is True

    def test_skips_non_json_and_blank_lines(self, monkeypatch):
        lines = [
            'data: {"type":"status","message":"ok"}',
            "data: not-json",
            "data:",
            ": keepalive comment",
        ]
        _install_fake_client(monkeypatch, _FakeResp(200, json_data={}, lines=lines))
        client = _client()

        events = list(client.stream_agent("m", project_path="/tmp/p"))

        assert len(events) == 1
        assert events[0]["type"] == "status"

    def test_stream_http_error_raises(self, monkeypatch):
        _install_fake_client(monkeypatch, _FakeResp(500, text="boom"))
        client = _client()
        with pytest.raises(CloudCLIError, match="500"):
            list(client.stream_agent("m", project_path="/tmp/p"))


class TestValidation:
    def test_missing_key(self):
        client = CloudCLIClient(api_key="")
        with pytest.raises(CloudCLIError, match="CLOUDCLI_API_KEY"):
            client.trigger_agent("m", project_path="/tmp/p")

    def test_no_target_raises(self):
        client = _client()
        with pytest.raises(ValueError, match="github_url or project_path"):
            client.trigger_agent("m")

    def test_bad_provider_raises(self):
        client = _client()
        with pytest.raises(ValueError, match="provider"):
            client.trigger_agent("m", project_path="/tmp/p", provider="not-a-provider")

    def test_empty_message_raises(self):
        client = _client()
        with pytest.raises(ValueError, match="message"):
            client.trigger_agent("   ", project_path="/tmp/p")


class TestEnvFallbacks:
    def test_api_key_from_env(self):
        client = _client(api_key=None, env={"CLOUDCLI_API_KEY": "ck-env-key"})
        assert client.api_key == "ck-env-key"

    def test_base_url_from_env(self):
        client = _client(api_key="k", env={"CLOUDCLI_BASE_URL": "http://localhost:9999"})
        assert client.config.base_url == "http://localhost:9999"

    def test_default_base_url(self):
        client = CloudCLIClient(api_key="k")
        assert client.config.base_url == mod.DEFAULT_BASE_URL
