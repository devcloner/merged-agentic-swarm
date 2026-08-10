---
type: community
cohesion: 0.21
members: 13
---

# .run_all

**Cohesion:** 0.21 - loosely connected
**Members:** 13 nodes

## Members
- [[dot-check_fcc()]] - code - src/merged_agentic_swarm/health_check.py
- [[dot-check_opencode()]] - code - src/merged_agentic_swarm/health_check.py
- [[dot-check_providers()]] - code - src/merged_agentic_swarm/health_check.py
- [[dot-check_routatic()]] - code - src/merged_agentic_swarm/health_check.py
- [[dot-check_streaming()]] - code - src/merged_agentic_swarm/health_check.py
- [[dot-run_all()]] - code - src/merged_agentic_swarm/health_check.py
- [[Check upstream OpenCode API reachability (models endpoint).]] - rationale - src/merged_agentic_swarm/health_check.py
- [[Monitor providercircuit-breaker status via routatic + FCC models list.]] - rationale - src/merged_agentic_swarm/health_check.py
- [[Probe routatic-proxy health and surface circuit-breaker metrics.]] - rationale - src/merged_agentic_swarm/health_check.py
- [[Probe the FCC gateway health endpoint.]] - rationale - src/merged_agentic_swarm/health_check.py
- [[Run every check; returns results in a stable order.]] - rationale - src/merged_agentic_swarm/health_check.py
- [[Stream a tiny v1messages request and time first token + total. ``endpoint``…]] - rationale - src/merged_agentic_swarm/health_check.py
- [[_truncate()]] - code - src/merged_agentic_swarm/health_check.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/run_all
SORT file.name ASC
```

## Connections to other communities
- 10 edges to [[_COMMUNITY_HopResult]]
- 6 edges to [[_COMMUNITY_ProxyChainHealth]]

## Top bridge nodes
- [[dot-run_all()]] - degree 8, connects to 2 communities
- [[dot-check_providers()]] - degree 6, connects to 2 communities
- [[dot-check_routatic()]] - degree 6, connects to 2 communities
- [[dot-check_streaming()]] - degree 6, connects to 2 communities
- [[dot-check_fcc()]] - degree 5, connects to 2 communities