#!/usr/bin/env python3
"""
Golden Repos Configuration Handler

Manages project templates in shared/golden-repos/.
MEDIUM protection level - should verify structure before adding.
"""
# File UUID: e8f1a3b5-4c7d-4e9a-9f2b-3d6c8e9f1a2b

from pathlib import Path
from typing import Optional
import yaml
from datetime import datetime

class GoldenReposHandler:
    """Handler for golden repo templates (shared/golden-repos/)."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.golden_repos_dir = project_root / "shared" / "golden-repos"

    def get_stats(self) -> str:
        """Get current stats for menu display."""
        if not self.golden_repos_dir.exists():
            return "0 templates"

        templates = [d for d in self.golden_repos_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]
        return f"{len(templates)} templates available"

    def show_section_menu(self) -> dict:
        """Show golden repos section menu."""
        # List existing templates
        templates = []
        if self.golden_repos_dir.exists():
            for template_dir in sorted(self.golden_repos_dir.iterdir()):
                if template_dir.is_dir() and not template_dir.name.startswith("."):
                    # Try to read metadata
                    metadata_file = template_dir / ".template-metadata.yaml"
                    if metadata_file.exists():
                        with open(metadata_file) as f:
                            metadata = yaml.safe_load(f)
                            desc = metadata.get("description", "No description")
                    else:
                        desc = "No metadata"

                    templates.append(f"  - {template_dir.name}: {desc}")

        templates_display = "\n".join(templates) if templates else "  (none)"

        menu = f"""
╔══════════════════════════════════════════════════════════════╗
║         GOLDEN REPO TEMPLATES                                ║
╚══════════════════════════════════════════════════════════════╝

Current Templates:
{templates_display}

Operations:
  [1] Add new template
  [2] Update existing template
  [3] View template details
  [4] Remove template
  [5] Search GitHub for exemplar
  [b] Back to main menu

Select [1-5] or 'b':
"""

        return {
            "status": "awaiting_input",
            "prompt": menu,
            "section": "golden-repos"
        }

    def handle_add(self, template_name: str) -> dict:
        """Add new golden repo template."""
        template_dir = self.golden_repos_dir / template_name

        if template_dir.exists():
            return {
                "status": "error",
                "message": f"Template already exists: {template_name}"
            }

        # Determine template type from name
        tech_stack = self._infer_tech_stack(template_name)

        # Show preview and options
        preview = f"""
Adding new golden repo template:

  Name: {template_name}
  Location: shared/golden-repos/{template_name}/
  Inferred tech: {tech_stack}

Options:
  [1] Search GitHub for exemplar (recommended)
  [2] Create from scratch with standard structure
  [3] Copy from existing template
  [c] Cancel

Select [1-3] or 'c':
"""

        return {
            "status": "awaiting_input",
            "prompt": preview,
            "operation": "add_template_source",
            "data": {
                "template_name": template_name,
                "template_dir": str(template_dir),
                "tech_stack": tech_stack
            }
        }

    def _infer_tech_stack(self, template_name: str) -> str:
        """Infer technology stack from template name."""
        name_lower = template_name.lower()

        if "python" in name_lower:
            if "fastapi" in name_lower:
                return "Python, FastAPI, Pydantic"
            elif "cli" in name_lower:
                return "Python, Click, Rich"
            else:
                return "Python"
        elif "typescript" in name_lower or "ts" in name_lower:
            if "nextjs" in name_lower or "next" in name_lower:
                return "TypeScript, Next.js, React"
            elif "react" in name_lower:
                return "TypeScript, React, Vite"
            elif "cdk" in name_lower:
                return "TypeScript, AWS CDK"
            elif "expo" in name_lower:
                return "TypeScript, Expo, React Native"
            else:
                return "TypeScript"
        elif "react" in name_lower:
            return "React, TypeScript"
        elif "vite" in name_lower:
            return "Vite, TypeScript"
        else:
            return "Unknown (will prompt)"

    def handle_add_from_github(self, template_name: str, github_url: str) -> dict:
        """Add template by cloning from GitHub exemplar."""
        template_dir = self.golden_repos_dir / template_name

        # Show preview and request confirmation
        preview = f"""
Adding template from GitHub exemplar:

  Template: {template_name}
  Source: {github_url}
  Location: shared/golden-repos/{template_name}/

Steps:
  1. Clone repository
  2. Remove git history
  3. Create .template-metadata.yaml
  4. Add README with usage instructions

