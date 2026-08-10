# TestLatencyTest

> 7 nodes · cohesion 0.33

## Key Concepts

- **CI test job** (3 connections) — `.github/workflows/ci.yml`
- **Import-chain smoke script** (2 connections) — `.github/workflows/ci.yml`
- **uv dependency sync** (2 connections) — `.github/workflows/ci.yml`
- **Cross-platform check job** (2 connections) — `.github/workflows/matrix-ci.yml`
- **merged_agentic_swarm import check** (2 connections) — `.github/workflows/matrix-ci.yml`
- **uv dependency sync (matrix)** (2 connections) — `.github/workflows/matrix-ci.yml`
- **Ruff lint and format check** (1 connections) — `.github/workflows/ci.yml`

## Relationships

- No strong cross-community connections detected

## Source Files

- `.github/workflows/ci.yml`
- `.github/workflows/matrix-ci.yml`

## Audit Trail

- EXTRACTED: 10 (71%)
- INFERRED: 4 (29%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*