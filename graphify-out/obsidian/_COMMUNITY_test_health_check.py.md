---
type: community
cohesion: 0.10
members: 22
---

# test_health_check.py

**Cohesion:** 0.10 - loosely connected
**Members:** 22 nodes

## Members
- [[--json flag emits machine-readable JSON for all checks.]] - rationale - tests/test_health_check.py
- [[--json reports degraded when a check fails.]] - rationale - tests/test_health_check.py
- [[dot-__init__()_3]] - code - src/merged_agentic_swarm/health_check.py
- [[dot-from_env()_1]] - code - src/merged_agentic_swarm/health_check.py
- [[Response_3]] - code
- [[Return a 200 httpx.Response whose .stream yields SSE events.]] - rationale - tests/test_health_check.py
- [[_make_sse_response()]] - code - tests/test_health_check.py
- [[from_env casts numeric env vars to intfloat.]] - rationale - tests/test_health_check.py
- [[from_env picks up env overrides for string fields.]] - rationale - tests/test_health_check.py
- [[from_env returns defaults when no env vars are set.]] - rationale - tests/test_health_check.py
- [[from_env surfaces ValueError for non-numeric env values (no silent fallback).]] - rationale - tests/test_health_check.py
- [[providers' subcommand runs providercircuit-breaker checks.]] - rationale - tests/test_health_check.py
- [[status' subcommand runs hop probes only (no streaming).]] - rationale - tests/test_health_check.py
- [[test_from_env_defaults()]] - code - tests/test_health_check.py
- [[test_from_env_invalid_numeric_falls_through()]] - code - tests/test_health_check.py
- [[test_from_env_override_numerics()]] - code - tests/test_health_check.py
- [[test_from_env_override_strings()]] - code - tests/test_health_check.py
- [[test_health_check.py]] - code - tests/test_health_check.py
- [[test_main_json_output_all()]] - code - tests/test_health_check.py
- [[test_main_json_output_degraded()]] - code - tests/test_health_check.py
- [[test_main_providers_subcommand()]] - code - tests/test_health_check.py
- [[test_main_status_command()]] - code - tests/test_health_check.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/test_health_checkpy
SORT file.name ASC
```

## Connections to other communities
- 27 edges to [[_COMMUNITY_ProxyChainHealth]]
- 14 edges to [[_COMMUNITY_HopResult]]
- 4 edges to [[_COMMUNITY_test_check_streaming_fcc_happy_path]]
- 1 edge to [[_COMMUNITY_test_streaming_proxy.py]]

## Top bridge nodes
- [[test_health_check.py]] - degree 43, connects to 4 communities
- [[dot-from_env()_1]] - degree 7, connects to 2 communities
- [[test_main_json_output_all()]] - degree 4, connects to 2 communities
- [[test_main_json_output_degraded()]] - degree 4, connects to 2 communities
- [[test_main_providers_subcommand()]] - degree 4, connects to 2 communities