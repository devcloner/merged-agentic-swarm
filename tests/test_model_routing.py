"""
Tests for services/model_routing.py

Coverage: role -> litellm alias resolution, unknown role -> default, missing
registry file -> code-side fallback, fabric route litellm lookup, and validation
that the on-disk PROVIDER_REGISTRY.json still parses with a role_routing section.
"""

import json
from pathlib import Path
from unittest.mock import patch

import merged_agentic_swarm.services.model_routing as mr


class TestResolveLitellmModelForRole:
    def setup_method(self):
        mr._registry_cache = None

    def test_deep_role_maps_to_gemini_batch(self):
        assert mr.resolve_litellm_model_for_role("deep") == "gemini-batch"

    def test_main_role_maps_to_gemini_batch_lite(self):
        assert mr.resolve_litellm_model_for_role("main") == "gemini-batch-lite"

    def test_fast_role_maps_to_fast_flash(self):
        assert mr.resolve_litellm_model_for_role("fast") == "fast-flash"

    def test_registered_role_maps_via_policy_tier(self):
        # cc-orchestrator is registered under the deep tier.
        assert mr.resolve_litellm_model_for_role("cc-orchestrator") == "gemini-batch"
        # domain-module-worker is registered under the main tier.
        assert mr.resolve_litellm_model_for_role("domain-module-worker") == "gemini-batch-lite"
        # budget-route-auditor is registered under the fast tier.
        assert mr.resolve_litellm_model_for_role("budget-route-auditor") == "fast-flash"

    def test_unknown_role_falls_back_to_smart_auto(self):
        assert mr.resolve_litellm_model_for_role("no-such-role") == "smart-auto"

    def test_worker_role_maps_via_code_fallback(self):
        # WorkerRole enum values (models/agent_models.py) resolve per-role instead
        # of sharing one hardcoded alias.
        assert mr.resolve_litellm_model_for_role("core_engineer") == "gemini-batch-lite"
        assert mr.resolve_litellm_model_for_role("security_verifier") == "fast-flash"
        assert mr.resolve_litellm_model_for_role("master_architect") == "gemini-batch"
        assert mr.resolve_litellm_model_for_role("hot_micro_specialist") == "fast-flash"
        assert mr.resolve_litellm_model_for_role("unit_tester") == "gemini-batch-lite"

    def test_empty_string_role_falls_back_to_smart_auto(self):
        assert mr.resolve_litellm_model_for_role("") == "smart-auto"

    def test_missing_registry_file_uses_code_fallback(self):
        with patch.object(mr, "_REGISTRY_PATH", Path("/nonexistent/PROVIDER_REGISTRY.json")):
            mr._registry_cache = None
            assert mr.resolve_litellm_model_for_role("deep") == "gemini-batch"
            assert mr.resolve_litellm_model_for_role("main") == "gemini-batch-lite"
            assert mr.resolve_litellm_model_for_role("fast") == "fast-flash"
            assert mr.resolve_litellm_model_for_role("cc-orchestrator") == "gemini-batch"
            assert mr.resolve_litellm_model_for_role("unknown") == "smart-auto"

    def test_registry_without_role_routing_uses_code_fallback(self, tmp_path):
        reg = tmp_path / "PROVIDER_REGISTRY.json"
        reg.write_text(json.dumps({"version": 1, "tiers": {}, "backends": {}}), encoding="utf-8")
        with patch.object(mr, "_REGISTRY_PATH", reg):
            mr._registry_cache = None
            assert mr.resolve_litellm_model_for_role("deep") == "gemini-batch"
            assert mr.resolve_litellm_model_for_role("fast") == "fast-flash"
            assert mr.resolve_litellm_model_for_role("unknown") == "smart-auto"

    def test_registry_role_routing_takes_precedence_over_code_fallback(self, tmp_path):
        reg = tmp_path / "PROVIDER_REGISTRY.json"
        reg.write_text(
            json.dumps({"role_routing": {"tiers": {"deep": "gemini-batch", "fast": "custom-fast-alias"}}}),
            encoding="utf-8",
        )
        with patch.object(mr, "_REGISTRY_PATH", reg):
            mr._registry_cache = None
            assert mr.resolve_litellm_model_for_role("deep") == "gemini-batch"
            assert mr.resolve_litellm_model_for_role("fast") == "custom-fast-alias"
            # Main tier not present in the file -> falls back to code-side mapping.
            assert mr.resolve_litellm_model_for_role("main") == "gemini-batch-lite"


