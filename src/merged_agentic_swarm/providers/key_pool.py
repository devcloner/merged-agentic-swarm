"""
API Key Pool Manager & Key Rotator
Supports multi-provider key rotation, quota handling, cooldown tracking, and health checks.
"""

import logging
import os
import threading
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any

logger = logging.getLogger("key_pool")


class KeyStatus(str, Enum):
    ACTIVE = "active"
    COOLDOWN = "cooldown"
    EXHAUSTED = "exhausted"
    DISABLED = "disabled"


@dataclass
class APIKeyInfo:
    key_id: str
    provider: str
    secret_value: str
    status: KeyStatus = KeyStatus.ACTIVE
    cooldown_until: float = 0.0
    failure_count: int = 0
    total_requests: int = 0
    total_tokens: int = 0
    last_used_at: float = 0.0
    avg_latency_ms: float = 0.0

    def __repr__(self):
        """Avoid leaking the secret value in logs/debug output."""
        return (
            f"APIKeyInfo(key_id='{self.key_id}', provider='{self.provider}', "
            f"status='{self.status.value}', failure_count={self.failure_count}, "
            f"total_requests={self.total_requests})"
        )


class KeyPoolManager:
    def __init__(self, env_file_path: str | None = None):
        if env_file_path is None:
            env_file_path = os.path.expanduser("~/env.txt")
        self.env_file_path = env_file_path
        self.keys_by_provider: dict[str, list[APIKeyInfo]] = {}
        self._lock = threading.Lock()
        self.load_keys()

    def _collect_keys_from_sources(self) -> list[tuple[str, str, str]]:
        """Gather (provider, secret_value, key_id) candidates from all key sources.

        Placeholder strings (e.g. "Gemini API Key...") are dropped so callers can
        trust the returned list contains only usable keys.
        """
        candidates: list[tuple[str, str, str]] = []

        # 1. Parse env.txt if exists
        env_vars = {}
        if os.path.exists(self.env_file_path):
            with open(self.env_file_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        env_vars[k.strip()] = v.strip().strip('"').strip("'")

        # 2. Extract Gemini Keys (single & comma-separated pool)
        gemini_keys = []
        if env_vars.get("GEMINI_API_KEYS"):
            gemini_keys.extend([k.strip() for k in env_vars["GEMINI_API_KEYS"].split(",") if k.strip()])
        if env_vars.get("GEMINI_API_KEY") and env_vars["GEMINI_API_KEY"] not in gemini_keys:
            gemini_keys.append(env_vars["GEMINI_API_KEY"])

        # Load from gemini-keys/working-keys.txt if available (also check misspelled legacy path)
        for candidate in (
            os.path.expanduser("~/gemini-keys/working-keys.txt"),
            os.path.expanduser("~/gemlni-keys/working-keys.txt"),
        ):
            if os.path.exists(candidate):
                working_keys_file = candidate
                break
        else:
            working_keys_file = None
        if working_keys_file and os.path.exists(working_keys_file):
            with open(working_keys_file, "r", encoding="utf-8") as f:
                for line in f:
                    k = line.strip()
                    if k and k not in gemini_keys:
                        gemini_keys.append(k)

        for idx, key in enumerate(gemini_keys):
            candidates.append(("gemini", key, f"gemini-{idx + 1}"))

        # 3. OpenCode Keys
        opencode_key = env_vars.get("OPENCODE_API_KEY") or os.environ.get("OPENCODE_API_KEY")
        if opencode_key:
            candidates.append(("opencode", opencode_key, "opencode-main"))

        # 4. Groq Keys
        groq_key = env_vars.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
        if groq_key:
            candidates.append(("groq", groq_key, "groq-main"))

        # 5. Mistral Keys
        mistral_key = env_vars.get("MISTRAL_API_KEY") or os.environ.get("MISTRAL_API_KEY")
        if mistral_key:
            candidates.append(("mistral", mistral_key, "mistral-main"))

        # 6. NVIDIA NIM Keys
        nim_key = env_vars.get("NVIDIA_NIM_API_KEY") or os.environ.get("NVIDIA_NIM_API_KEY")
        if nim_key:
            candidates.append(("nvidia_nim", nim_key, "nvidia-main"))

        # 7. OpenRouter Keys
        openrouter_key = env_vars.get("OPENROUTER_API_KEY") or os.environ.get("OPENROUTER_API_KEY")
        if openrouter_key:
            candidates.append(("openrouter", openrouter_key, "openrouter-main"))

        # 8. AlibabaCloud Keys
        alibaba_key = env_vars.get("ALIBABACLOUD_API_KEY") or os.environ.get("ALIBABACLOUD_API_KEY")
        if alibaba_key:
            candidates.append(("alibabacloud", alibaba_key, "alibabacloud-main"))

        # 9. DigitalOcean / Custom Keys
        do_key = env_vars.get("DO_API_KEY") or env_vars.get("CUSTOM_API_KEY") or os.environ.get("DO_API_KEY")
        if do_key:
            candidates.append(("digitalocean", do_key, "digitalocean-main"))

        # 10. AWS Bedrock — needs access key + secret (SigV4), store as compound
        aws_access_key = env_vars.get("AWS_ACCESS_KEY_ID") or os.environ.get("AWS_ACCESS_KEY_ID")
        aws_secret_key = env_vars.get("AWS_SECRET_ACCESS_KEY") or os.environ.get("AWS_SECRET_ACCESS_KEY")
        if aws_access_key and aws_secret_key:
            candidates.append(("amazonaws", f"{aws_access_key}:{aws_secret_key}", "aws-bedrock-main"))

        # 10. liteLLM Proxy (local, fast, low-latency)
        litellm_key = env_vars.get("LITELLM_PROXY_KEY")
        if litellm_key:
            candidates.append(("litellm", litellm_key, "litellm-main"))

        # 11. FCC Proxy (localhost:8080) — uses ANTHROPIC_AUTH_TOKEN or falls back to "freecc"
        fcc_proxy_key = env_vars.get("ANTHROPIC_AUTH_TOKEN") or os.environ.get("ANTHROPIC_AUTH_TOKEN") or "freecc"
        candidates.append(("fcc-proxy", fcc_proxy_key, "fcc-proxy-main"))

        # 12. Routatic-proxy (localhost:3456) — standalone model router,
        #     does not interfere with FCC on port 8080. Uses same ANTHROPIC_AUTH_TOKEN.
        candidates.append(("routatic-proxy", fcc_proxy_key, "routatic-proxy-main"))

        # 13. CloudCLI (cloneclove.com) — remote agent-triggering API
        cloudcli_key = env_vars.get("CLOUDCLI_API_KEY") or os.environ.get("CLOUDCLI_API_KEY")
        if cloudcli_key:
            candidates.append(("cloudcli", cloudcli_key, "cloudcli-main"))

        return [
            (provider, secret, key_id)
            for provider, secret, key_id in candidates
            if secret and not secret.startswith("Gemini API Key")
        ]

    def load_keys(self):
        """Loads API keys from env file, environment variables, and local key files."""
        self.keys_by_provider = {}
        for provider, secret_value, key_id in self._collect_keys_from_sources():
            self.add_key(provider, secret_value, key_id)
        logger.info(f"Loaded key pools for providers: {list(self.keys_by_provider.keys())}")

    def reload(self):
        """Hot-reload keys from all sources, preserving runtime stats for persistent keys.

        Key rotation typically swaps secret values while keeping the same key_id
        (e.g. gemini-1). Reconcile by key_id so cooldowns, failure counts, and usage
        counters survive the reload; only brand-new keys get fresh state. Runs under
        self._lock so get_key/mark_* never observe a half-built pool.
        """
        with self._lock:
            existing = {
                key.key_id: key
                for keys in self.keys_by_provider.values()
                for key in keys
            }
            new_pools: dict[str, list[APIKeyInfo]] = {}
            added = 0
            preserved = 0
            for provider, secret_value, key_id in self._collect_keys_from_sources():
                prev = existing.get(key_id)
                if prev is not None:
                    prev.secret_value = secret_value
                    new_pools.setdefault(provider, []).append(prev)
                    preserved += 1
                else:
                    key_info = APIKeyInfo(key_id=key_id, provider=provider, secret_value=secret_value)
                    new_pools.setdefault(provider, []).append(key_info)
                    added += 1
            self.keys_by_provider = new_pools
            logger.info(
                f"Reloaded key pools: {added} new, {preserved} preserved across "
                f"{list(self.keys_by_provider.keys())}"
            )

    def add_key(self, provider: str, secret_value: str, key_id: str):
        if not secret_value or secret_value.startswith("Gemini API Key"):
            # Skip placeholder strings
            return
        if provider not in self.keys_by_provider:
            self.keys_by_provider[provider] = []
        key_info = APIKeyInfo(key_id=key_id, provider=provider, secret_value=secret_value)
        self.keys_by_provider[provider].append(key_info)

    def get_key(self, provider: str) -> APIKeyInfo | None:
        """Gets an active API key using round-robin / least-used strategy."""
        with self._lock:
            return self._get_key_unlocked(provider)

    def _get_key_unlocked(self, provider: str) -> APIKeyInfo | None:
        """Internal: must be called while holding self._lock."""
        now = time.time()
        keys = self.keys_by_provider.get(provider, [])
        if not keys:
            return None

        # Check and recover cooldowns
        available_keys = []
        for k in keys:
            if k.status == KeyStatus.COOLDOWN and now >= k.cooldown_until:
                k.status = KeyStatus.ACTIVE
                k.failure_count = max(0, k.failure_count - 1)
            if k.status == KeyStatus.ACTIVE:
                available_keys.append(k)

        if not available_keys:
            # Do NOT force-recover a still-cooling key: reusing a throttled key
            # just re-triggers its 429 and resets the cooldown, so the pool never
            # recovers and the fabric cascade never advances to a healthy provider.
            return None

        # Sort by total requests then last used time
        available_keys.sort(key=lambda x: (x.total_requests, x.last_used_at))
        selected = available_keys[0]
        selected.last_used_at = now
        selected.total_requests += 1
        return selected

    def mark_success(self, key_info: APIKeyInfo, latency_ms: float = 0.0, tokens: int = 0):
        with self._lock:
            key_info.status = KeyStatus.ACTIVE
            key_info.failure_count = 0
            key_info.total_tokens += tokens
            if key_info.avg_latency_ms == 0.0:
                key_info.avg_latency_ms = latency_ms
            else:
                key_info.avg_latency_ms = (key_info.avg_latency_ms * 0.8) + (latency_ms * 0.2)

    def mark_rate_limited(self, key_info: APIKeyInfo, cooldown_seconds: float = 60.0):
        with self._lock:
            key_info.status = KeyStatus.COOLDOWN
            key_info.cooldown_until = time.time() + cooldown_seconds
            key_info.failure_count += 1
            logger.warning(
                f"Key {key_info.key_id} for provider {key_info.provider} rate-limited. Cooldown for {cooldown_seconds}s."
            )

    def get_summary(self) -> dict[str, Any]:
        with self._lock:
            return self._get_summary_unlocked()

    def _get_summary_unlocked(self) -> dict[str, Any]:
        summary = {}
        now = time.time()
        for provider, keys in self.keys_by_provider.items():
            cooling = [k for k in keys if k.status == KeyStatus.COOLDOWN and now < k.cooldown_until]
            latencies = [k.avg_latency_ms for k in keys if k.avg_latency_ms > 0]
            summary[provider] = {
                "total_keys": len(keys),
                "active_keys": sum(
                    1
                    for k in keys
                    if k.status == KeyStatus.ACTIVE
                    or (k.status == KeyStatus.COOLDOWN and now >= k.cooldown_until)
                ),
                "cooldown_keys": len(cooling),
                "exhausted_keys": sum(1 for k in keys if k.status == KeyStatus.EXHAUSTED),
                "next_cooldown_until": min((k.cooldown_until for k in cooling), default=None),
                "avg_latency_ms": round(sum(latencies) / len(latencies), 2) if latencies else 0.0,
                "total_requests": sum(k.total_requests for k in keys),
                "total_tokens": sum(k.total_tokens for k in keys),
            }
        return summary


# Global Singleton
default_key_pool = KeyPoolManager()
