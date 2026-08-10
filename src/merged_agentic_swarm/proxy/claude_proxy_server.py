"""
Claude API Key Pool Proxy Server
Exposes Anthropic-compatible, OpenAI-compatible API endpoints, and audio transcription
backed by multi-provider key pools / NVIDIA NIM Whisper.
"""

import argparse
import json
import logging
import os
import re
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from typing import Any

import requests

from merged_agentic_swarm.fast_fallback import default_fast_fallback
from merged_agentic_swarm.fast_pool import warm_all
from merged_agentic_swarm.providers.key_pool import default_key_pool
from merged_agentic_swarm.providers.multi_provider_fabric import default_fabric

logger = logging.getLogger("claude_proxy")

FAST_FALLBACK_FLAG = "FAST_FALLBACK_ENABLED"


def _proxy_dispatch(
    model_alias: str,
    messages: list[dict[str, Any]],
    system_prompt: str | None = None,
    max_tokens: int = 4096,
    temperature: float = 0.7,
) -> dict[str, Any]:
    """Route a request through the hedged fast-fallback router when enabled.

    Both routers return the same Anthropic-shaped dict (with a simulation
    fallback), so the two dispatch paths are interchangeable at the proxy.
    """
    if os.environ.get(FAST_FALLBACK_FLAG, "").lower() in ("1", "true", "yes"):
        return default_fast_fallback.dispatch(
            model_alias=model_alias,
            messages=messages,
            system_prompt=system_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
        )
    return default_fabric.dispatch_request(
        model_alias=model_alias,
        messages=messages,
        system_prompt=system_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
    )


# ── Request body size limits ─────────────────────────────────────────────
MAX_JSON_BODY_BYTES = 5 * 1024 * 1024  # 5 MiB for JSON endpoints
MAX_AUDIO_BODY_BYTES = 25 * 1024 * 1024  # 25 MiB for audio transcription

# ── Audio transcription helpers ──────────────────────────────────────────

MIME_MAP = {
    "wav": "audio/wav",
    "mp3": "audio/mpeg",
    "ogg": "audio/ogg",
    "m4a": "audio/mp4",
    "webm": "audio/webm",
    "flac": "audio/flac",
    "aac": "audio/aac",
}


def _parse_multipart(body: bytes, content_type: str) -> tuple[bytes | None, str | None, str | None]:
    """Return (file_bytes, file_name, model_name) from a multipart body."""
    m = re.search(r'boundary=(?:"([^"]+)"|([^;]+))', content_type)
    if not m:
        return None, None, None
    boundary = (m.group(1) or m.group(2)).encode()

    file_data = file_name = None
    model_name = "openai/whisper-large-v3"

    for part in body.split(b"--" + boundary):
        if b"Content-Disposition" not in part:
            continue
        hdr_end = part.find(b"\r\n\r\n")
        if hdr_end == -1:
            continue
        headers_raw = part[:hdr_end].decode("utf-8", errors="replace")
        body_data = part[hdr_end + 4 :]
        # Strip trailing boundary markers and CRLF
        if body_data.endswith(b"\r\n"):
            body_data = body_data[:-2]
        if body_data.endswith(b"--"):
            body_data = body_data[:-2]

        nm = re.search(r'name="([^"]*)"', headers_raw)
        if not nm:
            continue
        field_name = nm.group(1)

        if field_name == "file":
            file_data = body_data
            fn = re.search(r'filename="([^"]*)"', headers_raw)
            file_name = fn.group(1) if fn else "audio.wav"
        elif field_name == "model":
            model_name = body_data.decode("utf-8", errors="replace").strip()

    return file_data, file_name, model_name


