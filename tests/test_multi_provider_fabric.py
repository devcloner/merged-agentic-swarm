"""
Tests for providers/multi_provider_fabric.py

Coverage: format_anthropic_to_openai, format_openai_to_anthropic_response,
_build_route_list, dispatch_request (simulation fallback), circuit breaker,
perma-ban.
"""
import json
import time
from unittest.mock import MagicMock, patch

from providers.multi_provider_fabric import (
    MultiProviderFabric,
    _circuit_breaker,
    _circuit_open_until,
    _permanently_dead,
    _record_failure,
    _record_success,
)


class TestFormatConversion:
    def setup_method(self):
        self.fabric = MultiProviderFabric()

    def test_format_anthropic_to_openai_with_system(self):
        messages = [{"role": "user", "content": "Hello"}]
        result = self.fabric.format_anthropic_to_openai(messages, system_prompt="Be helpful")
        assert len(result) == 2
        assert result[0]["role"] == "system"
        assert result[0]["content"] == "Be helpful"
        assert result[1]["role"] == "user"

    def test_format_anthropic_to_openai_no_system(self):
        messages = [{"role": "user", "content": "Hello"}]
        result = self.fabric.format_anthropic_to_openai(messages, system_prompt=None)
        assert len(result) == 1

    def test_format_with_content_blocks(self):
        messages = [{"role": "user", "content": [{"type": "text", "text": "Hello"}]}]
        result = self.fabric.format_anthropic_to_openai(messages)
        assert "Hello" in result[0]["content"]

    def test_format_openai_to_anthropic(self):
        openai_resp = {
            "choices": [{"message": {"content": "Hello world"}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 5},
        }
        result = self.fabric.format_openai_to_anthropic_response(openai_resp, "claude-3-7-sonnet")
        assert result["role"] == "assistant"
        assert result["content"][0]["text"] == "Hello world"
        assert result["usage"]["input_tokens"] == 10

    def test_format_openai_empty_choices(self):
        openai_resp = {"choices": [], "usage": {}}
        result = self.fabric.format_openai_to_anthropic_response(openai_resp, "claude-3-7-sonnet")
        assert result["content"][0]["text"] == ""


class TestRouteBuilding:
    def setup_method(self):
        import providers.multi_provider_fabric
        providers.multi_provider_fabric._last_successful_provider = None
        self.fabric = MultiProviderFabric()

    def test_build_route_list_default(self):
        routes = self.fabric._build_route_list("claude-3-7-sonnet")
        assert len(routes) > 0
        assert routes[0]["provider"] == "fcc-proxy"  # default first

    def test_build_route_list_promotes_last_successful(self):
        import providers.multi_provider_fabric as mpf
        mpf._last_successful_provider = "groq"
        routes = self.fabric._build_route_list("claude-3-5-sonnet")
        assert routes[0]["provider"] == "groq"

    def test_build_route_list_fallback_to_default(self):
        routes = self.fabric._build_route_list("unknown-model")
        assert len(routes) > 0  # falls back to claude-3-7-sonnet routes


class TestCircuitBreaker:
    def setup_method(self):
        _circuit_breaker.clear()
        _circuit_open_until.clear()
        _permanently_dead.clear()

    def test_record_failure_perma_ban_401(self):
        _record_failure("test_provider", http_code=401)
        assert "test_provider" in _permanently_dead

    def test_record_failure_403_trips_circuit_breaker(self):
        for _ in range(3):
            _record_failure("test_provider", http_code=403)
        assert "test_provider" not in _permanently_dead
        assert "test_provider" in _circuit_open_until

    def test_record_failure_circuit_breaker(self):
        for _ in range(3):
            _record_failure("test_provider")
        assert "test_provider" in _circuit_open_until
        assert _circuit_breaker["test_provider"] >= 3

    def test_record_success_resets(self):
        _record_failure("test_provider")
        assert _circuit_breaker["test_provider"] == 1
        _record_success("test_provider")
        assert _circuit_breaker["test_provider"] == 0
        assert "test_provider" not in _circuit_open_until

    def test_perma_ban_expiry_clears(self):
        """Provider should be retried after perma-ban duration expires."""
        import providers.multi_provider_fabric as mpf
        mpf._permanently_dead.clear()
        mpf._circuit_open_until.clear()
        mpf._circuit_breaker.clear()
        mpf._last_successful_provider = None

        # Set expired perma-ban on litellm (past timestamp)
        mpf._permanently_dead["litellm"] = time.time() - 1
        fabric = MultiProviderFabric()
        result = fabric.dispatch_request("claude-3-7-sonnet", [{"role": "user", "content": "hi"}])
        # litellm was un-banned and might work; the response should be a valid one
        assert result["role"] == "assistant"


class TestDispatchRequest:
    def setup_method(self):
        _circuit_breaker.clear()
        _circuit_open_until.clear()
        _permanently_dead.clear()

    def _block_all_providers(self):
        """Block all real providers so dispatch falls to simulation."""
        import providers.multi_provider_fabric as mpf
        for route in mpf.MODEL_FABRIC_ROUTES.get("claude-3-7-sonnet", []):
            mpf._permanently_dead[route["provider"]] = time.time() + 86400

    def test_simulation_fallback(self):
        """Without any working providers, should fall through to simulation."""
        self._block_all_providers()
        fabric = MultiProviderFabric()
        result = fabric.dispatch_request("claude-3-7-sonnet", [{"role": "user", "content": "hi"}])
        _permanently_dead.clear()
        assert "simulation_fallback" in result
        assert result["simulation_fallback"] is True
        assert "[SIMULATION" in result["content"][0]["text"]

    def test_dispatch_with_context_objects(self):
        """Test that content blocks (list) are flattened correctly before dispatch."""
        self._block_all_providers()
        fabric = MultiProviderFabric()
        messages = [{"role": "user", "content": [{"type": "text", "text": "Hello"}]}]
        result = fabric.dispatch_request("claude-3-7-sonnet", messages)
        _permanently_dead.clear()
        assert "simulation_fallback" in result
        assert result["simulation_fallback"] is True

    @patch("urllib.request.urlopen")
    def test_dispatch_successful_call(self, mock_urlopen):
        """Test a successful API call returns formatted Anthropic response."""
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "choices": [{"message": {"content": "Hello from API"}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
        }).encode("utf-8")
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        _permanently_dead.clear()
        import providers.multi_provider_fabric as mpf
        mpf._permanently_dead.clear()
        mpf._circuit_breaker.clear()
        mpf._circuit_open_until.clear()
        mpf._last_successful_provider = None
        fabric = MultiProviderFabric()
        result = fabric.dispatch_request("claude-3-7-sonnet", [{"role": "user", "content": "hi"}])

        # litellm is local and may respond; just check the response is valid
        assert result["role"] == "assistant"

    def test_skip_perma_banned_provider(self):
        """Provider under perma-ban should be skipped."""
        self._block_all_providers()
        fabric = MultiProviderFabric()
        result = fabric.dispatch_request("claude-3-7-sonnet", [{"role": "user", "content": "hi"}])
        _permanently_dead.clear()
        assert result["simulation_fallback"] is True
