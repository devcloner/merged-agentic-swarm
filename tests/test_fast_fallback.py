"""
Tests for merged_agentic_swarm/fast_fallback.py

Coverage: parallel probe first-success-wins, cooperative cancellation of
in-flight losers, circuit breaker skip + half-open after cooldown, adaptive
selection promotion of a fast fallback, perma-ban/breaker shared-state honour,
rate-limit key rotation, simulation fallback when all providers are blocked,
config from env, and delegation to the fabric when disabled.

All tests stub ``fast_fallback.pool_dispatch`` and replace the fabric's route
table with a fixed two-route list (providers ``primary``/``fallback``) so probes
are deterministic and no real provider is contacted.
"""
import time
from unittest.mock import MagicMock, patch

import httpx

from merged_agentic_swarm.fast_fallback import (
    FastFallbackConfig,
    FastFallbackRouter,
    dispatch_fast,
)
from merged_agentic_swarm.providers.multi_provider_fabric import (
    MultiProviderFabric,
    _circuit_breaker,
    _circuit_open_until,
    _last_successful_provider,
    _permanently_dead,
)

# Fixed two-route table used by every test router (providers must match the
# keys added in _router_with_keys).
TEST_ROUTES = [
    {"provider": "primary", "model": "m-primary", "url": "https://primary.example/v1/chat/completions"},
    {"provider": "fallback", "model": "m-fallback", "url": "https://fallback.example/v1/chat/completions"},
]


def _reset_shared_fabric_state():
    """Clear module-level fabric circuit/perma-ban state shared with the router."""
    _circuit_breaker.clear()
    _circuit_open_until.clear()
    _permanently_dead.clear()
    _last_successful_provider.clear()


def _anthropic_response(model: str = "claude-3-7-sonnet", text: str = "hello from api") -> dict:
    return {
        "id": "msg_1",
        "type": "message",
        "role": "assistant",
        "model": model,
        "content": [{"type": "text", "text": text}],
        "stop_reason": "end_turn",
        "stop_sequence": None,
        "usage": {"input_tokens": 1, "output_tokens": 1, "total_tokens": 2},
    }


def _mock_response(payload: dict, status_code: int = 200) -> MagicMock:
    mock = MagicMock()
    mock.status_code = status_code
    mock.text = "{}"
    mock.request = MagicMock()
    mock.json.return_value = payload
    return mock


def _url_routed(side_map: dict[str, object]):
    """Build a pool_dispatch side_effect that routes by URL substring.

    ``side_map`` maps a URL substring to either a response mock or a callable.
    Probes for an unlisted URL raise AssertionError, surfacing test drift.
    """

    def _handler(*args, **_kwargs):
        url = args[0]
        for key, action in side_map.items():
            if key in url:
                if isinstance(action, MagicMock):
                    return action  # MagicMock is callable — return, never invoke
                if callable(action):
                    return action(*args, **_kwargs)
                return action
        raise AssertionError(f"no route stub for URL {url}")

    return _handler


def _router_with_keys(isolated_key_pool, config: FastFallbackConfig | None = None) -> FastFallbackRouter:
    """Build a router over the fixed two-route table with keys for both providers."""
    isolated_key_pool.add_key("primary", "pk-1", key_id="primary-1")
    isolated_key_pool.add_key("fallback", "fk-1", key_id="fallback-1")
    cfg = config or FastFallbackConfig(parallel_probes=2, circuit_breaker_threshold=2)
    fabric = MultiProviderFabric(key_pool=isolated_key_pool)
    router = FastFallbackRouter(config=cfg, key_pool=isolated_key_pool, fabric=fabric)
    # Shadow the class method so dispatch uses the deterministic test table.
    router.fabric._build_route_list = lambda model_alias: list(TEST_ROUTES)
    return router


