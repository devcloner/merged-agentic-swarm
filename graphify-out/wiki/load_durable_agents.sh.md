# load_durable_agents.sh

> 7 nodes · cohesion 0.29

## Key Concepts

- **_StallStream** (8 connections) — `tests/test_streaming_proxy.py`
- **drain()** (5 connections) — `tests/test_streaming_proxy.py`
- **.aclose()** (4 connections) — `tests/test_streaming_proxy.py`
- **Consume (or close) a StreamingResponse so upstream streams are torn down.** (1 connections) — `tests/test_streaming_proxy.py`
- **Async byte stream that never yields (simulates a stalled upstream).** (1 connections) — `tests/test_streaming_proxy.py`
- **.__aiter__()** (1 connections) — `tests/test_streaming_proxy.py`
- **.__init__()** (1 connections) — `tests/test_streaming_proxy.py`

## Relationships

- [cmd_config](cmd_config.md) (6 shared connections)
- [Merged Agentic Swarm](Merged_Agentic_Swarm.md) (1 shared connections)
- [_forward_transcription](_forward_transcription.md) (1 shared connections)
- [TestDispatchRequest](TestDispatchRequest.md) (1 shared connections)

## Source Files

- `tests/test_streaming_proxy.py`

## Audit Trail

- EXTRACTED: 18 (86%)
- INFERRED: 3 (14%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*