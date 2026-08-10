# MultiProviderFabric

> 28 nodes · cohesion 0.11

## Key Concepts

- **MultiProviderFabric** (47 connections) — `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- **TestDispatchRequest** (13 connections) — `tests/test_multi_provider_fabric.py`
- **TestRouteBuilding** (7 connections) — `tests/test_multi_provider_fabric.py`
- **patch** (5 connections)
- **._block_all_providers()** (5 connections) — `tests/test_multi_provider_fabric.py`
- **.test_consecutive_429s_trip_circuit_breaker()** (5 connections) — `tests/test_multi_provider_fabric.py`
- **.test_dispatch_http_status_error_triggers_cascade()** (4 connections) — `tests/test_multi_provider_fabric.py`
- **.test_dispatch_non_dict_json_body_falls_through()** (4 connections) — `tests/test_multi_provider_fabric.py`
- **.test_dispatch_non_json_body_falls_through()** (4 connections) — `tests/test_multi_provider_fabric.py`
- **.test_dispatch_successful_call()** (4 connections) — `tests/test_multi_provider_fabric.py`
- **.test_dispatch_with_context_objects()** (4 connections) — `tests/test_multi_provider_fabric.py`
- **.test_simulation_fallback()** (4 connections) — `tests/test_multi_provider_fabric.py`
- **.test_skip_perma_banned_provider()** (4 connections) — `tests/test_multi_provider_fabric.py`
- **.setup_method()** (2 connections) — `tests/test_multi_provider_fabric.py`
- **.__init__()** (1 connections) — `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- **Block all real providers so dispatch falls to simulation.** (1 connections) — `tests/test_multi_provider_fabric.py`
- **Without any working providers, should fall through to simulation.** (1 connections) — `tests/test_multi_provider_fabric.py`
- **Test that content blocks (list) are flattened correctly before dispatch.** (1 connections) — `tests/test_multi_provider_fabric.py`
- **Test a successful API call returns formatted Anthropic response.** (1 connections) — `tests/test_multi_provider_fabric.py`
- **A 2xx with a non-dict JSON body must cascade, not crash on .get().** (1 connections) — `tests/test_multi_provider_fabric.py`
- **A 2xx with an empty/non-JSON body must cascade, not raise JSONDecodeError.** (1 connections) — `tests/test_multi_provider_fabric.py`
- **4xx/5xx from dispatch() must be caught by HTTPStatusError handling.** (1 connections) — `tests/test_multi_provider_fabric.py`
- **Provider under perma-ban should be skipped.** (1 connections) — `tests/test_multi_provider_fabric.py`
- **Consecutive 429 responses must count as a provider circuit-breaker event (not…** (1 connections) — `tests/test_multi_provider_fabric.py`
- **.setup_method()** (1 connections) — `tests/test_multi_provider_fabric.py`
- *... and 3 more nodes in this community*

## Relationships

- [test_health_check.py](test_health_check.py.md) (9 shared connections)
- [webapp.py](webapp.py.md) (7 shared connections)
- [litellm](litellm.md) (6 shared connections)
- [.run_full_agentic_workflow](run_full_agentic_workflow.md) (4 shared connections)
- [verify_component.sh](verify_component.sh.md) (4 shared connections)
- [services/__init__.py](services-__init__.py.md) (4 shared connections)
- [KeyPoolManager](KeyPoolManager.md) (3 shared connections)
- [.get_available_worker](get_available_worker.md) (2 shared connections)
- [conftest.py](conftest.py.md) (1 shared connections)

## Source Files

- `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- `tests/test_multi_provider_fabric.py`

## Audit Trail

- EXTRACTED: 102 (81%)
- INFERRED: 24 (19%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*