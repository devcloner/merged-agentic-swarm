#!/usr/bin/env python3
"""Modular all-in-one swarm run launcher.

Generates a fleet-scale ultraswarm task plan from the repo's own backlog
(GitLab issues, untested/under-tested modules, lint, module hygiene, docs)
and drives the ultraswarm runner through plan/preview/run/merge/post phases.

Usage:
  uv run scripts/swarm_run.py --phase plan --agents 100
  uv run scripts/swarm_run.py --phase preview
  uv run scripts/swarm_run.py --phase run
  uv run scripts/swarm_run.py --phase merge --run-id <id>
  uv run scripts/swarm_run.py --phase all --agents 100
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent
PLAN_FILE = REPO / ".ultraswarm-plan.json"
PACKAGE = REPO / "src" / "merged_agentic_swarm"
TESTS = REPO / "tests"
DEFAULT_PROJECT = "zev-oer/merged-agentic-swarm"  # moved from lunaclone (2026-08-09); glab POST 405 on old path
ULTRASWARM_HOME = Path(os.environ.get("ULTRASWARM_HOME", "~/projects/ultraswarm")).expanduser()

# Plan-schema task keys (runner rejects unknown keys).
_TASK_KEYS = (
    "id",
    "description",
    "files",
    "complexity_score",
    "risk",
    "dependencies",
    "prompt",
    "cli",
    "model_tier",
    "effort",
    "competition",
    "requirements",
    "contract",
)
_ID_OK = re.compile(r"^[A-Za-z0-9._-]+$")

# Modules that must never get a pytest/ruff task target (data, no code).
_LIVING_DOCS = [
    "README.md",
    "docs/swarm_project_prd.md",
    "docs/stack-analysis-2026-08-06.md",
    "docs/agentic/OPERATOR_RUNBOOK.md",
    "docs/agentic/RUNBOOK.md",
    "docs/agentic/AGENT_SPEC_CONTRACT.md",
    "docs/agentic/KNOWLEDGE_BOX_SCHEMA.md",
]


def _slug(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]", "-", name)


def _run(cmd: list[str], cwd: Path = REPO, timeout: int = 60) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)


def _runner(*args: str, timeout: int = 120) -> subprocess.CompletedProcess:
    return _run(["node", str(ULTRASWARM_HOME / "bin" / "ultraswarm.mjs"), *args], timeout=timeout)


def _issue_risk(issue: dict[str, Any]) -> str:
    text = f"{issue.get('labels', '')} {issue.get('title', '')}".lower()
    return "high" if "security" in text or "sec:" in text or "leak" in text else "routine"


def fetch_issues(project: str) -> list[dict[str, Any]]:
    glab = shutil.which("glab")
    if not glab:
        print("  ! glab not found — skipping GitLab issue tasks")
        return []
    res = _run([glab, "issue", "list", "-R", project, "--output", "json"])
    if res.returncode != 0:
        print(f"  ! glab issue list failed ({res.stderr.strip()[:120]}) — skipping GitLab issue tasks")
        return []
    try:
        return json.loads(res.stdout)
    except json.JSONDecodeError:
        print("  ! glab issue list returned non-JSON — skipping GitLab issue tasks")
        return []


def discover_modules() -> list[Path]:
    return sorted(p for p in PACKAGE.rglob("*.py") if p.name != "__init__.py" and "__pycache__" not in p.parts)


def make_todo_task(entry: dict[str, Any]) -> dict[str, Any]:
    title = entry.get("title", "untitled task")
    files = entry.get("files") or ["src/merged_agentic_swarm"]
    risk = entry.get("risk") if entry.get("risk") in ("routine", "high") else "routine"
    return {
        "id": f"todo-{_slug(title)[:40]}",
        "description": title,
        "files": files,
        "complexity_score": int(entry.get("complexity", 2)),
        "risk": risk,
        "dependencies": [],
        "prompt": (
            f"{title}\n\n{entry.get('description', '')}\n\nSuggested approach:\n"
            f"{entry.get('suggested_approach', '')}\n\nImplement this change, add or update tests, and "
            "ensure `uv run pytest -q` passes. Stay scoped to the files listed."
        ),
        "contract": {
            "commands": ["uv run pytest -q"],
            "assertions": [f"{title} implemented"],
            "allowed_paths": files,
        },
    }


def make_issue_task(issue: dict[str, Any]) -> dict[str, Any]:
    iid = issue.get("iid", "0")
    title = issue.get("title", "untitled")
    desc = (issue.get("description") or "").strip()[:2000] or "No description provided."
    risk = _issue_risk(issue)
    return {
        "id": f"issue-{iid}",
        "description": f"Issue #{iid}: {title}",
        "files": ["src/merged_agentic_swarm", "tests"],
        "complexity_score": 3 if risk == "high" else 2,
        "risk": risk,
        "dependencies": [],
        "prompt": (
            f"Work in the merged-agentic-swarm repository. Resolve GitLab issue #{iid}: {title}.\n\n"
            f"Issue description:\n{desc}\n\n"
            "Investigate, implement the fix or feature, add or update tests, and ensure the module's "
            "tests and `uv run pytest -q` pass. Stay scoped to this issue. Report exactly what you changed."
        ),
    }


def make_test_task(module: Path) -> dict[str, Any]:
    rel = module.relative_to(REPO)
    name = module.stem
    test_file = TESTS / f"test_{name}.py"
    test_rel = test_file.relative_to(REPO)
    return {
        "id": f"tests-{_slug(name)}",
        "description": f"Add pytest coverage for src/merged_agentic_swarm/{module.relative_to(PACKAGE)}",
        "files": [str(rel), str(test_rel)],
        "complexity_score": 2,
        "risk": "routine",
        "dependencies": [],
        "prompt": (
            f"Write {test_rel} for the {module} module in this repo. Read the module first to learn its "
            "exact public API. Follow the style of tests/test_knowledge_cache.py (plain pytest, no unittest "
            "classes). Cover the main paths and edge cases. The tests must pass with:\n"
            f"  uv run pytest {test_rel} -v"
        ),
        "contract": {
            "commands": [f"uv run pytest {test_rel} -v"],
            "assertions": [f"{test_rel} exists", f"uv run pytest {test_rel} -v passes"],
            "allowed_paths": [str(test_rel)],
        },
    }


def make_strengthen_task(test_file: Path) -> dict[str, Any]:
    test_rel = test_file.relative_to(REPO)
    name = test_file.stem.removeprefix("test_")
    return {
        "id": f"tests-{_slug(name)}-edge",
        "description": f"Strengthen edge-case coverage in {test_rel}",
        "files": [str(test_rel)],
        "complexity_score": 1,
        "risk": "routine",
        "dependencies": [],
        "prompt": (
            f"Strengthen the test file {test_rel}. Add edge cases the current suite misses: empty inputs, "
            "single-element collections, boundary values, error paths, concurrency bookkeeping. Keep the "
            "existing style. The suite must pass with:\n"
            f"  uv run pytest {test_rel} -v"
        ),
        "contract": {
            "commands": [f"uv run pytest {test_rel} -v"],
            "assertions": [f"new edge-case tests added to {test_rel}", f"uv run pytest {test_rel} -v passes"],
            "allowed_paths": [str(test_rel)],
        },
    }


def make_lint_task(module: Path) -> dict[str, Any]:
    rel = module.relative_to(REPO)
    return {
        "id": f"lint-{_slug(module.stem)}",
        "description": f"Ruff-clean {rel}",
        "files": [str(rel)],
        "complexity_score": 1,
        "risk": "routine",
        "dependencies": [],
        "prompt": (
            f"Run `uv run ruff check {rel}` and fix every violation. Do not add `# type: ignore`. Do not "
            "re-parenthesize except blocks (ruff targets py314, PEP 758 strips them). Do not change "
            "behavior. Then run `uv run ruff check {rel}` again to confirm it passes."
        ),
        "contract": {
            "commands": [f"uv run ruff check {rel}"],
            "assertions": [f"uv run ruff check {rel} passes"],
            "allowed_paths": [str(rel)],
        },
    }


def make_hygiene_task(module: Path) -> dict[str, Any]:
    rel = module.relative_to(REPO)
    import_path = "merged_agentic_swarm." + ".".join(module.relative_to(PACKAGE).parent.parts + (module.stem,))
    return {
        "id": f"hygiene-{_slug(module.stem)}",
        "description": f"Docstring + type-hint hygiene for {rel}",
        "files": [str(rel)],
        "complexity_score": 1,
        "risk": "routine",
        "dependencies": [],
        "prompt": (
            f"Audit {rel}: ensure it has a one-line module docstring, public functions/classes have concise "
            "docstrings, and type hints are accurate (no `# type: ignore`). Do not change behavior. Verify "
            f"it still imports with: `uv run python -c 'import {import_path}'`"
        ),
    }


def make_docs_task(doc: str) -> dict[str, Any]:
    return {
        "id": f"docs-{_slug(Path(doc).stem)}",
        "description": f"Refresh {doc} against the current codebase",
        "files": [doc],
        "complexity_score": 1,
        "risk": "routine",
        "dependencies": [],
        "prompt": (
            f"Review {doc} in this repo. Fix inaccuracies against the current source tree (module names, "
            "commands, config keys, behaviors). Keep the existing style and structure. Do not invent "
            "features. `uv run pytest -q` must still pass."
        ),
        "contract": {
            "commands": ["uv run pytest -q"],
            "assertions": [f"{doc} updated to match the codebase"],
            "allowed_paths": [doc],
        },
    }


def build_tasks(
    target: str, project: str, agents: int, feature_desc: str | None
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    breakdown: dict[str, int] = {}
    tasks: list[dict[str, Any]] = []

    if target in ("self", "issues"):
        issues = fetch_issues(project)
        issue_tasks = [make_issue_task(i) for i in issues]
        tasks.extend(issue_tasks)
        breakdown["issues"] = len(issue_tasks)

    modules = discover_modules()
    tested = {p for p in modules if (TESTS / f"test_{p.stem}.py").exists()}
    untested = [p for p in modules if p not in tested]

    if target in ("self", "tests"):
        new = [make_test_task(p) for p in untested]
        tasks.extend(new)
        breakdown["test_new"] = len(new)
        strong = [make_strengthen_task(TESTS / f"test_{p.stem}.py") for p in sorted(tested)]
        tasks.extend(strong)
        breakdown["test_strengthen"] = len(strong)

    if target in ("self", "lint"):
        lint = [make_lint_task(p) for p in modules]
        tasks.extend(lint)
        breakdown["lint"] = len(lint)

    if target in ("self", "docs"):
        doc_tasks = [make_docs_task(d) for d in _LIVING_DOCS if (REPO / d).exists()]
        tasks.extend(doc_tasks)
        breakdown["docs"] = len(doc_tasks)

    if target.startswith("todo:"):
        todo_path = Path(target.split(":", 1)[1]).expanduser()
        if not todo_path.exists():
            print(f"  ! todo file not found: {todo_path}")
            return tasks, breakdown
        entries = json.loads(todo_path.read_text())
        todo_tasks = [make_todo_task(e) for e in entries]
        tasks.extend(todo_tasks)
        breakdown["todo"] = len(todo_tasks)

    if target.startswith("feature"):
        if feature_desc:
            desc = feature_desc
        elif ":" in target:
            desc = target.split(":", 1)[1]
        else:
            desc = "implement the requested feature"
        tasks.append(
            {
                "id": "feature-main",
                "description": f"Feature: {desc[:120]}",
                "files": ["src/merged_agentic_swarm", "tests"],
                "complexity_score": 5,
                "risk": "high",
                "dependencies": [],
                "prompt": f"Implement the requested feature in this repo: {desc}. Add tests and update docs. `uv run pytest -q` must pass.",
            }
        )
        breakdown["feature"] = 1

    # Pad to the requested agent count with low-risk per-module subtasks (logged, no silent inflation).
    padded = 0
    while len(tasks) < agents:
        for p in modules:
            if len(tasks) >= agents:
                break
            tasks.append(make_hygiene_task(p))
            padded += 1
        if padded and padded % len(modules) == 0 and len(tasks) < agents:
            break  # never duplicate infinitely; report the shortfall honestly
    breakdown["padded"] = padded

    return tasks, breakdown


def write_plan(tasks: list[dict[str, Any]]) -> Path:
    PLAN_FILE.write_text(json.dumps({"tasks": tasks}, indent=2))
    return PLAN_FILE


def validate_tasks(tasks: list[dict[str, Any]]) -> list[str]:
    problems = []
    for t in tasks:
        for key in _TASK_KEYS:
            if key not in t and key not in ("cli", "model_tier", "effort", "competition", "requirements", "contract"):
                problems.append(f"{t.get('id')}: missing required key {key}")
        if not _ID_OK.match(t.get("id", "")) or t.get("id", "").startswith("-"):
            problems.append(f"invalid id {t.get('id')!r}")
        if t.get("risk") not in ("routine", "high"):
            problems.append(f"{t.get('id')}: risk must be routine|high")
        extra = set(t) - set(_TASK_KEYS)
        if extra:
            problems.append(f"{t.get('id')}: unknown keys {sorted(extra)}")
    return problems


def latest_run_id() -> str | None:
    res = _runner("status", "--json")
    if res.returncode != 0:
        return None
    try:
        data = json.loads(res.stdout)
    except json.JSONDecodeError:
        return None
    runs = data if isinstance(data, list) else data.get("runs", data.get("active", []))
    if isinstance(runs, dict):
        runs = list(runs.values())
    if not runs:
        return None
    run = max(runs, key=lambda r: r.get("startedAt", r.get("createdAt", 0)))
    return run.get("id") or run.get("runId")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--phase", choices=["plan", "preview", "run", "merge", "post", "all"], default="plan")
    ap.add_argument("--agents", type=int, default=100, help="target total task count (default 100)")
    ap.add_argument("--target", default="self", help="self | issues | tests | lint | docs | feature:<desc>")
    ap.add_argument("--project", default=DEFAULT_PROJECT, help="GitLab project for issue tasks")
    ap.add_argument("--feature-desc", help="description when --target feature")
    ap.add_argument("--run-id", help="run id for merge/post phases")
    ap.add_argument("--dry-run", action="store_true", help="generate the plan but do not write it")
    args = ap.parse_args(argv)

    if args.phase in ("plan", "run", "all"):
        tasks, breakdown = build_tasks(args.target, args.project, args.agents, args.feature_desc)
        problems = validate_tasks(tasks)
        if problems:
            for p in problems[:10]:
                print(f"  ! plan problem: {p}")
            return 1
        print(f"Plan: {len(tasks)} tasks  sources={breakdown}")
        if not args.dry_run:
            path = write_plan(tasks)
            print(f"Wrote {path}")

    if args.phase == "plan":
        return 0

    if args.phase in ("preview", "run"):
        if not PLAN_FILE.exists():
            print("No plan — run --phase plan first")
            return 1
        cmd = ["run", "--plan-file", str(PLAN_FILE)]
        if args.phase == "run":
            cmd.append("--approve-plan")
        res = _runner(*cmd, timeout=600)
        print(res.stdout)
        if res.stderr:
            print(res.stderr, file=sys.stderr)
        return 0 if res.returncode == 0 else res.returncode

    if args.phase == "merge":
        run_id = args.run_id or latest_run_id()
        if not run_id:
            print("No run id — pass --run-id")
            return 1
        res = _runner("merge", run_id, "--approve", timeout=600)
        print(res.stdout)
        if res.stderr:
            print(res.stderr, file=sys.stderr)
        return 0 if res.returncode == 0 else res.returncode

    if args.phase == "post":
        agent = shutil.which("commit-agent")
        if not agent:
            print("commit-agent not installed — nothing to run for --phase post")
            return 0
        res = _run([agent, str(REPO)], timeout=600)
        print(res.stdout)
        if res.stderr:
            print(res.stderr, file=sys.stderr)
        return 0 if res.returncode == 0 else res.returncode

    if args.phase == "all":
        run_id = latest_run_id()
        if run_id:
            res = _runner("merge", run_id, "--approve", timeout=600)
            print(res.stdout)
        agent = shutil.which("commit-agent")
        if agent:
            res = _run([agent, str(REPO)], timeout=600)
            print(res.stdout)
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
