# test_check_streaming_fcc_happy_path

> 9 nodes · cohesion 0.25

## Key Concepts

- **_load_registry()** (6 connections) — `src/merged_agentic_swarm/services/model_routing.py`
- **reload_registry()** (6 connections) — `src/merged_agentic_swarm/services/model_routing.py`
- **_role_mapping()** (6 connections) — `src/merged_agentic_swarm/webapp.py`
- **_write_registry_roles()** (4 connections) — `src/merged_agentic_swarm/webapp.py`
- **Any** (2 connections)
- **Load the provider registry (cached); return {} when missing/unreadable.** (1 connections) — `src/merged_agentic_swarm/services/model_routing.py`
- **Clear the cached registry and reload it from disk. Called after the provider…** (1 connections) — `src/merged_agentic_swarm/services/model_routing.py`
- **Persist one role -> alias mapping into PROVIDER_REGISTRY.json atomically. The…** (1 connections) — `src/merged_agentic_swarm/webapp.py`
- **Tier + registered-role -> litellm alias via model_routing resolution.** (1 connections) — `src/merged_agentic_swarm/webapp.py`

## Relationships

- [PassthroughStreamingProxy](PassthroughStreamingProxy.md) (5 shared connections)
- [_make_learning_entry](_make_learning_entry.md) (3 shared connections)
- [FastFallbackConfig](FastFallbackConfig.md) (2 shared connections)

## Source Files

- `src/merged_agentic_swarm/services/model_routing.py`
- `src/merged_agentic_swarm/webapp.py`

## Audit Trail

- EXTRACTED: 26 (93%)
- INFERRED: 2 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*