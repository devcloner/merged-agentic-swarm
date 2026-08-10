---
type: community
cohesion: 0.25
members: 9
---

# _load_registry

**Cohesion:** 0.25 - loosely connected
**Members:** 9 nodes

## Members
- [[Any_15]] - code
- [[Clear the cached registry and reload it from disk. Called after the provider…]] - rationale - src/merged_agentic_swarm/services/model_routing.py
- [[Load the provider registry (cached); return {} when missingunreadable.]] - rationale - src/merged_agentic_swarm/services/model_routing.py
- [[Persist one role - alias mapping into PROVIDER_REGISTRY.json atomically. The…]] - rationale - src/merged_agentic_swarm/webapp.py
- [[Tier + registered-role - litellm alias via model_routing resolution.]] - rationale - src/merged_agentic_swarm/webapp.py
- [[_load_registry()]] - code - src/merged_agentic_swarm/services/model_routing.py
- [[_role_mapping()]] - code - src/merged_agentic_swarm/webapp.py
- [[_write_registry_roles()]] - code - src/merged_agentic_swarm/webapp.py
- [[reload_registry()]] - code - src/merged_agentic_swarm/services/model_routing.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/_load_registry
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_services__init__.py]]
- 5 edges to [[_COMMUNITY_webapp.py]]

## Top bridge nodes
- [[_role_mapping()]] - degree 6, connects to 2 communities
- [[_load_registry()]] - degree 6, connects to 1 community
- [[reload_registry()]] - degree 6, connects to 1 community
- [[_write_registry_roles()]] - degree 4, connects to 1 community