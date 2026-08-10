---
type: community
cohesion: 0.12
members: 35
---

# FastFallbackRouter

**Cohesion:** 0.12 - loosely connected
**Members:** 35 nodes

## Members
- [[dot-_build_payload()]] - code - src/merged_agentic_swarm/fast_fallback.py
- [[dot-_error_response()]] - code - src/merged_agentic_swarm/fast_fallback.py
- [[dot-_format_response()]] - code - src/merged_agentic_swarm/fast_fallback.py
- [[dot-_handle_http_error()]] - code - src/merged_agentic_swarm/fast_fallback.py
- [[dot-_is_skipped()]] - code - src/merged_agentic_swarm/fast_fallback.py
- [[dot-_maybe_reset_expired()]] - code - src/merged_agentic_swarm/fast_fallback.py
- [[dot-_order_candidates()]] - code - src/merged_agentic_swarm/fast_fallback.py
- [[dot-_probe_single()]] - code - src/merged_agentic_swarm/fast_fallback.py
- [[dot-_probe_wave()]] - code - src/merged_agentic_swarm/fast_fallback.py
- [[dot-_record_failure()]] - code - src/merged_agentic_swarm/fast_fallback.py
- [[dot-_record_success()]] - code - src/merged_agentic_swarm/fast_fallback.py
- [[dot-_route_timeout()]] - code - src/merged_agentic_swarm/fast_fallback.py
- [[dot-_simulation_fallback()]] - code - src/merged_agentic_swarm/fast_fallback.py
- [[dot-circuit_status()]] - code - src/merged_agentic_swarm/fast_fallback.py
- [[dot-dispatch()]] - code - src/merged_agentic_swarm/fast_fallback.py
- [[dot-reset()]] - code - src/merged_agentic_swarm/fast_fallback.py
- [[Any_1]] - code
- [[Build the per-provider payload, reusing the fabric's format helpers.]] - rationale - src/merged_agentic_swarm/fast_fallback.py
- [[Clear circuit-breaker and latency state (used by testshealth checks).]] - rationale - src/merged_agentic_swarm/fast_fallback.py
- [[Dispatch a request across providers with parallel fallback probing. Returns an…]] - rationale - src/merged_agentic_swarm/fast_fallback.py
- [[Dispatch a request through the fast-fallback router. Mirrors…]] - rationale - src/merged_agentic_swarm/fast_fallback.py
- [[Event]] - code
- [[Fast Fallback Router — parallel-probe, minimal-latency fallback dispatch. Why…]] - rationale - src/merged_agentic_swarm/fast_fallback.py
- [[FastFallbackRouter]] - code - src/merged_agentic_swarm/fast_fallback.py
- [[Fire one wave of probes concurrently; return the first success (or None).]] - rationale - src/merged_agentic_swarm/fast_fallback.py
- [[Normalize a provider response into the Anthropic-shaped return value.]] - rationale - src/merged_agentic_swarm/fast_fallback.py
- [[Parallel-probe fallback router over the model fabric's route table.…]] - rationale - src/merged_agentic_swarm/fast_fallback.py
- [[Probe one route; returns a result that records its own health effects.]] - rationale - src/merged_agentic_swarm/fast_fallback.py
- [[Record an HTTP error's health effects and return a failure result.]] - rationale - src/merged_agentic_swarm/fast_fallback.py
- [[Return healthy routes ordered by static priority + EWMA latency. Score = static…]] - rationale - src/merged_agentic_swarm/fast_fallback.py
- [[Snapshot of circuit-breaker and latency state per provider.]] - rationale - src/merged_agentic_swarm/fast_fallback.py
- [[_ProbeContext]] - code - src/merged_agentic_swarm/fast_fallback.py
- [[_ProbeResult]] - code - src/merged_agentic_swarm/fast_fallback.py
- [[dispatch_fast()]] - code - src/merged_agentic_swarm/fast_fallback.py
- [[fast_fallback.py]] - code - src/merged_agentic_swarm/fast_fallback.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/FastFallbackRouter
SORT file.name ASC
```

## Connections to other communities
- 9 edges to [[_COMMUNITY__router_with_keys]]
- 6 edges to [[_COMMUNITY_APIKeyInfo]]
- 5 edges to [[_COMMUNITY_FastFallbackConfig]]
- 4 edges to [[_COMMUNITY_MultiProviderFabric]]
- 3 edges to [[_COMMUNITY_multi_provider_fabric.py]]
- 2 edges to [[_COMMUNITY__record_failure]]
- 1 edge to [[_COMMUNITY_claude_proxy_server.py]]

## Top bridge nodes
- [[fast_fallback.py]] - degree 16, connects to 7 communities
- [[FastFallbackRouter]] - degree 31, connects to 4 communities
- [[_ProbeContext]] - degree 6, connects to 2 communities
- [[_ProbeResult]] - degree 6, connects to 2 communities
- [[Any_1]] - degree 13, connects to 1 community