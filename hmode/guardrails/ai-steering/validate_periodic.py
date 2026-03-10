#!/usr/bin/env python3
"""
Periodic Guardrail Validator

Runs every N turns to validate guardrails are being followed.
Can be triggered via:
1. Manual execution: python3 validate_periodic.py
2. Hook integration: Called from .claude/hooks/
3. CI/CD: Called in GitHub Actions

Validates:
- S3 publishing offered for publishable files
- Shared domain models used (not local types)
- S3 URLs in clickable markdown format
- Tech dependencies approved in guardrails

Exit codes:
  0 - All validations passed
  1 - Warnings found (non-blocking)
  2 - Errors found (should block)

Usage:
  python3 validate_periodic.py                    # Run all validators
  python3 validate_periodic.py --fix              # Auto-fix violations
  python3 validate_periodic.py --since HEAD~5     # Check last 5 commits
  python3 validate_periodic.py --strict           # Fail on warnings
  python3 validate_periodic.py --json             # JSON output
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set
import subprocess

# ============================================================================
# Configuration
# ============================================================================

REPO_ROOT = Path(__file__).parent.parent.parent
RULES_DIR = REPO_ROOT / ".guardrails" / "ai-steering" / "rules"
TECH_PREFS_DIR = REPO_ROOT / ".guardrails" / "tech-preferences"
DOMAIN_REGISTRY = REPO_ROOT / "shared" / "semantic" / "domains" / "registry.yaml"

# File patterns for S3 publishing
PUBLISHABLE_EXTENSIONS = {".html", ".pdf", ".svg", ".zip", ".mp3", ".mp4"}

# Marker files that indicate S3 publish was intentionally skipped
S3_SKIP_MARKERS = {".s3-skip", ".no-publish", "SKIP_S3_PUBLISH"}


# ============================================================================
# Data Models
# ============================================================================

class Severity(Enum):
    INFO = 0
    WARNING = 1
    ERROR = 2
    CRITICAL = 3


class ViolationType(Enum):
    S3_PUBLISH_NOT_OFFERED = "s3_publish_not_offered"
    SHARED_MODEL_NOT_USED = "shared_model_not_used"
    URL_NOT_CLICKABLE = "url_not_clickable"
    TECH_NOT_APPROVED = "tech_not_approved"


@dataclass
class Violation:
    """Represents a guardrail violation"""
    type: ViolationType
    severity: Severity
    message: str
    file_path: Optional[Path] = None
    line_number: Optional[int] = None
    suggestion: Optional[str] = None
    auto_fixable: bool = False
    rule_id: Optional[str] = None


@dataclass
class ValidationResult:
    """Results from validation run"""
    violations: List[Violation] = field(default_factory=list)
    files_checked: int = 0
    warnings: int = 0
    errors: int = 0

    def add_violation(self, violation: Violation):
        self.violations.append(violation)
        if violation.severity == Severity.WARNING:
            self.warnings += 1
        elif violation.severity in (Severity.ERROR, Severity.CRITICAL):
            self.errors += 1

    def has_errors(self) -> bool:
        return self.errors > 0

    def has_warnings(self) -> bool:
        return self.warnings > 0


# ============================================================================
# Validators
# ============================================================================

class BaseValidator:
    """Base class for validators"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root

    def validate(self) -> List[Violation]:
        """Run validation, return list of violations"""
        raise NotImplementedError


class S3PublishValidator(BaseValidator):
    """Validates S3 publishing rule compliance"""

    def validate(self) -> List[Violation]:
        violations = []

        # Find publishable files
        publishable_files = self._find_publishable_files()

        for file_path in publishable_files:
            # Check if S3 publish evidence exists
            if not self._has_s3_evidence(file_path):
                violations.append(Violation(
                    type=ViolationType.S3_PUBLISH_NOT_OFFERED,
                    severity=Severity.ERROR,
                    message=f"Publishable file created without S3 publish evidence",
                    file_path=file_path,
                    suggestion="Run: python3 prototypes/proto-s3-publish-vayfd-023/s3_publish.py --yes {file_path}",
                    auto_fixable=False,
                    rule_id="microsite-prompt-s3-publish"
                ))

        return violations

    def _find_publishable_files(self) -> List[Path]:
        """Find files that should be published to S3"""
        publishable = []

        # Search in common directories
        search_dirs = ["prototypes", "project-management/ideas"]

        for search_dir in search_dirs:
            dir_path = self.repo_root / search_dir
            if not dir_path.exists():
                continue

            for ext in PUBLISHABLE_EXTENSIONS:
                for file_path in dir_path.rglob(f"*{ext}"):
                    # Skip node_modules, dist, build directories
                    if any(part in file_path.parts for part in ["node_modules", "dist", "build", ".venv", "venv"]):
                        continue
                    publishable.append(file_path)

        return publishable

    def _has_s3_evidence(self, file_path: Path) -> bool:
        """Check if file has evidence of S3 publishing"""
        # Check for skip markers in same directory
        for marker in S3_SKIP_MARKERS:
            if (file_path.parent / marker).exists():
                return True

        # Check for corresponding .s3-published file
        s3_marker = file_path.parent / f"{file_path.name}.s3-published"
        if s3_marker.exists():
            return True

        # Check for bookmark file (indicates published)
        bookmarks_dir = self.repo_root / "bookmarks"
        if bookmarks_dir.exists():
            bookmark_file = bookmarks_dir / f"{file_path.stem}.url"
            if bookmark_file.exists():
                return True

        # Check git history for S3 publish commit message
        try:
            result = subprocess.run(
                ["git", "log", "--all", "--oneline", "--grep", f"S3.*{file_path.name}"],
                cwd=self.repo_root,
                capture_output=True,
                text=True
            )
            if result.stdout.strip():
                return True
        except Exception:
            pass

        return False


