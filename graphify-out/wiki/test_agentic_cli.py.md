# test_agentic_cli.py

> 13 nodes · cohesion 0.22

## Key Concepts

- **_forward_transcription()** (9 connections) — `src/merged_agentic_swarm/proxy/claude_proxy_server.py`
- **_FakeResp** (8 connections) — `tests/test_claude_proxy_server.py`
- **TestForwardTranscription** (7 connections) — `tests/test_claude_proxy_server.py`
- **.test_post_audio_transcriptions_success()** (4 connections) — `tests/test_claude_proxy_server.py`
- **.test_backend_error_returns_status()** (3 connections) — `tests/test_claude_proxy_server.py`
- **.test_success_returns_json()** (3 connections) — `tests/test_claude_proxy_server.py`
- **.test_connection_error_returns_503()** (2 connections) — `tests/test_claude_proxy_server.py`
- **.test_generic_exception_returns_500()** (2 connections) — `tests/test_claude_proxy_server.py`
- **.test_unknown_extension_defaults_to_wav()** (2 connections) — `tests/test_claude_proxy_server.py`
- **Forward a transcription request to the configured Whisper backend.** (1 connections) — `src/merged_agentic_swarm/proxy/claude_proxy_server.py`
- **.__init__()** (1 connections) — `tests/test_claude_proxy_server.py`
- **.json()** (1 connections) — `tests/test_claude_proxy_server.py`
- **Multipart audio POST → forwarded to Whisper backend → JSON response.** (1 connections) — `tests/test_claude_proxy_server.py`

## Relationships

- [MultiLayeredAgenticOrchestrator](MultiLayeredAgenticOrchestrator.md) (2 shared connections)
- [ClaudeProxyHandler](ClaudeProxyHandler.md) (2 shared connections)
- [TestLitellmPresenceInRoutes](TestLitellmPresenceInRoutes.md) (2 shared connections)
- [Ultracode Swarm Audit Fleet Manifest](Ultracode_Swarm_Audit_Fleet_Manifest.md) (2 shared connections)
- [services/__init__.py](services-__init__.py.md) (1 shared connections)
- [TestClaudeProxyHandler](TestClaudeProxyHandler.md) (1 shared connections)

## Source Files

- `src/merged_agentic_swarm/proxy/claude_proxy_server.py`
- `tests/test_claude_proxy_server.py`

## Audit Trail

- EXTRACTED: 42 (95%)
- INFERRED: 2 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*