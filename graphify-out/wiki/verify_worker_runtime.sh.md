# verify_worker_runtime.sh

> 8 nodes · cohesion 0.32

## Key Concepts

- **.handle_task_failure()** (5 connections) — `src/merged_agentic_swarm/services/progress_ledger_service.py`
- **.log_progress()** (5 connections) — `src/merged_agentic_swarm/services/progress_ledger_service.py`
- **.match_and_remediate()** (4 connections) — `src/merged_agentic_swarm/services/progress_ledger_service.py`
- **.record_success_marker()** (3 connections) — `src/merged_agentic_swarm/services/progress_ledger_service.py`
- **.save_ledger()** (3 connections) — `src/merged_agentic_swarm/services/progress_ledger_service.py`
- **Any** (3 connections)
- **Processes a task failure through self-healing playbooks.** (1 connections) — `src/merged_agentic_swarm/services/progress_ledger_service.py`
- **Matches error against playbooks and applies self-healing strategy.** (1 connections) — `src/merged_agentic_swarm/services/progress_ledger_service.py`

## Relationships

- [TestRunFullAgenticWorkflow](TestRunFullAgenticWorkflow.md) (4 shared connections)
- [ProgressLogEntry](ProgressLogEntry.md) (2 shared connections)
- [_evaluate_promotion_criteria](_evaluate_promotion_criteria.md) (1 shared connections)

## Source Files

- `src/merged_agentic_swarm/services/progress_ledger_service.py`

## Audit Trail

- EXTRACTED: 25 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*