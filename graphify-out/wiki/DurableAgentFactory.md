# DurableAgentFactory

> 38 nodes · cohesion 0.10

## Key Concepts

- **ProxyChainHealth** (31 connections) — `src/merged_agentic_swarm/health_check.py`
- **HealthConfig** (27 connections) — `src/merged_agentic_swarm/health_check.py`
- **_patch_client()** (27 connections) — `tests/test_health_check.py`
- **test_check_opencode_connection_error()** (5 connections) — `tests/test_health_check.py`
- **test_check_opencode_error_response()** (5 connections) — `tests/test_health_check.py`
- **test_check_opencode_happy_path()** (5 connections) — `tests/test_health_check.py`
- **test_check_providers_fcc_models_error()** (5 connections) — `tests/test_health_check.py`
- **test_check_providers_fcc_models_list_format()** (5 connections) — `tests/test_health_check.py`
- **test_check_providers_happy_path()** (5 connections) — `tests/test_health_check.py`
- **test_check_routatic_connection_error()** (5 connections) — `tests/test_health_check.py`
- **test_check_routatic_happy_path()** (5 connections) — `tests/test_health_check.py`
- **test_check_routatic_non_json_body()** (5 connections) — `tests/test_health_check.py`
- **test_check_streaming_connection_error()** (5 connections) — `tests/test_health_check.py`
- **test_check_streaming_http_error()** (5 connections) — `tests/test_health_check.py`
- **test_check_streaming_no_deltas()** (5 connections) — `tests/test_health_check.py`
- **test_run_all_stable_order()** (5 connections) — `tests/test_health_check.py`
- **test_run_all_without_stream()** (5 connections) — `tests/test_health_check.py`
- **test_check_fcc_accepts_json_status_healthy()** (4 connections) — `tests/test_health_check.py`
- **test_check_fcc_accepts_json_status_ok()** (4 connections) — `tests/test_health_check.py`
- **test_check_fcc_connection_error_reports_fail()** (4 connections) — `tests/test_health_check.py`
- **test_check_fcc_plain_text_healthy()** (4 connections) — `tests/test_health_check.py`
- **test_check_fcc_rejects_json_status_degraded()** (4 connections) — `tests/test_health_check.py`
- **Runs reachability, streaming, and provider-status checks.** (1 connections) — `src/merged_agentic_swarm/health_check.py`
- **Endpoints and request tuning for the health checks. Each field falls back to…** (1 connections) — `src/merged_agentic_swarm/health_check.py`
- **check_opencode reports failure on HTTP 500 from upstream.** (1 connections) — `tests/test_health_check.py`
- *... and 13 more nodes in this community*

## Relationships

- [Graphify Knowledge Graph Pipeline](Graphify_Knowledge_Graph_Pipeline.md) (27 shared connections)
- [_DNSCache](_DNSCache.md) (7 shared connections)
- [_parse_multipart](_parse_multipart.md) (6 shared connections)
- [HopResult](HopResult.md) (5 shared connections)

## Source Files

- `src/merged_agentic_swarm/health_check.py`
- `tests/test_health_check.py`

## Audit Trail

- EXTRACTED: 191 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*