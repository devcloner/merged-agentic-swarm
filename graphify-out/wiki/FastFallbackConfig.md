# FastFallbackConfig

> 22 nodes · cohesion 0.12

## Key Concepts

- **webapp.py** (43 connections) — `src/merged_agentic_swarm/webapp.py`
- **handle_status()** (8 connections) — `src/merged_agentic_swarm/webapp.py`
- **handle_run_status()** (6 connections) — `src/merged_agentic_swarm/webapp.py`
- **_spawn_agentic_run()** (6 connections) — `src/merged_agentic_swarm/webapp.py`
- **RunHandle** (5 connections) — `src/merged_agentic_swarm/webapp.py`
- **_fabric_routes()** (3 connections) — `src/merged_agentic_swarm/webapp.py`
- **_key_pool_snapshot()** (3 connections) — `src/merged_agentic_swarm/webapp.py`
- **_latest_report()** (3 connections) — `src/merged_agentic_swarm/webapp.py`
- **_registry_backends()** (3 connections) — `src/merged_agentic_swarm/webapp.py`
- **_report_detail()** (3 connections) — `src/merged_agentic_swarm/webapp.py`
- **_report_list()** (3 connections) — `src/merged_agentic_swarm/webapp.py`
- **_serialize_run()** (3 connections) — `src/merged_agentic_swarm/webapp.py`
- **Agentic Swarm — Web UI Control Panel. A Starlette control panel (JSON API + a…** (1 connections) — `src/merged_agentic_swarm/webapp.py`
- **PROVIDER_REGISTRY backends -> {base_url, auth_env NAME, status, primary}.** (1 connections) — `src/merged_agentic_swarm/webapp.py`
- **Newest reports/*.json parsed into a summary + timeline (or None).** (1 connections) — `src/merged_agentic_swarm/webapp.py`
- **[{name, mtime}] for every reports/*.json, newest first.** (1 connections) — `src/merged_agentic_swarm/webapp.py`
- **Load one report by safe stem; None when missing or unreadable.** (1 connections) — `src/merged_agentic_swarm/webapp.py`
- **Registry entry for a background workflow run.** (1 connections) — `src/merged_agentic_swarm/webapp.py`
- **Start a real agentic workflow on a background daemon thread (returns now).…** (1 connections) — `src/merged_agentic_swarm/webapp.py`
- **Report live status for a run (or all runs when no ``run_id`` is given).** (1 connections) — `src/merged_agentic_swarm/webapp.py`
- **Provider -> {active, total, key_ids} — key_id list only, never values.** (1 connections) — `src/merged_agentic_swarm/webapp.py`
- **MODEL_FABRIC_ROUTES as alias -> [{provider, model}] chains.** (1 connections) — `src/merged_agentic_swarm/webapp.py`

## Relationships

- [_make_learning_entry](_make_learning_entry.md) (21 shared connections)
- [PassthroughStreamingProxy](PassthroughStreamingProxy.md) (5 shared connections)
- [services/__init__.py](services-__init__.py.md) (3 shared connections)
- [ProxyChainHealth](ProxyChainHealth.md) (3 shared connections)
- [TestCmdProviders](TestCmdProviders.md) (3 shared connections)
- [check_proxy_health.sh](check_proxy_health.sh.md) (3 shared connections)
- [test_check_streaming_fcc_happy_path](test_check_streaming_fcc_happy_path.md) (2 shared connections)
- [Community 164](Community_164.md) (1 shared connections)
- [Community 165](Community_165.md) (1 shared connections)
- [TestWaveGatesWithRealState](TestWaveGatesWithRealState.md) (1 shared connections)

## Source Files

- `src/merged_agentic_swarm/webapp.py`

## Audit Trail

- EXTRACTED: 95 (96%)
- INFERRED: 4 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*