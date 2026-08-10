---
type: community
cohesion: 0.23
members: 12
---

# _parse_multipart

**Cohesion:** 0.23 - loosely connected
**Members:** 12 nodes

## Members
- [[dot-test_default_model_when_no_model_field()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_missing_boundary()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_no_file_field()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_parses_file_and_model()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_post_audio_transcriptions_backend_down()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_post_audio_transcriptions_no_file()]] - code - tests/test_claude_proxy_server.py
- [[Backend connection failure → 503 with unavailable message.]] - rationale - tests/test_claude_proxy_server.py
- [[Multipart POST without a file field → 400.]] - rationale - tests/test_claude_proxy_server.py
- [[Return (file_bytes, file_name, model_name) from a multipart body.]] - rationale - src/merged_agentic_swarm/proxy/claude_proxy_server.py
- [[TestParseMultipart]] - code - tests/test_claude_proxy_server.py
- [[_multipart_body()]] - code - tests/test_claude_proxy_server.py
- [[_parse_multipart()]] - code - src/merged_agentic_swarm/proxy/claude_proxy_server.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/_parse_multipart
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_test_claude_proxy_server.py]]
- 2 edges to [[_COMMUNITY__forward_transcription]]
- 2 edges to [[_COMMUNITY_TestClaudeProxyHandler]]
- 1 edge to [[_COMMUNITY_multi_provider_fabric.py]]
- 1 edge to [[_COMMUNITY_ClaudeProxyHandler]]
- 1 edge to [[_COMMUNITY_ProxyServerDaemon]]

## Top bridge nodes
- [[_parse_multipart()]] - degree 7, connects to 2 communities
- [[_multipart_body()]] - degree 6, connects to 2 communities
- [[TestParseMultipart]] - degree 6, connects to 2 communities
- [[dot-test_post_audio_transcriptions_no_file()]] - degree 4, connects to 2 communities
- [[dot-test_post_audio_transcriptions_backend_down()]] - degree 3, connects to 1 community