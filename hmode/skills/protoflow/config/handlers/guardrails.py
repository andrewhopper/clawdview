#!/usr/bin/env python3
"""
Guardrails Configuration Handler

Manages tech preferences, architecture preferences, and AI steering rules.
HIGH protection level - requires explicit approval for all changes.
"""
# File UUID: d7e9f2a4-3b6c-4d8e-9f1a-2c5d7e8f9b0c

from pathlib import Path
from typing import Optional, Literal
import yaml
from datetime import datetime

SteeringLevel = Literal["NEVER", "ALWAYS", "MUST", "SHOULD"]

class GuardrailsHandler:
    """Handler for guardrails configuration (hmode/guardrails/)."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.guardrails_dir = project_root / "hmode" / "guardrails"
        self.tech_prefs_dir = self.guardrails_dir / "tech-preferences"
        self.arch_prefs_dir = self.guardrails_dir / "architecture-preferences"
        self.ai_steering_dir = self.guardrails_dir / "ai-steering"

    def get_stats(self) -> str:
        """Get current stats for menu display."""
        tech_count = len(list(self.tech_prefs_dir.glob("*.yaml")))
        arch_count = len(list(self.arch_prefs_dir.glob("*.yaml")))
        steering_count = len(list(self.ai_steering_dir.glob("*.yaml")))

        return f"{tech_count} tech categories, {arch_count} arch patterns, {steering_count} steering rules"

    def show_section_menu(self) -> dict:
        """Show guardrails section menu."""
        tech_categories = [f.stem for f in self.tech_prefs_dir.glob("*.yaml")]
        arch_patterns = [f.stem for f in self.arch_prefs_dir.glob("*.yaml")]

        menu = f"""
╔══════════════════════════════════════════════════════════════╗
║         GUARDRAILS CONFIGURATION                             ║
╚══════════════════════════════════════════════════════════════╝

⚠️  HIGH PROTECTION LEVEL - All changes require approval

Current Configuration:
  Tech Categories: {', '.join(tech_categories)}
  Arch Patterns: {', '.join(arch_patterns)}

Operations:
  [1] Add approved technology
  [2] Remove approved technology
  [3] Add architecture pattern
  [4] Add AI steering rule
  [5] View current tech preferences
  [6] View current arch preferences
  [7] View AI steering rules
  [b] Back to main menu

Select [1-7] or 'b':
"""

        return {
            "status": "awaiting_input",
            "prompt": menu,
            "section": "guardrails"
        }

    def handle_add_tech(self, tech_name: str, category: str) -> dict:
        """Add approved technology to guardrails."""
        category_file = self.tech_prefs_dir / f"{category}.yaml"

        # Load existing preferences or create new
        if category_file.exists():
            with open(category_file) as f:
                prefs = yaml.safe_load(f) or {}
        else:
            prefs = {
                "category": category,
                "technologies": []
            }

        # Check if already exists
        existing = [t for t in prefs.get("technologies", []) if t["name"].lower() == tech_name.lower()]
        if existing:
            return {
                "status": "error",
                "message": f"{tech_name} already approved in {category}"
            }

        # Prepare new entry
        new_tech = {
            "name": tech_name,
            "status": "approved",
            "added_date": datetime.now().isoformat(),
            "notes": f"Auto-approved {tech_name} for {category}"
        }

        # Show preview and request confirmation
        preview = f"""
Adding technology to guardrails:

  File: hmode/guardrails/tech-preferences/{category}.yaml
  Technology: {tech_name}
  Status: approved
  Category: {category}

This will make {tech_name} auto-approved for all future projects.

⚠️  CONFIRMATION REQUIRED - This modifies protected guardrails.

Proceed? [Y/n]
"""

        return {
            "status": "awaiting_confirmation",
            "prompt": preview,
            "operation": "add_tech",
            "data": {
                "category_file": str(category_file),
                "new_tech": new_tech,
                "preferences": prefs
            }
        }

    def confirm_add_tech(self, data: dict) -> dict:
        """Execute approved tech addition."""
        category_file = Path(data["category_file"])
        new_tech = data["new_tech"]
        prefs = data["preferences"]

        # Add to technologies list
        if "technologies" not in prefs:
            prefs["technologies"] = []
        prefs["technologies"].append(new_tech)

        # Sort by name
        prefs["technologies"] = sorted(prefs["technologies"], key=lambda t: t["name"])

        # Write back
        category_file.parent.mkdir(parents=True, exist_ok=True)
        with open(category_file, "w") as f:
            yaml.dump(prefs, f, default_flow_style=False, sort_keys=False)

        return {
            "status": "success",
            "message": f"Added {new_tech['name']} to {prefs['category']} guardrails",
            "file": str(category_file)
        }

    def handle_remove_tech(self, tech_name: str, category: str) -> dict:
        """Remove technology from guardrails."""
        category_file = self.tech_prefs_dir / f"{category}.yaml"

        if not category_file.exists():
            return {
                "status": "error",
                "message": f"Category file not found: {category}.yaml"
            }

        # Load preferences
        with open(category_file) as f:
            prefs = yaml.safe_load(f) or {}

        # Find technology
        technologies = prefs.get("technologies", [])
        tech = next((t for t in technologies if t["name"].lower() == tech_name.lower()), None)

        if not tech:
            return {
                "status": "error",
                "message": f"{tech_name} not found in {category}"
            }

        # Show preview and request confirmation
        preview = f"""
Removing technology from guardrails:

  File: hmode/guardrails/tech-preferences/{category}.yaml
  Technology: {tech_name}
  Category: {category}

