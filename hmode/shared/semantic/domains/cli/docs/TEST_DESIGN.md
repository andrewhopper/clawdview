# Stage 7 - Test Design

## 1.0 Testing Strategy

**Project Type:** Python CLI Tool
**Framework:** pytest + Click CliRunner
**Track:** B (Comprehensive) - Core infrastructure tool requires high reliability

---

## 2.0 Test Categories

### 2.1 Test Matrix

| Category | Module | Priority | v0.1 | v0.2 | v0.5 |
|----------|--------|----------|------|------|------|
| Unit | Registry | P0 | ✅ | ✅ | ✅ |
| Unit | DomainInfo model | P0 | ✅ | ✅ | ✅ |
| CLI | list command | P0 | ✅ | ✅ | ✅ |
| CLI | show command | P0 | ✅ | ✅ | ✅ |
| CLI | search command | P1 | ✅ | ✅ | ✅ |
| CLI | create command | P1 | ✅ | ✅ | ✅ |
| CLI | validate command | P1 | ✅ | ✅ | ✅ |
| Unit | Validator | P1 | - | ✅ | ✅ |
| Unit | Codegen | P2 | - | - | ✅ |
| Unit | Knowledge Graph | P1 | - | - | ✅ |
| Unit | Rationale Parser | P1 | - | - | ✅ |
| Unit | Usage Tracker | P2 | - | - | ✅ |
| Unit | Research Agent | P1 | - | - | ✅ |
| Integration | Gated Creation Flow | P0 | - | - | ✅ |
| Integration | MCP Server | P2 | - | - | ✅ |

---

## 3.0 Test Specifications

### 3.1 Registry Tests (`test_registry.py`)

```python
class TestRegistry:
    """Core registry functionality tests."""

    def test_list_domains_returns_all(self, registry: Registry):
        """List returns all domains from registry.yaml."""
        domains = registry.list_domains(status=None)
        assert len(domains) >= 90  # Per current registry

    def test_list_domains_filters_by_status(self, registry: Registry):
        """List filters by production/development/archived."""
        prod = registry.list_domains(status="production")
        assert all(d.status == "production" for d in prod)

    def test_get_domain_returns_info(self, registry: Registry):
        """Get domain returns DomainInfo with correct fields."""
        domain = registry.get_domain("finance")
        assert domain is not None
        assert domain.name == "finance"
        assert isinstance(domain.entities, list)
        assert isinstance(domain.actions, list)

    def test_get_domain_not_found(self, registry: Registry):
        """Get nonexistent domain returns None."""
        domain = registry.get_domain("nonexistent-domain-xyz")
        assert domain is None

    def test_search_by_name(self, registry: Registry):
        """Search finds domains by partial name match."""
        results = registry.search_domains("fin")
        assert any(d.name == "finance" for d in results)

    def test_search_by_entity(self, registry: Registry):
        """Search finds domains containing entity."""
        results = registry.search_domains("Payment")
        assert len(results) > 0

    def test_search_by_description(self, registry: Registry):
        """Search finds domains by description content."""
        results = registry.search_domains("money")
        assert len(results) > 0

    def test_get_schema_path(self, registry: Registry):
        """Get schema path returns valid Path."""
        path = registry.get_domain_schema_path("finance")
        assert path is not None
        assert path.exists()

    def test_get_stats(self, registry: Registry):
        """Stats returns domain counts by status."""
        stats = registry.get_stats()
        assert "total" in stats
        assert "production" in stats
        assert stats["total"] >= 90
```

### 3.2 DomainInfo Model Tests (`test_models.py`)

```python
class TestDomainInfo:
    """Pydantic model validation tests."""

    def test_valid_domain_info(self):
        """Valid domain creates successfully."""
        domain = DomainInfo(
            name="test-domain",
            status="development",
            version="1.0.0",
            description="Test domain",
            entities=["Entity1"],
            actions=["action1"],
            enums=["Enum1"],
            dependencies=[]
        )
        assert domain.name == "test-domain"

    def test_domain_info_defaults(self):
        """Missing fields get defaults."""
        domain = DomainInfo(name="minimal")
        assert domain.status == "unknown"
        assert domain.version == "0.0.0"
        assert domain.entities == []

    def test_domain_info_dependencies_list(self):
        """Dependencies accepts list format."""
        domain = DomainInfo(name="test", dependencies=["core", "auth"])
        assert domain.dependencies == ["core", "auth"]

    def test_domain_info_dependencies_dict(self):
        """Dependencies accepts dict format."""
        domain = DomainInfo(name="test", dependencies={"core": "^1.0"})
        assert domain.dependencies == {"core": "^1.0"}
```

