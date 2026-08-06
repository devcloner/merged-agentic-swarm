"""
Model Role Routing
Resolves a worker role (deep / main / fast tier, or a registered role name) to a
litellm virtual Gemini alias exposed by the local gateway on 127.0.0.1:4000.
"""

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger("model_routing")

_REPO_ROOT = Path(__file__).resolve().parents[3]
_REGISTRY_PATH = _REPO_ROOT / "docs" / "agentic" / "providers" / "PROVIDER_REGISTRY.json"

# Code-side fallback mapping — used when PROVIDER_REGISTRY.json is missing or
# unreadable so role routing keeps working offline.
DEFAULT_TIER_ALIASES: dict[str, str] = {
    "deep": "gemini-batch",
    "main": "gemini-batch-lite",
    "fast": "fast-flash",
}
DEFAULT_TIER_BY_ROLE: dict[str, str] = {
    "cc-orchestrator": "deep",
    "tm-operator": "main",
    "spawn-gate": "main",
    "prd-decomposer": "deep",
    "spec-gap-detector": "main",
    "budget-route-auditor": "fast",
    "domain-module-worker": "main",
    "type-hardening-worker": "fast",
    "test-engineer": "main",
    "sec-a11y-auditor": "deep",
    "codebase-ast-mapper": "main",
    # WorkerRole enum values (models/agent_models.py) — so swarm workers dispatch
    # per-role instead of every worker sharing one hardcoded alias.
    "master_architect": "deep",
    "codebase_mapper": "main",
    "spec_gap_closer": "main",
    "core_engineer": "main",
    "refactor_specialist": "main",
    "unit_tester": "main",
    "security_verifier": "fast",
    "hot_micro_specialist": "fast",
    "cold_durable": "main",
}
DEFAULT_LITELLM_ALIAS = "smart-auto"

# Cache of the parsed registry so repeated routing calls don't re-read disk.
_registry_cache: dict[str, Any] | None = None


def _load_registry() -> dict[str, Any]:
    """Load the provider registry (cached); return {} when missing/unreadable."""
    global _registry_cache
    if _registry_cache is not None:
        return _registry_cache
    try:
        with open(_REGISTRY_PATH, encoding="utf-8") as f:
            registry = json.load(f)
        if isinstance(registry, dict):
            _registry_cache = registry
            return _registry_cache
    except OSError, ValueError:
        logger.warning("Provider registry missing/unreadable; using code-side role routing fallback.")
    return {}


def reload_registry() -> dict[str, Any]:
    """Clear the cached registry and reload it from disk.

    Called after the provider registry file is rewritten (e.g. the web UI models
    PUT) so subsequent role resolutions observe the updated aliases without a
    process restart.
    """
    global _registry_cache
    _registry_cache = None
    return _load_registry()


def resolve_litellm_model_for_role(role: str) -> str:
    """Return the litellm virtual Gemini alias for a worker role.

    Resolution order:
      1. role_routing.roles[role]  — explicit per-role override
      2. role_routing.tiers[role]  — direct tier name (deep / main / fast)
      3. policy.default_tier_by_role[role] -> tier alias (drift-tolerant)
      4. code-side fallback (registry absent)
      5. DEFAULT_LITELLM_ALIAS ("smart-auto") for unknown roles
    """
    registry = _load_registry()
    role_routing = registry.get("role_routing")
    tiers: dict[str, Any] = {}
    if isinstance(role_routing, dict):
        tiers = role_routing.get("tiers") if isinstance(role_routing.get("tiers"), dict) else {}
        for key in ("roles", "tiers"):
            table = role_routing.get(key)
            if isinstance(table, dict):
                alias = table.get(role)
                if isinstance(alias, str) and alias:
                    return alias

    policy = registry.get("policy")
    if isinstance(policy, dict):
        tier_by_role = policy.get("default_tier_by_role")
        if isinstance(tier_by_role, dict):
            tier = tier_by_role.get(role)
            if isinstance(tier, str):
                alias = tiers.get(tier)
                if isinstance(alias, str) and alias:
                    return alias

    if role in DEFAULT_TIER_ALIASES:
        return DEFAULT_TIER_ALIASES[role]
    tier = DEFAULT_TIER_BY_ROLE.get(role)
    if tier:
        return DEFAULT_TIER_ALIASES.get(tier, DEFAULT_LITELLM_ALIAS)
    return DEFAULT_LITELLM_ALIAS


def litellm_model_for_fabric_route(model_alias: str) -> str | None:
    """Return the first litellm model in the fabric route list for a model alias."""
    from merged_agentic_swarm.providers.multi_provider_fabric import MODEL_FABRIC_ROUTES

    for route in MODEL_FABRIC_ROUTES.get(model_alias, []):
        if route.get("provider") == "litellm":
            return route.get("model")
    return None
