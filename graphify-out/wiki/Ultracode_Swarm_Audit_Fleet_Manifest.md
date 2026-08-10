# Ultracode Swarm Audit Fleet Manifest

> 12 nodes · cohesion 0.23

## Key Concepts

- **_parse_multipart()** (7 connections) — `src/merged_agentic_swarm/proxy/claude_proxy_server.py`
- **_multipart_body()** (6 connections) — `tests/test_claude_proxy_server.py`
- **TestParseMultipart** (6 connections) — `tests/test_claude_proxy_server.py`
- **.test_post_audio_transcriptions_no_file()** (4 connections) — `tests/test_claude_proxy_server.py`
- **.test_post_audio_transcriptions_backend_down()** (3 connections) — `tests/test_claude_proxy_server.py`
- **.test_no_file_field()** (3 connections) — `tests/test_claude_proxy_server.py`
- **.test_parses_file_and_model()** (3 connections) — `tests/test_claude_proxy_server.py`
- **.test_default_model_when_no_model_field()** (2 connections) — `tests/test_claude_proxy_server.py`
- **.test_missing_boundary()** (2 connections) — `tests/test_claude_proxy_server.py`
- **Return (file_bytes, file_name, model_name) from a multipart body.** (1 connections) — `src/merged_agentic_swarm/proxy/claude_proxy_server.py`
- **Multipart POST without a file field → 400.** (1 connections) — `tests/test_claude_proxy_server.py`
- **Backend connection failure → 503 with unavailable message.** (1 connections) — `tests/test_claude_proxy_server.py`

## Relationships

- [TestLitellmPresenceInRoutes](TestLitellmPresenceInRoutes.md) (2 shared connections)
- [test_agentic_cli.py](test_agentic_cli.py.md) (2 shared connections)
- [TestClaudeProxyHandler](TestClaudeProxyHandler.md) (2 shared connections)
- [services/__init__.py](services-__init__.py.md) (1 shared connections)
- [MultiLayeredAgenticOrchestrator](MultiLayeredAgenticOrchestrator.md) (1 shared connections)
- [ClaudeProxyHandler](ClaudeProxyHandler.md) (1 shared connections)

## Source Files

- `src/merged_agentic_swarm/proxy/claude_proxy_server.py`
- `tests/test_claude_proxy_server.py`

## Audit Trail

- EXTRACTED: 38 (97%)
- INFERRED: 1 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*