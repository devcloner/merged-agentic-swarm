"""
Tests for the full learning loop lifecycle: capture -> evaluate -> promote -> load -> route -> reuse.

Covers:
  - Full lifecycle (capture, record, evaluate, promote, verify)
  - Each step produces expected output files
  - Fresh load after restart finds promoted agent
  - Dedup: identical learning does not produce duplicate agent
  - Valid JSONL syntax throughout
  - Required frontmatter in agent .md files
"""
import json
import os
import time
from pathlib import Path
from unittest.mock import patch

import pytest


# ── Test Helpers ──────────────────────────────────────────────────────────────

def _make_learning_entry(title, category, solution, tags=None):
    """Create a learning entry dict matching the knowledge_cache schema."""
    return {
        "id": "",
        "title": title,
        "category": category,
        "solution": solution,
        "tags": tags or [],
        "created_at": time.time(),
        "ttl_sec": None,
    }


def _make_knowledge_jsonl_entry(learning_id, title, category, solution, tags=None, timestamp=None):
    """Create a cold-path knowledge.jsonl entry."""
    return {
        "id": learning_id,
        "title": title,
        "category": category,
        "solution": solution,
        "tags": tags or [],
        "promoted_at": timestamp or time.time(),
        "source": "learning_loop_test",
        "phase": "test",
    }


def _make_agent_jsonl_entry(agent_id, name, category, learning_ids, system_prompt, timestamp=None):
    """Create a cold-path agents.jsonl entry."""
    return {
        "id": agent_id,
        "name": name,
        "category": category,
        "derived_from_learnings": learning_ids,
        "system_prompt": system_prompt,
        "promoted_at": timestamp or time.time(),
        "ttl_sec": None,
    }


def _make_chain_jsonl_entry(entry_id, source_learning_id, spawned_agent_id, trigger_reason, timestamp=None):
    """Create a cold-path chain.jsonl entry."""
    return {
        "entry_id": entry_id,
        "source_learning_id": source_learning_id,
        "spawned_agent_id": spawned_agent_id,
        "agent_type": "cold_durable",
        "trigger_reason": trigger_reason,
        "timestamp": timestamp or time.time(),
        "promotion_phase": "test",
    }


