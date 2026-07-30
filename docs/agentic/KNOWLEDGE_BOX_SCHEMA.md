# Knowledge Box Schema

**Version:** 1.0.0
**Purpose:** Defines the JSONL schema for cold-path knowledge entries.

---

## File Location

```
docs/agentic/registry/knowledge.jsonl
```

---

## Schema

Each line is a JSON object with the following fields:

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Unique identifier (e.g., `LEARN-0001`). Auto-incrementing. |
| `title` | string | yes | Human-readable pattern title. MUST be unique per category. |
| `category` | string | yes | Classification category. One of the defined categories (see below). |
| `solution` | string | yes | Specific, actionable solution or pattern description. NOT generic boilerplate. |
| `tags` | array[string] | yes | Searchable tags for discovery. At least 1 tag required. |
| `promoted_at` | float | yes | Unix timestamp of promotion to cold-path. |
| `source` | string | no | Source of the knowledge: `orchestrator_cold_path`, `anomaly_detection`, `manual`. Default: `orchestrator_cold_path`. |
| `phase` | string | no | Phase label (e.g., `wave_2`, `wave_3_final`, `manual_cli`). |

---

## Example Entry

```json
{
  "id": "LEARN-0001",
  "title": "Multi-provider fallback timeout configuration",
  "category": "provider_fabric",
  "solution": "Set 5s timeout for localhost (litellm proxy) and 10s for external providers. After 3 consecutive failures, circuit-breaker adds 120s cooldown. 401/403 errors trigger permanent blacklist.",
  "tags": ["provider", "fabric", "timeout", "circuit-breaker"],
  "promoted_at": 1785421371.4449553,
  "source": "orchestrator_cold_path",
  "phase": "wave_2"
}
```

---

## Categories

| Category | Description |
|---|---|
| `swarm_concurrency` | Worker pool management, threading, parallel execution |
| `wave_gating` | Phase gates, pre-condition verification, sequential advancement |
| `knowledge_promotion` | Cold-path pipeline, registry management, dedup |
| `codebase_analysis` | AST scanning, spec gap detection, repository mapping |
| `provider_fabric` | Multi-provider routing, circuit breakers, timeouts, fallback |
| `verification` | Syntax checks, CI passes, import chain validation |
| `anomaly` | Runtime errors, rate limits, unexpected failures |
| `general` | Default fallback — should be used as last resort |

---

## Dedup Rules

1. No two entries with the same `id` may exist in the registry.
2. Before appending a new entry, scan existing entries for matching `id`.
3. If `id` matches: skip the append (do not create a duplicate).
4. If `title + category` matches: the entry is a duplicate of existing knowledge. Skip the append and log a warning.
5. Periodic compaction pass: group by `id`, keep only the LAST occurrence.

---

## Integrity Rules

1. All `id` values referenced in `agents.jsonl` field `derived_from_learnings` MUST exist in `knowledge.jsonl`.
2. All `source_learning_id` values in `chain.jsonl` MUST exist in `knowledge.jsonl`.
3. Cross-registry integrity check should run after each promotion cycle.
