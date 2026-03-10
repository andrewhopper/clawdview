#!/usr/bin/env python3
"""
Domain Models Configuration Handler

Manages semantic domain registry in shared/semantic/domains/.
Delegates to domain-modeling-specialist agent for complex operations.
"""
# File UUID: a1b2c3d4-5e6f-7a8b-9c0d-1e2f3a4b5c6d

from pathlib import Path
from typing import Optional
import yaml

class DomainModelsHandler:
    """Handler for domain models configuration (shared/semantic/domains/)."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.domains_dir = project_root / "shared" / "semantic" / "domains"
        self.registry_file = self.domains_dir / "registry.yaml"

    def get_stats(self) -> str:
        """Get current stats for menu display."""
        if not self.registry_file.exists():
            return "0 domains registered"

        with open(self.registry_file) as f:
            registry = yaml.safe_load(f)

        domain_count = len(registry.get("domains", []))
        return f"{domain_count} domains registered"

    def show_section_menu(self) -> dict:
        """Show domain models section menu."""
        # Read registry
        domains = []
        if self.registry_file.exists():
            with open(self.registry_file) as f:
                registry = yaml.safe_load(f) or {}
                domains = registry.get("domains", [])

        domains_display = "\n".join(f"  - {d['name']}: {d.get('description', 'No description')}"
                                    for d in domains) if domains else "  (none)"

        menu = f"""
╔══════════════════════════════════════════════════════════════╗
║         DOMAIN MODELS CONFIGURATION                          ║
╚══════════════════════════════════════════════════════════════╝

Registered Domains:
{domains_display}

Operations:
  [1] List all domains
  [2] Search domains
  [3] Add new domain (spawns domain-modeling-specialist)
  [4] Evolve existing domain (spawns domain-modeling-specialist)
  [5] View domain details
  [b] Back to main menu

Select [1-5] or 'b':
"""

        return {
            "status": "awaiting_input",
            "prompt": menu,
            "section": "domain-models"
        }

    def handle_list(self) -> dict:
        """List all registered domains."""
        if not self.registry_file.exists():
            return {
                "status": "success",
                "message": "No domains registered yet",
                "domains": []
            }

        with open(self.registry_file) as f:
            registry = yaml.safe_load(f) or {}

        domains = registry.get("domains", [])

        # Format output
        output = ["Registered Domains:\n"]
        for domain in domains:
            output.append(f"  {domain['name']}")
            output.append(f"    Description: {domain.get('description', 'N/A')}")
            output.append(f"    Version: {domain.get('version', '1.0.0')}")
            output.append(f"    Location: {domain.get('path', 'N/A')}")
            output.append("")

        return {
            "status": "success",
            "message": "\n".join(output),
            "domains": domains
        }

    def handle_add(self, domain_name: str) -> dict:
        """Add new domain - delegates to domain-modeling-specialist agent."""
        return {
            "status": "delegate",
            "message": f"Creating domain '{domain_name}' requires domain-modeling-specialist agent",
            "action": "spawn_agent",
            "agent": "domain-modeling-specialist",
            "prompt": f"Create new semantic domain model for '{domain_name}' with external research and human approval workflow"
        }

    def handle_search(self, query: str) -> dict:
        """Search domains by name or description."""
        if not self.registry_file.exists():
            return {
                "status": "success",
                "message": "No domains registered yet",
                "matches": []
            }

        with open(self.registry_file) as f:
            registry = yaml.safe_load(f) or {}

        domains = registry.get("domains", [])
        query_lower = query.lower()

        matches = [
            d for d in domains
            if query_lower in d.get("name", "").lower()
            or query_lower in d.get("description", "").lower()
        ]

        if matches:
            output = [f"Found {len(matches)} matching domain(s):\n"]
            for domain in matches:
                output.append(f"  {domain['name']}")
                output.append(f"    Description: {domain.get('description', 'N/A')}")
                output.append("")

            return {
                "status": "success",
                "message": "\n".join(output),
                "matches": matches
            }
        else:
            return {
                "status": "success",
                "message": f"No domains matching '{query}' found",
                "matches": []
            }
