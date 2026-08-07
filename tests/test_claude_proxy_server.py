"""
Tests for proxy/claude_proxy_server.py

Coverage: ClaudeProxyHandler (do_GET, do_POST), ProxyServerDaemon
(start, stop), JSON response helpers, multipart audio parsing, and
Whisper transcription forwarding (backend HTTP transport stubbed).
"""

import json

import pytest

from merged_agentic_swarm.proxy import claude_proxy_server
from merged_agentic_swarm.proxy.claude_proxy_server import (
    ProxyServerDaemon,
    _forward_transcription,
    _parse_multipart,
)


class _FakeResp:
    def __init__(self, status_code=200, json_data=None, text=""):
        self.status_code = status_code
        self._json = json_data or {}
        self.text = text

    def json(self):
        return self._json


def _multipart_body(include_file=True):
    parts = []
    if include_file:
        parts.append(
            b"--boundary123\r\n"
            b'Content-Disposition: form-data; name="file"; filename="test.wav"\r\n'
            b"Content-Type: audio/wav\r\n"
            b"\r\n"
            b"WAVE-data-bytes\r\n"
        )
    parts.append(b'--boundary123\r\nContent-Disposition: form-data; name="model"\r\n\r\nopenai/whisper-large-v3\r\n')
    parts.append(b"--boundary123--\r\n")
    return b"".join(parts)


class TestParseMultipart:
    def test_parses_file_and_model(self):
        body = _multipart_body()
        file_data, file_name, model_name = _parse_multipart(body, "multipart/form-data; boundary=boundary123")
        assert file_data == b"WAVE-data-bytes"
        assert file_name == "test.wav"
        assert model_name == "openai/whisper-large-v3"

    def test_no_file_field(self):
        body = _multipart_body(include_file=False)
        file_data, _file_name, model_name = _parse_multipart(body, "multipart/form-data; boundary=boundary123")
        assert file_data is None
        assert model_name == "openai/whisper-large-v3"

    def test_missing_boundary(self):
        file_data, file_name, model_name = _parse_multipart(b"", "multipart/form-data")
        assert file_data is None and file_name is None and model_name is None

    def test_default_model_when_no_model_field(self):
        body = (
            b"--boundary123\r\n"
            b'Content-Disposition: form-data; name="file"; filename="a.mp3"\r\n'
            b"\r\n"
            b"MP3DATA\r\n"
            b"--boundary123--\r\n"
        )
        _, file_name, model_name = _parse_multipart(body, "multipart/form-data; boundary=boundary123")
        assert file_name == "a.mp3"
        assert model_name == "openai/whisper-large-v3"


class TestForwardTranscription:
    def test_success_returns_json(self, monkeypatch):
        monkeypatch.setattr(
            claude_proxy_server.requests,
            "post",
            lambda *a, **k: _FakeResp(200, {"text": "hello world"}),
        )
        result = _forward_transcription(b"WAVE", "a.wav", "openai/whisper-large-v3")
        assert result == {"text": "hello world"}

    def test_connection_error_returns_503(self, monkeypatch):
        def boom(*a, **k):
            raise claude_proxy_server.requests.exceptions.ConnectionError("down")

        monkeypatch.setattr(claude_proxy_server.requests, "post", boom)
        code, body = _forward_transcription(b"WAVE", "a.wav", "model")
        assert code == 503
        assert "unavailable" in body["error"]

    def test_generic_exception_returns_500(self, monkeypatch):
        def boom(*a, **k):
            raise RuntimeError("bad gateway")

        monkeypatch.setattr(claude_proxy_server.requests, "post", boom)
        code, body = _forward_transcription(b"WAVE", "a.wav", "model")
        assert code == 500
        assert "Transcription error" in body["error"]

    def test_backend_error_returns_status(self, monkeypatch):
        monkeypatch.setattr(
            claude_proxy_server.requests,
            "post",
            lambda *a, **k: _FakeResp(502, text="upstream failed"),
        )
        code, body = _forward_transcription(b"WAVE", "a.wav", "model")
        assert code == 502
        assert "NIM transcription failed" in body["error"]

    def test_unknown_extension_defaults_to_wav(self, monkeypatch):
        captured = {}

        def fake_post(url, **kwargs):
            captured["files"] = kwargs["files"]
            return _FakeResp(200, {"text": "ok"})

        monkeypatch.setattr(claude_proxy_server.requests, "post", fake_post)
        _forward_transcription(b"WAVE", "noext", "model")
        name, data, mime = captured["files"]["file"]
        assert name == "noext"
        assert data == b"WAVE"
        assert mime == "audio/wav"


