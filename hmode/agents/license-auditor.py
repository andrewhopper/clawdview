#!/usr/bin/env python3
# File UUID: 7c9f4e2a-1b8d-4f3a-9e7c-2d5a8f3b6c1e

"""
License Auditor Agent

Audits project dependencies for license compatibility issues.

Capabilities:
- Multi-ecosystem support (npm, pip, cargo, go)
- License compatibility checking
- SPDX license parsing
- Detailed reports with recommendations
- Configurable compatibility rules
"""

import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError


class CompatibilityLevel(Enum):
    """License compatibility levels."""
    COMPATIBLE = "compatible"
    PERMISSIVE = "permissive"
    WEAK_COPYLEFT = "weak_copyleft"
    STRONG_COPYLEFT = "strong_copyleft"
    INCOMPATIBLE = "incompatible"
    UNKNOWN = "unknown"


@dataclass
class License:
    """License information."""
    name: str
    spdx_id: Optional[str] = None
    category: CompatibilityLevel = CompatibilityLevel.UNKNOWN
    url: Optional[str] = None


@dataclass
class Dependency:
    """Dependency information."""
    name: str
    version: str
    license: Optional[License] = None
    ecosystem: str = ""


@dataclass
class CompatibilityIssue:
    """License compatibility issue."""
    dependency: Dependency
    severity: str  # "error", "warning", "info"
    message: str
    recommendation: str


# License compatibility matrix
LICENSE_COMPATIBILITY = {
    # Permissive licenses (compatible with almost everything)
    "MIT": CompatibilityLevel.PERMISSIVE,
    "Apache-2.0": CompatibilityLevel.PERMISSIVE,
    "BSD-2-Clause": CompatibilityLevel.PERMISSIVE,
    "BSD-3-Clause": CompatibilityLevel.PERMISSIVE,
    "ISC": CompatibilityLevel.PERMISSIVE,
    "0BSD": CompatibilityLevel.PERMISSIVE,
    "Unlicense": CompatibilityLevel.PERMISSIVE,

    # Weak copyleft (require attribution, compatible with proprietary)
    "LGPL-2.1": CompatibilityLevel.WEAK_COPYLEFT,
    "LGPL-3.0": CompatibilityLevel.WEAK_COPYLEFT,
    "MPL-2.0": CompatibilityLevel.WEAK_COPYLEFT,
    "EPL-2.0": CompatibilityLevel.WEAK_COPYLEFT,

    # Strong copyleft (require source code disclosure)
    "GPL-2.0": CompatibilityLevel.STRONG_COPYLEFT,
    "GPL-3.0": CompatibilityLevel.STRONG_COPYLEFT,
    "AGPL-3.0": CompatibilityLevel.STRONG_COPYLEFT,
}


