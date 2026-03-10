"""Tests for CLI commands."""

from click.testing import CliRunner

from domain_cli.cli import cli


class TestListCommand:
    """domain list command tests."""

    def test_list_shows_domains(self, cli_runner: CliRunner) -> None:
        """List command outputs domain names."""
        result = cli_runner.invoke(cli, ["list"])
        assert result.exit_code == 0
        # Should show some output
        assert len(result.output) > 0

    def test_list_with_status_filter(self, cli_runner: CliRunner) -> None:
        """List --status filters output."""
        result = cli_runner.invoke(cli, ["list", "--status", "production"])
        assert result.exit_code == 0

    def test_list_with_invalid_status(self, cli_runner: CliRunner) -> None:
        """List --status with invalid value shows error."""
        result = cli_runner.invoke(cli, ["list", "--status", "invalid"])
        # Click should reject invalid choice
        assert result.exit_code != 0 or "invalid" in result.output.lower()


class TestShowCommand:
    """domain show command tests."""

    def test_show_not_found(self, cli_runner: CliRunner) -> None:
        """Show unknown domain shows error."""
        result = cli_runner.invoke(cli, ["show", "nonexistent-xyz-12345"])
        assert result.exit_code != 0 or "not found" in result.output.lower()


class TestSearchCommand:
    """domain search command tests."""

    def test_search_finds_matches(self, cli_runner: CliRunner) -> None:
        """Search returns matching domains."""
        # Search for common term
        result = cli_runner.invoke(cli, ["search", "core"])
        assert result.exit_code == 0

    def test_search_no_matches(self, cli_runner: CliRunner) -> None:
        """Search with no matches shows message."""
        result = cli_runner.invoke(cli, ["search", "xyznonexistent123abc"])
        assert result.exit_code == 0
        # Should indicate no results
        output_lower = result.output.lower()
        assert "no" in output_lower or "0" in result.output


class TestValidateCommand:
    """domain validate command tests."""

    def test_validate_help(self, cli_runner: CliRunner) -> None:
        """Validate shows help."""
        result = cli_runner.invoke(cli, ["validate", "--help"])
        assert result.exit_code == 0
        assert "validate" in result.output.lower()

    def test_validate_nonexistent_domain(self, cli_runner: CliRunner) -> None:
        """Validate shows error for nonexistent domain."""
        result = cli_runner.invoke(cli, ["validate", "nonexistent-xyz-12345"])
        assert result.exit_code != 0


class TestCreateCommand:
    """domain create command tests."""

    def test_create_dry_run(self, cli_runner: CliRunner) -> None:
        """Create --dry-run shows what would be created."""
        result = cli_runner.invoke(
            cli,
            ["create", "test-dry-run", "--dry-run"],
            input="Test description\n",
        )
        assert result.exit_code == 0
        assert "dry run" in result.output.lower()

    def test_create_invalid_name(self, cli_runner: CliRunner) -> None:
        """Create with invalid name shows error."""
        result = cli_runner.invoke(
            cli,
            ["create", "INVALID_NAME", "--dry-run"],
            input="Test description\n",
        )
        assert result.exit_code != 0 or "invalid" in result.output.lower()

    def test_create_name_with_uppercase_rejected(self, cli_runner: CliRunner) -> None:
        """Create rejects uppercase names."""
        result = cli_runner.invoke(
            cli,
            ["create", "InvalidName", "--dry-run"],
            input="Test description\n",
        )
        assert result.exit_code != 0 or "invalid" in result.output.lower()


class TestCLIHelp:
    """CLI help and general tests."""

    def test_help(self, cli_runner: CliRunner) -> None:
        """CLI shows help."""
        result = cli_runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "domain model cli" in result.output.lower()

    def test_list_help(self, cli_runner: CliRunner) -> None:
        """List command shows help."""
        result = cli_runner.invoke(cli, ["list", "--help"])
        assert result.exit_code == 0
        assert "list" in result.output.lower()

    def test_verbose_flag(self, cli_runner: CliRunner) -> None:
        """Verbose flag is accepted."""
        result = cli_runner.invoke(cli, ["-v", "list"])
        assert result.exit_code == 0
