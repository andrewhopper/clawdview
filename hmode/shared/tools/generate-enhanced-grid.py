#!/usr/bin/env python3
"""Generate enhanced infrastructure data grid with resource details."""

import boto3
import json
from pathlib import Path
from typing import Dict, List, Set
import re
from collections import Counter

# Project to stacks mapping
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

def get_stack_resources(cfn, stack_name: str) -> List[str]:
    """Get resource types from stack."""
    try:
        resources = []
        paginator = cfn.get_paginator('list_stack_resources')
        for page in paginator.paginate(StackName=stack_name):
            for resource in page['StackResourceSummaries']:
                resources.append(resource['ResourceType'])
        return resources
    except:
        return []

def simplify_resource_type(resource_type: str) -> str:
    """Convert AWS::Service::Type to simplified name."""
    mapping = {
        'AWS::DynamoDB::Table': 'DynamoDB',
        'AWS::S3::Bucket': 'S3',
        'AWS::ECS::Service': 'ECS',
        'AWS::ECS::Cluster': 'ECS',
        'AWS::ECS::TaskDefinition': 'ECS',
        'AWS::Lambda::Function': 'Lambda',
        'AWS::ApiGateway::RestApi': 'API Gateway',
        'AWS::ApiGatewayV2::Api': 'API Gateway',
        'AWS::CloudFront::Distribution': 'CloudFront',
        'AWS::Cognito::UserPool': 'Cognito',
        'AWS::EC2::VPC': 'VPC',
        'AWS::RDS::DBInstance': 'RDS',
        'AWS::ECR::Repository': 'ECR',
        'AWS::IoT::Thing': 'IoT Core',
        'AWS::SQS::Queue': 'SQS',
        'AWS::SNS::Topic': 'SNS',
        'AWS::StepFunctions::StateMachine': 'Step Functions',
        'AWS::ElasticLoadBalancingV2::LoadBalancer': 'Load Balancer',
        'AWS::Amplify::App': 'Amplify',
        'AWS::CodePipeline::Pipeline': 'CodePipeline',
        'AWS::CodeBuild::Project': 'CodeBuild',
    }

    for key, value in mapping.items():
        if key in resource_type:
            return value

    # Default: extract service name
    if '::' in resource_type:
        parts = resource_type.split('::')
        return parts[1] if len(parts) > 1 else resource_type

    return resource_type

def get_infrastructure_summary(cfn, stacks: List[str]) -> str:
    """Get summarized infrastructure resources."""
    all_resources = []
    for stack in stacks:
        resources = get_stack_resources(cfn, stack)
        all_resources.extend(resources)

    # Simplify and count
    simplified = [simplify_resource_type(r) for r in all_resources]
    counts = Counter(simplified)

    # Sort by count and create summary
    sorted_resources = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    # Build summary string
    parts = []
    for resource, count in sorted_resources:
        # Skip CDK metadata and IAM roles/policies for cleaner view
        if resource in ['CDK', 'IAM', 'Metadata']:
            continue
        if count > 1:
            parts.append(f"{resource} ({count})")
        else:
            parts.append(resource)

    return ', '.join(parts[:10])  # Top 10 resource types

def get_stack_outputs(cfn, stack_name: str) -> Dict:
    """Get stack outputs."""
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

def extract_domains(outputs: Dict, project_data: Dict) -> tuple[str, List[str]]:
    """Extract primary domain and other domains."""
    all_domains = set()
    primary_domain = None

    # Check .project for primary domain
    if 'domain' in project_data:
        domain = str(project_data['domain'])
        if '.b.lfg.new' in domain:
            primary_domain = domain
        else:
            all_domains.add(domain)

    # Check deployment info
    if 'deployment' in project_data and isinstance(project_data['deployment'], dict):
        for env, details in project_data['deployment'].items():
            if isinstance(details, dict):
                if 'custom_domain' in details:
                    domain = details['custom_domain']
                    if '.b.lfg.new' in domain:
                        primary_domain = domain
                    else:
                        all_domains.add(domain)

    # Extract from outputs
    for key, value in outputs.items():
        if not isinstance(value, str):
            continue

        urls = re.findall(r'https?://[^\s,\'"]+', value)
        for url in urls:
            url = url.rstrip('/')
            if '.b.lfg.new' in url and not primary_domain:
                primary_domain = url
            else:
                all_domains.add(url)

    # Remove primary from other domains
    if primary_domain and primary_domain in all_domains:
        all_domains.remove(primary_domain)

    return primary_domain, sorted(list(all_domains))

def check_error_tracker(project_path: Path) -> bool:
    """Check if error tracker is installed."""
    # Check package.json
    package_json = project_path / 'package.json'
    if package_json.exists():
        try:
            with open(package_json, 'r') as f:
                pkg = json.load(f)
                deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}
                if '@protoflow/error-tracker' in deps or 'error-tracker' in deps:
                    return True
        except:
            pass

    # Check requirements.txt
    requirements = project_path / 'requirements.txt'
    if requirements.exists():
        content = requirements.read_text()
        if 'error-tracker' in content or 'error_tracker' in content:
            return True

    # Check for error-tracker config
    if (project_path / '.error-tracker.json').exists():
        return True

    return False

def check_iac_status(project_path: Path) -> str:
    """Check IAC status."""
    has_cdk = (
        (project_path / 'infra' / 'cdk.json').exists() or
        (project_path / 'cdk' / 'cdk.json').exists() or
        ((project_path / 'infra' / 'lib').exists() and (project_path / 'infra' / 'bin').exists())
    )
    return "All CDK" if has_cdk else "Imported Only"

def main():
    session = boto3.Session(profile_name='admin-507745175693', region_name='us-east-1')
    cfn = session.client('cloudformation')
    monorepo = Path('/Users/andyhop/dev/protoflow')

    data = []

    for project_path_str, stacks in PROJECT_STACKS.items():
        project_path = monorepo / project_path_str

        # Read .project
        project_file = project_path / '.project'
        project_data = {}
        if project_file.exists():
            with open(project_file, 'r') as f:
                try:
                    project_data = json.load(f)
                except:
                    pass

        # Get all outputs
        all_outputs = {}
        for stack in stacks:
            outputs = get_stack_outputs(cfn, stack)
            all_outputs.update(outputs)

        # Extract domains
        primary_domain, other_domains = extract_domains(all_outputs, project_data)

        # Get infrastructure summary
        infra_summary = get_infrastructure_summary(cfn, stacks)

        # Check error tracker
        has_error_tracker = check_error_tracker(project_path)

        # IAC status
        iac_status = check_iac_status(project_path)

        data.append({
            'uuid': project_data.get('uuid', project_data.get('id', project_path.name)),
            'name': project_data.get('name', project_path.name),
            'stacks': stacks,
            'stack_count': len(stacks),
            'infrastructure': infra_summary,
            'primary_domain': primary_domain or 'N/A',
            'other_domains': other_domains,
            'config_path': project_path_str + '/infra/config/config.yml',
            'iac_status': iac_status,
            'has_error_tracker': has_error_tracker,
            'project_path': project_path_str
        })

    # Sort by stack count
    data.sort(key=lambda x: x['stack_count'], reverse=True)

    print(json.dumps(data, indent=2))

if __name__ == '__main__':
    main()
