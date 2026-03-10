#!/usr/bin/env python3
# File UUID: 7c8d9e0f-1a2b-3c4d-5e6f-7a8b9c0d1e2f

"""
Sync Amplify App IDs to SSM

Discovers Amplify app IDs from existing infrastructure and stores them in SSM.
This allows CDK to always use mode='import' without manual toggling.

Usage:
    # Sync a specific project
    python sync-amplify-to-ssm.py --project-name myproject

    # Sync by CloudFormation stack name
    python sync-amplify-to-ssm.py --stack-name MyProjectStack

    # Auto-discover from all stacks with Amplify apps
    python sync-amplify-to-ssm.py --auto-discover

    # Sync using project UUID
    python sync-amplify-to-ssm.py --project-uuid a1b2c3d4

    # Dry run (preview only)
    python sync-amplify-to-ssm.py --project-name myproject --dry-run
"""

import argparse
import boto3
import json
import sys
from typing import Optional, Dict, List
from pathlib import Path

# Initialize AWS clients
cf_client = boto3.client('cloudformation')
amplify_client = boto3.client('amplify')
ssm_client = boto3.client('ssm')


def get_ssm_path(project_name: str) -> str:
    """Get SSM parameter path for project."""
    return f"/protoflow/projects/{project_name}/amplify-app-id"


def find_amplify_app_in_stack(stack_name: str) -> Optional[str]:
    """Find Amplify app ID from CloudFormation stack outputs."""
    try:
        response = cf_client.describe_stacks(StackName=stack_name)
        stacks = response.get('Stacks', [])

        if not stacks:
            return None

        stack = stacks[0]
        outputs = stack.get('Outputs', [])

        # Look for output keys that contain "Amplify" and "App"
        for output in outputs:
            key = output.get('OutputKey', '')
            if 'amplify' in key.lower() and 'app' in key.lower() and 'id' in key.lower():
                return output.get('OutputValue')

        # Also check stack resources directly
        response = cf_client.list_stack_resources(StackName=stack_name)
        resources = response.get('StackResourceSummaries', [])

        for resource in resources:
            if resource.get('ResourceType') == 'AWS::Amplify::App':
                return resource.get('PhysicalResourceId')

        return None
    except Exception as e:
        print(f"Error finding Amplify app in stack {stack_name}: {e}", file=sys.stderr)
        return None


def find_amplify_app_by_name(app_name: str) -> Optional[str]:
    """Find Amplify app ID by app name."""
    try:
        response = amplify_client.list_apps(maxResults=100)
        apps = response.get('apps', [])

        for app in apps:
            if app.get('name') == app_name:
                return app.get('appId')

        return None
    except Exception as e:
        print(f"Error finding Amplify app by name {app_name}: {e}", file=sys.stderr)
        return None


def get_amplify_app_info(app_id: str) -> Dict:
    """Get Amplify app details."""
    try:
        response = amplify_client.get_app(appId=app_id)
        app = response.get('app', {})
        return {
            'appId': app.get('appId'),
            'name': app.get('name'),
            'defaultDomain': app.get('defaultDomain'),
            'repository': app.get('repository', 'N/A'),
        }
    except Exception as e:
        print(f"Error getting Amplify app info: {e}", file=sys.stderr)
        return {}


def store_in_ssm(project_name: str, app_id: str, dry_run: bool = False) -> bool:
    """Store Amplify app ID in SSM."""
    ssm_path = get_ssm_path(project_name)

    if dry_run:
        print(f"[DRY RUN] Would store: {ssm_path} = {app_id}")
        return True

    try:
        ssm_client.put_parameter(
            Name=ssm_path,
            Value=app_id,
            Type='String',
            Description=f"Amplify App ID for {project_name}",
            Overwrite=True,  # Upsert behavior
        )
        print(f"✅ Stored: {ssm_path} = {app_id}")
        return True
    except Exception as e:
        print(f"❌ Error storing in SSM: {e}", file=sys.stderr)
        return False


def get_from_ssm(project_name: str) -> Optional[str]:
    """Get current value from SSM."""
    ssm_path = get_ssm_path(project_name)
    try:
        response = ssm_client.get_parameter(Name=ssm_path)
        return response['Parameter']['Value']
    except ssm_client.exceptions.ParameterNotFound:
        return None
    except Exception as e:
        print(f"Error reading from SSM: {e}", file=sys.stderr)
        return None


def find_project_uuid_from_name(project_name: str) -> Optional[str]:
    """Find project UUID from project name by reading .project file."""
    # Search in projects directory
    projects_dir = Path('/home/user/protoflow/projects')

    # Common project locations
    search_paths = [
        projects_dir / 'personal' / 'active',
        projects_dir / 'work',
        projects_dir / 'shared',
        projects_dir / 'unspecified',
    ]

    for search_path in search_paths:
        if not search_path.exists():
            continue

        for project_dir in search_path.iterdir():
            if not project_dir.is_dir():
                continue

            # Check if directory name contains project name
            if project_name.lower() in project_dir.name.lower():
                project_file = project_dir / '.project'
                if project_file.exists():
                    # Read .project file to get UUID
                    content = project_file.read_text()
                    # Simple extraction - could be more robust
                    for line in content.split('\n'):
                        if 'uuid:' in line.lower():
                            uuid = line.split(':', 1)[1].strip()
                            return uuid

    return None


