---
source_file: "src/merged_agentic_swarm/services/agentic_worker_loop.py"
type: "code"
community: "AgenticWorkerLoop"
location: "L126"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/AgenticWorkerLoop
---

# _command_safety_error()

## Connections
- [[dot-_tool_run_command()]] - `calls` [EXTRACTED]
- [[dot-test_allowed_commands()]] - `calls` [EXTRACTED]
- [[dot-test_denylist_global_destructive()]] - `calls` [EXTRACTED]
- [[dot-test_empty_and_parse_failures()]] - `calls` [EXTRACTED]
- [[dot-test_refused_curl_wget_pipe_to_sh()]] - `calls` [EXTRACTED]
- [[dot-test_refused_git_state_destroying()]] - `calls` [EXTRACTED]
- [[dot-test_refused_shell_operators()]] - `calls` [EXTRACTED]
- [[dot-test_refused_system_destructive_tokens()]] - `calls` [EXTRACTED]
- [[dot-test_shell_operators_allowed_under_run_prefix()]] - `calls` [EXTRACTED]
- [[dot-test_sudo_token()]] - `calls` [EXTRACTED]
- [[Return a refusal reason if ``command`` is unsafe, else None.]] - `rationale_for` [EXTRACTED]
- [[agentic_worker_loop.py]] - `contains` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/AgenticWorkerLoop