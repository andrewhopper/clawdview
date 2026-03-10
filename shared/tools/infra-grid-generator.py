#!/usr/bin/env python3
"""
Infrastructure Data Grid Generator
Creates comprehensive data grid of all projects with infrastructure tracking.
"""

import json
import yaml
import os
from pathlib import Path
from typing import Dict, List, Any
import re


def get_all_stacks_for_project(project_path: Path) -> List[str]:
    """Get all stack names from manifest files."""
    stacks = []
    releases_dir = project_path / 'infra' / 'deploys' / 'releases'

    if not releases_dir.exists():
        return stacks

    # Get all manifest files
    for manifest_file in releases_dir.glob('*/manifest.json'):
        try:
            with open(manifest_file, 'r') as f:
                manifest = json.load(f)
                if 'stack_name' in manifest:
                    stack_name = manifest['stack_name']
                    if stack_name not in stacks:
                        stacks.append(stack_name)
        except:
            continue

    return stacks


def get_domains_from_outputs(project_path: Path) -> List[str]:
    """Extract domain names from outputs.json."""
    domains = set()
    outputs_file = project_path / 'infra' / 'deploys' / 'current' / 'outputs.json'

    if not outputs_file.exists():
        return list(domains)

    try:
        with open(outputs_file, 'r') as f:
            outputs = json.load(f)

            for key, value in outputs.items():
                val = value.get('value', '') if isinstance(value, dict) else value

                if not isinstance(val, str):
                    continue

                # Extract URLs
                url_matches = re.findall(r'https?://[^\s,\'"]+', val)
                for url in url_matches:
                    # Clean up URL
                    url = url.rstrip('/')
                    domains.add(url)

                # Extract domain-like strings (without http)
                if any(tld in val for tld in ['.com', '.net', '.new', '.io', '.org']) and 'http' not in val:
                    # Check if it's a clean domain
                    domain_match = re.search(r'([a-z0-9-]+\.[a-z0-9.-]+\.(com|net|new|io|org))', val, re.IGNORECASE)
                    if domain_match:
                        domains.add(domain_match.group(1))
    except:
        pass

    return sorted(list(domains))


def check_iac_status(project_path: Path, stacks: List[str]) -> str:
    """Determine IAC status (All CDK, Some CDK, No CDK)."""
    # Check for CDK infrastructure code
    has_cdk_code = (
        (project_path / 'infra' / 'cdk.json').exists() or
        (project_path / 'cdk' / 'cdk.json').exists() or
        (project_path / 'infra' / 'lib').exists() or
        (project_path / 'infra' / 'bin').exists()
    )

    if has_cdk_code:
        return "All CDK"
    elif stacks:
        # Has stacks but no CDK code - was deployed but not tracked as IaC
        return "Imported Only"
    else:
        return "No CDK"


def generate_grid_data() -> List[Dict[str, Any]]:
    """Generate complete grid data for all projects."""
    monorepo_root = Path('/Users/andyhop/dev/protoflow')
    projects_dir = monorepo_root / 'projects'

    # Find all projects with imported infrastructure
    project_paths = []
    for config_file in projects_dir.rglob('infra/config/config.yml'):
        project_path = config_file.parent.parent.parent
        project_paths.append(project_path)

    data = []

    for project_path in project_paths:
        # Read .project file
        project_file = project_path / '.project'
        project_data = {}

        if project_file.exists():
            with open(project_file, 'r') as f:
                content = f.read()
                try:
                    project_data = json.loads(content)
                except:
                    # Parse as YAML-like
                    try:
                        project_data = yaml.safe_load(content) or {}
                    except:
                        project_data = {}

        # Get all stacks
        stacks = get_all_stacks_for_project(project_path)

        # Get domains
        domains = get_domains_from_outputs(project_path)

        # Add domain from .project if exists
        if 'domain' in project_data:
            domains.insert(0, str(project_data['domain']))

        # Get config path (relative)
        try:
            config_path = project_path.relative_to(monorepo_root) / 'infra' / 'config' / 'config.yml'
        except:
            config_path = project_path / 'infra' / 'config' / 'config.yml'

        # Determine IAC status
        iac_status = check_iac_status(project_path, stacks)

        # Get project name
        project_name = project_data.get('name', project_path.name)

        # Get UUID
        uuid = project_data.get('uuid', project_data.get('id', project_path.name))

        data.append({
            'uuid': str(uuid),
            'name': str(project_name),
            'stacks': ', '.join(stacks) if stacks else 'N/A',
            'stack_count': len(stacks),
            'domains': ', '.join(domains) if domains else 'N/A',
            'config_path': str(config_path),
            'iac_status': iac_status,
            'project_path': str(project_path.relative_to(monorepo_root))
        })

    # Sort by stack count (descending)
    data.sort(key=lambda x: x['stack_count'], reverse=True)

    return data


def main():
    """Generate and output grid data."""
    data = generate_grid_data()
    print(json.dumps(data, indent=2))


if __name__ == '__main__':
    main()
