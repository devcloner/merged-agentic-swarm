---
type: community
cohesion: 0.09
members: 48
---

# webapp.py

**Cohesion:** 0.09 - loosely connected
**Members:** 48 nodes

## Members
- [[Agentic Swarm — Web UI Control Panel. A Starlette control panel (JSON API + a…]] - rationale - src/merged_agentic_swarm/webapp.py
- [[AsyncBaseTransport_1]] - code
- [[Create the control-panel Starlette app. A shared ``httpx.AsyncClient``…]] - rationale - src/merged_agentic_swarm/webapp.py
- [[HTMLResponse]] - code
- [[JSONResponse]] - code
- [[Load one report by safe stem; None when missing or unreadable.]] - rationale - src/merged_agentic_swarm/webapp.py
- [[MODEL_FABRIC_ROUTES as alias - {provider, model} chains.]] - rationale - src/merged_agentic_swarm/webapp.py
- [[Merged fabric chain view code MODEL_FABRIC_ROUTES overlaid per alias.]] - rationale - src/merged_agentic_swarm/webapp.py
- [[Newest reports.json parsed into a summary + timeline (or None).]] - rationale - src/merged_agentic_swarm/webapp.py
- [[PROVIDER_REGISTRY backends - {base_url, auth_env NAME, status, primary}.]] - rationale - src/merged_agentic_swarm/webapp.py
- [[Persist profiles to disk atomically and invalidate the load cache.]] - rationale - src/merged_agentic_swarm/webapp.py
- [[Provider - {active, total, key_ids} — key_id list only, never values.]] - rationale - src/merged_agentic_swarm/webapp.py
- [[Report live status for a run (or all runs when no ``run_id`` is given).]] - rationale - src/merged_agentic_swarm/webapp.py
- [[Request_1]] - code
- [[Run the control panel on loopback only.]] - rationale - src/merged_agentic_swarm/webapp.py
- [[Signal a running workflow to abort at the next wave boundary.]] - rationale - src/merged_agentic_swarm/webapp.py
- [[Starlette_1]] - code
- [[Upsert one chain alias into fabric-routes.json atomically.]] - rationale - src/merged_agentic_swarm/webapp.py
- [[{name, mtime} for every reports.json, newest first.]] - rationale - src/merged_agentic_swarm/webapp.py
- [[_fabric_chains()]] - code - src/merged_agentic_swarm/webapp.py
- [[_fabric_routes()]] - code - src/merged_agentic_swarm/webapp.py
- [[_key_pool_snapshot()]] - code - src/merged_agentic_swarm/webapp.py
- [[_latest_report()]] - code - src/merged_agentic_swarm/webapp.py
- [[_load_fabric_overlay()]] - code - src/merged_agentic_swarm/webapp.py
- [[_registry_backends()]] - code - src/merged_agentic_swarm/webapp.py
- [[_report_detail()]] - code - src/merged_agentic_swarm/webapp.py
- [[_report_list()]] - code - src/merged_agentic_swarm/webapp.py
- [[_serialize_run()]] - code - src/merged_agentic_swarm/webapp.py
- [[_write_fabric_overlay()]] - code - src/merged_agentic_swarm/webapp.py
- [[_write_profiles()]] - code - src/merged_agentic_swarm/webapp.py
- [[create_app()]] - code - src/merged_agentic_swarm/webapp.py
- [[fabric-routes.json as {routes {alias route, …}}; {} when absent.]] - rationale - src/merged_agentic_swarm/webapp.py
- [[handle_chain_update()]] - code - src/merged_agentic_swarm/webapp.py
- [[handle_chains()]] - code - src/merged_agentic_swarm/webapp.py
- [[handle_dashboard()]] - code - src/merged_agentic_swarm/webapp.py
- [[handle_latency_test()]] - code - src/merged_agentic_swarm/webapp.py
- [[handle_model_role_update()]] - code - src/merged_agentic_swarm/webapp.py
- [[handle_models()]] - code - src/merged_agentic_swarm/webapp.py
- [[handle_profile_update()]] - code - src/merged_agentic_swarm/webapp.py
- [[handle_profiles()]] - code - src/merged_agentic_swarm/webapp.py
- [[handle_report_detail()]] - code - src/merged_agentic_swarm/webapp.py
- [[handle_reports_list()]] - code - src/merged_agentic_swarm/webapp.py
- [[handle_run_cancel()]] - code - src/merged_agentic_swarm/webapp.py
- [[handle_run_plan()]] - code - src/merged_agentic_swarm/webapp.py
- [[handle_run_status()]] - code - src/merged_agentic_swarm/webapp.py
- [[handle_status()]] - code - src/merged_agentic_swarm/webapp.py
- [[main()_7]] - code - src/merged_agentic_swarm/webapp.py
- [[webapp.py]] - code - src/merged_agentic_swarm/webapp.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/webapppy
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_services__init__.py]]
- 7 edges to [[_COMMUNITY_handle_run]]
- 6 edges to [[_COMMUNITY__run_latency_test]]
- 5 edges to [[_COMMUNITY__load_registry]]
- 2 edges to [[_COMMUNITY_APIKeyInfo]]
- 2 edges to [[_COMMUNITY_multi_provider_fabric.py]]
- 1 edge to [[_COMMUNITY_PassthroughStreamingProxy]]
- 1 edge to [[_COMMUNITY_MultiLayeredAgenticOrchestrator]]

## Top bridge nodes
- [[webapp.py]] - degree 43, connects to 7 communities
- [[create_app()]] - degree 22, connects to 3 communities
- [[handle_models()]] - degree 6, connects to 2 communities
- [[Request_1]] - degree 15, connects to 1 community
- [[JSONResponse]] - degree 14, connects to 1 community