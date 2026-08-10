# ci.sh

> 5 nodes · cohesion 0.70

## Key Concepts

- **TestCmdProviders** (6 connections) — `tests/test_agentic_cli.py`
- **._setup()** (5 connections) — `tests/test_agentic_cli.py`
- **.test_providers_through_main()** (3 connections) — `tests/test_agentic_cli.py`
- **.test_providers_never_leaks_key_values()** (2 connections) — `tests/test_agentic_cli.py`
- **.test_providers_renders_key_names_env_names_and_routes()** (2 connections) — `tests/test_agentic_cli.py`

## Relationships

- [KeyPoolManager](KeyPoolManager.md) (2 shared connections)
- [test_webapp.py](test_webapp.py.md) (1 shared connections)
- [task_spine_cli.py](task_spine_cli.py.md) (1 shared connections)

## Source Files

- `tests/test_agentic_cli.py`

## Audit Trail

- EXTRACTED: 16 (89%)
- INFERRED: 2 (11%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*