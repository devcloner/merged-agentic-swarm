---
type: community
cohesion: 0.21
members: 12
---

# _FakeClient

**Cohesion:** 0.21 - loosely connected
**Members:** 12 nodes

## Members
- [[dot-__init__()_30]] - code - tests/test_fast_pool.py
- [[dot-close()_1]] - code - tests/test_fast_pool.py
- [[dot-is_closed()]] - code - tests/test_fast_pool.py
- [[dot-post()_1]] - code - tests/test_fast_pool.py
- [[Records the per-request timeout passed to post() without network IO.]] - rationale - tests/test_fast_pool.py
- [[Response_2]] - code
- [[Timeout]] - code
- [[_FakeClient_1]] - code - tests/test_fast_pool.py
- [[_install_fake()]] - code - tests/test_fast_pool.py
- [[test_dispatch_localhost_uses_local_connect_timeout()]] - code - tests/test_fast_pool.py
- [[test_dispatch_remote_keeps_configured_connect_timeout()]] - code - tests/test_fast_pool.py
- [[test_fast_pool.py]] - code - tests/test_fast_pool.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/_FakeClient
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_multi_provider_fabric.py]]

## Top bridge nodes
- [[_FakeClient_1]] - degree 8, connects to 1 community
- [[test_fast_pool.py]] - degree 5, connects to 1 community
- [[test_dispatch_localhost_uses_local_connect_timeout()]] - degree 4, connects to 1 community
- [[test_dispatch_remote_keeps_configured_connect_timeout()]] - degree 4, connects to 1 community