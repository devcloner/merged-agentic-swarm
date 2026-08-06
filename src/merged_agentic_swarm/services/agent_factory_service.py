"""
Durable Agent Factory & Knowledge-Box -> Spawn Chain Registry
Turns validated learnings into HOT micro-specialists or COLD durable agents, maintaining a persistent chain registry.
"""

import json
import logging
import os
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from merged_agentic_swarm.models.agent_models import AgentSpec, AgentType, SpawnChainEntry, WorkerRole
from merged_agentic_swarm.tools.knowledge_cache import default_knowledge_cache

logger = logging.getLogger("agent_factory")


class ChainRegistry:
    def __init__(self, registry_file: str | None = None):
        if registry_file is None:
            registry_file = os.path.expanduser("~/.taskmaster/tasks/spawn_chain_registry.json")
        self.registry_file = registry_file
        self.entries: list[SpawnChainEntry] = []
        self.load_registry()

    def load_registry(self):
        if os.path.exists(self.registry_file):
            try:
                with open(self.registry_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.entries = [
                        SpawnChainEntry(
                            entry_id=d["entry_id"],
                            source_learning_id=d["source_learning_id"],
                            spawned_agent_id=d["spawned_agent_id"],
                            agent_type=AgentType(d["agent_type"]),
                            trigger_reason=d["trigger_reason"],
                            parent_entry_id=d.get("parent_entry_id"),
                            timestamp=d.get("timestamp", time.time()),
                        )
                        for d in data
                    ]
            except Exception as e:
                logger.error(f"Failed loading spawn chain registry: {e}")

    def save_registry(self):
        os.makedirs(os.path.dirname(self.registry_file), exist_ok=True)
        try:
            with open(self.registry_file, "w", encoding="utf-8") as f:
                json.dump([e.to_dict() for e in self.entries], f, indent=2)
        except Exception as e:
            logger.error(f"Failed saving spawn chain registry: {e}")

    def register_spawn(
        self,
        source_learning_id: str,
        spawned_agent_id: str,
        agent_type: AgentType,
        trigger_reason: str,
        parent_entry_id: str | None = None,
    ) -> SpawnChainEntry:
        entry = SpawnChainEntry(
            entry_id=f"CHAIN-{len(self.entries) + 1:04d}",
            source_learning_id=source_learning_id,
            spawned_agent_id=spawned_agent_id,
            agent_type=agent_type,
            trigger_reason=trigger_reason,
            parent_entry_id=parent_entry_id,
        )
        self.entries.append(entry)
        self.save_registry()
        logger.info(f"Registered spawn chain entry {entry.entry_id}: {agent_type.value} agent {spawned_agent_id}")
        return entry


class DurableAgentFactory:
    def __init__(self, chain_registry: ChainRegistry | None = None):
        self.chain_registry = chain_registry or ChainRegistry()
        self.active_hot_specialists: dict[str, AgentSpec] = {}
        self.active_cold_agents: dict[str, AgentSpec] = {}
        self._load_cold_agents_from_registry()

    def purge_expired(self) -> int:
        """Remove and return count of expired HOT micro-specialists (FIX-09)."""
        now = time.time()
        expired_ids = [aid for aid, spec in self.active_hot_specialists.items() if spec.is_expired]
        for aid in expired_ids:
            expired = self.active_hot_specialists.pop(aid, None)
            if expired:
                logger.info(f"Purged expired HOT agent {aid} (lived {now - expired.created_at:.1f}s)")
        return len(expired_ids)

    def _load_cold_agents_from_registry(self):
        """Load durable agents from the cold-path agents.jsonl registry.

        Called once at init so a fresh process discovers agents promoted by
        previous runs — this is the key restart-survival path.
        """
        import json

        agents_registry = os.path.expanduser("~/.config/merged-agentic-swarm/agents.jsonl")
        if not os.path.exists(agents_registry):
            # Fallback to repo-relative path (file is at src/merged_agentic_swarm/services/)
            repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            agents_registry = os.path.join(repo_root, "docs", "agentic", "registry", "agents.jsonl")
        if not os.path.exists(agents_registry):
            logger.debug("No agents.jsonl found; no durable agents to load.")
            return

        try:
            with open(agents_registry) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    spec_dict = json.loads(line)
                    agent_id = spec_dict.get("id", "")
                    if agent_id and spec_dict.get("ttl_sec") is None:  # durable — no TTL
                        role_str = spec_dict.get("role", "core_engineer")
                        try:
                            role = WorkerRole(role_str)
                        except ValueError:
                            role = WorkerRole.CORE_ENGINEER
                        spec = AgentSpec(
                            id=agent_id,
                            name=spec_dict.get("name", agent_id),
                            role=role,
                            agent_type=AgentType.COLD_DURABLE,
                            system_prompt=spec_dict.get("system_prompt", ""),
                            created_at=spec_dict.get("promoted_at", 0.0),
                            ttl_sec=None,  # durable
                        )
                        self.active_cold_agents[agent_id] = spec
            logger.info(f"Loaded {len(self.active_cold_agents)} durable agents from {agents_registry}")
        except Exception as e:
            logger.warning(f"Failed to load durable agents from {agents_registry}: {e}")

    def _write_agent_spec_file(self, agent_spec: dict[str, Any]) -> str | None:
        """Write an agent spec .md file from a JSONL entry.

        Returns the file path, or None if the file already exists (skipped).
        """
        agent_id = agent_spec.get("id", "")
        agents_dir = os.path.join(os.path.expanduser("~"), ".claude", "agents")
        file_path = os.path.join(agents_dir, f"{agent_id}.md")

        if os.path.exists(file_path):
            logger.info(f"Agent spec file already exists, skipping: {file_path}")
            return None

        os.makedirs(agents_dir, exist_ok=True)

        name = agent_spec.get("name", agent_id)
        category = agent_spec.get("category", "uncategorized")
        agent_type = agent_spec.get("type", "cold_durable")
        promoted_at = agent_spec.get("promoted_at", 0.0)
        try:
            created_str = datetime.fromtimestamp(promoted_at, tz=UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
        except (OSError, ValueError):
            created_str = str(promoted_at)

        derived = agent_spec.get("derived_from_learnings", [])
        if isinstance(derived, list):
            derived_str = ", ".join(derived)
        else:
            derived_str = str(derived)

        system_prompt = agent_spec.get("system_prompt", "")

        task_tags = agent_spec.get("task_tags")
        if task_tags is None:
            task_tags = "none"

        ttl_sec = agent_spec.get("ttl_sec", "null")
        ttl_display = (
            f"{ttl_sec} (null = permanent / no expiry)" if ttl_sec is None or ttl_sec == "null" else str(ttl_sec)
        )

        content = f"""# Agent: {name}

- **ID:** {agent_id}
- **Category:** {category}
- **Type:** {agent_type}
- **Created:** {created_str}
- **Derived from learnings:** {derived_str}

## System Prompt
{system_prompt}

## Owned Tasks
- {task_tags}

## TTL
{ttl_display}
"""

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info(f"Wrote agent spec file: {file_path}")
        return file_path

    def sync_agent_specs(self) -> int:
        """Read agents.jsonl and write spec files for every entry.

        Returns the count of files actually created (skipped pre-existing files
        are not counted).
        """
        _repo_root = Path(__file__).resolve().parents[3]
        registry_path = str(_repo_root / "docs" / "agentic" / "registry" / "agents.jsonl")
        count = 0
        if not os.path.exists(registry_path):
            logger.warning(f"Agent registry not found: {registry_path}")
            return count

        with open(registry_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse JSONL line: {e}")
                    continue
                result = self._write_agent_spec_file(entry)
                if result is not None:
                    count += 1

        logger.info(f"synced {count} new agent spec file(s)")
        return count

    def spawn_from_learning(
        self, learning_id: str, trigger_reason: str, force_type: AgentType | None = None
    ) -> AgentSpec:
        """Evaluates validated learning from Knowledge-Box and spawns HOT or COLD agent."""
        learning = default_knowledge_cache.get_learning(learning_id)

        # Decide agent type
        if force_type:
            agent_type = force_type
        else:
            # HOT for acute, transient, or fix-focused learnings; COLD for structural / persistent patterns
            category = learning.get("category", "") if learning else ""
            if category in ("error_fix", "hot_fix", "micro_patch"):
                agent_type = AgentType.HOT_MICRO_SPECIALIST
            else:
                agent_type = AgentType.COLD_DURABLE

        agent_id = f"agent-{agent_type.value}-{int(time.time() * 1000)}"
        system_prompt = f"""You are a specialized Agent ({agent_type.value}) created from Validated Learning [{learning_id}].
Topic/Pattern: {learning.get("title", "General Learning") if learning else "Custom Task"}
Directives:
1. Apply proven resolution patterns.
2. Maintain strict verification and zero-regression standards.
"""

        role = (
            WorkerRole.HOT_MICRO_SPECIALIST if agent_type == AgentType.HOT_MICRO_SPECIALIST else WorkerRole.COLD_DURABLE
        )
        spec = AgentSpec(
            id=agent_id,
            name=f"Specialist-{learning_id}",
            role=role,
            agent_type=agent_type,
            system_prompt=system_prompt,
            ttl_sec=300.0 if agent_type == AgentType.HOT_MICRO_SPECIALIST else None,
            validated_learnings_applied=[learning_id],
        )

        if agent_type == AgentType.HOT_MICRO_SPECIALIST:
            self.active_hot_specialists[agent_id] = spec
        else:
            self.active_cold_agents[agent_id] = spec

        # Register in Spawn Chain
        self.chain_registry.register_spawn(
            source_learning_id=learning_id,
            spawned_agent_id=agent_id,
            agent_type=agent_type,
            trigger_reason=trigger_reason,
        )

        return spec


# Global Singleton
default_agent_factory = DurableAgentFactory()
