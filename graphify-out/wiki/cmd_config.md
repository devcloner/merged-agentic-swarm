# cmd_config

> 31 nodes · cohesion 0.17

## Key Concepts

- **test_streaming_proxy.py** (31 connections) — `tests/test_streaming_proxy.py`
- **asyncio** (23 connections)
- **make_proxy()** (22 connections) — `tests/test_streaming_proxy.py`
- **post()** (17 connections) — `tests/test_streaming_proxy.py`
- **test_connection_reuse_single_pooled_client()** (6 connections) — `tests/test_streaming_proxy.py`
- **test_first_chunk_delivered_before_upstream_emits_rest()** (6 connections) — `tests/test_streaming_proxy.py`
- **test_client_disconnect_closes_upstream()** (5 connections) — `tests/test_streaming_proxy.py`
- **test_request_headers_allowlisted_and_defaults()** (5 connections) — `tests/test_streaming_proxy.py`
- **test_stalled_upstream_times_out_and_records_failure()** (5 connections) — `tests/test_streaming_proxy.py`
- **test_zero_buffering_preserves_chunk_boundaries()** (5 connections) — `tests/test_streaming_proxy.py`
- **test_circuit_opens_and_rejects_with_503()** (4 connections) — `tests/test_streaming_proxy.py`
- **test_circuit_recovers_after_cooldown_half_open_probe()** (4 connections) — `tests/test_streaming_proxy.py`
- **test_connect_error_fails_fast_without_retry()** (4 connections) — `tests/test_streaming_proxy.py`
- **test_drop_in_asgi_app_handles_messages_endpoint()** (4 connections) — `tests/test_streaming_proxy.py`
- **test_mid_stream_failure_stops_gracefully_and_closes_upstream()** (4 connections) — `tests/test_streaming_proxy.py`
- **test_non_2xx_upstream_body_passthrough_and_failure_recorded()** (4 connections) — `tests/test_streaming_proxy.py`
- **test_passthrough_preserves_bytes_and_headers()** (4 connections) — `tests/test_streaming_proxy.py`
- **test_success_resets_failure_counter()** (4 connections) — `tests/test_streaming_proxy.py`
- **make_request()** (3 connections) — `tests/test_streaming_proxy.py`
- **test_health_endpoint_503_when_upstream_down()** (3 connections) — `tests/test_streaming_proxy.py`
- **test_health_endpoint_ok()** (3 connections) — `tests/test_streaming_proxy.py`
- **test_prewarm_false_when_upstream_degraded_or_down()** (3 connections) — `tests/test_streaming_proxy.py`
- **test_prewarm_true_on_healthy_upstream()** (3 connections) — `tests/test_streaming_proxy.py`
- **Tests for ``merged_agentic_swarm.streaming_proxy``. Covers the zero-buffering…** (1 connections) — `tests/test_streaming_proxy.py`
- **Send one proxied request and return the proxy's Response.** (1 connections) — `tests/test_streaming_proxy.py`
- *... and 6 more nodes in this community*

## Relationships

- [load_durable_agents.sh](load_durable_agents.sh.md) (6 shared connections)
- [Merged Agentic Swarm](Merged_Agentic_Swarm.md) (5 shared connections)
- [_forward_transcription](_forward_transcription.md) (2 shared connections)
- [package.json](package.json.md) (2 shared connections)
- [HopResult](HopResult.md) (1 shared connections)
- [Graphify Knowledge Graph Pipeline](Graphify_Knowledge_Graph_Pipeline.md) (1 shared connections)
- [TestDispatchRequest](TestDispatchRequest.md) (1 shared connections)

## Source Files

- `tests/test_streaming_proxy.py`

## Audit Trail

- EXTRACTED: 180 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*