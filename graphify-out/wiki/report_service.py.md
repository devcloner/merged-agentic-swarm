# report_service.py

> 21 nodes · cohesion 0.18

## Key Concepts

- **_make_learning_entry()** (22 connections) — `tests/test_learning_loop.py`
- **_promote_learning()** (21 connections) — `tests/test_learning_loop.py`
- **TestPromoteStep** (9 connections) — `tests/test_learning_loop.py`
- **TestDedup** (6 connections) — `tests/test_learning_loop.py`
- **.test_dedup_via_content_hash()** (5 connections) — `tests/test_learning_loop.py`
- **.test_different_content_not_deduped()** (5 connections) — `tests/test_learning_loop.py`
- **.test_duplicate_learning_not_promoted()** (4 connections) — `tests/test_learning_loop.py`
- **.test_fresh_load_finds_promoted_agent()** (4 connections) — `tests/test_learning_loop.py`
- **.test_promote_agents_jsonl_has_correct_fields()** (4 connections) — `tests/test_learning_loop.py`
- **.test_promote_chain_jsonl_has_correct_fields()** (4 connections) — `tests/test_learning_loop.py`
- **.test_promote_knowledge_jsonl_has_correct_fields()** (4 connections) — `tests/test_learning_loop.py`
- **.test_promote_writes_all_five_artifacts()** (4 connections) — `tests/test_learning_loop.py`
- **.test_agent_md_file_survives_restart()** (3 connections) — `tests/test_learning_loop.py`
- **.test_promote_agent_md_has_required_frontmatter()** (3 connections) — `tests/test_learning_loop.py`
- **.test_promote_progress_json_updated()** (3 connections) — `tests/test_learning_loop.py`
- **Execute cold-path promotion: write all 5 output files. Returns dict with paths…** (1 connections) — `tests/test_learning_loop.py`
- **Create a learning entry dict matching the knowledge_cache schema.** (1 connections) — `tests/test_learning_loop.py`
- **Step 4: PROMOTE — Write all 5 cold-path artifacts.** (1 connections) — `tests/test_learning_loop.py`
- **Dedup: identical learning should not produce duplicate agent.** (1 connections) — `tests/test_learning_loop.py`
- **Verify that content-hash-based dedup catches semantically identical entries.** (1 connections) — `tests/test_learning_loop.py`
- **Entries with different content should not collide.** (1 connections) — `tests/test_learning_loop.py`

## Relationships

- [run_learning_loop_test.sh](run_learning_loop_test.sh.md) (9 shared connections)
- [Merged Agentic Swarm OS Progress Report](Merged_Agentic_Swarm_OS_Progress_Report.md) (9 shared connections)
- [StreamingProxyConfig](StreamingProxyConfig.md) (7 shared connections)
- [_load_registry](_load_registry.md) (4 shared connections)
- [TestRunPlan](TestRunPlan.md) (2 shared connections)
- [KnowledgeCache](KnowledgeCache.md) (2 shared connections)

## Source Files

- `tests/test_learning_loop.py`

## Audit Trail

- EXTRACTED: 105 (98%)
- INFERRED: 2 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*