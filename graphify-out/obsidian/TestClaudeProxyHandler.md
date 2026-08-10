---
source_file: "tests/test_claude_proxy_server.py"
type: "code"
community: "TestClaudeProxyHandler"
location: "L150"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/TestClaudeProxyHandler
---

# TestClaudeProxyHandler

## Connections
- [[dot-setup_server()]] - `method` [EXTRACTED]
- [[dot-test_empty_content_length()]] - `method` [EXTRACTED]
- [[dot-test_fast_fallback_router_not_used_when_flag_unset()]] - `method` [EXTRACTED]
- [[dot-test_fast_fallback_router_used_when_flag_set()]] - `method` [EXTRACTED]
- [[dot-test_get_unknown_endpoint_returns_404()]] - `method` [EXTRACTED]
- [[dot-test_health_endpoint()]] - `method` [EXTRACTED]
- [[dot-test_options_request()]] - `method` [EXTRACTED]
- [[dot-test_post_audio_transcriptions_backend_down()]] - `method` [EXTRACTED]
- [[dot-test_post_audio_transcriptions_no_file()]] - `method` [EXTRACTED]
- [[dot-test_post_audio_transcriptions_success()]] - `method` [EXTRACTED]
- [[dot-test_post_chat_completions_openai_conversion()]] - `method` [EXTRACTED]
- [[dot-test_post_chat_completions_with_invalid_json()]] - `method` [EXTRACTED]
- [[dot-test_post_json_body_within_limit_not_413()]] - `method` [EXTRACTED]
- [[dot-test_post_oversized_audio_body_rejected_413()]] - `method` [EXTRACTED]
- [[dot-test_post_oversized_json_body_rejected_413()]] - `method` [EXTRACTED]
- [[dot-test_post_unsupported_endpoint()]] - `method` [EXTRACTED]
- [[dot-test_post_v1_messages()]] - `method` [EXTRACTED]
- [[dot-test_post_v1_messages_with_bearer_token()]] - `method` [EXTRACTED]
- [[dot-test_post_v1_messages_with_wrong_token_returns_401()]] - `method` [EXTRACTED]
- [[dot-test_post_v1_messages_without_token_returns_401()]] - `method` [EXTRACTED]
- [[dot-test_status_endpoint()]] - `method` [EXTRACTED]
- [[dot-test_status_endpoint_includes_per_key_metrics()]] - `method` [EXTRACTED]
- [[ProxyServerDaemon]] - `uses` [INFERRED]
- [[test_claude_proxy_server.py]] - `contains` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/TestClaudeProxyHandler