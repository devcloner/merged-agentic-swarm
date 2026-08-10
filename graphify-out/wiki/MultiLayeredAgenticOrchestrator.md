# MultiLayeredAgenticOrchestrator

> 15 nodes · cohesion 0.21

## Key Concepts

- **ClaudeProxyHandler** (11 connections) — `src/merged_agentic_swarm/proxy/claude_proxy_server.py`
- **.do_POST()** (6 connections) — `src/merged_agentic_swarm/proxy/claude_proxy_server.py`
- **.send_json_response()** (6 connections) — `src/merged_agentic_swarm/proxy/claude_proxy_server.py`
- **._handle_audio_transcription()** (5 connections) — `src/merged_agentic_swarm/proxy/claude_proxy_server.py`
- **._authorized()** (4 connections) — `src/merged_agentic_swarm/proxy/claude_proxy_server.py`
- **_proxy_dispatch()** (4 connections) — `src/merged_agentic_swarm/proxy/claude_proxy_server.py`
- **._send_413()** (3 connections) — `src/merged_agentic_swarm/proxy/claude_proxy_server.py`
- **Any** (3 connections)
- **.do_GET()** (2 connections) — `src/merged_agentic_swarm/proxy/claude_proxy_server.py`
- **BaseHTTPRequestHandler** (1 connections)
- **.do_OPTIONS()** (1 connections) — `src/merged_agentic_swarm/proxy/claude_proxy_server.py`
- **.log_message()** (1 connections) — `src/merged_agentic_swarm/proxy/claude_proxy_server.py`
- **Reject an oversized body. Close the connection since the unread bytes would…** (1 connections) — `src/merged_agentic_swarm/proxy/claude_proxy_server.py`
- **Enforce the inbound proxy token (ANTHROPIC_AUTH_TOKEN, default 'freecc').…** (1 connections) — `src/merged_agentic_swarm/proxy/claude_proxy_server.py`
- **Route a request through the hedged fast-fallback router when enabled. Both…** (1 connections) — `src/merged_agentic_swarm/proxy/claude_proxy_server.py`

## Relationships

- [services/__init__.py](services-__init__.py.md) (2 shared connections)
- [test_agentic_cli.py](test_agentic_cli.py.md) (2 shared connections)
- [TestLitellmPresenceInRoutes](TestLitellmPresenceInRoutes.md) (1 shared connections)
- [Ultracode Swarm Audit Fleet Manifest](Ultracode_Swarm_Audit_Fleet_Manifest.md) (1 shared connections)

## Source Files

- `src/merged_agentic_swarm/proxy/claude_proxy_server.py`

## Audit Trail

- EXTRACTED: 50 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*