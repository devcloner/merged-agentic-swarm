"""
Tests for providers/key_pool.py

Coverage: APIKeyInfo, KeyPoolManager (load_keys, get_key, add_key,
mark_success, mark_rate_limited, get_summary).
"""

import time

import pytest

from merged_agentic_swarm.providers.key_pool import APIKeyInfo, KeyPoolManager, KeyStatus


class TestAPIKeyInfo:
    def test_default_creation(self):
        key = APIKeyInfo(key_id="test-1", provider="gemini", secret_value="sk-abc")
        assert key.status == KeyStatus.ACTIVE
        assert key.cooldown_until == 0.0
        assert key.failure_count == 0
        assert key.total_requests == 0

    def test_repr_does_not_leak_secret(self):
        key = APIKeyInfo(key_id="test-1", provider="gemini", secret_value="super-secret-key")
        r = repr(key)
        assert "super-secret-key" not in r
        assert "active" in r  # status.value is lowercase

    def test_mark_cooldown(self):
        key = APIKeyInfo(key_id="test-1", provider="gemini", secret_value="sk-abc")
        key.status = KeyStatus.COOLDOWN
        key.cooldown_until = time.time() + 60
        assert key.status == KeyStatus.COOLDOWN


class TestKeyPoolManager:
    def test_load_keys_from_env_file(self, temp_env_file):
        pool = KeyPoolManager(env_file_path=temp_env_file)
        # May also have env var keys — ensure env file keys are loaded
        all_providers = list(pool.keys_by_provider.keys())
        assert len(all_providers) > 0

    def test_cloudcli_key_loaded_from_env(self, monkeypatch):
        monkeypatch.setenv("CLOUDCLI_API_KEY", "ck-x")
        pool = KeyPoolManager(env_file_path="/dev/null")
        assert "cloudcli" in pool.keys_by_provider
        assert pool.keys_by_provider["cloudcli"][0].key_id == "cloudcli-main"

    def test_add_key_skips_placeholder(self):
        pool = KeyPoolManager(env_file_path="/dev/null")
        pool.keys_by_provider = {}  # clear env-loaded keys
        pool.add_key("gemini", "Gemini API Key", "g-1")
        assert "gemini" not in pool.keys_by_provider

    def test_add_key_creates_new_provider(self):
        pool = KeyPoolManager(env_file_path="/dev/null")
        pool.keys_by_provider = {}  # clear env-loaded keys
        pool.add_key("test_provider", "sk-real-key", "tp-1")
        assert "test_provider" in pool.keys_by_provider

    def test_add_key_appends_to_existing(self):
        pool = KeyPoolManager(env_file_path="/dev/null")
        pool.keys_by_provider = {}  # clear env-loaded keys
        pool.add_key("gemini", "key-1", "g-1")
        pool.add_key("gemini", "key-2", "g-2")
        gemini_keys = [k for k in pool.keys_by_provider.get("gemini", [])]
        assert len(gemini_keys) == 2

    def test_get_key_no_provider(self):
        pool = KeyPoolManager(env_file_path="/dev/null")
        pool.keys_by_provider = {}
        assert pool.get_key("nonexistent") is None

    def test_get_key_returns_least_used(self):
        pool = KeyPoolManager(env_file_path="/dev/null")
        pool.keys_by_provider = {}
        pool.add_key("test", "key-1", "t-1")
        pool.add_key("test", "key-2", "t-2")
        key = pool.get_key("test")
        assert key is not None
        assert key.total_requests == 1  # just incremented

    def test_get_key_round_robin(self):
        pool = KeyPoolManager(env_file_path="/dev/null")
        pool.keys_by_provider = {}
        pool.add_key("test", "key-1", "t-1")
        pool.add_key("test", "key-2", "t-2")
        k1 = pool.get_key("test")
        k2 = pool.get_key("test")
        assert k1 is not None
        assert k2 is not None
        # Both should have been used once
        total_used = sum(k.total_requests for k in pool.keys_by_provider["test"])
        assert total_used == 2

    def test_get_key_recovers_cooldown(self):
        pool = KeyPoolManager(env_file_path="/dev/null")
        pool.keys_by_provider = {}
        pool.add_key("test", "key-1", "t-1")
        key = pool.keys_by_provider["test"][0]
        key.status = KeyStatus.COOLDOWN
        key.cooldown_until = time.time() - 1  # expired cooldown
        result = pool.get_key("test")
        assert result is not None
        assert result.status == KeyStatus.ACTIVE

    def test_get_key_all_cooldown_returns_none(self):
        """When every key is still cooling down, get_key returns None so the
        fabric cascade advances instead of force-recovering a throttled key."""
        pool = KeyPoolManager(env_file_path="/dev/null")
        pool.keys_by_provider = {}
        pool.add_key("test", "key-1", "t-1")
        key = pool.keys_by_provider["test"][0]
        key.status = KeyStatus.COOLDOWN
        key.cooldown_until = time.time() + 300  # still cooling down
        result = pool.get_key("test")
        assert result is None
        # The throttled key must NOT have been reactivated
        assert key.status == KeyStatus.COOLDOWN

    def test_get_key_all_cooldown_multi_key_returns_none(self):
        """Even with many keys, none may be reused while every one is cooling down."""
        pool = KeyPoolManager(env_file_path="/dev/null")
        pool.keys_by_provider = {}
        pool.add_key("test", "key-1", "t-1")
        pool.add_key("test", "key-2", "t-2")
        for key in pool.keys_by_provider["test"]:
            key.status = KeyStatus.COOLDOWN
            key.cooldown_until = time.time() + 300
        assert pool.get_key("test") is None

    def test_get_key_returns_active_key_when_one_in_cooldown(self):
        """A key still cooling down must not be picked while another is active."""
        pool = KeyPoolManager(env_file_path="/dev/null")
        pool.keys_by_provider = {}
        pool.add_key("test", "key-1", "t-1")
        pool.add_key("test", "key-2", "t-2")
        pool.keys_by_provider["test"][0].status = KeyStatus.COOLDOWN
        pool.keys_by_provider["test"][0].cooldown_until = time.time() + 300
        result = pool.get_key("test")
        assert result is not None
        assert result.key_id == "t-2"  # the active key, not the throttled one

    def test_mark_success(self):
        pool = KeyPoolManager(env_file_path="/dev/null")
        pool.keys_by_provider = {}
        pool.add_key("test", "key-1", "t-1")
        key = pool.keys_by_provider["test"][0]
        key.failure_count = 2
        pool.mark_success(key, latency_ms=100.0, tokens=50)
        assert key.failure_count == 0
        assert key.total_tokens == 50
        assert key.avg_latency_ms == 100.0

    def test_mark_success_smoothed_latency(self):
        pool = KeyPoolManager(env_file_path="/dev/null")
        pool.keys_by_provider = {}
        pool.add_key("test", "key-1", "t-1")
        key = pool.keys_by_provider["test"][0]
        key.avg_latency_ms = 200.0
        pool.mark_success(key, latency_ms=100.0)
        # 200 * 0.8 + 100 * 0.2 = 160 + 20 = 180
        assert key.avg_latency_ms == pytest.approx(180.0)

    def test_mark_rate_limited(self):
        pool = KeyPoolManager(env_file_path="/dev/null")
        pool.keys_by_provider = {}
        pool.add_key("test", "key-1", "t-1")
        key = pool.keys_by_provider["test"][0]
        pool.mark_rate_limited(key, cooldown_seconds=60.0)
        assert key.status == KeyStatus.COOLDOWN
        assert key.cooldown_until > time.time()
        assert key.failure_count == 1

    def test_get_summary(self):
        pool = KeyPoolManager(env_file_path="/dev/null")
        pool.keys_by_provider = {}
        pool.add_key("gemini", "key-1", "g-1")
        pool.add_key("gemini", "key-2", "g-2")
        pool.add_key("groq", "key-3", "gr-1")
        summary = pool.get_summary()
        assert "gemini" in summary
        assert "groq" in summary
        assert summary["gemini"]["total_keys"] == 2
        assert summary["groq"]["total_keys"] == 1

    def test_get_summary_new_metric_fields(self):
        """#42: summary reports exhausted count, next cooldown expiry, avg latency."""
        pool = KeyPoolManager(env_file_path="/dev/null")
        pool.keys_by_provider = {}
        pool.add_key("gemini", "key-1", "g-1")
        pool.add_key("gemini", "key-2", "g-2")
        pool.add_key("gemini", "key-3", "g-3")
        keys = pool.keys_by_provider["gemini"]
        keys[0].status = KeyStatus.EXHAUSTED
        keys[1].status = KeyStatus.COOLDOWN
        keys[1].cooldown_until = time.time() + 60
        keys[2].avg_latency_ms = 120.5
        summary = pool.get_summary()["gemini"]
        assert summary["exhausted_keys"] == 1
        assert summary["cooldown_keys"] == 1
        assert summary["next_cooldown_until"] == keys[1].cooldown_until
        assert summary["avg_latency_ms"] == 120.5
        assert summary["active_keys"] == 1  # only key-3 is active

    def test_get_summary_no_cooldown_defaults(self):
        pool = KeyPoolManager(env_file_path="/dev/null")
        pool.keys_by_provider = {}
        pool.add_key("gemini", "key-1", "g-1")
        summary = pool.get_summary()["gemini"]
        assert summary["next_cooldown_until"] is None
        assert summary["exhausted_keys"] == 0
        assert summary["avg_latency_ms"] == 0.0

    def test_get_key_missing(self):
        """Getting a key from a provider that doesn't exist should not raise."""
        pool = KeyPoolManager(env_file_path="/dev/null")
        pool.keys_by_provider = {}
        assert pool.get_key("nonexistent") is None


