---
type: community
cohesion: 0.06
members: 64
---

# AgenticWorkerLoop

**Cohesion:** 0.06 - loosely connected
**Members:** 64 nodes

## Members
- [[dot-__init__()_10]] - code - src/merged_agentic_swarm/services/agentic_worker_loop.py
- [[dot-__init__()_26]] - code - tests/test_agentic_worker_loop.py
- [[dot-_resolve_in_workdir()]] - code - src/merged_agentic_swarm/services/agentic_worker_loop.py
- [[dot-_run_tool()]] - code - src/merged_agentic_swarm/services/agentic_worker_loop.py
- [[dot-_tool_list_dir()]] - code - src/merged_agentic_swarm/services/agentic_worker_loop.py
- [[dot-_tool_read_file()]] - code - src/merged_agentic_swarm/services/agentic_worker_loop.py
- [[dot-_tool_run_command()]] - code - src/merged_agentic_swarm/services/agentic_worker_loop.py
- [[dot-_tool_write_file()]] - code - src/merged_agentic_swarm/services/agentic_worker_loop.py
- [[dot-dispatch_request()_1]] - code - tests/test_agentic_worker_loop.py
- [[dot-execute()]] - code - src/merged_agentic_swarm/services/agentic_worker_loop.py
- [[dot-test_allowed_commands()]] - code - tests/test_agentic_worker_loop.py
- [[dot-test_completes_on_final_text()]] - code - tests/test_agentic_worker_loop.py
- [[dot-test_denylist_global_destructive()]] - code - tests/test_agentic_worker_loop.py
- [[dot-test_dispatch_error_fails()]] - code - tests/test_agentic_worker_loop.py
- [[dot-test_empty_and_parse_failures()]] - code - tests/test_agentic_worker_loop.py
- [[dot-test_executes_tool_call_then_completes()]] - code - tests/test_agentic_worker_loop.py
- [[dot-test_iteration_bound_keeps_partial_work()]] - code - tests/test_agentic_worker_loop.py
- [[dot-test_list_dir()]] - code - tests/test_agentic_worker_loop.py
- [[dot-test_path_escape_refused()]] - code - tests/test_agentic_worker_loop.py
- [[dot-test_plain_string()]] - code - tests/test_agentic_worker_loop.py
- [[dot-test_refused_curl_wget_pipe_to_sh()]] - code - tests/test_agentic_worker_loop.py
- [[dot-test_refused_git_state_destroying()]] - code - tests/test_agentic_worker_loop.py
- [[dot-test_refused_shell_operators()]] - code - tests/test_agentic_worker_loop.py
- [[dot-test_refused_system_destructive_tokens()]] - code - tests/test_agentic_worker_loop.py
- [[dot-test_run_command_captures_failure()]] - code - tests/test_agentic_worker_loop.py
- [[dot-test_run_command_real_subprocess()]] - code - tests/test_agentic_worker_loop.py
- [[dot-test_run_command_refuses_denylist()]] - code - tests/test_agentic_worker_loop.py
- [[dot-test_run_command_respects_timeout()]] - code - tests/test_agentic_worker_loop.py
- [[dot-test_run_command_tool_hints_uv()]] - code - tests/test_agentic_worker_loop.py
- [[dot-test_shell_operators_allowed_under_run_prefix()]] - code - tests/test_agentic_worker_loop.py
- [[dot-test_simulation_is_failure()]] - code - tests/test_agentic_worker_loop.py
- [[dot-test_sudo_token()]] - code - tests/test_agentic_worker_loop.py
- [[dot-test_text_blocks()]] - code - tests/test_agentic_worker_loop.py
- [[dot-test_tool_use_blocks_ignored()]] - code - tests/test_agentic_worker_loop.py
- [[dot-test_write_and_read_file()]] - code - tests/test_agentic_worker_loop.py
- [[dot-test_write_file_creates_parents()]] - code - tests/test_agentic_worker_loop.py
- [[Agentic Worker Tool Loop Runs a real agentic loop over the multi-provider…]] - rationale - src/merged_agentic_swarm/services/agentic_worker_loop.py
- [[AgenticWorkerLoop]] - code - src/merged_agentic_swarm/services/agentic_worker_loop.py
- [[Any_12]] - code
- [[Execute one tool call for real. Returns (result_text, error_or_None).]] - rationale - src/merged_agentic_swarm/services/agentic_worker_loop.py
- [[Executes a subtask with real tools through the multi-provider fabric.]] - rationale - src/merged_agentic_swarm/services/agentic_worker_loop.py
- [[Extract the assistant's text content from an Anthropic-shaped response.]] - rationale - src/merged_agentic_swarm/services/agentic_worker_loop.py
- [[Hitting max_iterations completes with real partial work kept.]] - rationale - tests/test_agentic_worker_loop.py
- [[No tool_calls in the response → completed with the model's summary.]] - rationale - tests/test_agentic_worker_loop.py
- [[Resolve a repo-relative path, refusing escapes outside ``workdir``.]] - rationale - src/merged_agentic_swarm/services/agentic_worker_loop.py
- [[Return a refusal reason if ``command`` is unsafe, else None.]] - rationale - src/merged_agentic_swarm/services/agentic_worker_loop.py
- [[Run the agentic loop for one subtask and return a result dict. Result keys…]] - rationale - src/merged_agentic_swarm/services/agentic_worker_loop.py
- [[RuntimeError]] - code
- [[Scripted fabric serves a queue of responses, records requests.]] - rationale - tests/test_agentic_worker_loop.py
- [[TestCommandSafety]] - code - tests/test_agentic_worker_loop.py
- [[TestExtractText]] - code - tests/test_agentic_worker_loop.py
- [[TestLoopControlFlow]] - code - tests/test_agentic_worker_loop.py
- [[TestRealToolExecution]] - code - tests/test_agentic_worker_loop.py
- [[Tests for servicesagentic_worker_loop.py Coverage real tool execution…]] - rationale - tests/test_agentic_worker_loop.py
- [[The run_command schema must steer models to the uv toolchain — bare ``python``…]] - rationale - tests/test_agentic_worker_loop.py
- [[Tool call is executed for real, result fed back, then completes.]] - rationale - tests/test_agentic_worker_loop.py
- [[Tools execute for real against a tmp workdir.]] - rationale - tests/test_agentic_worker_loop.py
- [[_FakeFabric]] - code - tests/test_agentic_worker_loop.py
- [[_command_safety_error()]] - code - src/merged_agentic_swarm/services/agentic_worker_loop.py
- [[_extract_text()]] - code - src/merged_agentic_swarm/services/agentic_worker_loop.py
- [[_text_response()]] - code - tests/test_agentic_worker_loop.py
- [[_tool_response()]] - code - tests/test_agentic_worker_loop.py
- [[agentic_worker_loop.py]] - code - src/merged_agentic_swarm/services/agentic_worker_loop.py
- [[test_agentic_worker_loop.py]] - code - tests/test_agentic_worker_loop.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/AgenticWorkerLoop
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_multi_provider_fabric.py]]
- 1 edge to [[_COMMUNITY_WorkerRole]]
- 1 edge to [[_COMMUNITY_CloudCLIClient]]
- 1 edge to [[_COMMUNITY_test_agentic_cli.py]]
- 1 edge to [[_COMMUNITY_TestRunFullAgenticWorkflow]]

## Top bridge nodes
- [[RuntimeError]] - degree 4, connects to 3 communities
- [[agentic_worker_loop.py]] - degree 7, connects to 2 communities