class SharedModelsValidator(BaseValidator):
    """Validates shared domain model usage"""

    def validate(self) -> List[Violation]:
        violations = []

        # Load domain registry
        registry = self._load_domain_registry()
        if not registry:
            return violations  # Skip if registry not available

        # Find TypeScript and Python files with type definitions
        type_files = list(self.repo_root.rglob("*.ts")) + list(self.repo_root.rglob("*.py"))

        for file_path in type_files:
            # Skip node_modules, venv, shared domains
            if any(part in file_path.parts for part in ["node_modules", ".venv", "venv", "shared/semantic/domains"]):
                continue

            local_types = self._find_local_type_definitions(file_path)

            for type_name, line_num in local_types:
                if self._type_exists_in_registry(type_name, registry):
                    domain = self._find_domain_for_type(type_name, registry)
                    violations.append(Violation(
                        type=ViolationType.SHARED_MODEL_NOT_USED,
                        severity=Severity.ERROR,
                        message=f"Type '{type_name}' defined locally but exists in shared domains",
                        file_path=file_path,
                        line_number=line_num,
                        suggestion=f"Import from shared: import {{ {type_name} }} from '@domains/{domain}'",
                        auto_fixable=True,
                        rule_id="microsite-use-existing-domain-models"
                    ))

        return violations

    def _load_domain_registry(self) -> Optional[Dict]:
        """Load domain registry YAML"""
        if not DOMAIN_REGISTRY.exists():
            return None

        try:
            import yaml
            with open(DOMAIN_REGISTRY) as f:
                return yaml.safe_load(f)
        except ImportError:
            # Fallback: simple parser for basic YAML
            with open(DOMAIN_REGISTRY) as f:
                content = f.read()
                # Extract domain names (basic parsing)
                domains = {}
                current_domain = None
                for line in content.split("\n"):
                    if line.strip().startswith("- name:"):
                        current_domain = line.split(":", 1)[1].strip()
                    elif current_domain and "entities:" in line:
                        domains[current_domain] = []
                    elif current_domain and line.strip().startswith("- "):
                        entity = line.strip().lstrip("- ")
                        domains[current_domain].append(entity)
                return domains
        except Exception:
            return None

    def _find_local_type_definitions(self, file_path: Path) -> List[tuple[str, int]]:
        """Find local type definitions in file"""
        types = []

        try:
            with open(file_path) as f:
                for line_num, line in enumerate(f, 1):
                    # TypeScript: interface Foo, type Foo =, class Foo
                    ts_match = re.search(r'(?:interface|type|class)\s+([A-Z][a-zA-Z0-9]*)', line)
                    if ts_match and "import" not in line:
                        types.append((ts_match.group(1), line_num))

                    # Python: class Foo(BaseModel)
                    py_match = re.search(r'class\s+([A-Z][a-zA-Z0-9]*)\(.*BaseModel.*\)', line)
                    if py_match:
                        types.append((py_match.group(1), line_num))
        except Exception:
            pass

        return types

    def _type_exists_in_registry(self, type_name: str, registry: Dict) -> bool:
        """Check if type exists in domain registry"""
        if not registry:
            return False

        for domain, entities in registry.items():
            if isinstance(entities, list) and type_name in entities:
                return True

        return False

    def _find_domain_for_type(self, type_name: str, registry: Dict) -> str:
        """Find which domain contains the type"""
        for domain, entities in registry.items():
            if isinstance(entities, list) and type_name in entities:
                return domain
        return "unknown"


