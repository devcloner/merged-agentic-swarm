# litellm

> 24 nodes · cohesion 0.09

## Key Concepts

- **test_multi_provider_fabric.py** (11 connections) — `tests/test_multi_provider_fabric.py`
- **TestBanPersistence** (8 connections) — `tests/test_multi_provider_fabric.py`
- **TestMalformedOverlayRoutes** (7 connections) — `tests/test_multi_provider_fabric.py`
- **TestLitellmPresenceInRoutes** (6 connections) — `tests/test_multi_provider_fabric.py`
- **TestFabricRouteOverlay** (5 connections) — `tests/test_multi_provider_fabric.py`
- **_isolated_bans_path()** (3 connections) — `tests/test_multi_provider_fabric.py`
- **._install()** (3 connections) — `tests/test_multi_provider_fabric.py`
- **.test_litellm_alias_routes_lead_with_litellm()** (2 connections) — `tests/test_multi_provider_fabric.py`
- **.test_all_malformed_alias_falls_back_to_code_defaults()** (2 connections) — `tests/test_multi_provider_fabric.py`
- **.test_malformed_routes_filtered_at_load()** (2 connections) — `tests/test_multi_provider_fabric.py`
- **fixture** (1 connections)
- **Tests for providers/multi_provider_fabric.py Coverage:…** (1 connections) — `tests/test_multi_provider_fabric.py`
- **#40: 401 perma-bans persist to disk and are honored across reloads.** (1 connections) — `tests/test_multi_provider_fabric.py`
- **Redirect the persisted-bans path so tests never write into the repo.** (1 connections) — `tests/test_multi_provider_fabric.py`
- **Role routing maps worker roles to litellm aliases, so every fabric tier must…** (1 connections) — `tests/test_multi_provider_fabric.py`
- **Worker-tier aliases route through the litellm gateway FIRST (42-key Gemini…** (1 connections) — `tests/test_multi_provider_fabric.py`
- **Malformed overlay routes are dropped at load, never crashing dispatch (issue…** (1 connections) — `tests/test_multi_provider_fabric.py`
- **.setup_method()** (1 connections) — `tests/test_multi_provider_fabric.py`
- **.test_401_persists_ban_and_reload_restores()** (1 connections) — `tests/test_multi_provider_fabric.py`
- **.test_expired_ban_dropped_on_load()** (1 connections) — `tests/test_multi_provider_fabric.py`
- **.test_non_401_failure_does_not_persist_ban()** (1 connections) — `tests/test_multi_provider_fabric.py`
- **.test_missing_overlay_falls_back_to_code_defaults()** (1 connections) — `tests/test_multi_provider_fabric.py`
- **.test_overlay_overrides_per_alias_and_reload_refreshes()** (1 connections) — `tests/test_multi_provider_fabric.py`
- **.test_each_fabric_alias_has_litellm_route()** (1 connections) — `tests/test_multi_provider_fabric.py`

## Relationships

- [MultiProviderFabric](MultiProviderFabric.md) (6 shared connections)
- [KeyPoolManager](KeyPoolManager.md) (4 shared connections)
- [services/__init__.py](services-__init__.py.md) (2 shared connections)
- [.get_available_worker](get_available_worker.md) (1 shared connections)

## Source Files

- `tests/test_multi_provider_fabric.py`

## Audit Trail

- EXTRACTED: 55 (87%)
- INFERRED: 8 (13%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*