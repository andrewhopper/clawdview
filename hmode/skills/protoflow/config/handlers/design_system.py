#!/usr/bin/env python3
"""
Design System Configuration Handler

Manages design tokens, UI components, and guidelines in shared/design-system/.
MEDIUM protection level - must maintain consistency with existing system.
"""
# File UUID: f9a2b4c6-5d8e-4f1a-9c3b-4e7d9f1a2c3d

from pathlib import Path
from typing import Optional, Literal
import re
from datetime import datetime

AtomicLevel = Literal["atom", "molecule", "organism", "template", "page"]

class DesignSystemHandler:
    """Handler for design system configuration (shared/design-system/)."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.design_system_dir = project_root / "shared" / "design-system"
        self.globals_css = self.design_system_dir / "globals.css"
        self.atoms_dir = self.design_system_dir / "atoms"
        self.molecules_dir = self.design_system_dir / "molecules"
        self.organisms_dir = self.design_system_dir / "organisms"
        self.templates_dir = self.design_system_dir / "templates"

    def get_stats(self) -> str:
        """Get current stats for menu display."""
        if not self.design_system_dir.exists():
            return "Design system not initialized"

        # Count tokens in globals.css
        token_count = 0
        if self.globals_css.exists():
            with open(self.globals_css) as f:
                content = f.read()
                token_count = len(re.findall(r'--[\w-]+:', content))

        # Count components
        atom_count = len(list(self.atoms_dir.glob("*"))) if self.atoms_dir.exists() else 0
        molecule_count = len(list(self.molecules_dir.glob("*"))) if self.molecules_dir.exists() else 0
        organism_count = len(list(self.organisms_dir.glob("*"))) if self.organisms_dir.exists() else 0

        return f"{token_count} tokens, {atom_count} atoms, {molecule_count} molecules, {organism_count} organisms"

    def show_section_menu(self) -> dict:
        """Show design system section menu."""
        stats = self.get_stats()

        menu = f"""
╔══════════════════════════════════════════════════════════════╗
║         DESIGN SYSTEM CONFIGURATION                          ║
╚══════════════════════════════════════════════════════════════╝

Current Status: {stats}

Operations:
  [1] Add color token
  [2] Add spacing token
  [3] Add typography token
  [4] Add component (atom/molecule/organism)
  [5] View current tokens
  [6] Update guidelines
  [7] Validate compliance
  [b] Back to main menu

Select [1-7] or 'b':
"""

        return {
            "status": "awaiting_input",
            "prompt": menu,
            "section": "design-system"
        }

    def handle_add_color(self, color_name: str) -> dict:
        """Add color token to design system."""
        if not self.globals_css.exists():
            return {
                "status": "error",
                "message": "globals.css not found. Initialize design system first."
            }

        # Read current globals.css
        with open(self.globals_css) as f:
            content = f.read()

        # Check if color already exists
        if f"--{color_name}:" in content:
            return {
                "status": "error",
                "message": f"Color token '--{color_name}' already exists"
            }

        # Get suggested HSL values based on color name
        suggested_hsl = self._suggest_hsl_for_color(color_name)

        # Show preview
        preview = f"""
Adding color token to design system:

  Token: --{color_name}
  Suggested HSL: {suggested_hsl}
  Foreground: --{color_name}-foreground

Location: shared/design-system/globals.css

Example usage:
  ❌ NEVER: background-color: #22c55e
  ✅ ALWAYS: background-color: hsl(var(--{color_name}))

Preview:
  :root {{
    --{color_name}: {suggested_hsl};
    --{color_name}-foreground: 0 0% 100%;
  }}

Adjust HSL values? [Y/n/custom]
"""

        return {
            "status": "awaiting_input",
            "prompt": preview,
            "operation": "add_color_confirm",
            "data": {
                "color_name": color_name,
                "suggested_hsl": suggested_hsl
            }
        }

    def _suggest_hsl_for_color(self, color_name: str) -> str:
        """Suggest HSL values based on color name."""
        color_map = {
            "success": "142 76% 36%",  # Green
            "error": "0 72% 51%",      # Red
            "warning": "38 92% 50%",   # Orange
            "info": "199 89% 48%",     # Blue
            "purple": "262 52% 47%",   # Purple
            "pink": "330 81% 60%",     # Pink
            "teal": "173 58% 39%",     # Teal
        }

        return color_map.get(color_name.lower(), "0 0% 50%")  # Default gray

    def confirm_add_color(self, color_name: str, hsl_value: str) -> dict:
        """Execute color token addition."""
        # Read current globals.css
        with open(self.globals_css) as f:
            content = f.read()

        # Find :root section and add tokens
        root_pattern = r'(:root\s*\{)'
        new_tokens = f"""
    --{color_name}: {hsl_value};
    --{color_name}-foreground: 0 0% 100%;"""

        # Insert after :root {
        updated_content = re.sub(
            root_pattern,
            r'\1' + new_tokens,
            content,
            count=1
        )

        # Write back
        with open(self.globals_css, "w") as f:
            f.write(updated_content)

        return {
            "status": "success",
            "message": f"Added color token '--{color_name}'",
            "file": str(self.globals_css),
            "usage": f"hsl(var(--{color_name}))"
        }

    def handle_add_component(self, component_name: str, atomic_level: AtomicLevel) -> dict:
        """Add UI component to design system."""
        # Determine target directory
        level_dirs = {
            "atom": self.atoms_dir,
            "molecule": self.molecules_dir,
            "organism": self.organisms_dir,
        }

        if atomic_level not in level_dirs:
            return {
                "status": "error",
                "message": f"Invalid atomic level. Must be: atom, molecule, or organism"
            }

        target_dir = level_dirs[atomic_level]
        component_file = target_dir / f"{component_name}.html"

        if component_file.exists():
            return {
                "status": "error",
                "message": f"Component already exists: {component_name}.html"
            }

        # Generate component UUID
        import uuid
        component_uuid = str(uuid.uuid4())[:8]

        # Show preview
        preview = f"""
