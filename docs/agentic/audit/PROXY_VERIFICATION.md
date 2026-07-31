# Proxy Verification Report — 2026-07-31

## Test 1: Real Chat Request (valid auth)

**Command:**
```bash
curl -s -m 5 -X POST http://localhost:8080/v1/messages \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer freecc" \
  -d '{"model":"opencode_go/deepseek-v4-flash","messages":[{"role":"user","content":"Return exactly: OK 42"}],"max_tokens":10}'
```

**Result:** HTTP 200

**Response:** Valid Anthropic Messages API response with content blocks (thinking + text), usage stats, model name `deepseek-v4-flash`, stop_reason `max_tokens`. The model appeared to reason about the instruction ("OK 42") before hitting max_tokens.

**Latency:** ~4-5s (proxy-internal routing + upstream Deepseek inference)

---

## Test 2: Bad Auth

**Command:**
```bash
curl -s -m 5 -X POST http://localhost:8080/v1/messages \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer BADTOKEN" \
  -d '...'
```

**Result:** HTTP 401

**Response:** `{"detail":"Invalid proxy authentication token"}`

**Assessment:** Auth gate works correctly. Unauthorized tokens are rejected before reaching upstream providers.

---

## Test 3: Model Tier Availability

| Tier  | Model ID                          | HTTP Code | Result  |
|-------|-----------------------------------|-----------|---------|
| Deep  | `opencode_go/deepseek-v4-pro`     | 200       | PASS    |
| Main  | `opencode_go/deepseek-v4-flash`   | 200       | PASS    |
| Fast  | `opencode_go/deepseek-v4-flash-free` | 401    | FAIL — "Model deepseek-v4-flash-free is not supported" |

**Note:** The fast-tier model (`deepseek-v4-flash-free`) is not available in the upstream provider. The deep and main tiers are both functional.

---

## Test 4: Fabric Routing Fix

### Problem Found:
1. The fabric route URL for `fcc-proxy` was `http://localhost:8080/v1/chat/completions` — this endpoint returns **404 Not Found** because the proxy on port 8080 (CLIProxyAPI) uses the **Anthropic Messages API** (`/v1/messages`), not OpenAI Chat Completions.
2. The `dispatch_request()` method unconditionally called `format_openai_to_anthropic_response()` on all responses. The proxy returns **Anthropic-format** responses (with `type: "message"`), not OpenAI format (with `choices[]`). This caused content extraction to produce empty strings.
3. `fcc-proxy` was only listed as a route for `claude-3-7-sonnet`. Other tier aliases (`claude-3-5-sonnet`, `claude-3-5-haiku`, `claude-3-opus`) had no fcc-proxy route.

### Fixes Applied:

**File:** `/home/ubuntu/providers/multi_provider_fabric.py`

1. **URL corrected** in all `fcc-proxy` routes: `/v1/chat/completions` → `/v1/messages`
2. **fcc-proxy added as FIRST route** for all four model aliases (`claude-3-7-sonnet`, `claude-3-5-sonnet`, `claude-3-5-haiku`, `claude-3-opus`)
3. **Response handling fixed** in `dispatch_request()`: when the response already has `type == "message"` (Anthropic format), it is returned directly instead of being passed through the OpenAI-to-Anthropic converter. The model alias is overridden in the response for caller traceability.

---

## Test 5: Live Swarm Verification

**Command:**
```python
mgr = OpenCodeSwarmManager()
st = SubTask(id='PROXY-TEST', title='Echo test', description='Return just the word: PONG')
result = mgr.execute_subtask_with_worker(st, WorkerRole.CORE_ENGINEER)
```

**Result:**
- Status: `completed`
- Simulation fallback: **False**
- Verdict: **SUCCESS — Live provider reached**

The swarm orchestrator successfully dispatched through the fabric to the fcc-proxy, which routed the request to the upstream Deepseek provider and returned a real inference result.

---

## Verdict: **PASS**

| Check                          | Status |
|--------------------------------|--------|
| Proxy auth gate (valid token)  | PASS   |
| Proxy auth gate (bad token)    | PASS   |
| Deep tier availability         | PASS   |
| Main tier availability         | PASS   |
| Fast tier availability         | FAIL   |
| Fabric URL corrected           | PASS   |
| Fabric response parsing fixed  | PASS   |
| Fabric route coverage (4 tiers)| PASS   |
| Live swarm end-to-end          | PASS   |

**Remaining issue:** The `deepseek-v4-flash-free` fast-tier model is not supported by the upstream provider. The swarm will fall back to main-tier `deepseek-v4-flash` or other providers for fast-tier requests.