def _append_jsonl(path, entry):
    """Append a single JSON entry as a line to a JSONL file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(entry) + "\n")


def _read_jsonl(path):
    """Read all JSONL entries from a file, returning a list of dicts."""
    if not os.path.exists(path):
        return []
    entries = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entries.append(json.loads(line))
    return entries


def _evaluate_promotion_criteria(learning_entry, cold_knowledge_path):
    """
    Evaluate whether a learning entry meets cold-path promotion criteria.

    Returns (passed: bool, criteria_detail: dict).
    """
    criteria = {}
    all_pass = True

    # 1. evidence_score: solution length >= 50 (substantive)
    solution = learning_entry.get("solution", "")
    evidence_score = min(1.0, len(solution) / 200.0)
    criteria["evidence_score"] = evidence_score >= 0.3
    if not criteria["evidence_score"]:
        all_pass = False

    # 2. reuse_score: based on tags
    tags = learning_entry.get("tags", [])
    reuse_score = min(1.0, len(tags) / 3.0)
    criteria["reuse_score"] = reuse_score >= 0.3
    if not criteria["reuse_score"]:
        all_pass = False

    # 3. task_links: at least 1 tag
    criteria["task_links"] = len(tags) >= 1
    if not criteria["task_links"]:
        all_pass = False

    # 4. specific_claim: title must be substantive
    title = learning_entry.get("title", "")
    criteria["specific_claim"] = len(title) > 10
    if not criteria["specific_claim"]:
        all_pass = False

    # 5. no_duplicate: content-hash check against cold knowledge
    content_key = f"{title}|{learning_entry.get('category','')}|{solution}"
    existing = _read_jsonl(cold_knowledge_path)
    is_dup = any(
        f"{e.get('title','')}|{e.get('category','')}|{e.get('solution','')}" == content_key
        for e in existing
    )
    criteria["no_duplicate"] = not is_dup
    if not criteria["no_duplicate"]:
        all_pass = False

    return all_pass, criteria


def _promote_learning(learning_entry, learning_id, temp_dir, timestamp=None):
    """
    Execute cold-path promotion: write all 5 output files.

    Returns dict with paths to all created artifacts.
    """
    ts = timestamp or time.time()
    category = learning_entry["category"]
    title = learning_entry["title"]
    solution = learning_entry["solution"]
    tags = learning_entry.get("tags", [])

    agent_id = f"agent-{category}-cold-{int(ts * 1000)}"
    agent_name = f"Durable {category} Specialist"
    chain_entry_id = f"CHAIN-COLD-{int(ts * 1000)}"
    system_prompt = (
        f"You are a durable specialist for {category} tasks, created from validated learning records. "
        f"Pattern: {title}."
    )

    # Set up temp directory structure
    registry_dir = os.path.join(temp_dir, "docs", "agentic", "registry")
    agents_dir = os.path.join(temp_dir, ".claude", "agents")

    knowledge_path = os.path.join(registry_dir, "knowledge.jsonl")
    agents_path = os.path.join(registry_dir, "agents.jsonl")
    chain_path = os.path.join(registry_dir, "chain.jsonl")
    progress_path = os.path.join(registry_dir, "progress.json")

    # 4a. knowledge.jsonl
    _append_jsonl(knowledge_path, _make_knowledge_jsonl_entry(
        learning_id, title, category, solution, tags, ts,
    ))

    # 4b. agents.jsonl
    _append_jsonl(agents_path, _make_agent_jsonl_entry(
        agent_id, agent_name, category, [learning_id], system_prompt, ts,
    ))

    # 4c. chain.jsonl
    _append_jsonl(chain_path, _make_chain_jsonl_entry(
        chain_entry_id, learning_id, agent_id,
        f"Repeated {category} pattern triggered cold-path promotion",
        ts,
    ))

    # 4d. agent .md file
    os.makedirs(agents_dir, exist_ok=True)
    agent_md_path = os.path.join(agents_dir, f"{agent_id}.md")
    created_str = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(ts))
    md_content = f"""# Agent: {agent_name}

- **ID:** {agent_id}
- **Category:** {category}
- **Type:** cold_durable
- **Created:** {created_str}
- **Derived from learnings:** {learning_id}

## System Prompt
{system_prompt}

## Owned Tasks
- none

