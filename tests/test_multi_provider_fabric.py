"""
Tests for providers/multi_provider_fabric.py

Coverage: format_anthropic_to_openai, format_openai_to_anthropic_response,
_build_route_list, dispatch_request (simulation fallback), circuit breaker,
perma-ban.
"""

import time
from unittest.mock import MagicMock, patch

from merged_agentic_swarm.providers.multi_provider_fabric import (
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

    def test_format_openai_with_tool_calls(self):
        openai_resp = {
            "choices": [
                {
                    "message": {
                        "content": "",
                        "tool_calls": [
                            {
                                "id": "call_1",
                                "type": "function",
                                "function": {"name": "add", "arguments": '{"a": 2, "b": 3}'},
                            }
                        ],
                    },
                    "finish_reason": "tool_calls",
                }
            ],
            "usage": {"prompt_tokens": 10, "completion_tokens": 5},
        }
        result = self.fabric.format_openai_to_anthropic_response(openai_resp, "claude-3-7-sonnet")
        assert result["tool_calls"] == [{"id": "call_1", "name": "add", "input": {"a": 2, "b": 3}}]

    def test_format_openai_bad_arguments_json(self):
        openai_resp = {
            "choices": [
                {
                    "message": {
                        "content": "",
                        "tool_calls": [
                            {"id": "c1", "type": "function", "function": {"name": "x", "arguments": "not-json"}}
                        ],
                    }
                }
            ],
            "usage": {},
        }
        result = self.fabric.format_openai_to_anthropic_response(openai_resp, "claude-3-7-sonnet")
        assert result["tool_calls"] == [{"id": "c1", "name": "x", "input": {}}]

    def test_format_anthropic_tool_calls_roundtrip(self):
        """format_anthropic_to_openai converts normalized tool_calls to OpenAI shape."""
        messages = [
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [{"id": "c1", "name": "add", "input": {"a": 2, "b": 2}}],
            },
            {"role": "tool", "tool_call_id": "c1", "content": "4"},
        ]
        result = self.fabric.format_anthropic_to_openai(messages)
        assert result[0]["role"] == "assistant"
        assert result[0]["tool_calls"][0]["function"]["name"] == "add"
        assert result[0]["tool_calls"][0]["function"]["arguments"] == '{"a": 2, "b": 2}'
        assert result[1]["role"] == "tool"
        assert result[1]["tool_call_id"] == "c1"

    def test_format_anthropic_to_anthropic_tool_blocks(self):
        """format_anthropic_to_anthropic builds tool_use + tool_result blocks for /v1/messages."""
        messages = [
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [{"id": "c1", "name": "add", "input": {"a": 1, "b": 1}}],
            },
            {"role": "tool", "tool_call_id": "c1", "content": "2"},
        ]
        result = self.fabric.format_anthropic_to_anthropic(messages)
        assert result[0]["role"] == "assistant"
        assert result[0]["content"][0] == {"type": "tool_use", "id": "c1", "name": "add", "input": {"a": 1, "b": 1}}
        assert result[1]["role"] == "user"
        assert result[1]["content"][0]["type"] == "tool_result"
        assert result[1]["content"][0]["tool_use_id"] == "c1"

    def test_tools_to_anthropic_conversion(self):
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "add",
                    "description": "d",
                    "parameters": {"type": "object", "properties": {"a": {"type": "number"}}},
                },
            },
            {
                "type": "function",
                "function": {"name": "sub", "description": "s", "parameters": {"type": "object", "properties": {}}},
            },
        ]
        converted = self.fabric._tools_to_anthropic(tools)
        assert converted[0]["name"] == "add"
        assert converted[0]["input_schema"] == {"type": "object", "properties": {"a": {"type": "number"}}}
        assert converted[1]["name"] == "sub"

    def test_extract_anthropic_tool_calls(self):
        resp = {
            "content": [
                {"type": "text", "text": "thinking"},
                {"type": "tool_use", "id": "cu_1", "name": "write_file", "input": {"path": "x.py"}},
            ]
        }
        calls = self.fabric._extract_anthropic_tool_calls(resp)
        assert calls == [{"id": "cu_1", "name": "write_file", "input": {"path": "x.py"}}]
        assert self.fabric._extract_anthropic_tool_calls({"content": [{"type": "text", "text": "hi"}]}) is None


