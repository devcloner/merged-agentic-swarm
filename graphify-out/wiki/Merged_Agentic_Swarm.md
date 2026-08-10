# Merged Agentic Swarm

> 11 nodes · cohesion 0.22

## Key Concepts

- **StreamingProxyConfig** (8 connections) — `src/merged_agentic_swarm/streaming_proxy.py`
- **streaming_proxy.py** (7 connections) — `src/merged_agentic_swarm/streaming_proxy.py`
- **create_streaming_proxy_app()** (7 connections) — `src/merged_agentic_swarm/streaming_proxy.py`
- **.as_asgi_app()** (4 connections) — `src/merged_agentic_swarm/streaming_proxy.py`
- **Starlette** (2 connections)
- **test_config_defaults()** (2 connections) — `tests/test_streaming_proxy.py`
- **test_create_streaming_proxy_app_factory()** (2 connections) — `tests/test_streaming_proxy.py`
- **Zero-buffering streaming passthrough proxy for Anthropic Messages API. Accepts…** (1 connections) — `src/merged_agentic_swarm/streaming_proxy.py`
- **Return a standalone Starlette ASGI application.** (1 connections) — `src/merged_agentic_swarm/streaming_proxy.py`
- **Create a configured streaming proxy Starlette app in one call.** (1 connections) — `src/merged_agentic_swarm/streaming_proxy.py`
- **Configuration for the zero-buffering streaming proxy.** (1 connections) — `src/merged_agentic_swarm/streaming_proxy.py`

## Relationships

- [cmd_config](cmd_config.md) (5 shared connections)
- [TestDispatchRequest](TestDispatchRequest.md) (3 shared connections)
- [_forward_transcription](_forward_transcription.md) (2 shared connections)
- [package.json](package.json.md) (1 shared connections)
- [load_durable_agents.sh](load_durable_agents.sh.md) (1 shared connections)

## Source Files

- `src/merged_agentic_swarm/streaming_proxy.py`
- `tests/test_streaming_proxy.py`

## Audit Trail

- EXTRACTED: 34 (94%)
- INFERRED: 2 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*