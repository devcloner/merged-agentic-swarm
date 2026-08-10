# test_health_check.py

> 21 nodes · cohesion 0.14

## Key Concepts

- **.dispatch_request()** (11 connections) — `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- **Any** (9 connections)
- **.format_anthropic_to_anthropic()** (6 connections) — `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- **._flatten_content_to_text()** (5 connections) — `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- **.format_anthropic_to_openai()** (5 connections) — `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- **_load_fabric_routes_overlay()** (4 connections) — `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- **._build_route_list()** (4 connections) — `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- **._content_to_anthropic_blocks()** (4 connections) — `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- **._extract_anthropic_tool_calls()** (4 connections) — `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- **.format_openai_to_anthropic_response()** (4 connections) — `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- **._tools_to_anthropic()** (4 connections) — `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- **Load the per-alias route overlay (cached); {} when missing or unreadable.** (1 connections) — `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- **Flatten Anthropic content blocks (or plain text) into a single text string.** (1 connections) — `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- **Convert normalized messages (Anthropic-shaped) to OpenAI Chat Completions…** (1 connections) — `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- **Normalize a content value into a list of Anthropic content blocks.** (1 connections) — `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- **Convert normalized messages to Anthropic Messages API format. Used for…** (1 connections) — `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- **Convert OpenAI function-tool schemas to Anthropic ``tools`` payload entries.** (1 connections) — `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- **Extract normalized tool calls from an Anthropic-format response's content…** (1 connections) — `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- **Converts OpenAI response payload to Anthropic messages payload format.** (1 connections) — `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- **Build route list, promoting the last successful provider for this alias to the…** (1 connections) — `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- **Dispatches request across multi-backend provider fallback cascade. ``tools`` is…** (1 connections) — `src/merged_agentic_swarm/providers/multi_provider_fabric.py`

## Relationships

- [MultiProviderFabric](MultiProviderFabric.md) (9 shared connections)
- [services/__init__.py](services-__init__.py.md) (3 shared connections)

## Source Files

- `src/merged_agentic_swarm/providers/multi_provider_fabric.py`

## Audit Trail

- EXTRACTED: 70 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*