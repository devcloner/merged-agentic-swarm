---
source_file: "tests/test_task_master_service.py"
type: "rationale"
community: "TaskMasterService"
location: "L197"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/TaskMasterService
---

# Concurrent save_state calls must never leave a torn JSON target.

## Connections
- [[dot-test_concurrent_saves_produce_complete_json()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/TaskMasterService