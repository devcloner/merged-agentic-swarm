---
type: community
cohesion: 0.15
members: 23
---

# MultiProviderFabric

**Cohesion:** 0.15 - loosely connected
**Members:** 23 nodes

## Members
- [[dot-__init__()_6]] - code - src/merged_agentic_swarm/providers/multi_provider_fabric.py
- [[dot-_build_route_list()]] - code - src/merged_agentic_swarm/providers/multi_provider_fabric.py
- [[dot-_content_to_anthropic_blocks()]] - code - src/merged_agentic_swarm/providers/multi_provider_fabric.py
- [[dot-_extract_anthropic_tool_calls()]] - code - src/merged_agentic_swarm/providers/multi_provider_fabric.py
- [[dot-_flatten_content_to_text()]] - code - src/merged_agentic_swarm/providers/multi_provider_fabric.py
- [[dot-_tools_to_anthropic()]] - code - src/merged_agentic_swarm/providers/multi_provider_fabric.py
- [[dot-dispatch_request()]] - code - src/merged_agentic_swarm/providers/multi_provider_fabric.py
- [[dot-format_anthropic_to_anthropic()]] - code - src/merged_agentic_swarm/providers/multi_provider_fabric.py
- [[dot-format_anthropic_to_openai()]] - code - src/merged_agentic_swarm/providers/multi_provider_fabric.py
- [[dot-format_openai_to_anthropic_response()]] - code - src/merged_agentic_swarm/providers/multi_provider_fabric.py
- [[Any_9]] - code
- [[Build route list, promoting the last successful provider for this alias to the…]] - rationale - src/merged_agentic_swarm/providers/multi_provider_fabric.py
- [[Convert OpenAI function-tool schemas to Anthropic ``tools`` payload entries.]] - rationale - src/merged_agentic_swarm/providers/multi_provider_fabric.py
- [[Convert normalized messages (Anthropic-shaped) to OpenAI Chat Completions…]] - rationale - src/merged_agentic_swarm/providers/multi_provider_fabric.py
- [[Convert normalized messages to Anthropic Messages API format. Used for…]] - rationale - src/merged_agentic_swarm/providers/multi_provider_fabric.py
- [[Converts OpenAI response payload to Anthropic messages payload format.]] - rationale - src/merged_agentic_swarm/providers/multi_provider_fabric.py
- [[Dispatches request across multi-backend provider fallback cascade. ``tools`` is…]] - rationale - src/merged_agentic_swarm/providers/multi_provider_fabric.py
- [[Extract normalized tool calls from an Anthropic-format response's content…]] - rationale - src/merged_agentic_swarm/providers/multi_provider_fabric.py
- [[Flatten Anthropic content blocks (or plain text) into a single text string.]] - rationale - src/merged_agentic_swarm/providers/multi_provider_fabric.py
- [[Load the per-alias route overlay (cached); {} when missing or unreadable.]] - rationale - src/merged_agentic_swarm/providers/multi_provider_fabric.py
- [[MultiProviderFabric]] - code - src/merged_agentic_swarm/providers/multi_provider_fabric.py
- [[Normalize a content value into a list of Anthropic content blocks.]] - rationale - src/merged_agentic_swarm/providers/multi_provider_fabric.py
- [[_load_fabric_routes_overlay()]] - code - src/merged_agentic_swarm/providers/multi_provider_fabric.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/MultiProviderFabric
SORT file.name ASC
```

## Connections to other communities
- 9 edges to [[_COMMUNITY_TestDispatchRequest]]
- 7 edges to [[_COMMUNITY__router_with_keys]]
- 4 edges to [[_COMMUNITY_FastFallbackConfig]]
- 4 edges to [[_COMMUNITY__record_failure]]
- 3 edges to [[_COMMUNITY_multi_provider_fabric.py]]
- 3 edges to [[_COMMUNITY_FastFallbackRouter]]
- 3 edges to [[_COMMUNITY_test_multi_provider_fabric.py]]
- 2 edges to [[_COMMUNITY_TestFormatConversion]]
- 1 edge to [[_COMMUNITY_APIKeyInfo]]
- 1 edge to [[_COMMUNITY_conftest.py]]
- 1 edge to [[_COMMUNITY_TestBanPersistence]]
- 1 edge to [[_COMMUNITY_TestLitellmPresenceInRoutes]]
- 1 edge to [[_COMMUNITY_TestMalformedOverlayRoutes]]

## Top bridge nodes
- [[MultiProviderFabric]] - degree 47, connects to 13 communities
- [[dot-dispatch_request()]] - degree 11, connects to 1 community
- [[_load_fabric_routes_overlay()]] - degree 4, connects to 1 community