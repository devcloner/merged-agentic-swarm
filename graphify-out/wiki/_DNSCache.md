# _DNSCache

> 8 nodes · cohesion 0.25

## Key Concepts

- **test_check_streaming_fcc_happy_path()** (6 connections) — `tests/test_health_check.py`
- **test_check_streaming_routatic_endpoint()** (6 connections) — `tests/test_health_check.py`
- **_sse_event()** (5 connections) — `tests/test_health_check.py`
- **test_main_stream_subcommand()** (5 connections) — `tests/test_health_check.py`
- **Build a single SSE data line for an Anthropic streaming content-block-delta.** (1 connections) — `tests/test_health_check.py`
- **check_streaming through FCC endpoint measures TTFB and total latency.** (1 connections) — `tests/test_health_check.py`
- **check_streaming targets routatic-proxy when endpoint='routatic'.** (1 connections) — `tests/test_health_check.py`
- **stream' subcommand runs only the streaming check.** (1 connections) — `tests/test_health_check.py`

## Relationships

- [DurableAgentFactory](DurableAgentFactory.md) (7 shared connections)
- [Graphify Knowledge Graph Pipeline](Graphify_Knowledge_Graph_Pipeline.md) (4 shared connections)
- [HopResult](HopResult.md) (1 shared connections)

## Source Files

- `tests/test_health_check.py`

## Audit Trail

- EXTRACTED: 26 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*