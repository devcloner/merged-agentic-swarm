# Proxy Verification Report

**Date**: 2026-07-31
**Status**: PASS — live provider verified (Mistral)
**Verification script**: `scripts/agentic/verify_proxy.sh`

---

## Environment

| Item | Value | Status |
|:-----|:------|:-------|
| fcc-server | Port `8080` | Healthy — intercepts Anthropic API calls |
| `ANTHROPIC_BASE_URL` | `http://127.0.0.1:8080` | Set |
| `ANTHROPIC_AUTH_TOKEN` | `freecc` | Set |
| Python proxy (`ClaudeProxyServer`) | Port `8089` | Running — moved from `8085` to avoid conflict with CloudCLI |
| CloudCLI Web UI | Port `8085` | Running — originally crashed, fixed by correcting permissions |
| CLIProxyAPI Dashboard | Port `3000` | Running |
| OpenCode IDE | Port `9200` | Running |

The Python proxy (`src/merged_agentic_swarm/proxy/claude_proxy_server.py`) provides Anthropic Messages and OpenAI-compatible endpoints backed by the key pool and the multi-provider fabric.

---

## Provider Status

Six providers are loaded in the key pool (`providers/key_pool.py`): **gemini, opencode, groq, mistral, nvidia_nim, openrouter**. Upstream live tests:

| Provider | Test Models | Result | Detail |
|:---------|:------------|:-------|:-------|
| Mistral | `mistral-small-latest`, `ministral-8b-latest`, `mistral-tiny` | **WORKS** | All three returned HTTP 200 |
| OpenCode | — | NO CREDITS | Insufficient balance error |
| OpenRouter | — | INVALID KEY | HTTP 401 |
| NVIDIA NIM | — | TIMEOUT | No response within 30 s |

**Only working provider: Mistral** (key `qLWSa...`). All other keyed providers are unusable in the current environment and are skipped in practice by the routing cascade.

---

## Verified Tiers

All three model tiers were verified live through Mistral via the proxy:

| Tier | Alias | Backend (Mistral) | HTTP | Result |
|:-----|:------|:------------------|:-----|:-------|
| deep | `claude-3-opus` | `codestral-latest` | 200 | OK |
| main | `claude-3-7-sonnet` | `mistral-small-latest` | 200 | OK |
| fast | `claude-3-5-haiku` | `mistral-tiny` | 200 | OK |

Every tier returns a valid response; the fabric overrides the returned model name to the alias so callers see `claude-3-*` regardless of the Mistral backend.

---

## Routing Configuration

The routing table in `providers/multi_provider_fabric.py` (`MODEL_FABRIC_ROUTES`) was updated so **Mistral is first in every model route**:

- `claude-3-opus` → `codestral-latest` (mistral) → `mistral-large-latest` (mistral) → `fcc-proxy`
- `claude-3-7-sonnet` → `mistral-small-latest` (mistral) → `ministral-8b-latest` (mistral) → `fcc-proxy`
- `claude-3-5-haiku` → `mistral-tiny` (mistral) → `ministral-8b-latest` (mistral) → `fcc-proxy`

Requests are dispatched in priority order with key-pool rotation; the first route that succeeds wins.

---

## Authentication

- Inbound auth token: `freecc` (`ANTHROPIC_AUTH_TOKEN`).
- `verify_proxy.sh` sends `x-api-key: $AUTH_TOKEN` plus `anthropic-version: 2023-06-01` for tier tests.
- An invalid token (e.g. `bad-token-xyz`) is rejected with HTTP 401/403 before it reaches any upstream provider — the auth gate works.
- Mistral upstream auth uses the pool key `qLWSa...`; the remaining five providers either lack valid keys, lack credits, or time out.

---

## Error Cases

| Case | Observed Behavior |
|:-----|:------------------|
| OpenCode upstream | Insufficient balance — provider returns a credit error, never a 200 |
| OpenRouter upstream | HTTP 401 invalid key — fabric records it and skips |
| NVIDIA NIM upstream | 30 s timeout, no response |
| Invalid proxy auth token | HTTP 401/403 — rejected before dispatch |
| Unknown/unsupported model | Non-200 — rejected by the proxy |

Per-provider failures are recorded with perma-ban on 401 auth errors and circuit-breaking on other errors, so a dead provider is not retried within a dispatch.

---

## Fallback Behavior

- The fabric iterates the route list in priority order; on `HTTPError` or transport exception it records `last_error` and tries the next route.
- If **every** live route fails or is unconfigured, `dispatch_request()` falls back to an offline **simulation payload** (flagged with `simulation_fallback: true` so callers can detect synthetic responses).
- Because only Mistral is verified, realistic production traffic hits Mistral directly; the simulation fallback is reached only if Mistral itself goes down or the key is exhausted.

---

## Verdict

| Check | Status |
|:------|:-------|
| fcc-server healthy on 8080, intercepts Anthropic calls | PASS |
| Python proxy on 8089 | PASS |
| Mistral upstream (3 models) | PASS |
| OpenCode | FAIL (no credits) |
| OpenRouter | FAIL (invalid key) |
| NVIDIA NIM | FAIL (timeout) |
| deep tier → `codestral-latest` | PASS |
| main tier → `mistral-small-latest` | PASS |
| fast tier → `mistral-tiny` | PASS |
| Auth gate (bad token rejected) | PASS |
| Mistral first in all model routes | PASS |

**Residual risks**:

- **Single-provider dependence**: Mistral is the only working provider. An outage or key exhaustion drops the whole stack to simulation mode.
- **Unverified balance**: OpenCode has credits remaining conceptually but is unusable (Insufficient balance); OpenRouter and NVIDIA NIM need key replacement.
- **Simulation fallback**: When triggered it produces synthetic responses — callers must check `simulation_fallback` and treat those as degraded.
