# ConcurrencyRampController

> 24 nodes · cohesion 0.09

## Key Concepts

- **TestTokenSavior** (12 connections) — `tests/test_token_savior.py`
- **tools/__init__.py** (7 connections) — `src/merged_agentic_swarm/tools/__init__.py`
- **TokenSavior** (7 connections) — `src/merged_agentic_swarm/tools/token_savior.py`
- **token_savior.py** (4 connections) — `src/merged_agentic_swarm/tools/token_savior.py`
- **test_token_savior.py** (3 connections) — `tests/test_token_savior.py`
- **.compact_bash_output()** (2 connections) — `src/merged_agentic_swarm/tools/token_savior.py`
- **.compact_code_snippet()** (2 connections) — `src/merged_agentic_swarm/tools/token_savior.py`
- **.compress_prose_output()** (2 connections) — `src/merged_agentic_swarm/tools/token_savior.py`
- **.setup_method()** (2 connections) — `tests/test_token_savior.py`
- **Tools Package Initialization** (1 connections) — `src/merged_agentic_swarm/tools/__init__.py`
- **Token Savior & Context Compactor Optimizes context window consumption via…** (1 connections) — `src/merged_agentic_swarm/tools/token_savior.py`
- **Removes blank lines and excessive indentation spaces to save tokens.** (1 connections) — `src/merged_agentic_swarm/tools/token_savior.py`
- **Filters noisy bash logs and retains error tracebacks + summary lines.** (1 connections) — `src/merged_agentic_swarm/tools/token_savior.py`
- **Compresses assistant prose (Caveman mode) by removing pleasantries, hedging,…** (1 connections) — `src/merged_agentic_swarm/tools/token_savior.py`
- **Tests for tools/token_savior.py Coverage: TokenSavior — compact_code_snippet,…** (1 connections) — `tests/test_token_savior.py`
- **.test_compact_bash_output_filters_errors()** (1 connections) — `tests/test_token_savior.py`
- **.test_compact_bash_output_short()** (1 connections) — `tests/test_token_savior.py`
- **.test_compact_code_does_not_truncate_short()** (1 connections) — `tests/test_token_savior.py`
- **.test_compact_code_removes_blank_and_comment_lines()** (1 connections) — `tests/test_token_savior.py`
- **.test_compact_code_truncates_long()** (1 connections) — `tests/test_token_savior.py`
- **.test_compress_prose_does_not_mutate_clean_text()** (1 connections) — `tests/test_token_savior.py`
- **.test_compress_prose_keeps_essential()** (1 connections) — `tests/test_token_savior.py`
- **.test_compress_prose_removes_fillers()** (1 connections) — `tests/test_token_savior.py`
- **.test_empty_input()** (1 connections) — `tests/test_token_savior.py`

## Relationships

- [AgentSpec](AgentSpec.md) (1 shared connections)
- [KnowledgeCache](KnowledgeCache.md) (1 shared connections)
- [test_webapp.py](test_webapp.py.md) (1 shared connections)
- [test_streaming_proxy.py](test_streaming_proxy.py.md) (1 shared connections)

## Source Files

- `src/merged_agentic_swarm/tools/__init__.py`
- `src/merged_agentic_swarm/tools/token_savior.py`
- `tests/test_token_savior.py`

## Audit Trail

- EXTRACTED: 54 (96%)
- INFERRED: 2 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*