# TestCmdProviders

> 6 nodes · cohesion 0.33

## Key Concepts

- **_fabric_chains()** (5 connections) — `src/merged_agentic_swarm/webapp.py`
- **_write_fabric_overlay()** (5 connections) — `src/merged_agentic_swarm/webapp.py`
- **_load_fabric_overlay()** (4 connections) — `src/merged_agentic_swarm/webapp.py`
- **fabric-routes.json as {"routes": {alias: [route, …]}}; {} when absent.** (1 connections) — `src/merged_agentic_swarm/webapp.py`
- **Merged fabric chain view: code MODEL_FABRIC_ROUTES overlaid per alias.** (1 connections) — `src/merged_agentic_swarm/webapp.py`
- **Upsert one chain alias into fabric-routes.json atomically.** (1 connections) — `src/merged_agentic_swarm/webapp.py`

## Relationships

- [FastFallbackConfig](FastFallbackConfig.md) (3 shared connections)
- [_make_learning_entry](_make_learning_entry.md) (3 shared connections)
- [services/__init__.py](services-__init__.py.md) (1 shared connections)

## Source Files

- `src/merged_agentic_swarm/webapp.py`

## Audit Trail

- EXTRACTED: 16 (94%)
- INFERRED: 1 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*