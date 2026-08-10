---
type: community
cohesion: 0.17
members: 31
---

# test_streaming_proxy.py

**Cohesion:** 0.17 - loosely connected
**Members:** 31 nodes

## Members
- [[39 an upstream that stalls mid-stream must not hang the client forever.]] - rationale - tests/test_streaming_proxy.py
- [[All requests share one httpx.AsyncClient (connection pooling).]] - rationale - tests/test_streaming_proxy.py
- [[Build a PassthroughStreamingProxy pointed at a MockTransport upstream.]] - rationale - tests/test_streaming_proxy.py
- [[Build a Starlette Request carrying an Anthropic Messages body.]] - rationale - tests/test_streaming_proxy.py
- [[Each upstream network chunk must reach the client with identical boundaries —…]] - rationale - tests/test_streaming_proxy.py
- [[Proves no-buffering the first chunk is yielded the instant the upstream writes…]] - rationale - tests/test_streaming_proxy.py
- [[Send one proxied request and return the proxy's Response.]] - rationale - tests/test_streaming_proxy.py
- [[Tests for ``merged_agentic_swarm.streaming_proxy``. Covers the zero-buffering…]] - rationale - tests/test_streaming_proxy.py
- [[asyncio]] - code
- [[make_proxy()]] - code - tests/test_streaming_proxy.py
- [[make_request()]] - code - tests/test_streaming_proxy.py
- [[post()]] - code - tests/test_streaming_proxy.py
- [[test_circuit_opens_and_rejects_with_503()]] - code - tests/test_streaming_proxy.py
- [[test_circuit_recovers_after_cooldown_half_open_probe()]] - code - tests/test_streaming_proxy.py
- [[test_client_disconnect_closes_upstream()]] - code - tests/test_streaming_proxy.py
- [[test_connect_error_fails_fast_without_retry()]] - code - tests/test_streaming_proxy.py
- [[test_connection_reuse_single_pooled_client()]] - code - tests/test_streaming_proxy.py
- [[test_drop_in_asgi_app_handles_messages_endpoint()]] - code - tests/test_streaming_proxy.py
- [[test_first_chunk_delivered_before_upstream_emits_rest()]] - code - tests/test_streaming_proxy.py
- [[test_health_endpoint_503_when_upstream_down()]] - code - tests/test_streaming_proxy.py
- [[test_health_endpoint_ok()]] - code - tests/test_streaming_proxy.py
- [[test_mid_stream_failure_stops_gracefully_and_closes_upstream()]] - code - tests/test_streaming_proxy.py
- [[test_non_2xx_upstream_body_passthrough_and_failure_recorded()]] - code - tests/test_streaming_proxy.py
- [[test_passthrough_preserves_bytes_and_headers()]] - code - tests/test_streaming_proxy.py
- [[test_prewarm_false_when_upstream_degraded_or_down()]] - code - tests/test_streaming_proxy.py
- [[test_prewarm_true_on_healthy_upstream()]] - code - tests/test_streaming_proxy.py
- [[test_request_headers_allowlisted_and_defaults()]] - code - tests/test_streaming_proxy.py
- [[test_stalled_upstream_times_out_and_records_failure()]] - code - tests/test_streaming_proxy.py
- [[test_streaming_proxy.py]] - code - tests/test_streaming_proxy.py
- [[test_success_resets_failure_counter()]] - code - tests/test_streaming_proxy.py
- [[test_zero_buffering_preserves_chunk_boundaries()]] - code - tests/test_streaming_proxy.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/test_streaming_proxypy
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY__StallStream]]
- 5 edges to [[_COMMUNITY_StreamingProxyConfig]]
- 2 edges to [[_COMMUNITY__ChunkStream]]
- 2 edges to [[_COMMUNITY_CircuitBreaker]]
- 1 edge to [[_COMMUNITY_HopResult]]
- 1 edge to [[_COMMUNITY_PassthroughStreamingProxy]]
- 1 edge to [[_COMMUNITY_test_health_check.py]]

## Top bridge nodes
- [[test_streaming_proxy.py]] - degree 31, connects to 4 communities
- [[asyncio]] - degree 23, connects to 4 communities
- [[make_proxy()]] - degree 22, connects to 2 communities
- [[test_connection_reuse_single_pooled_client()]] - degree 6, connects to 1 community
- [[test_first_chunk_delivered_before_upstream_emits_rest()]] - degree 6, connects to 1 community