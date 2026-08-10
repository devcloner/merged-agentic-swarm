# Merged Agentic Swarm OS PRD v2

> 13 nodes · cohesion 0.23

## Key Concepts

- **LiteLLM Gateway** (9 connections) — `.github/workflows/opencode-review.yml`
- **OpenCode Review Workflow** (8 connections) — `.github/workflows/opencode-review.yml`
- **OpenCode Scheduled Maintenance Workflow** (8 connections) — `.github/workflows/opencode-scheduled.yml`
- **actions/checkout** (2 connections) — `.github/workflows/opencode-review.yml`
- **anomalyco/opencode/github** (2 connections) — `.github/workflows/opencode-review.yml`
- **GITHUB_TOKEN** (2 connections) — `.github/workflows/opencode-review.yml`
- **LITELLM_MASTER_KEY Secret** (2 connections) — `.github/workflows/opencode-review.yml`
- **OPENCODE_RUNNER Variable** (2 connections) — `.github/workflows/opencode-review.yml`
- **Fast Flash Model** (1 connections) — `.github/workflows/opencode-review.yml`
- **High Throughput Model** (1 connections) — `.github/workflows/opencode-review.yml`
- **Smart Auto Model** (1 connections) — `.github/workflows/opencode-review.yml`
- **OpenCode Maintenance Prompt** (1 connections) — `.github/workflows/opencode-scheduled.yml`
- **OpenCode Review Prompt** (1 connections) — `.github/workflows/opencode-review.yml`

## Relationships

- [ProgressLedgerService](ProgressLedgerService.md) (3 shared connections)
- [CircuitBreaker](CircuitBreaker.md) (1 shared connections)

## Source Files

- `.github/workflows/opencode-review.yml`
- `.github/workflows/opencode-scheduled.yml`

## Audit Trail

- EXTRACTED: 37 (92%)
- INFERRED: 3 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*