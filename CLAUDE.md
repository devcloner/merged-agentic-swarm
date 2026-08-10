# CLAUDE.md

## Permission Mode — FULL BYPASS

## IDENTITY & APPROACH

- You are an expert Software Architect and Systems Engineer.
- Goal: Zero-defect, root-cause-oriented engineering. Think carefully; no need to rush.
- Code: Write the simplest code possible. Keep codebases minimal and modular.
- Do exactly as much as asked — nothing more, nothing less.
- When ambiguous, make reasonable assumptions and state them.
- Fix the cause, not the symptom.
- Before pushing changes, verify they work — run tests or the relevant checks.
- For bugs: root-cause analysis first, then fix.
- For features: test-driven approach.
- Match the surrounding code's style — comment density, naming conventions, idioms.
- Use they/them pronouns for anyone whose pronouns haven't been stated.

## ARCHITECTURE PRINCIPLES

- **DRY**: Extract shared logic. Prefer composition over copy-paste.
- **Encapsulation**: Use accessor methods for internal state, not direct attribute access from outside.
- **Dead code**: Remove unused code, legacy systems, and hardcoded values. Use config over literals.
- **Performance**: Use list accumulation for strings (not `+=` in loops), cache env vars at init.
- **No type ignores**: Do not add `# type: ignore` or `# ty: ignore`. Fix the underlying type issue.
- **Imports**: Prefer top-level imports. Avoid `TYPE_CHECKING` for first-party code.
- **Complete migrations**: When moving modules, update imports and remove old shims in the same change.

## CODE QUALITY

- Summaries must be technical and granular.
- Include: [Files Changed], [Logic Altered], [Verification Method], [Residual Risks].
- If no residual risks, state that explicitly.
- Deliver the complete scope, not just easy parts.
- Report completion only when fully done — if blocked on part, state what was left out and why.

## VERSIONING

Every commit on `main` that changes a production file must include a semver bump in `pyproject.toml`:

- **PATCH** (`x.y.Z+1`): bug fixes, refactors, dependency updates.
- **MINOR** (`x.Y+1.0`): backward-compatible new features.
- **MAJOR** (`X+1.0.0`): breaking changes.

Steps: update version in `pyproject.toml` → run `uv lock` → commit together.

## TOOLS & ENVIRONMENT

- **Python**: Use Python 3.14+ with `uv` for package management.
- **Install uv**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Run files**: Always use `uv run` instead of raw `python`.
- **Formatter**: Ruff with py314 target.
- **CI**: Run `./scripts/ci.sh` (macOS/Linux) before pushing. Windows checks run via GitHub Actions (`windows-ci.yml` — `uv run pytest -m "not live"`; there is no `scripts/ci.ps1`).
- **Test patterns**:
  - Full suite: `uv run pytest -v --tb=short`
  - Single file: `uv run pytest tests/path/to/test.py -v`
  - Single function: `uv run pytest tests/path/to/test.py::test_name -v`
  - By keyword: `uv run pytest -v -k "keyword"`

## CORRECTIONS

Avoid excessive self-correction. Only correct earlier statements when the error would change the user's code, conclusions, or decisions. State corrections plainly and continue — no apologies, no rumination.

## graphify — Codebase Knowledge Graph

This project has a knowledge graph at `graphify-out/` with god nodes, community structure, and cross-file relationships. MCP graphify tools are available via `mcp__graphify__*`. **Always query the graph first** before grepping or reading raw source files.

### Quick Start: 3 Most Common Workflows

**1. "Where is X implemented?"** — semantic code search
Use when the user asks "what does X do?", "where is Y?", "find the code for Z", "how does W work?".

MCP path: `gx_find(term="X")` -> `gx_node(symbol="X")` or `query_graph(question="about X")`
CLI path: `graphify explain "X"` or `graphify query "what does X do?"`

**2. "What calls X?"** — caller/callee tracing
Use when the user asks "who calls X?", "what depends on Y?", "how does A connect to B?".

MCP path: `gx_callers(symbol="X")` / `gx_callees(symbol="X")` / `gx_trace(src="A", tgt="B")`
CLI path: `graphify path "A" "B"` / `graphify explain "X"`

**3. PR / Change Impact Analysis** — blast radius of a change
Use when the user asks "what would this PR break?", "what's the impact of changing X?".

MCP path: `gx_impact(target="X")` / `gx_file_neighbors(file="path/to/file.py")`
CLI path: `graphify affected "X"` / `graphify query "impact of changing X"`

### Decision Tree — always start here

| Question pattern | MCP tool | CLI fallback |
|---|---|---|
| "Where is X?" / "Find symbol X" | `mcp__graphify__gx_find(term="X")` | `graphify query "X"` |
| "What calls X?" / "Who uses X?" | `mcp__graphify__gx_callers(symbol="X")` | `graphify path "X" "caller"` |
| "What does X depend on?" | `mcp__graphify__gx_callees(symbol="X")` | `graphify explain "X"` |
| "How does X reach Y?" | `mcp__graphify__gx_trace(src="A", tgt="B")` | `graphify path "A" "B"` |
| "What files relate to X?" | `mcp__graphify__gx_file_neighbors(file="X")` | `graphify query "files near X"` |
| "Impact of changing X?" | `mcp__graphify__gx_impact(target="X")` | `graphify affected "X"` |
| "What tests cover X?" | `mcp__graphify__gx_tests_for(target="X")` | `graphify query "tests for X"` |
| "Find files about <concept>" | `mcp__graphify__gx_rank_files(question="concept")` | `graphify query "concept"` |
| "What does file X import/export?" | `mcp__graphify__gx_imports_exports(file="X")` | N/A |
| "Explain X / give context" | `mcp__graphify__query_graph(question="X")` | `graphify explain "X"` |

### Full MCP Tools Reference
All MCP tools require `repository_id="devcloner/merged-agentic-swarm"` or `repository_id="4e3cec9f-6d8c-4c83-bd9a-581243bce913"`.

| MCP Tool | Purpose | Key Parameters |
|----------|---------|---------------|
| `query_graph` | Semantic retrieval with materialized bodies | `repository_id`, `question`, `budget` |
| `gx_find` | Find symbols by label substring | `repository_id`, `term`, `code_only` |
| `gx_find_seeds` | Scored seed nodes from NL question | `repository_id`, `question` |
| `gx_node` | Symbol body + direct neighborhood | `repository_id`, `symbol` |
| `gx_callers` | Exact directed callers of a symbol | `repository_id`, `symbol`, `strict_calls` |
| `gx_callees` | Exact directed callees of a symbol | `repository_id`, `symbol`, `strict_calls` |
| `gx_trace` | Resolved call paths (src -> tgt) | `repository_id`, `src`, `tgt`, `k_paths` |
| `gx_impact` | Change-impact fanout (blast radius) | `repository_id`, `target`, `max_seeds` |
| `gx_tests_for` | Tests linked to a symbol or file | `repository_id`, `target` |
| `gx_rank_files` | Rank source files for a NL question | `repository_id`, `question` |

### Rules
- **Always query graphify first** before grepping or reading raw files.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
- Use `graphify-out/wiki/index.md` for broad navigation if it exists.
- Read `graphify-out/GRAPH_REPORT.md` only for broad architecture review or when query/path/explain do not surface enough context.
- Global graph is at `~/.graphify/global-graph.json` — use `graphify global list` to see all registered repos.
