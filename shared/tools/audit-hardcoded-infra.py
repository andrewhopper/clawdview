#!/usr/bin/env python3
# File UUID: a1b2c3d4-5e6f-7a8b-9c0d-1e2f3a4b5c6d

"""
Infrastructure Hardcoding Audit

Scans codebase for hardcoded AWS resource IDs and generates a comprehensive
report with recommendations for migration to SSM-backed discovery pattern.

Usage:
    # Audit entire codebase
    python audit-hardcoded-infra.py

    # Audit specific directory
    python audit-hardcoded-infra.py --path projects/myproject

    # Output as JSON
    python audit-hardcoded-infra.py --format json --output audit.json

    # Show only high-priority findings
    python audit-hardcoded-infra.py --severity high

    # Generate migration plan
    python audit-hardcoded-infra.py --migration-plan
"""

import re
import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Optional, Set
from dataclasses import dataclass, field, asdict
from collections import defaultdict
from enum import Enum


class Severity(Enum):
    HIGH = "high"      # Hardcoded in application code
    MEDIUM = "medium"  # Hardcoded in infrastructure code
    LOW = "low"        # In documentation or comments


class ResourceType(Enum):
    AMPLIFY_APP = "amplify-app"
    COGNITO_POOL = "cognito-pool"
    COGNITO_CLIENT = "cognito-client"
    S3_BUCKET = "s3-bucket"
    DYNAMODB_TABLE = "dynamodb-table"
    API_GATEWAY = "api-gateway"
    LAMBDA_ARN = "lambda-arn"
    ACCOUNT_ID = "account-id"
    REGION = "region"
    GENERIC_ID = "generic-id"


@dataclass
class Finding:
    """Represents a hardcoded value found in the codebase."""
    file_path: str
    line_number: int
    resource_type: ResourceType
    value: str
    context: str  # Surrounding lines
    severity: Severity
    recommendation: str
    can_auto_migrate: bool = False
    migration_ssm_path: Optional[str] = None


@dataclass
class AuditReport:
    """Complete audit report."""
    total_files_scanned: int = 0
    total_findings: int = 0
    findings_by_type: Dict[str, int] = field(default_factory=dict)
    findings_by_severity: Dict[str, int] = field(default_factory=dict)
    findings: List[Finding] = field(default_factory=list)
    migration_candidates: List[Finding] = field(default_factory=list)


# Regex patterns for AWS resource IDs
PATTERNS = {
    ResourceType.AMPLIFY_APP: [
        (r'\bd[0-9a-z]{13}\b', 'Amplify App ID'),
    ],
    ResourceType.COGNITO_POOL: [
        (r'\b[a-z]+-[a-z]+-[0-9]+_[A-Za-z0-9]{9}\b', 'Cognito User Pool ID'),
    ],
    ResourceType.COGNITO_CLIENT: [
        (r'\b[0-9a-v]{26}\b', 'Cognito Client ID (26 chars)'),
    ],
    ResourceType.S3_BUCKET: [
        # More specific: must contain project name patterns or specific suffixes
        (r'\b[a-z0-9]+(?:-[a-z0-9]+){2,}(?:-assets|-backups|-uploads|-data|-logs?)\b', 'S3 Bucket Name (with suffix)'),
        (r'\b[a-z0-9]+-[a-z0-9]+-[a-z0-9]{6,}\b', 'S3 Bucket Name (with hash)'),
    ],
    ResourceType.DYNAMODB_TABLE: [
        # More specific: project-name-purpose pattern or with env suffix
        (r'\b[a-z][a-z0-9]+(?:-[a-z0-9]+){2,}(?:-users|-sessions|-events|-items|-data)(?:-dev|-staging|-prod)?\b', 'DynamoDB Table Name'),
    ],
    ResourceType.ACCOUNT_ID: [
        (r'\b[0-9]{12}\b', 'AWS Account ID'),
    ],
    ResourceType.API_GATEWAY: [
        (r'\b[a-z0-9]{10}\b', 'API Gateway ID'),
    ],
    ResourceType.LAMBDA_ARN: [
        (r'\barn:aws:lambda:[a-z0-9\-]+:[0-9]{12}:function:[a-zA-Z0-9\-_]+\b', 'Lambda ARN'),
    ],
}

# File patterns to skip
SKIP_PATTERNS = [
    '**/.git/**',
    '**/node_modules/**',
    '**/venv/**',
    '**/__pycache__/**',
    '**/dist/**',
    '**/build/**',
    '**/.next/**',
    '**/coverage/**',
    '**/*.log',
    '**/*.pyc',
    '**/*.min.js',
    '**/package-lock.json',
    '**/yarn.lock',
    '**/audit-hardcoded-infra.py',  # This script
    '**/*AUDIT*.md',  # Audit reports
    '**/*MIGRATION*.md',  # Migration guides
    '**/*USAGE*.md',  # Usage guides (contain examples)
    '**/*GUIDE*.md',  # Other guides
    '**/README.md',  # READMEs contain examples
]

