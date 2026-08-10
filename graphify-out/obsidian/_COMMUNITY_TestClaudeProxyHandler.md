---
type: community
cohesion: 0.06
members: 33
---

# TestClaudeProxyHandler

**Cohesion:** 0.06 - loosely connected
**Members:** 33 nodes

## Members
- [[33 FAST_FALLBACK_ENABLED routes through the hedged router.]] - rationale - tests/test_claude_proxy_server.py
- [[33 without the flag the proxy keeps using the fabric dispatch path.]] - rationale - tests/test_claude_proxy_server.py
- [[35 a body over the JSON cap must be rejected before buffering.]] - rationale - tests/test_claude_proxy_server.py
- [[35 a body under the cap still reaches normal processing (400 here).]] - rationale - tests/test_claude_proxy_server.py
- [[35 audio multipart bodies have their own (higher) cap.]] - rationale - tests/test_claude_proxy_server.py
- [[42 status surfaces exhaustedcooldownlatency per provider.]] - rationale - tests/test_claude_proxy_server.py
- [[dot-test_empty_content_length()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_fast_fallback_router_not_used_when_flag_unset()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_fast_fallback_router_used_when_flag_set()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_get_unknown_endpoint_returns_404()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_health_endpoint()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_options_request()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_post_chat_completions_openai_conversion()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_post_chat_completions_with_invalid_json()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_post_json_body_within_limit_not_413()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_post_oversized_audio_body_rejected_413()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_post_oversized_json_body_rejected_413()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_post_unsupported_endpoint()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_post_v1_messages()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_post_v1_messages_with_bearer_token()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_post_v1_messages_with_wrong_token_returns_401()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_post_v1_messages_without_token_returns_401()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_status_endpoint()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_status_endpoint_includes_per_key_metrics()]] - code - tests/test_claude_proxy_server.py
- [[OPTIONS request should return CORS headers.]] - rationale - tests/test_claude_proxy_server.py
- [[POST v1chatcompletions converts an Anthropic response to OpenAI shape.]] - rationale - tests/test_claude_proxy_server.py
- [[POST v1messages authenticated via Authorization Bearer → 200.]] - rationale - tests/test_claude_proxy_server.py
- [[POST v1messages should return a response (simulation fallback).]] - rationale - tests/test_claude_proxy_server.py
- [[POST v1messages with an invalid token → 401.]] - rationale - tests/test_claude_proxy_server.py
- [[POST v1messages without an auth token → 401.]] - rationale - tests/test_claude_proxy_server.py
- [[POST to unsupported path should return 404.]] - rationale - tests/test_claude_proxy_server.py
- [[POST with zero content-length should be handled.]] - rationale - tests/test_claude_proxy_server.py
- [[TestClaudeProxyHandler]] - code - tests/test_claude_proxy_server.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/TestClaudeProxyHandler
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_ProxyServerDaemon]]
- 2 edges to [[_COMMUNITY__parse_multipart]]
- 1 edge to [[_COMMUNITY_test_claude_proxy_server.py]]
- 1 edge to [[_COMMUNITY__forward_transcription]]

## Top bridge nodes
- [[TestClaudeProxyHandler]] - degree 24, connects to 4 communities