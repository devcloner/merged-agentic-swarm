#!/usr/bin/env bash
set -euo pipefail

# ── discover_environment.sh ──────────────────────────────────────────────
# Inspects the local runtime environment and writes a structured JSON
# report to config/runtime/environment.generated.json. The same report is
# printed to stdout as pretty-printed JSON. Secret values are redacted.
# ─────────────────────────────────────────────────────────────────────────

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUTPUT_DIR="$REPO_ROOT/config/runtime"
OUTPUT_FILE="$OUTPUT_DIR/environment.generated.json"
OPENCODE_BIN="$HOME/.opencode/bin/opencode"
TASKMASTER_CONFIG="$HOME/.taskmaster/config.json"
REGISTRY_DIR="$REPO_ROOT/docs/agentic/registry"

# ── help ─────────────────────────────────────────────────────────────────
usage() {
    cat <<'EOF'
Usage: discover_environment.sh [--help]

Discover the local runtime environment and write a structured JSON report
to config/runtime/environment.generated.json. The same report is printed to
stdout as pretty-printed JSON.

Flags:
  --help    Show this help message and exit
EOF
    exit 0
}

[[ "${1:-}" == "--help" ]] && usage

# ── helpers ──────────────────────────────────────────────────────────────
critical_fail() {
    local msg="$1"
    echo "CRITICAL: $msg" >&2
    exit 1
}

# ── discover and build the report ────────────────────────────────────────
echo "Discovering environment..." >&2
mkdir -p "$OUTPUT_DIR"

python3 <<'PYEOF' > "$OUTPUT_FILE"
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

REPO_ROOT = os.getcwd()
OPENCODE_BIN = os.path.expanduser("~/.opencode/bin/opencode")
TASKMASTER_CONFIG = os.path.expanduser("~/.taskmaster/config.json")
REGISTRY_DIR = os.path.join(REPO_ROOT, "docs", "agentic", "registry")

def run(cmd, **kwargs):
    """Run a command and return stdout, or a fallback string on failure."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15, **kwargs)
        return result.stdout.strip()
    except Exception:
        return ""

def run_code(cmd, fallback="not-found"):
    """Run a command expecting a non-zero exit, return fallback on failure."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        return result.stdout.strip()
    except Exception:
        return fallback

# ── OS ───────────────────────────────────────────────────────────────────
os_name_raw = run(["lsb_release", "-ds"])
if not os_name_raw:
    try:
        with open("/etc/os-release") as f:
            for line in f:
                if line.startswith("PRETTY_NAME="):
                    os_name_raw = line.strip().split("=", 1)[1].strip('"')
                    break
    except Exception:
        os_name_raw = "unknown"
if not os_name_raw:
    os_name_raw = run(["uname", "-s"]) or "unknown"

os_name = os_name_raw
os_arch = run(["uname", "-m"]) or "unknown"
os_kernel = run(["uname", "-r"]) or "unknown"

# ── Runtimes ─────────────────────────────────────────────────────────────
py_ver = run(["python3", "--version"]).split()[-1] if run(["python3", "--version"]) else "not-found"
node_ver_raw = run(["node", "--version"])
node_ver = node_ver_raw.lstrip("v") if node_ver_raw else "not-found"
uv_ver = run(["uv", "--version"]).split()[1] if run(["uv", "--version"]) else "not-found"
git_ver = run(["git", "--version"]).split()[-1] if run(["git", "--version"]) else "not-found"
docker_ver = "not-found"
try:
    docker_out = run(["docker", "--version"])
    if docker_out:
        docker_ver = docker_out.split()[2].rstrip(",")
except Exception:
    pass

# ── Listening ports ──────────────────────────────────────────────────────
ports_list = []
ss_raw = run(["ss", "-tlnp"])
for line in ss_raw.split("\n")[1:]:  # skip header
    if not line.strip():
        continue
    parts = line.split()
    if len(parts) < 5:
        continue
    address = parts[3]
    port = address.rsplit(":", 1)[-1]
    proc_part = " ".join(parts[5:]) if len(parts) > 5 else ""
    m = re.search(r'users:\(\(\"([^\"]+)\"', proc_part)
    process = m.group(1) if m else ""
    ports_list.append({
        "port": port,
        "address": address,
        "process": process
    })

# ── Matched processes (redacted) ─────────────────────────────────────────
def redact(s: str) -> str:
    """Replace secret patterns."""
    s = re.sub(
        r'(key|token|password|secret|auth)\s*[:=]\s*\S+',
        r'\1=REDACTED',
        s,
        flags=re.IGNORECASE
    )
    return s

procs_list = []
ps_raw = run(["ps", "aux"])
for line in ps_raw.split("\n")[1:]:
    if not line.strip():
        continue
    if re.search(r'fcc|proxy|opencode|litellm|task', line, re.IGNORECASE) and "grep" not in line:
        parts = line.split(None, 10)
        if len(parts) >= 11:
            procs_list.append({
                "pid": parts[1],
                "user": parts[0],
                "command": redact(parts[10])
            })

