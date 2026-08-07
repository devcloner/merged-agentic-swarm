"""
Merged Agentic Swarm — CLI Entry Point
Provides run, status, promote, config, providers, report, and swarm subcommands.
"""

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")
logger = logging.getLogger("agentic_cli")

# Resolve repo root relative to this file (tools/ → merged_agentic_swarm/ → src/ → repo_root)
_REPO_ROOT = Path(__file__).resolve().parents[3]


def cmd_run(args):
    """Run the full orchestrator workflow."""
    from merged_agentic_swarm.tools.agentic_orchestrator import MultiLayeredAgenticOrchestrator

    prd_path = args.prd or str(_REPO_ROOT / ".taskmaster" / "docs" / "prd_agentic_codebase_optimization.md")
    if not os.path.exists(prd_path):
        print(f"ERROR: PRD file not found at {prd_path}")
        sys.exit(1)

    profile_name = getattr(args, "profile", None)
    run_kwargs = {}
    if profile_name:
        from merged_agentic_swarm.services import resolve_model_alias_for_profile, resolve_profile

        try:
            profile = resolve_profile(profile_name)
        except (KeyError, ValueError) as e:
            print(f"ERROR: {e}")
            sys.exit(1)
        ramp_sequence = profile.get("waves", []) or None  # empty waves -> default ramp
        default_model = resolve_model_alias_for_profile(profile_name)
        run_kwargs = {
            "ramp_sequence": ramp_sequence,
            "default_model": default_model,
            "gates": profile.get("gates"),
        }
        print(f"Using swarm profile: {profile_name}")
        print(f"  Wave ramp:     {ramp_sequence or '[4, 8, 16, 24, 40] (default)'}")
        print(f"  Model alias:   {default_model}")
        print(f"  Gates:         {profile.get('gates', True)}")
        print()

    try:
        with open(prd_path) as f:
            prd = f.read()

        orch = MultiLayeredAgenticOrchestrator(prd_title=args.title or "Merged Agentic Swarm OS")
        result = orch.run_full_agentic_workflow(prd, **run_kwargs)

        print()
        print("=" * 60)
        print("ORCHESTRATOR RESULT")
        print("=" * 60)
        print(f"  Status:          {result.get('status', '?')}")
        print(f"  Waves completed: {result.get('waves_completed', '?')}")
        print(f"  Epics completed: {result.get('epics_completed', '?')}")
        print(f"  Success markers: {result.get('total_success_markers', '?')}")
        print(f"  Chain entries:   {result.get('chain_registry_entries', '?')}")
        cp = result.get("cold_path", {})
        if cp:
            print(
                f"  Cold-path:       {cp.get('total_knowledge_records', 0)} knowledge, "
                f"{cp.get('total_durable_agents', 0)} agents promoted"
            )
        print()

        # Auto-save a run report after a successful orchestrator run
        if result.get("status") in ("success", "completed"):
            from merged_agentic_swarm.services import report_service

            try:
                saved = report_service.save_run_report(_REPO_ROOT)
            except Exception as e:
                logger.warning(f"Auto-save run report failed: {e}")
            else:
                print(f"  Report:          {saved['md_path']}")
                print(f"  Report JSON:     {saved['json_path']}")
                print()

        if args.verbose:
            print("Full result:")
            print(json.dumps(result, indent=2, default=str))
            print()
        return result
    except Exception as e:
        logger.exception("Orchestrator workflow failed")
        print(f"ERROR: Workflow failed: {e}")
        sys.exit(1)


def _progress_ledger_path() -> str:
    """Resolve the live progress ledger path (default source for ``cmd_status``)."""
    from merged_agentic_swarm.services.progress_ledger_service import default_progress_ledger

    return default_progress_ledger.ledger_file


