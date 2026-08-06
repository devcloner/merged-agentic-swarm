"""
Swarm Profile Service
Named, slash-command-style presets for pushing a large multi-agent swarm of a
chosen type. Profiles live in docs/agentic/swarm-profiles.json; a small code-side
dict is used as a fallback so resolution keeps working when the file is absent.
"""

import json
import logging
from pathlib import Path

from merged_agentic_swarm.services.model_routing import resolve_litellm_model_for_role

logger = logging.getLogger("swarm_profiles")

_REPO_ROOT = Path(__file__).resolve().parents[3]
_PROFILES_PATH = _REPO_ROOT / "docs" / "agentic" / "swarm-profiles.json"

# Code-side fallback — mirrors the on-disk profiles so resolution works offline.
FALLBACK_PROFILES: dict[str, dict] = {
    "build": {
        "description": "Full multi-wave build across the whole codebase",
        "waves": [4, 8, 16, 24, 40],
        "default_tier": "deep",
        "gates": True,
        "worker_roles": ["master_architect", "codebase_mapper", "core_engineer", "unit_tester"],
    },
    "review": {
        "description": "Code review pass with security and refactor verifiers",
        "waves": [4, 8],
        "default_tier": "fast",
        "gates": True,
        "worker_roles": ["security_verifier", "refactor_specialist", "unit_tester"],
    },
    "ultra": {
        "description": "Maximum concurrency using every tier and worker role",
        "waves": [8, 16, 24, 40],
        "default_tier": "deep",
        "gates": True,
        "worker_roles": ["master_architect", "core_engineer", "security_verifier", "hot_micro_specialist"],
    },
    "patch": {
        "description": "Quick targeted patch with a minimal focused swarm",
        "waves": [4],
        "default_tier": "fast",
        "gates": False,
        "worker_roles": ["core_engineer", "unit_tester"],
    },
    "learning": {
        "description": "Cold-path promotion and registry compact only (no worker waves)",
        "waves": [],
        "default_tier": "deep",
        "gates": False,
        "worker_roles": ["cold_durable"],
    },
}

# Cache of the parsed profiles so repeated resolution doesn't re-read disk.
_profiles_cache: dict[str, dict] | None = None


def load_profiles() -> dict[str, dict]:
    """Load all swarm profiles (cached); fall back to the code-side dict when missing."""
    global _profiles_cache
    if _profiles_cache is not None:
        return _profiles_cache
    try:
        with open(_PROFILES_PATH, encoding="utf-8") as f:
            profiles = json.load(f)
        if isinstance(profiles, dict) and profiles:
            _profiles_cache = profiles
            return _profiles_cache
    except OSError, ValueError:
        logger.warning("swarm-profiles.json missing/unreadable; using code-side fallback profiles.")
    _profiles_cache = dict(FALLBACK_PROFILES)
    return _profiles_cache


def resolve_profile(name: str) -> dict:
    """Return the resolved profile dict for a name; raise KeyError for unknown names."""
    profiles = load_profiles()
    if name not in profiles:
        raise KeyError(f"Unknown swarm profile: {name!r}. Known profiles: {', '.join(sorted(profiles))}")
    return profiles[name]


def list_profiles() -> list[dict]:
    """Return [{name, description}] entries for every known profile, name-sorted."""
    profiles = load_profiles()
    return [{"name": name, "description": profile.get("description", "")} for name, profile in sorted(profiles.items())]


def resolve_model_alias_for_profile(name: str) -> str | None:
    """Return the profile's model alias, or resolve via model_routing when absent.

    When a profile carries no explicit ``model_alias``, the profile's
    ``default_tier`` (deep / main / fast) is resolved through
    ``resolve_litellm_model_for_role`` to a litellm virtual Gemini alias.
    """
    profile = resolve_profile(name)
    alias = profile.get("model_alias")
    if isinstance(alias, str) and alias:
        return alias
    return resolve_litellm_model_for_role(profile.get("default_tier", "deep"))
