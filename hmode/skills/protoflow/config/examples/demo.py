#!/usr/bin/env python3
"""
Demo script showing config skill usage patterns.

This demonstrates how to use the config skill programmatically
and shows expected flow for each operation type.
"""
# File UUID: f6a7b8c9-0d1e-2f3a-4b5c-6d7e8f9a0b1c

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(project_root))

from ..handlers import (
    GuardrailsHandler,
    GoldenReposHandler,
    DesignSystemHandler,
    DomainModelsHandler,
    CodeStandardsHandler,
)


def demo_interactive_flow():
    """Demonstrate interactive menu flow."""
    print("=" * 70)
    print("DEMO: Interactive Flow")
    print("=" * 70)

    from ..skill import ConfigManager

    manager = ConfigManager(project_root)

    # Step 1: Show main menu
    result = manager.handle_interactive()
    print("\nStep 1 - Main Menu:")
    print(result["prompt"])

    # Step 2: User selects option 1 (Guardrails)
    result = manager.process_selection("1")
    print("\nStep 2 - Guardrails Menu:")
    print(result["prompt"])

    print("\n✅ Interactive flow demonstrated")


def demo_direct_operations():
    """Demonstrate direct operation flow."""
    print("\n" + "=" * 70)
    print("DEMO: Direct Operations")
    print("=" * 70)

    handler = GuardrailsHandler(project_root)

    # Example: Add technology
    print("\nOperation: Add FastAPI to backend guardrails")
    result = handler.handle_add_tech("fastapi", "backend")

    print(f"\nStatus: {result['status']}")
    if result['status'] == 'awaiting_confirmation':
        print(result['prompt'])
        print("\n⚠️  Awaiting user confirmation...")

    print("\n✅ Direct operation demonstrated")


def demo_design_system():
    """Demonstrate design system operations."""
    print("\n" + "=" * 70)
    print("DEMO: Design System Operations")
    print("=" * 70)

    handler = DesignSystemHandler(project_root)

    # Get current stats
    stats = handler.get_stats()
    print(f"\nCurrent Status: {stats}")

    # Show section menu
    result = handler.show_section_menu()
    print(result["prompt"])

    # Example: Add color token
    print("\nOperation: Add 'success' color token")
    result = handler.handle_add_color("success")

    print(f"\nStatus: {result['status']}")
    if 'prompt' in result:
        print(result['prompt'])

    print("\n✅ Design system operations demonstrated")


def demo_domain_models():
    """Demonstrate domain model operations."""
    print("\n" + "=" * 70)
    print("DEMO: Domain Model Operations")
    print("=" * 70)

    handler = DomainModelsHandler(project_root)

    # List domains
    result = handler.handle_list()
    print(f"\n{result['message']}")

    # Example: Add domain (delegates to agent)
    print("\nOperation: Add 'ecommerce' domain")
    result = handler.handle_add("ecommerce")

    print(f"\nStatus: {result['status']}")
    if result['status'] == 'delegate':
        print(f"→ Delegating to: {result['agent']}")
        print(f"→ Prompt: {result['prompt']}")

    print("\n✅ Domain model operations demonstrated")


def demo_golden_repos():
    """Demonstrate golden repo operations."""
    print("\n" + "=" * 70)
    print("DEMO: Golden Repo Operations")
    print("=" * 70)

    handler = GoldenReposHandler(project_root)

    # Show section menu
    result = handler.show_section_menu()
    print(result["prompt"])

    # Example: Add new template
    print("\nOperation: Add 'typescript-remix' template")
    result = handler.handle_add("typescript-remix")

    print(f"\nStatus: {result['status']}")
    if 'prompt' in result:
        print(result['prompt'])

    print("\n✅ Golden repo operations demonstrated")


def demo_validation():
    """Demonstrate design system validation."""
    print("\n" + "=" * 70)
    print("DEMO: Design System Validation")
    print("=" * 70)

    handler = DesignSystemHandler(project_root)

    # Example: Validate a file
    test_file = project_root / "shared" / "design-system" / "examples" / "compliant-mockup.html"

    if test_file.exists():
        print(f"\nValidating: {test_file.name}")
        result = handler.validate_compliance(str(test_file))

        print(f"\nStatus: {result['status']}")
        print(result['report'])
    else:
        print(f"\n⚠️  Test file not found: {test_file}")

    print("\n✅ Validation demonstrated")


def main():
    """Run all demos."""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "CONFIG SKILL DEMONSTRATION" + " " * 27 + "║")
    print("╚" + "=" * 68 + "╝")
    print()

    demos = [
        demo_interactive_flow,
        demo_direct_operations,
        demo_design_system,
        demo_domain_models,
        demo_golden_repos,
        demo_validation,
    ]

    for demo in demos:
        try:
            demo()
        except Exception as e:
            print(f"\n❌ Demo failed: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 70)
    print("✅ All demos completed")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
