"""
Merged Agentic Swarm — CLI Entry Point
Provides run, status, promote, and config subcommands.
"""

import argparse
import json
import logging
import os
import sys
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

    try:
        with open(prd_path) as f:
            prd = f.read()

        orch = MultiLayeredAgenticOrchestrator(prd_title=args.title or "Merged Agentic Swarm OS")
        result = orch.run_full_agentic_workflow(prd)

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

        if args.verbose:
            print("Full result:")
            print(json.dumps(result, indent=2, default=str))
            print()
        return result
    except Exception as e:
        logger.exception("Orchestrator workflow failed")
        print(f"ERROR: Workflow failed: {e}")
        sys.exit(1)


def cmd_status(args):
    """Show current system status."""
    reg_dir = _REPO_ROOT / "docs" / "agentic" / "registry"
    progress_path = args.progress or str(reg_dir / "progress.json")
    if os.path.exists(progress_path):
        try:
            with open(progress_path) as f:
                progress = json.load(f)
            print("=" * 60)
            print("SYSTEM STATUS")
            print("=" * 60)
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
        except Exception as e:
            print(f"ERROR reading progress.json: {e}")
    else:
        print("No progress.json found. Run the orchestrator first.")

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
        print(
            f"  {provider}: {info.get('active_keys', '?')}/{info.get('total_keys', '?')} active, "
            f"{info.get('total_requests', 0)} requests"
        )

    from merged_agentic_swarm.providers.multi_provider_fabric import MODEL_FABRIC_ROUTES

    for alias, routes in MODEL_FABRIC_ROUTES.items():
        print(f"Route: {alias}")
        for r in routes:
            print(f"  → {r['provider']:15s} {r['model']}")

    from merged_agentic_swarm.models.agent_models import WorkerPoolConfig

    cfg = WorkerPoolConfig()
    print(f"Swarm: {cfg.max_total_workers} max workers, roles={list(cfg.role_allocations.keys())}")


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
        """,
    )
    sub = parser.add_subparsers(dest="command")
    p_run = sub.add_parser("run", help="Run full orchestrator workflow")
    p_run.add_argument(
        "--prd", help="Path to PRD file (default: .taskmaster/docs/prd_agentic_codebase_optimization.md)"
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

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    args.func(args)


if __name__ == "__main__":
    main()
