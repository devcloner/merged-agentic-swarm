---
source_file: "tests/test_task_master_service.py"
type: "rationale"
community: "TaskMasterService"
location: "L169"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/TaskMasterService
---

# Regression for #41: temp file must not be the fixed <target>.tmp.

## Connections
- [[dot-test_save_state_uses_unique_temp_name()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/TaskMasterService