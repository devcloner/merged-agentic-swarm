# Stack Analysis — 2026-08-06

Deep audit of the agentic-AI stack on this host (litellm gateway, fcc-server, opencode,
bluesminds/K1, ultraswarm, merged-agentic-swarm, aerolink). Produced by a 64-agent
ultracode fleet (8 recon areas → adversarial verify → score → plan).
**54 findings found, 49 verified.** 1 verify agent failed (stream error) — item marked.

---

## Security — do these FIRST (all are user actions)

| # | Issue | Where | Action |
|---|-------|-------|--------|
| 1 | Live opencode-go API key committed in git history | `merged-agentic-swarm/claude-code-proxy.json` (since `0fd1798`) | **Rotate key**, then scrub history |
| 2 | Live `PROXY_TOKEN` committed | `spotify-ai/SESSIONS_REPORT.md` | **Rotate**, replace with placeholder |
| 3 | Live GitHub PAT on disk (untracked) | `spotify-ai/.GitHubBoard/github-sync.json` | **Revoke now** in GitHub settings |
| 4 | GitHub PAT previously committed in `merged-agentic-swarm` history | "K" commit `a9f5261` (tree removed 2026-08-06, still in git objects) | **Revoke** — mandatory regardless of purge |
| 5 | `.GitHubBoard/` not in `spotify-ai/.gitignore` | `spotify-ai/.gitignore` | Append `.GitHubBoard/` |
| 6 | Hardcoded `sk-` literals in committed script | `spotify-ai/api_proxy/start.sh` | Verify dead, replace with `${VAR}` |
| 7 | Plaintext provider keys in world-readable (mode 664) opencode configs | `/home/ubuntu/opencode.json`, `/home/ubuntu/opencode-swarm.json`, `~/.config/opencode/opencode.json` | `chmod 600`, move apiKeys to env |
| 8 | BluesMinds + Aerolink keys plaintext, group-readable | opencode.json, `.codex/config.toml` | `chmod 600`; prefer gateway routing |

**Note:** findings 1–4 involve **live credentials in git history**. History scrub is
cosmetic; **rotation/revocation is the real fix** and must happen first.

---

## Top operational issues (non-security)

| # | Priority | Effort | Issue | Fix |
|---|----------|--------|-------|-----|
| 9 | 1 | minutes | 70/420 litellm model_list entries reference UNSET `GEMINI_KEY_36..42`; running container has stale env → ~1/6 of first attempts 401 across all model groups | Recreate container: `cd /home/ubuntu/deployments/litellm && docker compose up -d` (re-reads `.env.keys`; host already has values 36–42). Verify `env \| grep -c '^GEMINI_KEY'` → 42 |
| 10 | 2 | minutes | Retry/fallback turns each dead-key hit into 2-retry + cooldown + fallback chain | Resolved by #9; confirm amplification gone |
| 21 | 3 | hours | **Concurrency ramp hard-capped at 4 workers** — orchestrator never passes `wave_gate_level`; the 40-worker ramp never progresses | Pass wave level into `execute_subtask_batch_parallel` |
| 12 | 4 | hours | `create_custom_provider` calls `registry.add(entry)` (dataclass) but signature is `add(display_name, base_url, api_keys, ...)` → admin custom-provider creation always 500s | Fix call at `admin_custom_routes.py:272` to positional contract, or add `add_entry(entry)` |
| 13 | 5 | hours | Same handler accepts only a single API key — multi-key providers can't be created via API | Extend payload to `api_keys` list |
| 14 | 6 | hours | In-memory `ProviderRegistry` loads `custom_providers.json` once (`_loaded` flag), never re-reads → external edits ignored until restart | mtime/size-based reload + regression test |
| 15 | 7 | minutes | Running fcc-server has stale registry — bluesminds not active | Restart fcc-server; use admin API going forward |
| 16 | 8 | hours | Gateway has no model-aware routing: K1 models hit shared 20 RPM account first (2× 503, then failover) | Add `K1/*` → k1 connection routing; exclude k1 from non-K1 traffic ($5/day cap) |
| 17 | 9 | minutes | fcc `custom_bluesminds` failover pool includes K1 key as last-resort for ALL models → non-K1 traffic leaks onto $5/day budget | Split K1 key into own single-key provider |
| 18 | 10 | hours | Gateway `main` + `main2` are same account treated as independent → parallel fan-out exceeds real 20 RPM → 429s | Enforce shared sliding window or collapse to one connection |
| 19 | 11 | half-day | opencode `bluesminds`/`bluesminds-k1` providers bypass the gateway entirely (direct api.bluesminds.com) → no rate-limit/k1 routing, K1 spend untracked | Point both providers at gateway base URL |
| 22 | 12 | minutes | fcc routes ALL claude families (fable/opus/sonnet/haiku) to `opencode_go/deepseek-v4-flash` — opus/fable silently downgraded | Align MODEL_OPUS/FABLE to deepseek-v4-pro |
| 28 | 13 | half-day | Wave 3 "Zero Defect / Tests Passing" gate declared but never evaluated — passes on statuses alone | Wire syntax/test checks into `evaluate_gate_criteria` |
| 35 | 14 | hours | Last-successful-provider pinning keeps a degraded provider at front of every cascade (~90s dead time under throttle) | Treat consecutive 429s as breaker, not pin |
| 36 | 15 | hours | Key cooldown defeated by `force-recover` in `_get_key_unlocked` — 429 retry loop is a no-op | Return None for COOLDOWN keys so cascade advances |
| 40 | 16 | hours | fcc claude-code path has NO model-level fallback — opencode-go outage fails the request | Re-enable routatic fallback or add cross-model fallback |

