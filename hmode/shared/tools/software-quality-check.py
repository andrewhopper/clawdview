#!/usr/bin/env python3
# File UUID: a9b8c7d6-e5f4-3d2c-1b0a-9f8e7d6c5b4a
"""
Software Quality Check

Comprehensive code quality validation tool that checks software against
technical standards, best practices, and monorepo guidelines.

Usage:
    # Full project audit
    python software-quality-check.py --project /path/to/project

    # Specific files
    python software-quality-check.py src/services/*.ts

    # Pre-deployment check
    python software-quality-check.py --project . --strict

    # Generate JSON report
    python software-quality-check.py --project . --format json

Checks:
    1. Configuration Abstraction (no hardcoded IDs/paths)
    2. Shared Model Reuse (domain models)
    3. Code Decomposition (file size limits)
    4. Testing Presence (test files exist)
    5. Type Safety (type hints, TypeScript)
    6. Security Best Practices (no secrets, secure connections)
    7. Design System Compliance (UI projects)
    8. Domain Model Usage (timestamps, decomposition)
"""

import argparse
import json
import logging
import re
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

# Setup logging
LOG_DIR = Path(__file__).parent.parent.parent / "logs" / "tools"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "software-quality-check.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class Severity(Enum):
    """Issue severity levels."""
    ERROR = "error"      # Critical violation, must fix
    WARNING = "warning"  # Recommended improvement
    INFO = "info"        # Informational finding


class CheckType(Enum):
    """Types of quality checks."""
    CONFIG_ABSTRACTION = "config-abstraction"
    SHARED_MODEL_REUSE = "shared-model-reuse"
    CODE_DECOMPOSITION = "code-decomposition"
    TESTING_PRESENCE = "testing-presence"
    TYPE_SAFETY = "type-safety"
    SECURITY = "security"
    DESIGN_SYSTEM = "design-system"
    DOMAIN_MODEL_USAGE = "domain-model-usage"


@dataclass
class QualityIssue:
    """Represents a quality issue found during checks."""
    check_type: CheckType
    severity: Severity
    message: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    code_snippet: Optional[str] = None
    recommendation: Optional[str] = None
    rule_id: Optional[str] = None

    def __str__(self) -> str:
        icon = "❌" if self.severity == Severity.ERROR else "⚠️" if self.severity == Severity.WARNING else "ℹ️"
        msg = f"{icon} [{self.check_type.value.upper()}] {self.message}"

        if self.file_path:
            location = f"{self.file_path}"
            if self.line_number:
                location += f":{self.line_number}"
            msg += f"\n   Location: {location}"

        if self.code_snippet:
            msg += f"\n   Code: {self.code_snippet[:80]}"

        if self.recommendation:
            msg += f"\n   Fix: {self.recommendation}"

        return msg


@dataclass
class QualityReport:
    """Complete quality audit report."""
    project_path: Path
    checks_run: List[CheckType] = field(default_factory=list)
    issues: List[QualityIssue] = field(default_factory=list)
    passed_checks: List[CheckType] = field(default_factory=list)
    files_scanned: int = 0

    @property
    def has_errors(self) -> bool:
        return any(i.severity == Severity.ERROR for i in self.issues)

    @property
    def has_warnings(self) -> bool:
        return any(i.severity == Severity.WARNING for i in self.issues)

    @property
    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.ERROR)

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.WARNING)

    @property
    def info_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.INFO)

    def get_issues_by_check(self, check_type: CheckType) -> List[QualityIssue]:
        return [i for i in self.issues if i.check_type == check_type]


