# Durable Agent Routing Hook — Verification

**Date**: 2026-07-31T12:38:00Z
**Component**: `services/opencode_swarm_service.py`
**Status**: ✅ VERIFIED USED

---

## Implementation

### DurableAgentRouter class

Added to `services/opencode_swarm_service.py` lines 28-237.

**Methods**:
- `load()` — Loads agents from `agents.jsonl` (registry) and `.claude/agents/*.md` (frontmatter). Returns agent count.
- `find_matching_agent(task: SubTask) -> dict | None` — Matches a subtask against loaded agents by category + keyword overlap.
- `get_stats() -> dict` — Returns router statistics for reporting.
- `_extract_keywords(text) -> set[str]` — Extracts lowercase tokens, dropping stop words.
- `_scan_agent_triggers(agent) -> set[str]` — Collects trigger keywords from agent body + system_prompt.

**Scoring**:
- Category match: +2.0
- Per keyword overlap: +1.0
- Minimum threshold: 1.0

### Routing Hook (in `execute_subtask_with_worker`)

Before dispatching to a generic worker:
1. Call `get_durable_router().find_matching_agent(subtask)`
2. If matched (score ≥ MIN_SCORE): use agent's `system_prompt` + body as the system prompt, set `worker_id = "durable-agent:<id>"`
3. If no match: fall through to generic round-robin worker
4. Router failure is caught — never blocks dispatch
5. Response includes `routed_agent` and `routed_agent_score` when routed

### Global Singleton

```python
def get_durable_router() -> DurableAgentRouter:
    """Lazy-initialised singleton."""
```

---

## Verification

### Router Stats
```
Total agents: 14
Categories: swarm_concurrency, verification, threshold_test, single_agent_cat, learning_loop_test, code_generation
```

### Match Test: "Validate email input with regex" (category=code_generation)
```
✅ ROUTED: Durable Regex Validation Specialist (Verified)
   id=agent-validation-regex-vfy-1785495956, score=6.0
```

### Match Test: "Something completely random" (category=nonexistent)
```
✅ Correctly NO MATCH
```

### Full Dispatch Test
```json
{
  "status": "completed",
  "worker_id": "durable-agent:agent-validation-regex-vfy-1785495956",
  "routed_agent": "agent-validation-regex-vfy-1785495956",
  "routed_agent_score": 6.0
}
```

---

## Files Changed

| File | Change |
|:-----|:-------|
| `services/opencode_swarm_service.py` | Added `DurableAgentRouter` class (~210 lines), modified `execute_subtask_with_worker` to route through matching durable agents |

---

## Residual Risks

- **Provider dependency**: Routing does not change the provider chain. If all providers timeout (as currently), even routed tasks fall to simulation.
- **Cold start**: On first dispatch, the router loads agents from disk (~200ms for 14 agents). Subsequent calls use in-memory cache.
- **Score tuning**: The weights (W_CATEGORY=2.0, W_KEYWORD=1.0, MIN_SCORE=1.0) are reasonable defaults. Production may need tuning with real task volume.
