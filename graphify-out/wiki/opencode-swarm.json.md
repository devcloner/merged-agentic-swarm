# opencode-swarm.json

> 8 nodes · cohesion 0.25

## Key Concepts

- **.load_keys()** (5 connections) — `src/merged_agentic_swarm/providers/key_pool.py`
- **._collect_keys_from_sources()** (4 connections) — `src/merged_agentic_swarm/providers/key_pool.py`
- **.reload()** (4 connections) — `src/merged_agentic_swarm/providers/key_pool.py`
- **.add_key()** (3 connections) — `src/merged_agentic_swarm/providers/key_pool.py`
- **.__init__()** (2 connections) — `src/merged_agentic_swarm/providers/key_pool.py`
- **Loads API keys from env file, environment variables, and local key files.** (1 connections) — `src/merged_agentic_swarm/providers/key_pool.py`
- **Hot-reload keys from all sources, preserving runtime stats for persistent keys.…** (1 connections) — `src/merged_agentic_swarm/providers/key_pool.py`
- **Gather (provider, secret_value, key_id) candidates from all key sources.…** (1 connections) — `src/merged_agentic_swarm/providers/key_pool.py`

## Relationships

- [KeyPoolManager](KeyPoolManager.md) (5 shared connections)
- [TestFormatConversion](TestFormatConversion.md) (2 shared connections)

## Source Files

- `src/merged_agentic_swarm/providers/key_pool.py`

## Audit Trail

- EXTRACTED: 21 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*