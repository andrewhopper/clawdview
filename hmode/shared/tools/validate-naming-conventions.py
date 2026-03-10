#!/usr/bin/env python3
"""
Naming Convention Validator

Validates that ProtoFlow components follow naming conventions defined in
.claude/skills/protoflow/NAMING_CONVENTIONS.md

Usage:
    python validate-naming-conventions.py
    python validate-naming-conventions.py --strict
    python validate-naming-conventions.py --directory .claude/agents
    python validate-naming-conventions.py --fix  # Generate rename script
"""
# File UUID: e7b4c8f2-3d9a-4e1b-9c5f-2a6d8e1f3b7c

import sys
import re
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class ComponentType(Enum):
    AGENT = "agent"
    COMMAND = "command"
    SKILL = "skill"
    TOOL = "tool"
    SCRIPT = "script"

@dataclass
class ValidationResult:
    """Result of validating a single component"""
    component_type: ComponentType
    path: Path
    filename: str
    is_valid: bool
    issues: List[str]
    suggestion: Optional[str] = None

@dataclass
class ValidationSummary:
    """Summary of all validation results"""
    total: int
    valid: int
    invalid: int
    results: List[ValidationResult]

class NamingValidator:
    """Validates ProtoFlow component naming conventions"""

    # Agent role suffixes
    AGENT_ROLES = ['-specialist', '-agent', '-expert']

    # Command action verbs
    COMMAND_VERBS = [
        'generate', 'create', 'add', 'update', 'deliver', 'publish',
        'check', 'scan', 'list', 'run', 'push', 'pull', 'merge',
        'audit', 'validate', 'prepare', 'deploy', 'upload', 'archive'
    ]

    # Tool verbs
    TOOL_VERBS = [
        'generate', 'audit', 'enforce', 'validate', 'sync', 'bootstrap',
        'add', 'post', 'pre', 'check', 'scan'
    ]

    # Reserved/generic names to avoid
    RESERVED_NAMES = [
        'helper', 'utility', 'manager', 'handler', 'tool', 'script',
        'agent', 'command'
    ]

    def __init__(self, strict: bool = False):
        self.strict = strict

    def validate_agent(self, path: Path) -> ValidationResult:
        """Validate agent naming (kebab-case with role suffix)"""
        filename = path.stem
        issues = []

        # Check kebab-case
        if not self._is_kebab_case(filename):
            issues.append(f"Not kebab-case: {filename}")

        # Check role suffix
        has_role = any(filename.endswith(role) for role in self.AGENT_ROLES)
        if not has_role:
            issues.append(f"Missing role suffix ({', '.join(self.AGENT_ROLES)})")

        # Check length
        if len(filename) > 40:
            issues.append(f"Name too long ({len(filename)} > 40 chars)")

        # Check for reserved names
        for reserved in self.RESERVED_NAMES:
            if reserved in filename:
                issues.append(f"Contains reserved word: {reserved}")

        # Generate suggestion if invalid
        suggestion = None
        if issues:
            suggestion = self._suggest_agent_name(filename)

        return ValidationResult(
            component_type=ComponentType.AGENT,
            path=path,
            filename=filename,
            is_valid=len(issues) == 0,
            issues=issues,
            suggestion=suggestion
        )

    def validate_command(self, path: Path) -> ValidationResult:
        """Validate command naming (kebab-case with action-noun)"""
        filename = path.stem
        issues = []

        # Skip single-letter shortcuts
        if len(filename) == 1:
            return ValidationResult(
                component_type=ComponentType.COMMAND,
                path=path,
                filename=filename,
                is_valid=True,
                issues=[]
            )

        # Check kebab-case
        if not self._is_kebab_case(filename):
            issues.append(f"Not kebab-case: {filename}")

        # Check if starts with action verb (optional but recommended)
        starts_with_verb = any(filename.startswith(verb) for verb in self.COMMAND_VERBS)
        if self.strict and not starts_with_verb:
            issues.append(f"Should start with action verb")

        # Check length
        if len(filename) > 40:
            issues.append(f"Name too long ({len(filename)} > 40 chars)")

        suggestion = None
        if issues:
            suggestion = self._suggest_command_name(filename)

        return ValidationResult(
            component_type=ComponentType.COMMAND,
            path=path,
            filename=filename,
            is_valid=len(issues) == 0,
            issues=issues,
            suggestion=suggestion
        )

    def validate_skill(self, path: Path) -> ValidationResult:
        """Validate skill naming (protoflow: namespace prefix)"""
        # For skills, we check the name in skill.yaml, not the directory name
        skill_yaml = path / "skill.yaml"
        if not skill_yaml.exists():
            # Check for skill.json as fallback
            skill_json = path / "skill.json"
            if not skill_json.exists():
                return ValidationResult(
                    component_type=ComponentType.SKILL,
                    path=path,
                    filename=path.name,
                    is_valid=False,
                    issues=["Missing skill.yaml or skill.json"],
                    suggestion=None
                )

        # For now, just validate directory name is kebab-case
        dirname = path.name
        issues = []

        if not self._is_kebab_case(dirname):
            issues.append(f"Directory not kebab-case: {dirname}")

        return ValidationResult(
            component_type=ComponentType.SKILL,
            path=path,
            filename=dirname,
            is_valid=len(issues) == 0,
            issues=issues,
            suggestion=None
        )

    def validate_tool(self, path: Path) -> ValidationResult:
        """Validate tool naming (kebab-case verb-noun.py)"""
        filename = path.stem
        issues = []

        # Check kebab-case
        if not self._is_kebab_case(filename):
            issues.append(f"Not kebab-case: {filename}")

        # Check starts with verb
        starts_with_verb = any(filename.startswith(verb) for verb in self.TOOL_VERBS)
        if not starts_with_verb:
            issues.append(f"Should start with action verb")

        # Check length
        if len(filename) > 40:
            issues.append(f"Name too long ({len(filename)} > 40 chars)")

        suggestion = None
        if issues:
            suggestion = self._suggest_tool_name(filename)

        return ValidationResult(
            component_type=ComponentType.TOOL,
            path=path,
            filename=filename,
            is_valid=len(issues) == 0,
            issues=issues,
            suggestion=suggestion
        )

    def validate_script(self, path: Path) -> ValidationResult:
        """Validate script naming (snake_case for .py, kebab-case for .sh)"""
        filename = path.stem
        extension = path.suffix
        issues = []

        if extension == ".py":
            # Python scripts should use snake_case
            if not self._is_snake_case(filename):
                issues.append(f"Python script not snake_case: {filename}")
        elif extension == ".sh":
            # Shell scripts should use kebab-case
            if not self._is_kebab_case(filename):
                issues.append(f"Shell script not kebab-case: {filename}")

        # Check length
        if len(filename) > 40:
            issues.append(f"Name too long ({len(filename)} > 40 chars)")

        suggestion = None
        if issues:
            suggestion = self._suggest_script_name(filename, extension)

        return ValidationResult(
            component_type=ComponentType.SCRIPT,
            path=path,
            filename=filename,
            is_valid=len(issues) == 0,
            issues=issues,
            suggestion=suggestion
        )

    def _is_kebab_case(self, name: str) -> bool:
        """Check if name is kebab-case"""
        return bool(re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name))

    def _is_snake_case(self, name: str) -> bool:
        """Check if name is snake_case"""
        return bool(re.match(r'^[a-z0-9]+(_[a-z0-9]+)*$', name))

    def _suggest_agent_name(self, current: str) -> str:
        """Suggest a valid agent name"""
        # Convert to kebab-case
        suggested = current.lower().replace('_', '-').replace(' ', '-')

        # Add role suffix if missing
        has_role = any(suggested.endswith(role) for role in self.AGENT_ROLES)
        if not has_role:
            suggested += '-agent'

        return suggested

    def _suggest_command_name(self, current: str) -> str:
        """Suggest a valid command name"""
        return current.lower().replace('_', '-').replace(' ', '-')

    def _suggest_tool_name(self, current: str) -> str:
        """Suggest a valid tool name"""
        return current.lower().replace('_', '-').replace(' ', '-')

    def _suggest_script_name(self, current: str, extension: str) -> str:
        """Suggest a valid script name"""
        if extension == ".py":
            return current.lower().replace('-', '_').replace(' ', '_')
        else:
            return current.lower().replace('_', '-').replace(' ', '-')

