# _parse_multipart

> 13 nodes · cohesion 0.21

## Key Concepts

- **.run_all()** (8 connections) — `src/merged_agentic_swarm/health_check.py`
- **.check_providers()** (6 connections) — `src/merged_agentic_swarm/health_check.py`
- **.check_routatic()** (6 connections) — `src/merged_agentic_swarm/health_check.py`
- **.check_streaming()** (6 connections) — `src/merged_agentic_swarm/health_check.py`
- **_truncate()** (6 connections) — `src/merged_agentic_swarm/health_check.py`
- **.check_fcc()** (5 connections) — `src/merged_agentic_swarm/health_check.py`
- **.check_opencode()** (5 connections) — `src/merged_agentic_swarm/health_check.py`
- **Probe routatic-proxy /health and surface circuit-breaker metrics.** (1 connections) — `src/merged_agentic_swarm/health_check.py`
- **Probe the FCC gateway /health endpoint.** (1 connections) — `src/merged_agentic_swarm/health_check.py`
- **Check upstream OpenCode API reachability (models endpoint).** (1 connections) — `src/merged_agentic_swarm/health_check.py`
- **Stream a tiny /v1/messages request and time first token + total. ``endpoint``…** (1 connections) — `src/merged_agentic_swarm/health_check.py`
- **Monitor provider/circuit-breaker status via routatic + FCC models list.** (1 connections) — `src/merged_agentic_swarm/health_check.py`
- **Run every check; returns results in a stable order.** (1 connections) — `src/merged_agentic_swarm/health_check.py`

## Relationships

- [HopResult](HopResult.md) (10 shared connections)
- [DurableAgentFactory](DurableAgentFactory.md) (6 shared connections)

## Source Files

- `src/merged_agentic_swarm/health_check.py`

## Audit Trail

- EXTRACTED: 48 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*