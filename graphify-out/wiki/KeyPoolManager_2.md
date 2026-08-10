# KeyPoolManager

> God node · 61 connections · `src/merged_agentic_swarm/providers/key_pool.py`

**Community:** [KeyPoolManager](KeyPoolManager.md)

## Connections by Relation

### calls
- ._setup() `INFERRED`
- .test_consecutive_429s_trip_circuit_breaker() `INFERRED`
- isolated_key_pool() `INFERRED`
- .test_get_key_all_cooldown_multi_key_returns_none() `EXTRACTED`
- .test_get_key_all_cooldown_returns_none() `EXTRACTED`
- .test_get_key_missing() `EXTRACTED`
- .test_get_key_returns_active_key_when_one_in_cooldown() `EXTRACTED`
- .test_get_summary_new_metric_fields() `EXTRACTED`
- .test_add_key_appends_to_existing() `EXTRACTED`
- .test_add_key_creates_new_provider() `EXTRACTED`
- .test_add_key_skips_placeholder() `EXTRACTED`
- .test_cloudcli_key_loaded_from_env() `EXTRACTED`
- .test_get_key_no_provider() `EXTRACTED`
- .test_get_key_recovers_cooldown() `EXTRACTED`
- .test_get_key_returns_least_used() `EXTRACTED`
- .test_get_key_round_robin() `EXTRACTED`
- .test_get_summary() `EXTRACTED`
- .test_get_summary_no_cooldown_defaults() `EXTRACTED`
- .test_load_keys_from_env_file() `EXTRACTED`
- .test_mark_rate_limited() `EXTRACTED`

### contains
- key_pool.py `EXTRACTED`

### imports
- providers/__init__.py `EXTRACTED`

### method
- .load_keys() `EXTRACTED`
- ._collect_keys_from_sources() `EXTRACTED`
- .get_key() `EXTRACTED`
- ._get_key_unlocked() `EXTRACTED`
- .reload() `EXTRACTED`
- .add_key() `EXTRACTED`
- .get_summary() `EXTRACTED`
- ._get_summary_unlocked() `EXTRACTED`
- .__init__() `EXTRACTED`
- .mark_rate_limited() `EXTRACTED`
- .mark_success() `EXTRACTED`

### uses
- TestKeyPoolManager `INFERRED`
- [TestFormatConversion](TestFormatConversion.md) `INFERRED`
- [TestDispatchRequest](TestDispatchRequest.md) `INFERRED`
- TestCmdSwarm `INFERRED`
- TestCmdStatus `INFERRED`
- TestCmdRun `INFERRED`
- TestKeyPoolReload `INFERRED`
- TestCircuitBreaker `INFERRED`
- [TestBanPersistence](TestBanPersistence.md) `INFERRED`
- TestAPIKeyInfo `INFERRED`
- [TestMalformedOverlayRoutes](TestMalformedOverlayRoutes.md) `INFERRED`
- TestRouteBuilding `INFERRED`
- [TestCmdProviders](TestCmdProviders.md) `INFERRED`
- TestCmdReport `INFERRED`
- [TestLitellmPresenceInRoutes](TestLitellmPresenceInRoutes.md) `INFERRED`
- [TestCLIStringFunctions](TestCLIStringFunctions.md) `INFERRED`
- TestCmdConfig `INFERRED`
- TestMain `INFERRED`
- TestFabricRouteOverlay `INFERRED`
- TestCmdPromote `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*