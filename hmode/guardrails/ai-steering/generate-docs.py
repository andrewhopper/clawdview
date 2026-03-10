#!/usr/bin/env python3
"""
Generate markdown documentation from JSON steering rules.

Usage:
    python generate-docs.py                    # Generate all docs
    python generate-docs.py tool-usage         # Generate specific category
    python generate-docs.py --validate         # Validate JSON first
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


def load_rule_file(file_path: Path) -> Dict[str, Any]:
    """Load and parse a rule JSON file."""
    with open(file_path) as f:
        return json.load(f)


def constraint_level_emoji(level: str) -> str:
    """Get emoji for constraint level."""
    emojis = {
        "NEVER": "🚫",
        "ALWAYS": "✅",
        "MUST": "⚠️",
        "MUST_NOT": "❌",
        "SHOULD": "💡",
        "SHOULD_NOT": "⚡",
        "PREFER": "👍",
        "AVOID": "👎"
    }
    return emojis.get(level, "📋")


def format_rule_header(rule: Dict[str, Any]) -> str:
    """Format rule header section."""
    level = rule["level"]
    emoji = constraint_level_emoji(level)

    return f"""### {emoji} {rule['id']}

**Level:** {level}
**Category:** {rule['category']}

{rule['description']}
"""


def format_context(context: Dict[str, Any]) -> str:
    """Format context matching section."""
    if not context:
        return ""

    lines = ["\n**Context:**"]

    if "when" in context and context["when"]:
        lines.append(f"- **When:** {', '.join(context['when'])}")

    if "unless" in context and context["unless"]:
        lines.append(f"- **Unless:** {', '.join(context['unless'])}")

    if "phase" in context:
        lines.append(f"- **Phases:** {', '.join(context['phase'])}")

    if "filePattern" in context:
        lines.append(f"- **File Pattern:** `{context['filePattern']}`")

    if "fileCount" in context:
        fc = context["fileCount"]
        if "min" in fc:
            lines.append(f"- **Min Files:** {fc['min']}")
        if "max" in fc:
            lines.append(f"- **Max Files:** {fc['max']}")

    if "taskType" in context:
        lines.append(f"- **Task Types:** {', '.join(context['taskType'])}")

    if "toolInvolved" in context:
        lines.append(f"- **Tools:** {', '.join(context['toolInvolved'])}")

    if "destructive" in context:
        lines.append(f"- **Destructive:** {context['destructive']}")

    return "\n".join(lines)


def format_action(action: Dict[str, Any]) -> str:
    """Format action section."""
    lines = ["\n**Action:**"]
    lines.append(f"- **Directive:** {action['directive']}")
    lines.append(f"- **Target:** {action['target']}")

    if action.get("alternative"):
        lines.append(f"- **Alternative:** {action['alternative']}")

    if action.get("message"):
        lines.append(f"- **Message:** \"{action['message']}\"")

    return "\n".join(lines)


def format_examples(examples: List[Dict[str, Any]]) -> str:
    """Format examples section."""
    if not examples:
        return ""

    lines = ["\n**Examples:**"]

    for i, example in enumerate(examples, 1):
        lines.append(f"\n{i}. **Scenario:** {example['scenario']}")
        lines.append(f"   - ✅ **Correct:** {example['correct']}")
        if "incorrect" in example:
            lines.append(f"   - ❌ **Incorrect:** {example['incorrect']}")

    return "\n".join(lines)


def format_rule(rule: Dict[str, Any]) -> str:
    """Format complete rule as markdown."""
    sections = [
        format_rule_header(rule),
        f"**Rationale:** {rule.get('rationale', 'N/A')}"
    ]

    if "context" in rule:
        sections.append(format_context(rule["context"]))

    sections.append(format_action(rule["action"]))

    if "examples" in rule:
        sections.append(format_examples(rule["examples"]))

    if "metadata" in rule:
        meta = rule["metadata"]
        sections.append(f"\n*Approved by: {meta.get('approvedBy', 'N/A')} on {meta.get('approvedDate', 'N/A')}*")

    sections.append("\n---\n")

    return "\n".join(sections)


def generate_category_doc(category_name: str, rules_dir: Path, output_dir: Path) -> None:
    """Generate markdown documentation for a rule category."""
    rules_file = rules_dir / f"{category_name}.json"

    if not rules_file.exists():
        print(f"❌ Rule file not found: {rules_file}")
        return

    data = load_rule_file(rules_file)
    rules = data.get("rules", [])

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate markdown
    output_file = output_dir / f"{category_name}.md"

    with open(output_file, "w") as f:
        # Header
        f.write(f"# {category_name.replace('-', ' ').title()} Rules\n\n")
        f.write(f"**Version:** {data.get('version', 'N/A')}  \n")
        f.write(f"**Last Updated:** {data.get('lastUpdated', 'N/A')}  \n")

        if "description" in data:
            f.write(f"**Description:** {data['description']}  \n")

        f.write(f"**Rule Count:** {len(rules)}\n\n")

        # Table of contents
        f.write("## Table of Contents\n\n")
        for i, rule in enumerate(rules, 1):
            level_emoji = constraint_level_emoji(rule["level"])
            f.write(f"{i}. [{level_emoji} {rule['id']}](#{rule['id'].replace('_', '-')})\n")

        f.write("\n---\n\n")

        # Rules
        f.write("## Rules\n\n")
        for rule in rules:
            f.write(format_rule(rule))

    print(f"✅ Generated: {output_file}")


def generate_index_doc(rules_dir: Path, output_dir: Path) -> None:
    """Generate index/summary documentation."""
    index_file = rules_dir / "index.json"

    if not index_file.exists():
        print(f"❌ Index file not found: {index_file}")
        return

    index = load_rule_file(index_file)

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "INDEX.md"

    with open(output_file, "w") as f:
        f.write("# AI Steering Rules - Index\n\n")
        f.write(f"**Version:** {index.get('version', 'N/A')}  \n")
        f.write(f"**Last Updated:** {index.get('lastUpdated', 'N/A')}  \n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write(f"{index.get('description', '')}\n\n")

        # Summary
        summary = index.get("summary", {})
        f.write("## Summary\n\n")
        f.write(f"- **Total Rules:** {summary.get('totalRules', 0)}\n")
        f.write(f"- **Total Categories:** {summary.get('totalCategories', 0)}\n\n")

        # Constraint levels breakdown
        f.write("### Constraint Levels\n\n")
        levels = summary.get("constraintLevels", {})
        for level, count in levels.items():
            emoji = constraint_level_emoji(level)
            f.write(f"- {emoji} **{level}:** {count} rules\n")

        f.write("\n")

        # Categories
        f.write("## Categories\n\n")
        for cat in index.get("categories", []):
            priority_emoji = {"critical": "🔴", "high": "🟡", "medium": "🟢"}.get(cat["priority"], "⚪")
            f.write(f"### {priority_emoji} {cat['name'].replace('_', ' ').title()}\n\n")
            f.write(f"**File:** `{cat['file']}`  \n")
            f.write(f"**Rules:** {cat['ruleCount']}  \n")
            f.write(f"**Priority:** {cat['priority']}  \n")
            f.write(f"{cat['description']}\n\n")
            f.write(f"[📄 View Generated Docs](./{cat['file'].replace('.json', '.md')})\n\n")

        # Usage
        f.write("## Usage\n\n")
        for key, value in index.get("usage", {}).items():
            f.write(f"- **{key.replace('_', ' ').title()}:** {value}\n")

        f.write("\n")

        # Integration
        f.write("## Integration\n\n")
        for key, value in index.get("integration", {}).items():
            f.write(f"- **{key}:** {value}\n")

    print(f"✅ Generated: {output_file}")


def main():
    """Main entry point."""
    rules_dir = Path(__file__).parent / "rules"
    output_dir = Path(__file__).parent / "generated"

    # Check arguments
    if len(sys.argv) > 1:
        category = sys.argv[1]
        if category == "--validate":
            print("🔍 Validation not yet implemented")
            sys.exit(0)

        # Generate specific category
        generate_category_doc(category, rules_dir, output_dir)
    else:
        # Generate all
        print("📝 Generating all documentation...\n")

        # Generate index
        generate_index_doc(rules_dir, output_dir)

        # Generate category docs
        index_file = rules_dir / "index.json"
        if index_file.exists():
            index = load_rule_file(index_file)
            for cat in index.get("categories", []):
                category_name = cat["file"].replace(".json", "")
                generate_category_doc(category_name, rules_dir, output_dir)

        print(f"\n✅ All documentation generated in: {output_dir}")


if __name__ == "__main__":
    main()
