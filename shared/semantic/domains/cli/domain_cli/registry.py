"""Domain registry operations - load and query domain models."""

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel


class DomainInfo(BaseModel):
    """Domain metadata from registry."""

    name: str
    status: str = "unknown"
    version: str = "0.0.0"
    description: str = ""
    owner: str = "unknown"
    entities: list[str] = []
    actions: list[str] = []
    enums: list[str] = []
    dependencies: list[str] | dict[str, str] = []
    path: str | None = None


class Registry:
    """Load and query the domain registry."""

    def __init__(self, domains_root: Path | None = None) -> None:
        """Initialize registry with domains root path."""
        if domains_root is None:
            # Default to parent of cli/ directory
            domains_root = Path(__file__).parent.parent.parent
        self.domains_root = domains_root
        self.registry_path = domains_root / "registry.yaml"
        self._data: dict[str, Any] | None = None

    def _load(self) -> dict[str, Any]:
        """Load registry data from YAML."""
        if self._data is None:
            with open(self.registry_path) as f:
                self._data = yaml.safe_load(f)
        return self._data

    @property
    def version(self) -> str:
        """Registry version."""
        return self._load().get("version", "unknown")

    @property
    def updated(self) -> str:
        """Registry last updated date."""
        return self._load().get("updated", "unknown")

    def list_domains(self, status: str | None = None) -> list[DomainInfo]:
        """List all domains, optionally filtered by status."""
        data = self._load()
        domains = []

        for name, info in data.get("domains", {}).items():
            if isinstance(info, dict):
                # Handle dependencies - can be list or dict
                deps = info.get("dependencies", [])
                if isinstance(deps, dict):
                    deps = list(deps.keys())

                domain = DomainInfo(
                    name=name,
                    status=info.get("status", "unknown"),
                    version=info.get("version", info.get("current_version", "0.0.0")),
                    description=info.get("description", ""),
                    owner=info.get("owner", "unknown"),
                    entities=info.get("entities", []),
                    actions=info.get("actions", []),
                    enums=info.get("enums", []),
                    dependencies=deps,
                    path=info.get("path"),
                )

                if status is None or domain.status == status:
                    domains.append(domain)

        return sorted(domains, key=lambda d: d.name)

    def get_domain(self, name: str) -> DomainInfo | None:
        """Get a specific domain by name."""
        data = self._load()
        domains = data.get("domains", {})

        if name not in domains:
            return None

        info = domains[name]
        if not isinstance(info, dict):
            return None

        deps = info.get("dependencies", [])
        if isinstance(deps, dict):
            deps = list(deps.keys())

        return DomainInfo(
            name=name,
            status=info.get("status", "unknown"),
            version=info.get("version", info.get("current_version", "0.0.0")),
            description=info.get("description", ""),
            owner=info.get("owner", "unknown"),
            entities=info.get("entities", []),
            actions=info.get("actions", []),
            enums=info.get("enums", []),
            dependencies=deps,
            path=info.get("path"),
        )

    def search_domains(self, query: str) -> list[DomainInfo]:
        """Search domains by name, description, or entities."""
        query_lower = query.lower()
        results = []

        for domain in self.list_domains():
            # Search in name
            if query_lower in domain.name.lower():
                results.append(domain)
                continue

            # Search in description
            if query_lower in domain.description.lower():
                results.append(domain)
                continue

            # Search in entities
            for entity in domain.entities:
                if query_lower in entity.lower():
                    results.append(domain)
                    break

        return results

    def get_domain_schema_path(self, name: str) -> Path | None:
        """Get the schema file path for a domain."""
        domain = self.get_domain(name)
        if domain is None:
            return None

        # Check various schema locations
        candidates = [
            self.domains_root / name / "schema.yaml",
            self.domains_root / name / "models.yaml",
            self.domains_root / name / f"{name}.yaml",
        ]

        # If domain has explicit path
        if domain.path:
            candidates.insert(0, self.domains_root / domain.path)

        for path in candidates:
            if path.exists():
                return path

        return None

    def get_stats(self) -> dict[str, int]:
        """Get registry statistics."""
        domains = self.list_domains()
        stats = {
            "total": len(domains),
            "production": 0,
            "development": 0,
            "deprecated": 0,
            "other": 0,
        }

        for domain in domains:
            if domain.status == "production":
                stats["production"] += 1
            elif domain.status == "development":
                stats["development"] += 1
            elif domain.status == "deprecated":
                stats["deprecated"] += 1
            else:
                stats["other"] += 1

        return stats