class TestLitellmModelForFabricRoute:
    def test_returns_first_litellm_model(self):
        assert mr.litellm_model_for_fabric_route("claude-3-opus") == "gemini-2.5-flash"
        assert mr.litellm_model_for_fabric_route("claude-3-5-haiku") == "gemini-2.5-flash-lite"

    def test_unknown_route_returns_none(self):
        assert mr.litellm_model_for_fabric_route("no-such-alias") is None


class TestReloadRegistry:
    def setup_method(self):
        mr._registry_cache = None

    def test_reload_registry_reloads_after_change(self, tmp_path):
        """reload_registry() clears the cache so an updated registry file is seen."""
        reg = tmp_path / "PROVIDER_REGISTRY.json"
        reg.write_text(json.dumps({"role_routing": {"tiers": {"deep": "gemini-batch"}}}), encoding="utf-8")
        with patch.object(mr, "_REGISTRY_PATH", reg):
            mr._registry_cache = None
            assert mr.resolve_litellm_model_for_role("deep") == "gemini-batch"
            # Rewrite the file on disk, then reload — stale cache must not hide it.
            reg.write_text(json.dumps({"role_routing": {"tiers": {"deep": "custom-deep"}}}), encoding="utf-8")
            mr.reload_registry()
            assert mr.resolve_litellm_model_for_role("deep") == "custom-deep"

    def test_reload_registry_missing_file_uses_code_fallback(self, tmp_path):
        reg = tmp_path / "PROVIDER_REGISTRY.json"  # does not exist
        with patch.object(mr, "_REGISTRY_PATH", reg):
            mr.reload_registry()
            assert mr.resolve_litellm_model_for_role("deep") == "gemini-batch"

    def test_reload_registry_returns_loaded_registry(self, tmp_path):
        reg = tmp_path / "PROVIDER_REGISTRY.json"
        reg.write_text(json.dumps({"role_routing": {"tiers": {"deep": "gemini-batch"}}}), encoding="utf-8")
        with patch.object(mr, "_REGISTRY_PATH", reg):
            assert mr.reload_registry()["role_routing"]["tiers"]["deep"] == "gemini-batch"


class TestRegistryFile:
    def setup_method(self):
        mr._registry_cache = None

    def test_registry_json_is_valid_and_has_role_routing(self):
        """The on-disk registry must parse and carry a consistent role_routing section."""
        reg = json.loads(Path(mr._REGISTRY_PATH).read_text(encoding="utf-8"))
        role_routing = reg["role_routing"]
        assert role_routing["provider"] == "litellm"
        assert role_routing["default"] == "smart-auto"
        assert role_routing["tiers"]["deep"] == "gemini-batch"
        assert role_routing["tiers"]["main"] == "gemini-batch-lite"
        assert role_routing["tiers"]["fast"] == "fast-flash"
        # Every default_tier_by_role role has an explicit alias mirroring its tier.
        tier_by_role = reg["policy"]["default_tier_by_role"]
        assert set(role_routing["roles"]) == set(tier_by_role)
        for role, tier in tier_by_role.items():
            assert role_routing["roles"][role] == role_routing["tiers"][tier]

    def test_resolver_agrees_with_registry_file(self):
        """Live resolution should match the tier aliases in the registry file."""
        reg = json.loads(Path(mr._REGISTRY_PATH).read_text(encoding="utf-8"))
        tiers = reg["role_routing"]["tiers"]
        for role, alias in tiers.items():
            assert mr.resolve_litellm_model_for_role(role) == alias
