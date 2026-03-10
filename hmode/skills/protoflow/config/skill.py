#!/usr/bin/env python3
"""
Monorepo Configuration Manager

Unified interface for managing all monorepo configuration:
- Guardrails (tech/arch preferences, AI steering)
- Golden Repos (project templates)
- Design System (tokens, components, guidelines)
- Domain Models (semantic domain registry)
- Code Standards (language-specific patterns)

Usage:
    /config                                    # Interactive menu
    /config --section=guardrails               # Jump to section
    /config --add-tech fastapi backend         # Direct operation
    /guardrails                                # Alias for guardrails section
    /golden-repo                               # Alias for golden-repos section
    /design-system                             # Alias for design-system section
"""
# File UUID: c8f3a9d2-4b7e-4c6f-9a2d-1e5f8b3c7d9a

import sys
from pathlib import Path
from typing import Optional, Literal
import yaml

# Add project root to path
project_root = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(project_root))

from .handlers.guardrails import GuardrailsHandler
from .handlers.golden_repos import GoldenReposHandler
from .handlers.design_system import DesignSystemHandler
from .handlers.domain_models import DomainModelsHandler
from .handlers.code_standards import CodeStandardsHandler

ConfigSection = Literal[
    "guardrails",
    "golden-repos",
    "design-system",
    "domain-models",
    "code-standards"
]

class ConfigManager:
    """Main configuration manager orchestrator."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.handlers = {
            "guardrails": GuardrailsHandler(project_root),
            "golden-repos": GoldenReposHandler(project_root),
            "design-system": DesignSystemHandler(project_root),
            "domain-models": DomainModelsHandler(project_root),
            "code-standards": CodeStandardsHandler(project_root),
        }

    def show_menu(self) -> str:
        """Display interactive menu."""
        # Get stats from each handler
        stats = {
            name: handler.get_stats()
            for name, handler in self.handlers.items()
        }

        menu = """
╔══════════════════════════════════════════════════════════════╗
║         MONOREPO CONFIGURATION MANAGER                       ║
╚══════════════════════════════════════════════════════════════╝

Select configuration area:

[1] Guardrails
    Tech/arch preferences, AI steering rules
    Status: {guardrails}

[2] Golden Repos
    Project templates and starters
    Status: {golden_repos}

[3] Design System
    Design tokens, UI components, guidelines
    Status: {design_system}

[4] Domain Models
    Semantic domain registry
    Status: {domain_models}

[5] Code Standards
    Language-specific patterns and conventions
    Status: {code_standards}

[q] Quit

Select [1-5] or 'q':
""".format(**stats)

        return menu

    def handle_interactive(self) -> dict:
        """Handle interactive menu-driven workflow."""
        menu = self.show_menu()

        # Return menu and wait for user selection
        return {
            "status": "awaiting_input",
            "prompt": menu,
            "next_step": "process_selection"
        }

    def process_selection(self, selection: str) -> dict:
        """Process user's menu selection."""
        section_map = {
            "1": "guardrails",
            "2": "golden-repos",
            "3": "design-system",
            "4": "domain-models",
            "5": "code-standards",
        }

        if selection.lower() == "q":
            return {"status": "cancelled", "message": "Configuration cancelled."}

        section = section_map.get(selection)
        if not section:
            return {
                "status": "error",
                "message": f"Invalid selection: {selection}. Choose 1-5 or 'q'."
            }

        # Delegate to section handler
        handler = self.handlers[section]
        return handler.show_section_menu()

    def handle_direct(
        self,
        section: ConfigSection,
        operation: str,
        args: list[str]
    ) -> dict:
        """Handle direct invocation with specific operation."""
        if section not in self.handlers:
            return {
                "status": "error",
                "message": f"Unknown section: {section}"
            }

        handler = self.handlers[section]

        # Delegate operation to handler
        operation_method = getattr(handler, f"handle_{operation}", None)
        if not operation_method:
            return {
                "status": "error",
                "message": f"Unknown operation '{operation}' for section '{section}'"
            }

        return operation_method(*args)


