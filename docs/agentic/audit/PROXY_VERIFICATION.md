# Proxy Verification Report

**Date**: 2026-08-06
**Status**: PASS — live multi-provider fabric verified (Gemini pool), systemd-daemonized on 8089
**Verification script**: `scripts/agentic/verify_proxy.sh` → `RESULT: 5 passed, 0 failed | STATUS: SUCCESS`
**Supersedes**: the 2026-07-31 report (single-provider/Mistral-only, pre-auth-gate)

---

## Environment

| Item | Value | Status |
|:-----|:------|:-------|
| systemd unit `claude-proxy` | Port `8089`, `Type=simple`, `User=ubuntu` | Active + enabled (Restart=always, RestartSec=5) |
| `ExecStart` | `.venv/bin/python -m merged_agentic_swarm.proxy.claude_proxy_server --host 0.0.0.0 --port 8089` | Live |
| `Environment` | `ANTHROPIC_AUTH_TOKEN=freecc`, `PYTHONUNBUFFERED=1` | Set |
| Inbound auth gate | `x-api-key` or `Authorization: Bearer <token>` vs `ANTHROPIC_AUTH_TOKEN` (default `freecc`) | Verified 401/401/200 |
| Health monitor | `scripts/agentic/check_proxy_health.sh` via cron `*/2 * * * *` | Installed (idempotent) |
| fcc-server | Port `8080` | Healthy (prewarm HEAD 204) |
| Connection prewarm | `fast_pool.warm_all()` at startup | 7/7 provider hosts reachable |

The proxy (`src/merged_agentic_swarm/proxy/claude_proxy_server.py`) exposes Anthropic Messages (`/v1/messages`), OpenAI-compatible (`/v1/chat/completions`), and audio transcription (`/v1/audio/transcriptions`, NVIDIA NIM Whisper) — all backed by the key pool + multi-provider fabric. Health/status endpoints and CORS preflight stay unauthenticated so monitors can probe.

---

## Key Pool Status (live `/status`)

| Provider | Keys | Active | Cooldown | Requests | Tokens |
|:---------|-----:|-------:|---------:|---------:|-------:|
| gemini | 42 | 42 | 0 | 5 | 76 |
| opencode | 1 | 1 | 0 | 0 | 0 |
| mistral | 1 | 1 | 0 | 0 | 0 |
| nvidia_nim | 1 | 1 | 0 | 0 | 0 |
| openrouter | 1 | 1 | 0 | 0 | 0 |
| litellm | 1 | 1 | 0 | 0 | 0 |
| fcc-proxy | 1 | 1 | 0 | 0 | 0 |
| routatic-proxy | 1 | 1 | 0 | 0 | 0 |

Keys are referenced by env-var name only (`GEMINI_API_KEYS`, `OPENCODE_API_KEY`, `MISTRAL_API_KEY`, `NVIDIA_NIM_API_KEY`, `OPENROUTER_API_KEY`, `LITELLM_PROXY_KEY`, `ANTHROPIC_AUTH_TOKEN`). The Gemini pool (42 keys) is the fabric's deep provider; the 5 tier-probe requests dispatched to `generativelanguage.googleapis.com` returned HTTP 200 (see below).

---

## Verified Tiers (live dispatch, not simulation)

All three model tiers dispatched through the fabric with real provider latency (Gemini backend); journal confirms POSTs to `generativelanguage.googleapis.com/v1beta/openai/chat/completions` → HTTP 200:

| Tier | Alias | HTTP | Latency | Result |
|:-----|:------|:-----|:--------|:-------|
| deep | `claude-3-opus` | 200 | ~453 ms | OK |
| main | `claude-3-7-sonnet` | 200 | ~495 ms | OK |
| fast | `claude-3-5-haiku` | 200 | ~363 ms | OK |

The fabric overrides the returned model name to the alias so callers see `claude-3-*` regardless of the backend provider.

---

## Authentication Gate

- Inbound token: `ANTHROPIC_AUTH_TOKEN` (default `freecc`). Accepts `x-api-key` header first, then `Authorization: Bearer <token>`.
- Gate runs first in `do_POST`; `/health`, `/status`, and `do_OPTIONS` remain unauthenticated.
- Live checks (8089):
  - `/health` → **200**, `/status` → **200** (no token required)
  - POST `/v1/messages` with **no token** → **401** JSON
  - POST `/v1/messages` with **wrong token** (`bad-token-xyz`) → **401** JSON
  - POST `/v1/messages` with `Authorization: Bearer freecc` → **200**
