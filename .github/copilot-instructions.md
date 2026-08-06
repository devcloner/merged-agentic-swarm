# Repository Instructions for Coding Agents

These instructions are read by GitHub Copilot Chat (VSCode) and are safe to
share with any coding agent working in this repository. Model keys and proxy
tokens are referenced by environment-variable name only — never hardcode a
secret value in a file.

## What this repo is

Merged Agentic Swarm is a Python 3.14 orchestration layer that routes requests
across a multi-provider model fabric (gemini, mistral, openrouter, nvidia_nim,
litellm, fcc-proxy, routatic-proxy, opencode) with:

- **MultiProviderFabric** — dispatch, cascading fallback, perma-ban, latency
  tracking (`src/merged_agentic_swarm/providers/`)
- **KeyPool** — per-provider key rotation with health checks
- **TaskMaster** — PRD → epic/subtask parsing
- **WaveGateController** — 4-wave gating with ownership-map checks
- **MultiLayeredAgenticOrchestrator** — the full PRD → execution → cold-path
  learning loop (`tools/agentic_orchestrator.py`)
- **ultraswarm workers** — codex / opencode / agy / pi / claude
  (see `docs/swarm_project_prd.md`)

## Model discovery on this host

Coding agents that need a model list can query these OpenAI/Anthropic-compatible
endpoints (all on localhost):

| Endpoint                    | Auth (env var)            | Shape         | Notes                              |
| --------------------------- | ------------------------- | ------------- | ---------------------------------- |
| `http://127.0.0.1:4000/v1/models` | `LITELLM_PROXY_KEY` | OpenAI        | litellm virtual fleet (~17 routes: `gemini-batch`, `smart-auto`, `fast-flash`, …) |
| `http://127.0.0.1:8080/v1/models`  | `FCC_AUTH_TOKEN`          | OpenAI        | free-claude-code gateway            |
| `http://127.0.0.1:8317/v1/models`  | (config.local)            | OpenAI        | CLIProxyAPI                         |
| `http://127.0.0.1:3456/v1/models`  | routatic token            | OpenAI        | routatic proxy                      |

Prefer `LITELLM_PROXY_KEY` for anything that can consume an OpenAI-shaped API.
For Claude-shaped calls (`/v1/messages`), use the fcc gateway on `:8080`.

## Commands

- Install deps: `uv sync`
- Run a file: `uv run python path/to/file.py` (never bare `python`)
- Full test suite: `uv run pytest -v --tb=short`
- CI (must pass before pushing): `bash scripts/ci.sh`
- Lint/format: `uv run ruff check .` / `uv run ruff format --check .`

## Code rules that matter here

- Python 3.14 target (ruff `py314`). Under PEP 758, `except A, B:` is valid on
  3.14 only — do not parenthesize except clauses, ruff strips the parens back
  and 3.12/3.13 reject both forms' grammar anyway (hence the 3.14 floor).
- No `# type: ignore`. Fix the underlying type.
- Prefer top-level imports; avoid `TYPE_CHECKING` for first-party code.
- DRY; remove dead code; config over literals.
- Keep modules minimal and modular.

## Versioning

Every commit on `main` that changes a production file bumps the version in
`pyproject.toml` (PATCH for fixes, MINOR for new features) and runs `uv lock`.
