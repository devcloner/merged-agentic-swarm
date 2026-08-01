"""Phase 5: Durable Learning Loop End-to-End Verification"""
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from merged_agentic_swarm.tools.agentic_orchestrator import MultiLayeredAgenticOrchestrator
from merged_agentic_swarm.tools.knowledge_cache import default_knowledge_cache
from merged_agentic_swarm.services.agent_factory_service import DurableAgentFactory

REG_DIR = Path("docs/agentic/registry")
AGENTS_DIR = Path(os.path.expanduser("~/.claude/agents"))

print("=" * 60)
print("PHASE 5: DURABLE LEARNING LOOP E2E VERIFICATION")
print("=" * 60)

# ── Step 1: Capture learnings ──
print("\n── Step 1: Capture learnings in hot cache ──")
orch = MultiLayeredAgenticOrchestrator(prd_title="Learning Loop E2E Test")

learnings = [
    ("Mistral 429 Rate-Limit Recovery Pattern", "provider-resilience",
     "When Mistral returns HTTP 429, read Retry-After header. Wait that duration (default 5s). "
     "Retry with exponential backoff: 1s, 2s, 4s. Max 3 retries. Log each attempt.",
     ["mistral", "rate-limit", "429", "retry"]),
    ("Mistral 5xx Circuit Breaker Strategy", "provider-resilience",
     "After 3 consecutive 5xx errors from Mistral, open circuit breaker for 120s. "
     "Route traffic to fallback provider. Log all breaker state transitions.",
     ["mistral", "circuit-breaker", "5xx", "fallback"]),
    ("Mistral Key Rotation Load Balancing", "provider-resilience",
     "Use least-used key selection. Track tokens per key. Rotate when approaching rate limits. "
     "Balance load across available keys with weighted round-robin.",
     ["mistral", "key-rotation", "load-balancing"]),
]

for title, cat, sol, tags in learnings:
    eid = default_knowledge_cache.add_learning(title=title, category=cat, pattern_solution=sol, tags=tags)
    print(f"  Added: {eid}")

print(f"  Hot cache size: {len(default_knowledge_cache.learnings)}")

# ── Step 2: Promote cold path ──
print("\n── Step 2: Promote cold path ──")
default_knowledge_cache.load_cache()
result = orch._promote_cold_path()
print(f"  Knowledge promoted: {result.get('promoted_knowledge', 0)}")
print(f"  Agents promoted: {result.get('promoted_agents', 0)}")

# ── Step 3: Check files written to disk ──
print("\n── Step 3: Files written to disk ──")
for name in ["knowledge.jsonl", "agents.jsonl", "chain.jsonl"]:
    path = REG_DIR / name
    lines = len(path.read_text().splitlines()) if path.exists() else 0
    print(f"  {name}: {lines} lines")

agent_files = list(AGENTS_DIR.glob("*.md")) if AGENTS_DIR.exists() else []
print(f"  .claude/agents/: {len(agent_files)} .md files")
for af in agent_files:
    content = af.read_text()
    print(f"    → {af.name} ({len(content)} bytes)")
    if content.startswith("---"):
        end = content.find("---", 3)
        if end > 0:
            for line in content[3:end].strip().split("\n"):
                print(f"       {line.strip()}")

# ── Step 4: Simulate restart — re-instantiate factory ──
print("\n── Step 4: Simulate restart — re-load factory ──")
factory2 = DurableAgentFactory()
print(f"  Hot specialists loaded: {len(factory2.active_hot_specialists)}")
print(f"  Cold durable agents loaded: {len(factory2.active_cold_agents)}")
for agent_id, spec in factory2.active_cold_agents.items():
    print(f"    → {agent_id}: {spec.name} (role={spec.role.value})")

# ── Step 5: Summary ──
print("\n── Step 5: Summary ──")
promoted = result.get("promoted_agents", 0)
agent_files_count = len(agent_files)
registry_entries = sum(1 for _ in (REG_DIR / "agents.jsonl").read_text().splitlines()) if (REG_DIR / "agents.jsonl").exists() else 0
cold_agents = len(factory2.active_cold_agents)

checks = {
    "Learnings added to hot cache": len(default_knowledge_cache.learnings) >= 3,
    "Cold-path learnings promoted": result.get("promoted_knowledge", 0) > 0,
    "Durable agent promoted": promoted > 0,
    "Agent .md file on disk": agent_files_count > 0,
    "Registry entries (agents.jsonl)": registry_entries > 0,
    "Agent survives restart (cold dict)": cold_agents > 0,
}
all_pass = all(checks.values())
print(f"  Status: {'PASSED' if all_pass else 'PARTIAL'}")
for check, passed in checks.items():
    print(f"    {'✓' if passed else '✗'} {check}")

sys.exit(0 if all_pass else 1)