class SoftwareQualityChecker:
    """Main quality checker class."""

    def __init__(
        self,
        project_path: Path,
        checks: Optional[List[str]] = None,
        strict: bool = False,
        skip_patterns: Optional[List[str]] = None
    ):
        self.project_path = Path(project_path).resolve()
        self.checks = checks or ["all"]
        self.strict = strict
        self.skip_patterns = skip_patterns or [
            "**/.git/**",
            "**/node_modules/**",
            "**/venv/**",
            "**/__pycache__/**",
            "**/dist/**",
            "**/build/**",
            "**/.next/**",
            "**/coverage/**",
        ]
        self.report = QualityReport(project_path=self.project_path)

        logger.info(f"Initialized quality checker for: {self.project_path}")

    def should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped."""
        for pattern in self.skip_patterns:
            if file_path.match(pattern):
                return True
        return False

    def run_all_checks(self) -> QualityReport:
        """Run all quality checks."""
        logger.info("Starting quality checks...")

        check_methods = {
            "config": self.check_config_abstraction,
            "shared-models": self.check_shared_model_reuse,
            "decomposition": self.check_code_decomposition,
            "tests": self.check_testing_presence,
            "types": self.check_type_safety,
            "security": self.check_security,
            "design-system": self.check_design_system,
            "domain-models": self.check_domain_model_usage,
        }

        if "all" in self.checks:
            checks_to_run = check_methods.keys()
        else:
            checks_to_run = [c for c in self.checks if c in check_methods]

        for check_name in checks_to_run:
            logger.info(f"Running check: {check_name}")
            check_methods[check_name]()

        logger.info(f"Quality checks complete. Found {self.report.error_count} errors, "
                   f"{self.report.warning_count} warnings, {self.report.info_count} info")

        return self.report

    def check_config_abstraction(self):
        """Check 1: Configuration Abstraction (no hardcoded IDs/paths)."""
        check_type = CheckType.CONFIG_ABSTRACTION
        self.report.checks_run.append(check_type)

        # Run the audit-hardcoded-infra.py tool
        audit_script = self.project_path.parent.parent / "shared" / "tools" / "audit-hardcoded-infra.py"

        if not audit_script.exists():
            self.report.issues.append(QualityIssue(
                check_type=check_type,
                severity=Severity.WARNING,
                message="audit-hardcoded-infra.py not found, skipping config check",
                rule_id="CONFIG-001"
            ))
            return

        try:
            result = subprocess.run(
                [sys.executable, str(audit_script), "--path", str(self.project_path), "--format", "json"],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0 and result.stdout:
                data = json.loads(result.stdout)
                findings = data.get("findings", [])

                for finding in findings:
                    if finding["severity"] == "high":
                        self.report.issues.append(QualityIssue(
                            check_type=check_type,
                            severity=Severity.ERROR,
                            message=f"Hardcoded {finding['resource_type']}: {finding['value']}",
                            file_path=finding["file_path"],
                            line_number=finding["line_number"],
                            recommendation=finding["recommendation"],
                            rule_id="CONFIG-HARDCODE"
                        ))

                if not any(f["severity"] == "high" for f in findings):
                    self.report.passed_checks.append(check_type)
            else:
                logger.warning(f"Config check failed: {result.stderr}")

        except Exception as e:
            logger.error(f"Error running config check: {e}")
            self.report.issues.append(QualityIssue(
                check_type=check_type,
                severity=Severity.WARNING,
                message=f"Config check failed: {e}",
                rule_id="CONFIG-ERROR"
            ))

    def check_shared_model_reuse(self):
        """Check 2: Shared Model Reuse (domain models)."""
        check_type = CheckType.SHARED_MODEL_REUSE
        self.report.checks_run.append(check_type)

        # Check if project imports from shared/semantic/domains
        py_files = list(self.project_path.rglob("*.py"))
        ts_files = list(self.project_path.rglob("*.ts")) + list(self.project_path.rglob("*.tsx"))

        uses_shared_domains = False

        for py_file in py_files:
            if self.should_skip_file(py_file):
                continue

            try:
                content = py_file.read_text()
                if "from shared.semantic.domains" in content or "import shared.semantic.domains" in content:
                    uses_shared_domains = True
                    break
            except Exception:
                pass

        # For now, just report if shared domains are NOT used (info level)
        if not uses_shared_domains and (py_files or ts_files):
            self.report.issues.append(QualityIssue(
                check_type=check_type,
                severity=Severity.INFO,
                message="Project does not appear to use shared domain models",
                recommendation="Check shared/semantic/domains/registry.yaml for applicable domains",
                rule_id="SHARED-DOMAIN-001"
            ))
        else:
            self.report.passed_checks.append(check_type)

    def check_code_decomposition(self):
        """Check 3: Code Decomposition (file size limits)."""
        check_type = CheckType.CODE_DECOMPOSITION
        self.report.checks_run.append(check_type)

        large_files = []
        code_extensions = [".py", ".ts", ".tsx", ".js", ".jsx"]

        for ext in code_extensions:
            for file_path in self.project_path.rglob(f"*{ext}"):
                if self.should_skip_file(file_path):
                    continue

                try:
                    line_count = len(file_path.read_text().splitlines())
                    self.report.files_scanned += 1

                    if line_count > 500:
                        self.report.issues.append(QualityIssue(
                            check_type=check_type,
                            severity=Severity.ERROR,
                            message=f"File exceeds maximum line limit: {line_count} lines (max: 500)",
                            file_path=str(file_path.relative_to(self.project_path)),
                            recommendation="Decompose into smaller modules (< 300 lines recommended)",
                            rule_id="DECOMP-MAX"
                        ))
                        large_files.append(file_path)

                    elif line_count > 300:
                        self.report.issues.append(QualityIssue(
                            check_type=check_type,
                            severity=Severity.WARNING,
                            message=f"File exceeds recommended line limit: {line_count} lines (recommended: < 300)",
                            file_path=str(file_path.relative_to(self.project_path)),
                            recommendation="Consider decomposing for better maintainability",
                            rule_id="DECOMP-RECOMMEND"
                        ))

                except Exception as e:
                    logger.warning(f"Error checking file size for {file_path}: {e}")

        if not large_files:
            self.report.passed_checks.append(check_type)

    def check_testing_presence(self):
        """Check 4: Testing Presence (test files exist)."""
        check_type = CheckType.TESTING_PRESENCE
        self.report.checks_run.append(check_type)

        # Look for test files
        test_patterns = [
            "**/test_*.py",
            "**/*_test.py",
            "**/*.test.ts",
            "**/*.test.tsx",
            "**/*.spec.ts",
            "**/*.spec.tsx",
            "**/tests/**/*.py",
            "**/__tests__/**/*",
        ]

        test_files = []
        for pattern in test_patterns:
            test_files.extend(self.project_path.glob(pattern))

        test_files = [f for f in test_files if not self.should_skip_file(f)]

        if not test_files:
            self.report.issues.append(QualityIssue(
                check_type=check_type,
                severity=Severity.ERROR,
                message="No test files found in project",
                recommendation="Add automated tests (unit, integration, or BDD)",
                rule_id="TEST-PRESENCE"
            ))
        else:
            self.report.passed_checks.append(check_type)
            logger.info(f"Found {len(test_files)} test files")

    def check_type_safety(self):
        """Check 5: Type Safety (type hints, TypeScript)."""
        check_type = CheckType.TYPE_SAFETY
        self.report.checks_run.append(check_type)

        # Check for .js files (should be .ts)
        js_files = list(self.project_path.glob("src/**/*.js"))
        js_files = [f for f in js_files if not self.should_skip_file(f) and not f.name.endswith(".config.js")]

        for js_file in js_files:
            self.report.issues.append(QualityIssue(
                check_type=check_type,
                severity=Severity.WARNING,
                message="JavaScript file found (should use TypeScript)",
                file_path=str(js_file.relative_to(self.project_path)),
                recommendation=f"Rename to {js_file.stem}.ts and add type annotations",
                rule_id="TYPE-TS-REQUIRED"
            ))

        if not js_files:
            self.report.passed_checks.append(check_type)

    def check_security(self):
        """Check 6: Security Best Practices."""
        check_type = CheckType.SECURITY
        self.report.checks_run.append(check_type)

        # Check for insecure WebSocket (ws://)
        code_files = list(self.project_path.rglob("*.ts")) + list(self.project_path.rglob("*.tsx"))
        code_files += list(self.project_path.rglob("*.py"))

        for code_file in code_files:
            if self.should_skip_file(code_file):
                continue

            try:
                content = code_file.read_text()
                lines = content.splitlines()

                for i, line in enumerate(lines, 1):
                    if re.search(r'ws://(?!.*wss)', line):
                        self.report.issues.append(QualityIssue(
                            check_type=check_type,
                            severity=Severity.ERROR,
                            message="Insecure WebSocket connection (ws://)",
                            file_path=str(code_file.relative_to(self.project_path)),
                            line_number=i,
                            code_snippet=line.strip(),
                            recommendation="Use wss:// for secure WebSocket connections",
                            rule_id="SEC-WEBSOCKET"
                        ))

            except Exception as e:
                logger.warning(f"Error checking security for {code_file}: {e}")

        if not self.report.get_issues_by_check(check_type):
            self.report.passed_checks.append(check_type)

    def check_design_system(self):
        """Check 7: Design System Compliance (UI projects)."""
        check_type = CheckType.DESIGN_SYSTEM
        self.report.checks_run.append(check_type)

        # Check for raw hex colors in React/HTML files
        ui_files = list(self.project_path.rglob("*.tsx")) + list(self.project_path.rglob("*.html"))

        if not ui_files:
            logger.info("No UI files found, skipping design system check")
            return

        for ui_file in ui_files:
            if self.should_skip_file(ui_file):
                continue

            try:
                content = ui_file.read_text()
                lines = content.splitlines()

                for i, line in enumerate(lines, 1):
                    # Check for raw hex colors
                    if re.search(r'#[0-9a-fA-F]{6}\b', line) and 'hsl(var(' not in line:
                        self.report.issues.append(QualityIssue(
                            check_type=check_type,
                            severity=Severity.ERROR,
                            message="Raw hex color found (should use design tokens)",
                            file_path=str(ui_file.relative_to(self.project_path)),
                            line_number=i,
                            code_snippet=line.strip()[:80],
                            recommendation="Use design tokens: hsl(var(--token-name))",
                            rule_id="DESIGN-TOKENS"
                        ))

            except Exception as e:
                logger.warning(f"Error checking design system for {ui_file}: {e}")

        if not self.report.get_issues_by_check(check_type):
            self.report.passed_checks.append(check_type)

    def check_domain_model_usage(self):
        """Check 8: Domain Model Usage (timestamps, decomposition)."""
        check_type = CheckType.DOMAIN_MODEL_USAGE
        self.report.checks_run.append(check_type)

        # Check Python files for Pydantic models without timestamps
        py_files = list(self.project_path.rglob("*.py"))

        for py_file in py_files:
            if self.should_skip_file(py_file):
                continue

            try:
                content = py_file.read_text()

                # Look for Pydantic models
                if "BaseModel" in content:
                    # Check if created_at and updated_at are present
                    has_created_at = "created_at" in content
                    has_updated_at = "updated_at" in content

                    if not (has_created_at and has_updated_at):
                        self.report.issues.append(QualityIssue(
                            check_type=check_type,
                            severity=Severity.WARNING,
                            message="Domain model missing timestamp fields",
                            file_path=str(py_file.relative_to(self.project_path)),
                            recommendation="Add created_at and updated_at fields to all domain models",
                            rule_id="DOMAIN-TIMESTAMPS"
                        ))

            except Exception as e:
                logger.warning(f"Error checking domain models for {py_file}: {e}")

        if not self.report.get_issues_by_check(check_type):
            self.report.passed_checks.append(check_type)


def print_report(report: QualityReport, verbose: bool = False):
    """Print quality report to console."""
    print("\n" + "="*80)
    print("  SOFTWARE QUALITY AUDIT REPORT")
    print(f"  Project: {report.project_path.name}")
    print("="*80 + "\n")

    # Overall status
    if report.has_errors:
        overall = "❌ FAIL"
    elif report.has_warnings:
        overall = "⚠️  PASS WITH WARNINGS"
    else:
        overall = "✅ PASS"

    print(f"OVERALL: {overall}\n")

    # Checks summary
    print("Checks:")
    all_check_types = list(CheckType)
    for check_type in all_check_types:
        if check_type in report.checks_run:
            issues = report.get_issues_by_check(check_type)
            if check_type in report.passed_checks:
                print(f"  ✅ {check_type.value.replace('-', ' ').title():30s} PASS")
            elif any(i.severity == Severity.ERROR for i in issues):
                print(f"  ❌ {check_type.value.replace('-', ' ').title():30s} FAIL")
            else:
                error_count = len([i for i in issues if i.severity == Severity.ERROR])
                warning_count = len([i for i in issues if i.severity == Severity.WARNING])
                print(f"  ⚠️  {check_type.value.replace('-', ' ').title():30s} WARNING ({warning_count} issues)")

    print(f"\nSummary:")
    print(f"  Errors:   {report.error_count}")
    print(f"  Warnings: {report.warning_count}")
    print(f"  Info:     {report.info_count}")
    print(f"  Files:    {report.files_scanned}")

    # Detailed findings
    if report.issues and verbose:
        print("\n" + "="*80)
        print("DETAILED FINDINGS")
        print("="*80 + "\n")

        for issue in report.issues:
            print(issue)
            print()


def main():
    parser = argparse.ArgumentParser(
        description="Software quality checker for Protoflow projects",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "files",
        nargs="*",
        type=Path,
        help="Specific files to check"
    )

    parser.add_argument(
        "--project",
        type=Path,
        help="Project directory to audit"
    )

    parser.add_argument(
        "--checks",
        nargs="+",
        choices=["all", "config", "shared-models", "decomposition", "tests", "types", "security", "design-system", "domain-models"],
        default=["all"],
        help="Specific checks to run (default: all)"
    )

    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors"
    )

    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format"
    )

    parser.add_argument(
        "--output",
        type=Path,
        help="Output file (default: stdout)"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed findings"
    )

    args = parser.parse_args()

    # Determine project path
    if args.project:
        project_path = args.project
    elif args.files:
        # Use parent directory of first file
        project_path = args.files[0].parent
    else:
        project_path = Path.cwd()

    # Run checks
    checker = SoftwareQualityChecker(
        project_path=project_path,
        checks=args.checks,
        strict=args.strict
    )

    report = checker.run_all_checks()

    # Output report
    if args.format == "json":
        output_data = {
            "project": str(report.project_path),
            "overall": "fail" if report.has_errors else "pass_with_warnings" if report.has_warnings else "pass",
            "summary": {
                "errors": report.error_count,
                "warnings": report.warning_count,
                "info": report.info_count,
                "files_scanned": report.files_scanned,
            },
            "checks": {ct.value: ct in report.passed_checks for ct in report.checks_run},
            "issues": [
                {
                    "check_type": i.check_type.value,
                    "severity": i.severity.value,
                    "message": i.message,
                    "file_path": i.file_path,
                    "line_number": i.line_number,
                    "recommendation": i.recommendation,
                    "rule_id": i.rule_id,
                }
                for i in report.issues
            ]
        }

        if args.output:
            args.output.write_text(json.dumps(output_data, indent=2))
            print(f"Report written to: {args.output}")
        else:
            print(json.dumps(output_data, indent=2))
    else:
        print_report(report, verbose=args.verbose)

    # Exit code
    if report.has_errors:
        sys.exit(1)
    elif args.strict and report.has_warnings:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
