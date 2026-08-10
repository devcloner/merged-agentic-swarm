---
source_file: "src/merged_agentic_swarm/providers/key_pool.py"
type: "code"
community: "KeyPoolManager"
location: "L46"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/KeyPoolManager
---

# KeyPoolManager

## Connections
- [[dot-__init__()_5]] - `method` [EXTRACTED]
- [[dot-_collect_keys_from_sources()]] - `method` [EXTRACTED]
- [[dot-_get_key_unlocked()]] - `method` [EXTRACTED]
- [[dot-_get_summary_unlocked()]] - `method` [EXTRACTED]
- [[dot-_setup()]] - `calls` [INFERRED]
- [[dot-add_key()]] - `method` [EXTRACTED]
- [[dot-get_key()]] - `method` [EXTRACTED]
- [[dot-get_summary()]] - `method` [EXTRACTED]
- [[dot-load_keys()]] - `method` [EXTRACTED]
- [[dot-mark_rate_limited()]] - `method` [EXTRACTED]
- [[dot-mark_success()]] - `method` [EXTRACTED]
- [[dot-reload()]] - `method` [EXTRACTED]
- [[dot-test_add_key_appends_to_existing()]] - `calls` [EXTRACTED]
- [[dot-test_add_key_creates_new_provider()]] - `calls` [EXTRACTED]
- [[dot-test_add_key_skips_placeholder()]] - `calls` [EXTRACTED]
- [[dot-test_cloudcli_key_loaded_from_env()]] - `calls` [EXTRACTED]
- [[dot-test_consecutive_429s_trip_circuit_breaker()]] - `calls` [INFERRED]
- [[dot-test_get_key_all_cooldown_multi_key_returns_none()]] - `calls` [EXTRACTED]
- [[dot-test_get_key_all_cooldown_returns_none()]] - `calls` [EXTRACTED]
- [[dot-test_get_key_missing()]] - `calls` [EXTRACTED]
- [[dot-test_get_key_no_provider()]] - `calls` [EXTRACTED]
- [[dot-test_get_key_recovers_cooldown()]] - `calls` [EXTRACTED]
- [[dot-test_get_key_returns_active_key_when_one_in_cooldown()]] - `calls` [EXTRACTED]
- [[dot-test_get_key_returns_least_used()]] - `calls` [EXTRACTED]
- [[dot-test_get_key_round_robin()]] - `calls` [EXTRACTED]
- [[dot-test_get_summary()]] - `calls` [EXTRACTED]
- [[dot-test_get_summary_new_metric_fields()]] - `calls` [EXTRACTED]
- [[dot-test_get_summary_no_cooldown_defaults()]] - `calls` [EXTRACTED]
- [[dot-test_load_keys_from_env_file()]] - `calls` [EXTRACTED]
- [[dot-test_mark_rate_limited()]] - `calls` [EXTRACTED]
- [[dot-test_mark_success()]] - `calls` [EXTRACTED]
- [[dot-test_mark_success_smoothed_latency()]] - `calls` [EXTRACTED]
- [[dot-test_reload_drops_keys_not_present_in_sources()]] - `calls` [EXTRACTED]
- [[dot-test_reload_picks_up_newly_added_source_key()]] - `calls` [EXTRACTED]
- [[dot-test_reload_preserves_stats_for_existing_key()]] - `calls` [EXTRACTED]
- [[dot-test_reload_replaces_pool_without_duplicating()]] - `calls` [EXTRACTED]
- [[dot-test_reload_swaps_rotated_secret_preserving_stats()]] - `calls` [EXTRACTED]
- [[TestAPIKeyInfo]] - `uses` [INFERRED]
- [[TestBanPersistence]] - `uses` [INFERRED]
- [[TestCLIStringFunctions]] - `uses` [INFERRED]
- [[TestCircuitBreaker_1]] - `uses` [INFERRED]
- [[TestCmdConfig]] - `uses` [INFERRED]
- [[TestCmdPromote]] - `uses` [INFERRED]
- [[TestCmdProviders]] - `uses` [INFERRED]
- [[TestCmdReport]] - `uses` [INFERRED]
- [[TestCmdRun]] - `uses` [INFERRED]
- [[TestCmdRunAutoSave]] - `uses` [INFERRED]
- [[TestCmdStatus]] - `uses` [INFERRED]
- [[TestCmdSwarm]] - `uses` [INFERRED]
- [[TestDispatchRequest]] - `uses` [INFERRED]
- [[TestFabricRouteOverlay]] - `uses` [INFERRED]
- [[TestFormatConversion]] - `uses` [INFERRED]
- [[TestKeyPoolManager]] - `uses` [INFERRED]
- [[TestKeyPoolReload]] - `uses` [INFERRED]
- [[TestLitellmPresenceInRoutes]] - `uses` [INFERRED]
- [[TestMain]] - `uses` [INFERRED]
- [[TestMalformedOverlayRoutes]] - `uses` [INFERRED]
- [[TestRouteBuilding]] - `uses` [INFERRED]
- [[isolated_key_pool()]] - `calls` [INFERRED]
- [[key_pool.py]] - `contains` [EXTRACTED]
- [[providers__init__.py]] - `imports` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/KeyPoolManager