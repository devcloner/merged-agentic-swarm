---
type: community
cohesion: 0.13
members: 17
---

# ProxyServerDaemon

**Cohesion:** 0.13 - loosely connected
**Members:** 17 nodes

## Members
- [[dot-__init__()_7]] - code - src/merged_agentic_swarm/proxy/claude_proxy_server.py
- [[dot-_prewarm()]] - code - src/merged_agentic_swarm/proxy/claude_proxy_server.py
- [[dot-setup_server()]] - code - tests/test_claude_proxy_server.py
- [[dot-start()]] - code - src/merged_agentic_swarm/proxy/claude_proxy_server.py
- [[dot-stop()]] - code - src/merged_agentic_swarm/proxy/claude_proxy_server.py
- [[dot-test_double_start()]] - code - tests/test_claude_proxy_server.py
- [[dot-test_start_stop()]] - code - tests/test_claude_proxy_server.py
- [[Calling start() twice should not create a second server.]] - rationale - tests/test_claude_proxy_server.py
- [[HTTPServer]] - code
- [[ProxyServerDaemon]] - code - src/merged_agentic_swarm/proxy/claude_proxy_server.py
- [[ProxyServerDaemon should start and stop without error.]] - rationale - tests/test_claude_proxy_server.py
- [[Start a server on random port for each test.]] - rationale - tests/test_claude_proxy_server.py
- [[TestProxyServerDaemon]] - code - tests/test_claude_proxy_server.py
- [[Threaded HTTP server to handle concurrent requests.]] - rationale - src/merged_agentic_swarm/proxy/claude_proxy_server.py
- [[ThreadedHTTPServer]] - code - src/merged_agentic_swarm/proxy/claude_proxy_server.py
- [[ThreadingMixIn]] - code
- [[fixture_2]] - code

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ProxyServerDaemon
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_claude_proxy_server.py]]
- 2 edges to [[_COMMUNITY_MultiLayeredAgenticOrchestrator]]
- 2 edges to [[_COMMUNITY__forward_transcription]]
- 2 edges to [[_COMMUNITY_TestClaudeProxyHandler]]
- 1 edge to [[_COMMUNITY_multi_provider_fabric.py]]
- 1 edge to [[_COMMUNITY_WorkerRole]]

## Top bridge nodes
- [[ProxyServerDaemon]] - degree 17, connects to 5 communities
- [[ThreadedHTTPServer]] - degree 5, connects to 1 community
- [[dot-setup_server()]] - degree 4, connects to 1 community
- [[TestProxyServerDaemon]] - degree 4, connects to 1 community
- [[dot-_prewarm()]] - degree 2, connects to 1 community