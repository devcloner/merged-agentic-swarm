"""
Tests for services/swarm_profiles.py

Coverage: load_profiles reads the JSON and caches it, fallback when the file is
missing, resolve_profile known + unknown, list_profiles, model alias resolution
per tier (deep -> gemini-batch, fast -> fast-flash), explicit model_alias
precedence, and validation of the on-disk swarm-profiles.json.
"""

import json
from pathlib import Path
from unittest.mock import patch

import pytest

import merged_agentic_swarm.services.swarm_profiles as sp

# Tier aliases mirror services/model_routing.py DEFAULT_TIER_ALIASES.
TIER_ALIASES = {"deep": "gemini-batch", "main": "gemini-batch-lite", "fast": "fast-flash"}


@pytest.fixture(autouse=True)
def _fresh_cache():
    """Each test starts (and ends) with an empty profile cache."""
    sp._profiles_cache = None
    yield
    sp._profiles_cache = None


class TestLoadProfiles:
    def test_load_profiles_reads_json(self):
        profiles = sp.load_profiles()
        assert "build" in profiles
        assert "learning" in profiles
        assert profiles["build"]["waves"] == [4, 8, 16, 24, 40]
        assert profiles["build"]["default_tier"] == "deep"
        assert profiles["build"]["gates"] is True

    def test_load_profiles_caches_between_calls(self):
        first = sp.load_profiles()
        second = sp.load_profiles()
        assert first is second

    def test_fallback_when_json_missing(self):
        with patch.object(sp, "_PROFILES_PATH", Path("/nonexistent/swarm-profiles.json")):
            profiles = sp.load_profiles()
        assert "build" in profiles
        assert "learning" in profiles
        assert profiles["build"]["waves"] == [4, 8, 16, 24, 40]

    def test_load_profiles_recovers_after_missing_file(self):
        """A fallback load must not poison later loads once the real file returns."""
        with patch.object(sp, "_PROFILES_PATH", Path("/nonexistent/swarm-profiles.json")):
            sp.load_profiles()
        sp._profiles_cache = None
        profiles = sp.load_profiles()
        assert profiles["learning"]["waves"] == []


class TestResolveProfile:
    def test_resolve_known_profile(self):
        profile = sp.resolve_profile("build")
        assert profile["waves"] == [4, 8, 16, 24, 40]

    def test_resolve_unknown_raises_key_error(self):
        with pytest.raises(KeyError):
            sp.resolve_profile("no-such-profile")


class TestListProfiles:
    def test_list_profiles_names_and_descriptions(self):
        entries = sp.list_profiles()
        by_name = {e["name"]: e for e in entries}
        assert {"build", "review", "ultra", "patch", "learning"} <= set(by_name)
        assert "cold-path" in by_name["learning"]["description"].lower()
        assert "build" in by_name["build"]["description"].lower()

    def test_list_profiles_sorted(self):
        names = [e["name"] for e in sp.list_profiles()]
        assert names == sorted(names)


class TestResolveModelAliasForProfile:
    def test_deep_tier_resolves_gemini_batch(self):
        assert sp.resolve_model_alias_for_profile("build") == "gemini-batch"
        assert sp.resolve_model_alias_for_profile("ultra") == "gemini-batch"

    def test_fast_tier_resolves_fast_flash(self):
        assert sp.resolve_model_alias_for_profile("review") == "fast-flash"
        assert sp.resolve_model_alias_for_profile("patch") == "fast-flash"

    def test_explicit_model_alias_takes_precedence(self):
        with patch.object(
            sp,
            "resolve_profile",
            return_value={"default_tier": "fast", "model_alias": "claude-3-7-sonnet"},
        ):
            assert sp.resolve_model_alias_for_profile("anything") == "claude-3-7-sonnet"

    def test_unknown_profile_propagates_key_error(self):
        with pytest.raises(KeyError):
            sp.resolve_model_alias_for_profile("no-such-profile")


class TestProfilesFile:
    def test_json_file_is_valid_and_shaped(self):
        """The on-disk profiles file must parse and carry the documented fields."""
        data = json.loads(Path(sp._PROFILES_PATH).read_text(encoding="utf-8"))
        assert {"build", "review", "ultra", "patch", "learning"} <= set(data)
        for name, profile in data.items():
            assert isinstance(profile["description"], str) and profile["description"]
            assert isinstance(profile["waves"], list)
            assert all(isinstance(w, int) for w in profile["waves"])
            assert profile["default_tier"] in ("deep", "main", "fast")
            assert isinstance(profile["gates"], bool)
            assert isinstance(profile["worker_roles"], list)
            assert "model_alias" not in profile or isinstance(profile["model_alias"], str)
            # Every tier alias must resolve through model_routing.
            assert TIER_ALIASES[profile["default_tier"]] == sp.resolve_model_alias_for_profile(name)

    def test_learning_profile_has_no_worker_waves(self):
        assert sp.resolve_profile("learning")["waves"] == []
        assert sp.resolve_profile("learning")["gates"] is False
