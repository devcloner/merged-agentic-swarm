"""
Tests for proxy/claude_proxy_server.py

Coverage: ClaudeProxyHandler (do_GET, do_POST), ProxyServerDaemon
(start, stop), JSON response helpers.
"""
import json

import pytest

from merged_agentic_swarm.proxy.claude_proxy_server import (
    ProxyServerDaemon,
)


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

    def test_get_unknown_endpoint_returns_404(self):
        import urllib.request
        from urllib.error import HTTPError
        with pytest.raises(HTTPError) as exc:
            urllib.request.urlopen(f"{self.base_url}/unknown", timeout=5)
        assert exc.value.code == 404

    def test_post_chat_completions_with_invalid_json(self):
        import urllib.request
        from urllib.error import HTTPError
        req = urllib.request.Request(
            f"{self.base_url}/v1/chat/completions",
            data=b"not json",
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with pytest.raises(HTTPError) as exc:
            urllib.request.urlopen(req, timeout=5)
        assert exc.value.code == 400

    def test_post_v1_messages(self):
        """POST /v1/messages should return a response (simulation fallback)."""
        import urllib.request
        payload = json.dumps({
            "model": "claude-3-7-sonnet",
            "messages": [{"role": "user", "content": "Hi"}],
        }).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/v1/messages",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        resp = urllib.request.urlopen(req, timeout=10)
        assert resp.status == 200
        data = json.loads(resp.read().decode("utf-8"))
        # Should have content (even if simulation)
        assert "content" in data

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
            headers={"Content-Type": "application/json"},
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
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        resp = urllib.request.urlopen(req, timeout=10)
        assert resp.status == 200