def main():
    """Main entry point for /config skill."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Monorepo Configuration Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  /config                                    # Interactive menu
  /config --section=guardrails               # Jump to guardrails
  /config --add-tech fastapi backend         # Add tech to guardrails
  /config --add-golden-repo typescript-remix # Add new template
  /config --add-color success                # Add design token
  /guardrails                                # Alias for --section=guardrails
  /golden-repo                               # Alias for --section=golden-repos
  /design-system                             # Alias for --section=design-system
"""
    )

    # Mode selection
    parser.add_argument(
        "--section",
        type=str,
        choices=["guardrails", "golden-repos", "design-system", "domain-models", "code-standards"],
        help="Jump directly to a configuration section"
    )

    # Guardrails operations
    parser.add_argument("--add-tech", nargs=2, metavar=("NAME", "CATEGORY"),
                       help="Add approved technology")
    parser.add_argument("--remove-tech", nargs=2, metavar=("NAME", "CATEGORY"),
                       help="Remove approved technology")
    parser.add_argument("--add-arch-pattern", nargs="+", metavar="PATTERN",
                       help="Add approved architecture pattern")
    parser.add_argument("--add-steering-rule", nargs="+", metavar="RULE",
                       help="Add AI steering rule")

    # Golden repo operations
    parser.add_argument("--add-golden-repo", type=str, metavar="NAME",
                       help="Add new golden repo template")
    parser.add_argument("--update-golden-repo", type=str, metavar="NAME",
                       help="Update existing golden repo")

    # Design system operations
    parser.add_argument("--add-color", type=str, metavar="NAME",
                       help="Add design system color token")
    parser.add_argument("--add-component", nargs=2, metavar=("NAME", "LEVEL"),
                       help="Add UI component (atom/molecule/organism)")
    parser.add_argument("--update-guidelines", action="store_true",
                       help="Update design system guidelines")

    # Domain model operations
    parser.add_argument("--add-domain", type=str, metavar="NAME",
                       help="Add new semantic domain")
    parser.add_argument("--list-domains", action="store_true",
                       help="List all registered domains")

    # Code standards operations
    parser.add_argument("--add-standard", nargs=2, metavar=("LANG", "NAME"),
                       help="Add code standard for language")

    args = parser.parse_args()

    # Initialize manager
    manager = ConfigManager(project_root)

    # Determine mode and operation
    if args.section:
        # Jump to specific section
        result = manager.handlers[args.section].show_section_menu()
    elif args.add_tech:
        result = manager.handle_direct("guardrails", "add_tech", args.add_tech)
    elif args.remove_tech:
        result = manager.handle_direct("guardrails", "remove_tech", args.remove_tech)
    elif args.add_arch_pattern:
        result = manager.handle_direct("guardrails", "add_arch_pattern", args.add_arch_pattern)
    elif args.add_steering_rule:
        result = manager.handle_direct("guardrails", "add_steering_rule", args.add_steering_rule)
    elif args.add_golden_repo:
        result = manager.handle_direct("golden-repos", "add", [args.add_golden_repo])
    elif args.update_golden_repo:
        result = manager.handle_direct("golden-repos", "update", [args.update_golden_repo])
    elif args.add_color:
        result = manager.handle_direct("design-system", "add_color", [args.add_color])
    elif args.add_component:
        result = manager.handle_direct("design-system", "add_component", args.add_component)
    elif args.update_guidelines:
        result = manager.handle_direct("design-system", "update_guidelines", [])
    elif args.add_domain:
        result = manager.handle_direct("domain-models", "add", [args.add_domain])
    elif args.list_domains:
        result = manager.handle_direct("domain-models", "list", [])
    elif args.add_standard:
        result = manager.handle_direct("code-standards", "add", args.add_standard)
    else:
        # No args - interactive mode
        result = manager.handle_interactive()

    # Output result
    print(yaml.dump(result, default_flow_style=False))

    return 0 if result.get("status") != "error" else 1


if __name__ == "__main__":
    sys.exit(main())
