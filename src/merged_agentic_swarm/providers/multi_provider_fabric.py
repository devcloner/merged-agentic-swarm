"""
Multi-Backend Model Fabric
Routes requests across providers with priority fallbacks, format normalization, and key pool rotation.
"""
import json
import logging
import threading
import time
import urllib.error
import urllib.request
from typing import Any

from merged_agentic_swarm.providers.key_pool import default_key_pool

logger = logging.getLogger("model_fabric")

# ── Module-level circuit breaker state (shared across all fabric instances) ──
_circuit_breaker: dict[str, int] = {}
_circuit_open_until: dict[str, float] = {}
_permanently_dead: dict[str, float] = {}  # provider -> ban-expiry timestamp
_last_successful_provider: dict[str, str] = {}  # model_alias -> provider
CIRCUIT_BREAKER_THRESHOLD = 3
CIRCUIT_BREAKER_COOLDOWN = 120.0
PERMA_BAN_DURATION = 86400.0  # 24h — don't re-try auth-failed providers for a day
_fabric_lock = threading.Lock()


def _record_failure(provider: str, http_code: int | None = None):
    """Record a provider failure — perma-ban on 401 auth errors, circuit-break on others."""
    with _fabric_lock:
        if http_code == 401:
            _permanently_dead[provider] = time.time() + PERMA_BAN_DURATION
            logger.warning(f"Provider {provider} permanently blacklisted (HTTP {http_code}).")
            return
        _circuit_breaker[provider] = _circuit_breaker.get(provider, 0) + 1
        if _circuit_breaker[provider] >= CIRCUIT_BREAKER_THRESHOLD:
            _circuit_open_until[provider] = time.time() + CIRCUIT_BREAKER_COOLDOWN
            logger.warning(
                f"Circuit breaker tripped for {provider} "
                f"({_circuit_breaker[provider]} consecutive failures)."
            )


def _record_success(provider: str, model_alias: str | None = None):
    """Record a provider success — reset circuit breaker and update last-working cache."""
    with _fabric_lock:
        _circuit_breaker[provider] = 0
        _circuit_open_until.pop(provider, None)
        if model_alias:
            _last_successful_provider[model_alias] = provider

