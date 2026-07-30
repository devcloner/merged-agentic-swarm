"""
pytest fixtures and shared test utilities for Merged Agentic Swarm.
"""
import os
import sys
import time
import json
import tempfile
import pytest

# Ensure project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# ── Fixtures: temp directories ──

@pytest.fixture
def temp_dir():
    """Provide a temporary directory that is cleaned up after the test."""
    with tempfile.TemporaryDirectory() as d:
        yield d


@pytest.fixture
def temp_env_file(temp_dir):
    """Create a minimal env.txt with one key for testing."""
    path = os.path.join(temp_dir, "env.txt")
    with open(path, "w") as f:
        f.write("GEMINI_API_KEY=test-gemini-key\n")
        f.write("GROQ_API_KEY=test-groq-key\n")
    return path


# ── Fixtures: isolated singletons ──

@pytest.fixture
def isolated_key_pool(temp_env_file):
    """Return a KeyPoolManager pointed at a temp env file."""
    from providers.key_pool import KeyPoolManager
    pool = KeyPoolManager(env_file_path=temp_env_file)
    return pool


@pytest.fixture
def isolated_fabric(isolated_key_pool):
    """Return a MultiProviderFabric backed by the isolated key pool."""
    from providers.multi_provider_fabric import MultiProviderFabric
    fabric = MultiProviderFabric(key_pool=isolated_key_pool)
    return fabric


@pytest.fixture
def isolated_knowledge_cache(temp_dir):
    """Return a KnowledgeCache that writes to a temp file."""
    from tools.knowledge_cache import KnowledgeCache
    cache_file = os.path.join(temp_dir, "knowledge_cache.json")
    cache = KnowledgeCache(cache_file=cache_file, max_learnings=10)
    return cache


@pytest.fixture
def isolated_chain_registry(temp_dir):
    """Return a ChainRegistry that writes to a temp file."""
    from services.agent_factory_service import ChainRegistry
    reg_file = os.path.join(temp_dir, "spawn_chain_registry.json")
    reg = ChainRegistry(registry_file=reg_file)
    return reg


@pytest.fixture
def isolated_agent_factory(isolated_chain_registry):
    """Return a DurableAgentFactory with an isolated chain registry."""
    from services.agent_factory_service import DurableAgentFactory
    factory = DurableAgentFactory(chain_registry=isolated_chain_registry)
    return factory


@pytest.fixture
def isolated_progress_ledger(temp_dir):
    """Return a ProgressLedgerService that writes to a temp file."""
    from services.progress_ledger_service import ProgressLedgerService
    ledger_file = os.path.join(temp_dir, "progress_ledger.json")
    ledger = ProgressLedgerService(ledger_file=ledger_file)
    return ledger


@pytest.fixture
def isolated_task_master(temp_dir):
    """Return a TaskMasterService that writes to a temp file."""
    from services.task_master_service import TaskMasterService
    state_file = os.path.join(temp_dir, "tasks.json")
    tm = TaskMasterService(state_file_path=state_file)
    return tm


@pytest.fixture
def isolated_wave_controller():
    """Return a fresh WaveGateController (no persistent state to worry about)."""
    from services.wave_gate_service import WaveGateController
    return WaveGateController()


@pytest.fixture
def isolated_swarm_manager():
    """Return a fresh OpenCodeSwarmManager."""
    from services.opencode_swarm_service import OpenCodeSwarmManager
    return OpenCodeSwarmManager()


@pytest.fixture
def isolated_codebase_mapper(temp_dir):
    """Return a CodebaseMapService pointed at an isolated repo root."""
    from services.codebase_map_service import CodebaseMapService
    mapper = CodebaseMapService(repo_root=temp_dir)
    mapper.spec_gaps = []
    mapper.symbol_cache = {}
    return mapper


@pytest.fixture
def owner_map_file(temp_dir):
    """Create a minimal ownership-map.json and return its path."""
    owner_map = {
        "pools": [
            {
                "pool_id": "domain-module-workers",
                "owned_paths": ["services/*", "models/*"],
                "forbidden_paths": ["external/*"],
            }
        ]
    }
    path = os.path.join(temp_dir, "ownership-map.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(owner_map, f, indent=2)
    return path


# ── Helper factories ──

@pytest.fixture
def make_subtask():
    """Factory fixture that returns a function to create SubTask instances."""

    def _make(title="Test Task", desc="Test description", task_id=None):
        from models.prd_models import SubTask
        return SubTask(
            id=task_id or f"TASK-{int(time.time() * 1000) % 10000:04d}",
            title=title,
            description=desc,
        )

    return _make


@pytest.fixture
def make_epic(make_subtask):
    """Factory fixture that returns a function to create EpicTask instances."""

    def _make(title="Test Epic", epic_id=None, wave_id=0, subtask_count=1):
        from models.prd_models import EpicTask, TaskPriority
        subtasks = [make_subtask(title=f"ST-{i}", task_id=f"ST-{epic_id}-{i}") for i in range(subtask_count)]
        return EpicTask(
            id=epic_id or f"EPIC-{int(time.time() * 1000) % 100:02d}",
            title=title,
            description=f"Description for {title}",
            wave_id=wave_id,
            priority=TaskPriority.P1_HIGH,
            subtasks=subtasks,
        )

    return _make
