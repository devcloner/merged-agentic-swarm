# PassthroughStreamingProxy

> 20 nodes · cohesion 0.17

## Key Concepts

- **services/__init__.py** (32 connections) — `src/merged_agentic_swarm/services/__init__.py`
- **model_routing.py** (11 connections) — `src/merged_agentic_swarm/services/model_routing.py`
- **resolve_model_alias_for_profile()** (11 connections) — `src/merged_agentic_swarm/services/swarm_profiles.py`
- **swarm_profiles.py** (10 connections) — `src/merged_agentic_swarm/services/swarm_profiles.py`
- **resolve_profile()** (10 connections) — `src/merged_agentic_swarm/services/swarm_profiles.py`
- **resolve_litellm_model_for_role()** (9 connections) — `src/merged_agentic_swarm/services/model_routing.py`
- **handle_run()** (8 connections) — `src/merged_agentic_swarm/webapp.py`
- **load_profiles()** (7 connections) — `src/merged_agentic_swarm/services/swarm_profiles.py`
- **list_profiles()** (6 connections) — `src/merged_agentic_swarm/services/swarm_profiles.py`
- **litellm_model_for_fabric_route()** (3 connections) — `src/merged_agentic_swarm/services/model_routing.py`
- **Services Package Initialization** (1 connections) — `src/merged_agentic_swarm/services/__init__.py`
- **Model Role Routing Resolves a worker role (deep / main / fast tier, or a…** (1 connections) — `src/merged_agentic_swarm/services/model_routing.py`
- **Return the first litellm model in the fabric route list for a model alias.** (1 connections) — `src/merged_agentic_swarm/services/model_routing.py`
- **Return the litellm virtual Gemini alias for a worker role. Resolution order: 1.…** (1 connections) — `src/merged_agentic_swarm/services/model_routing.py`
- **Swarm Profile Service Named, slash-command-style presets for pushing a large…** (1 connections) — `src/merged_agentic_swarm/services/swarm_profiles.py`
- **Load all swarm profiles (cached); fall back to the code-side dict when missing.** (1 connections) — `src/merged_agentic_swarm/services/swarm_profiles.py`
- **Return the resolved profile dict for a name; raise KeyError for unknown names.** (1 connections) — `src/merged_agentic_swarm/services/swarm_profiles.py`
- **Return [{name, description}] entries for every known profile, name-sorted.** (1 connections) — `src/merged_agentic_swarm/services/swarm_profiles.py`
- **Return the profile's model alias, or resolve via model_routing when absent.…** (1 connections) — `src/merged_agentic_swarm/services/swarm_profiles.py`
- **Start a real agentic workflow in a background daemon thread; return now.** (1 connections) — `src/merged_agentic_swarm/webapp.py`

## Relationships

- [Merged Agentic Swarm Blueprint (Root)](Merged_Agentic_Swarm_Blueprint_%28Root%29.md) (8 shared connections)
- [_make_learning_entry](_make_learning_entry.md) (7 shared connections)
- [test_check_streaming_fcc_happy_path](test_check_streaming_fcc_happy_path.md) (5 shared connections)
- [FastFallbackConfig](FastFallbackConfig.md) (5 shared connections)
- [AgentSpec](AgentSpec.md) (4 shared connections)
- [multi_provider_fabric.py](multi_provider_fabric.py.md) (4 shared connections)
- [WorkerRole](WorkerRole.md) (3 shared connections)
- [SubTask](SubTask.md) (2 shared connections)
- [ObstaclePlaybookEngine](ObstaclePlaybookEngine.md) (2 shared connections)
- [swarm_run.py](swarm_run.py.md) (1 shared connections)
- [DurableAgentRouter](DurableAgentRouter.md) (1 shared connections)
- [_router_with_keys](_router_with_keys.md) (1 shared connections)

## Source Files

- `src/merged_agentic_swarm/services/__init__.py`
- `src/merged_agentic_swarm/services/model_routing.py`
- `src/merged_agentic_swarm/services/swarm_profiles.py`
- `src/merged_agentic_swarm/webapp.py`

## Audit Trail

- EXTRACTED: 115 (98%)
- INFERRED: 2 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*