# Fallback Routing Table
#
# Every route below was live-verified (HTTP 200) in this environment on 2026-08-01:
#   - Gemini  — 42 keys in ~/gemlni-keys/working-keys.txt rotate via KeyPoolManager
#               (least-used selection). gemini-2.5-flash: 36/42 keys 200;
#               gemini-2.5-flash-lite: 39/42 keys 200 (3 keys 404 — not enabled for
#               flash-lite); gemini-flash-latest alias also 200. The 2.5-pro / 2.0-flash
#               family 429s on all 42 keys (outside these keys' free quota) — excluded.
#   - NVIDIA NIM — integrate.api.nvidia.com, free tier. llama-3.1-8b / -70b / gpt-oss-20b /
#               glm-5.2 / mistral-nemotron / nemotron-super-49b / nemotron-3-super-120b
#               all 200 in <3s. llama-3.3-70b-instruct is 200 but ~44s — kept as a
#               deep fallback with a per-route timeout override (was misdiagnosed as
#               dead before the timeout fix; the fixed 10s timeout killed it).
#   - fcc-proxy (localhost:8080) — fronts 943 models; nvidia_nim/* and mistral/*
#               through the proxy are 200 (0.2-0.4s). Its opencode_go and open_router
#               upstreams 401 (dead upstream keys inside the proxy) — excluded.
#   - Mistral — api.mistral.ai, single working key; small/ministral/tiny/codestral/large 200.
#   - OpenRouter — ONLY :free models are referenced (user does not use paid models).
#               The env key is 401 "User not found" as of this audit, so these routes
#               perma-ban on first hit and are skipped cheaply; kept so a valid key
#               activates them automatically. 14 :free models exist on the platform.
# Routes are ordered verified-first (reliability × speed), then as fallbacks. Dead
# providers fail fast (perma-ban on 401 / circuit breaker) and fall through.
MODEL_FABRIC_ROUTES: dict[str, list[dict[str, Any]]] = {
    # ── deep tier (claude-3-opus) — strongest available models ─────────────
    "claude-3-opus": [
        {"provider": "gemini", "model": "gemini-2.5-flash", "url": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"},
        {"provider": "nvidia_nim", "model": "meta/llama-3.1-70b-instruct", "url": "https://integrate.api.nvidia.com/v1/chat/completions"},
        {"provider": "mistral", "model": "mistral-large-latest", "url": "https://api.mistral.ai/v1/chat/completions"},
        {"provider": "gemini", "model": "gemini-2.5-flash-lite", "url": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"},
        {"provider": "nvidia_nim", "model": "openai/gpt-oss-20b", "url": "https://integrate.api.nvidia.com/v1/chat/completions"},
        {"provider": "nvidia_nim", "model": "z-ai/glm-5.2", "url": "https://integrate.api.nvidia.com/v1/chat/completions"},
        {"provider": "fcc-proxy", "model": "nvidia_nim/meta/llama-3.1-70b-instruct", "url": "http://localhost:8080/v1/messages"},
        {"provider": "mistral", "model": "codestral-latest", "url": "https://api.mistral.ai/v1/chat/completions"},
        {"provider": "nvidia_nim", "model": "meta/llama-3.3-70b-instruct", "url": "https://integrate.api.nvidia.com/v1/chat/completions", "timeout": 60},
        {"provider": "openrouter", "model": "deepseek/deepseek-chat-v3.1:free", "url": "https://openrouter.ai/api/v1/chat/completions"},
    ],
    # ── main tier (claude-3-7-sonnet) ──────────────────────────────────────
    "claude-3-7-sonnet": [
        {"provider": "gemini", "model": "gemini-2.5-flash", "url": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"},
        {"provider": "nvidia_nim", "model": "meta/llama-3.1-70b-instruct", "url": "https://integrate.api.nvidia.com/v1/chat/completions"},
        {"provider": "mistral", "model": "mistral-small-latest", "url": "https://api.mistral.ai/v1/chat/completions"},
        {"provider": "gemini", "model": "gemini-2.5-flash-lite", "url": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"},
        {"provider": "nvidia_nim", "model": "openai/gpt-oss-20b", "url": "https://integrate.api.nvidia.com/v1/chat/completions"},
        {"provider": "nvidia_nim", "model": "z-ai/glm-5.2", "url": "https://integrate.api.nvidia.com/v1/chat/completions"},
        {"provider": "fcc-proxy", "model": "mistral/mistral-small-latest", "url": "http://localhost:8080/v1/messages"},
        {"provider": "mistral", "model": "ministral-8b-latest", "url": "https://api.mistral.ai/v1/chat/completions"},
        {"provider": "openrouter", "model": "deepseek/deepseek-chat-v3.1:free", "url": "https://openrouter.ai/api/v1/chat/completions"},
    ],
    # ── main tier (claude-3-5-sonnet) ──────────────────────────────────────
    "claude-3-5-sonnet": [
        {"provider": "gemini", "model": "gemini-2.5-flash", "url": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"},
        {"provider": "nvidia_nim", "model": "meta/llama-3.1-70b-instruct", "url": "https://integrate.api.nvidia.com/v1/chat/completions"},
        {"provider": "mistral", "model": "mistral-small-latest", "url": "https://api.mistral.ai/v1/chat/completions"},
        {"provider": "gemini", "model": "gemini-2.5-flash-lite", "url": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"},
        {"provider": "nvidia_nim", "model": "openai/gpt-oss-20b", "url": "https://integrate.api.nvidia.com/v1/chat/completions"},
        {"provider": "nvidia_nim", "model": "z-ai/glm-5.2", "url": "https://integrate.api.nvidia.com/v1/chat/completions"},
        {"provider": "fcc-proxy", "model": "mistral/mistral-small-latest", "url": "http://localhost:8080/v1/messages"},
        {"provider": "mistral", "model": "ministral-8b-latest", "url": "https://api.mistral.ai/v1/chat/completions"},
        {"provider": "openrouter", "model": "deepseek/deepseek-chat-v3.1:free", "url": "https://openrouter.ai/api/v1/chat/completions"},
    ],
    # ── fast tier (claude-3-5-haiku) — cheapest/latency-first ──────────────
    "claude-3-5-haiku": [
        {"provider": "gemini", "model": "gemini-2.5-flash-lite", "url": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"},
        {"provider": "nvidia_nim", "model": "meta/llama-3.1-8b-instruct", "url": "https://integrate.api.nvidia.com/v1/chat/completions"},
        {"provider": "mistral", "model": "mistral-tiny", "url": "https://api.mistral.ai/v1/chat/completions"},
        {"provider": "gemini", "model": "gemini-2.5-flash", "url": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"},
        {"provider": "nvidia_nim", "model": "mistralai/mistral-nemotron", "url": "https://integrate.api.nvidia.com/v1/chat/completions"},
        {"provider": "fcc-proxy", "model": "nvidia_nim/meta/llama-3.1-8b-instruct", "url": "http://localhost:8080/v1/messages"},
        {"provider": "mistral", "model": "ministral-8b-latest", "url": "https://api.mistral.ai/v1/chat/completions"},
        {"provider": "openrouter", "model": "deepseek/deepseek-chat-v3.1:free", "url": "https://openrouter.ai/api/v1/chat/completions"},
    ],
    # ── general-purpose alias (fabCFA) — mirrors main tier ─────────────────
    "fabCFA": [
        {"provider": "gemini", "model": "gemini-2.5-flash", "url": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"},
        {"provider": "nvidia_nim", "model": "meta/llama-3.1-70b-instruct", "url": "https://integrate.api.nvidia.com/v1/chat/completions"},
        {"provider": "mistral", "model": "mistral-small-latest", "url": "https://api.mistral.ai/v1/chat/completions"},
        {"provider": "gemini", "model": "gemini-2.5-flash-lite", "url": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"},
        {"provider": "nvidia_nim", "model": "openai/gpt-oss-20b", "url": "https://integrate.api.nvidia.com/v1/chat/completions"},
        {"provider": "nvidia_nim", "model": "z-ai/glm-5.2", "url": "https://integrate.api.nvidia.com/v1/chat/completions"},
        {"provider": "fcc-proxy", "model": "mistral/mistral-small-latest", "url": "http://localhost:8080/v1/messages"},
        {"provider": "mistral", "model": "ministral-8b-latest", "url": "https://api.mistral.ai/v1/chat/completions"},
        {"provider": "openrouter", "model": "deepseek/deepseek-chat-v3.1:free", "url": "https://openrouter.ai/api/v1/chat/completions"},
    ],
}

class MultiProviderFabric:
    def __init__(self, key_pool=None):
        self.key_pool = key_pool or default_key_pool

    def format_anthropic_to_openai(self, messages: list[dict[str, Any]], system_prompt: str | None = None) -> list[dict[str, Any]]:
        openai_messages = []
        if system_prompt:
            openai_messages.append({"role": "system", "content": system_prompt})
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if isinstance(content, list):
                # Flatten Anthropic content blocks to text string
                text_parts = []
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        text_parts.append(block.get("text", ""))
                    elif isinstance(block, str):
                        text_parts.append(block)
                content = "\n".join(text_parts)
            openai_messages.append({"role": role, "content": content})
        return openai_messages

    def format_openai_to_anthropic_response(self, openai_resp: dict[str, Any], model_alias: str) -> dict[str, Any]:
        """Converts OpenAI response payload to Anthropic messages payload format."""
        choices = openai_resp.get("choices", [])
        content_text = ""
        if choices:
            msg = choices[0].get("message", {})
            content_text = msg.get("content") or ""
            if not content_text:
                # Reasoning-only response (e.g. Gemini thinking models): extract from finish_reason context
                finish_reason = choices[0].get("finish_reason", "")
                if finish_reason == "length":
                    content_text = "[Reasoning completed — response truncated at token limit. Try a simpler prompt or increase max_tokens.]"
                elif finish_reason in ("stop", "end_turn"):
                    content_text = "[Model produced reasoning-only response with no visible text output.]"

        usage = openai_resp.get("usage", {})
        return {
            "id": f"msg_{int(time.time()*1000)}",
            "type": "message",
            "role": "assistant",
            "model": model_alias,
            "content": [
                {
                    "type": "text",
                    "text": content_text
                }
            ],
            "stop_reason": "end_turn",
            "stop_sequence": None,
            "usage": {
                "input_tokens": usage.get("prompt_tokens", 0),
                "output_tokens": usage.get("completion_tokens", 0)
            }
        }

    def _build_route_list(self, model_alias: str) -> list[dict[str, str]]:
        """Build route list, promoting the last successful provider for this alias to the front."""
        routes = list(MODEL_FABRIC_ROUTES.get(model_alias, MODEL_FABRIC_ROUTES["claude-3-7-sonnet"]))
        last_provider = _last_successful_provider.get(model_alias)
        if last_provider:
            idx = next((i for i, r in enumerate(routes) if r["provider"] == last_provider), None)
            if idx is not None and idx > 0:
                routes.insert(0, routes.pop(idx))
        return routes

    def dispatch_request(self, model_alias: str, messages: list[dict[str, Any]], system_prompt: str | None = None, max_tokens: int = 4096, temperature: float = 0.7) -> dict[str, Any]:
        """Dispatches request across multi-backend provider fallback cascade."""
        # Empty conversation is a malformed request — don't burn provider calls
        # (or cascade timeouts) on it; respond immediately like a 400 would.
        if not messages and not system_prompt:
            logger.warning("dispatch_request called with empty messages; returning error response.")
            return {
                "id": f"msg_err_{int(time.time()*1000)}",
                "type": "message",
                "role": "assistant",
                "model": model_alias,
                "content": [{"type": "text", "text": "[ERROR] Empty conversation: provide at least one message."}],
                "stop_reason": "end_turn",
                "stop_sequence": None,
                "usage": {"input_tokens": 0, "output_tokens": 0},
                "error": "empty_conversation",
            }

        routes = self._build_route_list(model_alias)

        last_error = None
        for route in routes:
            provider = route["provider"]
            target_model = route["model"]
            target_url = route["url"]

            # Skip permanently-dead providers (401/403)
            if provider in _permanently_dead:
                if time.time() < _permanently_dead[provider]:
                    continue
                else:
                    _permanently_dead.pop(provider, None)

            # Circuit breaker — skip provider under cooldown
            if provider in _circuit_open_until:
                if time.time() < _circuit_open_until[provider]:
                    continue
                else:
                    _circuit_open_until.pop(provider, None)
                    _circuit_breaker[provider] = 0

            # Try this route with up to KEY_RETRY_LIMIT distinct keys from the pool.
            # A 429/503 is a per-key throttle — with N keys rotating, the next key is
            # usually fine, so rotate within the route before cascading providers.
            # Only non-throttle failures (401, 5xx, timeout) trip the provider-level
            # circuit breaker, so one slow key can't take the whole provider down.
            key_retry_limit = 3
            for _ in range(key_retry_limit):
                key_info = self.key_pool.get_key(provider)
                if not key_info:
                    logger.debug(f"No key available for provider {provider}, trying next in fabric chain.")
                    break

                openai_msgs = self.format_anthropic_to_openai(messages, system_prompt)
                payload = {
                    "model": target_model,
                    "messages": openai_msgs,
                    "max_tokens": max_tokens,
                    "temperature": temperature
                }

                start_time = time.time()
                try:
                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {key_info.secret_value}",
                        "User-Agent": "MergedAgenticSwarm/1.0",
                    }

                    req_data = json.dumps(payload).encode("utf-8")
                    req = urllib.request.Request(target_url, data=req_data, headers=headers, method="POST")

                    is_local = any(host in target_url for host in ["localhost", "127.0.0.1"])
                    # Per-route timeout override: some free backends (e.g. NVIDIA NIM's
                    # llama-3.3-70b) are slow-but-alive and need more than the default
                    # 10s before they'd be falsely declared dead.
                    timeout = route.get("timeout", 5.0 if is_local else 10.0)
                    with urllib.request.urlopen(req, timeout=timeout) as response:
                        res_body = response.read().decode("utf-8")
                        resp_json = json.loads(res_body)
                        latency = (time.time() - start_time) * 1000
                        tokens = resp_json.get("usage", {}).get("total_tokens", 0)

                        self.key_pool.mark_success(key_info, latency_ms=latency, tokens=tokens)
                        _record_success(provider, model_alias=model_alias)

                        # If the response is already in Anthropic Messages format (e.g. fcc-proxy), return it directly.
                        if resp_json.get("type") == "message":
                            resp_json["model"] = model_alias  # override model name in response
                            return resp_json

                        return self.format_openai_to_anthropic_response(resp_json, model_alias)

                except urllib.error.HTTPError as e:
                    err_text = e.read().decode("utf-8", errors="ignore") if hasattr(e, "read") else str(e)
                    logger.warning(f"HTTPError {e.code} on provider {provider} (model {target_model}): {err_text[:200]}")
                    if e.code == 401:
                        # Auth failure — provider-level, perma-ban and move on.
                        last_error = f"HTTP {e.code}: {err_text[:200]}"
                        _record_failure(provider, http_code=e.code)
                        break
                    if e.code in (429, 503):
                        # Key-level throttle — cool this key down, rotate to another.
                        self.key_pool.mark_rate_limited(key_info, cooldown_seconds=60.0)
                        last_error = f"HTTP {e.code}: {err_text[:200]}"
                        continue
                    # Other HTTP errors — provider-level failure, trip breaker.
                    last_error = f"HTTP {e.code}: {err_text[:200]}"
                    _record_failure(provider, http_code=e.code)
                    break
                except Exception as e:
                    logger.warning(f"Error calling provider {provider}: {e}")
                    last_error = str(e)
                    _record_failure(provider)
                    break

        # Fallback offline simulation
        logger.warning(f"All live API providers unreachable or unconfigured for {model_alias}. Using simulation fallback (last error: {last_error}).")
        return {
            "id": f"msg_sim_{int(time.time()*1000)}",
            "type": "message",
            "role": "assistant",
            "model": model_alias,
            "content": [
                {
                    "type": "text",
                    "text": f"[SIMULATION — Model: {model_alias}]\nRequest processed via offline backup synthesis. All live providers failed."
                }
            ],
            "stop_reason": "end_turn",
            "stop_sequence": None,
            "usage": {"input_tokens": 0, "output_tokens": 0},
            "simulation_fallback": True,  # flag for callers to detect synthetic responses
        }

# Global Singleton
default_fabric = MultiProviderFabric()
