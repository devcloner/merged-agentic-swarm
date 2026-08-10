# Graphify Knowledge Graph Pipeline

> 22 nodes · cohesion 0.10

## Key Concepts

- **test_health_check.py** (43 connections) — `tests/test_health_check.py`
- **.from_env()** (7 connections) — `src/merged_agentic_swarm/health_check.py`
- **test_main_json_output_all()** (4 connections) — `tests/test_health_check.py`
- **test_main_json_output_degraded()** (4 connections) — `tests/test_health_check.py`
- **test_main_providers_subcommand()** (4 connections) — `tests/test_health_check.py`
- **test_main_status_command()** (4 connections) — `tests/test_health_check.py`
- **.__init__()** (3 connections) — `src/merged_agentic_swarm/health_check.py`
- **_make_sse_response()** (3 connections) — `tests/test_health_check.py`
- **test_from_env_defaults()** (3 connections) — `tests/test_health_check.py`
- **test_from_env_invalid_numeric_falls_through()** (3 connections) — `tests/test_health_check.py`
- **test_from_env_override_numerics()** (3 connections) — `tests/test_health_check.py`
- **test_from_env_override_strings()** (3 connections) — `tests/test_health_check.py`
- **Response** (1 connections)
- **Return a 200 httpx.Response whose .stream yields SSE events.** (1 connections) — `tests/test_health_check.py`
- **from_env returns defaults when no env vars are set.** (1 connections) — `tests/test_health_check.py`
- **from_env picks up env overrides for string fields.** (1 connections) — `tests/test_health_check.py`
- **from_env casts numeric env vars to int/float.** (1 connections) — `tests/test_health_check.py`
- **from_env surfaces ValueError for non-numeric env values (no silent fallback).** (1 connections) — `tests/test_health_check.py`
- **--json flag emits machine-readable JSON for all checks.** (1 connections) — `tests/test_health_check.py`
- **--json reports degraded when a check fails.** (1 connections) — `tests/test_health_check.py`
- **status' subcommand runs hop probes only (no streaming).** (1 connections) — `tests/test_health_check.py`
- **providers' subcommand runs provider/circuit-breaker checks.** (1 connections) — `tests/test_health_check.py`

## Relationships

- [DurableAgentFactory](DurableAgentFactory.md) (27 shared connections)
- [HopResult](HopResult.md) (14 shared connections)
- [_DNSCache](_DNSCache.md) (4 shared connections)
- [cmd_config](cmd_config.md) (1 shared connections)

## Source Files

- `src/merged_agentic_swarm/health_check.py`
- `tests/test_health_check.py`

## Audit Trail

- EXTRACTED: 94 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*