"""Test fixtures for domain-cli."""

from pathlib import Path

import pytest
from click.testing import CliRunner

from domain_cli.cli import cli
from domain_cli.registry import Registry


@pytest.fixture
def domains_root() -> Path:
    """Return path to actual domains directory."""
    # tests/ -> cli/ -> domains/
    return Path(__file__).parent.parent.parent


@pytest.fixture
def registry(domains_root: Path) -> Registry:
    """Create Registry instance with real domains."""
    return Registry(domains_root)


@pytest.fixture
def cli_runner() -> CliRunner:
    """Create Click CliRunner for command testing."""
    return CliRunner()


@pytest.fixture
def tmp_domain(tmp_path: Path) -> Path:
    """Create temporary domain for testing."""
    domain_dir = tmp_path / "test-domain"
    domain_dir.mkdir()
    schema = domain_dir / "schema.yaml"
    schema.write_text("""
name: test-domain
version: "1.0.0"
status: development
description: Test domain for unit tests
entities:
  TestEntity:
    properties:
      id: string
      name: string
actions:
  - test_action
enums:
  TestEnum:
    values: [VALUE_A, VALUE_B]
""")
    return domain_dir
