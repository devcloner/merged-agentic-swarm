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

## Natural-language prompts

Same jobs, said how you'd actually talk. These embed the full loop — learn, remember, promote, specialize — into everyday language.

### Models & providers

```md
Talk to the model fabric and tell me which providers are alive, which are on cooldown, and which are permanently dead. If gemini keeps carrying the load, that's useful to know — write it down as a learning so the system can route around failures smarter next time.
```

```md
Open the key pool and tell me what's actually usable. I want active keys per provider, what's cooling down, and whether any provider is quietly failing without us noticing. If you see a pattern in the failures, capture it.
```

```md
Send a real message through the fabric. Try liteLLM first, then fall through the routes if it fails. I want to see the circuit breaker work — if a provider is down, it should skip it, not crash. If the whole chain falls through to simulation, tell me that too.
```

```md
Run a quick dispatch test against claude-3-5-sonnet through all available routes. Which provider actually answers? Was it a real model or simulation? Capture the latency and route ordering so we know where the traffic really flows.
```

### Proxy

```md
Spin up the proxy daemon on its standard port and keep it alive. Ping /health to confirm it's up, then /status to see the live key pool state. Send one message through /v1/messages as a real caller would. Log everything and stop cleanly when done.
```

```md
Start the proxy, send a chat completions request through it, and verify it converts the response back to OpenAI format properly. If the proxy is the gateway, I want to know it handles both Claude-style and OpenAI-style callers without losing data.
```

### Knowledge & learning

```md
Look at what's in the hot cache right now. How many learnings are there, what categories dominate, and is anything expired or about to expire? If the cache is full of noise, tell me. If there's something valuable that hasn't been promoted yet, flag it.
```

```md
Run the cold-path promotion manually. Take whatever's in the hot cache that hasn't been promoted yet and push it through: hot cache → knowledge.jsonl → agents.jsonl → chain.jsonl. Tell me how many new entries each registry got and whether any category hit the agent-creation threshold. Run it again after and confirm it's idempotent.
```

```md
Add a new learning to the cache about something we just figured out. If it's a duplicate of something already there, I want it to quietly return the existing ID instead of duplicating. If the cache is full, evict the oldest entry first. And if this is a time-sensitive insight, give it a TTL so it cleans itself up later.
```

### Wave gates & progress

```md
Check the wave gate status. Are we still in Wave 0, or have we progressed? What does each wave's gate criteria actually check, and have we satisfied the current one? If we're stuck on a gate, tell me why rather than letting us spin.
```

```md
Read the progress ledger from start to finish. Show me the success markers, the failures, the obstacles that triggered playbooks, and how each one was resolved. I want to see the system recovering from its own problems, not just a log of wins.
```

```md
Advance to the next wave if the current gate passes. Don't force it — if the gate criteria aren't met, tell me exactly what's missing so we can fix it before moving on.
```

### Agent factory & spawning

```md
Look at the active agents. Which HOT specialists are alive, and are any of them expired and ready to be purged? Which COLD durables exist? If the HOT pool is stale, purge the dead ones. If a category is missing a durable agent but has enough learnings to justify one, promote it.
```

```md
Spawn an agent from a learning. Pick one from the hot cache that looks important, turn it into a HOT micro-specialist for immediate work and a COLD durable for long-term memory. Register the spawn chain so we can trace why this agent exists later.
```

### Full orchestrator run

```md
Start the full orchestrator workflow. Don't rush it — let it go through all four waves properly. After it finishes, audit everything: which epics completed, which failed, how many success markers were recorded, what cold-path promotion happened, and whether the registries got compacted. If anything errored, I want to know what was learned from it.
```

```md
Run the orchestrator end to end, but watch it closely. Every time it hits a wave gate, pause and show me the gate result. Every time it creates a learning or spawns an agent, show me what and why. At the end, give me the full cold-path state and tell me if the system is measurably smarter than before the run.
```

### Test suite & CI

```md
Run the full test suite and tell me which 224 tests pass and which don't. If something fails, don't just report it — investigate whether it's a real regression or just a test that needs better isolation from the live environment.
```

```md
Run the full CI pipeline from scratch. Syntax check, CLI smoke test, all 224 pytest cases, and the import chain test. Every step must pass before the next one starts. If CI is green, we ship. If not, stop and explain the first failure.
```

### Resilience & chaos

```md
Poke the circuit breaker. Simulate a few failures against one of the providers and watch it trip into cooldown after three strikes. Then simulate a 401 to see it get permanently banned. Then call success and confirm it resets. I want to trust that when a real provider goes down, the system doesn't fall apart.
```

```md
Force the system into simulation fallback. Ban all the providers temporarily and send a dispatch request. It should return a valid-looking response with the simulation flag set, not crash or hang. That's the last line of defence and I need to know it works.
```

### Quick everyday versions

```md
Show me the live provider status.
```

```md
Promote any new learnings from the hot cache.
```

```md
Run the test suite and tell me if CI is green.
```

```md
Start the proxy, ping it, send a message, stop it.
```

```md
Sweep the hot cache for expired entries and purge them.
```

```md
Check the wave gate and advance if clear.
```

```md
Run the orchestrator and audit the cold-path result.
```

```md
Simulate a provider failure and verify the circuit breaker catches it.
```

```md
Read me the latest progress ledger entries.
```

```md
Verify cold-path promotion is idempotent — run it twice, second run should add nothing.
```

## How to use these

Open a Claude Code terminal and say one of these verbatim as a prompt. Each one is self-contained and references the system by its file paths and CLI commands.

To save runs: prefix with "Run this, save the full output to a file, and also commit results to a results/ directory."