- The 2026-07-31 report's claim that "the auth gate works" was false at the time — the gate did not exist until this change; it is now verified live and covered by tests.

---

## Routing & Fallback

- `MODEL_FABRIC_ROUTES` in `providers/multi_provider_fabric.py` lists priority-ordered routes per tier (Gemini pool deep, then OpenRouter / FCC-proxy / others); the first route that succeeds wins. Unknown model names fall through to the default/fallback route (why `verify_proxy.sh` logs a WARN on unknown models that still return 200 — pre-existing quirk, not a regression).
- Per-provider failures are recorded (perma-ban on 401 auth errors, circuit-breaking otherwise) so a dead provider is not retried mid-dispatch.
- If every route fails or is unconfigured, `dispatch_request()` falls back to an offline **simulation payload** (flagged `simulation_fallback: true`). The 2026-08-06 tier probes did **not** hit simulation — real provider latencies and `/status` counters confirm live Gemini dispatch.

---

## Error Cases

| Case | Observed Behavior |
|:-----|:------------------|
| No inbound token | HTTP 401 — rejected before dispatch |
| Wrong inbound token | HTTP 401 — rejected before dispatch |
| Invalid JSON body | HTTP 400 |
| Audio transcription, no file field | HTTP 400 |
| Whisper backend down | HTTP 503 |
| Unknown/unsupported endpoint | HTTP 404 |

---

## Systemd Daemonization

Unit `/etc/systemd/system/claude-proxy.service`: `Type=simple`, `Restart=always`, `RestartSec=5`, `After/Wants=network-online.target`, installed/enabled via `systemctl daemon-reload` + `systemctl enable --now claude-proxy`. Auto-restart monitored by `check_proxy_health.sh` (cron every 2 min): probes `/health`, on non-200 issues one `systemctl restart`, logs to `/tmp/claude-proxy-health.log`.

---

## Deferred: Kubernetes / ARC Workflow Integration

Exposing the proxy to ARC runner pods (Helm `--set-string env[0].name="ANTHROPIC_BASE_URL"=http://172.17.0.1:8089` + `ANTHROPIC_AUTH_TOKEN=freecc`) is **NOT implemented**:

- No ARC runner-set is registered on this host — there is nothing to configure against.
- `172.17.0.1` is a guessed docker-bridge gateway, not a verified route from any runner pod.

Revisit when an ARC runner-set exists and the pod→host network path is confirmed (pod CIDR, host firewall, and whether the proxy should bind `0.0.0.0:8089` or a dedicated interface).

---

## Verdict

| Check | Status |
|:------|:-------|
| systemd unit active + enabled on 8089 | PASS |
| Inbound auth gate (no token / wrong token / Bearer) | PASS (401 / 401 / 200) |
| deep tier live dispatch | PASS (~453 ms) |
| main tier live dispatch | PASS (~495 ms) |
| fast tier live dispatch | PASS (~363 ms) |
| Gemini pool (42 keys) active, 0 cooldown | PASS |
| 7/7 provider hosts prewarmed | PASS |
| Health-check cron installed | PASS |
| `verify_proxy.sh` full run | PASS (5 passed, 0 failed) |
| ARC/Helm pod integration | DEFERRED (no runner-set; gateway unverified) |

**Residual risks**:

- **Dead-key replacement is a user action**: the 42-key Gemini pool and the single OpenRouter/Mistral/NVIDIA keys are only as good as the keys at rest. If any are dead, the fabric records them and cascades — but rotating them (Google AI Studio → `generate_litellm_config.py` → `systemctl reload litellm-proxy`; same for OpenRouter/Mistral/NVIDIA) is required to keep full redundancy.
- **Simulation fallback**: if every provider were exhausted at once, the proxy returns synthetic responses flagged `simulation_fallback: true`; callers must treat those as degraded.
- **Transient `/status` piped-parse race** observed once (empty stdin through a pipe); the endpoint itself always returned full valid JSON — a curl/pipe artifact, not a service defect.
- **Cosmetic**: `verify_proxy.sh` labels port 8089 as proxy type "unknown" (script only maps 3456/8080) — display-only.
