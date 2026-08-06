"""
Run Report Service
Builds and persists orchestration run reports (JSON + Markdown) from the live
progress ledger and the cold-path registries.

Sources:
  - progress ledger    (default_progress_ledger.ledger_file, ~/.taskmaster/tasks/progress_ledger.json)
  - chain registry     (docs/agentic/registry/chain.jsonl)
  - knowledge registry (docs/agentic/registry/knowledge.jsonl)
"""

import json
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

_STAMP_FORMAT = "%Y%m%dT%H%M%SZ"


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    entries: list[dict[str, Any]] = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def _build_waves(logs: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Group ledger logs by wave, tallying statuses, tokens, and distinct models."""
    waves: dict[str, dict[str, Any]] = {}
    for log in logs:
        wave_id = log.get("wave_id")
        if wave_id is None:
            continue
        key = str(wave_id)
        wave = waves.setdefault(key, {"status_counts": {}, "tokens_used": 0, "models": []})
        status = log.get("status") or "unknown"
        wave["status_counts"][status] = wave["status_counts"].get(status, 0) + 1
        wave["tokens_used"] += int(log.get("tokens_used") or 0)
        model = log.get("model")
        if model and model not in wave["models"]:
            wave["models"].append(model)
    return dict(sorted(waves.items(), key=lambda kv: int(kv[0])))


def _build_epics(logs: list[dict[str, Any]], snapshot: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Per-epic status from the ledger snapshot plus log-derived status tallies."""
    epics: dict[str, dict[str, Any]] = {}
    for epic in snapshot.get("epics", []) or []:
        if not isinstance(epic, dict):
            continue
        eid = str(epic.get("id") or "?")
        epics[eid] = {
            "title": epic.get("title", ""),
            "wave_id": epic.get("wave_id"),
            "status": epic.get("status", "unknown"),
        }
    for log in logs:
        task_id = log.get("task_id")
        if not task_id:
            continue
        epic = epics.setdefault(str(task_id), {"title": "", "wave_id": log.get("wave_id"), "status": "unknown"})
        counts = epic.setdefault("status_counts", {})
        status = log.get("status") or "unknown"
        counts[status] = counts.get(status, 0) + 1
    return epics


def _build_gates(logs: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Derive per-wave gate pass/fail from ledger log statuses.

    The orchestrator evaluates gates in-memory (not persisted to the ledger),
    so a wave is reported as passed only when every logged action completed.
    """
    gates: dict[str, dict[str, Any]] = {}
    for wave_id, wave in _build_waves(logs).items():
        counts = wave["status_counts"]
        blocking = [s for s in counts if s in ("failed", "escalated", "error")]
        gates[wave_id] = {"passed": not blocking, "status_counts": counts}
    return gates


def _build_timeline(logs: list[dict[str, Any]], chain: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Chronological event list (ledger steps + chain spawns) with model per step."""
    events: list[dict[str, Any]] = []
    for log in logs:
        events.append(
            {
                "timestamp": log.get("timestamp", 0),
                "kind": "step",
                "entry_id": log.get("entry_id"),
                "wave_id": log.get("wave_id"),
                "task_id": log.get("task_id"),
                "action": log.get("action"),
                "status": log.get("status"),
                "model": log.get("model"),
                "tokens_used": int(log.get("tokens_used") or 0),
            }
        )
    for entry in chain:
        events.append(
            {
                "timestamp": entry.get("timestamp", 0),
                "kind": "chain",
                "entry_id": entry.get("entry_id"),
                "wave_id": None,
                "task_id": entry.get("spawned_agent_id"),
                "action": f"chain_spawn:{entry.get('agent_type') or '?'}",
                "status": "spawned",
                "model": None,
                "tokens_used": 0,
            }
        )
    events.sort(key=lambda e: e["timestamp"])
    return events


def build_run_report(repo_root: Path, ledger_file: str | None = None) -> dict[str, Any]:
    """Build a run-report dict from the live progress ledger + cold-path registries."""
    from merged_agentic_swarm.services.progress_ledger_service import default_progress_ledger

    ledger_path = Path(ledger_file or default_progress_ledger.ledger_file)
    ledger = _read_json(ledger_path)
    logs = ledger.get("logs", [])
    markers = ledger.get("success_markers", [])
    snapshot = ledger.get("task_master_snapshot", {}) or {}
    if not isinstance(logs, list):
        logs = []
    if not isinstance(markers, list):
        markers = []

    reg_dir = repo_root / "docs" / "agentic" / "registry"
    chain = _read_jsonl(reg_dir / "chain.jsonl")
    knowledge = _read_jsonl(reg_dir / "knowledge.jsonl")

    return {
        "generated_at": time.time(),
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "ledger_path": str(ledger_path),
        "prd_title": snapshot.get("title"),
        "total_tokens_used": sum(int(l.get("tokens_used") or 0) for l in logs),
        "success_markers": len(markers),
        "chain_registry_entries": len(chain),
        "knowledge_registry_entries": len(knowledge),
        "waves": _build_waves(logs),
        "epics": _build_epics(logs, snapshot),
        "gates": _build_gates(logs),
        "timeline": _build_timeline(logs, chain),
    }


def _format_ts(epoch: float) -> str:
    if not epoch:
        return "-"
    try:
        return datetime.fromtimestamp(epoch, tz=UTC).strftime("%Y-%m-%d %H:%M:%S")
    except ValueError, OSError:
        return str(epoch)


def render_report_md(report: dict[str, Any]) -> str:
    """Render a run-report dict as human-readable Markdown (with model timeline)."""
    lines: list[str] = []
    lines.append("# Run Report")
    lines.append("")
    lines.append(f"- Generated (UTC): `{report.get('generated_at_utc')}`")
    lines.append(f"- Ledger: `{report.get('ledger_path')}`")
    lines.append(f"- PRD: {report.get('prd_title') or '(none)'}")
    lines.append(f"- Total tokens used: {report.get('total_tokens_used', 0)}")
    lines.append(f"- Success markers: {report.get('success_markers', 0)}")
    lines.append(f"- Chain registry entries: {report.get('chain_registry_entries', 0)}")
    lines.append(f"- Knowledge registry entries: {report.get('knowledge_registry_entries', 0)}")
    lines.append("")

    waves = report.get("waves", {})
    lines.append("## Per-Wave Status")
    lines.append("")
    if waves:
        lines.append("| Wave | status counts | tokens | models |")
        lines.append("| --- | --- | --- | --- |")
        for wave_id, wave in waves.items():
            counts = ", ".join(f"{s}:{c}" for s, c in wave["status_counts"].items())
            models = ", ".join(wave["models"]) or "-"
            lines.append(f"| {wave_id} | {counts} | {wave['tokens_used']} | {models} |")
    else:
        lines.append("_No wave activity logged._")
    lines.append("")

    gates = report.get("gates", {})
    lines.append("## Gate Results (derived from ledger statuses)")
    lines.append("")
    if gates:
        lines.append("| Wave | passed | status counts |")
        lines.append("| --- | --- | --- |")
        for wave_id, gate in gates.items():
            counts = ", ".join(f"{s}:{c}" for s, c in gate["status_counts"].items())
            lines.append(f"| {wave_id} | {'PASS' if gate['passed'] else 'FAIL'} | {counts} |")
    else:
        lines.append("_No gate data available._")
    lines.append("")

    epics = report.get("epics", {})
    lines.append("## Per-Epic Status")
    lines.append("")
    if epics:
        lines.append("| Epic | wave | status |")
        lines.append("| --- | --- | --- |")
        for epic_id, epic in epics.items():
            lines.append(f"| {epic_id} | {epic.get('wave_id') or '-'} | {epic.get('status') or 'unknown'} |")
    else:
        lines.append("_No epic data available._")
    lines.append("")

    timeline = report.get("timeline", [])
    lines.append("## Timeline")
    lines.append("")
    if timeline:
        lines.append("| Time (UTC) | wave | action | status | model | tokens |")
        lines.append("| --- | --- | --- | --- | --- | --- |")
        for ev in timeline:
            model = ev.get("model") or "-"
            lines.append(
                f"| {_format_ts(ev.get('timestamp'))} | {ev.get('wave_id') or '-'} "
                f"| {ev.get('action') or '?'} | {ev.get('status') or '?'} | {model} | {ev.get('tokens_used', 0)} |"
            )
    else:
        lines.append("_No timeline events logged._")
    lines.append("")
    return "\n".join(lines)


def save_run_report(
    repo_root: Path,
    ledger_file: str | None = None,
    reports_dir: Path | None = None,
) -> dict[str, Any]:
    """Build a run report and persist it as both JSON and Markdown.

    Returns ``{"report": ..., "json_path": ..., "md_path": ...}``. The
    ``reports_dir`` defaults to ``<repo_root>/reports`` and is created if missing.
    """
    report = build_run_report(repo_root, ledger_file=ledger_file)
    out_dir = Path(reports_dir) if reports_dir else Path(repo_root) / "reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime(_STAMP_FORMAT)
    json_path = out_dir / f"{stamp}.json"
    md_path = out_dir / f"{stamp}.md"
    json_path.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    md_path.write_text(render_report_md(report), encoding="utf-8")
    return {"report": report, "json_path": json_path, "md_path": md_path}
