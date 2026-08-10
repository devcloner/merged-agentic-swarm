# TestFormatConversion

> 15 nodes · cohesion 0.17

## Key Concepts

- **APIKeyInfo** (21 connections) — `src/merged_agentic_swarm/providers/key_pool.py`
- **TestAPIKeyInfo** (7 connections) — `tests/test_key_pool.py`
- **test_key_pool.py** (5 connections) — `tests/test_key_pool.py`
- **.get_key()** (4 connections) — `src/merged_agentic_swarm/providers/key_pool.py`
- **._get_key_unlocked()** (4 connections) — `src/merged_agentic_swarm/providers/key_pool.py`
- **.__repr__()** (2 connections) — `src/merged_agentic_swarm/providers/key_pool.py`
- **.mark_rate_limited()** (2 connections) — `src/merged_agentic_swarm/providers/key_pool.py`
- **.mark_success()** (2 connections) — `src/merged_agentic_swarm/providers/key_pool.py`
- **.test_default_creation()** (2 connections) — `tests/test_key_pool.py`
- **.test_mark_cooldown()** (2 connections) — `tests/test_key_pool.py`
- **.test_repr_does_not_leak_secret()** (2 connections) — `tests/test_key_pool.py`
- **Gets an active API key using round-robin / least-used strategy.** (1 connections) — `src/merged_agentic_swarm/providers/key_pool.py`
- **Internal: must be called while holding self._lock.** (1 connections) — `src/merged_agentic_swarm/providers/key_pool.py`
- **Avoid leaking the secret value in logs/debug output.** (1 connections) — `src/merged_agentic_swarm/providers/key_pool.py`
- **Tests for providers/key_pool.py Coverage: APIKeyInfo, KeyPoolManager…** (1 connections) — `tests/test_key_pool.py`

## Relationships

- [KeyPoolManager](KeyPoolManager.md) (9 shared connections)
- [.run_full_agentic_workflow](run_full_agentic_workflow.md) (5 shared connections)
- [services/__init__.py](services-__init__.py.md) (4 shared connections)
- [opencode-swarm.json](opencode-swarm.json.md) (2 shared connections)
- [verify_component.sh](verify_component.sh.md) (1 shared connections)

## Source Files

- `src/merged_agentic_swarm/providers/key_pool.py`
- `tests/test_key_pool.py`

## Audit Trail

- EXTRACTED: 47 (82%)
- INFERRED: 10 (18%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*