def _forward_transcription(
    audio_data: bytes,
    file_name: str | None,
    model_name: str,
) -> dict[str, Any] | tuple[int, dict[str, str]]:
    """Forward a transcription request to the configured Whisper backend."""
    backend_url = os.environ.get(
        "WHISPER_BACKEND_URL",
        "http://localhost:11434/v1/audio/transcriptions",
    )
    api_key = os.environ.get("WHISPER_API_KEY", "")

    ext = file_name.rsplit(".", 1)[-1].lower() if file_name and "." in file_name else "wav"
    mime_type = MIME_MAP.get(ext, "audio/wav")

    try:
        resp = requests.post(
            backend_url,
            files={"file": (file_name or "audio.wav", audio_data, mime_type)},
            data={"model": model_name},
            headers={"Authorization": f"Bearer {api_key}"} if api_key else {},
            timeout=60,
        )
    except requests.exceptions.ConnectionError:
        return 503, {"error": "Whisper backend unavailable (NVIDIA NIM not running)"}
    except Exception as exc:
        return 500, {"error": f"Transcription error: {exc}"}

    if resp.status_code == 200:
        return resp.json()
    return resp.status_code, {"error": f"NIM transcription failed: {resp.text}"}


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Threaded HTTP server to handle concurrent requests."""

    daemon_threads = True


class ClaudeProxyHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress default noisy access logs
        pass

    def send_json_response(self, code: int, data: dict[str, Any]):
        body = json.dumps(data).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()
        self.wfile.write(body)

    def _send_413(self, message: str):
        """Reject an oversized body. Close the connection since the unread
        bytes would otherwise desync the request stream."""
        self.send_response(413)
        self.send_header("Content-Type", "application/json")
        body = json.dumps({"error": message}).encode("utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

    def _authorized(self) -> bool:
        """Enforce the inbound proxy token (ANTHROPIC_AUTH_TOKEN, default 'freecc').

        Health/status endpoints and CORS preflight stay unauthenticated so
        monitors can probe the service; all data endpoints gate on the token.
        """
        expected = os.environ.get("ANTHROPIC_AUTH_TOKEN") or "freecc"
        supplied = self.headers.get("x-api-key")
        if supplied is None:
            authz = self.headers.get("Authorization", "")
            if authz.startswith("Bearer "):
                supplied = authz[len("Bearer ") :]
        if not supplied or supplied != expected:
            self.send_json_response(401, {"error": "Invalid or missing API token"})
            return False
        return True

    def do_GET(self):
        if self.path == "/health":
            self.send_json_response(
                200, {"status": "ok", "service": "Claude-Shaped Key Pool Proxy", "timestamp": time.time()}
            )
        elif self.path == "/status":
            summary = default_key_pool.get_summary()
            self.send_json_response(200, {"status": "active", "key_pools": summary, "timestamp": time.time()})
        else:
            self.send_json_response(404, {"error": "Endpoint not found"})

    def do_POST(self):
        if not self._authorized():
            return

        content_len = int(self.headers.get("Content-Length", 0))
        # Reject oversized bodies up front so a large/malicious request is
        # never buffered into memory. Audio multipart gets a higher cap.
        if self.path in ("/v1/audio/transcriptions", "/v1/audio/transcriptions/"):
            if content_len > MAX_AUDIO_BODY_BYTES:
                self._send_413("Audio request body exceeds size limit")
                return
        elif content_len > MAX_JSON_BODY_BYTES:
            self._send_413("Request body exceeds size limit")
            return
        post_body = self.rfile.read(content_len) if content_len > 0 else b"{}"

        # ── Audio transcription (multipart) ────────────────────────────
        if self.path in ("/v1/audio/transcriptions", "/v1/audio/transcriptions/"):
            self._handle_audio_transcription(post_body)
            return

        # ── JSON-based endpoints ────────────────────────────────────────
        try:
            req_data = json.loads(post_body.decode("utf-8"))
        except Exception:
            self.send_json_response(400, {"error": "Invalid JSON body"})
            return

        if self.path in ("/v1/messages", "/v1/messages/"):
            model = req_data.get("model", "claude-3-7-sonnet")
            messages = req_data.get("messages", [])
            system_prompt = req_data.get("system")
            max_tokens = req_data.get("max_tokens", 4096)
            temperature = req_data.get("temperature", 0.7)

            response_data = _proxy_dispatch(
                model_alias=model,
                messages=messages,
                system_prompt=system_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            self.send_json_response(200, response_data)

        elif self.path in ("/v1/chat/completions", "/v1/chat/completions/"):
            model = req_data.get("model", "claude-3-7-sonnet")
            messages = req_data.get("messages", [])
            max_tokens = req_data.get("max_tokens", 4096)
            temperature = req_data.get("temperature", 0.7)

            anthropic_resp = _proxy_dispatch(
                model_alias=model, messages=messages, max_tokens=max_tokens, temperature=temperature
            )

            # Convert back to OpenAI format for chat completions endpoint callers
            text_content = ""
            if anthropic_resp.get("content"):
                text_content = anthropic_resp["content"][0].get("text", "")

            openai_resp = {
                "id": anthropic_resp.get("id"),
                "object": "chat.completion",
                "created": int(time.time()),
                "model": model,
                "choices": [
                    {"index": 0, "message": {"role": "assistant", "content": text_content}, "finish_reason": "stop"}
                ],
                "usage": anthropic_resp.get("usage", {}),
            }
            self.send_json_response(200, openai_resp)
        else:
            self.send_json_response(404, {"error": "Unsupported proxy endpoint"})

    # ── Audio transcription handler ───────────────────────────────────
    def _handle_audio_transcription(self, post_body: bytes) -> None:
        content_type = self.headers.get("Content-Type", "")
        audio_data, file_name, model_name = _parse_multipart(post_body, content_type)

        if not audio_data:
            self.send_json_response(400, {"error": "No audio file found in request"})
            return

        result = _forward_transcription(audio_data, file_name, model_name)

        if isinstance(result, tuple):
            code, body = result
            self.send_json_response(code, body)
        else:
            self.send_json_response(200, result)


class ProxyServerDaemon:
    def __init__(self, host: str = "0.0.0.0", port: int = 8085):
        self.host = host
        self.port = port
        self.server: ThreadedHTTPServer | None = None
        self.thread: threading.Thread | None = None

    def start(self):
        if self.server:
            return
        self.server = ThreadedHTTPServer((self.host, self.port), ClaudeProxyHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        # Best-effort pre-warm in a daemon thread so startup is never blocked:
        # primes the shared DNS cache and establishes warm connections for
        # first-request latency reduction.
        threading.Thread(target=self._prewarm, daemon=True).start()
        logger.info(f"Claude API Key Pool Proxy running on http://{self.host}:{self.port}")

    @staticmethod
    def _prewarm() -> None:
        results = warm_all()
        ok = sum(1 for v in results.values() if v)
        logger.info(f"Connection pool pre-warmed: {ok}/{len(results)} provider hosts reachable")

    def stop(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.server = None
            logger.info("Proxy server stopped.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Claude-Shaped Key Pool Proxy")
    parser.add_argument("--host", default="0.0.0.0", help="Bind address (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8089, help="Bind port (default: 8089)")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    srv = ProxyServerDaemon(host=args.host, port=args.port)
    srv.start()
    print(f"Proxy server running on {args.host}:{args.port}... Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        srv.stop()
