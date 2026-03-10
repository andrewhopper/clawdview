#!/usr/bin/env python3
# File UUID: 8d9e0f1a-2b3c-4d5e-6f7a-8b9c0d1e2f3a

"""
Sync Infrastructure State to SSM

Universal tool to sync infrastructure resource IDs to SSM for CDK discovery.
Supports: Amplify apps, S3 buckets, DynamoDB tables, and more.

This allows CDK to always use mode='import' without manual toggling.

Usage:
    # Sync by project name (auto-discovers all resources)
    python sync-infra-to-ssm.py --project-name myproject

    # Sync specific resource type
    python sync-infra-to-ssm.py --project-name myproject --resource-type amplify

    # Sync from CloudFormation stack
    python sync-infra-to-ssm.py --stack-name MyProjectStack

    # Manual specification
    python sync-infra-to-ssm.py \
        --project-name myproject \
        --amplify-app-id d1a2b3c4d5e6 \
        --s3-bucket myproject-assets-123456 \
        --dynamodb-table myproject-users

    # Auto-discover all projects
    python sync-infra-to-ssm.py --auto-discover

    # Dry run (preview only)
    python sync-infra-to-ssm.py --project-name myproject --dry-run
"""

import argparse
import boto3
import json
import sys
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, field

# Initialize AWS clients
cf_client = boto3.client('cloudformation')
amplify_client = boto3.client('amplify')
s3_client = boto3.client('s3')
dynamodb_client = boto3.client('dynamodb')
ssm_client = boto3.client('ssm')


@dataclass
class ResourceSync:
    """Represents a resource to sync to SSM."""
    resource_type: str  # 'amplify', 's3', 'dynamodb'
    resource_id: str
    ssm_path: str
    current_ssm_value: Optional[str] = None
    needs_sync: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


def get_ssm_path(project_name: str, resource_type: str, suffix: str = '') -> str:
    """Get SSM parameter path for resource."""
    if resource_type == 'amplify':
        return f"/protoflow/projects/{project_name}/amplify-app-id"
    elif resource_type == 's3':
        return f"/protoflow/projects/{project_name}/s3-bucket-{suffix}"
    elif resource_type == 'dynamodb':
        return f"/protoflow/projects/{project_name}/dynamodb-table-{suffix}"
    else:
        return f"/protoflow/projects/{project_name}/{resource_type}-{suffix}"


def get_from_ssm(ssm_path: str) -> Optional[str]:
    """Get current value from SSM."""
    try:
        response = ssm_client.get_parameter(Name=ssm_path)
        return response['Parameter']['Value']
    except ssm_client.exceptions.ParameterNotFound:
        return None
    except Exception as e:
        print(f"Error reading from SSM: {e}", file=sys.stderr)
        return None


def store_in_ssm(ssm_path: str, value: str, description: str, dry_run: bool = False) -> bool:
    """Store value in SSM."""
    if dry_run:
        print(f"[DRY RUN] Would store: {ssm_path} = {value}")
        return True

    try:
        ssm_client.put_parameter(
            Name=ssm_path,
            Value=value,
            Type='String',
            Description=description,
            Overwrite=True,
        )
        print(f"✅ Stored: {ssm_path} = {value}")
        return True
    except Exception as e:
        print(f"❌ Error storing in SSM: {e}", file=sys.stderr)
        return False


