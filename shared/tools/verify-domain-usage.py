#!/usr/bin/env python3
"""
Verify Shared Domain Model Usage

Scans projects for usage of shared domain models from shared/semantic/domains/.
Reports which projects properly reuse shared domains vs. defining their own models.

File UUID: d4f2c8a1-5b7e-4d3f-a9c2-1e6d8f3a7b4c
"""

import os
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict


@dataclass
class DomainUsage:
    """Track domain model usage in a project."""
    project_path: str
    project_name: str
    shared_domains_used: List[str]
    local_pydantic_models: List[Tuple[str, str]]  # (file_path, model_name)
    local_typescript_models: List[Tuple[str, str]]  # (file_path, model_name)
    shared_import_count: int
    local_model_count: int
    compliance_score: float


@dataclass
class ScanReport:
    """Overall scan report."""
    total_projects: int
    projects_using_shared: int
    projects_with_local_only: int
    total_shared_imports: int
    total_local_models: int
    domain_usage: List[DomainUsage]
    shared_domains_available: List[str]


class DomainUsageScanner:
    """Scan projects for shared domain model usage."""

    def __init__(self, monorepo_root: Path):
        self.root = monorepo_root
        self.shared_domains_path = self.root / "shared" / "semantic" / "domains"
        self.projects_path = self.root / "projects"

        # Patterns for detecting domain imports and model definitions
        self.python_shared_import_pattern = re.compile(
            r'from\s+shared\.semantic\.domains\.(\w+).*import'
        )
        self.python_pydantic_pattern = re.compile(
            r'class\s+(\w+)\(BaseModel\)'
        )
        self.typescript_shared_import_pattern = re.compile(
            r'import.*from\s+["\'].*shared/semantic/domains/(\w+)'
        )
        self.typescript_type_pattern = re.compile(
            r'(?:interface|type)\s+(\w+)'
        )

    def get_available_domains(self) -> List[str]:
        """Get list of available shared domains."""
        if not self.shared_domains_path.exists():
            return []

        domains = []
        for item in self.shared_domains_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                domains.append(item.name)

        return sorted(domains)

    def scan_python_file(self, file_path: Path) -> Tuple[Set[str], List[str]]:
        """
        Scan a Python file for shared domain imports and local Pydantic models.

        Returns:
            Tuple of (shared_domains_used, local_model_names)
        """
        shared_domains = set()
        local_models = []

        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')

            # Find shared domain imports
            for match in self.python_shared_import_pattern.finditer(content):
                domain_name = match.group(1)
                shared_domains.add(domain_name)

            # Find local Pydantic models (only if BaseModel is imported)
            if 'from pydantic import' in content or 'from pydantic.v1 import' in content:
                for match in self.python_pydantic_pattern.finditer(content):
                    model_name = match.group(1)
                    local_models.append(model_name)

        except Exception as e:
            print(f"Warning: Error scanning {file_path}: {e}")

        return shared_domains, local_models

    def scan_typescript_file(self, file_path: Path) -> Tuple[Set[str], List[str]]:
        """
        Scan a TypeScript file for shared domain imports and local type definitions.

        Returns:
            Tuple of (shared_domains_used, local_type_names)
        """
        shared_domains = set()
        local_types = []

        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')

            # Find shared domain imports
            for match in self.typescript_shared_import_pattern.finditer(content):
                domain_name = match.group(1)
                shared_domains.add(domain_name)

            # Find local type/interface definitions
            for match in self.typescript_type_pattern.finditer(content):
                type_name = match.group(1)
                local_types.append(type_name)

        except Exception as e:
            print(f"Warning: Error scanning {file_path}: {e}")

        return shared_domains, local_types

    def scan_project(self, project_path: Path) -> DomainUsage:
        """Scan a single project for domain model usage."""
        shared_domains_used = set()
        local_pydantic_models = []
        local_typescript_models = []

        # Scan Python files
        for py_file in project_path.rglob("*.py"):
            # Skip venv, node_modules, .venv, etc.
            if any(part in py_file.parts for part in ['venv', 'node_modules', '.venv', '__pycache__', '.git']):
                continue

            domains, models = self.scan_python_file(py_file)
            shared_domains_used.update(domains)

            for model in models:
                rel_path = py_file.relative_to(project_path)
                local_pydantic_models.append((str(rel_path), model))

        # Scan TypeScript files
        for ts_file in project_path.rglob("*.ts"):
            if any(part in ts_file.parts for part in ['node_modules', '.git', 'dist', 'build']):
                continue

            domains, types = self.scan_typescript_file(ts_file)
            shared_domains_used.update(domains)

            for type_name in types:
                rel_path = ts_file.relative_to(project_path)
                local_typescript_models.append((str(rel_path), type_name))

        # Also check .tsx files
        for tsx_file in project_path.rglob("*.tsx"):
            if any(part in tsx_file.parts for part in ['node_modules', '.git', 'dist', 'build']):
                continue

            domains, types = self.scan_typescript_file(tsx_file)
            shared_domains_used.update(domains)

            for type_name in types:
                rel_path = tsx_file.relative_to(project_path)
                local_typescript_models.append((str(rel_path), type_name))

        # Calculate compliance score
        shared_count = len(shared_domains_used)
        local_count = len(local_pydantic_models) + len(local_typescript_models)

        if shared_count + local_count == 0:
            compliance_score = 0.0
        else:
            compliance_score = shared_count / (shared_count + local_count)

        return DomainUsage(
            project_path=str(project_path.relative_to(self.root)),
            project_name=project_path.name,
            shared_domains_used=sorted(list(shared_domains_used)),
            local_pydantic_models=local_pydantic_models,
            local_typescript_models=local_typescript_models,
            shared_import_count=shared_count,
            local_model_count=local_count,
            compliance_score=compliance_score
        )

    def scan_all_projects(self, category: str = None) -> ScanReport:
        """
        Scan all projects for domain model usage.

        Args:
            category: Optional category filter (personal, work, shared, oss, unspecified)
        """
        domain_usage_list = []

        # Get project directories
        if category:
            project_dirs = [self.projects_path / category]
        else:
            project_dirs = [
                d for d in self.projects_path.iterdir()
                if d.is_dir() and not d.name.startswith('.')
            ]

        # Scan each project directory
        for category_dir in project_dirs:
            if not category_dir.exists():
                continue

            for project_dir in category_dir.iterdir():
                if not project_dir.is_dir() or project_dir.name.startswith('.'):
                    continue

                # Check if it's an actual project (has .project file or src code)
                has_project_file = (project_dir / ".project").exists()
                has_python_files = any(project_dir.rglob("*.py"))
                has_typescript_files = any(project_dir.rglob("*.ts"))

                if not (has_project_file or has_python_files or has_typescript_files):
                    continue

                print(f"Scanning: {project_dir.relative_to(self.root)}")
                usage = self.scan_project(project_dir)

                # Only include projects with some model usage
                if usage.shared_import_count > 0 or usage.local_model_count > 0:
                    domain_usage_list.append(usage)

        # Calculate summary stats
        projects_using_shared = sum(1 for u in domain_usage_list if u.shared_import_count > 0)
        projects_with_local_only = sum(1 for u in domain_usage_list if u.local_model_count > 0 and u.shared_import_count == 0)
        total_shared_imports = sum(u.shared_import_count for u in domain_usage_list)
        total_local_models = sum(u.local_model_count for u in domain_usage_list)

        return ScanReport(
            total_projects=len(domain_usage_list),
            projects_using_shared=projects_using_shared,
            projects_with_local_only=projects_with_local_only,
            total_shared_imports=total_shared_imports,
            total_local_models=total_local_models,
            domain_usage=domain_usage_list,
            shared_domains_available=self.get_available_domains()
        )

    def generate_report(self, report: ScanReport, format: str = "text") -> str:
        """Generate a human-readable report."""
        if format == "json":
            return json.dumps(asdict(report), indent=2)

        # Text format
        lines = []
        lines.append("=" * 80)
        lines.append("SHARED DOMAIN MODEL USAGE REPORT")
        lines.append("=" * 80)
        lines.append("")

        lines.append(f"Available Shared Domains: {len(report.shared_domains_available)}")
        lines.append(f"  {', '.join(report.shared_domains_available)}")
        lines.append("")

        lines.append(f"Projects Scanned: {report.total_projects}")
        lines.append(f"  Using Shared Domains: {report.projects_using_shared}")
        lines.append(f"  Local Models Only: {report.projects_with_local_only}")
        lines.append("")

        lines.append(f"Total Shared Domain Imports: {report.total_shared_imports}")
        lines.append(f"Total Local Models Defined: {report.total_local_models}")
        lines.append("")

        # Sort by compliance score (ascending - worst first)
        sorted_usage = sorted(report.domain_usage, key=lambda u: u.compliance_score)

        lines.append("=" * 80)
        lines.append("PROJECTS BY COMPLIANCE SCORE")
        lines.append("=" * 80)
        lines.append("")

        for usage in sorted_usage:
            lines.append(f"Project: {usage.project_path}")
            lines.append(f"  Compliance Score: {usage.compliance_score:.1%}")
            lines.append(f"  Shared Domains Used: {usage.shared_import_count} {usage.shared_domains_used}")
            lines.append(f"  Local Python Models: {len(usage.local_pydantic_models)}")
            if usage.local_pydantic_models:
                for file_path, model_name in usage.local_pydantic_models[:5]:
                    lines.append(f"    - {model_name} in {file_path}")
                if len(usage.local_pydantic_models) > 5:
                    lines.append(f"    ... and {len(usage.local_pydantic_models) - 5} more")

            lines.append(f"  Local TypeScript Models: {len(usage.local_typescript_models)}")
            if usage.local_typescript_models:
                for file_path, type_name in usage.local_typescript_models[:5]:
                    lines.append(f"    - {type_name} in {file_path}")
                if len(usage.local_typescript_models) > 5:
                    lines.append(f"    ... and {len(usage.local_typescript_models) - 5} more")

            lines.append("")

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Verify shared domain model usage across projects"
    )
    parser.add_argument(
        "--category",
        choices=["personal", "work", "shared", "oss", "unspecified"],
        help="Filter by project category"
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output file path (default: stdout)"
    )

    args = parser.parse_args()

    # Find monorepo root
    current = Path.cwd()
    root = None
    while current != current.parent:
        if (current / "shared" / "semantic" / "domains").exists():
            root = current
            break
        current = current.parent

    if not root:
        print("Error: Could not find monorepo root (looking for shared/semantic/domains)")
        return 1

    print(f"Scanning from root: {root}")
    print()

    scanner = DomainUsageScanner(root)
    report = scanner.scan_all_projects(category=args.category)

    output = scanner.generate_report(report, format=args.format)

    if args.output:
        args.output.write_text(output)
        print(f"Report written to: {args.output}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    exit(main())
