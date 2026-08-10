---
type: community
cohesion: 0.18
members: 11
---

# TestChains

**Cohesion:** 0.18 - loosely connected
**Members:** 11 nodes

## Members
- [[dot-overlay_path()]] - code - tests/test_webapp.py
- [[dot-test_chains_get_merges_defaults_and_overlay()]] - code - tests/test_webapp.py
- [[dot-test_chains_put_invalid_400()]] - code - tests/test_webapp.py
- [[dot-test_chains_put_upserts_overlay_and_merges()]] - code - tests/test_webapp.py
- [[Point swarm_profiles at a throwaway registry seeded with the on-disk profiles.]] - rationale - tests/test_webapp.py
- [[Point webapp at a throwaway fabric-routes.json (never the real file).]] - rationale - tests/test_webapp.py
- [[Start each test with empty disk caches so patches don't leak across tests.]] - rationale - tests/test_webapp.py
- [[TestChains]] - code - tests/test_webapp.py
- [[_fresh_caches()]] - code - tests/test_webapp.py
- [[fixture_6]] - code
- [[tmp_profiles_file()]] - code - tests/test_webapp.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/TestChains
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_test_webapp.py]]
- 1 edge to [[_COMMUNITY_MultiLayeredAgenticOrchestrator]]
- 1 edge to [[_COMMUNITY_multi_provider_fabric.py]]

## Top bridge nodes
- [[TestChains]] - degree 6, connects to 2 communities
- [[fixture_6]] - degree 4, connects to 1 community
- [[_fresh_caches()]] - degree 3, connects to 1 community
- [[tmp_profiles_file()]] - degree 3, connects to 1 community