def discover_from_stack(stack_name: str, project_name: str) -> List[ResourceSync]:
    """Discover all resources from a CloudFormation stack."""
    resources = []

    try:
        # Get stack outputs
        response = cf_client.describe_stacks(StackName=stack_name)
        stacks = response.get('Stacks', [])
        if not stacks:
            return resources

        stack = stacks[0]
        outputs = stack.get('Outputs', [])

        # Get stack resources
        response = cf_client.list_stack_resources(StackName=stack_name)
        stack_resources = response.get('StackResourceSummaries', [])

        # Find Amplify apps
        for resource in stack_resources:
            if resource.get('ResourceType') == 'AWS::Amplify::App':
                app_id = resource.get('PhysicalResourceId')
                ssm_path = get_ssm_path(project_name, 'amplify')
                current_value = get_from_ssm(ssm_path)

                resources.append(ResourceSync(
                    resource_type='amplify',
                    resource_id=app_id,
                    ssm_path=ssm_path,
                    current_ssm_value=current_value,
                    needs_sync=current_value != app_id,
                    metadata={'logical_id': resource.get('LogicalResourceId')},
                ))

        # Find S3 buckets
        for resource in stack_resources:
            if resource.get('ResourceType') == 'AWS::S3::Bucket':
                bucket_name = resource.get('PhysicalResourceId')
                logical_id = resource.get('LogicalResourceId')

                # Infer suffix from logical ID
                suffix = logical_id.lower().replace('bucket', '').replace('stack', '') or 'default'

                ssm_path = get_ssm_path(project_name, 's3', suffix)
                current_value = get_from_ssm(ssm_path)

                resources.append(ResourceSync(
                    resource_type='s3',
                    resource_id=bucket_name,
                    ssm_path=ssm_path,
                    current_ssm_value=current_value,
                    needs_sync=current_value != bucket_name,
                    metadata={'logical_id': logical_id, 'suffix': suffix},
                ))

        # Find DynamoDB tables
        for resource in stack_resources:
            if resource.get('ResourceType') == 'AWS::DynamoDB::Table':
                table_name = resource.get('PhysicalResourceId')
                logical_id = resource.get('LogicalResourceId')

                # Infer suffix from logical ID
                suffix = logical_id.lower().replace('table', '').replace('stack', '') or 'default'

                ssm_path = get_ssm_path(project_name, 'dynamodb', suffix)
                current_value = get_from_ssm(ssm_path)

                resources.append(ResourceSync(
                    resource_type='dynamodb',
                    resource_id=table_name,
                    ssm_path=ssm_path,
                    current_ssm_value=current_value,
                    needs_sync=current_value != table_name,
                    metadata={'logical_id': logical_id, 'suffix': suffix},
                ))

    except Exception as e:
        print(f"Error discovering from stack: {e}", file=sys.stderr)

    return resources


def discover_amplify_by_name(app_name: str, project_name: str) -> Optional[ResourceSync]:
    """Discover Amplify app by name."""
    try:
        response = amplify_client.list_apps(maxResults=100)
        apps = response.get('apps', [])

        for app in apps:
            if app.get('name') == app_name:
                app_id = app.get('appId')
                ssm_path = get_ssm_path(project_name, 'amplify')
                current_value = get_from_ssm(ssm_path)

                return ResourceSync(
                    resource_type='amplify',
                    resource_id=app_id,
                    ssm_path=ssm_path,
                    current_ssm_value=current_value,
                    needs_sync=current_value != app_id,
                    metadata={'name': app.get('name'), 'defaultDomain': app.get('defaultDomain')},
                )
    except Exception as e:
        print(f"Error discovering Amplify app: {e}", file=sys.stderr)

    return None


