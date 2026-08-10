# orchestrator

> 10 nodes · cohesion 0.22

## Key Concepts

- **Multi-Provider Proxy Fabric (Layer 4)** (5 connections) — `docs/agentic/PRD_V2_EXECUTION_READY.md`
- **Baseline Audit of Agentic Orchestration** (4 connections) — `docs/agentic/audit/BASELINE_AUDIT.md`
- **Ultracode Swarm Audit Fleet Manifest** (4 connections) — `docs/fleet-manifests/2026-08-07-ultracode-swarm-audit.md`
- **FCC Server (port 8080, healthy)** (3 connections) — `docs/fleet-manifests/2026-08-07-ultracode-swarm-audit.md`
- **FCC Proxy (port 8080, verified)** (2 connections) — `docs/agentic/audit/BASELINE_AUDIT.md`
- **Critical Port Mismatch (fabric routes 4000 vs actual 8080)** (2 connections) — `docs/agentic/audit/BASELINE_AUDIT.md`
- **Test Coverage Analysis (66% combined)** (2 connections) — `docs/fleet-manifests/2026-08-07-ultracode-swarm-audit.md`
- **LiteLLM port 4000 confirmed dead** (1 connections) — `docs/agentic/audit/BASELINE_AUDIT.md`
- **Registry Integrity Issues (dup IDs, orphan chain)** (1 connections) — `docs/fleet-manifests/2026-08-07-ultracode-swarm-audit.md`
- **Routatic Proxy (port 3456, 300 models)** (1 connections) — `docs/fleet-manifests/2026-08-07-ultracode-swarm-audit.md`

## Relationships

- [ProgressLedgerService](ProgressLedgerService.md) (2 shared connections)
- [role_allocations](role_allocations.md) (1 shared connections)
- [Graphify Pipeline](Graphify_Pipeline.md) (1 shared connections)
- [verify_task_spine.sh](verify_task_spine.sh.md) (1 shared connections)

## Source Files

- `docs/agentic/PRD_V2_EXECUTION_READY.md`
- `docs/agentic/audit/BASELINE_AUDIT.md`
- `docs/fleet-manifests/2026-08-07-ultracode-swarm-audit.md`

## Audit Trail

- EXTRACTED: 20 (80%)
- INFERRED: 5 (20%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*