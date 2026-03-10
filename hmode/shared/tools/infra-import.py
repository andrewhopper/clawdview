#!/usr/bin/env python3
"""
Infrastructure Import Tool
Scans existing AWS CloudFormation/CDK stacks and imports them into Capistrano-style structure.
Extracts secrets to AWS Secrets Manager and creates git-safe config files.
"""

import boto3
import json
import os
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import re
import argparse


class InfraImporter:
    """Import existing AWS infrastructure into Capistrano-style deployment structure."""

    def __init__(self, profile: str = "admin-507745175693", region: str = "us-east-1"):
        """Initialize AWS clients."""
        self.session = boto3.Session(profile_name=profile, region_name=region)
        self.cfn = self.session.client('cloudformation')
        self.secrets = self.session.client('secretsmanager')
        self.region = region
        self.account_id = self.session.client('sts').get_caller_identity()['Account']

    def list_stacks(self) -> List[Dict[str, Any]]:
        """List all CloudFormation stacks in the account."""
        stacks = []
        paginator = self.cfn.get_paginator('list_stacks')

        # Only get active stacks (not deleted)
        for page in paginator.paginate(
            StackStatusFilter=[
                'CREATE_COMPLETE', 'UPDATE_COMPLETE', 'ROLLBACK_COMPLETE',
                'UPDATE_ROLLBACK_COMPLETE', 'IMPORT_COMPLETE'
            ]
        ):
            stacks.extend(page['StackSummaries'])

        return stacks

    def get_stack_details(self, stack_name: str) -> Dict[str, Any]:
        """Get detailed information about a stack."""
        response = self.cfn.describe_stacks(StackName=stack_name)
        stack = response['Stacks'][0]

        # Get outputs
        outputs = {}
        if 'Outputs' in stack:
            for output in stack['Outputs']:
                outputs[output['OutputKey']] = {
                    'value': output['OutputValue'],
                    'description': output.get('Description', ''),
                    'export_name': output.get('ExportName', '')
                }

        # Get parameters
        parameters = {}
        if 'Parameters' in stack:
            for param in stack['Parameters']:
                parameters[param['ParameterKey']] = param['ParameterValue']

        # Get tags
        tags = {}
        if 'Tags' in stack:
            for tag in stack['Tags']:
                tags[tag['Key']] = tag['Value']

        return {
            'stack_name': stack['StackName'],
            'stack_id': stack['StackId'],
            'status': stack['StackStatus'],
            'created_time': stack['CreationTime'].isoformat(),
            'last_updated': stack.get('LastUpdatedTime', stack['CreationTime']).isoformat(),
            'outputs': outputs,
            'parameters': parameters,
            'tags': tags,
            'description': stack.get('Description', '')
        }

    def get_stack_resources(self, stack_name: str) -> List[Dict[str, Any]]:
        """Get all resources in a stack."""
        resources = []
        paginator = self.cfn.get_paginator('list_stack_resources')

        for page in paginator.paginate(StackName=stack_name):
            for resource in page['StackResourceSummaries']:
                resources.append({
                    'logical_id': resource['LogicalResourceId'],
                    'physical_id': resource.get('PhysicalResourceId', ''),
                    'type': resource['ResourceType'],
                    'status': resource['ResourceStatus'],
                    'timestamp': resource['LastUpdatedTimestamp'].isoformat()
                })

        return resources

    def extract_secrets(self, config: Dict[str, Any]) -> tuple[Dict[str, Any], Dict[str, str]]:
        """
        Extract secrets from config and return (sanitized_config, secrets_dict).

        Detects common secret patterns:
        - Keys containing: password, secret, key, token, credential
        - Values that look like AWS access keys, API keys, etc.
        """
        secrets = {}
        sanitized = {}

        secret_patterns = [
            'password', 'secret', 'key', 'token', 'credential',
            'api_key', 'access_key', 'private', 'auth'
        ]

        def is_secret_key(key: str) -> bool:
            key_lower = key.lower()
            return any(pattern in key_lower for pattern in secret_patterns)

        def is_secret_value(value: str) -> bool:
            if not isinstance(value, str):
                return False
            # Check for common secret formats
            patterns = [
                r'^AKIA[0-9A-Z]{16}$',  # AWS access key
                r'^[A-Za-z0-9+/]{40}$',  # AWS secret key
                r'^sk-[a-zA-Z0-9]{32,}$',  # API keys starting with sk-
                r'^[a-f0-9]{32,}$',  # Long hex strings
            ]
            return any(re.match(pattern, value) for pattern in patterns)

        for key, value in config.items():
            if isinstance(value, dict):
                sanitized[key], nested_secrets = self.extract_secrets(value)
                secrets.update(nested_secrets)
            elif is_secret_key(key) or is_secret_value(str(value)):
                secret_key = f"{key}"
                secrets[secret_key] = str(value)
                # Replace with Secrets Manager reference
                sanitized[key] = f"{{{{secrets.{secret_key}}}}}"
            else:
                sanitized[key] = value

        return sanitized, secrets

    def store_secrets(self, project_name: str, secrets: Dict[str, str]) -> str:
        """Store secrets in AWS Secrets Manager and return the secret ARN."""
        secret_name = f"{project_name}/config"

        try:
            # Try to create new secret
            response = self.secrets.create_secret(
                Name=secret_name,
                SecretString=json.dumps(secrets),
                Description=f"Configuration secrets for {project_name}"
            )
            print(f"✓ Created new secret: {secret_name}")
            return response['ARN']
        except self.secrets.exceptions.ResourceExistsException:
            # Update existing secret
            response = self.secrets.update_secret(
                SecretId=secret_name,
                SecretString=json.dumps(secrets)
            )
            print(f"✓ Updated existing secret: {secret_name}")
            # Get ARN
            describe = self.secrets.describe_secret(SecretId=secret_name)
            return describe['ARN']

    def create_release_structure(
        self,
        project_path: Path,
        stack_details: Dict[str, Any],
        resources: List[Dict[str, Any]],
        timestamp: Optional[str] = None
    ) -> Path:
        """Create Capistrano-style release directory."""
        if timestamp is None:
            timestamp = datetime.now().strftime('%Y%m%d-%H%M')

        # Create directory structure
        releases_dir = project_path / 'infra' / 'deploys' / 'releases'
        release_dir = releases_dir / timestamp
        release_dir.mkdir(parents=True, exist_ok=True)

        shared_dir = project_path / 'infra' / 'deploys' / 'shared'
        shared_dir.mkdir(parents=True, exist_ok=True)

        # Write outputs.json
        outputs_file = release_dir / 'outputs.json'
        outputs_file.write_text(json.dumps(stack_details['outputs'], indent=2))

        # Write manifest.json
        manifest = {
            'timestamp': timestamp,
            'stack_name': stack_details['stack_name'],
            'stack_id': stack_details['stack_id'],
            'status': stack_details['status'],
            'deployed_at': stack_details['last_updated'],
            'region': self.region,
            'account_id': self.account_id,
            'resource_count': len(resources)
        }
        manifest_file = release_dir / 'manifest.json'
        manifest_file.write_text(json.dumps(manifest, indent=2))

        # Write resources.json
        resources_file = release_dir / 'resources.json'
        resources_file.write_text(json.dumps(resources, indent=2))

        # Write deploy.log (metadata)
        log_file = release_dir / 'deploy.log'
        log_file.write_text(f"""Deployment Import Log
Timestamp: {timestamp}
Stack: {stack_details['stack_name']}
Status: {stack_details['status']}
Region: {self.region}
Account: {self.account_id}

Imported from existing CloudFormation stack.
""")

        # Update 'current' symlink
        current_link = project_path / 'infra' / 'deploys' / 'current'
        if current_link.exists() or current_link.is_symlink():
            current_link.unlink()
        current_link.symlink_to(f'releases/{timestamp}')

        return release_dir

    def create_config_files(
        self,
        project_path: Path,
        stack_details: Dict[str, Any],
        secrets_arn: Optional[str] = None
    ) -> None:
        """Create git-safe config files with Secrets Manager references."""
        config_dir = project_path / 'infra' / 'config'
        config_dir.mkdir(parents=True, exist_ok=True)

        # Create config.yml (git-safe)
        config = {
            'project': stack_details['stack_name'],
            'region': self.region,
            'account_id': self.account_id,
            'stack_id': stack_details['stack_id'],
            'secrets_arn': secrets_arn or 'none',
            'tags': stack_details['tags'],
            'parameters': stack_details['parameters']
        }

        # Extract and sanitize secrets
        sanitized_config, extracted_secrets = self.extract_secrets(config)

        # Write sanitized config
        config_file = config_dir / 'config.yml'
        config_file.write_text(yaml.dump(sanitized_config, default_flow_style=False))

        # Create .env.example (template)
        env_example = config_dir / '.env.example'
        env_lines = [
            "# Environment Configuration",
            "# Copy to .env and fill in values",
            "# Secrets are stored in AWS Secrets Manager",
            "",
            f"AWS_REGION={self.region}",
            f"AWS_ACCOUNT_ID={self.account_id}",
            f"STACK_NAME={stack_details['stack_name']}",
            ""
        ]

        # Add secret placeholders
        if extracted_secrets:
            env_lines.append("# Secrets (loaded from AWS Secrets Manager)")
            for key in extracted_secrets.keys():
                env_lines.append(f"{key.upper()}={{{{secrets.{key}}}}}")

        env_example.write_text('\n'.join(env_lines))

        # Create secrets loader script
        loader_script = config_dir / 'load-secrets.sh'
        loader_script.write_text(f'''#!/bin/bash
# Load secrets from AWS Secrets Manager
# Usage: source infra/config/load-secrets.sh

set -e

AWS_PROFILE="${{AWS_PROFILE:-admin-507745175693}}"
SECRET_NAME="{stack_details['stack_name']}/config"

echo "Loading secrets from $SECRET_NAME..."

# Get secrets from AWS Secrets Manager
SECRETS=$(aws secretsmanager get-secret-value \\
    --secret-id "$SECRET_NAME" \\
    --profile "$AWS_PROFILE" \\
    --query SecretString \\
    --output text)

# Export as environment variables
while IFS= read -r line; do
    KEY=$(echo "$line" | cut -d: -f1 | tr -d ' "')
    VALUE=$(echo "$line" | cut -d: -f2- | sed 's/^[[:space:]]*"//;s/"[[:space:]]*,*$//')

    if [ -n "$KEY" ] && [ "$KEY" != "{{" ] && [ "$KEY" != "}}" ]; then
        export "$KEY=$VALUE"
        echo "✓ Loaded $KEY"
    fi
done < <(echo "$SECRETS" | jq -r 'to_entries | .[] | "\\(.key): \\(.value)"')

echo "✓ Secrets loaded successfully"
''')
        loader_script.chmod(0o755)

        print(f"✓ Created config files in {config_dir}")

    def import_stack(
        self,
        stack_name: str,
        project_path: Optional[Path] = None,
        store_secrets: bool = True
    ) -> None:
        """Import a single stack into the Capistrano structure."""
        print(f"\n📦 Importing stack: {stack_name}")

        # Get stack details
        stack_details = self.get_stack_details(stack_name)
        resources = self.get_stack_resources(stack_name)

        print(f"   Stack ID: {stack_details['stack_id']}")
        print(f"   Status: {stack_details['status']}")
        print(f"   Resources: {len(resources)}")
        print(f"   Outputs: {len(stack_details['outputs'])}")

        # Determine project path
        if project_path is None:
            # Use current directory
            project_path = Path.cwd()

        # Extract and store secrets
        secrets_arn = None
        if store_secrets:
            _, extracted_secrets = self.extract_secrets(stack_details['parameters'])
            if extracted_secrets:
                secrets_arn = self.store_secrets(stack_name, extracted_secrets)
                print(f"   Secrets: {len(extracted_secrets)} stored in Secrets Manager")

        # Create release structure
        release_dir = self.create_release_structure(
            project_path,
            stack_details,
            resources
        )
        print(f"   ✓ Created release: {release_dir}")

        # Create config files
        self.create_config_files(project_path, stack_details, secrets_arn)

        print(f"✓ Import complete: {stack_name}\n")

    def import_all_stacks(
        self,
        output_dir: Optional[Path] = None,
        filter_prefix: Optional[str] = None
    ) -> None:
        """Import all stacks in the account."""
        stacks = self.list_stacks()

        if filter_prefix:
            stacks = [s for s in stacks if s['StackName'].startswith(filter_prefix)]

        print(f"\n🔍 Found {len(stacks)} stacks to import")

        for stack in stacks:
            stack_name = stack['StackName']

            # Create project directory if using output_dir
            if output_dir:
                project_dir = output_dir / stack_name
                project_dir.mkdir(parents=True, exist_ok=True)
            else:
                project_dir = None

            try:
                self.import_stack(stack_name, project_dir)
            except Exception as e:
                print(f"✗ Error importing {stack_name}: {e}")
                continue


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Import existing AWS infrastructure into Capistrano-style structure'
    )
    parser.add_argument(
        '--stack',
        help='Import a specific stack by name'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Import all stacks in the account'
    )
    parser.add_argument(
        '--prefix',
        help='Filter stacks by name prefix'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        help='Output directory for imported stacks (default: current directory)'
    )
    parser.add_argument(
        '--profile',
        default='admin-507745175693',
        help='AWS profile to use (default: admin-507745175693)'
    )
    parser.add_argument(
        '--region',
        default='us-east-1',
        help='AWS region (default: us-east-1)'
    )
    parser.add_argument(
        '--no-secrets',
        action='store_true',
        help='Skip extracting secrets to Secrets Manager'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all stacks and exit'
    )

    args = parser.parse_args()

    # Initialize importer
    importer = InfraImporter(profile=args.profile, region=args.region)

    # List stacks
    if args.list:
        stacks = importer.list_stacks()
        print(f"\n📋 CloudFormation Stacks ({len(stacks)}):\n")
        for stack in stacks:
            print(f"   • {stack['StackName']}")
            print(f"     Status: {stack['StackStatus']}")
            print(f"     Updated: {stack.get('LastUpdatedTime', stack['CreationTime'])}")
            print()
        return

    # Import stacks
    if args.stack:
        importer.import_stack(
            args.stack,
            args.output_dir or Path.cwd(),
            store_secrets=not args.no_secrets
        )
    elif args.all:
        importer.import_all_stacks(
            args.output_dir,
            filter_prefix=args.prefix
        )
    else:
        parser.print_help()
        print("\nError: Specify --stack NAME, --all, or --list")
        exit(1)

    print("\n✅ Import complete!")
    print("\nNext steps:")
    print("1. Review infra/config/config.yml (git-safe)")
    print("2. Source infra/config/load-secrets.sh to load secrets")
    print("3. Commit config files to git")
    print("4. Add infra/deploys/ to .gitignore (optional)")


if __name__ == '__main__':
    main()
