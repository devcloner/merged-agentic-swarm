---
type: community
cohesion: 0.33
members: 6
---

# TestBanPersistence

**Cohesion:** 0.33 - loosely connected
**Members:** 6 nodes

## Members
- [[40 401 perma-bans persist to disk and are honored across reloads.]] - rationale - tests/test_multi_provider_fabric.py
- [[dot-setup_method()_14]] - code - tests/test_multi_provider_fabric.py
- [[dot-test_401_persists_ban_and_reload_restores()]] - code - tests/test_multi_provider_fabric.py
- [[dot-test_expired_ban_dropped_on_load()]] - code - tests/test_multi_provider_fabric.py
- [[dot-test_non_401_failure_does_not_persist_ban()]] - code - tests/test_multi_provider_fabric.py
- [[TestBanPersistence]] - code - tests/test_multi_provider_fabric.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/TestBanPersistence
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_KeyPoolManager]]
- 1 edge to [[_COMMUNITY_MultiProviderFabric]]
- 1 edge to [[_COMMUNITY_test_multi_provider_fabric.py]]

## Top bridge nodes
- [[TestBanPersistence]] - degree 8, connects to 3 communities