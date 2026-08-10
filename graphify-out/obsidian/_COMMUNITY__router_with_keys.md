---
type: community
cohesion: 0.09
members: 47
---

# _router_with_keys

**Cohesion:** 0.09 - loosely connected
**Members:** 47 nodes

## Members
- [[dot-setup_method()_4]] - code - tests/test_fast_fallback.py
- [[dot-setup_method()_6]] - code - tests/test_fast_fallback.py
- [[dot-setup_method()_7]] - code - tests/test_fast_fallback.py
- [[dot-setup_method()_3]] - code - tests/test_fast_fallback.py
- [[dot-test_dispatch_fast_uses_default_router()]] - code - tests/test_fast_fallback.py
- [[dot-test_empty_conversation_returns_error()]] - code - tests/test_fast_fallback.py
- [[dot-test_enabled_false_delegates_to_fabric()]] - code - tests/test_fast_fallback.py
- [[dot-test_first_success_wins()]] - code - tests/test_fast_fallback.py
- [[dot-test_half_open_after_cooldown_expiry()]] - code - tests/test_fast_fallback.py
- [[dot-test_honours_shared_fabric_perma_ban()]] - code - tests/test_fast_fallback.py
- [[dot-test_loser_records_no_spurious_failure()]] - code - tests/test_fast_fallback.py
- [[dot-test_non_dict_2xx_body_cascades()]] - code - tests/test_fast_fallback.py
- [[dot-test_non_json_2xx_body_cascades()]] - code - tests/test_fast_fallback.py
- [[dot-test_primary_failure_falls_to_fallback_in_same_wave()]] - code - tests/test_fast_fallback.py
- [[dot-test_provider_skipped_after_threshold_failures()]] - code - tests/test_fast_fallback.py
- [[dot-test_rate_limit_rotates_key_not_breaker()]] - code - tests/test_fast_fallback.py
- [[dot-test_simulation_fallback_when_all_blocked()]] - code - tests/test_fast_fallback.py
- [[dot-test_slow_primary_with_stagger_lets_primary_win()]] - code - tests/test_fast_fallback.py
- [[429 cools the key down but does not trip the provider breaker.]] - rationale - tests/test_fast_fallback.py
- [[A 2xx with a non-JSON body must be treated as failure, not raise.]] - rationale - tests/test_fast_fallback.py
- [[A 2xx with a non-dict body must be treated as failure, not crash.]] - rationale - tests/test_fast_fallback.py
- [[A fabric perma-banned provider is skipped without being probed.]] - rationale - tests/test_fast_fallback.py
- [[A failing primary overlaps the fallback's latency instead of serializing it.]] - rationale - tests/test_fast_fallback.py
- [[A losing in-flight probe (2xx after another probe won) must not corrupt state.]] - rationale - tests/test_fast_fallback.py
- [[After N consecutive failures the provider is skipped for the cooldown.]] - rationale - tests/test_fast_fallback.py
- [[Both wave probes fire concurrently; the first 2xx is returned.]] - rationale - tests/test_fast_fallback.py
- [[Build a pool_dispatch side_effect that routes by URL substring. ``side_map``…]] - rationale - tests/test_fast_fallback.py
- [[Build a router over the fixed two-route table with keys for both providers.]] - rationale - tests/test_fast_fallback.py
- [[Clear module-level fabric circuitperma-ban state shared with the router.]] - rationale - tests/test_fast_fallback.py
- [[Every provider skipped → simulation fallback, no provider calls.]] - rationale - tests/test_fast_fallback.py
- [[Malformed empty request short-circuits without any provider call.]] - rationale - tests/test_fast_fallback.py
- [[Once the cooldown expires the provider is probed again (half-open).]] - rationale - tests/test_fast_fallback.py
- [[TestCircuitBreaker]] - code - tests/test_fast_fallback.py
- [[TestDispatchBehavior]] - code - tests/test_fast_fallback.py
- [[TestDispatchHelper]] - code - tests/test_fast_fallback.py
- [[TestParallelProbe]] - code - tests/test_fast_fallback.py
- [[Tests for merged_agentic_swarmfast_fallback.py Coverage parallel probe first-…]] - rationale - tests/test_fast_fallback.py
- [[With probe_stagger_ms, the primary's head-start lets it win even if slower.]] - rationale - tests/test_fast_fallback.py
- [[_anthropic_response()]] - code - tests/test_fast_fallback.py
- [[_mock_response()]] - code - tests/test_fast_fallback.py
- [[_reset_shared_fabric_state()]] - code - tests/test_fast_fallback.py
- [[_router_with_keys()]] - code - tests/test_fast_fallback.py
- [[_url_routed()]] - code - tests/test_fast_fallback.py
- [[dispatch_fast reaches the default router and returns an Anthropic-shaped…]] - rationale - tests/test_fast_fallback.py
- [[enabled=False routes through the sequential fabric cascade.]] - rationale - tests/test_fast_fallback.py
- [[patch]] - code
- [[test_fast_fallback.py]] - code - tests/test_fast_fallback.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/_router_with_keys
SORT file.name ASC
```

## Connections to other communities
- 15 edges to [[_COMMUNITY_FastFallbackConfig]]
- 8 edges to [[_COMMUNITY_FastFallbackRouter]]
- 7 edges to [[_COMMUNITY_MultiProviderFabric]]
- 2 edges to [[_COMMUNITY_multi_provider_fabric.py]]

## Top bridge nodes
- [[_router_with_keys()]] - degree 20, connects to 3 communities
- [[TestDispatchBehavior]] - degree 10, connects to 3 communities
- [[TestCircuitBreaker]] - degree 9, connects to 3 communities
- [[dot-test_dispatch_fast_uses_default_router()]] - degree 9, connects to 3 communities
- [[TestParallelProbe]] - degree 9, connects to 3 communities