class TestProxyServerDaemon:
    def test_start_stop(self):
        """ProxyServerDaemon should start and stop without error."""
        server = ProxyServerDaemon(host="127.0.0.1", port=0)  # port 0 = random
        server.start()
        assert server.server is not None
        assert server.thread is not None
        server.stop()
        assert server.server is None

    def test_double_start(self):
        """Calling start() twice should not create a second server."""
        server = ProxyServerDaemon(host="127.0.0.1", port=0)
        server.start()
        first_server = server.server
        server.start()
        assert server.server is first_server  # same instance
        server.stop()


class TestClaudeProxyHandler:
    @pytest.fixture(autouse=True)
    def setup_server(self):
        """Start a server on random port for each test."""
        self.server = ProxyServerDaemon(host="127.0.0.1", port=0)
        self.server.start()
        # Get actual port
        self.port = self.server.server.server_address[1]
        self.base_url = f"http://127.0.0.1:{self.port}"
        yield
        self.server.stop()

    def test_health_endpoint(self):
        import urllib.request

        resp = urllib.request.urlopen(f"{self.base_url}/health", timeout=5)
        assert resp.status == 200
        data = json.loads(resp.read().decode("utf-8"))
        assert data["status"] == "ok"
        assert data["service"] == "Claude-Shaped Key Pool Proxy"

    def test_status_endpoint(self):
        import urllib.request

        resp = urllib.request.urlopen(f"{self.base_url}/status", timeout=5)
        assert resp.status == 200
        data = json.loads(resp.read().decode("utf-8"))
        assert data["status"] == "active"
        assert "key_pools" in data

    def test_status_endpoint_includes_per_key_metrics(self):
        """#42: /status surfaces exhausted/cooldown/latency per provider."""
        import urllib.request

        resp = urllib.request.urlopen(f"{self.base_url}/status", timeout=5)
        data = json.loads(resp.read().decode("utf-8"))
        pools = data["key_pools"]
        assert pools, "expected at least one provider pool"
        for info in pools.values():
            assert "exhausted_keys" in info
            assert "next_cooldown_until" in info
            assert "avg_latency_ms" in info

    def test_get_unknown_endpoint_returns_404(self):
        import urllib.request
        from urllib.error import HTTPError

        with pytest.raises(HTTPError) as exc:
            urllib.request.urlopen(f"{self.base_url}/unknown", timeout=5)
        assert exc.value.code == 404

    def test_post_oversized_json_body_rejected_413(self, monkeypatch):
        """#35: a body over the JSON cap must be rejected before buffering."""
        import urllib.request
        from urllib.error import HTTPError

        import merged_agentic_swarm.proxy.claude_proxy_server as proxy_mod

        monkeypatch.setattr(proxy_mod, "MAX_JSON_BODY_BYTES", 1024)
        req = urllib.request.Request(
            f"{self.base_url}/v1/chat/completions",
            data=b"x" * 2048,
            headers={"Content-Type": "application/json", "x-api-key": "freecc"},
            method="POST",
        )
        with pytest.raises(HTTPError) as exc:
            urllib.request.urlopen(req, timeout=5)
        assert exc.value.code == 413

    def test_post_json_body_within_limit_not_413(self, monkeypatch):
        """#35: a body under the cap still reaches normal processing (400 here)."""
        import urllib.request
        from urllib.error import HTTPError

        import merged_agentic_swarm.proxy.claude_proxy_server as proxy_mod

        monkeypatch.setattr(proxy_mod, "MAX_JSON_BODY_BYTES", 1024)
        req = urllib.request.Request(
            f"{self.base_url}/v1/chat/completions",
            data=b"x" * 500,  # under the cap → JSON parse fails → 400, not 413
            headers={"Content-Type": "application/json", "x-api-key": "freecc"},
            method="POST",
        )
        with pytest.raises(HTTPError) as exc:
            urllib.request.urlopen(req, timeout=5)
        assert exc.value.code == 400

    def test_post_oversized_audio_body_rejected_413(self, monkeypatch):
        """#35: audio multipart bodies have their own (higher) cap."""
        import urllib.request
        from urllib.error import HTTPError

        import merged_agentic_swarm.proxy.claude_proxy_server as proxy_mod

        monkeypatch.setattr(proxy_mod, "MAX_AUDIO_BODY_BYTES", 1024)
        req = urllib.request.Request(
            f"{self.base_url}/v1/audio/transcriptions",
            data=b"x" * 2048,
            headers={
                "Content-Type": "multipart/form-data; boundary=abc",
                "x-api-key": "freecc",
            },
            method="POST",
        )
        with pytest.raises(HTTPError) as exc:
            urllib.request.urlopen(req, timeout=5)
        assert exc.value.code == 413

    def test_post_chat_completions_with_invalid_json(self):
        import urllib.request
        from urllib.error import HTTPError

        req = urllib.request.Request(
            f"{self.base_url}/v1/chat/completions",
            data=b"not json",
            headers={"Content-Type": "application/json", "x-api-key": "freecc"},
            method="POST",
        )
        with pytest.raises(HTTPError) as exc:
            urllib.request.urlopen(req, timeout=5)
        assert exc.value.code == 400

    def test_post_v1_messages(self):
        """POST /v1/messages should return a response (simulation fallback)."""
        import urllib.request

        payload = json.dumps(
            {
                "model": "claude-3-7-sonnet",
                "messages": [{"role": "user", "content": "Hi"}],
            }
        ).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/v1/messages",
            data=payload,
            headers={"Content-Type": "application/json", "x-api-key": "freecc"},
            method="POST",
        )
        resp = urllib.request.urlopen(req, timeout=10)
        assert resp.status == 200
        data = json.loads(resp.read().decode("utf-8"))
        # Should have content (even if simulation)
        assert "content" in data

    def test_post_v1_messages_without_token_returns_401(self):
        """POST /v1/messages without an auth token → 401."""
        import urllib.request
        from urllib.error import HTTPError

        payload = json.dumps(
            {
                "model": "claude-3-7-sonnet",
                "messages": [{"role": "user", "content": "Hi"}],
            }
        ).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/v1/messages",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with pytest.raises(HTTPError) as exc:
            urllib.request.urlopen(req, timeout=5)
        assert exc.value.code == 401

    def test_post_v1_messages_with_wrong_token_returns_401(self):
        """POST /v1/messages with an invalid token → 401."""
        import urllib.request
        from urllib.error import HTTPError

        payload = json.dumps(
            {
                "model": "claude-3-7-sonnet",
                "messages": [{"role": "user", "content": "Hi"}],
            }
        ).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/v1/messages",
            data=payload,
            headers={"Content-Type": "application/json", "x-api-key": "bad-token-xyz"},
            method="POST",
        )
        with pytest.raises(HTTPError) as exc:
            urllib.request.urlopen(req, timeout=5)
        assert exc.value.code == 401

    def test_post_v1_messages_with_bearer_token(self):
        """POST /v1/messages authenticated via Authorization: Bearer → 200."""
        import urllib.request

        payload = json.dumps(
            {
                "model": "claude-3-7-sonnet",
                "messages": [{"role": "user", "content": "Hi"}],
            }
        ).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/v1/messages",
            data=payload,
            headers={"Content-Type": "application/json", "Authorization": "Bearer freecc"},
            method="POST",
        )
        resp = urllib.request.urlopen(req, timeout=10)
        assert resp.status == 200

    def test_options_request(self):
        """OPTIONS request should return CORS headers."""
        import urllib.request

        req = urllib.request.Request(
            f"{self.base_url}/health",
            method="OPTIONS",
        )
        resp = urllib.request.urlopen(req, timeout=5)
        assert resp.status == 200

    def test_post_unsupported_endpoint(self):
        """POST to unsupported path should return 404."""
        import urllib.request
        from urllib.error import HTTPError

        payload = json.dumps({"test": True}).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/unsupported",
            data=payload,
            headers={"Content-Type": "application/json", "x-api-key": "freecc"},
            method="POST",
        )
        with pytest.raises(HTTPError) as exc:
            urllib.request.urlopen(req, timeout=5)
        assert exc.value.code == 404

    def test_empty_content_length(self):
        """POST with zero content-length should be handled."""
        import urllib.request

        req = urllib.request.Request(
            f"{self.base_url}/v1/messages",
            data=b"{}",
            headers={"Content-Type": "application/json", "x-api-key": "freecc"},
            method="POST",
        )
        resp = urllib.request.urlopen(req, timeout=10)
        assert resp.status == 200

    def test_post_chat_completions_openai_conversion(self, monkeypatch):
        """POST /v1/chat/completions converts an Anthropic response to OpenAI shape."""
        import urllib.request

        from merged_agentic_swarm.proxy import claude_proxy_server as mod

        def fake_dispatch(**kwargs):
            assert kwargs["model_alias"] == "claude-3-7-sonnet"
            return {
                "id": "msg_123",
                "content": [{"type": "text", "text": "converted reply"}],
                "usage": {"input_tokens": 5, "output_tokens": 3},
            }

        monkeypatch.setattr(mod.default_fabric, "dispatch_request", fake_dispatch)
        payload = json.dumps(
            {
                "model": "claude-3-7-sonnet",
                "messages": [{"role": "user", "content": "Hi"}],
            }
        ).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/v1/chat/completions",
            data=payload,
            headers={"Content-Type": "application/json", "x-api-key": "freecc"},
            method="POST",
        )
        resp = urllib.request.urlopen(req, timeout=10)
        assert resp.status == 200
        data = json.loads(resp.read().decode("utf-8"))
        assert data["object"] == "chat.completion"
        assert data["choices"][0]["message"]["content"] == "converted reply"
        assert data["id"] == "msg_123"

    def test_post_audio_transcriptions_success(self, monkeypatch):
        """Multipart audio POST → forwarded to Whisper backend → JSON response."""
        import urllib.request

        from merged_agentic_swarm.proxy import claude_proxy_server as mod

        monkeypatch.setattr(
            mod.requests,
            "post",
            lambda *a, **k: _FakeResp(200, {"text": "transcribed"}),
        )
        req = urllib.request.Request(
            f"{self.base_url}/v1/audio/transcriptions",
            data=_multipart_body(),
            headers={"Content-Type": "multipart/form-data; boundary=boundary123", "x-api-key": "freecc"},
            method="POST",
        )
        resp = urllib.request.urlopen(req, timeout=10)
        assert resp.status == 200
        data = json.loads(resp.read().decode("utf-8"))
        assert data["text"] == "transcribed"

    def test_post_audio_transcriptions_no_file(self, monkeypatch):
        """Multipart POST without a file field → 400."""
        import urllib.request
        from urllib.error import HTTPError

        from merged_agentic_swarm.proxy import claude_proxy_server as mod

        monkeypatch.setattr(
            mod.requests,
            "post",
            lambda *a, **k: _FakeResp(200, {"text": "unused"}),
        )
        req = urllib.request.Request(
            f"{self.base_url}/v1/audio/transcriptions",
            data=_multipart_body(include_file=False),
            headers={"Content-Type": "multipart/form-data; boundary=boundary123", "x-api-key": "freecc"},
            method="POST",
        )
        with pytest.raises(HTTPError) as exc:
            urllib.request.urlopen(req, timeout=10)
        assert exc.value.code == 400

    def test_post_audio_transcriptions_backend_down(self, monkeypatch):
        """Backend connection failure → 503 with unavailable message."""
        import urllib.request
        from urllib.error import HTTPError

        from merged_agentic_swarm.proxy import claude_proxy_server as mod

        def boom(*a, **k):
            raise mod.requests.exceptions.ConnectionError("nim not running")

        monkeypatch.setattr(mod.requests, "post", boom)
        req = urllib.request.Request(
            f"{self.base_url}/v1/audio/transcriptions",
            data=_multipart_body(),
            headers={"Content-Type": "multipart/form-data; boundary=boundary123", "x-api-key": "freecc"},
            method="POST",
        )
        with pytest.raises(HTTPError) as exc:
            urllib.request.urlopen(req, timeout=10)
        assert exc.value.code == 503
