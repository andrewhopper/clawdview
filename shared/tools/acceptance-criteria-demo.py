#!/usr/bin/env python3
"""
Acceptance Criteria Tool - Demo

Quick demonstration of the acceptance criteria verification system.
"""
# File UUID: 4d6f8a1b-2c3e-5f7a-9b0c-1d2e3f4a5b6c

from acceptance_criteria import AcceptanceCriteria


def demo_html_verification():
    """Demonstrate HTML file verification."""
    print("\n" + "=" * 60)
    print("DEMO 1: HTML File Verification")
    print("=" * 60)

    context = {
        'task_type': 'html',
        'description': 'Generated landing page mockup',
        'files_affected': ['landing-page.html']
    }

    ac = AcceptanceCriteria(context)
    criteria = ac.generate_criteria()

    print(f"\nGenerated {len(criteria)} acceptance criteria:")
    for i, criterion in enumerate(criteria, 1):
        print(f"  {i}. {criterion['name']} ({criterion['type']})")

    print("\nNext steps:")
    print("  - User would select which criteria to run")
    print("  - Automated checks execute (curl, grep, etc.)")
    print("  - Manual checks prompt for confirmation")
    print("  - Results show pass/fail for each criterion")


def demo_api_verification():
    """Demonstrate API deployment verification."""
    print("\n" + "=" * 60)
    print("DEMO 2: API Deployment Verification")
    print("=" * 60)

    context = {
        'task_type': 'api',
        'description': 'Deploy API to staging',
        'api_url': 'https://api.staging.example.com'
    }

    ac = AcceptanceCriteria(context)
    criteria = ac.generate_criteria()

    print(f"\nGenerated {len(criteria)} acceptance criteria:")
    for i, criterion in enumerate(criteria, 1):
        check_type = "🤖 AUTO" if criterion['type'] == 'automated' else "👤 MANUAL"
        print(f"  {check_type} {i}. {criterion['name']}")
        if criterion['type'] == 'automated':
            print(f"        Command: {criterion['command']}")


def demo_deployment_verification():
    """Demonstrate infrastructure deployment verification."""
    print("\n" + "=" * 60)
    print("DEMO 3: Infrastructure Deployment Verification")
    print("=" * 60)

    context = {
        'task_type': 'deployment',
        'description': 'Deploy to production',
        'stack_name': 'my-app-prod',
        'domain': 'app.example.com'
    }

    ac = AcceptanceCriteria(context)
    criteria = ac.generate_criteria()

    print(f"\nGenerated {len(criteria)} acceptance criteria:")
    for i, criterion in enumerate(criteria, 1):
        check_type = "🤖 AUTO" if criterion['type'] == 'automated' else "👤 MANUAL"
        print(f"  {check_type} {i}. {criterion['name']}")


def demo_custom_criteria():
    """Demonstrate adding custom criteria."""
    print("\n" + "=" * 60)
    print("DEMO 4: Custom Criteria")
    print("=" * 60)

    context = {
        'task_type': 'html',
        'description': 'E-commerce product page',
        'files_affected': ['product-page.html']
    }

    ac = AcceptanceCriteria(context)
    ac.generate_criteria()

    # Add custom criteria
    ac.criteria.append({
        'id': '99',
        'name': 'Brand colors match style guide',
        'type': 'manual',
        'prompt': 'Compare colors against brand guidelines document'
    })

    ac.criteria.append({
        'id': '100',
        'name': 'Product images optimized',
        'type': 'automated',
        'command': 'find . -name "*.jpg" -size +500k',
        'success': 'No matches (all images < 500KB)'
    })

    print(f"\nGenerated {len(ac.criteria)} acceptance criteria (including custom):")
    for i, criterion in enumerate(ac.criteria, 1):
        check_type = "🤖 AUTO" if criterion['type'] == 'automated' else "👤 MANUAL"
        custom = " (CUSTOM)" if int(criterion['id']) >= 99 else ""
        print(f"  {check_type} [{criterion['id']}] {criterion['name']}{custom}")


def main():
    """Run all demos."""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "Acceptance Criteria Tool - DEMO" + " " * 16 + "║")
    print("╚" + "═" * 58 + "╝")

    demo_html_verification()
    demo_api_verification()
    demo_deployment_verification()
    demo_custom_criteria()

    print("\n" + "=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)
    print("\nTo run actual verification:")
    print("  1. Use the Python API (see examples above)")
    print("  2. Use CLI: acceptance_criteria.py --context '{...}'")
    print("  3. Use in Claude Code: /acceptance-criteria")
    print("\nDocumentation:")
    print("  - Guide: shared/tools/ACCEPTANCE_CRITERIA_GUIDE.md")
    print("  - Skill: .claude/skills/acceptance-criteria.md")
    print("  - Summary: docs/acceptance-criteria-agent-summary.md")
    print()


if __name__ == '__main__':
    main()
