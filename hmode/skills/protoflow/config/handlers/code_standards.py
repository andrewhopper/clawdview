#!/usr/bin/env python3
"""
Code Standards Configuration Handler

Manages language-specific code standards in shared/standards/code/.
"""
# File UUID: b2c3d4e5-6f7a-8b9c-0d1e-2f3a4b5c6d7e

from pathlib import Path
from typing import Optional
import yaml

class CodeStandardsHandler:
    """Handler for code standards configuration (shared/standards/code/)."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.standards_dir = project_root / "shared" / "standards" / "code"

    def get_stats(self) -> str:
        """Get current stats for menu display."""
        if not self.standards_dir.exists():
            return "0 language standards"

        lang_dirs = [d for d in self.standards_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]
        return f"{len(lang_dirs)} language standards"

    def show_section_menu(self) -> dict:
        """Show code standards section menu."""
        # List existing standards
        standards = []
        if self.standards_dir.exists():
            for lang_dir in sorted(self.standards_dir.iterdir()):
                if lang_dir.is_dir() and not lang_dir.name.startswith("."):
                    readme = lang_dir / "README.md"
                    if readme.exists():
                        # Try to extract description from README
                        with open(readme) as f:
                            first_line = f.readline().strip()
                            desc = first_line.replace("#", "").strip()
                    else:
                        desc = "No README"

                    standards.append(f"  - {lang_dir.name}: {desc}")

        standards_display = "\n".join(standards) if standards else "  (none)"

        menu = f"""
╔══════════════════════════════════════════════════════════════╗
║         CODE STANDARDS CONFIGURATION                         ║
╚══════════════════════════════════════════════════════════════╝

Available Standards:
{standards_display}

Operations:
  [1] Add new language standard
  [2] Update existing standard
  [3] View standard details
  [4] Remove standard
  [b] Back to main menu

Select [1-4] or 'b':
"""

        return {
            "status": "awaiting_input",
            "prompt": menu,
            "section": "code-standards"
        }

    def handle_add(self, language: str, standard_name: str) -> dict:
        """Add new code standard for language."""
        lang_dir = self.standards_dir / language
        standard_file = lang_dir / f"{standard_name}.md"

        if standard_file.exists():
            return {
                "status": "error",
                "message": f"Standard already exists: {language}/{standard_name}.md"
            }

        # Show preview
        preview = f"""
Adding code standard:

  Language: {language}
  Standard: {standard_name}
  Location: shared/standards/code/{language}/{standard_name}.md

Standard will include:
  - Pattern description
  - Code examples
  - Anti-patterns to avoid
  - When to use / when not to use

Create standard? [Y/n]
"""

        return {
            "status": "awaiting_confirmation",
            "prompt": preview,
            "operation": "add_standard",
            "data": {
                "language": language,
                "standard_name": standard_name,
                "standard_file": str(standard_file)
            }
        }

    def confirm_add_standard(self, data: dict) -> dict:
        """Execute standard addition."""
        from datetime import datetime

        standard_file = Path(data["standard_file"])
        language = data["language"]
        standard_name = data["standard_name"]

        # Create standard template
        standard_content = f"""# {standard_name}

**Language:** {language}
**Created:** {datetime.now().strftime('%Y-%m-%d')}

## Overview

Brief description of this code standard.

## When to Use

- Scenario 1
- Scenario 2

## When NOT to Use

- Anti-pattern 1
- Anti-pattern 2

## Pattern

```{language}
// Example code following this standard
```

## Anti-Patterns

```{language}
// Example of what NOT to do
```

## Examples

### Example 1: Basic Usage

```{language}
// Code example
```

### Example 2: Advanced Usage

```{language}
// Code example
```

## Related Standards

- Link to related standard 1
- Link to related standard 2

## References

- External reference 1
- External reference 2
"""

        # Write standard file
        standard_file.parent.mkdir(parents=True, exist_ok=True)
        with open(standard_file, "w") as f:
            f.write(standard_content)

        # Update README if it doesn't exist
        readme = standard_file.parent / "README.md"
        if not readme.exists():
            readme_content = f"""# {language.title()} Code Standards

Standards and patterns for {language} development.

## Standards

- [{standard_name}](./{standard_name}.md)

## Usage

These standards are automatically applied when writing {language} code in this monorepo.
"""
            with open(readme, "w") as f:
                f.write(readme_content)

        return {
            "status": "success",
            "message": f"Added code standard: {language}/{standard_name}",
            "file": str(standard_file)
        }

    def handle_update(self, language: str, standard_name: str) -> dict:
        """Update existing code standard."""
        lang_dir = self.standards_dir / language
        standard_file = lang_dir / f"{standard_name}.md"

        if not standard_file.exists():
            return {
                "status": "error",
                "message": f"Standard not found: {language}/{standard_name}.md"
            }

        menu = f"""
Update code standard: {language}/{standard_name}

Current file: {standard_file}

Update options:
  [1] Edit pattern section
  [2] Add example
  [3] Add anti-pattern
  [4] Update overview
  [5] Full rewrite
  [c] Cancel

Select [1-5] or 'c':
"""

        return {
            "status": "awaiting_input",
            "prompt": menu,
            "operation": "update_standard_section",
            "data": {
                "language": language,
                "standard_name": standard_name,
                "standard_file": str(standard_file)
            }
        }

    def handle_view(self, language: str) -> dict:
        """View all standards for a language."""
        lang_dir = self.standards_dir / language

        if not lang_dir.exists():
            return {
                "status": "error",
                "message": f"No standards found for language: {language}"
            }

        standards = [f.stem for f in lang_dir.glob("*.md") if f.name != "README.md"]

        if not standards:
            return {
                "status": "success",
                "message": f"No standards defined for {language}",
                "standards": []
            }

        output = [f"Code Standards for {language}:\n"]
        for standard in standards:
            standard_file = lang_dir / f"{standard}.md"
            with open(standard_file) as f:
                # Extract first line as description
                first_line = f.readline().strip().replace("#", "").strip()
                output.append(f"  - {standard}: {first_line}")

        return {
            "status": "success",
            "message": "\n".join(output),
            "standards": standards
        }
