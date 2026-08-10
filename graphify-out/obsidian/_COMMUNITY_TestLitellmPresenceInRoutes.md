---
type: community
cohesion: 0.40
members: 5
---

# TestLitellmPresenceInRoutes

**Cohesion:** 0.40 - moderately connected
**Members:** 5 nodes

## Members
- [[dot-test_each_fabric_alias_has_litellm_route()]] - code - tests/test_multi_provider_fabric.py
- [[dot-test_litellm_alias_routes_lead_with_litellm()]] - code - tests/test_multi_provider_fabric.py
- [[Role routing maps worker roles to litellm aliases, so every fabric tier must…]] - rationale - tests/test_multi_provider_fabric.py
- [[TestLitellmPresenceInRoutes]] - code - tests/test_multi_provider_fabric.py
- [[Worker-tier aliases route through the litellm gateway FIRST (42-key Gemini…]] - rationale - tests/test_multi_provider_fabric.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/TestLitellmPresenceInRoutes
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_KeyPoolManager]]
- 1 edge to [[_COMMUNITY_MultiProviderFabric]]
- 1 edge to [[_COMMUNITY_test_multi_provider_fabric.py]]

## Top bridge nodes
- [[TestLitellmPresenceInRoutes]] - degree 6, connects to 3 communities