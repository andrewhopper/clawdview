"""Tests for Registry module."""

from pathlib import Path

import pytest

from domain_cli.registry import DomainInfo, Registry


class TestDomainInfo:
    """Pydantic model validation tests."""

    def test_valid_domain_info(self) -> None:
        """Valid domain creates successfully."""
        domain = DomainInfo(
            name="test-domain",
            status="development",
            version="1.0.0",
            description="Test domain",
            entities=["Entity1"],
            actions=["action1"],
            enums=["Enum1"],
            dependencies=[],
        )
        assert domain.name == "test-domain"
        assert domain.status == "development"

    def test_domain_info_defaults(self) -> None:
        """Missing fields get defaults."""
        domain = DomainInfo(name="minimal")
        assert domain.status == "unknown"
        assert domain.version == "0.0.0"
        assert domain.entities == []
        assert domain.actions == []

    def test_domain_info_dependencies_list(self) -> None:
        """Dependencies accepts list format."""
        domain = DomainInfo(name="test", dependencies=["core", "auth"])
        assert domain.dependencies == ["core", "auth"]

    def test_domain_info_dependencies_dict(self) -> None:
        """Dependencies accepts dict format."""
        domain = DomainInfo(name="test", dependencies={"core": "^1.0"})
        assert domain.dependencies == {"core": "^1.0"}


class TestRegistry:
    """Core registry functionality tests."""

    def test_list_domains_returns_all(self, registry: Registry) -> None:
        """List returns all domains from registry.yaml."""
        domains = registry.list_domains(status=None)
        assert len(domains) >= 50  # Reasonable minimum

    def test_list_domains_filters_by_status(self, registry: Registry) -> None:
        """List filters by production/development/archived."""
        prod = registry.list_domains(status="production")
        if prod:  # Only test if there are production domains
            assert all(d.status == "production" for d in prod)

    def test_get_domain_returns_info(self, registry: Registry) -> None:
        """Get domain returns DomainInfo with correct fields."""
        # Use a domain that's likely to exist
        domains = registry.list_domains()
        if domains:
            first_domain = domains[0]
            domain = registry.get_domain(first_domain.name)
            assert domain is not None
            assert domain.name == first_domain.name
            assert isinstance(domain.entities, list)
            assert isinstance(domain.actions, list)

    def test_get_domain_not_found(self, registry: Registry) -> None:
        """Get nonexistent domain returns None."""
        domain = registry.get_domain("nonexistent-domain-xyz-12345")
        assert domain is None

    def test_search_by_name(self, registry: Registry) -> None:
        """Search finds domains by partial name match."""
        # Get first domain to search for
        domains = registry.list_domains()
        if domains:
            first_name = domains[0].name
            # Search for part of the name
            search_term = first_name[:3] if len(first_name) >= 3 else first_name
            results = registry.search_domains(search_term)
            assert len(results) > 0

    def test_search_no_results(self, registry: Registry) -> None:
        """Search with no matches returns empty list."""
        results = registry.search_domains("xyznonexistent12345abc")
        assert results == []

    def test_get_stats(self, registry: Registry) -> None:
        """Stats returns domain counts by status."""
        stats = registry.get_stats()
        assert "total" in stats
        assert "production" in stats
        assert "development" in stats
        assert stats["total"] >= 0

    def test_registry_version(self, registry: Registry) -> None:
        """Registry has version."""
        assert registry.version is not None

    def test_registry_updated(self, registry: Registry) -> None:
        """Registry has updated date."""
        assert registry.updated is not None
