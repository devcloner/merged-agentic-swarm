# services/__init__.py

> 29 nodes · cohesion 0.09

## Key Concepts

- **multi_provider_fabric.py** (20 connections) — `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- **claude_proxy_server.py** (15 connections) — `src/merged_agentic_swarm/proxy/claude_proxy_server.py`
- **key_pool.py** (11 connections) — `src/merged_agentic_swarm/providers/key_pool.py`
- **_record_failure()** (9 connections) — `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- **TestCircuitBreaker** (9 connections) — `tests/test_multi_provider_fabric.py`
- **providers/__init__.py** (8 connections) — `src/merged_agentic_swarm/providers/__init__.py`
- **KeyStatus** (7 connections) — `src/merged_agentic_swarm/providers/key_pool.py`
- **_record_success()** (5 connections) — `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- **_persist_bans()** (3 connections) — `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- **reload_fabric_routes()** (3 connections) — `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- **.test_perma_ban_expiry_clears()** (3 connections) — `tests/test_multi_provider_fabric.py`
- **.test_record_success_resets()** (3 connections) — `tests/test_multi_provider_fabric.py`
- **Enum** (2 connections)
- **_load_bans()** (2 connections) — `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- **.test_record_failure_403_trips_circuit_breaker()** (2 connections) — `tests/test_multi_provider_fabric.py`
- **.test_record_failure_circuit_breaker()** (2 connections) — `tests/test_multi_provider_fabric.py`
- **.test_record_failure_perma_ban_401()** (2 connections) — `tests/test_multi_provider_fabric.py`
- **Providers Package Initialization** (1 connections) — `src/merged_agentic_swarm/providers/__init__.py`
- **str** (1 connections)
- **API Key Pool Manager & Key Rotator Supports multi-provider key rotation, quota…** (1 connections) — `src/merged_agentic_swarm/providers/key_pool.py`
- **Multi-Backend Model Fabric Routes requests across providers with priority…** (1 connections) — `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- **Atomically write the perma-ban map to disk. Caller must hold _fabric_lock.** (1 connections) — `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- **Load persisted perma-bans into _permanently_dead, dropping expired entries.** (1 connections) — `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- **Clear the overlay cache so the next dispatch re-reads the JSON file.** (1 connections) — `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- **Record a provider failure — perma-ban on 401 auth errors, circuit-break on…** (1 connections) — `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- *... and 4 more nodes in this community*

## Relationships

- [KeyPoolManager](KeyPoolManager.md) (5 shared connections)
- [.run_full_agentic_workflow](run_full_agentic_workflow.md) (5 shared connections)
- [TestFormatConversion](TestFormatConversion.md) (4 shared connections)
- [MultiProviderFabric](MultiProviderFabric.md) (4 shared connections)
- [LatencyTracker](LatencyTracker.md) (4 shared connections)
- [FastFallbackConfig](FastFallbackConfig.md) (3 shared connections)
- [test_health_check.py](test_health_check.py.md) (3 shared connections)
- [AgentSpec](AgentSpec.md) (2 shared connections)
- [litellm](litellm.md) (2 shared connections)
- [TestLitellmPresenceInRoutes](TestLitellmPresenceInRoutes.md) (2 shared connections)
- [MultiLayeredAgenticOrchestrator](MultiLayeredAgenticOrchestrator.md) (2 shared connections)
- [ClaudeProxyHandler](ClaudeProxyHandler.md) (2 shared connections)

## Source Files

- `src/merged_agentic_swarm/providers/__init__.py`
- `src/merged_agentic_swarm/providers/key_pool.py`
- `src/merged_agentic_swarm/providers/multi_provider_fabric.py`
- `src/merged_agentic_swarm/proxy/claude_proxy_server.py`
- `tests/test_multi_provider_fabric.py`

## Audit Trail

- EXTRACTED: 112 (95%)
- INFERRED: 6 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*