# ── OpenCode binary ──────────────────────────────────────────────────────
oc_binary = OPENCODE_BIN
oc_exists = os.path.isfile(oc_binary)
oc_executable = os.access(oc_binary, os.X_OK)
oc_version = "n/a"
if oc_executable:
    oc_version = run([oc_binary, "--version"]) or "error"

# ── Proxy on port 8080 ───────────────────────────────────────────────────
proxy_reachable = False
proxy_model_count = 0
proxy_http_code = 0
try:
    import urllib.request
    req = urllib.request.Request(
        "http://localhost:8080/v1/models",
        headers={"Authorization": "Bearer freecc"}
    )
    resp = urllib.request.urlopen(req, timeout=10)
    proxy_http_code = resp.getcode()
    if proxy_http_code == 200:
        body = json.loads(resp.read().decode())
        proxy_model_count = len(body.get("data", []))
        proxy_reachable = True
except Exception:
    proxy_http_code = 0

# ── Port 4000 (expected dead) ────────────────────────────────────────────
port4000_http_code = 0
port4000_status = "dead"
try:
    import urllib.request
    resp = urllib.request.urlopen("http://localhost:4000", timeout=5)
    port4000_http_code = resp.getcode()
    port4000_status = "alive (unexpected)"
except Exception:
    port4000_http_code = 0
    port4000_status = "dead"

# ── Task Master config ───────────────────────────────────────────────────
tm_exists = os.path.isfile(TASKMASTER_CONFIG)
tm_provider = "n/a"
tm_model = "n/a"
if tm_exists:
    try:
        with open(TASKMASTER_CONFIG) as f:
            tm_data = json.load(f)
        tm_provider = tm_data.get("models", {}).get("main", {}).get("provider", "unknown")
        tm_model = tm_data.get("models", {}).get("main", {}).get("modelId", "unknown")
    except Exception:
        tm_provider = "error"
        tm_model = "error"

# ── Registries ───────────────────────────────────────────────────────────
def count_lines(path, fallback=0):
    try:
        with open(path) as f:
            return sum(1 for _ in f)
    except Exception:
        return fallback

reg_knowledge = count_lines(f"{REGISTRY_DIR}/knowledge.jsonl")
reg_agents = count_lines(f"{REGISTRY_DIR}/agents.jsonl")
reg_chain = count_lines(f"{REGISTRY_DIR}/chain.jsonl")
reg_progress = count_lines(f"{REGISTRY_DIR}/progress.json")

# ── Sub-agent MCP on port 8000 ───────────────────────────────────────────
mcp_reachable = False
mcp_http_code = 0
try:
    import urllib.request
    resp = urllib.request.urlopen("http://localhost:8000", timeout=5)
    mcp_http_code = resp.getcode()
    mcp_reachable = True
except Exception:
    mcp_http_code = 0
    mcp_reachable = False

# ── Assemble report ──────────────────────────────────────────────────────
report = {
    "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "hostname": run(["hostname"]) or "unknown",
    "script_version": "1.0.0",
    "os": {
        "name": os_name,
        "arch": os_arch,
        "kernel": os_kernel
    },
    "runtimes": {
        "python": py_ver,
        "node": node_ver,
        "uv": uv_ver,
        "git": git_ver,
        "docker": docker_ver
    },
    "listening_ports": ports_list,
    "matched_processes": procs_list,
    "opencode": {
        "binary": oc_binary,
        "exists": oc_exists,
        "executable": oc_executable,
        "version": oc_version
    },
    "proxy_8080": {
        "host": "localhost",
        "port": 8080,
        "reachable": proxy_reachable,
        "http_status": proxy_http_code,
        "model_count": proxy_model_count
    },
    "port_4000": {
        "host": "localhost",
        "port": 4000,
        "expected": "dead",
        "status": port4000_status,
        "http_status": port4000_http_code
    },
    "taskmaster": {
        "config_path": TASKMASTER_CONFIG,
        "exists": tm_exists,
        "main_provider": tm_provider,
        "main_model": tm_model
    },
    "registries": {
        "directory": REGISTRY_DIR,
        "knowledge_jsonl_lines": reg_knowledge,
        "agents_jsonl_lines": reg_agents,
        "chain_jsonl_lines": reg_chain,
        "progress_json_lines": reg_progress
    },
    "sub_agent_mcp": {
        "host": "localhost",
        "port": 8000,
        "reachable": mcp_reachable,
        "http_status": mcp_http_code
    }
}

json.dump(report, sys.stdout, indent=2)
sys.stdout.write("\n")
PYEOF

# ── validate and print ───────────────────────────────────────────────────
if python3 -c "import json; json.load(open('$OUTPUT_FILE'))" 2>/dev/null; then
    echo "Valid JSON written to $OUTPUT_FILE" >&2
    echo "" >&2
    python3 -m json.tool "$OUTPUT_FILE"
    exit 0
else
    critical_fail "Output file $OUTPUT_FILE is not valid JSON"
fi