class TestParallelProbe:
    def setup_method(self):
        _reset_shared_fabric_state()

    @patch("merged_agentic_swarm.fast_fallback.pool_dispatch")
    def test_first_success_wins(self, mock_dispatch, isolated_key_pool):
        """Both wave probes fire concurrently; the first 2xx is returned."""
        router = _router_with_keys(isolated_key_pool)

        def _primary(*_args, **_kwargs):
            time.sleep(0.05)
            return _mock_response(_anthropic_response(text="primary"))

        def _fallback(*_args, **_kwargs):
            time.sleep(0.01)
            return _mock_response(_anthropic_response(text="fallback"))

        mock_dispatch.side_effect = _url_routed({"primary": _primary, "fallback": _fallback})
        result = router.dispatch("claude-3-7-sonnet", [{"role": "user", "content": "hi"}])

        assert result["role"] == "assistant"
        assert result["content"][0]["text"] in ("primary", "fallback")
        assert result.get("simulation_fallback") is not True
        # Both probes entered dispatch (the sleeps guarantee neither completed
        # before the other submitted); the faster fallback wins.
        assert mock_dispatch.call_count == 2

    @patch("merged_agentic_swarm.fast_fallback.pool_dispatch")
    def test_primary_failure_falls_to_fallback_in_same_wave(self, mock_dispatch, isolated_key_pool):
        """A failing primary overlaps the fallback's latency instead of serializing it."""
        router = _router_with_keys(isolated_key_pool)

        def _unauthorized(*_args, **_kwargs):
            raise httpx.HTTPStatusError("401 auth", request=MagicMock(), response=_mock_response({}, 401))

        def _delayed_fallback(*_args, **_kwargs):
            # Delay the fallback so the primary's instant 401 error path records
            # the perma-ban before the fallback's success cancels the probe.
            time.sleep(0.1)
            return _mock_response(_anthropic_response(text="fallback ok"))

        mock_dispatch.side_effect = _url_routed({
            "primary": _unauthorized,
            "fallback": _delayed_fallback,
        })

        result = router.dispatch("claude-3-7-sonnet", [{"role": "user", "content": "hi"}])

        assert result["content"][0]["text"] == "fallback ok"
        # Primary got perma-banned via the shared fabric state.
        assert _permanently_dead["primary"] > time.time()

    @patch("merged_agentic_swarm.fast_fallback.pool_dispatch")
    def test_loser_records_no_spurious_failure(self, mock_dispatch, isolated_key_pool):
        """A losing in-flight probe (2xx after another probe won) must not corrupt state."""
        router = _router_with_keys(isolated_key_pool)

        def _slow_primary(*_args, **_kwargs):
            time.sleep(0.15)
            return _mock_response(_anthropic_response(text="primary late"))

        def _fast_fallback(*_args, **_kwargs):
            time.sleep(0.01)
            return _mock_response(_anthropic_response(text="fallback"))

        mock_dispatch.side_effect = _url_routed({"primary": _slow_primary, "fallback": _fast_fallback})
        result = router.dispatch("claude-3-7-sonnet", [{"role": "user", "content": "hi"}])

        assert result["content"][0]["text"] == "fallback"
        # Wait for the slow primary to finish in the background, then confirm the
        # router did not treat its late 2xx as a failure.
        time.sleep(0.25)
        assert router.circuit_status().get("primary", {}).get("consecutive_failures", 0) == 0
        assert _circuit_open_until.get("primary") is None

    @patch("merged_agentic_swarm.fast_fallback.pool_dispatch")
    def test_slow_primary_with_stagger_lets_primary_win(self, mock_dispatch, isolated_key_pool):
        """With probe_stagger_ms, the primary's head-start lets it win even if slower."""
        router = _router_with_keys(
            isolated_key_pool, FastFallbackConfig(parallel_probes=2, probe_stagger_ms=50.0)
        )

        def _primary(*_args, **_kwargs):
            time.sleep(0.03)
            return _mock_response(_anthropic_response(text="primary"))

        def _fallback(*_args, **_kwargs):
            time.sleep(0.01)
            return _mock_response(_anthropic_response(text="fallback"))

        mock_dispatch.side_effect = _url_routed({"primary": _primary, "fallback": _fallback})
        result = router.dispatch("claude-3-7-sonnet", [{"role": "user", "content": "hi"}])
        assert result["content"][0]["text"] == "primary"


