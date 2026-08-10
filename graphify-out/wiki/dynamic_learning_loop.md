# dynamic_learning_loop

> 11 nodes · cohesion 0.18

## Key Concepts

- **TestChains** (6 connections) — `tests/test_webapp.py`
- **fixture** (4 connections)
- **_fresh_caches()** (3 connections) — `tests/test_webapp.py`
- **.overlay_path()** (3 connections) — `tests/test_webapp.py`
- **tmp_profiles_file()** (3 connections) — `tests/test_webapp.py`
- **Start each test with empty disk caches so patches don't leak across tests.** (1 connections) — `tests/test_webapp.py`
- **Point webapp at a throwaway fabric-routes.json (never the real file).** (1 connections) — `tests/test_webapp.py`
- **Point swarm_profiles at a throwaway registry seeded with the on-disk profiles.** (1 connections) — `tests/test_webapp.py`
- **.test_chains_get_merges_defaults_and_overlay()** (1 connections) — `tests/test_webapp.py`
- **.test_chains_put_invalid_400()** (1 connections) — `tests/test_webapp.py`
- **.test_chains_put_upserts_overlay_and_merges()** (1 connections) — `tests/test_webapp.py`

## Relationships

- [ObstaclePlaybookEngine](ObstaclePlaybookEngine.md) (3 shared connections)
- [LatencyTracker](LatencyTracker.md) (1 shared connections)
- [ProxyChainHealth](ProxyChainHealth.md) (1 shared connections)

## Source Files

- `tests/test_webapp.py`

## Audit Trail

- EXTRACTED: 24 (96%)
- INFERRED: 1 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*