# Allowlist - known values that are OK to hardcode
ALLOWLIST = {
    '108782054816',  # Your AWS account ID (from CLAUDE.md)
    'us-east-1',     # Default region
}


def should_skip_file(file_path: Path) -> bool:
    """Check if file should be skipped."""
    for pattern in SKIP_PATTERNS:
        if file_path.match(pattern):
            return True
    return False


def get_severity(file_path: Path, line_content: str) -> Severity:
    """Determine severity based on file type and context."""
    # Comments or documentation
    if any(marker in line_content for marker in ['#', '//', '/*', '*', '<!--']):
        return Severity.LOW

    # Infrastructure code (CDK, CloudFormation, Terraform)
    if any(ext in file_path.suffixes for ext in ['.ts', '.js', '.py']) and 'infra' in str(file_path):
        return Severity.MEDIUM

    # Application code
    return Severity.HIGH


def extract_context(lines: List[str], line_num: int, context_size: int = 2) -> str:
    """Extract surrounding lines for context."""
    start = max(0, line_num - context_size)
    end = min(len(lines), line_num + context_size + 1)
    context_lines = []

    for i in range(start, end):
        marker = '→' if i == line_num else ' '
        context_lines.append(f"{i+1:4d}{marker} {lines[i].rstrip()}")

    return '\n'.join(context_lines)


def infer_project_name(file_path: Path) -> Optional[str]:
    """Infer project name from file path."""
    parts = file_path.parts

    # Look for projects/category/project-name pattern
    if 'projects' in parts:
        try:
            projects_idx = parts.index('projects')
            if len(parts) > projects_idx + 2:
                return parts[projects_idx + 2]
        except (ValueError, IndexError):
            pass

    return None


def generate_recommendation(
    finding: Finding,
    file_path: Path
) -> tuple[str, bool, Optional[str]]:
    """Generate migration recommendation."""
    project_name = infer_project_name(file_path)

    if finding.resource_type == ResourceType.AMPLIFY_APP:
        if project_name:
            ssm_path = f"/protoflow/projects/{project_name}/amplify-app-id"
            recommendation = f"""
Replace with SharedAmplifyApp:

  const app = new SharedAmplifyApp(this, 'App', {{
    projectName: '{project_name}',
    mode: 'import',
  }});

Then sync to SSM:
  python shared/tools/sync-infra-to-ssm.py \\
    --project-name {project_name} \\
    --amplify-app-id {finding.value}
"""
            return recommendation.strip(), True, ssm_path
        else:
            return "Replace with SharedAmplifyApp construct", False, None

    elif finding.resource_type == ResourceType.COGNITO_POOL:
        recommendation = """
Replace with SharedCognito:

  const auth = new SharedCognito(this, 'Auth', {{ mode: 'import' }});
  const client = auth.createClient('WebClient', {{ ... }});

Cognito pool should already be in SSM at:
  /protoflow/shared/cognito/user-pool-id
"""
        return recommendation.strip(), True, "/protoflow/shared/cognito/user-pool-id"

    elif finding.resource_type == ResourceType.S3_BUCKET:
        if project_name and 'bucket' in finding.context.lower():
            # Try to infer suffix from variable name
            suffix = "default"
            for word in ['asset', 'backup', 'upload', 'data', 'log']:
                if word in finding.context.lower():
                    suffix = word
                    break

            ssm_path = f"/protoflow/projects/{project_name}/s3-bucket-{suffix}"
            recommendation = f"""
Replace with SharedS3Bucket:

  const bucket = new SharedS3Bucket(this, 'Bucket', {{
    projectName: '{project_name}',
    bucketSuffix: '{suffix}',
    mode: 'import',
  }});

Then sync to SSM:
  python shared/tools/sync-infra-to-ssm.py \\
    --project-name {project_name} \\
    --s3-bucket {finding.value} \\
    --s3-suffix {suffix}
"""
            return recommendation.strip(), True, ssm_path
        else:
            return "Replace with SharedS3Bucket construct", False, None

    elif finding.resource_type == ResourceType.DYNAMODB_TABLE:
        if project_name:
            # Try to infer suffix from variable name
            suffix = "default"
            for word in ['user', 'session', 'event', 'data', 'item']:
                if word in finding.context.lower():
                    suffix = word
                    break

            ssm_path = f"/protoflow/projects/{project_name}/dynamodb-table-{suffix}"
            recommendation = f"""
Replace with SharedDynamoTable:

  const table = new SharedDynamoTable(this, 'Table', {{
    projectName: '{project_name}',
    tableSuffix: '{suffix}',
    mode: 'import',
  }});

Then sync to SSM:
  python shared/tools/sync-infra-to-ssm.py \\
    --project-name {project_name} \\
    --dynamodb-table {finding.value} \\
    --dynamodb-suffix {suffix}
"""
            return recommendation.strip(), True, ssm_path
        else:
            return "Replace with SharedDynamoTable construct", False, None

    elif finding.resource_type == ResourceType.ACCOUNT_ID:
        return "Use ConfigProvider.getAccountId(this) or SSM parameter", True, None

    return "Review and consider moving to SSM Parameter Store", False, None


