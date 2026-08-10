---
type: community
cohesion: 0.08
members: 43
---

# KeyPoolManager

**Cohesion:** 0.08 - loosely connected
**Members:** 43 nodes

## Members
- [[42 summary reports exhausted count, next cooldown expiry, avg latency.]] - rationale - tests/test_key_pool.py
- [[dot-__init__()_5]] - code - src/merged_agentic_swarm/providers/key_pool.py
- [[dot-_collect_keys_from_sources()]] - code - src/merged_agentic_swarm/providers/key_pool.py
- [[dot-_get_summary_unlocked()]] - code - src/merged_agentic_swarm/providers/key_pool.py
- [[dot-add_key()]] - code - src/merged_agentic_swarm/providers/key_pool.py
- [[dot-get_summary()]] - code - src/merged_agentic_swarm/providers/key_pool.py
- [[dot-load_keys()]] - code - src/merged_agentic_swarm/providers/key_pool.py
- [[dot-reload()]] - code - src/merged_agentic_swarm/providers/key_pool.py
- [[dot-test_add_key_appends_to_existing()]] - code - tests/test_key_pool.py
- [[dot-test_add_key_creates_new_provider()]] - code - tests/test_key_pool.py
- [[dot-test_add_key_skips_placeholder()]] - code - tests/test_key_pool.py
- [[dot-test_cloudcli_key_loaded_from_env()]] - code - tests/test_key_pool.py
- [[dot-test_get_key_all_cooldown_multi_key_returns_none()]] - code - tests/test_key_pool.py
- [[dot-test_get_key_all_cooldown_returns_none()]] - code - tests/test_key_pool.py
- [[dot-test_get_key_missing()]] - code - tests/test_key_pool.py
- [[dot-test_get_key_no_provider()]] - code - tests/test_key_pool.py
- [[dot-test_get_key_recovers_cooldown()]] - code - tests/test_key_pool.py
- [[dot-test_get_key_returns_active_key_when_one_in_cooldown()]] - code - tests/test_key_pool.py
- [[dot-test_get_key_returns_least_used()]] - code - tests/test_key_pool.py
- [[dot-test_get_key_round_robin()]] - code - tests/test_key_pool.py
- [[dot-test_get_summary()]] - code - tests/test_key_pool.py
- [[dot-test_get_summary_new_metric_fields()]] - code - tests/test_key_pool.py
- [[dot-test_get_summary_no_cooldown_defaults()]] - code - tests/test_key_pool.py
- [[dot-test_load_keys_from_env_file()]] - code - tests/test_key_pool.py
- [[dot-test_mark_rate_limited()]] - code - tests/test_key_pool.py
- [[dot-test_mark_success()]] - code - tests/test_key_pool.py
- [[dot-test_mark_success_smoothed_latency()]] - code - tests/test_key_pool.py
- [[dot-test_reload_drops_keys_not_present_in_sources()]] - code - tests/test_key_pool.py
- [[dot-test_reload_picks_up_newly_added_source_key()]] - code - tests/test_key_pool.py
- [[dot-test_reload_preserves_stats_for_existing_key()]] - code - tests/test_key_pool.py
- [[dot-test_reload_replaces_pool_without_duplicating()]] - code - tests/test_key_pool.py
- [[dot-test_reload_swaps_rotated_secret_preserving_stats()]] - code - tests/test_key_pool.py
- [[A key still cooling down must not be picked while another is active.]] - rationale - tests/test_key_pool.py
- [[Any_8]] - code
- [[Even with many keys, none may be reused while every one is cooling down.]] - rationale - tests/test_key_pool.py
- [[Gather (provider, secret_value, key_id) candidates from all key sources.…]] - rationale - src/merged_agentic_swarm/providers/key_pool.py
- [[Getting a key from a provider that doesn't exist should not raise.]] - rationale - tests/test_key_pool.py
- [[Hot-reload keys from all sources, preserving runtime stats for persistent keys.…]] - rationale - src/merged_agentic_swarm/providers/key_pool.py
- [[KeyPoolManager]] - code - src/merged_agentic_swarm/providers/key_pool.py
- [[Loads API keys from env file, environment variables, and local key files.]] - rationale - src/merged_agentic_swarm/providers/key_pool.py
- [[TestKeyPoolManager]] - code - tests/test_key_pool.py
- [[TestKeyPoolReload]] - code - tests/test_key_pool.py
- [[When every key is still cooling down, get_key returns None so the fabric…]] - rationale - tests/test_key_pool.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/KeyPoolManager
SORT file.name ASC
```

## Connections to other communities
- 15 edges to [[_COMMUNITY_APIKeyInfo]]
- 7 edges to [[_COMMUNITY_test_agentic_cli.py]]
- 2 edges to [[_COMMUNITY_TestCmdProviders]]
- 2 edges to [[_COMMUNITY_TestDispatchRequest]]
- 2 edges to [[_COMMUNITY_test_multi_provider_fabric.py]]
- 1 edge to [[_COMMUNITY_conftest.py]]
- 1 edge to [[_COMMUNITY_TestCLIStringFunctions]]
- 1 edge to [[_COMMUNITY_cmd_config]]
- 1 edge to [[_COMMUNITY_TestBanPersistence]]
- 1 edge to [[_COMMUNITY__record_failure]]
- 1 edge to [[_COMMUNITY_TestFormatConversion]]
- 1 edge to [[_COMMUNITY_TestLitellmPresenceInRoutes]]
- 1 edge to [[_COMMUNITY_TestMalformedOverlayRoutes]]

## Top bridge nodes
- [[KeyPoolManager]] - degree 61, connects to 13 communities
- [[TestKeyPoolManager]] - degree 23, connects to 1 community
- [[TestKeyPoolReload]] - degree 9, connects to 1 community
- [[dot-reload()]] - degree 4, connects to 1 community
- [[dot-add_key()]] - degree 3, connects to 1 community