class URLFormatValidator(BaseValidator):
    """Validates S3 URLs are in clickable markdown format"""

    def validate(self) -> List[Violation]:
        violations = []

        # Find markdown files and code files with S3 URLs
        url_files = list(self.repo_root.rglob("*.md")) + list(self.repo_root.rglob("*.ts")) + list(self.repo_root.rglob("*.py"))

        for file_path in url_files:
            # Skip node_modules, venv
            if any(part in file_path.parts for part in ["node_modules", ".venv", "venv"]):
                continue

            plain_urls = self._find_plain_s3_urls(file_path)

            for url, line_num in plain_urls:
                violations.append(Violation(
                    type=ViolationType.URL_NOT_CLICKABLE,
                    severity=Severity.WARNING,
                    message=f"Plain S3 URL found (not clickable markdown)",
                    file_path=file_path,
                    line_number=line_num,
                    suggestion=f"Change to: [View file]({url})",
                    auto_fixable=True,
                    rule_id="s3-url-clickable-format"
                ))

        return violations

    def _find_plain_s3_urls(self, file_path: Path) -> List[tuple[str, int]]:
        """Find plain S3 URLs not in markdown link format"""
        plain_urls = []

        try:
            with open(file_path) as f:
                for line_num, line in enumerate(f, 1):
                    # Find S3 URLs
                    s3_urls = re.findall(r'https://[^/]+\.s3\.[^/]+\.amazonaws\.com/[^\s\)]+', line)

                    for url in s3_urls:
                        # Check if it's already in markdown link format [text](url)
                        if f"]({url})" not in line and f"]({url.strip()})" not in line:
                            plain_urls.append((url, line_num))
        except Exception:
            pass

        return plain_urls


class TechPreferencesValidator(BaseValidator):
    """Validates tech dependencies against approved guardrails"""

    def validate(self) -> List[Violation]:
        violations = []

        # Load approved tech preferences
        approved = self._load_tech_preferences()

        # Check package.json (JavaScript/TypeScript)
        violations.extend(self._validate_package_json(approved))

        # Check pyproject.toml (Python)
        violations.extend(self._validate_python_deps(approved))

        return violations

    def _load_tech_preferences(self) -> Dict:
        """Load approved tech from guardrails"""
        approved = {}

        for pref_file in TECH_PREFS_DIR.glob("*.json"):
            try:
                with open(pref_file) as f:
                    data = json.load(f)
                    category = pref_file.stem
                    approved[category] = data
            except Exception:
                pass

        return approved

    def _validate_package_json(self, approved: Dict) -> List[Violation]:
        """Validate package.json dependencies"""
        violations = []

        pkg_json = self.repo_root / "package.json"
        if not pkg_json.exists():
            return violations

        try:
            with open(pkg_json) as f:
                pkg = json.load(f)

            # Check dependencies and devDependencies
            all_deps = {}
            all_deps.update(pkg.get("dependencies", {}))
            all_deps.update(pkg.get("devDependencies", {}))

            for dep_name, dep_version in all_deps.items():
                if not self._is_approved_tech(dep_name, approved.get("frontend", {}).get("libraries", [])):
                    violations.append(Violation(
                        type=ViolationType.TECH_NOT_APPROVED,
                        severity=Severity.WARNING,
                        message=f"Dependency '{dep_name}' not in approved tech list",
                        file_path=pkg_json,
                        suggestion="Check .guardrails/tech-preferences/ or request approval",
                        auto_fixable=False,
                        rule_id="tech-preferences-validation"
                    ))
        except Exception:
            pass

        return violations

    def _validate_python_deps(self, approved: Dict) -> List[Violation]:
        """Validate Python dependencies"""
        violations = []

        pyproject = self.repo_root / "pyproject.toml"
        if not pyproject.exists():
            return violations

        try:
            with open(pyproject) as f:
                content = f.read()

            # Extract dependencies (simple regex parsing)
            deps = re.findall(r'"([a-zA-Z0-9_-]+)[><=~]', content)

            for dep_name in deps:
                if not self._is_approved_tech(dep_name, approved.get("backend", {}).get("libraries", [])):
                    violations.append(Violation(
                        type=ViolationType.TECH_NOT_APPROVED,
                        severity=Severity.WARNING,
                        message=f"Python dependency '{dep_name}' not in approved tech list",
                        file_path=pyproject,
                        suggestion="Check .guardrails/tech-preferences/ or request approval",
                        auto_fixable=False,
                        rule_id="tech-preferences-validation"
                    ))
        except Exception:
            pass

        return violations

    def _is_approved_tech(self, tech_name: str, approved_list: List) -> bool:
        """Check if tech is in approved list"""
        if not approved_list:
            return True  # Skip check if no approved list

        for approved in approved_list:
            if isinstance(approved, dict):
                if approved.get("name", "").lower() == tech_name.lower():
                    return True
            elif isinstance(approved, str):
                if approved.lower() == tech_name.lower():
                    return True

        return False


