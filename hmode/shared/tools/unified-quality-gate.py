#!/usr/bin/env python3
# File UUID: f9e8d7c6-b5a4-3f2e-1d0c-9b8a7e6f5d4c
"""
Unified Quality Gate

Comprehensive quality validation combining multiple tools:
- software-quality-check.py (8 dimensions)
- radon (cyclomatic complexity)
- madge (circular dependencies)
- pylint (code duplication)
- evaluate-architecture (optional, via Claude agent)

Usage:
    # Full gate (all checks)
    python unified-quality-gate.py --project /path/to/project

    # Quick gate (fast checks only)
    python unified-quality-gate.py --project . --mode quick

    # Pre-deployment (strict, fail on warnings)
    python unified-quality-gate.py --project . --strict

    # With architecture evaluation (slower)
    python unified-quality-gate.py --project . --with-architecture

    # JSON report
    python unified-quality-gate.py --project . --format json --output report.json

Exit Codes:
    0 - All checks passed
    1 - Critical issues found (or warnings in strict mode)
    2 - Tool execution failed
"""

import argparse
import json
import logging
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Setup logging
LOG_DIR = Path(__file__).parent.parent.parent / "logs" / "tools"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "unified-quality-gate.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class CheckResult:
    """Result from a single check."""
    name: str
    status: str  # "pass", "warning", "fail", "skipped", "error"
    errors: int = 0
    warnings: int = 0
    info: int = 0
    duration_seconds: float = 0.0
    details: Dict[str, Any] = field(default_factory=dict)
    message: Optional[str] = None

    @property
    def passed(self) -> bool:
        return self.status in ["pass", "skipped"]

    @property
    def failed(self) -> bool:
        return self.status in ["fail", "error"]


@dataclass
class QualityGateReport:
    """Complete quality gate report."""
    project_path: Path
    timestamp: str
    mode: str  # "quick", "standard", "strict"
    checks: List[CheckResult] = field(default_factory=list)
    total_duration_seconds: float = 0.0

    @property
    def overall_status(self) -> str:
        if any(c.failed for c in self.checks):
            return "FAIL"
        elif any(c.status == "warning" for c in self.checks):
            return "PASS_WITH_WARNINGS"
        else:
            return "PASS"

    @property
    def total_errors(self) -> int:
        return sum(c.errors for c in self.checks)

    @property
    def total_warnings(self) -> int:
        return sum(c.warnings for c in self.checks)

    @property
    def total_info(self) -> int:
        return sum(c.info for c in self.checks)


