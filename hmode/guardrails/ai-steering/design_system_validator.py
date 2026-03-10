#!/usr/bin/env python3
"""
Design System Validator - Layer 4 of 4-layer enforcement

Validates React files for design system compliance.
Integrated with .claude/hooks/tool-result.sh for real-time AI feedback.

Layer 4 of 4-layer enforcement strategy:
- Layer 1: Guardrails (rules definition)
- Layer 2: ESLint (development time)
- Layer 3: Vite plugin (build time)
- Layer 4: Hook validation (AI assistance) ← YOU ARE HERE

Usage:
    python3 design_system_validator.py check <file_path>
    python3 design_system_validator.py validate <file_path>
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DESIGN SYSTEM RULES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RULES = {
    "raw-button": {
        "pattern": r"<button[\s>]",
        "message": "Raw <button> prohibited",
        "fix": "Use <Button> from shadcn/ui: import { Button } from '@/components/ui/button'",
        "severity": "error",
    },
    "raw-input": {
        "pattern": r"<input[\s/>]",
        "message": "Raw <input> prohibited",
        "fix": "Use <Input> from shadcn/ui: import { Input } from '@/components/ui/input'",
        "severity": "error",
    },
    "raw-select": {
        "pattern": r"<select[\s>]",
        "message": "Raw <select> prohibited",
        "fix": "Use <Select> from shadcn/ui: import { Select } from '@/components/ui/select'",
        "severity": "error",
    },
    "raw-textarea": {
        "pattern": r"<textarea[\s>]",
        "message": "Raw <textarea> prohibited",
        "fix": "Use <Textarea> from shadcn/ui: import { Textarea } from '@/components/ui/textarea'",
        "severity": "error",
    },
    "raw-dialog": {
        "pattern": r"<dialog[\s>]",
        "message": "Raw <dialog> prohibited",
        "fix": "Use <Dialog> from shadcn/ui: import { Dialog } from '@/components/ui/dialog'",
        "severity": "error",
    },
    "inline-style": {
        "pattern": r'style=\{\{',
        "message": "Inline styles prohibited",
        "fix": "Use Tailwind className: className='...'",
        "severity": "error",
    },
    "css-import": {
        "pattern": r"import\s+['\"].*\.css['\"]",
        "message": "CSS imports prohibited (except globals)",
        "fix": "Use Tailwind utilities or shadcn components",
        "severity": "warning",
    },
}

# Exclusion patterns
EXCLUDE_PATTERNS = [
    r"\.test\.tsx$",
    r"\.test\.jsx$",
    r"\.spec\.tsx$",
    r"\.spec\.jsx$",
    r"\.stories\.tsx$",
    r"\.stories\.jsx$",
    r"/components/ui/",  # shadcn components themselves
]

# Allowed CSS imports
ALLOWED_CSS_IMPORTS = ["index.css", "globals.css", "app.css"]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# VALIDATION FUNCTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def should_skip_file(file_path: str) -> bool:
    """Check if file should be skipped based on exclusion patterns."""
    for pattern in EXCLUDE_PATTERNS:
        if re.search(pattern, file_path):
            return True
    return False


def is_react_file(file_path: str) -> bool:
    """Check if file is a React file."""
    return file_path.endswith((".tsx", ".jsx"))


def validate_file(file_path: str) -> List[Dict]:
    """
    Validate a file for design system violations.

    Returns:
        List of violations, each containing:
        - rule: Rule ID
        - line: Line number
        - message: Error message
        - fix: Suggested fix
        - severity: 'error' or 'warning'
    """
    # Skip non-React files
    if not is_react_file(file_path):
        return []

    # Skip excluded files
    if should_skip_file(file_path):
        return []

    # Read file
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except (FileNotFoundError, UnicodeDecodeError):
        return []

    # Check if file uses shadcn (if so, likely already compliant)
    has_shadcn_import = re.search(r"from ['\"]@/components/ui/", content)

    violations = []

    # Check each rule
    for rule_id, rule in RULES.items():
        pattern = rule["pattern"]

        # Special handling for CSS imports
        if rule_id == "css-import":
            matches = re.finditer(pattern, content)
            for match in matches:
                # Check if it's an allowed CSS import
                import_line = match.group(0)
                if any(allowed in import_line for allowed in ALLOWED_CSS_IMPORTS):
                    continue

                line_num = content[: match.start()].count("\n") + 1
                violations.append(
                    {
                        "rule": rule_id,
                        "line": line_num,
                        "message": rule["message"],
                        "fix": rule["fix"],
                        "severity": rule["severity"],
                    }
                )
            continue

        # Regular pattern matching
        matches = re.finditer(pattern, content)

        for match in matches:
            line_num = content[: match.start()].count("\n") + 1

            violations.append(
                {
                    "rule": rule_id,
                    "line": line_num,
                    "message": rule["message"],
                    "fix": rule["fix"],
                    "severity": rule["severity"],
                }
            )

    return violations


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# OUTPUT FORMATTING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def format_violations_for_hook(file_path: str, violations: List[Dict]) -> str:
    """
    Format violations for display in tool-result.sh hook output.

    Returns a formatted string that will be appended to tool results
    to prompt the AI to fix violations.
    """
    if not violations:
        return ""

    errors = [v for v in violations if v["severity"] == "error"]
    warnings = [v for v in violations if v["severity"] == "warning"]

    output = []
    output.append("")
    output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    output.append("🤖 DESIGN SYSTEM GUARDRAIL REMINDER")
    output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    output.append("")

    if errors:
        output.append(f"❌ {len(errors)} DESIGN SYSTEM ERROR(S) in {file_path}:")
        output.append("")
        for violation in errors[:3]:  # Show max 3 errors
            output.append(f"  Line {violation['line']}: {violation['message']}")
            output.append(f"  Fix: {violation['fix']}")
            output.append("")

        if len(errors) > 3:
            output.append(f"  ... and {len(errors) - 3} more error(s)")
            output.append("")

    if warnings:
        output.append(f"⚠️  {len(warnings)} DESIGN SYSTEM WARNING(S):")
        for violation in warnings[:2]:  # Show max 2 warnings
            output.append(f"  Line {violation['line']}: {violation['message']}")
        output.append("")

    output.append("📋 REQUIRED ACTION:")
    output.append(
        "  Fix violations above by using shadcn/ui components instead of raw HTML."
    )
    output.append("  See: .guardrails/design-system-rules.md")
    output.append("")
    output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    return "\n".join(output)


def format_violations_for_cli(file_path: str, violations: List[Dict]) -> str:
    """Format violations for CLI output (detailed)."""
    if not violations:
        return f"✅ {file_path}: No violations"

    errors = [v for v in violations if v["severity"] == "error"]
    warnings = [v for v in violations if v["severity"] == "warning"]

    output = []
    output.append("")
    output.append(f"File: {file_path}")
    output.append("")

    if errors:
        output.append(f"❌ {len(errors)} ERROR(S):")
        for v in errors:
            output.append(f"  Line {v['line']}: {v['message']}")
            output.append(f"    Fix: {v['fix']}")
        output.append("")

    if warnings:
        output.append(f"⚠️  {len(warnings)} WARNING(S):")
        for v in warnings:
            output.append(f"  Line {v['line']}: {v['message']}")
        output.append("")

    return "\n".join(output)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CLI COMMANDS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def cmd_check(file_path: str) -> int:
    """
    Check file and print violations for hook output.

    Returns:
        0 if no errors, 1 if errors found
    """
    violations = validate_file(file_path)

    # Print for hook to capture
    output = format_violations_for_hook(file_path, violations)
    if output:
        print(output)

    # Return exit code
    errors = [v for v in violations if v["severity"] == "error"]
    return 1 if errors else 0


def cmd_validate(file_path: str) -> int:
    """
    Validate file and print detailed violations for CLI.

    Returns:
        0 if no errors, 1 if errors found
    """
    violations = validate_file(file_path)

    # Print detailed output
    print(format_violations_for_cli(file_path, violations))

    # Return exit code
    errors = [v for v in violations if v["severity"] == "error"]
    return 1 if errors else 0


def main():
    """CLI entry point."""
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python3 design_system_validator.py check <file_path>")
        print("  python3 design_system_validator.py validate <file_path>")
        sys.exit(1)

    command = sys.argv[1]
    file_path = sys.argv[2]

    if command == "check":
        sys.exit(cmd_check(file_path))
    elif command == "validate":
        sys.exit(cmd_validate(file_path))
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