def scan_file(file_path: Path) -> List[Finding]:
    """Scan a single file for hardcoded values."""
    findings = []

    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        lines = content.split('\n')
    except Exception as e:
        print(f"Error reading {file_path}: {e}", file=sys.stderr)
        return findings

    for resource_type, patterns in PATTERNS.items():
        for pattern, description in patterns:
            for line_num, line in enumerate(lines):
                matches = re.finditer(pattern, line)
                for match in matches:
                    value = match.group(0)

                    # Skip allowlisted values
                    if value in ALLOWLIST:
                        continue

                    # Skip if it's in a comment about patterns
                    if 'pattern' in line.lower() or 'regex' in line.lower():
                        continue

                    # Skip if it's in this audit script
                    if 'PATTERNS' in line or 'ALLOWLIST' in line:
                        continue

                    severity = get_severity(file_path, line)
                    context = extract_context(lines, line_num)

                    finding = Finding(
                        file_path=str(file_path),
                        line_number=line_num + 1,
                        resource_type=resource_type,
                        value=value,
                        context=context,
                        severity=severity,
                        recommendation="",
                    )

                    # Generate recommendation
                    rec, can_migrate, ssm_path = generate_recommendation(finding, file_path)
                    finding.recommendation = rec
                    finding.can_auto_migrate = can_migrate
                    finding.migration_ssm_path = ssm_path

                    findings.append(finding)

    return findings


def scan_directory(root_path: Path, recursive: bool = True) -> AuditReport:
    """Scan directory for hardcoded values."""
    report = AuditReport()

    # Collect all files to scan
    if recursive:
        files = [f for f in root_path.rglob('*') if f.is_file() and not should_skip_file(f)]
    else:
        files = [f for f in root_path.glob('*') if f.is_file() and not should_skip_file(f)]

    report.total_files_scanned = len(files)

    for file_path in files:
        findings = scan_file(file_path)
        report.findings.extend(findings)

    # Generate statistics
    report.total_findings = len(report.findings)

    for finding in report.findings:
        # By type
        type_key = finding.resource_type.value
        report.findings_by_type[type_key] = report.findings_by_type.get(type_key, 0) + 1

        # By severity
        severity_key = finding.severity.value
        report.findings_by_severity[severity_key] = report.findings_by_severity.get(severity_key, 0) + 1

        # Migration candidates
        if finding.can_auto_migrate and finding.severity != Severity.LOW:
            report.migration_candidates.append(finding)

    return report


def print_report(report: AuditReport, severity_filter: Optional[str] = None):
    """Print audit report to console."""
    print("\n" + "="*80)
    print("INFRASTRUCTURE HARDCODING AUDIT REPORT")
    print("="*80 + "\n")

    print(f"Files Scanned: {report.total_files_scanned}")
    print(f"Total Findings: {report.total_findings}")
    print(f"Migration Candidates: {len(report.migration_candidates)}\n")

    print("Findings by Type:")
    for resource_type, count in sorted(report.findings_by_type.items(), key=lambda x: x[1], reverse=True):
        print(f"  {resource_type:20s} {count:4d}")

    print("\nFindings by Severity:")
    for severity, count in sorted(report.findings_by_severity.items()):
        print(f"  {severity:10s} {count:4d}")

    # Filter findings by severity if specified
    findings_to_show = report.findings
    if severity_filter:
        findings_to_show = [f for f in findings_to_show if f.severity.value == severity_filter]

    if not findings_to_show:
        print("\nNo findings to display.")
        return

    print("\n" + "="*80)
    print("DETAILED FINDINGS")
    print("="*80 + "\n")

    # Group by file
    by_file = defaultdict(list)
    for finding in findings_to_show:
        by_file[finding.file_path].append(finding)

    for file_path, findings in sorted(by_file.items()):
        print(f"\n📄 {file_path}")
        print("-" * 80)

        for finding in findings:
            print(f"\n  Line {finding.line_number} | {finding.resource_type.value} | {finding.severity.value.upper()}")
            print(f"  Value: {finding.value}")

            if finding.can_auto_migrate:
                print(f"  ✅ Auto-migratable")
                if finding.migration_ssm_path:
                    print(f"  SSM Path: {finding.migration_ssm_path}")
            else:
                print(f"  ⚠️  Manual migration required")

            print(f"\n  Context:")
            for line in finding.context.split('\n'):
                print(f"    {line}")

            print(f"\n  Recommendation:")
            for line in finding.recommendation.split('\n'):
                print(f"    {line}")

            print()


