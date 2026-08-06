# VSCode remote, Copilot Chat, and Kepler — model discovery on this VPS

How coding agents that connect to this VPS find and use the model fleet, and
how this repo makes that work out of the box.

## The three levers

1. **VSCode Copilot Chat** reads `.github/copilot-instructions.md` (enabled by
   `.vscode/settings.json`). It gets repo context and the model-endpoint table,
   so its answers match this codebase. Copilot's *model picker* is resolved
   server-side by GitHub, not from repo files — the endpoint table in the
   instructions is the discovery aid it *can* consume.
2. **Kepler** (GitKraken agent server, `~/.kepler-server`, port from
   `data/server.port`) spawns the Claude Code CLI over ACP with
   `--setting-sources=user,project,local`, so the models Kepler sees are the
   Claude Code models. This repo pins those in `.claude/settings.json`
   (`ANTHROPIC_BASE_URL=http://127.0.0.1:8080`, model `claude-sonnet-5[1m]`);
   the auth token comes from the machine-level `~/.claude/settings.json` and is
   **never committed**.
3. **Auto-discovery of the model list** comes from the OpenAI-shaped gateways:
   litellm on `:4000` is the canonical one (`GET /v1/models` with
   `LITELLM_PROXY_KEY` returns the virtual fleet — `gemini-batch`,
   `smart-auto`, `fast-flash`, `high-throughput`, …). Any agent/tool with an
   OpenAI-compatible provider field can point at it and populate its model
   dropdown automatically.

## Endpoint reference (all localhost)

| Port | Service          | Auth env var          | API shape      | `/v1/models` |
| ---- | ---------------- | --------------------- | -------------- | ------------ |
| 4000 | litellm          | `LITELLM_PROXY_KEY`   | OpenAI + Anthropic | 17 virtual routes |
| 8080 | fcc-server       | `FCC_AUTH_TOKEN`      | Anthropic-shaped proxy | yes (auth required) |
| 8317 | CLIProxyAPI      | per `config.local.yaml` | OpenAI       | yes          |
| 3456 | routatic-proxy   | routatic token        | OpenAI         | yes          |

## One-time setup (this VPS already has the servers running)

- **Kepler** — already running (v0.8.1, PID in `~/.kepler-server/data/server.pid`).
  Open its UI at `http://<vps>:<port>/` where `<port>` is in
  `~/.kepler-server/data/server.port`; its workspace MCP is
  `http://127.0.0.1:<port>/mcp`.
- **Copilot CLI** — `~/.copilot` exists; authenticate with your GitHub account
  (`copilot auth` / the `gh copilot` flow) if the session expired.
- **VSCode remote** — extensions live in `~/.vscode-server/extensions` on the
  server (GitLens + a Claude Dev fork are installed). Install "GitHub Copilot
  Chat" from the *client*; it syncs to the server. Open the repo, and Copilot
  Chat picks up `.github/copilot-instructions.md` automatically.
- **A provider-style agent (e.g. a Claude Dev fork)** — set its OpenAI-compatible
  API URL to `http://127.0.0.1:4000/v1` and its key to `$LITELLM_PROXY_KEY`; the
  model dropdown then populates from litellm automatically.

## Rules

- Never commit a real token. Reference by env-var name only (`LITELLM_PROXY_KEY`,
  `FCC_AUTH_TOKEN`). The committed `.claude/settings.json` sets only the base URL
  and model name; the token stays in `~/.claude/settings.json`.
- These files are inert on machines without the local proxies — delete
  `.claude/settings.json` if you don't run the gateway stack.
