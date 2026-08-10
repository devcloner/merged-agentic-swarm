---
type: community
cohesion: 0.33
members: 7
---

# CI test job

**Cohesion:** 0.33 - loosely connected
**Members:** 7 nodes

## Members
- [[CI test job]] - code - .github/workflows/ci.yml
- [[Cross-platform check job]] - code - .github/workflows/matrix-ci.yml
- [[Import-chain smoke script]] - code - .github/workflows/ci.yml
- [[Ruff lint and format check]] - code - .github/workflows/ci.yml
- [[merged_agentic_swarm import check]] - code - .github/workflows/matrix-ci.yml
- [[uv dependency sync]] - code - .github/workflows/ci.yml
- [[uv dependency sync (matrix)]] - code - .github/workflows/matrix-ci.yml

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/CI_test_job
SORT file.name ASC
```