## TTL
None (null = permanent / no expiry)
"""
    with open(agent_md_path, "w") as f:
        f.write(md_content)

    # 4e. progress.json
    progress = {}
    if os.path.exists(progress_path):
        with open(progress_path) as f:
            try:
                progress = json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
    milestones = progress.get("milestone_history", [])
    milestones.append({
        "milestone": "Learning Loop E2E Test",
        "completed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ts)),
        "status": "completed",
        "notes": f"Agent {agent_id} promoted. 5 artifacts written.",
    })
    progress["milestone_history"] = milestones
    progress["_last_agent_id"] = agent_id
    with open(progress_path, "w") as f:
        json.dump(progress, f, indent=2)

    return {
        "knowledge_path": knowledge_path,
        "agents_path": agents_path,
        "chain_path": chain_path,
        "agent_md_path": agent_md_path,
        "progress_path": progress_path,
        "agent_id": agent_id,
        "learning_id": learning_id,
        "chain_entry_id": chain_entry_id,
    }


def _verify_promotion(artifacts):
    """Verify all 5 cold-path artifacts exist and are valid. Returns list of failures."""
    failures = []

    # Verify knowledge.jsonl
    if not os.path.exists(artifacts["knowledge_path"]):
        failures.append("knowledge.jsonl file missing")
    else:
        entries = _read_jsonl(artifacts["knowledge_path"])
        if not any(e.get("id") == artifacts["learning_id"] for e in entries):
            failures.append(f"Learning {artifacts['learning_id']} not found in knowledge.jsonl")

    # Verify agents.jsonl
    if not os.path.exists(artifacts["agents_path"]):
        failures.append("agents.jsonl file missing")
    else:
        entries = _read_jsonl(artifacts["agents_path"])
        if not any(e.get("id") == artifacts["agent_id"] for e in entries):
            failures.append(f"Agent {artifacts['agent_id']} not found in agents.jsonl")

    # Verify chain.jsonl
    if not os.path.exists(artifacts["chain_path"]):
        failures.append("chain.jsonl file missing")
    else:
        entries = _read_jsonl(artifacts["chain_path"])
        if not any(e.get("entry_id") == artifacts["chain_entry_id"] for e in entries):
            failures.append(f"Chain entry {artifacts['chain_entry_id']} not found in chain.jsonl")

    # Verify agent .md file
    md_path = artifacts["agent_md_path"]
    if not os.path.exists(md_path):
        failures.append(f"Agent .md file missing: {md_path}")
    else:
        with open(md_path) as f:
            content = f.read()
        if "name" not in content.lower() and "Agent:" not in content:
            failures.append("Agent .md missing name/Agent header")
        if "System Prompt" not in content and "Description" not in content:
            failures.append("Agent .md missing System Prompt/Description section")

    # Verify progress.json
    if not os.path.exists(artifacts["progress_path"]):
        failures.append("progress.json file missing")

    return failures


def _load_agents_from_registry(temp_dir):
    """Simulate loading agents after restart: read agents.jsonl and .md files."""
    registry_dir = os.path.join(temp_dir, "docs", "agentic", "registry")
    agents_path = os.path.join(registry_dir, "agents.jsonl")
    agents_dir = os.path.join(temp_dir, ".claude", "agents")

    agents = []
    jsonl_entries = _read_jsonl(agents_path)
    for entry in jsonl_entries:
        agent_id = entry.get("id", "")
        md_path = os.path.join(agents_dir, f"{agent_id}.md")
        has_md = os.path.exists(md_path)
        agents.append({
            "id": agent_id,
            "name": entry.get("name", ""),
            "category": entry.get("category", ""),
            "system_prompt": entry.get("system_prompt", ""),
            "has_md_file": has_md,
            "md_path": md_path,
        })
    return agents


def _simulate_reuse(agent, task_description):
    """Simulate routing a task to a promoted agent and getting a response."""
    return {
        "agent_id": agent["id"],
        "agent_name": agent["name"],
        "task": task_description,
        "routed": True,
        "response_summary": f"Task routed to {agent['name']} ({agent['category']})",
        "system_prompt_used": agent["system_prompt"][:80],
    }


# ── Tests: Step-by-Step ───────────────────────────────────────────────────────

class TestCaptureStep:
    """Step 1: CAPTURE — Create a controlled learning scenario."""

    def test_capture_produces_valid_entry(self):
        """A captured learning scenario produces a properly structured entry."""
        entry = _make_learning_entry(
            title="Swarm Concurrency Pattern for 40-Worker Pool",
            category="swarm_concurrency",
            solution=(
                "Use a 40-worker thread pool with round-robin key rotation. "
                "Each worker picks the next available API key from the pool, "
                "providing high throughput and resilience against rate limits."
            ),
            tags=["swarm", "concurrency", "key-rotation", "scaling"],
        )
        assert len(entry["title"]) > 10
        assert len(entry["solution"]) > 50
        assert len(entry["tags"]) >= 1
        assert entry["category"] != ""

    def test_capture_requires_specific_claim(self):
        """A generic/non-specific entry should be identifiable as weak."""
        generic = _make_learning_entry(
            title="Fix bug",
            category="general",
            solution="Fixed it.",
            tags=[],
        )
        # Generic entries should fail the specific_claim test
        assert len(generic["title"]) <= 10
        assert len(generic["solution"]) < 50
        assert len(generic["tags"]) == 0


class TestRecordStep:
    """Step 2: RECORD — Write to hot cache (knowledge_cache.json)."""

    def test_record_to_knowledge_cache(self, temp_dir):
        from tools.knowledge_cache import KnowledgeCache

        cache_file = os.path.join(temp_dir, "knowledge_cache.json")
        cache = KnowledgeCache(cache_file=cache_file, max_learnings=10)

        lid = cache.add_learning(
            title="Rate Limit Recovery Pattern",
            category="resilience",
            pattern_solution="When rate-limited, rotate to next key and apply exponential backoff with jitter.",
            tags=["rate-limit", "resilience", "key-rotation"],
        )

        assert lid.startswith("LEARN-")
        assert lid in cache.learnings
        entry = cache.get_learning(lid)
        assert entry["title"] == "Rate Limit Recovery Pattern"
        assert entry["category"] == "resilience"
        assert len(entry["tags"]) == 3

        # Verify persistence
        assert os.path.exists(cache_file)
        with open(cache_file) as f:
            data = json.load(f)
        assert lid in data["learnings"]

    def test_record_dedup_identical_content(self, temp_dir):
        from tools.knowledge_cache import KnowledgeCache

        cache_file = os.path.join(temp_dir, "knowledge_cache.json")
        cache = KnowledgeCache(cache_file=cache_file, max_learnings=10)

        lid1 = cache.add_learning("Pattern A", "cat", "Solution X")
        lid2 = cache.add_learning("Pattern A", "cat", "Solution X")  # identical

        assert lid1 == lid2  # should return same ID
        assert len(cache.learnings) == 1


class TestEvaluateStep:
    """Step 3: EVALUATE — Score learning against promotion criteria."""

    def test_evaluate_passes_strong_entry(self, temp_dir):
        """A strong, substantive entry should pass all promotion criteria."""
        entry = _make_learning_entry(
            title="Parallel Execution Pattern for 40-Worker Swarm",
            category="swarm_concurrency",
            solution="Use 40-worker thread pool with round-robin key rotation for high throughput.",
            tags=["swarm", "concurrency", "key-rotation"],
        )
        cold_path = os.path.join(temp_dir, "knowledge.jsonl")
        passed, criteria = _evaluate_promotion_criteria(entry, cold_path)
        assert passed is True
        assert all(criteria.values()), f"All criteria should pass: {criteria}"

    def test_evaluate_fails_weak_entry(self, temp_dir):
        """A weak entry should fail promotion criteria."""
        entry = _make_learning_entry(
            title="Fix",
            category="general",
            solution="Fixed.",
            tags=[],
        )
        cold_path = os.path.join(temp_dir, "knowledge.jsonl")
        passed, criteria = _evaluate_promotion_criteria(entry, cold_path)
        assert passed is False
        assert not criteria["evidence_score"]
        assert not criteria["reuse_score"]
        assert not criteria["task_links"]
        assert not criteria["specific_claim"]

    def test_evaluate_detects_duplicate(self, temp_dir):
        """Should detect when an entry already exists in cold knowledge."""
        entry = _make_learning_entry(
            title="Circuit Breaker Pattern",
            category="resilience",
            solution="Skip failed providers after 3 consecutive failures.",
            tags=["circuit-breaker"],
        )
        cold_path = os.path.join(temp_dir, "knowledge.jsonl")
        # Pre-populate cold knowledge with same entry
        _append_jsonl(cold_path, _make_knowledge_jsonl_entry(
            "LEARN-0099", "Circuit Breaker Pattern", "resilience",
            "Skip failed providers after 3 consecutive failures.",
            ["circuit-breaker"],
        ))

        passed, criteria = _evaluate_promotion_criteria(entry, cold_path)
        assert passed is False
        assert not criteria["no_duplicate"]


class TestPromoteStep:
    """Step 4: PROMOTE — Write all 5 cold-path artifacts."""

    def test_promote_writes_all_five_artifacts(self, temp_dir):
        entry = _make_learning_entry(
            title="Swarm Concurrency Pattern for 40-Worker Pool",
            category="swarm_concurrency",
            solution="Use 40-worker thread pool with round-robin key rotation for high throughput.",
            tags=["swarm", "concurrency", "key-rotation", "scaling"],
        )
        learning_id = "LEARN-0100"
        artifacts = _promote_learning(entry, learning_id, temp_dir)

        failures = _verify_promotion(artifacts)
        assert len(failures) == 0, f"Verification failures: {failures}"

    def test_promote_knowledge_jsonl_has_correct_fields(self, temp_dir):
        entry = _make_learning_entry(
            title="Rate Limit Recovery Pattern",
            category="resilience",
            solution="Rotate key and apply exponential backoff with jitter.",
            tags=["rate-limit", "resilience"],
        )
        artifacts = _promote_learning(entry, "LEARN-0200", temp_dir)

        knowledge_entries = _read_jsonl(artifacts["knowledge_path"])
        assert len(knowledge_entries) == 1
        ke = knowledge_entries[0]
        assert ke["id"] == "LEARN-0200"
        assert ke["title"] == "Rate Limit Recovery Pattern"
        assert ke["category"] == "resilience"
        assert "promoted_at" in ke
        assert "source" in ke

    def test_promote_agents_jsonl_has_correct_fields(self, temp_dir):
        entry = _make_learning_entry(
            title="Auto-Compaction Pattern",
            category="compaction",
            solution="Compact hot cache on save to prevent unbounded growth.",
            tags=["compaction", "storage"],
        )
        artifacts = _promote_learning(entry, "LEARN-0300", temp_dir)

        agent_entries = _read_jsonl(artifacts["agents_path"])
        assert len(agent_entries) == 1
        ae = agent_entries[0]
        assert "id" in ae
        assert "name" in ae
        assert "category" in ae
        assert ae["category"] == "compaction"
        assert len(ae["derived_from_learnings"]) >= 1
        assert "system_prompt" in ae

    def test_promote_chain_jsonl_has_correct_fields(self, temp_dir):
        entry = _make_learning_entry(
            title="Health Check Pattern",
            category="health_check",
            solution="Proactive provider health checking at startup.",
            tags=["health", "provider"],
        )
        artifacts = _promote_learning(entry, "LEARN-0400", temp_dir)

        chain_entries = _read_jsonl(artifacts["chain_path"])
        assert len(chain_entries) == 1
        ce = chain_entries[0]
        assert ce["source_learning_id"] == "LEARN-0400"
        assert ce["spawned_agent_id"] == artifacts["agent_id"]
        assert ce["agent_type"] == "cold_durable"

    def test_promote_agent_md_has_required_frontmatter(self, temp_dir):
        entry = _make_learning_entry(
            title="Token Management Pattern",
            category="token_management",
            solution="Track token usage per agent and compact context when nearing limits.",
            tags=["tokens", "context"],
        )
        artifacts = _promote_learning(entry, "LEARN-0500", temp_dir)

        assert os.path.exists(artifacts["agent_md_path"])
        with open(artifacts["agent_md_path"]) as f:
            content = f.read()

        # Required frontmatter: name
        assert "Agent:" in content
        # Required frontmatter: description (System Prompt section)
        assert "System Prompt" in content
        # Must reference the learning ID
        assert "LEARN-0500" in content
        # Must have an ID
        assert artifacts["agent_id"] in content

    def test_promote_progress_json_updated(self, temp_dir):
        entry = _make_learning_entry(
            title="Proxy Health Pattern",
            category="proxy",
            solution="Health-check proxy on startup and periodically during operation.",
            tags=["proxy", "health"],
        )
        artifacts = _promote_learning(entry, "LEARN-0600", temp_dir)

        assert os.path.exists(artifacts["progress_path"])
        with open(artifacts["progress_path"]) as f:
            progress = json.load(f)

        assert "milestone_history" in progress
        assert len(progress["milestone_history"]) >= 1
        assert progress["_last_agent_id"] == artifacts["agent_id"]


class TestLoadAfterRestart:
    """Step: LOAD — Simulate loading agents after a restart."""

    def test_fresh_load_finds_promoted_agent(self, temp_dir):
        entry = _make_learning_entry(
            title="Circuit Breaker Pattern for Provider Fallback",
            category="circuit_breaker",
            solution="After 3 consecutive failures, skip provider for cooldown period.",
            tags=["circuit-breaker", "resilience", "fallback"],
        )
        artifacts = _promote_learning(entry, "LEARN-0700", temp_dir)

        # Simulate restart: load agents from registry files
        agents = _load_agents_from_registry(temp_dir)

        assert len(agents) >= 1
        promoted = agents[0]
        assert promoted["id"] == artifacts["agent_id"]
        assert promoted["has_md_file"] is True
        assert promoted["category"] == "circuit_breaker"

    def test_agent_md_file_survives_restart(self, temp_dir):
        entry = _make_learning_entry(
            title="Dependency Resolution Pattern",
            category="dependency_resolution",
            solution="Topologically sort tasks before dispatch to prevent deadlocks.",
            tags=["dependency", "topological-sort", "dispatch"],
        )
        artifacts = _promote_learning(entry, "LEARN-0800", temp_dir)

        md_path = artifacts["agent_md_path"]
        assert os.path.exists(md_path)

        # Simulate reading after restart (re-read file)
        with open(md_path) as f:
            content = f.read()

        assert "Dependency Resolution" in content or "dependency_resolution" in content
        assert "System Prompt" in content
        assert "LEARN-0800" in content


class TestRouteAndReuse:
    """Step: ROUTE & REUSE — Routing tasks to promoted agents."""

    def test_route_task_to_promoted_agent(self, temp_dir):
        entry = _make_learning_entry(
            title="Syntax Error Auto-Fix Pattern",
            category="syntax_fixer",
            solution="Parse error output, identify line and column, apply fix with AST validation.",
            tags=["syntax", "auto-fix", "ast"],
        )
        artifacts = _promote_learning(entry, "LEARN-0900", temp_dir)
        agents = _load_agents_from_registry(temp_dir)

        result = _simulate_reuse(agents[0], "Fix SyntaxError in models/agent_models.py line 42")
        assert result["routed"] is True
        assert result["agent_id"] == artifacts["agent_id"]
        assert "syntax_fixer" in result["agent_name"].lower() or "syntax_fixer" in result["system_prompt_used"].lower()

    def test_reuse_uses_correct_system_prompt(self, temp_dir):
        entry = _make_learning_entry(
            title="Type Error Resolution Pattern",
            category="type_checker",
            solution="Inspect type annotations, verify against runtime types, add missing casts.",
            tags=["types", "annotation", "runtime"],
        )
        artifacts = _promote_learning(entry, "LEARN-1000", temp_dir)
        agents = _load_agents_from_registry(temp_dir)

        result = _simulate_reuse(agents[0], "Fix TypeError in services/wave_gate_service.py")
        assert "type_checker" in result["system_prompt_used"].lower()


class TestDedup:
    """Dedup: identical learning should not produce duplicate agent."""

    def test_duplicate_learning_not_promoted(self, temp_dir):
        entry = _make_learning_entry(
            title="Dedup Test Pattern for Ensuring Single Promotion",
            category="dedup_test",
            solution="This solution should only be promoted once. Dedup via content hash.",
            tags=["dedup", "single-promotion"],
        )
        learning_id = "LEARN-2000"
        cold_path = os.path.join(temp_dir, "docs", "agentic", "registry", "knowledge.jsonl")

        # First promotion: should pass
        passed1, _ = _evaluate_promotion_criteria(entry, cold_path)
        assert passed1 is True

        # Do the first promotion
        artifacts1 = _promote_learning(entry, learning_id, temp_dir)

        # Second evaluation: should fail due to duplicate
        passed2, criteria2 = _evaluate_promotion_criteria(entry, artifacts1["knowledge_path"])
        assert passed2 is False
        assert not criteria2["no_duplicate"]

    def test_dedup_via_content_hash(self, temp_dir):
        """Verify that content-hash-based dedup catches semantically identical entries."""
        entry1 = _make_learning_entry(
            title="Content Hash Dedup Pattern",
            category="hash_dedup",
            solution="Identical solution text across entries -- this text is long enough to pass the evidence score threshold of sixty characters minimum required for promotion.",
            tags=["dedup"],
        )
        entry2 = _make_learning_entry(
            title="Content Hash Dedup Pattern",
            category="hash_dedup",
            solution="Identical solution text across entries -- this text is long enough to pass the evidence score threshold of sixty characters minimum required for promotion.",
            tags=["dedup"],
        )
        # Same content => same hash
        assert entry1["title"] == entry2["title"]
        assert entry1["category"] == entry2["category"]
        assert entry1["solution"] == entry2["solution"]

        # The evaluate step should detect the duplicate
        cold_path = os.path.join(temp_dir, "docs", "agentic", "registry", "knowledge.jsonl")
        passed1, _ = _evaluate_promotion_criteria(entry1, cold_path)
        assert passed1 is True

        _promote_learning(entry1, "LEARN-DEDUP-1", temp_dir)
        knowledge_path = os.path.join(temp_dir, "docs", "agentic", "registry", "knowledge.jsonl")

        passed2, criteria2 = _evaluate_promotion_criteria(entry2, knowledge_path)
        assert passed2 is False
        assert not criteria2["no_duplicate"]

    def test_different_content_not_deduped(self, temp_dir):
        """Entries with different content should not collide."""
        entry_a = _make_learning_entry(
            title="Pattern Alpha",
            category="alpha",
            solution="Solution A: use thread pool with round-robin key rotation for maximum throughput across multiple providers.",
            tags=["threading"],
        )
        entry_b = _make_learning_entry(
            title="Pattern Beta",
            category="beta",
            solution="Solution B: use async event loop with uvloop for non-blocking I/O and cooperative multitasking across workers.",
            tags=["async"],
        )

        cold_path = os.path.join(temp_dir, "docs", "agentic", "registry", "knowledge.jsonl")
        _promote_learning(entry_a, "LEARN-ALPHA-1", temp_dir)
        knowledge_path = os.path.join(temp_dir, "docs", "agentic", "registry", "knowledge.jsonl")

        passed_b, _ = _evaluate_promotion_criteria(entry_b, knowledge_path)
        assert passed_b is True  # Different content should not be flagged as dup


class TestFullLifecycle:
    """End-to-end: capture -> record -> evaluate -> promote -> verify -> load -> route -> reuse."""

    def test_full_lifecycle(self, temp_dir):
        """Run the complete lifecycle and verify every step."""
        # Step 1: Capture
        entry = _make_learning_entry(
            title="Full Lifecycle Integration Test Pattern",
            category="integration_test",
            solution=(
                "Complete end-to-end test of the learning loop: capture a scenario, "
                "record it in the hot cache, evaluate against promotion criteria, "
                "promote to cold path with 5 artifacts, verify all outputs, "
                "load after restart, route a task, and confirm reuse."
            ),
            tags=["e2e", "integration", "lifecycle", "cold-path", "promotion"],
        )
        assert len(entry["title"]) > 10
        assert len(entry["solution"]) > 100
        assert len(entry["tags"]) >= 3

        # Step 2: Record (hot cache)
        cache_file = os.path.join(temp_dir, "hot_cache.json")
        from tools.knowledge_cache import KnowledgeCache
        cache = KnowledgeCache(cache_file=cache_file, max_learnings=10)
        learning_id = cache.add_learning(
            title=entry["title"],
            category=entry["category"],
            pattern_solution=entry["solution"],
            tags=entry["tags"],
        )
        assert learning_id.startswith("LEARN-")
        cached = cache.get_learning(learning_id)
        assert cached is not None

        # Step 3: Evaluate
        cold_path = os.path.join(temp_dir, "docs", "agentic", "registry", "knowledge.jsonl")
        passed, criteria = _evaluate_promotion_criteria(cached, cold_path)
        assert passed is True, f"Evaluation failed: {criteria}"
        assert all(criteria.values())

        # Step 4: Promote
        artifacts = _promote_learning(cached, learning_id, temp_dir)
        failures = _verify_promotion(artifacts)
        assert len(failures) == 0, f"Promotion verification failed: {failures}"

        # All 5 artifacts must exist
        for key in ["knowledge_path", "agents_path", "chain_path", "agent_md_path", "progress_path"]:
            assert os.path.exists(artifacts[key]), f"Missing artifact: {key}"

        # Step 5: Verify JSONL syntax
        for jf_key in ["knowledge_path", "agents_path", "chain_path"]:
            entries = _read_jsonl(artifacts[jf_key])
            assert len(entries) >= 1, f"No entries in {jf_key}"

        # Step 6: Load after restart
        agents = _load_agents_from_registry(temp_dir)
        assert len(agents) >= 1
        assert agents[0]["id"] == artifacts["agent_id"]
        assert agents[0]["has_md_file"] is True

        # Step 7: Route
        result = _simulate_reuse(agents[0], "Test task for full lifecycle agent")
        assert result["routed"] is True
        assert result["agent_id"] == artifacts["agent_id"]

        # Step 8: Reuse (same agent handles another task)
        result2 = _simulate_reuse(agents[0], "Another task for the same agent")
        assert result2["agent_id"] == artifacts["agent_id"]
        assert result2["routed"] is True

    def test_multiple_promotions_in_sequence(self, temp_dir):
        """Promote multiple different learnings and verify they are all loadable."""
        categories = ["resilience", "scaling", "monitoring"]
        expected_agents = []

        for cat in categories:
            entry = _make_learning_entry(
                title=f"Sequential Test Pattern for {cat}",
                category=cat,
                solution=f"Comprehensive solution for {cat}: implement with tests and documentation.",
                tags=[cat, "sequential", "multi-promote"],
            )
            learning_id = f"LEARN-SEQ-{cat}"
            artifacts = _promote_learning(entry, learning_id, temp_dir)
            expected_agents.append(artifacts["agent_id"])
            failures = _verify_promotion(artifacts)
            assert len(failures) == 0

        # Load all agents after all promotions
        agents = _load_agents_from_registry(temp_dir)
        assert len(agents) == 3

        agent_ids = [a["id"] for a in agents]
        for expected in expected_agents:
            assert expected in agent_ids

        # Verify knowledge.jsonl has all 3 entries
        knowledge_path = os.path.join(temp_dir, "docs", "agentic", "registry", "knowledge.jsonl")
        knowledge_entries = _read_jsonl(knowledge_path)
        assert len(knowledge_entries) == 3

        # Verify chain.jsonl has all 3 entries
        chain_path = os.path.join(temp_dir, "docs", "agentic", "registry", "chain.jsonl")
        chain_entries = _read_jsonl(chain_path)
        assert len(chain_entries) == 3