---

## Medium / lower priority

- **#11** Zombie run `fc7abe32` stuck "running" in `.ultraswarm/state.sqlite` — cancel, do NOT resume
- **#20** `oh-my-opencode.json` references cliproxyapi models not in the provider's models list
- **#23** Only K1/claude-opus-4.6-thinking verified working; other 5 K1 models unverified
- **#24** Wave-2 COLD_DURABLE spawns never written to agents.jsonl / `.claude/agents/`
- **#25** Cold-path chain entries get duplicate entry_ids within one promotion batch
- **#26** Stale `.bak-swarmfix-20260806` agent files still reference `anthropic/claude-*` (not loaded, confusing)
- **#27** Commit `81d622b` has no GitHub home — no `devcloner/ultraswarm` fork; upstream-worthy loadConfig fix will drift
- **#29** `progress.json` read by `agentic-cli status` is stale — never written by runtime
- **#30** `_apply_worker_outputs` resolves text-mode `# file:` paths against `src/merged_agentic_swarm/` not repo root
- **#31** Registry count / final summary crashes with FileNotFoundError when no learnings exist
- **#32** Two different "chain" counts reported; retry config drift
- **#33** Promoted-learning IDs persisted only on full success → re-promotions on aborted runs
- **#34** Ownership-map / durable-agent lookups depend on process CWD / hardcoded home paths
- **#37** Aerolink codex config verified correct; 0.3s latency claim stale (sol ~11s TTFT)
- **#39** `opencode-cliproxyapi-sync` atomically replaces entire opencode.json — wipes manual provider/model edits
- **#41** routatic-proxy is Anthropic-wire only — OpenAI `/v1/chat/completions` 404s; `custom_routatic_proxy` would break if re-enabled
- **#42** Model-substitution chain: no-paid-zen MATCHED, gemini-first NOT matched by fcc/routatic chains (deliberate fast-path)
- **#43/#44** Config notes drift + LITELLM_PROXY_KEY launch-env fragility
- **#45** Duplicate litellm provider block across both opencode configs; dangling opencode-go ref
- **#46–49** Verified non-issues (even key rotation, fake test fixtures, matching 5-worker config)

---

## Proposed execution order (from the fleet)

`3 → 4 → 5` (minutes) → **user rotations** (PAT revoke, key rotations) → `1 → 2`
(history scrub, after rotation) → `6 → 7 → 8` → `9 → 10` (litellm keys + retry) →
remaining operational items by priority.

## Must do by the user (cannot be scripted)

1. **Revoke the `ghp_` GitHub PAT** (Settings → Developer settings → Tokens). Already in
   git history + on disk; grants repo write.
2. **Rotate `sk-ziIQQ***`** (opencode-go key) and the live PROXY_TOKEN — both in
   HEAD-reachable history of shared repos. Rotation devalues them; history scrub is cosmetic.
3. **Decide on the ultraswarm fork**: create `devcloner/ultraswarm` (fork of fubak/ultraswarm)
   and PR the loadConfig fix, or keep the commit local and note it.

---

*Generated by 64-agent analysis fleet (3.76M tokens, 1619 tool uses). 1 verify agent
failed with a stream error — the affected finding (verify:F9) should be re-run.*
