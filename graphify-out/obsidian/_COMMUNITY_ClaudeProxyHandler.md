---
type: community
cohesion: 0.21
members: 15
---

# ClaudeProxyHandler

**Cohesion:** 0.21 - loosely connected
**Members:** 15 nodes

## Members
- [[dot-_authorized()]] - code - src/merged_agentic_swarm/proxy/claude_proxy_server.py
- [[dot-_handle_audio_transcription()]] - code - src/merged_agentic_swarm/proxy/claude_proxy_server.py
- [[dot-_send_413()]] - code - src/merged_agentic_swarm/proxy/claude_proxy_server.py
- [[dot-do_GET()]] - code - src/merged_agentic_swarm/proxy/claude_proxy_server.py
- [[dot-do_OPTIONS()]] - code - src/merged_agentic_swarm/proxy/claude_proxy_server.py
- [[dot-do_POST()]] - code - src/merged_agentic_swarm/proxy/claude_proxy_server.py
- [[dot-log_message()]] - code - src/merged_agentic_swarm/proxy/claude_proxy_server.py
- [[dot-send_json_response()]] - code - src/merged_agentic_swarm/proxy/claude_proxy_server.py
- [[Any_10]] - code
- [[BaseHTTPRequestHandler]] - code
- [[ClaudeProxyHandler]] - code - src/merged_agentic_swarm/proxy/claude_proxy_server.py
- [[Enforce the inbound proxy token (ANTHROPIC_AUTH_TOKEN, default 'freecc').…]] - rationale - src/merged_agentic_swarm/proxy/claude_proxy_server.py
- [[Reject an oversized body. Close the connection since the unread bytes would…]] - rationale - src/merged_agentic_swarm/proxy/claude_proxy_server.py
- [[Route a request through the hedged fast-fallback router when enabled. Both…]] - rationale - src/merged_agentic_swarm/proxy/claude_proxy_server.py
- [[_proxy_dispatch()]] - code - src/merged_agentic_swarm/proxy/claude_proxy_server.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ClaudeProxyHandler
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_claude_proxy_server.py]]
- 2 edges to [[_COMMUNITY__forward_transcription]]

## Top bridge nodes
- [[dot-_handle_audio_transcription()]] - degree 5, connects to 2 communities
- [[ClaudeProxyHandler]] - degree 11, connects to 1 community
- [[_proxy_dispatch()]] - degree 4, connects to 1 community
- [[Any_10]] - degree 3, connects to 1 community