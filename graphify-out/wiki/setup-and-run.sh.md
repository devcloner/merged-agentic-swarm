# setup-and-run.sh

> 5 nodes · cohesion 0.40

## Key Concepts

- **_Stream** (6 connections) — `tests/test_webapp.py`
- **Async byte stream over fixed chunks for the mocked litellm SSE response.** (1 connections) — `tests/test_webapp.py`
- **.aclose()** (1 connections) — `tests/test_webapp.py`
- **.__aiter__()** (1 connections) — `tests/test_webapp.py`
- **.__init__()** (1 connections) — `tests/test_webapp.py`

## Relationships

- [ProxyChainHealth](ProxyChainHealth.md) (1 shared connections)
- [ObstaclePlaybookEngine](ObstaclePlaybookEngine.md) (1 shared connections)

## Source Files

- `tests/test_webapp.py`

## Audit Trail

- EXTRACTED: 9 (90%)
- INFERRED: 1 (10%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*