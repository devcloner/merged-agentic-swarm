"""
Services Package Initialization
"""

from merged_agentic_swarm.services.agent_factory_service import (
    ChainRegistry,
    DurableAgentFactory,
    default_agent_factory,
)
from merged_agentic_swarm.services.cloudcli_service import CloudCLIClient, CloudCLIError
from merged_agentic_swarm.services.codebase_map_service import CodebaseMapService, default_codebase_mapper
from merged_agentic_swarm.services.model_routing import (
    litellm_model_for_fabric_route,
    resolve_litellm_model_for_role,
)
from merged_agentic_swarm.services.opencode_swarm_service import OpenCodeSwarmManager, default_swarm_manager
from merged_agentic_swarm.services.progress_ledger_service import (
    ObstaclePlaybookEngine,
    ProgressLedgerService,
    default_progress_ledger,
)
from merged_agentic_swarm.services.swarm_profiles import (
    list_profiles,
    load_profiles,
    resolve_model_alias_for_profile,
    resolve_profile,
)
from merged_agentic_swarm.services.task_master_service import TaskMasterService, default_task_master
from merged_agentic_swarm.services.wave_gate_service import WaveGateController, default_wave_controller

__all__ = [
    "ChainRegistry",
    "CloudCLIClient",
    "CloudCLIError",
    "CodebaseMapService",
    "DurableAgentFactory",
    "ObstaclePlaybookEngine",
    "OpenCodeSwarmManager",
    "ProgressLedgerService",
    "TaskMasterService",
    "WaveGateController",
    "default_agent_factory",
    "default_codebase_mapper",
    "default_progress_ledger",
    "default_swarm_manager",
    "default_task_master",
    "default_wave_controller",
    "list_profiles",
    "litellm_model_for_fabric_route",
    "load_profiles",
    "resolve_litellm_model_for_role",
    "resolve_model_alias_for_profile",
    "resolve_profile",
]
