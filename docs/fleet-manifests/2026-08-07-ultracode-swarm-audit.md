# Ultracode Fleet Manifest — 2026-08-07 22:13–22:43 UTC

## Fleet Stats

| Metric | Value |
|--------|-------|
| **Agents deployed** | 94 |
| **Agents completed** | 94 |
| **Agents errored** | 0 |
| **Tool calls** | 889 |
| **Total tokens** | 4,492,024 |
| **Duration** | 30.5 minutes |
| **Model used** | `deepseek-v4-pro` (all 94 agents) |
| **Workflow phases** | 5 (Audit → Adversarial Verify → Coverage → Synthesize → Remediate) |

## Model Provider

All 94 agents ran through:
- **Provider**: DeepSeek (via OpenRouter free tier)
- **Model**: `deepseek-v4-pro`
- **Gateway**: FCC Proxy (`fcc-server` PID 1270926 on port 8080) → Routatic Proxy (PID 1598 on port 3456)

## Infrastructure (Live Gateways)

### Routatic Proxy (`:3456`) — 300 models, 30+ providers

| Provider | Models |
|----------|--------|
| **alibaba** | qwen-flash, qwen-max, qwen-omni-turbo, qwen-plus, qwen-turbo, qwen-vl-max, qwen-vl-plus, qwen2-5-vl-72b, qwen3-235b, qwen3-32b, qwen3-coder-*, qwen3-max, qwen3-next-*, qwen3-vl-plus, qwen3.5-*, qwen3.6-*, qwen3.7-*, qwen3.8-*, qwq-plus |
| **anthropic** | claude-3-5-haiku/sonnet, claude-3-7-sonnet, claude-3-haiku, claude-fable-5, claude-haiku-4-5, claude-opus-4-0/1/5/6/7/8, claude-opus-5, claude-sonnet-4-0/5/6, claude-sonnet-5 |
| **cohere** | c4ai-aya-expanse-32b/8b, c4ai-aya-vision-32b/8b, command-a-03-2025, command-a-plus-05-2026, command-a-reasoning, command-a-translate, command-a-vision, command-r/r-plus, command-r7b, command-r7b-arabic, north-mini-code |
| **deepseek** | deepseek-chat, deepseek-r1, deepseek-reasoner, deepseek-v4-flash, deepseek-v4-flash-free, deepseek-v4-pro |
| **google** | deep-research-max, gemini-2.0-flash/lite, gemini-2.5-computer-use, gemini-2.5-flash/image/lite/tts/pro, gemini-3-flash/pro/pro-image, gemini-3.1-flash-*/pro, gemini-3.5-flash/lite/live-translate, gemini-3.6-flash, gemini-embedding-001/2, gemini-flash-latest/lite-latest, gemini-omni-flash, gemini-robotics, gemma-4-*, lyria-3-*, veo-3.1-* |
| **meta** | llama-3.3-70b, llama-4-maverick-17b, llama-4-scout-17b, muse-spark-1.1 |
| **minimax** | MiniMax-M2/M2.1/M2.5/M2.7/M3 (with highspeed variants) |
| **mistral** | codestral-latest, devstral-2512/medium/small, magistral-medium, mistral-large-2411/2512, mistral-medium-2505/2604, mistral-nemo, mistral-small-2506/2603, pixtral-12b, pixtral-large |
| **moonshotai** | kimi-k2-thinking/turbo, kimi-k2.5/k2.6, kimi-k2.7-code/highspeed, kimi-k3 |
| **nvidia** | llama-3.1-nemotron-70b/safety/ultra-253b, llama-3.3-nemotron-super-49b, nemotron-3-nano/super/ultra, nemotron-3.5-content-safety, nemotron-cascade-2, nemotron-mini/nano/voicechat, mistral-nemotron |
| **openai** | gpt-3.5-turbo, gpt-4/turbo/4.1/mini/nano/o, gpt-5 through gpt-5.6-* (codex, chat, pro, mini, nano, instant, luna, sol, terra), o1/o1-pro, o3/o3-mini/pro/deep-research, o4-mini, whisper-*, gpt-image-1/1.5/2, gpt-oss-*, gpt-realtime-* |
| **perplexity** | sonar, sonar-pro, sonar-reasoning-pro |
| **poolside** | laguna-m.1, laguna-s-2.1, laguna-xs-2.1/2 |
| **sakana** | fugu, fugu-ultra |
| **sarvam** | sarvam-105b, sarvam-30b |
| **stepfun** | step-3.5-flash/2603, step-3.7-flash |
| **thinkingmachines** | inkling, inkling-small |
| **xai** | grok-4.20 (reasoning/non-reasoning), grok-4.3/4.5, grok-build-0.1, grok-imagine-video-1.5 |
| **xiaomi** | mimo-v2-flash/omni/pro, mimo-v2.5/pro/ultraspeed |
| **zhipuai** | glm-4.5/air/flash/v, glm-4.6/v, glm-4.7/flash/flashx, glm-5/turbo, glm-5.1/5.2, glm-5v-turbo |

