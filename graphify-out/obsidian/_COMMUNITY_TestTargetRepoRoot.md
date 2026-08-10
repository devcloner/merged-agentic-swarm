---
type: community
cohesion: 0.38
members: 7
---

# TestTargetRepoRoot

**Cohesion:** 0.38 - loosely connected
**Members:** 7 nodes

## Members
- [[dot-_target_repo_root()]] - code - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[dot-test_defaults_to_existing_sibling_or_cwd()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_env_var_wins()]] - code - tests/test_opencode_swarm_service.py
- [[dot-test_getcwd_fallback()]] - code - tests/test_opencode_swarm_service.py
- [[Resolve the working repo the swarm writes into. ``SWARM_TARGET_REPO`` env var…]] - rationale - src/merged_agentic_swarm/services/opencode_swarm_service.py
- [[TestTargetRepoRoot]] - code - tests/test_opencode_swarm_service.py
- [[When SWARM_TARGET_REPO is unset and no sibling target repo exists,…]] - rationale - tests/test_opencode_swarm_service.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/TestTargetRepoRoot
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_WorkerRole]]
- 2 edges to [[_COMMUNITY_DurableAgentRouter]]
- 2 edges to [[_COMMUNITY_OpenCodeSwarmManager]]
- 1 edge to [[_COMMUNITY_PRDAnalysisResult]]
- 1 edge to [[_COMMUNITY_SubTask]]
- 1 edge to [[_COMMUNITY_ConcurrencyRampController]]

## Top bridge nodes
- [[TestTargetRepoRoot]] - degree 11, connects to 6 communities
- [[dot-_target_repo_root()]] - degree 6, connects to 2 communities