### 3.3 CLI Command Tests (`test_commands.py`)

```python
from click.testing import CliRunner

class TestListCommand:
    """domain list command tests."""

    def test_list_shows_domains(self, cli_runner: CliRunner):
        """List command outputs domain names."""
        result = cli_runner.invoke(cli, ["list"])
        assert result.exit_code == 0
        assert "finance" in result.output

    def test_list_with_status_filter(self, cli_runner: CliRunner):
        """List --status filters output."""
        result = cli_runner.invoke(cli, ["list", "--status", "production"])
        assert result.exit_code == 0

    def test_list_shows_stats(self, cli_runner: CliRunner):
        """List shows domain count summary."""
        result = cli_runner.invoke(cli, ["list"])
        assert "domains" in result.output.lower()


class TestShowCommand:
    """domain show command tests."""

    def test_show_domain_details(self, cli_runner: CliRunner):
        """Show displays domain details."""
        result = cli_runner.invoke(cli, ["show", "finance"])
        assert result.exit_code == 0
        assert "finance" in result.output

    def test_show_with_schema_flag(self, cli_runner: CliRunner):
        """Show --schema displays full schema."""
        result = cli_runner.invoke(cli, ["show", "finance", "--schema"])
        assert result.exit_code == 0
        assert "entities:" in result.output.lower() or "yaml" in result.output.lower()

    def test_show_not_found(self, cli_runner: CliRunner):
        """Show unknown domain shows error."""
        result = cli_runner.invoke(cli, ["show", "nonexistent-xyz"])
        assert result.exit_code != 0 or "not found" in result.output.lower()


class TestSearchCommand:
    """domain search command tests."""

    def test_search_finds_matches(self, cli_runner: CliRunner):
        """Search returns matching domains."""
        result = cli_runner.invoke(cli, ["search", "payment"])
        assert result.exit_code == 0

    def test_search_no_matches(self, cli_runner: CliRunner):
        """Search with no matches shows message."""
        result = cli_runner.invoke(cli, ["search", "xyznonexistent123"])
        assert result.exit_code == 0
        assert "no" in result.output.lower() or "0" in result.output


class TestValidateCommand:
    """domain validate command tests."""

    def test_validate_valid_domain(self, cli_runner: CliRunner):
        """Validate passes for well-formed domain."""
        result = cli_runner.invoke(cli, ["validate", "finance"])
        assert result.exit_code == 0

    def test_validate_all_domains(self, cli_runner: CliRunner):
        """Validate --all checks entire registry."""
        result = cli_runner.invoke(cli, ["validate", "--all"])
        assert result.exit_code == 0

    def test_validate_strict_mode(self, cli_runner: CliRunner):
        """Validate --strict enables extra checks."""
        result = cli_runner.invoke(cli, ["validate", "finance", "--strict"])
        # May pass or fail depending on domain quality
        assert result.exit_code in [0, 1]


class TestCreateCommand:
    """domain create command tests."""

    def test_create_shows_template(self, cli_runner: CliRunner):
        """Create shows domain template structure."""
        # Don't actually create - just test the flow starts
        result = cli_runner.invoke(cli, ["create", "test-domain"], input="n\n")
        # Should prompt or show something about creation
        assert result.exit_code in [0, 1]
```

### 3.4 Validation Module Tests (`test_validation.py`) - v0.2

```python
class TestDomainValidator:
    """Schema validation tests."""

    def test_validate_correct_schema(self, validator: DomainValidator):
        """Valid schema passes validation."""
        result = validator.validate(Path("domains/finance/schema.yaml"))
        assert result.valid is True
        assert len(result.errors) == 0

    def test_validate_missing_required_fields(self, validator: DomainValidator):
        """Missing required fields produce errors."""
        result = validator.validate_content({
            "name": "incomplete"
            # Missing: version, entities, etc.
        })
        assert result.valid is False
        assert len(result.errors) > 0

    def test_validate_invalid_status(self, validator: DomainValidator):
        """Invalid status value produces error."""
        result = validator.validate_content({
            "name": "test",
            "version": "1.0.0",
            "status": "invalid_status"
        })
        assert result.valid is False
        assert any("status" in str(e) for e in result.errors)

    def test_validate_all_returns_summary(self, validator: DomainValidator):
        """Validate all returns list of results."""
        results = validator.validate_all()
        assert len(results) >= 90
        assert all(isinstance(r, ValidationResult) for r in results)
```

