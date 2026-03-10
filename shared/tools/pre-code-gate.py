#!/usr/bin/env python3
"""
Pre-Code Gate Enforcement

Checks if all required artifacts exist before allowing code to be written.
Enforces: Requirements → Mockups → Data Model → Code sequence.
"""
# File UUID: 1f3a5c7e-9b2d-4f6a-8c0e-3d5f7a9b1c2d

import sys
import yaml
from pathlib import Path
from typing import Tuple, List, Dict, Any
from datetime import datetime
import argparse


class PreCodeGate:
    """Enforce requirements → mockups → data model → code sequence."""

    def __init__(self, project_path: Path):
        """Initialize with project directory."""
        self.project_path = project_path
        self.project_file = project_path / '.project'
        self.missing_artifacts: List[str] = []
        self.found_artifacts: Dict[str, str] = {}

    def check(self) -> Tuple[bool, List[str], Dict[str, Any]]:
        """
        Check if code writing is allowed.

        Returns:
            (can_proceed, missing_artifacts, details)
        """
        details = {
            'phase': None,
            'phase_name': None,
            'requirements': None,
            'mockups': [],
            'data_model': None,
            'spike_mode': False
        }

        # 1. Check if .project exists
        if not self.project_file.exists():
            return (False, [".project file not found"], details)

        # 2. Load project config
        try:
            with open(self.project_file) as f:
                project_data = yaml.safe_load(f)
        except Exception as e:
            return (False, [f"Failed to parse .project: {e}"], details)

        # 3. Check phase
        phase = project_data.get('phase', 1)
        phase_name = project_data.get('phase_name', 'SEED')
        details['phase'] = phase
        details['phase_name'] = phase_name

        # Check if SPIKE mode
        project_type = project_data.get('project_type', 'prototype')
        spike_mode = project_data.get('spike_mode', False)
        details['spike_mode'] = spike_mode

        if spike_mode:
            # SPIKE mode - bypass gate
            return (True, [], details)

        if phase < 8:
            self.missing_artifacts.append(
                f"Phase {phase} ({phase_name}) - code allowed in Phase 8+"
            )

        # 4. Check requirements document
        req_found = self._check_requirements()
        if req_found:
            details['requirements'] = req_found
        else:
            self.missing_artifacts.append("Requirements document")

        # 5. Check mockups
        mockups = self._check_mockups()
        if mockups:
            details['mockups'] = mockups
        else:
            self.missing_artifacts.append("Low-fidelity mockups")

        # 6. Check data model
        data_model = self._check_data_model(project_data)
        if data_model:
            details['data_model'] = data_model
        else:
            self.missing_artifacts.append("Data model definition")

        can_proceed = len(self.missing_artifacts) == 0
        return (can_proceed, self.missing_artifacts, details)

    def _check_requirements(self) -> str | None:
        """Check for requirements document."""
        candidates = [
            self.project_path / 'REQUIREMENTS.md',
            self.project_path / 'requirements.md',
            self.project_path / 'docs' / 'requirements.md',
            self.project_path / 'docs' / 'REQUIREMENTS.md',
        ]

        # Check if requirements/ directory exists with any .md files
        req_dir = self.project_path / 'requirements'
        if req_dir.exists() and req_dir.is_dir():
            md_files = list(req_dir.glob('*.md'))
            if md_files:
                return str(md_files[0].relative_to(self.project_path))

        for candidate in candidates:
            if candidate.exists():
                return str(candidate.relative_to(self.project_path))

        return None

    def _check_mockups(self) -> List[str]:
        """Check for mockup files."""
        mockup_files = []

        mockup_dirs = [
            self.project_path / 'mockups',
            self.project_path / 'docs' / 'mockups',
            self.project_path / 'design',
            self.project_path / 'wireframes',
        ]

        for mockup_dir in mockup_dirs:
            if mockup_dir.exists() and mockup_dir.is_dir():
                # Look for HTML, PNG, JPG, SVG files
                patterns = ['*.html', '*.png', '*.jpg', '*.jpeg', '*.svg']
                for pattern in patterns:
                    for file in mockup_dir.glob(pattern):
                        mockup_files.append(
                            str(file.relative_to(self.project_path))
                        )

        return mockup_files

    def _check_data_model(self, project_data: Dict[str, Any]) -> str | None:
        """Check for data model definition."""
        # 1. Check for local data model files
        model_candidates = [
            self.project_path / 'data-model.yaml',
            self.project_path / 'models',
            self.project_path / 'docs' / 'data-model.yaml',
        ]

        for candidate in model_candidates:
            if candidate.exists():
                if candidate.is_file():
                    return str(candidate.relative_to(self.project_path))
                elif candidate.is_dir():
                    yaml_files = list(candidate.glob('*.yaml')) + \
                                list(candidate.glob('*.yml'))
                    if yaml_files:
                        return str(candidate.relative_to(self.project_path))

        # 2. Check if project references semantic domains
        domains = project_data.get('domains', [])
        if domains:
            # Verify domains exist
            semantic_path = Path('shared/semantic/domains')
            for domain in domains:
                domain_path = semantic_path / domain
                if domain_path.exists():
                    return f"shared/semantic/domains/{domain}"

        return None

    def format_blocking_message(
        self,
        missing: List[str],
        details: Dict[str, Any]
    ) -> str:
        """Format user-friendly blocking message."""
        lines = []
        lines.append("❌ Cannot write code yet - missing required artifacts")
        lines.append("")

        if details['phase']:
            lines.append(f"Current phase: {details['phase']} ({details['phase_name']})")
            lines.append("Code allowed in: Phase 8 (Implementation)")
            lines.append("")

        lines.append("Required before coding:")
        lines.append("  [ ] Requirements documented")
        lines.append("  [ ] Low-fidelity mockups")
        lines.append("  [ ] Data model defined")
        lines.append("")

        lines.append("What's missing:")
        for item in missing:
            lines.append(f"  ✗ {item}")
        lines.append("")

        lines.append("Options:")
        lines.append("  [1] Create all artifacts in sequence (recommended)")
        lines.append("  [2] Create requirements only")
        lines.append("  [3] Create mockups only")
        lines.append("  [4] Create data model only")
        lines.append("  [5] Declare SPIKE mode (skip to code)")
        lines.append("  [6] Advance through phases normally")
        lines.append("")
        lines.append("Your choice:")

        return "\n".join(lines)

    def format_success_message(self, details: Dict[str, Any]) -> str:
        """Format success message showing found artifacts."""
        lines = []
        lines.append("✅ Pre-code gate passed - all artifacts present")
        lines.append("")

        if details['spike_mode']:
            lines.append("⚡ SPIKE MODE - bypassing gate")
            lines.append("")

        lines.append(f"Phase: {details['phase']} ({details['phase_name']})")
        lines.append("")

        lines.append("Found artifacts:")
        if details['requirements']:
            lines.append(f"  ✓ Requirements: {details['requirements']}")
        if details['mockups']:
            lines.append(f"  ✓ Mockups: {len(details['mockups'])} file(s)")
            for mockup in details['mockups'][:3]:  # Show first 3
                lines.append(f"    - {mockup}")
            if len(details['mockups']) > 3:
                lines.append(f"    ... and {len(details['mockups']) - 3} more")
        if details['data_model']:
            lines.append(f"  ✓ Data Model: {details['data_model']}")
        lines.append("")

        lines.append("✅ Code writing is ALLOWED")

        return "\n".join(lines)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Pre-Code Gate Enforcement - Check if code writing is allowed'
    )
    parser.add_argument(
        '--project',
        default='.',
        help='Project directory path (default: current directory)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed output'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON'
    )

    args = parser.parse_args()

    project_path = Path(args.project).resolve()

    if not project_path.exists():
        print(f"Error: Project path does not exist: {project_path}", file=sys.stderr)
        sys.exit(1)

    gate = PreCodeGate(project_path)
    can_proceed, missing, details = gate.check()

    if args.json:
        import json
        output = {
            'can_proceed': can_proceed,
            'missing_artifacts': missing,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        print(json.dumps(output, indent=2))
    else:
        if can_proceed:
            print(gate.format_success_message(details))
        else:
            print(gate.format_blocking_message(missing, details))

    # Exit code: 0 if can proceed, 1 if blocked
    sys.exit(0 if can_proceed else 1)


if __name__ == '__main__':
    main()
