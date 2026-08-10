---
type: community
cohesion: 0.14
members: 18
---

# FastFallbackConfig

**Cohesion:** 0.14 - loosely connected
**Members:** 18 nodes

## Members
- [[dot-__init__()]] - code - src/merged_agentic_swarm/fast_fallback.py
- [[dot-__post_init__()]] - code - src/merged_agentic_swarm/fast_fallback.py
- [[dot-from_env()]] - code - src/merged_agentic_swarm/fast_fallback.py
- [[dot-setup_method()_5]] - code - tests/test_fast_fallback.py
- [[dot-test_defaults()]] - code - tests/test_fast_fallback.py
- [[dot-test_env_overrides()]] - code - tests/test_fast_fallback.py
- [[dot-test_fast_fallback_promoted()]] - code - tests/test_fast_fallback.py
- [[dot-test_skipped_provider_removed_from_order()]] - code - tests/test_fast_fallback.py
- [[dot-test_static_order_preserved_without_samples()]] - code - tests/test_fast_fallback.py
- [[A fallback with strong latency history outranks a slow primary.]] - rationale - tests/test_fast_fallback.py
- [[A perma-banned provider does not appear in the candidate list.]] - rationale - tests/test_fast_fallback.py
- [[Build a config from ``FAST_FALLBACK_`` environment variables.]] - rationale - src/merged_agentic_swarm/fast_fallback.py
- [[FastFallbackConfig]] - code - src/merged_agentic_swarm/fast_fallback.py
- [[No latency history → static verified-first order is untouched.]] - rationale - tests/test_fast_fallback.py
- [[TestAdaptiveSelection]] - code - tests/test_fast_fallback.py
- [[TestConfigFromEnv]] - code - tests/test_fast_fallback.py
- [[Tunables for the fast-fallback router (dataclass defaults + env overrides).]] - rationale - src/merged_agentic_swarm/fast_fallback.py
- [[dict]] - code

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/FastFallbackConfig
SORT file.name ASC
```

## Connections to other communities
- 15 edges to [[_COMMUNITY__router_with_keys]]
- 5 edges to [[_COMMUNITY_FastFallbackRouter]]
- 4 edges to [[_COMMUNITY_MultiProviderFabric]]
- 1 edge to [[_COMMUNITY_APIKeyInfo]]

## Top bridge nodes
- [[FastFallbackConfig]] - degree 19, connects to 4 communities
- [[TestAdaptiveSelection]] - degree 8, connects to 3 communities
- [[TestConfigFromEnv]] - degree 6, connects to 3 communities
- [[dot-__init__()]] - degree 5, connects to 2 communities
- [[dot-test_fast_fallback_promoted()]] - degree 4, connects to 1 community