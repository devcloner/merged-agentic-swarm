# webapp.py

> 47 nodes · cohesion 0.09

## Key Concepts

- **_router_with_keys()** (20 connections) — `tests/test_fast_fallback.py`
- **test_fast_fallback.py** (14 connections) — `tests/test_fast_fallback.py`
- **patch** (14 connections)
- **_url_routed()** (12 connections) — `tests/test_fast_fallback.py`
- **TestDispatchBehavior** (10 connections) — `tests/test_fast_fallback.py`
- **TestCircuitBreaker** (9 connections) — `tests/test_fast_fallback.py`
- **.test_dispatch_fast_uses_default_router()** (9 connections) — `tests/test_fast_fallback.py`
- **TestParallelProbe** (9 connections) — `tests/test_fast_fallback.py`
- **.test_half_open_after_cooldown_expiry()** (8 connections) — `tests/test_fast_fallback.py`
- **.test_enabled_false_delegates_to_fabric()** (8 connections) — `tests/test_fast_fallback.py`
- **_anthropic_response()** (7 connections) — `tests/test_fast_fallback.py`
- **_mock_response()** (7 connections) — `tests/test_fast_fallback.py`
- **_reset_shared_fabric_state()** (7 connections) — `tests/test_fast_fallback.py`
- **.test_honours_shared_fabric_perma_ban()** (7 connections) — `tests/test_fast_fallback.py`
- **.test_non_dict_2xx_body_cascades()** (7 connections) — `tests/test_fast_fallback.py`
- **.test_non_json_2xx_body_cascades()** (7 connections) — `tests/test_fast_fallback.py`
- **TestDispatchHelper** (6 connections) — `tests/test_fast_fallback.py`
- **.test_slow_primary_with_stagger_lets_primary_win()** (6 connections) — `tests/test_fast_fallback.py`
- **.test_provider_skipped_after_threshold_failures()** (5 connections) — `tests/test_fast_fallback.py`
- **.test_rate_limit_rotates_key_not_breaker()** (5 connections) — `tests/test_fast_fallback.py`
- **.test_first_success_wins()** (5 connections) — `tests/test_fast_fallback.py`
- **.test_loser_records_no_spurious_failure()** (5 connections) — `tests/test_fast_fallback.py`
- **.test_primary_failure_falls_to_fallback_in_same_wave()** (5 connections) — `tests/test_fast_fallback.py`
- **.test_empty_conversation_returns_error()** (4 connections) — `tests/test_fast_fallback.py`
- **.test_simulation_fallback_when_all_blocked()** (4 connections) — `tests/test_fast_fallback.py`
- *... and 22 more nodes in this community*

## Relationships

- [verify_component.sh](verify_component.sh.md) (15 shared connections)
- [.run_full_agentic_workflow](run_full_agentic_workflow.md) (9 shared connections)
- [MultiProviderFabric](MultiProviderFabric.md) (7 shared connections)
- [services/__init__.py](services-__init__.py.md) (1 shared connections)

## Source Files

- `tests/test_fast_fallback.py`

## Audit Trail

- EXTRACTED: 214 (95%)
- INFERRED: 12 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*