def print_resources(resources: List[ResourceSync]):
    """Print discovered resources in a table."""
    if not resources:
        print("No resources found.")
        return

    print(f"\nFound {len(resources)} resource(s):\n")

    for i, res in enumerate(resources, 1):
        status = "✅ In sync" if not res.needs_sync else "⚠️  Needs sync"
        print(f"{i}. {res.resource_type.upper()}: {res.resource_id}")
        print(f"   SSM Path: {res.ssm_path}")
        print(f"   Current: {res.current_ssm_value or '(not set)'}")
        print(f"   Status: {status}")
        if res.metadata:
            for key, value in res.metadata.items():
                print(f"   {key}: {value}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description='Sync infrastructure state to SSM for CDK discovery'
    )

    # Input methods
    parser.add_argument('--project-name', help='Project name (e.g., myproject)')
    parser.add_argument('--stack-name', help='CloudFormation stack name')
    parser.add_argument('--auto-discover', action='store_true',
                        help='Auto-discover all Amplify apps')

    # Resource-specific inputs
    parser.add_argument('--amplify-app-id', help='Amplify app ID')
    parser.add_argument('--amplify-app-name', help='Amplify app name')
    parser.add_argument('--s3-bucket', help='S3 bucket name')
    parser.add_argument('--s3-suffix', default='default', help='S3 bucket suffix (default: default)')
    parser.add_argument('--dynamodb-table', help='DynamoDB table name')
    parser.add_argument('--dynamodb-suffix', default='default', help='DynamoDB table suffix (default: default)')

    # Options
    parser.add_argument('--resource-type', choices=['amplify', 's3', 'dynamodb', 'all'],
                        default='all', help='Resource type to sync')
    parser.add_argument('--dry-run', action='store_true', help='Preview without making changes')
    parser.add_argument('--force', action='store_true', help='Overwrite existing SSM values')

    args = parser.parse_args()

    resources_to_sync: List[ResourceSync] = []

    # Auto-discover mode
    if args.auto_discover:
        print("🔍 Auto-discovering Amplify apps...")
        try:
            response = amplify_client.list_apps(maxResults=100)
            apps = response.get('apps', [])

            for app in apps:
                app_id = app.get('appId')
                app_name = app.get('name')

                # Infer project name
                project_name = app_name
                for suffix in ['-frontend', '-web', '-app', '-ui']:
                    if project_name.endswith(suffix):
                        project_name = project_name[:-len(suffix)]
                        break

                ssm_path = get_ssm_path(project_name, 'amplify')
                current_value = get_from_ssm(ssm_path)

                resources_to_sync.append(ResourceSync(
                    resource_type='amplify',
                    resource_id=app_id,
                    ssm_path=ssm_path,
                    current_ssm_value=current_value,
                    needs_sync=current_value != app_id,
                    metadata={'name': app_name, 'project': project_name},
                ))
        except Exception as e:
            print(f"Error auto-discovering: {e}", file=sys.stderr)
            return 1

        print_resources(resources_to_sync)

        needs_sync = [r for r in resources_to_sync if r.needs_sync]
        if needs_sync and not args.dry_run:
            response = input(f"\nSync {len(needs_sync)} resource(s) to SSM? [y/N]: ")
            if response.lower() == 'y':
                for res in needs_sync:
                    store_in_ssm(
                        res.ssm_path,
                        res.resource_id,
                        f"{res.resource_type} resource for {res.metadata.get('project', 'unknown')}",
                        dry_run=False
                    )

        return 0

    # Require project name for other modes
    if not args.project_name and not args.stack_name:
        print("Error: --project-name or --stack-name required")
        parser.print_help()
        return 1

    project_name = args.project_name

    # Discover from CloudFormation stack
    if args.stack_name:
        if not project_name:
            # Infer project name from stack name
            project_name = args.stack_name.replace('Stack', '').replace('-dev', '').replace('-prod', '').lower()
            print(f"Inferred project name: {project_name}")

        print(f"🔍 Discovering resources from stack: {args.stack_name}")
        resources_to_sync = discover_from_stack(args.stack_name, project_name)

    # Manual specification
    else:
        # Amplify
        if args.amplify_app_id or args.amplify_app_name:
            app_id = args.amplify_app_id
            if not app_id and args.amplify_app_name:
                res = discover_amplify_by_name(args.amplify_app_name, project_name)
                if res:
                    resources_to_sync.append(res)
            elif app_id:
                ssm_path = get_ssm_path(project_name, 'amplify')
                current_value = get_from_ssm(ssm_path)
                resources_to_sync.append(ResourceSync(
                    resource_type='amplify',
                    resource_id=app_id,
                    ssm_path=ssm_path,
                    current_ssm_value=current_value,
                    needs_sync=current_value != app_id,
                ))

        # S3
        if args.s3_bucket:
            ssm_path = get_ssm_path(project_name, 's3', args.s3_suffix)
            current_value = get_from_ssm(ssm_path)
            resources_to_sync.append(ResourceSync(
                resource_type='s3',
                resource_id=args.s3_bucket,
                ssm_path=ssm_path,
                current_ssm_value=current_value,
                needs_sync=current_value != args.s3_bucket,
                metadata={'suffix': args.s3_suffix},
            ))

        # DynamoDB
        if args.dynamodb_table:
            ssm_path = get_ssm_path(project_name, 'dynamodb', args.dynamodb_suffix)
            current_value = get_from_ssm(ssm_path)
            resources_to_sync.append(ResourceSync(
                resource_type='dynamodb',
                resource_id=args.dynamodb_table,
                ssm_path=ssm_path,
                current_ssm_value=current_value,
                needs_sync=current_value != args.dynamodb_table,
                metadata={'suffix': args.dynamodb_suffix},
            ))

    if not resources_to_sync:
        print("❌ No resources found to sync.")
        return 1

    # Filter by resource type
    if args.resource_type != 'all':
        resources_to_sync = [r for r in resources_to_sync if r.resource_type == args.resource_type]

    print_resources(resources_to_sync)

    # Check if sync needed
    needs_sync = [r for r in resources_to_sync if r.needs_sync]
    if not needs_sync:
        print("✅ All resources already in sync!")
        return 0

    # Confirm and sync
    if not args.force and not args.dry_run:
        response = input(f"\nSync {len(needs_sync)} resource(s) to SSM? [y/N]: ")
        if response.lower() != 'y':
            print("Aborted.")
            return 0

    # Perform sync
    success_count = 0
    for res in needs_sync:
        description = f"{res.resource_type.capitalize()} resource for {project_name}"
        if res.metadata.get('suffix'):
            description += f" ({res.metadata['suffix']})"

        if store_in_ssm(res.ssm_path, res.resource_id, description, dry_run=args.dry_run):
            success_count += 1

    if not args.dry_run:
        print(f"\n✅ Synced {success_count}/{len(needs_sync)} resource(s)")
        print(f"\nYou can now use in CDK with mode='import'")

    return 0


if __name__ == '__main__':
    sys.exit(main())
