---
type: community
cohesion: 0.13
members: 22
---

# APIKeyInfo

**Cohesion:** 0.13 - loosely connected
**Members:** 22 nodes

## Members
- [[dot-__repr__()]] - code - src/merged_agentic_swarm/providers/key_pool.py
- [[dot-_get_key_unlocked()]] - code - src/merged_agentic_swarm/providers/key_pool.py
- [[dot-get_key()]] - code - src/merged_agentic_swarm/providers/key_pool.py
- [[dot-mark_rate_limited()]] - code - src/merged_agentic_swarm/providers/key_pool.py
- [[dot-mark_success()]] - code - src/merged_agentic_swarm/providers/key_pool.py
- [[dot-test_default_creation()_2]] - code - tests/test_key_pool.py
- [[dot-test_mark_cooldown()]] - code - tests/test_key_pool.py
- [[dot-test_repr_does_not_leak_secret()]] - code - tests/test_key_pool.py
- [[API Key Pool Manager & Key Rotator Supports multi-provider key rotation, quota…]] - rationale - src/merged_agentic_swarm/providers/key_pool.py
- [[APIKeyInfo]] - code - src/merged_agentic_swarm/providers/key_pool.py
- [[Avoid leaking the secret value in logsdebug output.]] - rationale - src/merged_agentic_swarm/providers/key_pool.py
- [[Enum_3]] - code
- [[Gets an active API key using round-robin  least-used strategy.]] - rationale - src/merged_agentic_swarm/providers/key_pool.py
- [[Internal must be called while holding self._lock.]] - rationale - src/merged_agentic_swarm/providers/key_pool.py
- [[KeyStatus]] - code - src/merged_agentic_swarm/providers/key_pool.py
- [[Providers Package Initialization]] - rationale - src/merged_agentic_swarm/providers/__init__.py
- [[TestAPIKeyInfo]] - code - tests/test_key_pool.py
- [[Tests for providerskey_pool.py Coverage APIKeyInfo, KeyPoolManager…]] - rationale - tests/test_key_pool.py
- [[key_pool.py]] - code - src/merged_agentic_swarm/providers/key_pool.py
- [[providers__init__.py]] - code - src/merged_agentic_swarm/providers/__init__.py
- [[str_3]] - code
- [[test_key_pool.py]] - code - tests/test_key_pool.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/APIKeyInfo
SORT file.name ASC
```

## Connections to other communities
- 15 edges to [[_COMMUNITY_KeyPoolManager]]
- 6 edges to [[_COMMUNITY_FastFallbackRouter]]
- 2 edges to [[_COMMUNITY_multi_provider_fabric.py]]
- 2 edges to [[_COMMUNITY_webapp.py]]
- 1 edge to [[_COMMUNITY_FastFallbackConfig]]
- 1 edge to [[_COMMUNITY_MultiProviderFabric]]
- 1 edge to [[_COMMUNITY_claude_proxy_server.py]]

## Top bridge nodes
- [[key_pool.py]] - degree 11, connects to 5 communities
- [[providers__init__.py]] - degree 8, connects to 4 communities
- [[APIKeyInfo]] - degree 21, connects to 3 communities
- [[KeyStatus]] - degree 7, connects to 1 community
- [[TestAPIKeyInfo]] - degree 7, connects to 1 community