def _render_ledger_status(progress: dict) -> None:
    """Render a live progress-ledger snapshot (logs + success markers + task-master snapshot)."""
    logs = progress.get("logs", [])
    markers = progress.get("success_markers", [])
    snapshot = progress.get("task_master_snapshot", {})
    status_counts: dict[str, int] = {}
    for log in logs:
        st = log.get("status", "unknown")
        status_counts[st] = status_counts.get(st, 0) + 1
    completed = status_counts.get("completed", 0)
    total_logged = len(logs)
    pct = int(completed / total_logged * 100) if total_logged else 0

    print(f"  Ledger:            {total_logged} log entries, {len(markers)} success markers")
    print(
        f"  Log status:        completed={completed}, "
        f"failed={status_counts.get('failed', 0)}, other={total_logged - completed - status_counts.get('failed', 0)}"
    )
    waves = sorted({log.get("wave_id") for log in logs if log.get("wave_id") is not None})
    print(f"  Waves covered:     {', '.join(str(w) for w in waves) or 'none'}")
    if snapshot:
        title = snapshot.get("title") or ""
        if title:
            print(f"  PRD:               {title}")
        epics = snapshot.get("epics")
        if isinstance(epics, list):
            done = sum(
                1 for e in epics if isinstance(e, dict) and str(e.get("status", "")).lower() in ("completed", "done")
            )
            print(f"  Epics:             {done}/{len(epics)} completed")
    print(f"  Completion:        ~{pct}% of logged actions completed")
    if logs:
        print("  Latest activity:")
        for log in logs[-5:]:
            print(
                f"    • [{log.get('entry_id', '?')}] wave {log.get('wave_id', '?')} "
                f"{log.get('action', '?')} on {log.get('task_id', '?')} — {log.get('status', '?')}"
            )


def _render_legacy_snapshot(progress: dict) -> None:
    """Render an older progress.json snapshot (kept so ``--progress`` still works on them)."""
    print(f"  Overall completion: {progress.get('overall_completion_pct', '?')}%")
    for phase, status in progress.get("phase_status", {}).items():
        print(
            f"  {phase}: {status.get('completion_pct', '?')}% "
            f"[{status.get('color', '?')}] — {status.get('status', '?')}"
        )
    print(f"  Blockers: {len(progress.get('blockers', []))}")
    for i, b in enumerate(progress.get("blockers", []), 1):
        print(f"    {i}. {b[:110]}...")
    milestones = progress.get("milestone_history", [])
    print(f"  Milestones ({len(milestones)}):")
    for m in milestones:
        print(f"    • {m.get('milestone', '?')} — {m.get('status', '?')}")


def cmd_status(args):
    """Show current system status from the live progress ledger."""
    reg_dir = _REPO_ROOT / "docs" / "agentic" / "registry"
    progress_path = args.progress or _progress_ledger_path()
    if os.path.exists(progress_path):
        try:
            with open(progress_path) as f:
                progress = json.load(f)
            print("=" * 60)
            print("SYSTEM STATUS")
            print("=" * 60)
            if isinstance(progress, dict) and ("logs" in progress or "success_markers" in progress):
                _render_ledger_status(progress)
            else:
                _render_legacy_snapshot(progress)
        except Exception as e:
            print(f"ERROR reading progress ledger: {e}")
    else:
        print("No progress ledger found. Run the orchestrator first.")

    for reg in ["knowledge.jsonl", "agents.jsonl", "chain.jsonl"]:
        path = reg_dir / reg
        if path.exists():
            try:
                with open(path) as f:
                    count = sum(1 for l in f if l.strip())
                print(f"  {reg}: {count} entries")
            except Exception as e:
                print(f"  {reg}: ERROR ({e})")

    chain_path = _REPO_ROOT / ".taskmaster" / "tasks" / "spawn_chain_registry.json"
    if chain_path.exists():
        try:
            with open(chain_path) as f:
                chain = json.load(f)
            print(f"  spawn_chain_registry: {len(chain)} entries")
        except Exception as e:
            print(f"  spawn_chain_registry: ERROR ({e})")
    print()


def cmd_promote(args):
    """Force cold-path promotion without running full orchestrator."""
    from merged_agentic_swarm.tools.agentic_orchestrator import MultiLayeredAgenticOrchestrator
    from merged_agentic_swarm.tools.knowledge_cache import default_knowledge_cache

    reg_dir = _REPO_ROOT / "docs" / "agentic" / "registry"
    try:
        orch = MultiLayeredAgenticOrchestrator()
        result = orch._promote_cold_path(phase_label="manual_cli")
        print(f"Promoted: {result.get('promoted_knowledge', 0)} knowledge, {result.get('promoted_agents', 0)} agents")
        for reg in ["knowledge.jsonl", "agents.jsonl", "chain.jsonl"]:
            path = reg_dir / reg
            if path.exists():
                with open(path) as f:
                    count = sum(1 for l in f if l.strip())
                print(f"  {reg}: {count} entries")
        print(f"  hot cache: {len(default_knowledge_cache.learnings)} learnings")
    except Exception as e:
        logger.exception("Promotion failed")
        print(f"ERROR: Promotion failed: {e}")
        sys.exit(1)