This will REMOVE auto-approval for {tech_name}.
Future uses will require explicit approval.

⚠️  CONFIRMATION REQUIRED - This modifies protected guardrails.

Proceed? [Y/n]
"""

        return {
            "status": "awaiting_confirmation",
            "prompt": preview,
            "operation": "remove_tech",
            "data": {
                "category_file": str(category_file),
                "tech_name": tech_name,
                "preferences": prefs
            }
        }

    def confirm_remove_tech(self, data: dict) -> dict:
        """Execute approved tech removal."""
        category_file = Path(data["category_file"])
        tech_name = data["tech_name"]
        prefs = data["preferences"]

        # Remove from technologies list
        prefs["technologies"] = [
            t for t in prefs.get("technologies", [])
            if t["name"].lower() != tech_name.lower()
        ]

        # Write back
        with open(category_file, "w") as f:
            yaml.dump(prefs, f, default_flow_style=False, sort_keys=False)

        return {
            "status": "success",
            "message": f"Removed {tech_name} from {prefs['category']} guardrails",
            "file": str(category_file)
        }

    def handle_add_arch_pattern(self, *pattern_args: str) -> dict:
        """Add architecture pattern to guardrails."""
        pattern_name = " ".join(pattern_args)
        pattern_slug = pattern_name.lower().replace(" ", "-")
        pattern_file = self.arch_prefs_dir / f"{pattern_slug}.yaml"

        if pattern_file.exists():
            return {
                "status": "error",
                "message": f"Pattern already exists: {pattern_slug}.yaml"
            }

        # Prepare new pattern
        new_pattern = {
            "name": pattern_name,
            "status": "approved",
            "added_date": datetime.now().isoformat(),
            "description": f"Approved architecture pattern: {pattern_name}",
            "use_cases": [],
            "constraints": []
        }

        # Show preview and request confirmation
        preview = f"""
Adding architecture pattern to guardrails:

  File: hmode/guardrails/architecture-preferences/{pattern_slug}.yaml
  Pattern: {pattern_name}
  Status: approved

This will make '{pattern_name}' auto-approved for all projects.

⚠️  CONFIRMATION REQUIRED - This modifies protected guardrails.

Proceed? [Y/n]
"""

        return {
            "status": "awaiting_confirmation",
            "prompt": preview,
            "operation": "add_arch_pattern",
            "data": {
                "pattern_file": str(pattern_file),
                "pattern": new_pattern
            }
        }

    def confirm_add_arch_pattern(self, data: dict) -> dict:
        """Execute approved arch pattern addition."""
        pattern_file = Path(data["pattern_file"])
        pattern = data["pattern"]

        # Write pattern file
        pattern_file.parent.mkdir(parents=True, exist_ok=True)
        with open(pattern_file, "w") as f:
            yaml.dump(pattern, f, default_flow_style=False, sort_keys=False)

        return {
            "status": "success",
            "message": f"Added architecture pattern: {pattern['name']}",
            "file": str(pattern_file)
        }

    def handle_add_steering_rule(self, *rule_args: str) -> dict:
        """Add AI steering rule to guardrails."""
        # Parse rule: level, category, rule_text
        # Example: NEVER use-tech "raw SQL queries without parameterization"
        if len(rule_args) < 3:
            return {
                "status": "error",
                "message": "Usage: /config --add-steering-rule <LEVEL> <category> <rule_text>"
            }

        level = rule_args[0].upper()
        category = rule_args[1]
        rule_text = " ".join(rule_args[2:])

        if level not in ["NEVER", "ALWAYS", "MUST", "SHOULD"]:
            return {
                "status": "error",
                "message": f"Invalid level: {level}. Must be NEVER, ALWAYS, MUST, or SHOULD"
            }

        category_file = self.ai_steering_dir / f"{category}.yaml"

        # Load existing rules or create new
        if category_file.exists():
            with open(category_file) as f:
                rules = yaml.safe_load(f) or {}
        else:
            rules = {
                "category": category,
                "rules": []
            }

        # Prepare new rule
        new_rule = {
            "level": level,
            "rule": rule_text,
            "added_date": datetime.now().isoformat()
        }

        # Show preview and request confirmation
        preview = f"""
Adding AI steering rule to guardrails:

  File: hmode/guardrails/ai-steering/{category}.yaml
  Level: {level}
  Rule: {rule_text}

Enforcement:
  NEVER  → Absolute prohibition, cannot proceed
  ALWAYS → Absolute requirement, cannot skip
  MUST   → Required unless exception
  SHOULD → Recommended (warning only)

⚠️  CONFIRMATION REQUIRED - This modifies protected guardrails.

Proceed? [Y/n]
"""

        return {
            "status": "awaiting_confirmation",
            "prompt": preview,
            "operation": "add_steering_rule",
            "data": {
                "category_file": str(category_file),
                "new_rule": new_rule,
                "rules": rules
            }
        }

    def confirm_add_steering_rule(self, data: dict) -> dict:
        """Execute approved steering rule addition."""
        category_file = Path(data["category_file"])
        new_rule = data["new_rule"]
        rules = data["rules"]

        # Add to rules list
        if "rules" not in rules:
            rules["rules"] = []
        rules["rules"].append(new_rule)

        # Write back
        category_file.parent.mkdir(parents=True, exist_ok=True)
        with open(category_file, "w") as f:
            yaml.dump(rules, f, default_flow_style=False, sort_keys=False)

        return {
            "status": "success",
            "message": f"Added {new_rule['level']} steering rule to {rules['category']}",
            "file": str(category_file)
        }
