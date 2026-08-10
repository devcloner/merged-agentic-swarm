---
type: community
cohesion: 0.18
members: 16
---

# claude_proxy_server.py

**Cohesion:** 0.18 - loosely connected
**Members:** 16 nodes

## Members
- [[dot-test_default_model_when_no_model_field()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_missing_boundary()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_no_file_field()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_parses_file_and_model()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_post_audio_transcriptions_backend_down()]] - code - tests/test_claude_proxy_server.py
- [[Backend connection failure → 503 with unavailable message.]] - rationale - tests/test_claude_proxy_server.py
- [[Claude API Key Pool Proxy Server Exposes Anthropic-compatible, OpenAI-…]] - rationale - src/merged_agentic_swarm/proxy/claude_proxy_server.py
- [[Proxy Package Initialization]] - rationale - src/merged_agentic_swarm/proxy/__init__.py
- [[Return (file_bytes, file_name, model_name) from a multipart body.]] - rationale - src/merged_agentic_swarm/proxy/claude_proxy_server.py
- [[TestParseMultipart]] - code - tests/test_claude_proxy_server.py
- [[Tests for proxyclaude_proxy_server.py Coverage ClaudeProxyHandler (do_GET,…]] - rationale - tests/test_claude_proxy_server.py
- [[_multipart_body()]] - code - tests/test_claude_proxy_server.py
- [[_parse_multipart()]] - code - src/merged_agentic_swarm/proxy/claude_proxy_server.py
- [[claude_proxy_server.py]] - code - src/merged_agentic_swarm/proxy/claude_proxy_server.py
- [[proxy__init__.py]] - code - src/merged_agentic_swarm/proxy/__init__.py
- [[test_claude_proxy_server.py]] - code - tests/test_claude_proxy_server.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/claude_proxy_serverpy
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_ProxyServerDaemon]]
- 5 edges to [[_COMMUNITY__forward_transcription]]
- 4 edges to [[_COMMUNITY_ClaudeProxyHandler]]
- 3 edges to [[_COMMUNITY_multi_provider_fabric.py]]
- 2 edges to [[_COMMUNITY_TestClaudeProxyHandler]]
- 1 edge to [[_COMMUNITY_FastFallbackRouter]]
- 1 edge to [[_COMMUNITY_APIKeyInfo]]
- 1 edge to [[_COMMUNITY_WorkerRole]]

## Top bridge nodes
- [[claude_proxy_server.py]] - degree 15, connects to 7 communities
- [[test_claude_proxy_server.py]] - degree 9, connects to 3 communities
- [[proxy__init__.py]] - degree 5, connects to 2 communities
- [[_parse_multipart()]] - degree 7, connects to 1 community
- [[_multipart_body()]] - degree 6, connects to 1 community