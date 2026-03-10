#!/usr/bin/env python3
"""
Infrastructure Audit & Drift Detection
Analyzes deployed AWS infrastructure and compares with monorepo projects.
"""

import boto3
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import re
from collections import defaultdict
import argparse


class InfraAuditor:
    """Audit infrastructure and detect drift from monorepo projects."""

    def __init__(
        self,
        profile: str = "admin-507745175693",
        region: str = "us-east-1",
        monorepo_root: Optional[Path] = None
    ):
        """Initialize AWS clients and paths."""
        self.session = boto3.Session(profile_name=profile, region_name=region)
        self.cfn = self.session.client('cloudformation')
        self.region = region
        self.account_id = self.session.client('sts').get_caller_identity()['Account']

        # Determine monorepo root
        if monorepo_root is None:
            # Try to find monorepo root by looking for CLAUDE.md
            current = Path.cwd()
            while current != current.parent:
                if (current / 'CLAUDE.md').exists():
                    monorepo_root = current
                    break
                current = current.parent
            else:
                monorepo_root = Path.cwd()

        self.monorepo_root = monorepo_root
        self.projects_dir = monorepo_root / 'projects'

    def list_all_stacks(self) -> List[Dict[str, Any]]:
        """List all CloudFormation stacks."""
        stacks = []
        paginator = self.cfn.get_paginator('list_stacks')

        for page in paginator.paginate(
            StackStatusFilter=[
                'CREATE_COMPLETE', 'UPDATE_COMPLETE', 'ROLLBACK_COMPLETE',
                'UPDATE_ROLLBACK_COMPLETE', 'IMPORT_COMPLETE'
            ]
        ):
            stacks.extend(page['StackSummaries'])

        return stacks

    def get_stack_details(self, stack_name: str) -> Dict[str, Any]:
        """Get detailed stack information."""
        try:
            response = self.cfn.describe_stacks(StackName=stack_name)
            stack = response['Stacks'][0]

            # Get tags
            tags = {}
            if 'Tags' in stack:
                for tag in stack['Tags']:
                    tags[tag['Key']] = tag['Value']

            # Get outputs
            outputs = {}
            if 'Outputs' in stack:
                for output in stack['Outputs']:
                    outputs[output['OutputKey']] = output['OutputValue']

            # Count resources
            try:
                resources = self.cfn.list_stack_resources(StackName=stack_name)
                resource_count = len(resources.get('StackResourceSummaries', []))
            except:
                resource_count = 0

            return {
                'name': stack['StackName'],
                'id': stack['StackId'],
                'status': stack['StackStatus'],
                'created': stack['CreationTime'].isoformat(),
                'updated': stack.get('LastUpdatedTime', stack['CreationTime']).isoformat(),
                'tags': tags,
                'outputs': outputs,
                'resource_count': resource_count,
                'description': stack.get('Description', '')
            }
        except Exception as e:
            return {
                'name': stack_name,
                'error': str(e),
                'status': 'ERROR'
            }

    def find_projects(self) -> List[Dict[str, Any]]:
        """Find all projects in monorepo."""
        projects = []

        if not self.projects_dir.exists():
            return projects

        # Search for .project files
        for project_file in self.projects_dir.rglob('.project'):
            project_dir = project_file.parent

            # Parse .project file
            try:
                with open(project_file, 'r') as f:
                    content = f.read()
                    # Try to parse as YAML-like
                    project_data = {}
                    for line in content.split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            project_data[key.strip()] = value.strip()
            except:
                project_data = {}

            # Check for infra directory
            infra_dir = project_dir / 'infra'
            has_infra = infra_dir.exists()

            # Check for deployed state
            current_link = infra_dir / 'deploys' / 'current' if has_infra else None
            has_deployed = current_link and current_link.exists()

            # Get relative path
            try:
                rel_path = project_dir.relative_to(self.monorepo_root)
            except:
                rel_path = project_dir

            projects.append({
                'name': project_dir.name,
                'path': str(rel_path),
                'full_path': project_dir,
                'has_infra': has_infra,
                'has_deployed': has_deployed,
                'project_data': project_data
            })

        # Also look for standalone infra/ directories without .project
        for infra_dir in self.projects_dir.rglob('infra'):
            project_dir = infra_dir.parent

            # Skip if already found via .project
            if any(p['full_path'] == project_dir for p in projects):
                continue

            # Check for CDK
            has_cdk = (infra_dir / 'cdk.json').exists()
            if not has_cdk:
                continue

            try:
                rel_path = project_dir.relative_to(self.monorepo_root)
            except:
                rel_path = project_dir

            projects.append({
                'name': project_dir.name,
                'path': str(rel_path),
                'full_path': project_dir,
                'has_infra': True,
                'has_deployed': False,
                'project_data': {}
            })

        return projects

    def normalize_name(self, name: str) -> str:
        """Normalize name for matching."""
        # Remove common suffixes
        name = re.sub(r'-(dev|prod|staging|test|personal)$', '', name, flags=re.IGNORECASE)
        # Remove stack suffix
        name = re.sub(r'Stack$', '', name, flags=re.IGNORECASE)
        # Remove CDK suffix
        name = re.sub(r'CDK$', '', name, flags=re.IGNORECASE)
        # Convert to lowercase
        name = name.lower()
        # Remove special characters
        name = re.sub(r'[^a-z0-9]', '', name)
        return name

    def match_stack_to_project(
        self,
        stack: Dict[str, Any],
        projects: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """Try to match a stack to a project."""
        stack_name = stack['name']
        stack_normalized = self.normalize_name(stack_name)

        # Try exact match first
        for project in projects:
            project_normalized = self.normalize_name(project['name'])
            if stack_normalized == project_normalized:
                return project

        # Try partial match (stack name contains project name or vice versa)
        for project in projects:
            project_normalized = self.normalize_name(project['name'])
            if project_normalized in stack_normalized or stack_normalized in project_normalized:
                return project

        # Try matching by tags
        if 'Project' in stack.get('tags', {}):
            project_tag = stack['tags']['Project']
            project_tag_normalized = self.normalize_name(project_tag)

            for project in projects:
                project_normalized = self.normalize_name(project['name'])
                if project_tag_normalized == project_normalized:
                    return project

        return None

    def analyze_drift(self) -> Dict[str, Any]:
        """Analyze drift between deployed stacks and projects."""
        print("🔍 Scanning infrastructure...")

        # Get all stacks
        stacks = self.list_all_stacks()
        print(f"   Found {len(stacks)} CloudFormation stacks")

        # Get stack details
        stack_details = []
        for stack in stacks:
            print(f"   Analyzing {stack['StackName']}...")
            details = self.get_stack_details(stack['StackName'])
            stack_details.append(details)

        # Get all projects
        print(f"\n🗂️  Scanning projects in {self.projects_dir}...")
        projects = self.find_projects()
        print(f"   Found {len(projects)} projects")

        # Match stacks to projects
        print(f"\n🔗 Matching stacks to projects...")
        matched = []
        orphaned_stacks = []

        for stack in stack_details:
            if stack.get('status') == 'ERROR':
                continue

            project = self.match_stack_to_project(stack, projects)
            if project:
                matched.append({
                    'stack': stack,
                    'project': project,
                    'aligned': project['has_deployed']
                })
                print(f"   ✓ {stack['name']} → {project['name']}")
            else:
                orphaned_stacks.append(stack)
                print(f"   ✗ {stack['name']} → No matching project")

        # Find projects without stacks
        matched_projects = {m['project']['name'] for m in matched}
        undeployed_projects = [
            p for p in projects
            if p['has_infra'] and p['name'] not in matched_projects
        ]

        return {
            'total_stacks': len(stack_details),
            'total_projects': len(projects),
            'matched': matched,
            'orphaned_stacks': orphaned_stacks,
            'undeployed_projects': undeployed_projects,
            'timestamp': datetime.now().isoformat()
        }

    def generate_report(self, analysis: Dict[str, Any]) -> str:
        """Generate human-readable report."""
        lines = []

        lines.append("=" * 80)
        lines.append("Infrastructure Audit Report")
        lines.append("=" * 80)
        lines.append(f"Generated: {analysis['timestamp']}")
        lines.append(f"Region: {self.region}")
        lines.append(f"Account: {self.account_id}")
        lines.append(f"Monorepo: {self.monorepo_root}")
        lines.append("")

        # Summary
        lines.append("📊 Summary")
        lines.append("-" * 80)
        lines.append(f"Total CloudFormation Stacks: {analysis['total_stacks']}")
        lines.append(f"Total Projects with Infra: {analysis['total_projects']}")
        lines.append(f"Matched (Stack → Project): {len(analysis['matched'])}")
        lines.append(f"Orphaned Stacks (No Project): {len(analysis['orphaned_stacks'])}")
        lines.append(f"Undeployed Projects (No Stack): {len(analysis['undeployed_projects'])}")
        lines.append("")

        # Matched stacks
        if analysis['matched']:
            lines.append("✅ Matched Stacks (Stack → Project)")
            lines.append("-" * 80)

            # Group by alignment status
            aligned = [m for m in analysis['matched'] if m['aligned']]
            unaligned = [m for m in analysis['matched'] if not m['aligned']]

            if aligned:
                lines.append(f"\n🟢 Aligned ({len(aligned)}) - Stack deployed and tracked in project:")
                lines.append("")
                for match in aligned:
                    stack = match['stack']
                    project = match['project']
                    lines.append(f"   {stack['name']}")
                    lines.append(f"   └─ Project: {project['path']}")
                    lines.append(f"      Status: {stack['status']}")
                    lines.append(f"      Updated: {stack['updated'][:10]}")
                    lines.append(f"      Resources: {stack['resource_count']}")
                    if stack['tags']:
                        lines.append(f"      Tags: {', '.join(f'{k}={v}' for k, v in stack['tags'].items())}")
                    lines.append("")

            if unaligned:
                lines.append(f"\n🟡 Matched but Not Tracked ({len(unaligned)}) - Need to import:")
                lines.append("")
                for match in unaligned:
                    stack = match['stack']
                    project = match['project']
                    lines.append(f"   {stack['name']}")
                    lines.append(f"   └─ Project: {project['path']}")
                    lines.append(f"      Status: {stack['status']}")
                    lines.append(f"      ⚠️  Run: cd {project['path']} && make infra-import STACK={stack['name']}")
                    lines.append("")

        # Orphaned stacks
        if analysis['orphaned_stacks']:
            lines.append(f"\n❌ Orphaned Stacks ({len(analysis['orphaned_stacks'])}) - No matching project:")
            lines.append("-" * 80)
            for stack in analysis['orphaned_stacks']:
                lines.append(f"\n   {stack['name']}")
                lines.append(f"      Status: {stack['status']}")
                lines.append(f"      Created: {stack['created'][:10]}")
                lines.append(f"      Updated: {stack['updated'][:10]}")
                lines.append(f"      Resources: {stack['resource_count']}")
                if stack['tags']:
                    lines.append(f"      Tags: {', '.join(f'{k}={v}' for k, v in stack['tags'].items())}")

                # Recommendations
                lines.append(f"      Recommendations:")
                lines.append(f"      • Create project: mkdir -p projects/personal/active/{stack['name'].lower()}")
                lines.append(f"      • Import stack: cd projects/... && make infra-import STACK={stack['name']}")
                lines.append(f"      • OR destroy if unused: aws cloudformation delete-stack --stack-name {stack['name']}")

        # Undeployed projects
        if analysis['undeployed_projects']:
            lines.append(f"\n⭕ Projects with Infra but No Deployed Stack ({len(analysis['undeployed_projects'])}):")
            lines.append("-" * 80)
            for project in analysis['undeployed_projects']:
                lines.append(f"\n   {project['name']}")
                lines.append(f"      Path: {project['path']}")
                lines.append(f"      Has infra/: {project['has_infra']}")
                lines.append(f"      Recommendations:")
                lines.append(f"      • Deploy: cd {project['path']} && make infra-bootstrap && make infra-deploy")
                lines.append(f"      • OR remove infra/ if not needed")

        # Recommendations
        lines.append("\n" + "=" * 80)
        lines.append("🎯 Recommended Actions")
        lines.append("=" * 80)

        drift_count = len(analysis['orphaned_stacks']) + len(analysis['undeployed_projects'])
        untracked_count = len([m for m in analysis['matched'] if not m['aligned']])

        if drift_count == 0 and untracked_count == 0:
            lines.append("\n✅ No drift detected! All infrastructure is aligned.")
        else:
            lines.append(f"\n📋 Total drift items: {drift_count}")
            lines.append(f"📋 Untracked deployments: {untracked_count}")
            lines.append("")

            if untracked_count > 0:
                lines.append("1. Import untracked stacks:")
                lines.append("   For each matched but untracked stack, run:")
                lines.append("   cd <project-path> && make infra-import STACK=<stack-name>")
                lines.append("")

            if analysis['orphaned_stacks']:
                lines.append("2. Handle orphaned stacks:")
                lines.append("   • Create projects for active stacks")
                lines.append("   • Destroy unused stacks")
                lines.append("")

            if analysis['undeployed_projects']:
                lines.append("3. Handle undeployed projects:")
                lines.append("   • Deploy projects that need infrastructure")
                lines.append("   • Remove infra/ from projects that don't")

        lines.append("\n" + "=" * 80)
        lines.append("End of Report")
        lines.append("=" * 80)

        return '\n'.join(lines)

    def generate_json_report(self, analysis: Dict[str, Any]) -> str:
        """Generate machine-readable JSON report."""
        return json.dumps(analysis, indent=2)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Audit AWS infrastructure and detect drift from monorepo projects'
    )
    parser.add_argument(
        '--profile',
        default='admin-507745175693',
        help='AWS profile to use'
    )
    parser.add_argument(
        '--region',
        default='us-east-1',
        help='AWS region'
    )
    parser.add_argument(
        '--monorepo-root',
        type=Path,
        help='Path to monorepo root (auto-detected if not specified)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output JSON instead of human-readable report'
    )
    parser.add_argument(
        '--output',
        type=Path,
        help='Write report to file instead of stdout'
    )

    args = parser.parse_args()

    # Run audit
    auditor = InfraAuditor(
        profile=args.profile,
        region=args.region,
        monorepo_root=args.monorepo_root
    )

    print("🚀 Starting infrastructure audit...\n")
    analysis = auditor.analyze_drift()

    print("\n📝 Generating report...\n")

    # Generate report
    if args.json:
        report = auditor.generate_json_report(analysis)
    else:
        report = auditor.generate_report(analysis)

    # Output report
    if args.output:
        args.output.write_text(report)
        print(f"✅ Report written to: {args.output}")
    else:
        print(report)


if __name__ == '__main__':
    main()
