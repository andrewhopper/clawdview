#!/usr/bin/env python3
# File UUID: 8a3f7b2c-1d4e-5f6a-9b0c-2e3d4f5a6b7c
"""
Generate buildinfo.json for frontend deployments.

Combines git metadata with CDK infrastructure outputs to create a single
buildinfo.json file that ships with the frontend bundle.

Usage:
    # Basic - just git info
    python generate-buildinfo.py --output dist/buildinfo.json

    # With CDK outputs
    python generate-buildinfo.py --output dist/buildinfo.json --cdk-outputs infra/deploys/current/outputs.json

    # With specific stack name filter
    python generate-buildinfo.py --output public/buildinfo.json --cdk-outputs outputs.json --stack MyAppStack

    # With project ID and environment
    python generate-buildinfo.py --output dist/buildinfo.json --project-id my-app-12345 --environment prod
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


def get_git_info() -> dict[str, str]:
    """Get git metadata for the current repository."""
    info = {
        "gitHash": "unknown",
        "gitHashFull": "unknown",
        "gitBranch": "unknown",
        "gitDirty": False,
    }

    try:
        # Short hash
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        info["gitHash"] = result.stdout.strip()

        # Full hash
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        info["gitHashFull"] = result.stdout.strip()

        # Branch name
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        info["gitBranch"] = result.stdout.strip()

        # Check if dirty
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True,
        )
        info["gitDirty"] = bool(result.stdout.strip())

    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    return info


def load_cdk_outputs(
    outputs_path: Path, stack_filter: Optional[str] = None
) -> dict[str, Any]:
    """Load and parse CDK outputs.json file."""
    if not outputs_path.exists():
        return {}

    try:
        with open(outputs_path) as f:
            outputs = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Could not parse CDK outputs: {e}", file=sys.stderr)
        return {}

    # If stack filter specified, only return that stack's outputs
    if stack_filter and stack_filter in outputs:
        return outputs[stack_filter]

    # Otherwise, flatten all stack outputs into a single dict
    flattened = {}
    for stack_name, stack_outputs in outputs.items():
        if isinstance(stack_outputs, dict):
            for key, value in stack_outputs.items():
                flattened[key] = value

    return flattened


def extract_infrastructure_info(cdk_outputs: dict[str, Any]) -> dict[str, Any]:
    """Extract relevant infrastructure ARNs and IDs from CDK outputs."""
    infra = {}

    # Common output key patterns and their normalized names
    key_mappings = {
        # CloudFront
        "cloudfrontdistributionid": "cloudfrontDistributionId",
        "cloudfrontdomain": "cloudfrontDomain",
        "distributionid": "cloudfrontDistributionId",
        "distributiondomain": "cloudfrontDomain",
        "cfndistributionid": "cloudfrontDistributionId",
        # S3
        "bucketname": "s3BucketName",
        "bucketarn": "s3BucketArn",
        "assetsbucket": "s3BucketName",
        "assetsbucketarn": "s3BucketArn",
        "websitebucket": "s3BucketName",
        "websitebucketarn": "s3BucketArn",
        # Cognito
        "userpoolid": "cognitoUserPoolId",
        "userpoolarn": "cognitoUserPoolArn",
        "userpoolclientid": "cognitoUserPoolClientId",
        "identitypoolid": "cognitoIdentityPoolId",
        "cognitouserpoolid": "cognitoUserPoolId",
        "cognitouserpoolarn": "cognitoUserPoolArn",
        "cognitoclientid": "cognitoUserPoolClientId",
        # API
        "apiurl": "apiUrl",
        "apiendpoint": "apiUrl",
        "restapurl": "apiUrl",
        "httpapurl": "apiUrl",
        "websocketurl": "websocketUrl",
        "wssurl": "websocketUrl",
        # Lambda
        "functionarn": "lambdaFunctionArn",
        "lambdaarn": "lambdaFunctionArn",
        # DynamoDB
        "tablearn": "dynamoDbTableArn",
        "tablename": "dynamoDbTableName",
        "dynamodbtablearn": "dynamoDbTableArn",
        "dynamodbtablename": "dynamoDbTableName",
        # SQS
        "queueurl": "sqsQueueUrl",
        "queuearn": "sqsQueueArn",
        # SNS
        "topicarn": "snsTopicArn",
        # AppSync
        "graphqlurl": "graphqlUrl",
        "appsyncurl": "graphqlUrl",
        # EventBridge
        "eventbusarn": "eventBusArn",
        "eventbusname": "eventBusName",
    }

    for key, value in cdk_outputs.items():
        # Normalize key for matching
        normalized_key = key.lower().replace("-", "").replace("_", "")

        # Check if this key matches any known pattern
        if normalized_key in key_mappings:
            infra[key_mappings[normalized_key]] = value
        # Also keep original key if it contains 'arn' or looks like infrastructure
        elif "arn" in normalized_key or "url" in normalized_key:
            infra[key] = value

    return infra


def generate_buildinfo(
    output_path: Path,
    cdk_outputs_path: Optional[Path] = None,
    stack_filter: Optional[str] = None,
    project_id: Optional[str] = None,
    environment: Optional[str] = None,
    release_id: Optional[str] = None,
) -> dict[str, Any]:
    """Generate the complete buildinfo.json structure."""
    git_info = get_git_info()

    buildinfo = {
        "build": {
            "gitHash": git_info["gitHash"],
            "gitHashFull": git_info["gitHashFull"],
            "gitBranch": git_info["gitBranch"],
            "gitDirty": git_info["gitDirty"],
            "buildDate": datetime.now(timezone.utc).isoformat(),
            "projectId": project_id or "unknown",
        },
        "infrastructure": {},
        "deployment": {
            "releaseId": release_id
            or datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"),
            "environment": environment or "unknown",
        },
    }

    # Load CDK outputs if provided
    if cdk_outputs_path:
        cdk_outputs = load_cdk_outputs(cdk_outputs_path, stack_filter)
        buildinfo["infrastructure"] = extract_infrastructure_info(cdk_outputs)

    return buildinfo


def main():
    parser = argparse.ArgumentParser(
        description="Generate buildinfo.json for frontend deployments",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("dist/buildinfo.json"),
        help="Output path for buildinfo.json (default: dist/buildinfo.json)",
    )
    parser.add_argument(
        "--cdk-outputs",
        type=Path,
        help="Path to CDK outputs.json file",
    )
    parser.add_argument(
        "--stack",
        help="Filter to specific CDK stack name",
    )
    parser.add_argument(
        "--project-id",
        help="Project identifier",
    )
    parser.add_argument(
        "--environment",
        "-e",
        help="Deployment environment (dev, staging, prod)",
    )
    parser.add_argument(
        "--release-id",
        help="Release identifier (defaults to timestamp)",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress output",
    )

    args = parser.parse_args()

    # Generate buildinfo
    buildinfo = generate_buildinfo(
        output_path=args.output,
        cdk_outputs_path=args.cdk_outputs,
        stack_filter=args.stack,
        project_id=args.project_id,
        environment=args.environment,
        release_id=args.release_id,
    )

    # Ensure output directory exists
    args.output.parent.mkdir(parents=True, exist_ok=True)

    # Write buildinfo.json
    with open(args.output, "w") as f:
        json.dump(buildinfo, f, indent=2)

    if not args.quiet:
        print(f"Generated {args.output}")
        print(json.dumps(buildinfo, indent=2))


if __name__ == "__main__":
    main()