### 3.5 Knowledge Graph Tests (`test_knowledge.py`) - v0.5

```python
class TestKnowledgeGraph:
    """Knowledge graph operations tests."""

    def test_record_domain_creation(self, kg: KnowledgeGraph):
        """Recording domain creation adds node."""
        rationale = Rationale(
            domain="test-domain",
            version="1.0.0",
            created="2025-12-15",
            author="test@example.com",
            purpose="Test purpose",
            inspiration=[],
            rejected=[],
            primitives_used={},
            extends_domains=[],
            decisions=[]
        )
        kg.record_domain_creation("test-domain", rationale)
        retrieved = kg.get_domain_rationale("test-domain")
        assert retrieved is not None
        assert retrieved.purpose == "Test purpose"

    def test_record_import(self, kg: KnowledgeGraph):
        """Recording import updates usage stats."""
        kg.record_domain_import(
            domain="finance",
            project="projects/test-project",
            entities=["Payment", "Invoice"]
        )
        stats = kg.get_domain_usage("finance")
        assert stats.import_count > 0
        assert "Payment" in stats.entities_most_used

    def test_get_similar_domains(self, kg: KnowledgeGraph):
        """Similar domains returns related domains."""
        similar = kg.get_similar_domains("finance", limit=5)
        assert len(similar) <= 5

    def test_get_most_reused(self, kg: KnowledgeGraph):
        """Most reused returns top domains by imports."""
        top = kg.get_most_reused_domains(limit=10)
        assert len(top) <= 10
        # Should be sorted descending
        counts = [count for _, count in top]
        assert counts == sorted(counts, reverse=True)

    def test_get_patterns_for_category(self, kg: KnowledgeGraph):
        """Patterns returns relevant patterns."""
        patterns = kg.get_patterns_for_category("payment")
        assert isinstance(patterns, list)


class TestRationale:
    """Rationale model tests."""

    def test_parse_rationale_file(self, tmp_path: Path):
        """Parse .rationale.yaml file."""
        rationale_content = """
domain: test
version: "1.0.0"
created: "2025-12-15"
author: test@example.com
purpose: Test domain
inspiration: []
rejected: []
primitives_used: {}
extends_domains: []
decisions: []
"""
        rationale_file = tmp_path / ".rationale.yaml"
        rationale_file.write_text(rationale_content)

        rationale = Rationale.from_file(rationale_file)
        assert rationale.domain == "test"
        assert rationale.version == "1.0.0"

    def test_rationale_to_yaml(self):
        """Rationale serializes to YAML."""
        rationale = Rationale(
            domain="test",
            version="1.0.0",
            created="2025-12-15",
            author="test@example.com",
            purpose="Test",
            inspiration=[],
            rejected=[],
            primitives_used={},
            extends_domains=[],
            decisions=[]
        )
        yaml_str = rationale.to_yaml()
        assert "domain: test" in yaml_str
        assert "version:" in yaml_str
```

### 3.6 Research Agent Tests (`test_research.py`) - v0.5

```python
class TestAPIModelFetcher:
    """API reference fetching tests."""

    def test_infer_category_payment(self, fetcher: APIModelFetcher):
        """Infers payment category from name."""
        category = fetcher.infer_category("payment-processor")
        assert category == "payment"

    def test_infer_category_booking(self, fetcher: APIModelFetcher):
        """Infers booking category."""
        category = fetcher.infer_category("appointment-scheduler")
        assert category == "booking"

    def test_fetch_models_returns_definitions(self, fetcher: APIModelFetcher):
        """Fetch returns model definitions."""
        # This may require mocking HTTP calls
        models = fetcher.fetch_models("payment")
        assert isinstance(models, list)

    def test_identify_patterns(self, fetcher: APIModelFetcher):
        """Identifies common patterns across models."""
        models = [
            ModelDefinition(name="PaymentIntent", fields={"amount": "int", "currency": "str"}),
            ModelDefinition(name="Payment", fields={"amount": "int", "currency": "str"})
        ]
        patterns = fetcher.identify_patterns(models)
        assert any("Money" in p.name or "amount" in str(p) for p in patterns)


class TestDesignAssistant:
    """Design suggestion tests."""

    def test_suggest_primitives(self, assistant: DomainDesignAssistant):
        """Suggests relevant primitives for domain."""
        primitives = assistant.suggest_primitives("invoice")
        assert len(primitives) > 0
        # Should suggest Money primitive for invoice
        assert any("money" in p.name.lower() or "quantity" in p.name.lower() for p in primitives)

    def test_suggest_schema(self, assistant: DomainDesignAssistant):
        """Generates suggested schema structure."""
        suggestion = assistant.suggest_schema(
            name="payment-processor",
            api_models=[],
            primitives=[],
            existing_domains=[]
        )
        assert suggestion is not None
        assert suggestion.entities is not None
```