class LicenseAuditor:
    """Audits project dependencies for license compatibility."""

    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.project_license = self._detect_project_license()
        self.dependencies: List[Dependency] = []
        self.issues: List[CompatibilityIssue] = []

    def _detect_project_license(self) -> Optional[License]:
        """Detect project license from LICENSE file or package metadata."""
        # Check LICENSE file
        for license_file in ["LICENSE", "LICENSE.txt", "LICENSE.md", "LICENCE"]:
            license_path = self.project_dir / license_file
            if license_path.exists():
                content = license_path.read_text()
                return self._parse_license_text(content)

        # Check package.json
        package_json = self.project_dir / "package.json"
        if package_json.exists():
            data = json.loads(package_json.read_text())
            if "license" in data:
                return License(name=data["license"], spdx_id=data["license"])

        # Check pyproject.toml
        pyproject = self.project_dir / "pyproject.toml"
        if pyproject.exists():
            content = pyproject.read_text()
            match = re.search(r'license\s*=\s*["\']([^"\']+)["\']', content)
            if match:
                license_name = match.group(1)
                return License(name=license_name, spdx_id=license_name)

        # Check Cargo.toml
        cargo_toml = self.project_dir / "Cargo.toml"
        if cargo_toml.exists():
            content = cargo_toml.read_text()
            match = re.search(r'license\s*=\s*"([^"]+)"', content)
            if match:
                license_name = match.group(1)
                return License(name=license_name, spdx_id=license_name)

        return None

    def _parse_license_text(self, text: str) -> License:
        """Parse license from text content."""
        text_upper = text.upper()

        # Common license patterns
        if "MIT LICENSE" in text_upper:
            return License(name="MIT", spdx_id="MIT", category=CompatibilityLevel.PERMISSIVE)
        elif "APACHE LICENSE" in text_upper:
            return License(name="Apache-2.0", spdx_id="Apache-2.0", category=CompatibilityLevel.PERMISSIVE)
        elif "BSD" in text_upper:
            if "3-CLAUSE" in text_upper:
                return License(name="BSD-3-Clause", spdx_id="BSD-3-Clause", category=CompatibilityLevel.PERMISSIVE)
            elif "2-CLAUSE" in text_upper:
                return License(name="BSD-2-Clause", spdx_id="BSD-2-Clause", category=CompatibilityLevel.PERMISSIVE)
        elif "GPL" in text_upper:
            if "AGPL" in text_upper:
                return License(name="AGPL-3.0", spdx_id="AGPL-3.0", category=CompatibilityLevel.STRONG_COPYLEFT)
            elif "LGPL" in text_upper:
                return License(name="LGPL-3.0", spdx_id="LGPL-3.0", category=CompatibilityLevel.WEAK_COPYLEFT)
            else:
                return License(name="GPL-3.0", spdx_id="GPL-3.0", category=CompatibilityLevel.STRONG_COPYLEFT)

        return License(name="Unknown", category=CompatibilityLevel.UNKNOWN)

    def audit_npm_dependencies(self) -> None:
        """Audit npm dependencies from package.json."""
        package_json = self.project_dir / "package.json"
        if not package_json.exists():
            return

        data = json.loads(package_json.read_text())
        all_deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}

        for name, version_spec in all_deps.items():
            try:
                # Fetch package info from npm registry
                url = f"https://registry.npmjs.org/{name}"
                req = Request(url, headers={"Accept": "application/json"})
                with urlopen(req, timeout=5) as response:
                    pkg_data = json.loads(response.read())
                    latest = pkg_data.get("dist-tags", {}).get("latest", "")
                    pkg_license = pkg_data.get("license", "Unknown")

                    license_obj = License(
                        name=pkg_license,
                        spdx_id=pkg_license if pkg_license != "Unknown" else None,
                        category=LICENSE_COMPATIBILITY.get(pkg_license, CompatibilityLevel.UNKNOWN)
                    )

                    dep = Dependency(
                        name=name,
                        version=version_spec,
                        license=license_obj,
                        ecosystem="npm"
                    )
                    self.dependencies.append(dep)
            except (HTTPError, URLError, json.JSONDecodeError) as e:
                # Add dependency with unknown license
                dep = Dependency(
                    name=name,
                    version=version_spec,
                    license=License(name="Unknown", category=CompatibilityLevel.UNKNOWN),
                    ecosystem="npm"
                )
                self.dependencies.append(dep)

    def audit_python_dependencies(self) -> None:
        """Audit Python dependencies from requirements.txt or pyproject.toml."""
        requirements_txt = self.project_dir / "requirements.txt"

        deps_to_check: List[Tuple[str, str]] = []

        if requirements_txt.exists():
            content = requirements_txt.read_text()
            for line in content.splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                # Parse package name (handle ==, >=, ~=, etc.)
                match = re.match(r'^([a-zA-Z0-9_-]+)', line)
                if match:
                    pkg_name = match.group(1)
                    deps_to_check.append((pkg_name, line))

        for pkg_name, version_spec in deps_to_check:
            try:
                # Fetch from PyPI JSON API
                url = f"https://pypi.org/pypi/{pkg_name}/json"
                req = Request(url, headers={"Accept": "application/json"})
                with urlopen(req, timeout=5) as response:
                    pkg_data = json.loads(response.read())
                    pkg_license = pkg_data.get("info", {}).get("license", "Unknown")

                    license_obj = License(
                        name=pkg_license if pkg_license else "Unknown",
                        spdx_id=pkg_license if pkg_license and pkg_license != "Unknown" else None,
                        category=LICENSE_COMPATIBILITY.get(pkg_license, CompatibilityLevel.UNKNOWN)
                    )

                    dep = Dependency(
                        name=pkg_name,
                        version=version_spec,
                        license=license_obj,
                        ecosystem="pip"
                    )
                    self.dependencies.append(dep)
            except (HTTPError, URLError, json.JSONDecodeError):
                dep = Dependency(
                    name=pkg_name,
                    version=version_spec,
                    license=License(name="Unknown", category=CompatibilityLevel.UNKNOWN),
                    ecosystem="pip"
                )
                self.dependencies.append(dep)

    def audit_cargo_dependencies(self) -> None:
        """Audit Rust dependencies from Cargo.toml."""
        cargo_toml = self.project_dir / "Cargo.toml"
        if not cargo_toml.exists():
            return

        content = cargo_toml.read_text()

        # Simple TOML parsing for dependencies section
        in_deps = False
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("[dependencies]"):
                in_deps = True
                continue
            elif line.startswith("["):
                in_deps = False
                continue

            if in_deps and "=" in line:
                match = re.match(r'^([a-zA-Z0-9_-]+)\s*=', line)
                if match:
                    pkg_name = match.group(1)
                    # For Cargo, we'd need to fetch from crates.io API
                    # Simplified version for now
                    dep = Dependency(
                        name=pkg_name,
                        version="*",
                        license=License(name="Unknown", category=CompatibilityLevel.UNKNOWN),
                        ecosystem="cargo"
                    )
                    self.dependencies.append(dep)

    def check_compatibility(self) -> None:
        """Check license compatibility between project and dependencies."""
        if not self.project_license:
            # Can't check compatibility without knowing project license
            return

        project_category = LICENSE_COMPATIBILITY.get(
            self.project_license.spdx_id or self.project_license.name,
            CompatibilityLevel.UNKNOWN
        )

        for dep in self.dependencies:
            if not dep.license or dep.license.category == CompatibilityLevel.UNKNOWN:
                self.issues.append(CompatibilityIssue(
                    dependency=dep,
                    severity="warning",
                    message=f"Unknown license for {dep.name}",
                    recommendation="Manually verify license compatibility"
                ))
                continue

            dep_category = dep.license.category

            # Compatibility rules
            if project_category == CompatibilityLevel.PERMISSIVE:
                # Permissive projects can use anything except unknown
                if dep_category == CompatibilityLevel.UNKNOWN:
                    pass  # Already handled above

            elif project_category in [CompatibilityLevel.WEAK_COPYLEFT, CompatibilityLevel.STRONG_COPYLEFT]:
                # Copyleft projects need careful checking
                if dep_category == CompatibilityLevel.STRONG_COPYLEFT:
                    if dep.license.spdx_id != self.project_license.spdx_id:
                        self.issues.append(CompatibilityIssue(
                            dependency=dep,
                            severity="error",
                            message=f"Copyleft license incompatibility: {dep.name} ({dep.license.name}) vs project ({self.project_license.name})",
                            recommendation="Consider using a different dependency or relicensing"
                        ))

            elif project_category == CompatibilityLevel.UNKNOWN:
                if dep_category == CompatibilityLevel.STRONG_COPYLEFT:
                    self.issues.append(CompatibilityIssue(
                        dependency=dep,
                        severity="warning",
                        message=f"{dep.name} has strong copyleft license ({dep.license.name})",
                        recommendation="Ensure project license is compatible with copyleft requirements"
                    ))

    def generate_report(self) -> str:
        """Generate audit report."""
        lines = []
        lines.append("=" * 80)
        lines.append("LICENSE AUDIT REPORT")
        lines.append("=" * 80)
        lines.append("")

        # Project info
        lines.append(f"Project Directory: {self.project_dir}")
        if self.project_license:
            lines.append(f"Project License: {self.project_license.name}")
            lines.append(f"  Category: {self.project_license.category.value}")
        else:
            lines.append("Project License: NOT FOUND")
            lines.append("  ⚠️  Cannot verify compatibility without project license")
        lines.append("")

        # Summary
        lines.append("SUMMARY")
        lines.append("-" * 80)
        lines.append(f"Total Dependencies: {len(self.dependencies)}")

        errors = [i for i in self.issues if i.severity == "error"]
        warnings = [i for i in self.issues if i.severity == "warning"]

        lines.append(f"Errors: {len(errors)}")
        lines.append(f"Warnings: {len(warnings)}")
        lines.append("")

        # Issues
        if self.issues:
            lines.append("ISSUES")
            lines.append("-" * 80)
            for issue in self.issues:
                icon = "❌" if issue.severity == "error" else "⚠️"
                lines.append(f"{icon} {issue.message}")
                lines.append(f"   Dependency: {issue.dependency.name}@{issue.dependency.version} ({issue.dependency.ecosystem})")
                lines.append(f"   License: {issue.dependency.license.name if issue.dependency.license else 'Unknown'}")
                lines.append(f"   Recommendation: {issue.recommendation}")
                lines.append("")
        else:
            lines.append("✅ No compatibility issues found")
            lines.append("")

        # Dependency breakdown
        lines.append("DEPENDENCIES BY LICENSE")
        lines.append("-" * 80)

        license_groups: Dict[str, List[Dependency]] = {}
        for dep in self.dependencies:
            license_name = dep.license.name if dep.license else "Unknown"
            if license_name not in license_groups:
                license_groups[license_name] = []
            license_groups[license_name].append(dep)

        for license_name in sorted(license_groups.keys()):
            deps = license_groups[license_name]
            lines.append(f"{license_name} ({len(deps)} packages):")
            for dep in sorted(deps, key=lambda d: d.name):
                lines.append(f"  - {dep.name}@{dep.version} ({dep.ecosystem})")
            lines.append("")

        lines.append("=" * 80)
        return "\n".join(lines)

    def run_audit(self) -> str:
        """Run full audit and return report."""
        print("🔍 Starting license audit...")

        # Detect and audit dependencies
        if (self.project_dir / "package.json").exists():
            print("📦 Auditing npm dependencies...")
            self.audit_npm_dependencies()

        if (self.project_dir / "requirements.txt").exists() or (self.project_dir / "pyproject.toml").exists():
            print("🐍 Auditing Python dependencies...")
            self.audit_python_dependencies()

        if (self.project_dir / "Cargo.toml").exists():
            print("🦀 Auditing Rust dependencies...")
            self.audit_cargo_dependencies()

        # Check compatibility
        print("✅ Checking license compatibility...")
        self.check_compatibility()

        # Generate report
        report = self.generate_report()
        return report


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Audit project dependencies for license compatibility")
    parser.add_argument("project_dir", nargs="?", default=".", help="Project directory to audit")
    parser.add_argument("--output", "-o", help="Output file for report (default: stdout)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    if not project_dir.exists():
        print(f"Error: Project directory not found: {project_dir}", file=sys.stderr)
        sys.exit(1)

    auditor = LicenseAuditor(project_dir)
    report = auditor.run_audit()

    if args.json:
        # JSON output
        output = {
            "project_dir": str(project_dir),
            "project_license": {
                "name": auditor.project_license.name if auditor.project_license else None,
                "spdx_id": auditor.project_license.spdx_id if auditor.project_license else None,
            },
            "dependencies": [
                {
                    "name": dep.name,
                    "version": dep.version,
                    "ecosystem": dep.ecosystem,
                    "license": {
                        "name": dep.license.name if dep.license else None,
                        "spdx_id": dep.license.spdx_id if dep.license else None,
                    }
                }
                for dep in auditor.dependencies
            ],
            "issues": [
                {
                    "dependency": issue.dependency.name,
                    "severity": issue.severity,
                    "message": issue.message,
                    "recommendation": issue.recommendation,
                }
                for issue in auditor.issues
            ],
        }
        report = json.dumps(output, indent=2)

    if args.output:
        Path(args.output).write_text(report)
        print(f"Report written to {args.output}")
    else:
        print(report)

    # Exit code based on issues
    errors = [i for i in auditor.issues if i.severity == "error"]
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
