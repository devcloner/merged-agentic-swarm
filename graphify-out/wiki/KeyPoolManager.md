# KeyPoolManager

> 32 nodes · cohesion 0.11

## Key Concepts

- **KeyPoolManager** (61 connections) — `src/merged_agentic_swarm/providers/key_pool.py`
- **TestKeyPoolManager** (23 connections) — `tests/test_key_pool.py`
- **TestKeyPoolReload** (9 connections) — `tests/test_key_pool.py`
- **.test_get_key_all_cooldown_multi_key_returns_none()** (3 connections) — `tests/test_key_pool.py`
- **.test_get_key_all_cooldown_returns_none()** (3 connections) — `tests/test_key_pool.py`
- **.test_get_key_missing()** (3 connections) — `tests/test_key_pool.py`
- **.test_get_key_returns_active_key_when_one_in_cooldown()** (3 connections) — `tests/test_key_pool.py`
- **.test_get_summary_new_metric_fields()** (3 connections) — `tests/test_key_pool.py`
- **.test_add_key_appends_to_existing()** (2 connections) — `tests/test_key_pool.py`
- **.test_add_key_creates_new_provider()** (2 connections) — `tests/test_key_pool.py`
- **.test_add_key_skips_placeholder()** (2 connections) — `tests/test_key_pool.py`
- **.test_cloudcli_key_loaded_from_env()** (2 connections) — `tests/test_key_pool.py`
- **.test_get_key_no_provider()** (2 connections) — `tests/test_key_pool.py`
- **.test_get_key_recovers_cooldown()** (2 connections) — `tests/test_key_pool.py`
- **.test_get_key_returns_least_used()** (2 connections) — `tests/test_key_pool.py`
- **.test_get_key_round_robin()** (2 connections) — `tests/test_key_pool.py`
- **.test_get_summary()** (2 connections) — `tests/test_key_pool.py`
- **.test_get_summary_no_cooldown_defaults()** (2 connections) — `tests/test_key_pool.py`
- **.test_load_keys_from_env_file()** (2 connections) — `tests/test_key_pool.py`
- **.test_mark_rate_limited()** (2 connections) — `tests/test_key_pool.py`
- **.test_mark_success()** (2 connections) — `tests/test_key_pool.py`
- **.test_mark_success_smoothed_latency()** (2 connections) — `tests/test_key_pool.py`
- **.test_reload_drops_keys_not_present_in_sources()** (2 connections) — `tests/test_key_pool.py`
- **.test_reload_picks_up_newly_added_source_key()** (2 connections) — `tests/test_key_pool.py`
- **.test_reload_preserves_stats_for_existing_key()** (2 connections) — `tests/test_key_pool.py`
- *... and 7 more nodes in this community*

## Relationships

- [TestFormatConversion](TestFormatConversion.md) (9 shared connections)
- [services/__init__.py](services-__init__.py.md) (5 shared connections)
- [opencode-swarm.json](opencode-swarm.json.md) (5 shared connections)
- [litellm](litellm.md) (4 shared connections)
- [_args](_args.md) (3 shared connections)
- [MultiProviderFabric](MultiProviderFabric.md) (3 shared connections)
- [Community 157](Community_157.md) (2 shared connections)
- [Merged Agentic Swarm Blueprint (Root)](Merged_Agentic_Swarm_Blueprint_%28Root%29.md) (2 shared connections)
- [test_webapp.py](test_webapp.py.md) (2 shared connections)
- [ci.sh](ci.sh.md) (2 shared connections)
- [task_spine_cli.py](task_spine_cli.py.md) (2 shared connections)
- [conftest.py](conftest.py.md) (1 shared connections)

## Source Files

- `src/merged_agentic_swarm/providers/key_pool.py`
- `tests/test_key_pool.py`

## Audit Trail

- EXTRACTED: 121 (80%)
- INFERRED: 30 (20%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*