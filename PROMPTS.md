# Merged Agentic Swarm — Ready-to-Say Prompts

Copy + paste any of these into a Claude Code session. Each runs the system from a different angle.

---

## 1. Quick Smoke Test (60 seconds)
_Verifies CI, CLI connectivity, provider routes, and proxy health._

```
Run the full CI pipeline (syntax check, CLI config, pytest suite, import chain), then start the proxy server, curl /health and /status, and stop it. Show me the full output.
```

---

## 2. System Status Deep Read
_Reads all registries, progress files, and state — no mutation._

```
Read and summarize: the progress.json phase completion, every registry (knowledge.jsonl, agents.jsonl, chain.jsonl) with entry counts and recent entries, the key pool provider summary, all model fabric routes, and the most recent 5 progress_ledger.json entries. Show me any anomalies.
```

---

## 3. Cold-Path Promotion End-to-End
_Adds learnings, promotes them through the cold path, verifies persistence._

```
Do a complete cold-path promotion test:
1. Clear learnings that don't already have promoted agents
2. Add 5 learnings across 3 categories to the hot cache (knowledge_cache)
3. Run the cold-path promote command (uv run tools/agentic_cli.py promote)
4. Verify knowledge.jsonl and agents.jsonl have new entries
5. Run the promote command again (idempotency check — should return 0 new)
6. Show me the final registry state
```

---

## 4. Proxy Server Integration Test
_Starts proxy, sends real/simulation requests, checks circuit breaker._

```
Start the proxy server on port 8085. Then:
1. curl http://localhost:8085/health — verify it responds
2. curl http://localhost:8085/status — show key pool state
3. Send a POST /v1/messages with {"model":"claude-3-7-sonnet","messages":[{"role":"user","content":"Say hello"}]} — capture the response
4. Check whether the response is live AI or simulation fallback
5. Send to /v1/chat/completions with the same payload — verify OpenAI format
6. Stop the proxy server. Show me the full transcript.
```

---

## 5. Circuit Breaker & Resilience Test
_Proves the system degrades gracefully under provider failures._

```
Test the fault tolerance:
1. Read the multi_provider_fabric.py circuit breaker logic
2. Simulate 3 sequential failures for the groq provider (calls to _record_failure)
3. Verify groq is in _circuit_open_until and _circuit_breaker count >= 3
4. Simulate a 401 error — verify groq goes to _permanently_dead
5. Call _record_success for groq — verify circuit resets
6. Run the full test suite for test_multi_provider_fabric.py to confirm unit coverage
```

---

## 6. Full Orchestrator Run (Monitoring Mode)
_Runs the complete workflow with verbose output, then audits everything._

```
Run the full orchestrator workflow in verbose mode:
uv run tools/agentic_cli.py run --verbose

Wait for it to complete. Then audit the results:
1. Show me progress.json phase completion percentages
2. Count entries in knowledge.jsonl, agents.jsonl, chain.jsonl
3. Show me the last 10 entries in progress_ledger.json
4. Show me the spawn_chain_registry.json
5. Check for any ERROR or WARNING log messages
6. Run the full test suite to verify nothing broke
```

---

## 7. Complete System Validation (THE FULL MONTY)
_Everything: CI → proxy → orchestrator → resilience → registry → tests._

```
Perform a complete system validation. Follow these steps in order and report pass/fail for each:

**Phase 1: Infrastructure**
1. Run scripts/ci.sh — all steps must pass (syntax check, CLI config, pytest, import chain)
2. Start the proxy server on 8085, curl /health (expect 200), curl /status (expect key pools), then stop it

**Phase 2: Cold-Path Promotion**
3. Add 3 learnings ("Proxy failover", "swarm", "config") to hot cache
4. Run uv run tools/agentic_cli.py promote — must report > 0 promoted
5. Verify knowledge.jsonl has new entries matching the added learnings
6. Verify agents.jsonl has a new agent entry
7. Re-run promote — must report 0 new (idempotent)
8. Check that chain.jsonl was updated

**Phase 3: Orchestrator**
9. Run uv run tools/agentic_cli.py run --title "Validation Test"
10. Wait for completion — must report 4 waves completed
11. Verify progress.json shows > 0% completion
12. Verify progress_ledger.json has success markers

**Phase 4: Resilience**
13. Read the circuit breaker state — check provider status
14. Simulate failure: call _record_failure 3 times for a provider
15. Check the provider is in circuit breaker now
16. Simulate 401 — verify perma-ban takes effect

**Phase 5: Verification**
17. Run the full test suite (224 tests) — all must pass
18. Run uv run tools/agentic_cli.py config — all 9 providers, 21 routes present
19. Show me final counts for all registries

Report a final summary table with pass/fail per check.
```

---

## How to use these

Open a Claude Code terminal and say one of these verbatim as a prompt. Each one is self-contained and references the system by its file paths and CLI commands.

To save runs: prefix with "Run this, save the full output to a file, and also commit results to a results/ directory."
