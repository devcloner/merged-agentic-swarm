# run_learning_loop_test.sh

> 10 nodes · cohesion 0.20

## Key Concepts

- **test_learning_loop.py** (20 connections) — `tests/test_learning_loop.py`
- **TestLoadAfterRestart** (5 connections) — `tests/test_learning_loop.py`
- **_make_knowledge_jsonl_entry()** (4 connections) — `tests/test_learning_loop.py`
- **_make_agent_jsonl_entry()** (3 connections) — `tests/test_learning_loop.py`
- **_make_chain_jsonl_entry()** (3 connections) — `tests/test_learning_loop.py`
- **Tests for the full learning loop lifecycle: capture -> evaluate -> promote ->…** (1 connections) — `tests/test_learning_loop.py`
- **Create a cold-path knowledge.jsonl entry.** (1 connections) — `tests/test_learning_loop.py`
- **Create a cold-path agents.jsonl entry.** (1 connections) — `tests/test_learning_loop.py`
- **Step: LOAD — Simulate loading agents after a restart.** (1 connections) — `tests/test_learning_loop.py`
- **Create a cold-path chain.jsonl entry.** (1 connections) — `tests/test_learning_loop.py`

## Relationships

- [report_service.py](report_service.py.md) (9 shared connections)
- [StreamingProxyConfig](StreamingProxyConfig.md) (4 shared connections)
- [Merged Agentic Swarm OS Progress Report](Merged_Agentic_Swarm_OS_Progress_Report.md) (4 shared connections)
- [_load_registry](_load_registry.md) (2 shared connections)
- [KnowledgeCache](KnowledgeCache.md) (2 shared connections)
- [TestRunPlan](TestRunPlan.md) (1 shared connections)

## Source Files

- `tests/test_learning_loop.py`

## Audit Trail

- EXTRACTED: 39 (98%)
- INFERRED: 1 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*