class TestCircuitBreaker:
    def setup_method(self):
        _reset_shared_fabric_state()

    @patch("merged_agentic_swarm.fast_fallback.pool_dispatch")
    def test_provider_skipped_after_threshold_failures(self, mock_dispatch, isolated_key_pool):
        """After N consecutive failures the provider is skipped for the cooldown."""
        router = _router_with_keys(isolated_key_pool)  # threshold=2

        def _failing_primary(*_args, **_kwargs):
            raise httpx.ConnectError("refused", request=MagicMock())

        def _ok_fallback(*_args, **_kwargs):
            return _mock_response(_anthropic_response(text="fallback ok"))

        mock_dispatch.side_effect = _url_routed({"primary": _failing_primary, "fallback": _ok_fallback})

        # First two dispatches: primary fails (breaker trips on the second),
        # fallback answers each time.
        for _ in range(2):
            result = router.dispatch("claude-3-7-sonnet", [{"role": "user", "content": "hi"}])
            assert result["content"][0]["text"] == "fallback ok"

        status = router.circuit_status()
        assert status["primary"]["open_until"] > time.time()

        # Third dispatch: primary is skipped, only the fallback is probed.
        mock_dispatch.reset_mock()
        mock_dispatch.side_effect = _url_routed({"primary": _failing_primary, "fallback": _ok_fallback})
        result = router.dispatch("claude-3-7-sonnet", [{"role": "user", "content": "hi"}])
        assert result["content"][0]["text"] == "fallback ok"
        assert mock_dispatch.call_count == 1  # primary was never probed

    @patch("merged_agentic_swarm.fast_fallback.pool_dispatch")
    def test_half_open_after_cooldown_expiry(self, mock_dispatch, isolated_key_pool):
        """Once the cooldown expires the provider is probed again (half-open)."""
        router = _router_with_keys(isolated_key_pool, FastFallbackConfig(circuit_breaker_threshold=1))
        router._circuit_open_until["primary"] = time.time() - 0.01  # expired cooldown

        mock_dispatch.side_effect = _url_routed({
            "primary": _mock_response(_anthropic_response(text="primary back")),
            "fallback": _mock_response(_anthropic_response(text="fallback")),
        })
        result = router.dispatch("claude-3-7-sonnet", [{"role": "user", "content": "hi"}])
        assert result["content"][0]["text"] == "primary back"
        assert router.circuit_status().get("primary", {}).get("open_until", 0.0) == 0.0

    @patch("merged_agentic_swarm.fast_fallback.pool_dispatch")
    def test_honours_shared_fabric_perma_ban(self, mock_dispatch, isolated_key_pool):
        """A fabric perma-banned provider is skipped without being probed."""
        router = _router_with_keys(isolated_key_pool)
        _permanently_dead["primary"] = time.time() + 86400

        mock_dispatch.side_effect = _url_routed({
            "primary": _mock_response(_anthropic_response(text="should not happen")),
            "fallback": _mock_response(_anthropic_response(text="fallback ok")),
        })
        result = router.dispatch("claude-3-7-sonnet", [{"role": "user", "content": "hi"}])
        assert result["content"][0]["text"] == "fallback ok"
        assert mock_dispatch.call_count == 1  # only fallback probed

    @patch("merged_agentic_swarm.fast_fallback.pool_dispatch")
    def test_rate_limit_rotates_key_not_breaker(self, mock_dispatch, isolated_key_pool):
        """429 cools the key down but does not trip the provider breaker."""
        router = _router_with_keys(isolated_key_pool)

        def _throttled(*_args, **_kwargs):
            raise httpx.HTTPStatusError("429", request=MagicMock(), response=_mock_response({}, 429))

        def _delayed_fallback(*_args, **_kwargs):
            # Delay the fallback so the primary's instant 429 error path cools
            # the key down before the fallback's success cancels the probe.
            time.sleep(0.1)
            return _mock_response(_anthropic_response(text="fallback ok"))

        mock_dispatch.side_effect = _url_routed({
            "primary": _throttled,
            "fallback": _delayed_fallback,
        })
        result = router.dispatch("claude-3-7-sonnet", [{"role": "user", "content": "hi"}])
        assert result["content"][0]["text"] == "fallback ok"
        assert _circuit_open_until.get("primary") is None  # no provider breaker trip
        key = isolated_key_pool.keys_by_provider["primary"][0]
        assert key.status.value == "cooldown"


class TestAdaptiveSelection:
    def setup_method(self):
        _reset_shared_fabric_state()

    def test_fast_fallback_promoted(self, isolated_key_pool):
        """A fallback with strong latency history outranks a slow primary."""
        router = _router_with_keys(isolated_key_pool, FastFallbackConfig(min_latency_samples=2))
        router._ewma_latency["fallback"] = 50.0
        router._latency_samples["fallback"] = 5
        router._ewma_latency["primary"] = 5000.0
        router._latency_samples["primary"] = 5

        ordered = router._order_candidates(list(TEST_ROUTES))
        assert ordered[0]["provider"] == "fallback"

    def test_static_order_preserved_without_samples(self, isolated_key_pool):
        """No latency history → static verified-first order is untouched."""
        router = _router_with_keys(isolated_key_pool)
        ordered = router._order_candidates(list(TEST_ROUTES))
        assert [r["provider"] for r in ordered] == ["primary", "fallback"]

    def test_skipped_provider_removed_from_order(self, isolated_key_pool):
        """A perma-banned provider does not appear in the candidate list."""
        router = _router_with_keys(isolated_key_pool)
        _permanently_dead["primary"] = time.time() + 86400
        ordered = router._order_candidates(list(TEST_ROUTES))
        assert [r["provider"] for r in ordered] == ["fallback"]


