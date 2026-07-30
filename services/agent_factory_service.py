"""
Durable Agent Factory & Knowledge-Box -> Spawn Chain Registry
Turns validated learnings into HOT micro-specialists or COLD durable agents, maintaining a persistent chain registry.
"""
import os
import sys
import time
import json
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from typing import Dict, Any, List, Optional
from models.agent_models import AgentSpec, AgentType, WorkerRole, SpawnChainEntry
from tools.knowledge_cache import default_knowledge_cache

logger = logging.getLogger("agent_factory")

class ChainRegistry:
    def __init__(self, registry_file: str = "/home/ubuntu/.taskmaster/tasks/spawn_chain_registry.json"):
        self.registry_file = registry_file
        self.entries: List[SpawnChainEntry] = []
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
                            timestamp=d.get("timestamp", time.time())
                        )
                        for d in data
                    ]
            except Exception as e:
                logger.error(f"Failed loading spawn chain registry: {e}")

    def save_registry(self):
        os.makedirs(os.path.dirname(self.registry_file), exist_ok=True)
        with open(self.registry_file, "w", encoding="utf-8") as f:
            json.dump([e.to_dict() for e in self.entries], f, indent=2)

    def register_spawn(self, source_learning_id: str, spawned_agent_id: str, agent_type: AgentType, trigger_reason: str, parent_entry_id: Optional[str] = None) -> SpawnChainEntry:
        entry = SpawnChainEntry(
            entry_id=f"CHAIN-{len(self.entries)+1:04d}",
            source_learning_id=source_learning_id,
            spawned_agent_id=spawned_agent_id,
            agent_type=agent_type,
            trigger_reason=trigger_reason,
            parent_entry_id=parent_entry_id
        )
        self.entries.append(entry)
        self.save_registry()
        logger.info(f"Registered spawn chain entry {entry.entry_id}: {agent_type.value} agent {spawned_agent_id}")
        return entry

class DurableAgentFactory:
    def __init__(self, chain_registry: Optional[ChainRegistry] = None):
        self.chain_registry = chain_registry or ChainRegistry()
        self.active_hot_specialists: Dict[str, AgentSpec] = {}
        self.active_cold_agents: Dict[str, AgentSpec] = {}

    def spawn_from_learning(self, learning_id: str, trigger_reason: str, force_type: Optional[AgentType] = None) -> AgentSpec:
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

        agent_id = f"agent-{agent_type.value}-{int(time.time()*1000)}"
        system_prompt = f"""You are a specialized Agent ({agent_type.value}) created from Validated Learning [{learning_id}].
Topic/Pattern: {learning.get('title', 'General Learning') if learning else 'Custom Task'}
Directives:
1. Apply proven resolution patterns.
2. Maintain strict verification and zero-regression standards.
"""

        role = WorkerRole.HOT_MICRO_SPECIALIST if agent_type == AgentType.HOT_MICRO_SPECIALIST else WorkerRole.COLD_DURABLE
        spec = AgentSpec(
            id=agent_id,
            name=f"Specialist-{learning_id}",
            role=role,
            agent_type=agent_type,
            system_prompt=system_prompt,
            validated_learnings_applied=[learning_id]
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
            trigger_reason=trigger_reason
        )

        return spec

# Global Singleton
default_agent_factory = DurableAgentFactory()
