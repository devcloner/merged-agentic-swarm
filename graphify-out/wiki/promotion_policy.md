# promotion_policy

> 7 nodes · cohesion 0.38

## Key Concepts

- **TestTargetRepoRoot** (11 connections) — `tests/test_opencode_swarm_service.py`
- **._target_repo_root()** (6 connections) — `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- **.test_getcwd_fallback()** (3 connections) — `tests/test_opencode_swarm_service.py`
- **.test_defaults_to_existing_sibling_or_cwd()** (2 connections) — `tests/test_opencode_swarm_service.py`
- **.test_env_var_wins()** (2 connections) — `tests/test_opencode_swarm_service.py`
- **Resolve the working repo the swarm writes into. ``SWARM_TARGET_REPO`` env var…** (1 connections) — `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- **When SWARM_TARGET_REPO is unset and no sibling target repo exists,…** (1 connections) — `tests/test_opencode_swarm_service.py`

## Relationships

- [SubTask](SubTask.md) (3 shared connections)
- [CodebaseMapService](CodebaseMapService.md) (2 shared connections)
- [AgentSpec](AgentSpec.md) (1 shared connections)
- [WorkerPoolConfig](WorkerPoolConfig.md) (1 shared connections)
- [WorkerRole](WorkerRole.md) (1 shared connections)
- [test_streaming_proxy.py](test_streaming_proxy.py.md) (1 shared connections)
- [ChainRegistry](ChainRegistry.md) (1 shared connections)

## Source Files

- `src/merged_agentic_swarm/services/opencode_swarm_service.py`
- `tests/test_opencode_swarm_service.py`

## Audit Trail

- EXTRACTED: 19 (73%)
- INFERRED: 7 (27%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*