Adding UI component to design system:

  Name: {component_name}
  Atomic Level: {atomic_level}
  UUID: {component_uuid}
  Location: shared/design-system/{atomic_level}s/{component_name}.html

Component will include:
  - Metadata header (UUID, atomic level, tokens used)
  - Design token usage (NO raw hex colors)
  - Accessibility attributes
  - Responsive design

Create component? [Y/n]
"""

        return {
            "status": "awaiting_confirmation",
            "prompt": preview,
            "operation": "add_component",
            "data": {
                "component_name": component_name,
                "atomic_level": atomic_level,
                "component_uuid": component_uuid,
                "component_file": str(component_file)
            }
        }

    def confirm_add_component(self, data: dict) -> dict:
        """Execute component addition."""
        component_file = Path(data["component_file"])
        component_name = data["component_name"]
        atomic_level = data["atomic_level"]
        component_uuid = data["component_uuid"]

        # Create component template
        component_content = f"""<!--
  Component: {component_name}
  Asset ID: {component_uuid}
  Date: {datetime.now().strftime('%Y-%m-%d')}
  Design System: shared/design-system

  Atomic Level: {atomic_level}

  Tokens Used:
  - Colors: --background, --foreground, --primary
  - Spacing: (list spacing tokens used)
  - Typography: (list typography tokens used)
-->

<div class="{component_name}" style="
  background-color: hsl(var(--background));
  color: hsl(var(--foreground));
  padding: var(--space-4);
">
  <!-- Component content here -->
  <p>Placeholder for {component_name}</p>
</div>

<style>
.{component_name} {{
  /* Add component-specific styles */
  /* Use design tokens for all values */
}}
</style>
"""

        # Write component file
        component_file.parent.mkdir(parents=True, exist_ok=True)
        with open(component_file, "w") as f:
            f.write(component_content)

        return {
            "status": "success",
            "message": f"Added {atomic_level} component: {component_name}",
            "file": str(component_file),
            "uuid": component_uuid
        }

    def handle_update_guidelines(self) -> dict:
        """Update design system guidelines."""
        guidelines_file = self.design_system_dir / "MANAGEMENT_GUIDELINES.md"

        if not guidelines_file.exists():
            return {
                "status": "error",
                "message": "MANAGEMENT_GUIDELINES.md not found"
            }

        menu = f"""
Update Design System Guidelines:

Current file: {guidelines_file}

Update sections:
  [1] Token usage rules
  [2] Component creation standards
  [3] Atomic design classification
  [4] Validation checklist
  [5] Full rewrite
  [c] Cancel

Select [1-5] or 'c':
"""

        return {
            "status": "awaiting_input",
            "prompt": menu,
            "operation": "update_guidelines_section",
            "data": {
                "guidelines_file": str(guidelines_file)
            }
        }

    def validate_compliance(self, file_path: str) -> dict:
        """Validate file compliance with design system."""
        target_file = Path(file_path)

        if not target_file.exists():
            return {
                "status": "error",
                "message": f"File not found: {file_path}"
            }

        with open(target_file) as f:
            content = f.read()

        violations = []

        # Check for raw hex colors
        hex_pattern = r'#[0-9a-fA-F]{3,6}'
        hex_matches = re.findall(hex_pattern, content)
        if hex_matches:
            violations.append(f"❌ Raw hex colors found: {', '.join(set(hex_matches))}")

        # Check for magic numbers in padding/margin
        magic_number_pattern = r'(?:padding|margin):\s*(\d+)px'
        magic_matches = re.findall(magic_number_pattern, content)
        if magic_matches:
            violations.append(f"❌ Magic number spacing: {', '.join(set(magic_matches))}px")

        # Check for metadata header
        if "Asset ID:" not in content:
            violations.append("❌ Missing metadata header (Asset ID)")

        # Check for design token usage
        if "hsl(var(--" not in content and "var(--" not in content:
            violations.append("⚠️  No design token usage detected")

        # Generate report
        if violations:
            report = f"""
Design System Compliance Report
File: {file_path}

Violations Found:
{chr(10).join(violations)}

Recommendations:
  - Replace hex colors with hsl(var(--token))
  - Use spacing tokens (--space-4, --space-6, etc.)
  - Add metadata header with Asset ID
  - Use design tokens for all colors, spacing, typography
"""
            status = "violations_found"
        else:
            report = f"""
Design System Compliance Report
File: {file_path}

✅ No violations found
✅ Design token usage detected
✅ Metadata header present

Status: COMPLIANT
"""
            status = "compliant"

        return {
            "status": status,
            "report": report,
            "violations": violations
        }
