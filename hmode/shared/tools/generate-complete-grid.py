#!/usr/bin/env python3
"""Generate complete infrastructure data grid from AWS and local projects."""

import boto3
import json
from pathlib import Path
from typing import Dict, List
import re

# Project to stacks mapping (from our imports today)
PROJECT_STACKS = {
    "projects/personal/resource-manager-a2d7a": ["ResourceManager-dev"],
    "projects/personal/browser-check-api": ["BrowserCheckStack"],
    "projects/personal/tinder-approval-ui-gaawu": ["ApprovalStack", "ApprovalIoTStack"],
    "projects/personal/active/avatar-pipeline-53e47": ["AvatarPipeline-dev", "AvatarMicroservices-dev", "AvatarFrontend-dev"],
    "projects/personal/pcm-16ddc": ["PcmStack-dev"],
    "projects/personal/proto-story-wizard-web-8f4a2-001": ["StoryWizardStack"],
    "projects/unspecified/active/poc-web-bedrock-supabase-nextjs-joke-creator-1pwho": ["Supabase"],
    "projects/personal/active/tool-gocoder-web-agentic-coding-ui-like-claude-code-web-t9x2k": [
        "GoCoderAuthStack", "GoCoderNetworkStack", "GoCoderStorageStack",
        "GoCoderComputeStack", "GoCoderControlPlaneStack", "GoCoderFrontendStack",
        "GoCoderIoTStack", "GoCoderPipelineStack", "GoCoderPipelineStandaloneStack"
    ],
    "projects/personal/voice-review-agent": [
        "VoiceReview-CloudFront-dev", "VoiceReview-Amplify-dev", "VoiceReview-Backend-dev",
        "VoiceReview-Build-dev", "VoiceReview-Network-dev",
        "S2SCDK-S2SStack-dev", "S2SCDK-NetworkStack-dev",
        "S2SCDK-S2SStack-prod", "S2SCDK-NetworkStack-prod"
    ],
    "projects/shared/proto-audio-notetaker-4bdf7-001": ["MoAuthStack-personal", "MoBackendStack"],
    "projects/shared/shared-auth-gateway": ["shared-auth-AuthGatewayStack"],
    "projects/shared/aws-cdk-bootstrap": ["CDKToolkit"],
}

def get_stack_outputs(cfn, stack_name: str) -> Dict:
    """Get stack outputs from AWS."""
    try:
        response = cfn.describe_stacks(StackName=stack_name)
        stack = response['Stacks'][0]
        outputs = {}
        if 'Outputs' in stack:
            for output in stack['Outputs']:
                outputs[output['OutputKey']] = output['OutputValue']
        return outputs
    except:
        return {}

def extract_domains(outputs: Dict) -> List[str]:
    """Extract domains from stack outputs."""
    domains = set()
    for key, value in outputs.items():
        if not isinstance(value, str):
            continue
        # Extract URLs
        urls = re.findall(r'https?://[^\s,\'"]+', value)
        for url in urls:
            domains.add(url.rstrip('/'))
        # Extract domain-like strings
        if any(tld in value for tld in ['.com', '.net', '.new', '.io']) and 'http' not in value:
            match = re.search(r'([a-z0-9-]+\.[a-z0-9.-]+\.(com|net|new|io|org|aws))', value, re.IGNORECASE)
            if match:
                domains.add(match.group(1))
    return sorted(list(domains))

def check_iac_status(project_path: Path) -> str:
    """Check if project has CDK code."""
    has_cdk = (
        (project_path / 'infra' / 'cdk.json').exists() or
        (project_path / 'cdk' / 'cdk.json').exists() or
        (project_path / 'infra' / 'lib').exists() and (project_path / 'infra' / 'bin').exists()
    )
    return "All CDK" if has_cdk else "Imported Only"

def main():
    session = boto3.Session(profile_name='admin-507745175693', region_name='us-east-1')
    cfn = session.client('cloudformation')

    monorepo = Path('/Users/andyhop/dev/protoflow')
    data = []

    for project_path_str, stacks in PROJECT_STACKS.items():
        project_path = monorepo / project_path_str

        # Read .project file
        project_file = project_path / '.project'
        project_data = {}
        if project_file.exists():
            with open(project_file, 'r') as f:
                try:
                    project_data = json.load(f)
                except:
                    pass

        # Get all domains from all stacks
        all_domains = set()
        for stack in stacks:
            outputs = get_stack_outputs(cfn, stack)
            domains = extract_domains(outputs)
            all_domains.update(domains)

        # Add domain from .project
        if 'domain' in project_data:
            all_domains.add(str(project_data['domain']))

        # Get deployment info
        if 'deployment' in project_data and isinstance(project_data['deployment'], dict):
            for env, details in project_data['deployment'].items():
                if isinstance(details, dict):
                    if 'custom_domain' in details:
                        all_domains.add(details['custom_domain'])
                    if 'url' in details:
                        all_domains.add(details['url'])

        # Config path
        config_path = project_path_str + '/infra/config/config.yml'

        # IAC status
        iac_status = check_iac_status(project_path)

        data.append({
            'uuid': project_data.get('uuid', project_data.get('id', project_path.name)),
            'name': project_data.get('name', project_path.name),
            'stacks': ', '.join(stacks),
            'stack_count': len(stacks),
            'domains': ', '.join(sorted(all_domains)) if all_domains else 'N/A',
            'config_path': config_path,
            'iac_status': iac_status,
            'project_path': project_path_str
        })

    # Sort by stack count
    data.sort(key=lambda x: x['stack_count'], reverse=True)

    print(json.dumps(data, indent=2))

if __name__ == '__main__':
    main()
