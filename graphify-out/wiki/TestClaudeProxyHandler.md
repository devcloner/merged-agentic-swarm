# TestClaudeProxyHandler

> 33 nodes · cohesion 0.06

## Key Concepts

- **TestClaudeProxyHandler** (24 connections) — `tests/test_claude_proxy_server.py`
- **.test_empty_content_length()** (2 connections) — `tests/test_claude_proxy_server.py`
- **.test_fast_fallback_router_not_used_when_flag_unset()** (2 connections) — `tests/test_claude_proxy_server.py`
- **.test_fast_fallback_router_used_when_flag_set()** (2 connections) — `tests/test_claude_proxy_server.py`
- **.test_options_request()** (2 connections) — `tests/test_claude_proxy_server.py`
- **.test_post_chat_completions_openai_conversion()** (2 connections) — `tests/test_claude_proxy_server.py`
- **.test_post_json_body_within_limit_not_413()** (2 connections) — `tests/test_claude_proxy_server.py`
- **.test_post_oversized_audio_body_rejected_413()** (2 connections) — `tests/test_claude_proxy_server.py`
- **.test_post_oversized_json_body_rejected_413()** (2 connections) — `tests/test_claude_proxy_server.py`
- **.test_post_unsupported_endpoint()** (2 connections) — `tests/test_claude_proxy_server.py`
- **.test_post_v1_messages()** (2 connections) — `tests/test_claude_proxy_server.py`
- **.test_post_v1_messages_with_bearer_token()** (2 connections) — `tests/test_claude_proxy_server.py`
- **.test_post_v1_messages_with_wrong_token_returns_401()** (2 connections) — `tests/test_claude_proxy_server.py`
- **.test_post_v1_messages_without_token_returns_401()** (2 connections) — `tests/test_claude_proxy_server.py`
- **.test_status_endpoint_includes_per_key_metrics()** (2 connections) — `tests/test_claude_proxy_server.py`
- **#42: /status surfaces exhausted/cooldown/latency per provider.** (1 connections) — `tests/test_claude_proxy_server.py`
- **#35: a body over the JSON cap must be rejected before buffering.** (1 connections) — `tests/test_claude_proxy_server.py`
- **#35: a body under the cap still reaches normal processing (400 here).** (1 connections) — `tests/test_claude_proxy_server.py`
- **#35: audio multipart bodies have their own (higher) cap.** (1 connections) — `tests/test_claude_proxy_server.py`
- **#33: FAST_FALLBACK_ENABLED routes through the hedged router.** (1 connections) — `tests/test_claude_proxy_server.py`
- **#33: without the flag the proxy keeps using the fabric dispatch path.** (1 connections) — `tests/test_claude_proxy_server.py`
- **POST /v1/messages should return a response (simulation fallback).** (1 connections) — `tests/test_claude_proxy_server.py`
- **POST /v1/messages without an auth token → 401.** (1 connections) — `tests/test_claude_proxy_server.py`
- **POST /v1/messages with an invalid token → 401.** (1 connections) — `tests/test_claude_proxy_server.py`
- **POST /v1/messages authenticated via Authorization: Bearer → 200.** (1 connections) — `tests/test_claude_proxy_server.py`
- *... and 8 more nodes in this community*

## Relationships

- [ClaudeProxyHandler](ClaudeProxyHandler.md) (2 shared connections)
- [Ultracode Swarm Audit Fleet Manifest](Ultracode_Swarm_Audit_Fleet_Manifest.md) (2 shared connections)
- [TestLitellmPresenceInRoutes](TestLitellmPresenceInRoutes.md) (1 shared connections)
- [test_agentic_cli.py](test_agentic_cli.py.md) (1 shared connections)

## Source Files

- `tests/test_claude_proxy_server.py`

## Audit Trail

- EXTRACTED: 69 (99%)
- INFERRED: 1 (1%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*