def auto_discover_all() -> List[Dict]:
    """Auto-discover all Amplify apps and suggest SSM mappings."""
    print("🔍 Auto-discovering Amplify apps...")

    try:
        response = amplify_client.list_apps(maxResults=100)
        apps = response.get('apps', [])

        results = []
        for app in apps:
            app_id = app.get('appId')
            app_name = app.get('name')

            # Try to infer project name from app name
            # Common patterns: "myproject-frontend", "myproject-web", etc.
            project_name = app_name
            for suffix in ['-frontend', '-web', '-app', '-ui']:
                if project_name.endswith(suffix):
                    project_name = project_name[:-len(suffix)]
                    break

            # Check if already in SSM
            current_ssm_value = get_from_ssm(project_name)

            results.append({
                'appId': app_id,
                'appName': app_name,
                'projectName': project_name,
                'currentSsmValue': current_ssm_value,
                'needsSync': current_ssm_value != app_id,
            })

        return results
    except Exception as e:
        print(f"Error auto-discovering: {e}", file=sys.stderr)
        return []


def main():
    parser = argparse.ArgumentParser(
        description='Sync Amplify app IDs to SSM for infrastructure state management'
    )

    # Input methods (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--project-name', help='Project name (e.g., myproject)')
    input_group.add_argument('--project-uuid', help='Project UUID')
    input_group.add_argument('--stack-name', help='CloudFormation stack name')
    input_group.add_argument('--auto-discover', action='store_true',
                            help='Auto-discover all Amplify apps')

    # Optional parameters
    parser.add_argument('--app-id', help='Amplify app ID (if known)')
    parser.add_argument('--app-name', help='Amplify app name (for lookup)')
    parser.add_argument('--dry-run', action='store_true', help='Preview without making changes')
    parser.add_argument('--force', action='store_true', help='Overwrite existing SSM values')

    args = parser.parse_args()

    # Auto-discover mode
    if args.auto_discover:
        results = auto_discover_all()

        if not results:
            print("No Amplify apps found.")
            return 0

        print(f"\nFound {len(results)} Amplify app(s):\n")

        for i, result in enumerate(results, 1):
            status = "✅ In sync" if not result['needsSync'] else "⚠️  Needs sync"
            print(f"{i}. {result['appName']}")
            print(f"   App ID: {result['appId']}")
            print(f"   Project: {result['projectName']}")
            print(f"   SSM: {result['currentSsmValue'] or '(not set)'}")
            print(f"   Status: {status}")
            print()

        # Ask to sync all that need it
        needs_sync = [r for r in results if r['needsSync']]
        if needs_sync and not args.dry_run:
            response = input(f"\nSync {len(needs_sync)} app(s) to SSM? [y/N]: ")
            if response.lower() == 'y':
                for result in needs_sync:
                    store_in_ssm(result['projectName'], result['appId'], dry_run=False)

        return 0

    # Project UUID mode
    if args.project_uuid:
        # TODO: Could look up project name from UUID in future
        print("Error: --project-uuid not yet implemented. Use --project-name instead.")
        return 1

    # Determine project name
    project_name = args.project_name
    if args.stack_name:
        # Extract project name from stack name (heuristic)
        # Common patterns: "MyProjectStack", "myproject-dev", etc.
        project_name = args.stack_name.replace('Stack', '').replace('-dev', '').replace('-prod', '').lower()
        print(f"Inferred project name: {project_name}")

    # Find Amplify app ID
    app_id = args.app_id

    if not app_id and args.stack_name:
        print(f"🔍 Looking for Amplify app in stack: {args.stack_name}")
        app_id = find_amplify_app_in_stack(args.stack_name)

    if not app_id and args.app_name:
        print(f"🔍 Looking for Amplify app by name: {args.app_name}")
        app_id = find_amplify_app_by_name(args.app_name)

    if not app_id:
        print(f"🔍 Trying to find Amplify app by project name: {project_name}")
        # Try common naming patterns
        for suffix in ['', '-frontend', '-web', '-app']:
            app_name = f"{project_name}{suffix}"
            app_id = find_amplify_app_by_name(app_name)
            if app_id:
                print(f"Found app: {app_name}")
                break

    if not app_id:
        print(f"❌ Could not find Amplify app for project: {project_name}")
        print("\nTry specifying explicitly:")
        print(f"  --app-id <amplify-app-id>")
        print(f"  --app-name <amplify-app-name>")
        print(f"  --stack-name <cloudformation-stack>")
        return 1

    # Get app info
    print(f"\n📱 Amplify App Details:")
    app_info = get_amplify_app_info(app_id)
    for key, value in app_info.items():
        print(f"   {key}: {value}")

    # Check current SSM value
    current_value = get_from_ssm(project_name)
    if current_value:
        print(f"\n📝 Current SSM value: {current_value}")
        if current_value == app_id and not args.force:
            print("✅ Already in sync, no changes needed.")
            return 0
        elif not args.force:
            response = input("\n⚠️  SSM value exists. Overwrite? [y/N]: ")
            if response.lower() != 'y':
                print("Aborted.")
                return 0

    # Store in SSM
    print(f"\n💾 Storing in SSM...")
    success = store_in_ssm(project_name, app_id, dry_run=args.dry_run)

    if success and not args.dry_run:
        print(f"\n✅ Success! You can now use in CDK:")
        print(f"""
from aws_cdk_lib import SharedAmplifyApp

app = SharedAmplifyApp(self, 'App', {{
    projectName: '{project_name}',
    mode: 'import',  # Always import, no toggling needed
}})
        """)

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
