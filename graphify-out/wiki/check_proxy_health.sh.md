# check_proxy_health.sh

> 8 nodes · cohesion 0.25

## Key Concepts

- **_run_latency_test()** (5 connections) — `src/merged_agentic_swarm/webapp.py`
- **_fetch_litellm_aliases()** (4 connections) — `src/merged_agentic_swarm/webapp.py`
- **_latency_error()** (4 connections) — `src/merged_agentic_swarm/webapp.py`
- **AsyncClient** (3 connections)
- **Exception** (1 connections)
- **Live litellm /v1/models aliases; on failure (aliases=[], note).** (1 connections) — `src/merged_agentic_swarm/webapp.py`
- **ok:false payload — short error, never the key.** (1 connections) — `src/merged_agentic_swarm/webapp.py`
- **Stream one chat/completions request; report TTFB and total wall time.** (1 connections) — `src/merged_agentic_swarm/webapp.py`

## Relationships

- [FastFallbackConfig](FastFallbackConfig.md) (3 shared connections)
- [_make_learning_entry](_make_learning_entry.md) (3 shared connections)

## Source Files

- `src/merged_agentic_swarm/webapp.py`

## Audit Trail

- EXTRACTED: 20 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*