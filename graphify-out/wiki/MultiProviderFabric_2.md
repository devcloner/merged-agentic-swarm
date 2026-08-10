# MultiProviderFabric

> God node · 47 connections · `src/merged_agentic_swarm/providers/multi_provider_fabric.py`

**Community:** [MultiProviderFabric](MultiProviderFabric.md)

## Connections by Relation

### calls
- _router_with_keys() `EXTRACTED`
- .test_dispatch_fast_uses_default_router() `EXTRACTED`
- .test_enabled_false_delegates_to_fabric() `EXTRACTED`
- .test_consecutive_429s_trip_circuit_breaker() `EXTRACTED`
- isolated_fabric() `INFERRED`
- .test_dispatch_http_status_error_triggers_cascade() `EXTRACTED`
- .test_dispatch_non_dict_json_body_falls_through() `EXTRACTED`
- .test_dispatch_non_json_body_falls_through() `EXTRACTED`
- .test_dispatch_successful_call() `EXTRACTED`
- .test_dispatch_with_context_objects() `EXTRACTED`
- .test_simulation_fallback() `EXTRACTED`
- .test_skip_perma_banned_provider() `EXTRACTED`
- .test_perma_ban_expiry_clears() `EXTRACTED`
- .setup_method() `EXTRACTED`
- .setup_method() `EXTRACTED`

### contains
- [multi_provider_fabric.py](multi_provider_fabric.py.md) `EXTRACTED`

### imports
- fast_fallback.py `EXTRACTED`
- providers/__init__.py `EXTRACTED`

### method
- .dispatch_request() `EXTRACTED`
- .format_anthropic_to_anthropic() `EXTRACTED`
- ._flatten_content_to_text() `EXTRACTED`
- .format_anthropic_to_openai() `EXTRACTED`
- ._build_route_list() `EXTRACTED`
- ._content_to_anthropic_blocks() `EXTRACTED`
- ._extract_anthropic_tool_calls() `EXTRACTED`
- .format_openai_to_anthropic_response() `EXTRACTED`
- ._tools_to_anthropic() `EXTRACTED`
- .__init__() `EXTRACTED`

### references
- .__init__() `EXTRACTED`

### uses
- [FastFallbackRouter](FastFallbackRouter.md) `INFERRED`
- [FastFallbackConfig](FastFallbackConfig.md) `INFERRED`
- [TestFormatConversion](TestFormatConversion.md) `INFERRED`
- [TestDispatchRequest](TestDispatchRequest.md) `INFERRED`
- TestDispatchBehavior `INFERRED`
- TestCircuitBreaker `INFERRED`
- TestParallelProbe `INFERRED`
- TestCircuitBreaker `INFERRED`
- TestAdaptiveSelection `INFERRED`
- [TestBanPersistence](TestBanPersistence.md) `INFERRED`
- [TestMalformedOverlayRoutes](TestMalformedOverlayRoutes.md) `INFERRED`
- TestRouteBuilding `INFERRED`
- _ProbeResult `INFERRED`
- _ProbeContext `INFERRED`
- TestConfigFromEnv `INFERRED`
- TestDispatchHelper `INFERRED`
- [TestLitellmPresenceInRoutes](TestLitellmPresenceInRoutes.md) `INFERRED`
- TestFabricRouteOverlay `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*