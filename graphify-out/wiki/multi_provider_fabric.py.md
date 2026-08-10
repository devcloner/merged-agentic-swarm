# multi_provider_fabric.py

> 52 nodes · cohesion 0.07

## Key Concepts

- **CloudCLIClient** (16 connections) — `src/merged_agentic_swarm/services/cloudcli_service.py`
- **_FakeResp** (15 connections) — `tests/test_cloudcli_service.py`
- **_client()** (13 connections) — `tests/test_cloudcli_service.py`
- **CloudCLIError** (12 connections) — `src/merged_agentic_swarm/services/cloudcli_service.py`
- **test_cloudcli_service.py** (12 connections) — `tests/test_cloudcli_service.py`
- **_FakeClient** (10 connections) — `tests/test_cloudcli_service.py`
- **_install_fake_client()** (8 connections) — `tests/test_cloudcli_service.py`
- **TestValidation** (7 connections) — `tests/test_cloudcli_service.py`
- **cloudcli_service.py** (6 connections) — `src/merged_agentic_swarm/services/cloudcli_service.py`
- **TestEnvFallbacks** (6 connections) — `tests/test_cloudcli_service.py`
- **TestStreamAgent** (6 connections) — `tests/test_cloudcli_service.py`
- **TestTriggerAgent** (6 connections) — `tests/test_cloudcli_service.py`
- **.stream_agent()** (5 connections) — `src/merged_agentic_swarm/services/cloudcli_service.py`
- **.trigger_agent()** (5 connections) — `src/merged_agentic_swarm/services/cloudcli_service.py`
- **._build_payload()** (4 connections) — `src/merged_agentic_swarm/services/cloudcli_service.py`
- **.test_skips_non_json_and_blank_lines()** (4 connections) — `tests/test_cloudcli_service.py`
- **.test_stream_http_error_raises()** (4 connections) — `tests/test_cloudcli_service.py`
- **.test_yields_sse_events()** (4 connections) — `tests/test_cloudcli_service.py`
- **.test_branch_and_pr_flags()** (4 connections) — `tests/test_cloudcli_service.py`
- **.test_http_error_raises()** (4 connections) — `tests/test_cloudcli_service.py`
- **.test_sends_payload_and_parses_json()** (4 connections) — `tests/test_cloudcli_service.py`
- **.__init__()** (3 connections) — `src/merged_agentic_swarm/services/cloudcli_service.py`
- **CloudCLIConfig** (3 connections) — `src/merged_agentic_swarm/services/cloudcli_service.py`
- **Any** (3 connections)
- **.from_env()** (2 connections) — `src/merged_agentic_swarm/services/cloudcli_service.py`
- *... and 27 more nodes in this community*

## Relationships

- [PassthroughStreamingProxy](PassthroughStreamingProxy.md) (4 shared connections)
- [AgenticWorkerLoop](AgenticWorkerLoop.md) (1 shared connections)

## Source Files

- `src/merged_agentic_swarm/services/cloudcli_service.py`
- `tests/test_cloudcli_service.py`

## Audit Trail

- EXTRACTED: 177 (88%)
- INFERRED: 24 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*