---
source_file: "tests/test_streaming_proxy.py"
type: "code"
community: "test_streaming_proxy.py"
location: "L1"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/test_streaming_proxypy
---

# test_streaming_proxy.py

## Connections
- [[Tests for ``merged_agentic_swarm.streaming_proxy``. Covers the zero-buffering…]] - `rationale_for` [EXTRACTED]
- [[_ChunkStream]] - `contains` [EXTRACTED]
- [[_StallStream]] - `contains` [EXTRACTED]
- [[_sse_response()]] - `contains` [EXTRACTED]
- [[asyncio]] - `imports` [EXTRACTED]
- [[drain()]] - `contains` [EXTRACTED]
- [[make_proxy()]] - `contains` [EXTRACTED]
- [[make_request()]] - `contains` [EXTRACTED]
- [[post()]] - `contains` [EXTRACTED]
- [[streaming_proxy.py]] - `imports_from` [EXTRACTED]
- [[test_circuit_breaker_unit_transitions()]] - `contains` [EXTRACTED]
- [[test_circuit_opens_and_rejects_with_503()]] - `contains` [EXTRACTED]
- [[test_circuit_recovers_after_cooldown_half_open_probe()]] - `contains` [EXTRACTED]
- [[test_client_disconnect_closes_upstream()]] - `contains` [EXTRACTED]
- [[test_config_defaults()]] - `contains` [EXTRACTED]
- [[test_connect_error_fails_fast_without_retry()]] - `contains` [EXTRACTED]
- [[test_connection_reuse_single_pooled_client()]] - `contains` [EXTRACTED]
- [[test_create_streaming_proxy_app_factory()]] - `contains` [EXTRACTED]
- [[test_drop_in_asgi_app_handles_messages_endpoint()]] - `contains` [EXTRACTED]
- [[test_first_chunk_delivered_before_upstream_emits_rest()]] - `contains` [EXTRACTED]
- [[test_health_endpoint_503_when_upstream_down()]] - `contains` [EXTRACTED]
- [[test_health_endpoint_ok()]] - `contains` [EXTRACTED]
- [[test_mid_stream_failure_stops_gracefully_and_closes_upstream()]] - `contains` [EXTRACTED]
- [[test_non_2xx_upstream_body_passthrough_and_failure_recorded()]] - `contains` [EXTRACTED]
- [[test_passthrough_preserves_bytes_and_headers()]] - `contains` [EXTRACTED]
- [[test_prewarm_false_when_upstream_degraded_or_down()]] - `contains` [EXTRACTED]
- [[test_prewarm_true_on_healthy_upstream()]] - `contains` [EXTRACTED]
- [[test_request_headers_allowlisted_and_defaults()]] - `contains` [EXTRACTED]
- [[test_stalled_upstream_times_out_and_records_failure()]] - `contains` [EXTRACTED]
- [[test_success_resets_failure_counter()]] - `contains` [EXTRACTED]
- [[test_zero_buffering_preserves_chunk_boundaries()]] - `contains` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/test_streaming_proxypy