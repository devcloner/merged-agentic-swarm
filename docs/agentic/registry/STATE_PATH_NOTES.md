# Task Master State Path Reconciliation

## Paths

| System | Path | Status |
|---|---|---|
| **Real `task-master` CLI** | `.taskmaster/tasks/tasks.json` | Expected by blueprint; CLI cannot reach proxy |
| **Python `TaskMasterService`** | `.taskmaster/tasks/tasks.json` (was `task_master_state.json`) | Reconciled 2026-07-30 |
| **`.env` TASKMASTER_STATE_FILE** | `.taskmaster/tasks/tasks.json` | Updated 2026-07-30 |
| **Blueprint expectation** | `.taskmaster/tasks/tasks.json` | ✅ Matches |

## Divergence

The real `task-master-ai` (v0.43.1) expects to call Anthropic Messages API directly
at `http://127.0.0.1:8080/messages` (our fcc-server proxy), which returns 404 because
fcc-server is OpenAI-compatible, not Anthropic Messages API. The real TM also expects
a `PERPLEXITY_API_KEY` for research-backed task generation, which isn't set.

**Result**: The real TM CLI cannot generate or manage tasks in this environment. The
Python `TaskMasterService` is the working task spine, using the model fabric
(`providers/multi_provider_fabric.py`) which routes through the Python proxy on port
8085 or falls back to offline simulation.

## Resolution

- State file renamed: `task_master_state.json` → `tasks.json` ✓
- Python service default updated to `.taskmaster/tasks/tasks.json` ✓
- `.env` TASKMASTER_STATE_FILE updated to match ✓
- The real TM CLI is preserved for schema reference and future delegation when the
  proxy is Anthropic-compatible

## Future Work

- Option: delegate Python service to real TM CLI via subprocess when/if the proxy
  becomes Anthropic Messages API compatible
- The Python service's task schema (EpicTask/SubTask with wave_id) differs from the
  real TM's schema (flat task list with numeric IDs). Normalization needed for true
  interchange.
