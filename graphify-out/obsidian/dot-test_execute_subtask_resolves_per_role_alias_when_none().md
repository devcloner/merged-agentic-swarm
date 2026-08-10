---
source_file: "tests/test_opencode_swarm_service.py"
type: "code"
community: "TestExecuteSubtaskDecisionLogic"
location: "L490"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/TestExecuteSubtaskDecisionLogic
---

# .test_execute_subtask_resolves_per_role_alias_when_none()

## Connections
- [[dot-_manager()]] - `calls` [EXTRACTED]
- [[TestExecuteSubtaskDecisionLogic]] - `method` [EXTRACTED]
- [[_router()]] - `calls` [EXTRACTED]
- [[make_subtask()]] - `calls` [INFERRED]
- [[model_alias=None resolves the role's litellm alias and feeds it to the worker…]] - `rationale_for` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/TestExecuteSubtaskDecisionLogic