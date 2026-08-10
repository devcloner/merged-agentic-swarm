# .get_available_worker

> 15 nodes · cohesion 0.13

## Key Concepts

- **TestFormatConversion** (15 connections) — `tests/test_multi_provider_fabric.py`
- **.setup_method()** (2 connections) — `tests/test_multi_provider_fabric.py`
- **.test_format_anthropic_to_anthropic_tool_blocks()** (2 connections) — `tests/test_multi_provider_fabric.py`
- **.test_format_anthropic_tool_calls_roundtrip()** (2 connections) — `tests/test_multi_provider_fabric.py`
- **format_anthropic_to_openai converts normalized tool_calls to OpenAI shape.** (1 connections) — `tests/test_multi_provider_fabric.py`
- **format_anthropic_to_anthropic builds tool_use + tool_result blocks for…** (1 connections) — `tests/test_multi_provider_fabric.py`
- **.test_extract_anthropic_tool_calls()** (1 connections) — `tests/test_multi_provider_fabric.py`
- **.test_format_anthropic_to_openai_no_system()** (1 connections) — `tests/test_multi_provider_fabric.py`
- **.test_format_anthropic_to_openai_with_system()** (1 connections) — `tests/test_multi_provider_fabric.py`
- **.test_format_openai_bad_arguments_json()** (1 connections) — `tests/test_multi_provider_fabric.py`
- **.test_format_openai_empty_choices()** (1 connections) — `tests/test_multi_provider_fabric.py`
- **.test_format_openai_to_anthropic()** (1 connections) — `tests/test_multi_provider_fabric.py`
- **.test_format_openai_with_tool_calls()** (1 connections) — `tests/test_multi_provider_fabric.py`
- **.test_format_with_content_blocks()** (1 connections) — `tests/test_multi_provider_fabric.py`
- **.test_tools_to_anthropic_conversion()** (1 connections) — `tests/test_multi_provider_fabric.py`

## Relationships

- [MultiProviderFabric](MultiProviderFabric.md) (2 shared connections)
- [KeyPoolManager](KeyPoolManager.md) (1 shared connections)
- [litellm](litellm.md) (1 shared connections)

## Source Files

- `tests/test_multi_provider_fabric.py`

## Audit Trail

- EXTRACTED: 30 (94%)
- INFERRED: 2 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*