### Other Gateways

| Gateway | Port | PID | Status |
|---------|------|-----|--------|
| FCC Server | 8080 | 1270926 | healthy |
| Routatic Proxy | 3456 | 1598 | 300 models |
| LiteLLM | 4000 | ? | 0 models loaded |
| CLIProxyAPI | 8317 | ? | no health response |

## Workflow Results

### Audit Phase
- **99 findings** across 9 files (44 production, 55 test)
- 4 production auditors + 4 test auditors

### Adversarial Verification (3-lens: security, correctness, regression)
- **24 findings verified**, 7 survived (CONFIRMED real), 17 killed (refuted)
- ~72 verification agents (24 findings × 3 lenses)

### Coverage Analysis
| File | Coverage |
|------|----------|
| `latency_tracker.py` | **93%** |
| `multi_provider_fabric.py` | **82%** |
| `fast_pool.py` | **62%** |
| `health_check.py` | **26%** |
| **Combined (with branches)** | **66%** |

### Synthesis
- Ranked action plan with 7 confirmed findings
- Completeness critic: identified missing registry entries, schema inconsistencies
- Quality report compiled

### Remediation Phase
- Applied fixes across 14 production files
- Added 63 new tests (577 → 640)
- **640/640 tests pass, 0 failures, 0 regressions**

### Registry Issues Found
- `knowledge.jsonl`: 103 duplicate IDs (LEARN-0001 through LEARN-0010), LEARN-0009/LEARN-0010 missing
- `chain.jsonl`: 4 orphan entries referencing non-existent agents, -1 suffix duplication
- `agents.jsonl`: 23 near-identical skip_cat entries, ~92 cold_durable duplicates, inconsistent field schema
- `knowledge.jsonl`: 91% of entries have empty tags

## Version Bump Required
- Current: `1.13.0` → **MINOR bump** (new features: health_check improvements, fast_pool timeout fixes, latency_tracker percentile fix, multi_provider_fabric route hardening, provider-bans, concurrent-save fixes)

## Files Changed (28 files, +1267/-121)
Production: fast_pool.py, health_check.py, latency_tracker.py, key_pool.py, multi_provider_fabric.py, claude_proxy_server.py, agent_factory_service.py, agentic_worker_loop.py, codebase_map_service.py, opencode_swarm_service.py, progress_ledger_service.py, task_master_service.py, wave_gate_service.py, agentic_cli.py
Tests: test_agent_factory_service.py, test_agentic_worker_loop.py, test_claude_proxy_server.py, test_codebase_map_service.py, test_key_pool.py, test_latency_tracker.py, test_multi_provider_fabric.py, test_opencode_swarm_service.py, test_progress_ledger_service.py, test_task_master_service.py, test_wave_gate_service.py
New: test_fast_pool.py, test_health_check.py, provider-bans.json
