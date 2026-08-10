# TestRunPlan

> 6 nodes · cohesion 0.33

## Key Concepts

- **TestCaptureStep** (5 connections) — `tests/test_learning_loop.py`
- **.test_capture_produces_valid_entry()** (3 connections) — `tests/test_learning_loop.py`
- **.test_capture_requires_specific_claim()** (3 connections) — `tests/test_learning_loop.py`
- **Step 1: CAPTURE — Create a controlled learning scenario.** (1 connections) — `tests/test_learning_loop.py`
- **A captured learning scenario produces a properly structured entry.** (1 connections) — `tests/test_learning_loop.py`
- **A generic/non-specific entry should be identifiable as weak.** (1 connections) — `tests/test_learning_loop.py`

## Relationships

- [report_service.py](report_service.py.md) (2 shared connections)
- [KnowledgeCache](KnowledgeCache.md) (1 shared connections)
- [run_learning_loop_test.sh](run_learning_loop_test.sh.md) (1 shared connections)

## Source Files

- `tests/test_learning_loop.py`

## Audit Trail

- EXTRACTED: 13 (93%)
- INFERRED: 1 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*