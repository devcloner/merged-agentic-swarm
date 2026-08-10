# ClaudeProxyHandler

> 17 nodes · cohesion 0.13

## Key Concepts

- **ProxyServerDaemon** (17 connections) — `src/merged_agentic_swarm/proxy/claude_proxy_server.py`
- **ThreadedHTTPServer** (5 connections) — `src/merged_agentic_swarm/proxy/claude_proxy_server.py`
- **.setup_server()** (4 connections) — `tests/test_claude_proxy_server.py`
- **TestProxyServerDaemon** (4 connections) — `tests/test_claude_proxy_server.py`
- **.test_double_start()** (3 connections) — `tests/test_claude_proxy_server.py`
- **.test_start_stop()** (3 connections) — `tests/test_claude_proxy_server.py`
- **._prewarm()** (2 connections) — `src/merged_agentic_swarm/proxy/claude_proxy_server.py`
- **.start()** (2 connections) — `src/merged_agentic_swarm/proxy/claude_proxy_server.py`
- **HTTPServer** (1 connections)
- **.__init__()** (1 connections) — `src/merged_agentic_swarm/proxy/claude_proxy_server.py`
- **.stop()** (1 connections) — `src/merged_agentic_swarm/proxy/claude_proxy_server.py`
- **Threaded HTTP server to handle concurrent requests.** (1 connections) — `src/merged_agentic_swarm/proxy/claude_proxy_server.py`
- **fixture** (1 connections)
- **ProxyServerDaemon should start and stop without error.** (1 connections) — `tests/test_claude_proxy_server.py`
- **Calling start() twice should not create a second server.** (1 connections) — `tests/test_claude_proxy_server.py`
- **Start a server on random port for each test.** (1 connections) — `tests/test_claude_proxy_server.py`
- **ThreadingMixIn** (1 connections)

## Relationships

- [TestLitellmPresenceInRoutes](TestLitellmPresenceInRoutes.md) (2 shared connections)
- [services/__init__.py](services-__init__.py.md) (2 shared connections)
- [ProxyChainHealth](ProxyChainHealth.md) (2 shared connections)
- [test_agentic_cli.py](test_agentic_cli.py.md) (2 shared connections)
- [TestClaudeProxyHandler](TestClaudeProxyHandler.md) (2 shared connections)
- [AgentSpec](AgentSpec.md) (1 shared connections)
- [Ultracode Swarm Audit Fleet Manifest](Ultracode_Swarm_Audit_Fleet_Manifest.md) (1 shared connections)
- [LatencyTracker](LatencyTracker.md) (1 shared connections)

## Source Files

- `src/merged_agentic_swarm/proxy/claude_proxy_server.py`
- `tests/test_claude_proxy_server.py`

## Audit Trail

- EXTRACTED: 42 (86%)
- INFERRED: 7 (14%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*