def cmd_config(args):
    """Show configuration state."""
    print("=" * 60)
    print("CONFIGURATION STATE")
    print("=" * 60)
    from merged_agentic_swarm.providers.key_pool import default_key_pool

    summary = default_key_pool.get_summary()
    print(f"Key Pool ({len(summary)} providers):")
    for provider, info in summary.items():
        cooldown = info.get("next_cooldown_until")
        cooldown_str = time.strftime("%H:%M:%S", time.localtime(cooldown)) if cooldown else "-"
        print(
            f"  {provider}: {info.get('active_keys', '?')}/{info.get('total_keys', '?')} active, "
            f"{info.get('exhausted_keys', 0)} exhausted, next cooldown {cooldown_str}, "
            f"avg latency {info.get('avg_latency_ms', 0)}ms, {info.get('total_requests', 0)} requests"
        )

    from merged_agentic_swarm.providers.multi_provider_fabric import MODEL_FABRIC_ROUTES

    for alias, routes in MODEL_FABRIC_ROUTES.items():
        print(f"Route: {alias}")
        for r in routes:
            print(f"  → {r['provider']:15s} {r['model']}")

    from merged_agentic_swarm.models.agent_models import WorkerPoolConfig

    cfg = WorkerPoolConfig()
    print(f"Swarm: {cfg.max_total_workers} max workers, roles={list(cfg.role_allocations.keys())}")


def cmd_providers(args):
    """Show a provider + proxy inventory: key pools, fabric routes, registry backends."""
    from merged_agentic_swarm.providers.key_pool import default_key_pool
    from merged_agentic_swarm.providers.multi_provider_fabric import MODEL_FABRIC_ROUTES

    print("=" * 60)
    print("PROVIDER & PROXY INVENTORY")
    print("=" * 60)

    print("\nKey Pools (key_id -> active/total):")
    summary = default_key_pool.get_summary()
    if summary:
        for provider, info in summary.items():
            key_names = ", ".join(k.key_id for k in default_key_pool.keys_by_provider.get(provider, []))
            cooldown = info.get("next_cooldown_until")
            cooldown_str = time.strftime("%H:%M:%S", time.localtime(cooldown)) if cooldown else "-"
            print(
                f"  {provider:18s} {info.get('active_keys', '?')!s:>3}/{info.get('total_keys', '?')!s:<3} active"
                f"  {info.get('exhausted_keys', 0)!s:>3} exhausted"
                f"  next-cooldown={cooldown_str}"
                f"  avg={info.get('avg_latency_ms', 0)}ms"
                f"  keys=[{key_names}]"
            )
    else:
        print("  (no key pools loaded)")

    print("\nFabric Routes (MODEL_FABRIC_ROUTES):")
    for alias, routes in MODEL_FABRIC_ROUTES.items():
        print(f"  {alias}:")
        for route in routes:
            print(f"    -> {route['provider']:16s} {route['model']}")

    reg_path = _REPO_ROOT / "docs" / "agentic" / "providers" / "PROVIDER_REGISTRY.json"
    print("\nRegistry Backends (PROVIDER_REGISTRY.json):")
    if reg_path.exists():
        try:
            with open(reg_path) as f:
                registry = json.load(f)
            backends = registry.get("backends", {})
            if backends:
                for name, backend in backends.items():
                    print(
                        f"  {name:18s} {backend.get('status', '?')!s:12s} "
                        f"auth={backend.get('auth_env', '?')!s:45s} {backend.get('base_url', '?')}"
                    )
            else:
                print("  (no backends registered)")
        except Exception as e:
            print(f"  ERROR reading provider registry: {e}")
    else:
        print(f"  (provider registry not found at {reg_path})")
    print()


def cmd_report(args):
    """Generate and persist a run report, rendering a readable timeline."""
    from merged_agentic_swarm.services.report_service import render_report_md, save_run_report

    reports_dir = Path(args.out) if getattr(args, "out", None) else None
    try:
        saved = save_run_report(
            _REPO_ROOT,
            ledger_file=getattr(args, "ledger", None) or None,
            reports_dir=reports_dir,
        )
    except Exception as e:
        logger.exception("Report generation failed")
        print(f"ERROR: Report generation failed: {e}")
        sys.exit(1)

    print("=" * 60)
    print("RUN REPORT")
    print("=" * 60)
    print(render_report_md(saved["report"]).strip())
    print(f"JSON report:  {saved['json_path']}")
    print(f"Markdown:     {saved['md_path']}")
    print()
    return saved