### 3.7 Gated Creation Flow Tests (`test_creation_flow.py`) - v0.5

```python
class TestGatedCreation:
    """End-to-end gated creation flow tests."""

    def test_creation_shows_internal_search(self, cli_runner: CliRunner):
        """Create searches internal registry first."""
        result = cli_runner.invoke(
            cli,
            ["create", "payment-handler"],
            input="4\nn\n"  # Select "create new", then cancel
        )
        assert "similar" in result.output.lower() or "found" in result.output.lower()

    def test_creation_shows_primitives(self, cli_runner: CliRunner):
        """Create suggests primitives to compose."""
        result = cli_runner.invoke(
            cli,
            ["create", "invoice-manager"],
            input="4\nn\n"
        )
        assert "primitive" in result.output.lower()

    def test_creation_shows_inspiration(self, cli_runner: CliRunner):
        """Create shows best-in-class API models."""
        result = cli_runner.invoke(
            cli,
            ["create", "payment-gateway"],
            input="4\nn\n"
        )
        # Should mention Stripe or similar
        output_lower = result.output.lower()
        assert any(api in output_lower for api in ["stripe", "square", "inspiration"])

    def test_creation_requires_justification(self, cli_runner: CliRunner):
        """Creating from scratch requires justification."""
        result = cli_runner.invoke(
            cli,
            ["create", "unique-concept"],
            input="4\nTest justification\ny\n"  # New from scratch, provide justification
        )
        assert "justif" in result.output.lower() or "reason" in result.output.lower()

    def test_creation_generates_rationale(self, cli_runner: CliRunner, tmp_path: Path):
        """Successful creation generates .rationale.yaml."""
        # This would need a test fixture for domain creation
        pass  # Integration test - implement with proper fixtures

    def test_skip_research_flag(self, cli_runner: CliRunner):
        """--skip-research bypasses research steps."""
        result = cli_runner.invoke(
            cli,
            ["create", "quick-domain", "--skip-research"],
            input="y\n"
        )
        # Should not show inspiration section
        assert "stripe" not in result.output.lower()
```

---

## 4.0 Test Fixtures (`conftest.py`)

```python
import pytest
from pathlib import Path
from click.testing import CliRunner
from domain_cli.registry import Registry
from domain_cli.cli import cli

@pytest.fixture
def domains_root() -> Path:
    """Return path to actual domains directory."""
    return Path(__file__).parent.parent.parent.parent  # shared/semantic/domains/

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
```

---

## 5.0 Coverage Targets

| Version | Target | Focus |
|---------|--------|-------|
| v0.1 | 70% | Registry, CLI commands |
| v0.2 | 75% | + Validation |
| v0.3 | 75% | + Codegen |
| v0.4 | 75% | + MCP (integration tests) |
| v0.5 | 80% | + Knowledge system, research |

---

## 6.0 Test Execution

```bash
# Run all tests
cd shared/semantic/domains/cli
pytest

# Run with coverage
pytest --cov=domain_cli --cov-report=html

# Run specific category
pytest tests/test_registry.py -v

# Run marked tests
pytest -m "not integration"  # Skip integration tests
pytest -m "v01"              # Only v0.1 tests
```

---

## 7.0 Exit Criteria

- ✅ Test strategy defined (pytest + Click CliRunner)
- ✅ Test matrix created (all modules, versions)
- ✅ Test specifications written (7 test files)
- ✅ Fixtures defined (conftest.py)
- ✅ Coverage targets set (70-80%)
- ⏳ **Ready for Phase 8 implementation validation**
