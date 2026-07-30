"""
Claude API Key Pool Proxy Server
Exposes Anthropic-compatible and OpenAI-compatible API endpoints backed by multi-provider key pools.
"""
import os
import sys
import json
import time
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from typing import Dict, Any
from providers.key_pool import default_key_pool
from providers.multi_provider_fabric import default_fabric

logger = logging.getLogger("claude_proxy")

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Threaded HTTP server to handle concurrent requests."""
    daemon_threads = True

class ClaudeProxyHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress default noisy access logs
        pass

    def send_json_response(self, code: int, data: Dict[str, Any]):
        body = json.dumps(data).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

    def do_GET(self):
        if self.path == "/health":
            self.send_json_response(200, {"status": "ok", "service": "Claude-Shaped Key Pool Proxy", "timestamp": time.time()})
        elif self.path == "/status":
            summary = default_key_pool.get_summary()
            self.send_json_response(200, {"status": "active", "key_pools": summary, "timestamp": time.time()})
        else:
            self.send_json_response(404, {"error": "Endpoint not found"})

    def do_POST(self):
        content_len = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_len) if content_len > 0 else b"{}"

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

            response_data = default_fabric.dispatch_request(
                model_alias=model,
                messages=messages,
                system_prompt=system_prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            self.send_json_response(200, response_data)

        elif self.path in ("/v1/chat/completions", "/v1/chat/completions/"):
            model = req_data.get("model", "claude-3-7-sonnet")
            messages = req_data.get("messages", [])
            max_tokens = req_data.get("max_tokens", 4096)
            temperature = req_data.get("temperature", 0.7)

            anthropic_resp = default_fabric.dispatch_request(
                model_alias=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
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
                    {
                        "index": 0,
                        "message": {"role": "assistant", "content": text_content},
                        "finish_reason": "stop"
                    }
                ],
                "usage": anthropic_resp.get("usage", {})
            }
            self.send_json_response(200, openai_resp)
        else:
            self.send_json_response(404, {"error": "Unsupported proxy endpoint"})

class ProxyServerDaemon:
    def __init__(self, host: str = "0.0.0.0", port: int = 8085):
        self.host = host
        self.port = port
        self.server: Optional[ThreadedHTTPServer] = None
        self.thread: Optional[threading.Thread] = None

    def start(self):
        if self.server:
            return
        self.server = ThreadedHTTPServer((self.host, self.port), ClaudeProxyHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        logger.info(f"Claude API Key Pool Proxy running on http://{self.host}:{self.port}")

    def stop(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.server = None
            logger.info("Proxy server stopped.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    srv = ProxyServerDaemon(port=8085)
    srv.start()
    print(f"Proxy server running on port 8085... Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        srv.stop()
