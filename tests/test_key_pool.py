"""
Tests for providers/key_pool.py

Coverage: APIKeyInfo, KeyPoolManager (load_keys, get_key, add_key,
mark_success, mark_rate_limited, get_summary).
"""
import os
import time
import json
import pytest
from providers.key_pool import KeyPoolManager, APIKeyInfo, KeyStatus


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

    def test_get_key_returns_forced_recovered(self):
        pool = KeyPoolManager(env_file_path="/dev/null")
        pool.keys_by_provider = {}
        pool.add_key("test", "key-1", "t-1")
        key = pool.keys_by_provider["test"][0]
        key.status = KeyStatus.COOLDOWN
        key.cooldown_until = time.time() + 300  # still cooling down
        result = pool.get_key("test")
        # Should force-recover the cooldown key since no active key
        assert result is not None

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

    def test_get_key_missing(self):
        """Getting a key from a provider that doesn't exist should not raise."""
        pool = KeyPoolManager(env_file_path="/dev/null")
        pool.keys_by_provider = {}
        assert pool.get_key("nonexistent") is None
