"""
Merged Agentic Swarm — CLI Entry Point
Provides run, status, promote, and config subcommands.
"""
import os
import sys
import json
import time
import argparse
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")
logger = logging.getLogger("agentic_cli")


def cmd_run(args):
    """Run the full orchestrator workflow."""
    from tools.agentic_orchestrator import MultiLayeredAgenticOrchestrator

    prd_path = args.prd or ".taskmaster/docs/prd_agentic_codebase_optimization.md"
    if not os.path.exists(prd_path):
        print(f"ERROR: PRD file not found at {prd_path}")
        sys.exit(1)

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
        print(f"  Cold-path:       {cp.get('total_knowledge_records', 0)} knowledge, "
              f"{cp.get('total_durable_agents', 0)} agents promoted")
    print()

    if args.verbose:
        print("Full result:")
        print(json.dumps(result, indent=2, default=str))
        print()
    return result


def cmd_status(args):
    """Show current system status."""
    progress_path = args.progress or "docs/agentic/registry/progress.json"
    if os.path.exists(progress_path):
        with open(progress_path) as f:
            progress = json.load(f)
        print("=" * 60)
        print("SYSTEM STATUS")
        print("=" * 60)
        print(f"  Overall completion: {progress.get('overall_completion_pct', '?')}%")
        for phase, status in progress.get("phase_status", {}).items():
            print(f"  {phase}: {status.get('completion_pct', '?')}% "
                  f"[{status.get('color', '?')}] — {status.get('status', '?')}")
        print(f"  Blockers: {len(progress.get('blockers', []))}")
        for i, b in enumerate(progress.get("blockers", []), 1):
            print(f"    {i}. {b[:110]}...")
        milestones = progress.get("milestone_history", [])
        print(f"  Milestones ({len(milestones)}):")
        for m in milestones:
            print(f"    • {m.get('milestone', '?')} — {m.get('status', '?')}")
    else:
        print("No progress.json found. Run the orchestrator first.")

    for reg in ["knowledge.jsonl", "agents.jsonl", "chain.jsonl"]:
        path = f"docs/agentic/registry/{reg}"
        if os.path.exists(path):
            with open(path) as f:
                count = sum(1 for l in f if l.strip())
            print(f"  {reg}: {count} entries")

    chain_path = ".taskmaster/tasks/spawn_chain_registry.json"
    if os.path.exists(chain_path):
        with open(chain_path) as f:
            chain = json.load(f)
        print(f"  spawn_chain_registry: {len(chain)} entries")
    print()


def cmd_promote(args):
    """Force cold-path promotion without running full orchestrator."""
    from tools.knowledge_cache import default_knowledge_cache
    from tools.agentic_orchestrator import MultiLayeredAgenticOrchestrator

    orch = MultiLayeredAgenticOrchestrator()
    result = orch._promote_cold_path(phase_label="manual_cli")
    print(f"Promoted: {result.get('promoted_knowledge', 0)} knowledge, "
          f"{result.get('promoted_agents', 0)} agents")
    for reg in ["knowledge.jsonl", "agents.jsonl", "chain.jsonl"]:
        path = f"docs/agentic/registry/{reg}"
        if os.path.exists(path):
            with open(path) as f:
                count = sum(1 for l in f if l.strip())
            print(f"  {reg}: {count} entries")
    print(f"  hot cache: {len(default_knowledge_cache.learnings)} learnings")


def cmd_config(args):
    """Show configuration state."""
    print("=" * 60)
    print("CONFIGURATION STATE")
    print("=" * 60)
    from providers.key_pool import default_key_pool
    summary = default_key_pool.get_summary()
    print(f"Key Pool ({len(summary)} providers):")
    for provider, info in summary.items():
        print(f"  {provider}: {info.get('active_keys', '?')}/{info.get('total_keys', '?')} active, "
              f"{info.get('total_requests', 0)} requests")

    from providers.multi_provider_fabric import MODEL_FABRIC_ROUTES
    for alias, routes in MODEL_FABRIC_ROUTES.items():
        print(f"Route: {alias}")
        for r in routes:
            print(f"  → {r['provider']:15s} {r['model']}")

    from models.agent_models import WorkerPoolConfig
    cfg = WorkerPoolConfig()
    print(f"Swarm: {cfg.max_total_workers} max workers, roles={list(cfg.role_allocations.keys())}")


def main():
    parser = argparse.ArgumentParser(
        description="Merged Agentic Swarm CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python3 tools/agentic_cli.py run
  python3 tools/agentic_cli.py run --verbose
  python3 tools/agentic_cli.py status
  python3 tools/agentic_cli.py promote
  python3 tools/agentic_cli.py config
        """)
    sub = parser.add_subparsers(dest="command")
    p_run = sub.add_parser("run", help="Run full orchestrator workflow")
    p_run.add_argument("--prd", help="Path to PRD file (default: .taskmaster/docs/prd_agentic_codebase_optimization.md)")
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
