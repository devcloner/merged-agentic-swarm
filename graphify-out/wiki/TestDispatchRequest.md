# TestDispatchRequest

> 20 nodes · cohesion 0.15

## Key Concepts

- **PassthroughStreamingProxy** (16 connections) — `src/merged_agentic_swarm/streaming_proxy.py`
- **.proxy_request()** (8 connections) — `src/merged_agentic_swarm/streaming_proxy.py`
- **._get_client()** (6 connections) — `src/merged_agentic_swarm/streaming_proxy.py`
- **._handle_health()** (4 connections) — `src/merged_agentic_swarm/streaming_proxy.py`
- **._handle_messages()** (4 connections) — `src/merged_agentic_swarm/streaming_proxy.py`
- **.health()** (4 connections) — `src/merged_agentic_swarm/streaming_proxy.py`
- **.prewarm()** (3 connections) — `src/merged_agentic_swarm/streaming_proxy.py`
- **.router()** (3 connections) — `src/merged_agentic_swarm/streaming_proxy.py`
- **Request** (3 connections)
- **Response** (3 connections)
- **Route** (2 connections)
- **.close()** (2 connections) — `src/merged_agentic_swarm/streaming_proxy.py`
- **AsyncClient** (1 connections)
- **Zero-buffering SSE passthrough proxy. Accepts Anthropic Messages API streaming…** (1 connections) — `src/merged_agentic_swarm/streaming_proxy.py`
- **Return the shared httpx client, creating it if needed.** (1 connections) — `src/merged_agentic_swarm/streaming_proxy.py`
- **Close the underlying httpx client and release connections.** (1 connections) — `src/merged_agentic_swarm/streaming_proxy.py`
- **Pre-establish connections to the upstream. Sends a health-check request to warm…** (1 connections) — `src/merged_agentic_swarm/streaming_proxy.py`
- **Check upstream health. Returns a status dict.** (1 connections) — `src/merged_agentic_swarm/streaming_proxy.py`
- **Forward an incoming streaming request to upstream. Reads the request body,…** (1 connections) — `src/merged_agentic_swarm/streaming_proxy.py`
- **Return Starlette routes for this proxy. Mount these into a parent Starlette app…** (1 connections) — `src/merged_agentic_swarm/streaming_proxy.py`

## Relationships

- [Merged Agentic Swarm](Merged_Agentic_Swarm.md) (3 shared connections)
- [_forward_transcription](_forward_transcription.md) (3 shared connections)
- [_make_learning_entry](_make_learning_entry.md) (1 shared connections)
- [package.json](package.json.md) (1 shared connections)
- [cmd_config](cmd_config.md) (1 shared connections)
- [load_durable_agents.sh](load_durable_agents.sh.md) (1 shared connections)

## Source Files

- `src/merged_agentic_swarm/streaming_proxy.py`

## Audit Trail

- EXTRACTED: 63 (95%)
- INFERRED: 3 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*