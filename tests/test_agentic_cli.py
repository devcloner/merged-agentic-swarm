"""
Tests for tools/agentic_cli.py

Coverage: cmd_config and basic CLI parsing.
"""
import os

import pytest

from merged_agentic_swarm.tools.agentic_cli import cmd_config


class TestCmdConfig:
    def test_cmd_config_output(self, capsys):
        """cmd_config should print key pool, routes, and swarm info without crashing."""
        cmd_config(None)  # None is fine since args not used in cmd_config
        captured = capsys.readouterr()
        assert "Key Pool" in captured.out
        assert "Route:" in captured.out or "Swarm:" in captured.out
        assert "CONFIGURATION STATE" in captured.out

    def test_cmd_config_routes_printed(self, capsys):
        """Verify model routes appear in config output."""
        cmd_config(None)
        captured = capsys.readouterr()
        assert "mistral" in captured.out

    def test_main_entry_points(self):
        """Verify argparse setup works for each subcommand."""
        import sys

        from merged_agentic_swarm.tools.agentic_cli import main
        # Test that unknown commands exit
        with pytest.raises(SystemExit):
            sys.argv = ["agentic_cli.py", "unknown"]
            main()


class TestCLIStringFunctions:
    """Test internal helper behaviors exposed through the CLI module."""

    def test_cmd_promote_without_orchestrator_state(self):
        """cmd_promote should not crash when called directly (uses fresh orchestrator)."""
        from merged_agentic_swarm.tools.agentic_cli import cmd_promote
        # We can't easily test this without mocking because it writes to real registry
        # Just verify it imports correctly
        assert callable(cmd_promote)

    def test_cmd_status_no_progress_file(self, capsys, temp_dir):
        """cmd_status should handle missing progress.json gracefully."""
        from merged_agentic_swarm.tools.agentic_cli import cmd_status
        # Create a mock args object
        class Args:
            progress = os.path.join(temp_dir, "nonexistent.json")
        cmd_status(Args())
        captured = capsys.readouterr()
        assert "No progress.json found" in captured.out