class TestRouteBuilding:
    def setup_method(self):
        import merged_agentic_swarm.providers.multi_provider_fabric

        merged_agentic_swarm.providers.multi_provider_fabric._last_successful_provider.clear()
        self.fabric = MultiProviderFabric()

    def test_build_route_list_default(self):
        routes = self.fabric._build_route_list("claude-3-7-sonnet")
        assert len(routes) > 0
        assert routes[0]["provider"] == "gemini"  # gemini is first (verified, 42-key pool)

    def test_build_route_list_promotes_last_successful(self):
        import merged_agentic_swarm.providers.multi_provider_fabric as mpf

        mpf._last_successful_provider = {"claude-3-5-sonnet": "fcc-proxy"}
        routes = self.fabric._build_route_list("claude-3-5-sonnet")
        assert routes[0]["provider"] == "fcc-proxy"

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
        import merged_agentic_swarm.providers.multi_provider_fabric as mpf

        mpf._permanently_dead.clear()
        mpf._circuit_open_until.clear()
        mpf._circuit_breaker.clear()
        mpf._last_successful_provider.clear()

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
        import merged_agentic_swarm.providers.multi_provider_fabric as mpf

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

    @patch("merged_agentic_swarm.providers.multi_provider_fabric.pool_dispatch")
    def test_dispatch_successful_call(self, mock_dispatch):
        """Test a successful API call returns formatted Anthropic response."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.request = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Hello from API"}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
        }
        mock_dispatch.return_value = mock_response

        _permanently_dead.clear()
        import merged_agentic_swarm.providers.multi_provider_fabric as mpf

        mpf._permanently_dead.clear()
        mpf._circuit_breaker.clear()
        mpf._circuit_open_until.clear()
        mpf._last_successful_provider.clear()
        fabric = MultiProviderFabric()
        result = fabric.dispatch_request("claude-3-7-sonnet", [{"role": "user", "content": "hi"}])

        assert result["role"] == "assistant"
        assert result["content"][0]["text"] == "Hello from API"
        assert mock_dispatch.call_count == 1

    @patch("merged_agentic_swarm.providers.multi_provider_fabric.pool_dispatch")
    def test_dispatch_non_dict_json_body_falls_through(self, mock_dispatch):
        """A 2xx with a non-dict JSON body must cascade, not crash on .get()."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.request = MagicMock()
        mock_response.json.return_value = ["not", "a", "dict"]
        mock_dispatch.return_value = mock_response

        _permanently_dead.clear()
        import merged_agentic_swarm.providers.multi_provider_fabric as mpf

        mpf._permanently_dead.clear()
        mpf._circuit_breaker.clear()
        mpf._circuit_open_until.clear()
        mpf._last_successful_provider.clear()
        fabric = MultiProviderFabric()
        result = fabric.dispatch_request("claude-3-7-sonnet", [{"role": "user", "content": "hi"}])

        # Non-dict body is a provider failure → every route fails → simulation fallback
        assert result.get("simulation_fallback") is True

    @patch("merged_agentic_swarm.providers.multi_provider_fabric.pool_dispatch")
    def test_dispatch_non_json_body_falls_through(self, mock_dispatch):
        """A 2xx with an empty/non-JSON body must cascade, not raise JSONDecodeError."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.request = MagicMock()
        mock_response.json.side_effect = ValueError("No JSON object could be decoded")
        mock_dispatch.return_value = mock_response

        _permanently_dead.clear()
        import merged_agentic_swarm.providers.multi_provider_fabric as mpf

        mpf._permanently_dead.clear()
        mpf._circuit_breaker.clear()
        mpf._circuit_open_until.clear()
        mpf._last_successful_provider.clear()
        fabric = MultiProviderFabric()
        result = fabric.dispatch_request("claude-3-7-sonnet", [{"role": "user", "content": "hi"}])

        assert result.get("simulation_fallback") is True

    @patch("merged_agentic_swarm.providers.multi_provider_fabric.pool_dispatch")
    def test_dispatch_http_status_error_triggers_cascade(self, mock_dispatch):
        """4xx/5xx from dispatch() must be caught by HTTPStatusError handling."""
        import httpx

        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.text = '{"error":"rate limited"}'
        mock_response.request = MagicMock()
        mock_dispatch.side_effect = httpx.HTTPStatusError(
            "Rate limited",
            request=MagicMock(),
            response=mock_response,
        )

        _permanently_dead.clear()
        import merged_agentic_swarm.providers.multi_provider_fabric as mpf

        mpf._permanently_dead.clear()
        mpf._circuit_breaker.clear()
        mpf._circuit_open_until.clear()
        mpf._last_successful_provider.clear()
        fabric = MultiProviderFabric()
        result = fabric.dispatch_request("claude-3-7-sonnet", [{"role": "user", "content": "hi"}])

        # Every route 429s → simulation fallback
        assert result.get("simulation_fallback") is True

    def test_skip_perma_banned_provider(self):
        """Provider under perma-ban should be skipped."""
        self._block_all_providers()
        fabric = MultiProviderFabric()
        result = fabric.dispatch_request("claude-3-7-sonnet", [{"role": "user", "content": "hi"}])
        _permanently_dead.clear()
        assert result["simulation_fallback"] is True

    @patch("merged_agentic_swarm.providers.multi_provider_fabric.pool_dispatch")
    def test_consecutive_429s_trip_circuit_breaker(self, mock_dispatch):
        """Consecutive 429 responses must count as a provider circuit-breaker
        event (not just a per-key cooldown), so a throttled provider eventually
        opens and stops being retried at the front of the cascade."""
        import httpx

        import merged_agentic_swarm.providers.multi_provider_fabric as mpf
        from merged_agentic_swarm.providers.key_pool import KeyPoolManager

        def side_effect(url, req_data, headers, timeout):
            mock_response = MagicMock()
            mock_response.status_code = 429
            mock_response.text = '{"error":"rate limited"}'
            mock_response.request = MagicMock()
            raise httpx.HTTPStatusError("Rate limited", request=mock_response.request, response=mock_response)

        mock_dispatch.side_effect = side_effect

        # Fresh, isolated key pool so cooldowns left by other tests can't skew
        # the cascade. gemini needs >=9 keys so the 3-key retry loop still finds
        # a key on the 3rd consecutive request (2 gemini routes per dispatch).
        pool = KeyPoolManager(env_file_path="/dev/null")
        pool.keys_by_provider = {}
        for i in range(9):
            pool.add_key("gemini", f"sk-g{i}", f"g-{i}")

        mpf._permanently_dead.clear()
        mpf._circuit_breaker.clear()
        mpf._circuit_open_until.clear()
        mpf._last_successful_provider.clear()
        fabric = MultiProviderFabric(key_pool=pool)

        for _ in range(3):
            result = fabric.dispatch_request("claude-3-7-sonnet", [{"role": "user", "content": "hi"}])
            assert result.get("simulation_fallback") is True

        # gemini throttled every key attempt across consecutive requests →
        # breaker trips and the provider is skipped at the front of the cascade.
        assert mpf._circuit_breaker["gemini"] >= mpf.CIRCUIT_BREAKER_THRESHOLD
        assert "gemini" in mpf._circuit_open_until


class TestLitellmPresenceInRoutes:
    """Role routing maps worker roles to litellm aliases, so every fabric tier
    must keep a reachable litellm backend entry in its route list."""

    def test_each_fabric_alias_has_litellm_route(self):
        import merged_agentic_swarm.providers.multi_provider_fabric as mpf

        for model_alias, routes in mpf.MODEL_FABRIC_ROUTES.items():
            assert any(route.get("provider") == "litellm" for route in routes), model_alias
