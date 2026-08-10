---
type: community
cohesion: 0.18
members: 15
---

# _forward_transcription

**Cohesion:** 0.18 - loosely connected
**Members:** 15 nodes

## Members
- [[dot-__init__()_27]] - code - tests/test_claude_proxy_server.py
- [[dot-json()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_backend_error_returns_status()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_connection_error_returns_503()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_generic_exception_returns_500()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_post_audio_transcriptions_no_file()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_post_audio_transcriptions_success()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_success_returns_json()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_unknown_extension_defaults_to_wav()]] - code - tests/test_claude_proxy_server.py
- [[Forward a transcription request to the configured Whisper backend.]] - rationale - src/merged_agentic_swarm/proxy/claude_proxy_server.py
- [[Multipart POST without a file field → 400.]] - rationale - tests/test_claude_proxy_server.py
- [[Multipart audio POST → forwarded to Whisper backend → JSON response.]] - rationale - tests/test_claude_proxy_server.py
- [[TestForwardTranscription]] - code - tests/test_claude_proxy_server.py
- [[_FakeResp]] - code - tests/test_claude_proxy_server.py
- [[_forward_transcription()]] - code - src/merged_agentic_swarm/proxy/claude_proxy_server.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/_forward_transcription
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_claude_proxy_server.py]]
- 2 edges to [[_COMMUNITY_ClaudeProxyHandler]]
- 2 edges to [[_COMMUNITY_ProxyServerDaemon]]
- 2 edges to [[_COMMUNITY_TestClaudeProxyHandler]]

## Top bridge nodes
- [[_forward_transcription()]] - degree 9, connects to 2 communities
- [[_FakeResp]] - degree 8, connects to 2 communities
- [[TestForwardTranscription]] - degree 7, connects to 2 communities
- [[dot-test_post_audio_transcriptions_no_file()]] - degree 4, connects to 2 communities
- [[dot-test_post_audio_transcriptions_success()]] - degree 4, connects to 2 communities