def validate_directory(
    directory: Path,
    component_type: ComponentType,
    validator: NamingValidator
) -> List[ValidationResult]:
    """Validate all components in a directory"""
    results = []

    if component_type == ComponentType.SKILL:
        # Skills are directories
        for item in directory.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                result = validator.validate_skill(item)
                results.append(result)
    else:
        # Other components are files
        patterns = {
            ComponentType.AGENT: "*.md",
            ComponentType.COMMAND: "*.md",
            ComponentType.TOOL: "*.py",
            ComponentType.SCRIPT: ["*.py", "*.sh"]
        }

        pattern_list = patterns[component_type]
        if not isinstance(pattern_list, list):
            pattern_list = [pattern_list]

        for pattern in pattern_list:
            for item in directory.glob(pattern):
                if item.is_file():
                    if component_type == ComponentType.AGENT:
                        result = validator.validate_agent(item)
                    elif component_type == ComponentType.COMMAND:
                        result = validator.validate_command(item)
                    elif component_type == ComponentType.TOOL:
                        result = validator.validate_tool(item)
                    elif component_type == ComponentType.SCRIPT:
                        result = validator.validate_script(item)

                    results.append(result)

    return results

def print_results(summary: ValidationSummary, verbose: bool = True):
    """Print validation results"""
    print("\n" + "=" * 80)
    print(f"NAMING CONVENTION VALIDATION RESULTS")
    print("=" * 80)
    print(f"\nTotal: {summary.total} | Valid: {summary.valid} | Invalid: {summary.invalid}")

    if summary.invalid > 0:
        print("\n" + "-" * 80)
        print("ISSUES FOUND:")
        print("-" * 80)

        for result in summary.results:
            if not result.is_valid:
                print(f"\n❌ {result.component_type.value.upper()}: {result.filename}")
                print(f"   Path: {result.path}")
                for issue in result.issues:
                    print(f"   - {issue}")
                if result.suggestion:
                    print(f"   💡 Suggestion: {result.suggestion}")

    if verbose and summary.valid > 0:
        print("\n" + "-" * 80)
        print("VALID FILES:")
        print("-" * 80)
        for result in summary.results:
            if result.is_valid:
                print(f"✅ {result.component_type.value}: {result.filename}")

    print("\n" + "=" * 80)

    if summary.invalid > 0:
        print(f"❌ {summary.invalid} files need attention")
        return 1
    else:
        print("✅ All files follow naming conventions!")
        return 0