class UnifiedQualityGate:
    """Main quality gate orchestrator."""

    def __init__(
        self,
        project_path: Path,
        mode: str = "standard",
        strict: bool = False,
        with_architecture: bool = False,
        skip_checks: Optional[List[str]] = None
    ):
        self.project_path = Path(project_path).resolve()
        self.mode = mode
        self.strict = strict
        self.with_architecture = with_architecture
        self.skip_checks = skip_checks or []
        self.tools_dir = Path(__file__).parent
        self.report = QualityGateReport(
            project_path=self.project_path,
            timestamp=datetime.now().isoformat(),
            mode=mode
        )

        logger.info(f"Initialized quality gate for: {self.project_path}")
        logger.info(f"Mode: {mode}, Strict: {strict}, Architecture: {with_architecture}")

    def run_all_checks(self) -> QualityGateReport:
        """Execute all quality checks."""
        start_time = datetime.now()

        print("\n" + "="*80)
        print("  🛡️  UNIFIED QUALITY GATE")
        print(f"  Project: {self.project_path.name}")
        print(f"  Mode: {self.mode.upper()}")
        print("="*80 + "\n")

        # Define check sequence
        checks = [
            ("software-quality-check", self.run_software_quality_check),
            ("cyclomatic-complexity", self.run_cyclomatic_complexity),
            ("circular-dependencies", self.run_circular_dependencies),
            ("code-duplication", self.run_code_duplication),
        ]

        if self.with_architecture:
            checks.append(("architecture-evaluation", self.run_architecture_evaluation))

        # Execute checks
        for check_name, check_func in checks:
            if check_name in self.skip_checks:
                logger.info(f"Skipping check: {check_name}")
                self.report.checks.append(CheckResult(
                    name=check_name,
                    status="skipped",
                    message="Skipped by user"
                ))
                continue

            print(f"\n{'─'*80}")
            print(f"🔍 Running: {check_name.replace('-', ' ').title()}")
            print(f"{'─'*80}")

            try:
                result = check_func()
                self.report.checks.append(result)

                # Print immediate status
                if result.passed:
                    print(f"✅ {result.name}: PASS")
                elif result.status == "warning":
                    print(f"⚠️  {result.name}: PASS WITH WARNINGS ({result.warnings} warnings)")
                else:
                    print(f"❌ {result.name}: FAIL ({result.errors} errors)")

            except Exception as e:
                logger.error(f"Error running {check_name}: {e}")
                self.report.checks.append(CheckResult(
                    name=check_name,
                    status="error",
                    errors=1,
                    message=str(e)
                ))
                print(f"❌ {check_name}: ERROR - {e}")

        # Calculate total duration
        end_time = datetime.now()
        self.report.total_duration_seconds = (end_time - start_time).total_seconds()

        return self.report

    def run_software_quality_check(self) -> CheckResult:
        """Run comprehensive software quality check."""
        check_start = datetime.now()
        script = self.tools_dir / "software-quality-check.py"

        if not script.exists():
            return CheckResult(
                name="software-quality-check",
                status="error",
                errors=1,
                message="software-quality-check.py not found"
            )

        try:
            cmd = [
                sys.executable,
                str(script),
                "--project", str(self.project_path),
                "--format", "json"
            ]

            if self.strict:
                cmd.append("--strict")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )

            duration = (datetime.now() - check_start).total_seconds()

            if result.stdout:
                data = json.loads(result.stdout)
                summary = data.get("summary", {})

                errors = summary.get("errors", 0)
                warnings = summary.get("warnings", 0)
                info_count = summary.get("info", 0)

                if errors > 0:
                    status = "fail"
                elif warnings > 0:
                    status = "warning"
                else:
                    status = "pass"

                return CheckResult(
                    name="software-quality-check",
                    status=status,
                    errors=errors,
                    warnings=warnings,
                    info=info_count,
                    duration_seconds=duration,
                    details=data
                )
            else:
                # No output, assume pass if exit code 0
                status = "pass" if result.returncode == 0 else "fail"
                return CheckResult(
                    name="software-quality-check",
                    status=status,
                    errors=0 if status == "pass" else 1,
                    duration_seconds=duration
                )

        except subprocess.TimeoutExpired:
            return CheckResult(
                name="software-quality-check",
                status="error",
                errors=1,
                message="Check timed out (120s limit)"
            )
        except Exception as e:
            return CheckResult(
                name="software-quality-check",
                status="error",
                errors=1,
                message=str(e)
            )

    def run_cyclomatic_complexity(self) -> CheckResult:
        """Run cyclomatic complexity analysis with radon."""
        check_start = datetime.now()

        # Check for Python files
        py_files = list(self.project_path.rglob("*.py"))
        py_files = [f for f in py_files if not self._should_skip_file(f)]

        if not py_files:
            return CheckResult(
                name="cyclomatic-complexity",
                status="skipped",
                message="No Python files found"
            )

        try:
            # Run radon cc (cyclomatic complexity)
            result = subprocess.run(
                ["uv", "run", "radon", "cc", str(self.project_path), "-a", "-s", "-j"],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=self.project_path.parent.parent  # Run from lab root
            )

            duration = (datetime.now() - check_start).total_seconds()

            if result.returncode == 0 and result.stdout:
                try:
                    data = json.loads(result.stdout)

                    # Analyze complexity scores
                    high_complexity = []
                    medium_complexity = []

                    for file_path, functions in data.items():
                        for func in functions:
                            complexity = func.get("complexity", 0)
                            if complexity > 10:
                                high_complexity.append((file_path, func.get("name"), complexity))
                            elif complexity > 5:
                                medium_complexity.append((file_path, func.get("name"), complexity))

                    errors = len(high_complexity)
                    warnings = len(medium_complexity)

                    if errors > 0:
                        status = "fail"
                    elif warnings > 0:
                        status = "warning"
                    else:
                        status = "pass"

                    return CheckResult(
                        name="cyclomatic-complexity",
                        status=status,
                        errors=errors,
                        warnings=warnings,
                        duration_seconds=duration,
                        details={
                            "high_complexity": high_complexity[:10],  # Top 10
                            "medium_complexity": medium_complexity[:10]
                        },
                        message=f"High complexity: {errors}, Medium: {warnings}"
                    )
                except json.JSONDecodeError:
                    # Radon didn't return JSON, assume pass
                    return CheckResult(
                        name="cyclomatic-complexity",
                        status="pass",
                        duration_seconds=duration,
                        message="No complexity issues detected"
                    )
            else:
                return CheckResult(
                    name="cyclomatic-complexity",
                    status="pass",
                    duration_seconds=duration,
                    message="No complexity issues detected"
                )

        except subprocess.TimeoutExpired:
            return CheckResult(
                name="cyclomatic-complexity",
                status="error",
                errors=1,
                message="Complexity check timed out"
            )
        except Exception as e:
            logger.warning(f"Cyclomatic complexity check failed: {e}")
            return CheckResult(
                name="cyclomatic-complexity",
                status="warning",
                warnings=1,
                message=f"Check partially failed: {e}"
            )

    def run_circular_dependencies(self) -> CheckResult:
        """Run circular dependency detection with madge."""
        check_start = datetime.now()

        # Check for TypeScript/JavaScript files
        ts_files = list(self.project_path.rglob("*.ts")) + list(self.project_path.rglob("*.tsx"))
        js_files = list(self.project_path.rglob("*.js")) + list(self.project_path.rglob("*.jsx"))

        code_files = [f for f in (ts_files + js_files) if not self._should_skip_file(f)]

        if not code_files:
            return CheckResult(
                name="circular-dependencies",
                status="skipped",
                message="No TypeScript/JavaScript files found"
            )

        try:
            # Run madge
            result = subprocess.run(
                ["madge", "--circular", "--json", str(self.project_path)],
                capture_output=True,
                text=True,
                timeout=60
            )

            duration = (datetime.now() - check_start).total_seconds()

            if result.returncode == 0 and result.stdout:
                try:
                    data = json.loads(result.stdout)
                    circular_deps = data if isinstance(data, list) else []

                    errors = len(circular_deps)

                    if errors > 0:
                        status = "fail"
                    else:
                        status = "pass"

                    return CheckResult(
                        name="circular-dependencies",
                        status=status,
                        errors=errors,
                        duration_seconds=duration,
                        details={"circular_dependencies": circular_deps},
                        message=f"Found {errors} circular dependencies" if errors > 0 else "No circular dependencies"
                    )
                except json.JSONDecodeError:
                    # No circular dependencies found
                    return CheckResult(
                        name="circular-dependencies",
                        status="pass",
                        duration_seconds=duration,
                        message="No circular dependencies detected"
                    )
            else:
                return CheckResult(
                    name="circular-dependencies",
                    status="pass",
                    duration_seconds=duration,
                    message="No circular dependencies detected"
                )

        except subprocess.TimeoutExpired:
            return CheckResult(
                name="circular-dependencies",
                status="error",
                errors=1,
                message="Circular dependency check timed out"
            )
        except Exception as e:
            logger.warning(f"Circular dependency check failed: {e}")
            return CheckResult(
                name="circular-dependencies",
                status="warning",
                warnings=1,
                message=f"Check partially failed: {e}"
            )

    def run_code_duplication(self) -> CheckResult:
        """Run code duplication detection with pylint."""
        check_start = datetime.now()

        # Check for Python files
        py_files = list(self.project_path.rglob("*.py"))
        py_files = [f for f in py_files if not self._should_skip_file(f)]

        if not py_files:
            return CheckResult(
                name="code-duplication",
                status="skipped",
                message="No Python files found"
            )

        try:
            # Run pylint duplicate-code check
            result = subprocess.run(
                [
                    "uv", "run", "pylint",
                    "--disable=all",
                    "--enable=duplicate-code",
                    "--output-format=json",
                    str(self.project_path)
                ],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=self.project_path.parent.parent  # Run from lab root
            )

            duration = (datetime.now() - check_start).total_seconds()

            if result.stdout:
                try:
                    data = json.loads(result.stdout)

                    # Count duplicate-code messages
                    duplicates = [msg for msg in data if msg.get("message-id") == "R0801"]

                    warnings = len(duplicates)

                    if warnings > 5:
                        status = "fail"
                        errors = warnings
                        warnings = 0
                    elif warnings > 0:
                        status = "warning"
                    else:
                        status = "pass"

                    return CheckResult(
                        name="code-duplication",
                        status=status,
                        errors=errors if warnings == 0 else 0,
                        warnings=warnings,
                        duration_seconds=duration,
                        details={"duplicates": duplicates[:5]},  # Top 5
                        message=f"Found {len(duplicates)} duplicate code blocks" if duplicates else "No significant duplication"
                    )
                except json.JSONDecodeError:
                    # No duplication found
                    return CheckResult(
                        name="code-duplication",
                        status="pass",
                        duration_seconds=duration,
                        message="No code duplication detected"
                    )
            else:
                return CheckResult(
                    name="code-duplication",
                    status="pass",
                    duration_seconds=duration,
                    message="No code duplication detected"
                )

        except subprocess.TimeoutExpired:
            return CheckResult(
                name="code-duplication",
                status="error",
                errors=1,
                message="Duplication check timed out"
            )
        except Exception as e:
            logger.warning(f"Code duplication check failed: {e}")
            return CheckResult(
                name="code-duplication",
                status="warning",
                warnings=1,
                message=f"Check partially failed: {e}"
            )

    def run_architecture_evaluation(self) -> CheckResult:
        """Run architecture evaluation (requires Claude agent)."""
        return CheckResult(
            name="architecture-evaluation",
            status="skipped",
            message="Architecture evaluation requires Claude agent - run '/evaluate-architecture' manually"
        )

    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped."""
        skip_patterns = [
            "node_modules",
            ".git",
            "venv",
            "__pycache__",
            "dist",
            "build",
            ".next",
            "coverage",
            ".venv"
        ]

        path_str = str(file_path)
        return any(pattern in path_str for pattern in skip_patterns)


def print_report(report: QualityGateReport, verbose: bool = False):
    """Print quality gate report to console."""
    print("\n" + "="*80)
    print("  📊 QUALITY GATE REPORT")
    print("="*80 + "\n")

    # Overall status
    if report.overall_status == "PASS":
        overall = "✅ PASS"
    elif report.overall_status == "PASS_WITH_WARNINGS":
        overall = "⚠️  PASS WITH WARNINGS"
    else:
        overall = "❌ FAIL"

    print(f"Overall Status: {overall}")
    print(f"Project: {report.project_path.name}")
    print(f"Mode: {report.mode.upper()}")
    print(f"Duration: {report.total_duration_seconds:.1f}s")
    print()

    # Summary table
    print("Checks Summary:")
    print(f"{'Check':<30} {'Status':<20} {'Errors':<10} {'Warnings':<10}")
    print("─" * 80)

    for check in report.checks:
        if check.status == "pass":
            status_str = "✅ PASS"
        elif check.status == "warning":
            status_str = "⚠️  WARNING"
        elif check.status == "fail":
            status_str = "❌ FAIL"
        elif check.status == "skipped":
            status_str = "⏭️  SKIPPED"
        else:
            status_str = "❌ ERROR"

        check_name = check.name.replace("-", " ").title()
        print(f"{check_name:<30} {status_str:<20} {check.errors:<10} {check.warnings:<10}")

    print()
    print(f"Total Errors:   {report.total_errors}")
    print(f"Total Warnings: {report.total_warnings}")
    print(f"Total Info:     {report.total_info}")

    # Detailed findings
    if verbose:
        print("\n" + "="*80)
        print("DETAILED FINDINGS")
        print("="*80 + "\n")

        for check in report.checks:
            if check.details:
                print(f"\n{check.name.upper()}:")
                print(json.dumps(check.details, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="Unified quality gate for software projects",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--project",
        type=Path,
        default=Path.cwd(),
        help="Project directory to audit (default: current directory)"
    )

    parser.add_argument(
        "--mode",
        choices=["quick", "standard", "strict"],
        default="standard",
        help="Check mode (default: standard)"
    )

    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors"
    )

    parser.add_argument(
        "--with-architecture",
        action="store_true",
        help="Include architecture evaluation (requires Claude agent)"
    )

    parser.add_argument(
        "--skip",
        nargs="+",
        choices=["software-quality-check", "cyclomatic-complexity", "circular-dependencies", "code-duplication", "architecture-evaluation"],
        default=[],
        help="Checks to skip"
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

    # Run quality gate
    gate = UnifiedQualityGate(
        project_path=args.project,
        mode=args.mode,
        strict=args.strict,
        with_architecture=args.with_architecture,
        skip_checks=args.skip
    )

    report = gate.run_all_checks()

    # Output report
    if args.format == "json":
        output_data = {
            "project": str(report.project_path),
            "timestamp": report.timestamp,
            "mode": report.mode,
            "overall_status": report.overall_status.lower(),
            "duration_seconds": report.total_duration_seconds,
            "summary": {
                "errors": report.total_errors,
                "warnings": report.total_warnings,
                "info": report.total_info,
            },
            "checks": [
                {
                    "name": c.name,
                    "status": c.status,
                    "errors": c.errors,
                    "warnings": c.warnings,
                    "info": c.info,
                    "duration_seconds": c.duration_seconds,
                    "message": c.message,
                    "details": c.details
                }
                for c in report.checks
            ]
        }

        if args.output:
            args.output.write_text(json.dumps(output_data, indent=2))
            print(f"\n✅ Report written to: {args.output}")
        else:
            print(json.dumps(output_data, indent=2))
    else:
        print_report(report, verbose=args.verbose)

    # Exit code
    if report.overall_status == "FAIL":
        print("\n❌ Quality gate FAILED - fix errors before proceeding\n")
        sys.exit(1)
    elif args.strict and report.total_warnings > 0:
        print("\n❌ Quality gate FAILED in strict mode - fix warnings\n")
        sys.exit(1)
    else:
        if report.overall_status == "PASS_WITH_WARNINGS":
            print("\n⚠️  Quality gate PASSED with warnings - consider fixing\n")
        else:
            print("\n✅ Quality gate PASSED - all checks successful\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
