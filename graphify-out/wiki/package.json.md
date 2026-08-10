# package.json

> 7 nodes · cohesion 0.29

## Key Concepts

- **_ChunkStream** (9 connections) — `tests/test_streaming_proxy.py`
- **_sse_response()** (3 connections) — `tests/test_streaming_proxy.py`
- **.aclose()** (1 connections) — `tests/test_streaming_proxy.py`
- **.__aiter__()** (1 connections) — `tests/test_streaming_proxy.py`
- **.__init__()** (1 connections) — `tests/test_streaming_proxy.py`
- **Async byte stream over a fixed list of chunks. Optionally raises ``exc`` after…** (1 connections) — `tests/test_streaming_proxy.py`
- **Build an upstream ``httpx.Response`` that streams ``chunks`` as SSE.** (1 connections) — `tests/test_streaming_proxy.py`

## Relationships

- [cmd_config](cmd_config.md) (2 shared connections)
- [Merged Agentic Swarm](Merged_Agentic_Swarm.md) (1 shared connections)
- [_forward_transcription](_forward_transcription.md) (1 shared connections)
- [TestDispatchRequest](TestDispatchRequest.md) (1 shared connections)

## Source Files

- `tests/test_streaming_proxy.py`

## Audit Trail

- EXTRACTED: 14 (82%)
- INFERRED: 3 (18%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*