Proceed? [Y/n]
"""

        return {
            "status": "awaiting_confirmation",
            "prompt": preview,
            "operation": "add_from_github",
            "data": {
                "template_name": template_name,
                "template_dir": str(template_dir),
                "github_url": github_url
            }
        }

    def confirm_add_from_github(self, data: dict) -> dict:
        """Execute GitHub template addition."""
        import subprocess

        template_dir = Path(data["template_dir"])
        github_url = data["github_url"]
        template_name = data["template_name"]

        # Create directory
        template_dir.parent.mkdir(parents=True, exist_ok=True)

        # Clone repository
        try:
            subprocess.run(
                ["git", "clone", github_url, str(template_dir)],
                check=True,
                capture_output=True
            )
        except subprocess.CalledProcessError as e:
            return {
                "status": "error",
                "message": f"Failed to clone repository: {e.stderr.decode()}"
            }

        # Remove .git directory
        import shutil
        git_dir = template_dir / ".git"
        if git_dir.exists():
            shutil.rmtree(git_dir)

        # Create metadata file
        metadata = {
            "name": template_name,
            "source": github_url,
            "added_date": datetime.now().isoformat(),
            "description": f"Template cloned from {github_url}",
            "tech_stack": self._infer_tech_stack(template_name),
        }

        metadata_file = template_dir / ".template-metadata.yaml"
        with open(metadata_file, "w") as f:
            yaml.dump(metadata, f, default_flow_style=False)

        return {
            "status": "success",
            "message": f"Added template '{template_name}' from GitHub",
            "location": str(template_dir)
        }

    def handle_add_from_scratch(self, template_name: str, tech_stack: str) -> dict:
        """Create template from scratch with standard structure."""
        template_dir = self.golden_repos_dir / template_name

        # Define standard structure based on tech stack
        structure = self._get_standard_structure(tech_stack)

        # Show preview
        structure_display = "\n".join(f"  {path}" for path in structure)

        preview = f"""
Creating template from scratch:

  Template: {template_name}
  Tech Stack: {tech_stack}
  Location: shared/golden-repos/{template_name}/

Standard Structure:
{structure_display}

Proceed? [Y/n]
"""

        return {
            "status": "awaiting_confirmation",
            "prompt": preview,
            "operation": "add_from_scratch",
            "data": {
                "template_name": template_name,
                "template_dir": str(template_dir),
                "tech_stack": tech_stack,
                "structure": structure
            }
        }

    def _get_standard_structure(self, tech_stack: str) -> list[str]:
        """Get standard directory structure for tech stack."""
        common = [
            "README.md",
            ".template-metadata.yaml",
            ".gitignore",
        ]

        if "python" in tech_stack.lower():
            return common + [
                "src/",
                "tests/",
                "pyproject.toml",
                "requirements.txt",
            ]
        elif "typescript" in tech_stack.lower():
            return common + [
                "src/",
                "tests/",
                "package.json",
                "tsconfig.json",
            ]
        else:
            return common + [
                "src/",
                "tests/",
            ]

    def confirm_add_from_scratch(self, data: dict) -> dict:
        """Execute from-scratch template creation."""
        template_dir = Path(data["template_dir"])
        template_name = data["template_name"]
        tech_stack = data["tech_stack"]
        structure = data["structure"]

        # Create directory structure
        template_dir.mkdir(parents=True, exist_ok=True)

        for path in structure:
            full_path = template_dir / path
            if path.endswith("/"):
                full_path.mkdir(exist_ok=True)
            else:
                full_path.parent.mkdir(parents=True, exist_ok=True)
                if not full_path.exists():
                    full_path.touch()

        # Create metadata
        metadata = {
            "name": template_name,
            "source": "created from scratch",
            "added_date": datetime.now().isoformat(),
            "description": f"Standard {tech_stack} template",
            "tech_stack": tech_stack,
        }

        metadata_file = template_dir / ".template-metadata.yaml"
        with open(metadata_file, "w") as f:
            yaml.dump(metadata, f, default_flow_style=False)

        # Create README
        readme = f"""# {template_name}

Template for {tech_stack} projects.

## Structure

{chr(10).join('- ' + path for path in structure)}

## Usage

1. Copy this template to your project location
2. Update package.json / pyproject.toml with your project details
3. Remove .template-metadata.yaml
4. Initialize git repository
"""

        readme_file = template_dir / "README.md"
        with open(readme_file, "w") as f:
            f.write(readme)

        return {
            "status": "success",
            "message": f"Created template '{template_name}' from scratch",
            "location": str(template_dir)
        }

    def handle_update(self, template_name: str) -> dict:
        """Update existing template."""
        template_dir = self.golden_repos_dir / template_name

        if not template_dir.exists():
            return {
                "status": "error",
                "message": f"Template not found: {template_name}"
            }

        # Read current metadata
        metadata_file = template_dir / ".template-metadata.yaml"
        if metadata_file.exists():
            with open(metadata_file) as f:
                metadata = yaml.safe_load(f)
        else:
            metadata = {}

        menu = f"""
Update template: {template_name}

Current metadata:
  Source: {metadata.get('source', 'unknown')}
  Tech Stack: {metadata.get('tech_stack', 'unknown')}
  Description: {metadata.get('description', 'none')}

Update options:
  [1] Update from GitHub (if sourced from GitHub)
  [2] Update metadata
  [3] Update structure
  [c] Cancel

Select [1-3] or 'c':
"""

        return {
            "status": "awaiting_input",
            "prompt": menu,
            "operation": "update_template",
            "data": {
                "template_name": template_name,
                "template_dir": str(template_dir),
                "metadata": metadata
            }
        }