class TestKeyPoolReload:
    def test_reload_preserves_stats_for_existing_key(self, temp_env_file):
        pool = KeyPoolManager(env_file_path=temp_env_file)
        # gemini-1 is the env-file GEMINI_API_KEY (sources are read in order).
        key = pool.keys_by_provider["gemini"][0]
        assert key.key_id == "gemini-1"
        pool.mark_rate_limited(key, cooldown_seconds=60.0)
        pool.reload()
        reloaded = pool.keys_by_provider["gemini"][0]
        assert reloaded.key_id == "gemini-1"
        assert reloaded.status == KeyStatus.COOLDOWN
        assert reloaded.failure_count == 1
        assert reloaded.cooldown_until > time.time()
        assert reloaded is key  # same instance: cooldown/usage survived

    def test_reload_swaps_rotated_secret_preserving_stats(self, temp_env_file):
        pool = KeyPoolManager(env_file_path=temp_env_file)
        key = pool.get_key("gemini")
        assert key is not None
        with open(temp_env_file, "a") as f:
            f.write("GEMINI_API_KEY=rotated-key\n")
        pool.reload()
        reloaded = pool.keys_by_provider["gemini"][0]
        assert reloaded.secret_value == "rotated-key"
        assert reloaded.total_requests >= 1  # usage carried over across rotation

    def test_reload_picks_up_newly_added_source_key(self, temp_env_file):
        pool = KeyPoolManager(env_file_path=temp_env_file)
        assert "mistral" not in pool.keys_by_provider
        with open(temp_env_file, "a") as f:
            f.write("MISTRAL_API_KEY=test-mistral-key\n")
        pool.reload()
        assert pool.keys_by_provider["mistral"][0].key_id == "mistral-main"
        assert pool.keys_by_provider["mistral"][0].secret_value == "test-mistral-key"

    def test_reload_drops_keys_not_present_in_sources(self, temp_env_file):
        pool = KeyPoolManager(env_file_path=temp_env_file)
        pool.add_key("manual", "sk-manual", "manual-1")
        assert "manual" in pool.keys_by_provider
        pool.reload()
        assert "manual" not in pool.keys_by_provider

    def test_reload_replaces_pool_without_duplicating(self, temp_env_file):
        pool = KeyPoolManager(env_file_path=temp_env_file)
        pool.reload()
        pool.reload()
        gemini_ids = [k.key_id for k in pool.keys_by_provider["gemini"]]
        assert sum(1 for kid in gemini_ids if kid == "gemini-1") == 1
