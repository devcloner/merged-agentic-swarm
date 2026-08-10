---
type: community
cohesion: 0.25
members: 8
---

# test_check_streaming_fcc_happy_path

**Cohesion:** 0.25 - loosely connected
**Members:** 8 nodes

## Members
- [[Build a single SSE data line for an Anthropic streaming content-block-delta.]] - rationale - tests/test_health_check.py
- [[_sse_event()]] - code - tests/test_health_check.py
- [[check_streaming targets routatic-proxy when endpoint='routatic'.]] - rationale - tests/test_health_check.py
- [[check_streaming through FCC endpoint measures TTFB and total latency.]] - rationale - tests/test_health_check.py
- [[stream' subcommand runs only the streaming check.]] - rationale - tests/test_health_check.py
- [[test_check_streaming_fcc_happy_path()]] - code - tests/test_health_check.py
- [[test_check_streaming_routatic_endpoint()]] - code - tests/test_health_check.py
- [[test_main_stream_subcommand()]] - code - tests/test_health_check.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/test_check_streaming_fcc_happy_path
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_ProxyChainHealth]]
- 4 edges to [[_COMMUNITY_test_health_check.py]]
- 1 edge to [[_COMMUNITY_HopResult]]

## Top bridge nodes
- [[test_main_stream_subcommand()]] - degree 5, connects to 3 communities
- [[test_check_streaming_fcc_happy_path()]] - degree 6, connects to 2 communities
- [[test_check_streaming_routatic_endpoint()]] - degree 6, connects to 2 communities
- [[_sse_event()]] - degree 5, connects to 1 community