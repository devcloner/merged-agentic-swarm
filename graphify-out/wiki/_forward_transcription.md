# _forward_transcription

> 14 nodes · cohesion 0.14

## Key Concepts

- **CircuitBreaker** (11 connections) — `src/merged_agentic_swarm/streaming_proxy.py`
- **.__init__()** (4 connections) — `src/merged_agentic_swarm/streaming_proxy.py`
- **.record_failure()** (3 connections) — `src/merged_agentic_swarm/streaming_proxy.py`
- **.record_success()** (3 connections) — `src/merged_agentic_swarm/streaming_proxy.py`
- **test_circuit_breaker_unit_transitions()** (3 connections) — `tests/test_streaming_proxy.py`
- **.failure_count()** (2 connections) — `src/merged_agentic_swarm/streaming_proxy.py`
- **.is_open()** (2 connections) — `src/merged_agentic_swarm/streaming_proxy.py`
- **.__init__()** (1 connections) — `src/merged_agentic_swarm/streaming_proxy.py`
- **AsyncBaseTransport** (1 connections)
- **Simple fail-fast circuit breaker. Tracks consecutive failures. After…** (1 connections) — `src/merged_agentic_swarm/streaming_proxy.py`
- **True when the circuit is open (requests should be rejected).** (1 connections) — `src/merged_agentic_swarm/streaming_proxy.py`
- **Current consecutive failure count.** (1 connections) — `src/merged_agentic_swarm/streaming_proxy.py`
- **Reset the failure counter after a successful request.** (1 connections) — `src/merged_agentic_swarm/streaming_proxy.py`
- **Increment the failure counter; open circuit if threshold reached.** (1 connections) — `src/merged_agentic_swarm/streaming_proxy.py`

## Relationships

- [TestDispatchRequest](TestDispatchRequest.md) (3 shared connections)
- [Merged Agentic Swarm](Merged_Agentic_Swarm.md) (2 shared connections)
- [cmd_config](cmd_config.md) (2 shared connections)
- [package.json](package.json.md) (1 shared connections)
- [load_durable_agents.sh](load_durable_agents.sh.md) (1 shared connections)

## Source Files

- `src/merged_agentic_swarm/streaming_proxy.py`
- `tests/test_streaming_proxy.py`

## Audit Trail

- EXTRACTED: 33 (94%)
- INFERRED: 2 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*