class TestDispatchBehavior:
    def setup_method(self):
        _reset_shared_fabric_state()

    @patch("merged_agentic_swarm.fast_fallback.pool_dispatch")
    def test_simulation_fallback_when_all_blocked(self, mock_dispatch, isolated_key_pool):
        """Every provider skipped → simulation fallback, no provider calls."""
        router = _router_with_keys(isolated_key_pool)
        _permanently_dead["primary"] = time.time() + 86400
        _permanently_dead["fallback"] = time.time() + 86400

        result = router.dispatch("claude-3-7-sonnet", [{"role": "user", "content": "hi"}])
        assert result["simulation_fallback"] is True
        assert "[SIMULATION" in result["content"][0]["text"]
        assert mock_dispatch.call_count == 0

    @patch("merged_agentic_swarm.fast_fallback.pool_dispatch")
    def test_empty_conversation_returns_error(self, mock_dispatch, isolated_key_pool):
        """Malformed empty request short-circuits without any provider call."""
        router = _router_with_keys(isolated_key_pool)
        result = router.dispatch("claude-3-7-sonnet", [])
        assert result["error"] == "empty_conversation"
        assert mock_dispatch.call_count == 0

    @patch("merged_agentic_swarm.fast_fallback.pool_dispatch")
    def test_enabled_false_delegates_to_fabric(self, mock_dispatch, isolated_key_pool):
        """enabled=False routes through the sequential fabric cascade."""
        fabric = MultiProviderFabric(key_pool=isolated_key_pool)
        router = FastFallbackRouter(
            config=FastFallbackConfig(enabled=False),
            key_pool=isolated_key_pool,
            fabric=fabric,
        )
        # The fabric calls its own module-level pool_dispatch import.
        with patch("merged_agentic_swarm.providers.multi_provider_fabric.pool_dispatch", mock_dispatch):
            mock_dispatch.return_value = _mock_response(_anthropic_response(text="via fabric"))
            result = router.dispatch("claude-3-7-sonnet", [{"role": "user", "content": "hi"}])
        assert result["content"][0]["text"] == "via fabric"

    @patch("merged_agentic_swarm.fast_fallback.pool_dispatch")
    def test_non_dict_2xx_body_cascades(self, mock_dispatch, isolated_key_pool):
        """A 2xx with a non-dict body must be treated as failure, not crash."""
        router = _router_with_keys(isolated_key_pool)
        bad = MagicMock()
        bad.status_code = 200
        bad.text = "[]"
        bad.request = MagicMock()
        bad.json.return_value = ["not", "a", "dict"]
        mock_dispatch.side_effect = _url_routed({
            "primary": bad,
            "fallback": _mock_response(_anthropic_response(text="fallback")),
        })

        result = router.dispatch("claude-3-7-sonnet", [{"role": "user", "content": "hi"}])
        assert result["content"][0]["text"] == "fallback"

    @patch("merged_agentic_swarm.fast_fallback.pool_dispatch")
    def test_non_json_2xx_body_cascades(self, mock_dispatch, isolated_key_pool):
        """A 2xx with a non-JSON body must be treated as failure, not raise."""
        router = _router_with_keys(isolated_key_pool)
        bad = MagicMock()
        bad.status_code = 200
        bad.text = "<html>not json</html>"
        bad.request = MagicMock()
        bad.json.side_effect = ValueError("No JSON")
        mock_dispatch.side_effect = _url_routed({
            "primary": bad,
            "fallback": _mock_response(_anthropic_response(text="fallback")),
        })

        result = router.dispatch("claude-3-7-sonnet", [{"role": "user", "content": "hi"}])
        assert result["content"][0]["text"] == "fallback"


class TestConfigFromEnv:
    @patch.dict(
        "os.environ",
        {"FAST_FALLBACK_PARALLEL_PROBES": "3", "FAST_FALLBACK_ENABLED": "false"},
        clear=False,
    )
    def test_env_overrides(self):
        cfg = FastFallbackConfig.from_env()
        assert cfg.parallel_probes == 3
        assert cfg.enabled is False

    def test_defaults(self):
        cfg = FastFallbackConfig.from_env()
        assert cfg.parallel_probes == 2
        assert cfg.enabled is True
        assert cfg.circuit_breaker_threshold == 3


class TestDispatchHelper:
    def setup_method(self):
        _reset_shared_fabric_state()

    @patch("merged_agentic_swarm.fast_fallback.pool_dispatch")
    def test_dispatch_fast_uses_default_router(self, mock_dispatch, isolated_key_pool):
        """dispatch_fast reaches the default router and returns an Anthropic-shaped response."""
        isolated_key_pool.add_key("gemini", "gk-1", key_id="gemini-1")  # first real route
        router = FastFallbackRouter(
            config=FastFallbackConfig(enabled=True),
            key_pool=isolated_key_pool,
            fabric=MultiProviderFabric(key_pool=isolated_key_pool),
        )
        mock_dispatch.return_value = _mock_response(_anthropic_response(text="helper"))

        with patch("merged_agentic_swarm.fast_fallback.default_fast_fallback", new=router):
            result = dispatch_fast("claude-3-7-sonnet", [{"role": "user", "content": "hi"}])
        assert result["content"][0]["text"] == "helper"