def generate_rename_script(summary: ValidationSummary, output_path: Path):
    """Generate a shell script to rename invalid files"""
    with open(output_path, 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("# Auto-generated rename script\n")
        f.write("# Generated by validate-naming-conventions.py\n\n")
        f.write("set -e\n\n")

        for result in summary.results:
            if not result.is_valid and result.suggestion:
                old_path = result.path
                new_name = result.suggestion + result.path.suffix
                new_path = result.path.parent / new_name

                f.write(f"# {result.filename} -> {result.suggestion}\n")
                f.write(f"git mv \"{old_path}\" \"{new_path}\"\n\n")

        f.write("echo 'Rename complete!'\n")

    output_path.chmod(0o755)
    print(f"\n✅ Rename script generated: {output_path}")
    print(f"   Review and run: bash {output_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Validate ProtoFlow component naming conventions"
    )
    parser.add_argument(
        "--directory",
        type=Path,
        help="Specific directory to validate"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Enable strict validation"
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Generate rename script"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=True,
        help="Show all results"
    )

    args = parser.parse_args()

    # Find repo root
    repo_root = Path(__file__).parent.parent.parent

    validator = NamingValidator(strict=args.strict)
    all_results = []

    # Define validation targets
    targets = [
        (repo_root / ".claude/agents", ComponentType.AGENT),
        (repo_root / ".claude/commands", ComponentType.COMMAND),
        (repo_root / ".claude/skills/protoflow", ComponentType.SKILL),
        (repo_root / "shared/tools", ComponentType.TOOL),
        (repo_root / "bin", ComponentType.SCRIPT),
    ]

    # If specific directory provided, filter targets
    if args.directory:
        targets = [(args.directory, None)]  # Detect type from path

    # Validate each target
    for directory, component_type in targets:
        if not directory.exists():
            continue

        # Auto-detect component type if not specified
        if component_type is None:
            if "agents" in str(directory):
                component_type = ComponentType.AGENT
            elif "commands" in str(directory):
                component_type = ComponentType.COMMAND
            elif "skills" in str(directory):
                component_type = ComponentType.SKILL
            elif "tools" in str(directory):
                component_type = ComponentType.TOOL
            elif "bin" in str(directory):
                component_type = ComponentType.SCRIPT

        results = validate_directory(directory, component_type, validator)
        all_results.extend(results)

    # Create summary
    summary = ValidationSummary(
        total=len(all_results),
        valid=sum(1 for r in all_results if r.is_valid),
        invalid=sum(1 for r in all_results if not r.is_valid),
        results=all_results
    )

    # Print results
    exit_code = print_results(summary, verbose=args.verbose)

    # Generate rename script if requested
    if args.fix and summary.invalid > 0:
        script_path = repo_root / "rename_components.sh"
        generate_rename_script(summary, script_path)

    sys.exit(exit_code)

if __name__ == "__main__":
    main()
