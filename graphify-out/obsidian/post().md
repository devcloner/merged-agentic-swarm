---
source_file: "tests/test_streaming_proxy.py"
type: "code"
community: "test_streaming_proxy.py"
location: "L129"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/test_streaming_proxypy
---

# post()

## Connections
- [[Send one proxied request and return the proxy's Response.]] - `rationale_for` [EXTRACTED]
- [[make_request()]] - `calls` [EXTRACTED]
- [[test_circuit_opens_and_rejects_with_503()]] - `calls` [EXTRACTED]
- [[test_circuit_recovers_after_cooldown_half_open_probe()]] - `calls` [EXTRACTED]
- [[test_client_disconnect_closes_upstream()]] - `calls` [EXTRACTED]
- [[test_connect_error_fails_fast_without_retry()]] - `calls` [EXTRACTED]
- [[test_connection_reuse_single_pooled_client()]] - `calls` [EXTRACTED]
- [[test_drop_in_asgi_app_handles_messages_endpoint()]] - `calls` [EXTRACTED]
- [[test_first_chunk_delivered_before_upstream_emits_rest()]] - `calls` [EXTRACTED]
- [[test_mid_stream_failure_stops_gracefully_and_closes_upstream()]] - `calls` [EXTRACTED]
- [[test_non_2xx_upstream_body_passthrough_and_failure_recorded()]] - `calls` [EXTRACTED]
- [[test_passthrough_preserves_bytes_and_headers()]] - `calls` [EXTRACTED]
- [[test_request_headers_allowlisted_and_defaults()]] - `calls` [EXTRACTED]
- [[test_stalled_upstream_times_out_and_records_failure()]] - `calls` [EXTRACTED]
- [[test_streaming_proxy.py]] - `contains` [EXTRACTED]
- [[test_success_resets_failure_counter()]] - `calls` [EXTRACTED]
- [[test_zero_buffering_preserves_chunk_boundaries()]] - `calls` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/test_streaming_proxypy