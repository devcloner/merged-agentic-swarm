#!/usr/bin/env bash
# CI script for Merged Agentic Swarm
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONPATH="${ROOT}/src${PYTHONPATH:+:$PYTHONPATH}"

echo "=== Merged Agentic Swarm CI ==="
echo ""

# 1. Python syntax check
echo "--- Syntax check ---"
python3 << 'PYEOF'
import sys
files = [
    'src/merged_agentic_swarm/providers/multi_provider_fabric.py',
    'src/merged_agentic_swarm/providers/key_pool.py',
    'src/merged_agentic_swarm/services/progress_ledger_service.py',
    'src/merged_agentic_swarm/services/wave_gate_service.py',
    'src/merged_agentic_swarm/services/codebase_map_service.py',
    'src/merged_agentic_swarm/services/agent_factory_service.py',
    'src/merged_agentic_swarm/services/task_master_service.py',
    'src/merged_agentic_swarm/tools/knowledge_cache.py',
    'src/merged_agentic_swarm/tools/agentic_cli.py',
    'src/merged_agentic_swarm/tools/agentic_orchestrator.py',
    'src/merged_agentic_swarm/proxy/claude_proxy_server.py',
    'src/merged_agentic_swarm/models/prd_models.py',
    'src/merged_agentic_swarm/models/agent_models.py',
]
all_ok = True
for f in files:
    try:
        compile(open(f).read(), f, 'exec')
        print(f'  OK  {f}')
    except SyntaxError as e:
        print(f'  FAIL {f}: {e}')
        all_ok = False
if not all_ok:
    print('SYNTAX CHECK FAILED')
    sys.exit(1)
PYEOF
echo ""

# 2. CLI smoke test
echo "--- CLI smoke test ---"
python3 src/merged_agentic_swarm/tools/agentic_cli.py config 2>&1 | grep 'Key Pool\|Route:\|Swarm:'
echo ""

# 3. Pytest suite
echo "--- Pytest suite ---"
uv run pytest -v --tb=short --timeout=120 2>&1
echo ""

# 4. Import chain test
echo "--- Import chain test ---"
python3 << 'PYEOF'
from merged_agentic_swarm.providers.key_pool import default_key_pool
from merged_agentic_swarm.providers.multi_provider_fabric import default_fabric, MODEL_FABRIC_ROUTES
from merged_agentic_swarm.tools.knowledge_cache import default_knowledge_cache
print(f'  Key pools: {list(default_key_pool.keys_by_provider.keys())}')
print(f'  Routes:    {list(MODEL_FABRIC_ROUTES.keys())}')
print(f'  Learnings: {len(default_knowledge_cache.learnings)}')
PYEOF
echo ""

echo "=== CI PASSED ==="
