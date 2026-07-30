# Agent Spec Contract

**Version:** 1.0.0
**Purpose:** Defines the format and location for durable agent specification files.

---

## File Location

Every durable agent created via cold-path promotion must produce a corresponding markdown file at:

```
.claude/agents/{agent_id}.md
```

Where `{agent_id}` is the `id` field from the `agents.jsonl` entry (e.g., `agent-swarm_concurrency-cold-1785418247286`).

---

## File Format

```markdown
# Agent: {name}

- **ID:** {id}
- **Category:** {category}
- **Type:** cold_durable
- **Created:** {promoted_at} (Unix timestamp)
- **Derived from learnings:** {derived_from_learnings}

## System Prompt
{system_prompt}

## Owned Tasks
- {task_tags}

## TTL
{ttl_sec} (null = permanent / no expiry)
```

---

## Field Mapping (from agents.jsonl → .md)

| agents.jsonl field | .md equivalent |
|---|---|
| `name` | Heading `# Agent: {name}` |
| `id` | List item `**ID:** {id}` |
| `category` | List item `**Category:** {category}` |
| `system_prompt` | `## System Prompt` body |
| `derived_from_learnings` | `**Derived from learnings:**` comma-separated |
| `promoted_at` | `**Created:**` formatted timestamp |
| `ttl_sec` | `## TTL` line |

---

## Contract Rules

1. Every entry in `agents.jsonl` MUST have a corresponding `.claude/agents/{id}.md` file.
2. The `.md` file MUST NOT overwrite an existing file — if the agent already has a spec, skip.
3. Missing `.md` files MUST be created on the next cold-path promotion run.
4. Agent files with `ttl_sec: null` are permanent — never auto-delete.
5. Agent files with a numeric `ttl_sec` may be deleted after expiry.
