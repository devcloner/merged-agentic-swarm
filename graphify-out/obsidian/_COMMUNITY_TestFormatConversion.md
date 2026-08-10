---
type: community
cohesion: 0.13
members: 15
---

# TestFormatConversion

**Cohesion:** 0.13 - loosely connected
**Members:** 15 nodes

## Members
- [[dot-setup_method()_11]] - code - tests/test_multi_provider_fabric.py
- [[dot-test_extract_anthropic_tool_calls()]] - code - tests/test_multi_provider_fabric.py
- [[dot-test_format_anthropic_to_anthropic_tool_blocks()]] - code - tests/test_multi_provider_fabric.py
- [[dot-test_format_anthropic_to_openai_no_system()]] - code - tests/test_multi_provider_fabric.py
- [[dot-test_format_anthropic_to_openai_with_system()]] - code - tests/test_multi_provider_fabric.py
- [[dot-test_format_anthropic_tool_calls_roundtrip()]] - code - tests/test_multi_provider_fabric.py
- [[dot-test_format_openai_bad_arguments_json()]] - code - tests/test_multi_provider_fabric.py
- [[dot-test_format_openai_empty_choices()]] - code - tests/test_multi_provider_fabric.py
- [[dot-test_format_openai_to_anthropic()]] - code - tests/test_multi_provider_fabric.py
- [[dot-test_format_openai_with_tool_calls()]] - code - tests/test_multi_provider_fabric.py
- [[dot-test_format_with_content_blocks()]] - code - tests/test_multi_provider_fabric.py
- [[dot-test_tools_to_anthropic_conversion()]] - code - tests/test_multi_provider_fabric.py
- [[TestFormatConversion]] - code - tests/test_multi_provider_fabric.py
- [[format_anthropic_to_anthropic builds tool_use + tool_result blocks for…]] - rationale - tests/test_multi_provider_fabric.py
- [[format_anthropic_to_openai converts normalized tool_calls to OpenAI shape.]] - rationale - tests/test_multi_provider_fabric.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/TestFormatConversion
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_MultiProviderFabric]]
- 1 edge to [[_COMMUNITY_KeyPoolManager]]
- 1 edge to [[_COMMUNITY_test_multi_provider_fabric.py]]

## Top bridge nodes
- [[TestFormatConversion]] - degree 15, connects to 3 communities
- [[dot-setup_method()_11]] - degree 2, connects to 1 community