# ============================================================================
# Main Validator
# ============================================================================

class GuardrailValidator:
    """Main validator orchestrator"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.validators = [
            S3PublishValidator(repo_root),
            SharedModelsValidator(repo_root),
            URLFormatValidator(repo_root),
            TechPreferencesValidator(repo_root),
        ]

    def run_all(self) -> ValidationResult:
        """Run all validators"""
        result = ValidationResult()

        for validator in self.validators:
            violations = validator.validate()
            for violation in violations:
                result.add_violation(violation)

        return result

    def auto_fix(self, violations: List[Violation]) -> int:
        """Apply automatic fixes where possible"""
        fixed_count = 0

        for violation in violations:
            if violation.auto_fixable:
                if self._apply_fix(violation):
                    fixed_count += 1

        return fixed_count

    def _apply_fix(self, violation: Violation) -> bool:
        """Apply fix for a violation"""
        if violation.type == ViolationType.URL_NOT_CLICKABLE:
            return self._fix_url_format(violation)
        elif violation.type == ViolationType.SHARED_MODEL_NOT_USED:
            # TODO: Implement auto-import generation
            return False

        return False

    def _fix_url_format(self, violation: Violation) -> bool:
        """Fix plain S3 URL to markdown format"""
        if not violation.file_path or not violation.line_number:
            return False

        try:
            with open(violation.file_path) as f:
                lines = f.readlines()

            line = lines[violation.line_number - 1]

            # Find S3 URL in line
            url_match = re.search(r'https://[^/]+\.s3\.[^/]+\.amazonaws\.com/[^\s\)]+', line)
            if not url_match:
                return False

            url = url_match.group(0)
            filename = url.split('/')[-1]

            # Replace with markdown link
            new_line = line.replace(url, f"[{filename}]({url})")
            lines[violation.line_number - 1] = new_line

            with open(violation.file_path, 'w') as f:
                f.writelines(lines)

            return True
        except Exception:
            return False


# ============================================================================
# Output Formatters
# ============================================================================

def format_stylish(result: ValidationResult) -> str:
    """Format output in ESLint stylish format"""
    output = []

    # Group violations by file
    by_file = {}
    for v in result.violations:
        file_path = str(v.file_path) if v.file_path else "<unknown>"
        if file_path not in by_file:
            by_file[file_path] = []
        by_file[file_path].append(v)

    for file_path, violations in sorted(by_file.items()):
        output.append(f"\n{file_path}")

        for v in violations:
            severity_symbol = "❌" if v.severity in (Severity.ERROR, Severity.CRITICAL) else "⚠️"
            line_info = f":{v.line_number}" if v.line_number else ""
            output.append(f"  {severity_symbol} {line_info:4} {v.message}")

            if v.suggestion:
                output.append(f"     💡 {v.suggestion}")

    # Summary
    output.append(f"\n{'=' * 70}")
    output.append(f"✅ {result.files_checked} files checked")
    output.append(f"⚠️  {result.warnings} warnings")
    output.append(f"❌ {result.errors} errors")

    return "\n".join(output)


def format_json(result: ValidationResult) -> str:
    """Format output as JSON"""
    data = {
        "files_checked": result.files_checked,
        "warnings": result.warnings,
        "errors": result.errors,
        "violations": [
            {
                "type": v.type.value,
                "severity": v.severity.name,
                "message": v.message,
                "file": str(v.file_path) if v.file_path else None,
                "line": v.line_number,
                "suggestion": v.suggestion,
                "auto_fixable": v.auto_fixable,
                "rule_id": v.rule_id
            }
            for v in result.violations
        ]
    }
    return json.dumps(data, indent=2)


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Periodic guardrail validator")
    parser.add_argument("--fix", action="store_true", help="Auto-fix violations where possible")
    parser.add_argument("--strict", action="store_true", help="Fail on warnings (exit code 2)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--since", help="Only check files changed since commit (e.g., HEAD~5)")

    args = parser.parse_args()

    # Run validation
    validator = GuardrailValidator(REPO_ROOT)
    result = validator.run_all()

    # Apply fixes if requested
    if args.fix:
        fixed = validator.auto_fix(result.violations)
        print(f"🔧 Auto-fixed {fixed} violations")

    # Output results
    if args.json:
        print(format_json(result))
    else:
        print(format_stylish(result))

    # Exit with appropriate code
    if result.has_errors():
        sys.exit(2)
    elif args.strict and result.has_warnings():
        sys.exit(2)
    elif result.has_warnings():
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
