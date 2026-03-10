"""CLI tests."""

from click.testing import CliRunner

from src.cli import cli


def test_cli_help(cli_runner: CliRunner) -> None:
    """Test CLI help output."""
    result = cli_runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Gold standard Python CLI template" in result.output


def test_greet_command(cli_runner: CliRunner) -> None:
    """Test greet command."""
    result = cli_runner.invoke(cli, ["greet", "World"])
    assert result.exit_code == 0
    assert "Hello, World!" in result.output


def test_greet_command_loud(cli_runner: CliRunner) -> None:
    """Test greet command with loud option."""
    result = cli_runner.invoke(cli, ["greet", "--loud", "World"])
    assert result.exit_code == 0
    assert "HELLO, WORLD!" in result.output


def test_process_command_dry_run(cli_runner: CliRunner) -> None:
    """Test process command with dry run."""
    result = cli_runner.invoke(cli, ["process", "--dry-run", "file1.txt", "file2.txt"])
    assert result.exit_code == 0
    assert "Dry run mode" in result.output
    assert "file1.txt" in result.output
    assert "file2.txt" in result.output
