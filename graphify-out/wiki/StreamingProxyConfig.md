# StreamingProxyConfig

> 12 nodes · cohesion 0.20

## Key Concepts

- **_evaluate_promotion_criteria()** (10 connections) — `tests/test_learning_loop.py`
- **TestEvaluateStep** (6 connections) — `tests/test_learning_loop.py`
- **.test_evaluate_detects_duplicate()** (6 connections) — `tests/test_learning_loop.py`
- **_append_jsonl()** (4 connections) — `tests/test_learning_loop.py`
- **.test_evaluate_fails_weak_entry()** (4 connections) — `tests/test_learning_loop.py`
- **.test_evaluate_passes_strong_entry()** (4 connections) — `tests/test_learning_loop.py`
- **Step 3: EVALUATE — Score learning against promotion criteria.** (1 connections) — `tests/test_learning_loop.py`
- **A strong, substantive entry should pass all promotion criteria.** (1 connections) — `tests/test_learning_loop.py`
- **A weak entry should fail promotion criteria.** (1 connections) — `tests/test_learning_loop.py`
- **Should detect when an entry already exists in cold knowledge.** (1 connections) — `tests/test_learning_loop.py`
- **Append a single JSON entry as a line to a JSONL file.** (1 connections) — `tests/test_learning_loop.py`
- **Evaluate whether a learning entry meets cold-path promotion criteria. Returns…** (1 connections) — `tests/test_learning_loop.py`

## Relationships

- [report_service.py](report_service.py.md) (7 shared connections)
- [run_learning_loop_test.sh](run_learning_loop_test.sh.md) (4 shared connections)
- [Merged Agentic Swarm OS Progress Report](Merged_Agentic_Swarm_OS_Progress_Report.md) (2 shared connections)
- [KnowledgeCache](KnowledgeCache.md) (1 shared connections)

## Source Files

- `tests/test_learning_loop.py`

## Audit Trail

- EXTRACTED: 39 (98%)
- INFERRED: 1 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*