def generate_migration_plan(report: AuditReport):
    """Generate a migration plan."""
    print("\n" + "="*80)
    print("MIGRATION PLAN")
    print("="*80 + "\n")

    if not report.migration_candidates:
        print("No auto-migratable findings.")
        return

    # Group by project
    by_project = defaultdict(list)
    for finding in report.migration_candidates:
        file_path = Path(finding.file_path)
        project = infer_project_name(file_path) or "unknown"
        by_project[project].append(finding)

    print(f"Found {len(report.migration_candidates)} migration candidates across {len(by_project)} projects.\n")

    for project, findings in sorted(by_project.items()):
        print(f"\n## Project: {project}")
        print(f"   Findings: {len(findings)}\n")

        # Collect unique resource IDs by type
        resources = defaultdict(set)
        for finding in findings:
            resources[finding.resource_type].add(finding.value)

        # Generate sync commands
        print(f"   1. Sync resources to SSM:\n")

        amplify_ids = resources.get(ResourceType.AMPLIFY_APP, set())
        s3_buckets = resources.get(ResourceType.S3_BUCKET, set())
        dynamodb_tables = resources.get(ResourceType.DYNAMODB_TABLE, set())

        if amplify_ids or s3_buckets or dynamodb_tables:
            cmd_parts = [
                "      python shared/tools/sync-infra-to-ssm.py",
                f"        --project-name {project}",
            ]

            for amp_id in amplify_ids:
                cmd_parts.append(f"        --amplify-app-id {amp_id}")

            for bucket in s3_buckets:
                cmd_parts.append(f"        --s3-bucket {bucket}")

            for table in dynamodb_tables:
                cmd_parts.append(f"        --dynamodb-table {table}")

            print(" \\\n".join(cmd_parts))
            print()

        # Show files to update
        print(f"   2. Update these files to use Shared constructs:\n")
        file_set = set(f.file_path for f in findings)
        for file_path in sorted(file_set):
            print(f"      - {file_path}")

        print()


def main():
    parser = argparse.ArgumentParser(
        description='Audit codebase for hardcoded infrastructure values'
    )

    parser.add_argument('--path', default='/home/user/protoflow',
                        help='Root path to scan (default: /home/user/protoflow)')
    parser.add_argument('--format', choices=['text', 'json'], default='text',
                        help='Output format')
    parser.add_argument('--output', help='Output file (default: stdout)')
    parser.add_argument('--severity', choices=['high', 'medium', 'low'],
                        help='Filter by severity level')
    parser.add_argument('--migration-plan', action='store_true',
                        help='Generate migration plan')
    parser.add_argument('--resource-type',
                        choices=[rt.value for rt in ResourceType],
                        help='Filter by resource type')

    args = parser.parse_args()

    root_path = Path(args.path)
    if not root_path.exists():
        print(f"Error: Path does not exist: {root_path}", file=sys.stderr)
        return 1

    print(f"Scanning: {root_path}")
    print("This may take a minute...\n")

    report = scan_directory(root_path)

    # Filter by resource type if specified
    if args.resource_type:
        report.findings = [f for f in report.findings
                          if f.resource_type.value == args.resource_type]
        report.total_findings = len(report.findings)

    if args.format == 'json':
        output = {
            'summary': {
                'total_files_scanned': report.total_files_scanned,
                'total_findings': report.total_findings,
                'migration_candidates': len(report.migration_candidates),
                'findings_by_type': report.findings_by_type,
                'findings_by_severity': report.findings_by_severity,
            },
            'findings': [asdict(f) for f in report.findings],
        }

        if args.output:
            Path(args.output).write_text(json.dumps(output, indent=2, default=str))
            print(f"Report written to: {args.output}")
        else:
            print(json.dumps(output, indent=2, default=str))
    else:
        print_report(report, severity_filter=args.severity)

        if args.migration_plan:
            generate_migration_plan(report)

    return 0


if __name__ == '__main__':
    sys.exit(main())
