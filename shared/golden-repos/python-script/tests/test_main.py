"""Tests for main module."""

from typer.testing import CliRunner

from src.main import app

runner = CliRunner()


class TestMainCommand:
    """Tests for main CLI commands."""

    def test_run_no_args(self) -> None:
        """Test run command with no arguments."""
        result = runner.invoke(app, ["run"])
        assert result.exit_code == 0

    def test_run_verbose(self) -> None:
        """Test run command with verbose flag."""
        result = runner.invoke(app, ["run", "--verbose"])
        assert result.exit_code == 0

    def test_run_dry_run(self) -> None:
        """Test run command with dry-run flag."""
        result = runner.invoke(app, ["run", "--dry-run"])
        assert result.exit_code == 0

    def test_version(self) -> None:
        """Test version command."""
        result = runner.invoke(app, ["version"])
        assert result.exit_code == 0
        assert "v0.1.0" in result.stdout