def cmd_swarm(args):
    """List named swarm profiles or resolve one into a runnable orchestrator plan."""
    from merged_agentic_swarm.services import (
        list_profiles,
        resolve_model_alias_for_profile,
        resolve_profile,
    )

    if getattr(args, "list_profiles", False):
        print("=" * 60)
        print("SWARM PROFILES")
        print("=" * 60)
        for entry in list_profiles():
            alias = resolve_model_alias_for_profile(entry["name"])
            print(f"  {entry['name']:10s} {entry['description']}  (model: {alias})")
        print()
        return None

    name = getattr(args, "profile", None)
    if not name:
        print("ERROR: specify --profile <name> (or use --list to see available profiles)")
        sys.exit(1)
    try:
        profile = resolve_profile(name)
    except (KeyError, ValueError) as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    alias = resolve_model_alias_for_profile(name)
    waves = profile.get("waves", [])
    print("=" * 60)
    print(f"SWARM PROFILE: {name}")
    print("=" * 60)
    print(f"  Description:   {profile.get('description', '?')}")
    print(f"  Wave ramp:     {waves}")
    print(f"  Default tier:  {profile.get('default_tier', '?')}")
    print(f"  Model alias:   {alias}")
    print(f"  Gates:         {bool(profile.get('gates', True))}")
    print(f"  Worker roles:  {', '.join(profile.get('worker_roles', []))}")
    if waves:
        print(
            f"  Planned run:   agentic-cli run (MultiLayeredAgenticOrchestrator, "
            f"waves={len(waves)}, peak={max(waves)} workers)"
        )
    else:
        print("  Planned run:   cold-path maintenance only — no worker waves (use `agentic-cli promote`)")
    print()
    return profile


def main():
    parser = argparse.ArgumentParser(
        description="Merged Agentic Swarm CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  agentic-cli run
  agentic-cli run --verbose
  agentic-cli status
  agentic-cli promote
  agentic-cli config
  agentic-cli providers
  agentic-cli report
  agentic-cli report --out /tmp/reports
  agentic-cli swarm --list
  agentic-cli swarm --profile build
        """,
    )
    sub = parser.add_subparsers(dest="command")
    p_run = sub.add_parser("run", help="Run full orchestrator workflow")
    p_run.add_argument(
        "--prd", help="Path to PRD file (default: .taskmaster/docs/prd_agentic_codebase_optimization.md)"
    )
    p_run.add_argument(
        "--profile",
        help="Named swarm profile (build/review/ultra/patch/learning): drives the wave ramp "
        "and model tier of the run instead of the default ramp",
    )
    p_run.add_argument("--title", default="Merged Agentic Swarm OS", help="PRD title")
    p_run.add_argument("--verbose", "-v", action="store_true", help="Print full result JSON")
    p_run.set_defaults(func=cmd_run)

    p_status = sub.add_parser("status", help="Show system status")
    p_status.add_argument("--progress", help="Path to progress.json")
    p_status.set_defaults(func=cmd_status)

    p_promote = sub.add_parser("promote", help="Force cold-path promotion")
    p_promote.set_defaults(func=cmd_promote)

    p_config = sub.add_parser("config", help="Show configuration state")
    p_config.set_defaults(func=cmd_config)

    p_providers = sub.add_parser("providers", help="Show provider & proxy inventory")
    p_providers.set_defaults(func=cmd_providers)

    p_report = sub.add_parser("report", help="Generate and persist a run report")
    p_report.add_argument("--ledger", help="Path to progress ledger JSON (default: live ledger)")
    p_report.add_argument("--out", help="Output directory for the report (default: <repo>/reports)")
    p_report.set_defaults(func=cmd_report)

    p_swarm = sub.add_parser("swarm", help="List or resolve named swarm profiles")
    p_swarm.add_argument("--list", dest="list_profiles", action="store_true", help="List all profiles")
    p_swarm.add_argument("--profile", help="Resolve a named swarm profile into an orchestrator plan")
    p_swarm.set_defaults(func=cmd_swarm)

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    args.func(args)


if __name__ == "__main__":
    main()
