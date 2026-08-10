---
type: community
cohesion: 0.06
members: 84
---

# TaskSpineStore

**Cohesion:** 0.06 - loosely connected
**Members:** 84 nodes

## Members
- [[dot-__enter__()]] - code - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[dot-__exit__()]] - code - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[dot-__init__()_19]] - code - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[dot-__init__()_18]] - code - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[dot-__post_init__()_1]] - code - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[dot-_acquire_lock()]] - code - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[dot-_ensure_dir()]] - code - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[dot-_locked()]] - code - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[dot-_read_raw()]] - code - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[dot-_release_lock()]] - code - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[dot-_run_cli()]] - code - tests/test_task_spine_adapter.py
- [[dot-_store()]] - code - tests/test_task_spine_adapter.py
- [[dot-_write_atomic()]] - code - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[dot-attach_evidence()]] - code - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[dot-block()]] - code - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[dot-claim()]] - code - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[dot-complete()]] - code - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[dot-create()]] - code - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[dot-fail()_1]] - code - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[dot-from_dict()]] - code - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[dot-inspect()]] - code - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[dot-list_tasks()]] - code - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[dot-test_attach_evidence_missing()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_attach_evidence_preserves_status()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_block_missing()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_block_records_blocks_both_ways()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_claim_blocked_by_unresolved()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_claim_blocked_resolved_ok()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_claim_missing_task()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_claim_non_claimable_status()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_claim_pending()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_complete_missing()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_complete_with_evidence()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_create_and_inspect()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_create_idempotent_on_task_id()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_default_state_path_is_absolute()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_defaults_and_timestamps()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_fail_stores_error()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_from_dict_defaults()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_init_creates_file()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_invalid_status_raises()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_list_tasks_filter()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_main_block_and_attach_evidence()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_main_create_claim_flow()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_main_create_requires_title()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_main_fail_and_complete()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_main_init_creates_file()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_main_invalid_evidence_exits()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_main_list_and_inspect()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_main_no_command()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_missing_file_lists_empty()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_parser_has_commands()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_state_file_is_valid_json_after_ops()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_to_dict_roundtrip()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_update_allowed_fields()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_update_missing()]] - code - tests/test_task_spine_adapter.py
- [[dot-test_valid_statuses_are_claimable_set()]] - code - tests/test_task_spine_adapter.py
- [[dot-to_dict()_13]] - code - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[dot-update()]] - code - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[Any_19]] - code
- [[Append an evidence record to a task without changing its status.]] - rationale - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[ArgumentParser_1]] - code
- [[Claim a pending task for a worker. Sets status→in_progress.]] - rationale - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[Create a new task. Idempotent on task_id.]] - rationale - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[Create the spine file if it does not exist. Idempotent.]] - rationale - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[Generic update set arbitrary fields on a task.]] - rationale - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[List tasks, optionally filtered by status.]] - rationale - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[Manages the local task spine JSON file with fcntl locking.]] - rationale - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[Mark a task as blocked, optionally recording blocker ids.]] - rationale - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[Mark a task as completed with optional evidence.]] - rationale - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[Mark a task as failed with an error message stored in evidence.]] - rationale - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[Return full detail for a single task.]] - rationale - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[Run main() with argv and return the parsed JSON of its output.]] - rationale - tests/test_task_spine_adapter.py
- [[TaskRecord]] - code - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[TaskSpineStore]] - code - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[TestCLI]] - code - tests/test_task_spine_adapter.py
- [[TestTaskRecord]] - code - tests/test_task_spine_adapter.py
- [[TestTaskSpineStore]] - code - tests/test_task_spine_adapter.py
- [[Tests for servicestask_spine_adapter.py Real-behavior coverage TaskSpineStore…]] - rationale - tests/test_task_spine_adapter.py
- [[_LockedScope]] - code - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[_make_parser()]] - code - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[main()_5]] - code - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[task_spine_adapter.py]] - code - src/merged_agentic_swarm/services/task_spine_adapter.py
- [[test_task_spine_adapter.py]] - code - tests/test_task_spine_adapter.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/TaskSpineStore
SORT file.name ASC
```
