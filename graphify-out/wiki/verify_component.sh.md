# verify_component.sh

> 18 nodes · cohesion 0.14

## Key Concepts

- **FastFallbackConfig** (19 connections) — `src/merged_agentic_swarm/fast_fallback.py`
- **TestAdaptiveSelection** (8 connections) — `tests/test_fast_fallback.py`
- **TestConfigFromEnv** (6 connections) — `tests/test_fast_fallback.py`
- **.from_env()** (5 connections) — `src/merged_agentic_swarm/fast_fallback.py`
- **.__init__()** (5 connections) — `src/merged_agentic_swarm/fast_fallback.py`
- **.test_fast_fallback_promoted()** (4 connections) — `tests/test_fast_fallback.py`
- **.test_skipped_provider_removed_from_order()** (3 connections) — `tests/test_fast_fallback.py`
- **.test_static_order_preserved_without_samples()** (3 connections) — `tests/test_fast_fallback.py`
- **.test_env_overrides()** (3 connections) — `tests/test_fast_fallback.py`
- **.setup_method()** (2 connections) — `tests/test_fast_fallback.py`
- **.test_defaults()** (2 connections) — `tests/test_fast_fallback.py`
- **dict** (1 connections)
- **.__post_init__()** (1 connections) — `src/merged_agentic_swarm/fast_fallback.py`
- **Build a config from ``FAST_FALLBACK_*`` environment variables.** (1 connections) — `src/merged_agentic_swarm/fast_fallback.py`
- **Tunables for the fast-fallback router (dataclass defaults + env overrides).** (1 connections) — `src/merged_agentic_swarm/fast_fallback.py`
- **A fallback with strong latency history outranks a slow primary.** (1 connections) — `tests/test_fast_fallback.py`
- **No latency history → static verified-first order is untouched.** (1 connections) — `tests/test_fast_fallback.py`
- **A perma-banned provider does not appear in the candidate list.** (1 connections) — `tests/test_fast_fallback.py`

## Relationships

- [webapp.py](webapp.py.md) (15 shared connections)
- [.run_full_agentic_workflow](run_full_agentic_workflow.md) (5 shared connections)
- [MultiProviderFabric](MultiProviderFabric.md) (4 shared connections)
- [TestFormatConversion](TestFormatConversion.md) (1 shared connections)

## Source Files

- `src/merged_agentic_swarm/fast_fallback.py`
- `tests/test_fast_fallback.py`

## Audit Trail

- EXTRACTED: 53 (79%)
- INFERRED: 14 (21%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*