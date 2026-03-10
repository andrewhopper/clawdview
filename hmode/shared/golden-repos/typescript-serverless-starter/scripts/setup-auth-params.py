#!/usr/bin/env python3
"""
Setup SSM Parameters for Shared Auth Configuration

This script creates the SSM parameters for the shared auth.b.lfg.new
Cognito user pool. Run this once to bootstrap the parameters.

Usage:
    python scripts/setup-auth-params.py [--profile PROFILE] [--region REGION]

Parameters created:
    /shared/auth/user-pool-id
    /shared/auth/user-pool-arn
    /shared/auth/domain
"""

import argparse
import boto3
import json
import sys
from typing import Any


# Default auth.b.lfg.new configuration
DEFAULT_AUTH_CONFIG = {
    "user-pool-id": "us-east-1_p0fQSZLEG",
    "user-pool-arn": "arn:aws:cognito-idp:us-east-1:507745175693:userpool/us-east-1_p0fQSZLEG",
    "domain": "auth.b.lfg.new",
}

SSM_PREFIX = "/shared/auth"


def get_ssm_client(profile: str | None, region: str) -> Any:
    """Get SSM client with optional profile."""
    session_kwargs = {"region_name": region}
    if profile:
        session_kwargs["profile_name"] = profile

    session = boto3.Session(**session_kwargs)
    return session.client("ssm")


def put_parameter(ssm: Any, name: str, value: str, description: str) -> bool:
    """Create or update an SSM parameter."""
    try:
        ssm.put_parameter(
            Name=name,
            Value=value,
            Type="String",
            Description=description,
            Overwrite=True,
            Tags=[
                {"Key": "Project", "Value": "shared-auth"},
                {"Key": "ManagedBy", "Value": "serverless-starter"},
            ],
        )
        print(f"  ✓ {name}")
        return True
    except Exception as e:
        print(f"  ✗ {name}: {e}")
        return False


def get_parameter(ssm: Any, name: str) -> str | None:
    """Get an SSM parameter value."""
    try:
        response = ssm.get_parameter(Name=name)
        return response["Parameter"]["Value"]
    except ssm.exceptions.ParameterNotFound:
        return None
    except Exception as e:
        print(f"Error getting {name}: {e}")
        return None


def setup_parameters(ssm: Any, config: dict[str, str]) -> bool:
    """Create all SSM parameters."""
    print("\nCreating SSM parameters...")

    success = True
    for key, value in config.items():
        name = f"{SSM_PREFIX}/{key}"
        description = f"Shared auth configuration: {key}"
        if not put_parameter(ssm, name, value, description):
            success = False

    return success


def verify_parameters(ssm: Any) -> bool:
    """Verify all parameters exist and show their values."""
    print("\nVerifying SSM parameters...")

    all_exist = True
    for key in DEFAULT_AUTH_CONFIG.keys():
        name = f"{SSM_PREFIX}/{key}"
        value = get_parameter(ssm, name)
        if value:
            # Mask sensitive parts
            display_value = value
            if len(value) > 20:
                display_value = f"{value[:10]}...{value[-5:]}"
            print(f"  ✓ {name} = {display_value}")
        else:
            print(f"  ✗ {name} (not found)")
            all_exist = False

    return all_exist


def main():
    parser = argparse.ArgumentParser(
        description="Setup SSM parameters for shared auth configuration"
    )
    parser.add_argument(
        "--profile",
        help="AWS profile to use",
        default=None,
    )
    parser.add_argument(
        "--region",
        help="AWS region",
        default="us-east-1",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Only verify parameters exist, don't create",
    )
    parser.add_argument(
        "--user-pool-id",
        help="Override user pool ID",
        default=DEFAULT_AUTH_CONFIG["user-pool-id"],
    )
    parser.add_argument(
        "--user-pool-arn",
        help="Override user pool ARN",
    )
    parser.add_argument(
        "--domain",
        help="Override Cognito domain",
        default=DEFAULT_AUTH_CONFIG["domain"],
    )

    args = parser.parse_args()

    # Build config
    config = {
        "user-pool-id": args.user_pool_id,
        "user-pool-arn": args.user_pool_arn or f"arn:aws:cognito-idp:{args.region}:*:userpool/{args.user_pool_id}",
        "domain": args.domain,
    }

    # Use default ARN if using default pool ID
    if args.user_pool_id == DEFAULT_AUTH_CONFIG["user-pool-id"] and not args.user_pool_arn:
        config["user-pool-arn"] = DEFAULT_AUTH_CONFIG["user-pool-arn"]

    print(f"AWS Region: {args.region}")
    if args.profile:
        print(f"AWS Profile: {args.profile}")
    print(f"SSM Prefix: {SSM_PREFIX}")

    ssm = get_ssm_client(args.profile, args.region)

    if args.verify_only:
        if verify_parameters(ssm):
            print("\n✓ All parameters exist")
            sys.exit(0)
        else:
            print("\n✗ Some parameters missing")
            sys.exit(1)

    # Create parameters
    print("\nConfiguration:")
    for key, value in config.items():
        print(f"  {key}: {value}")

    if setup_parameters(ssm, config):
        print("\n✓ All parameters created successfully")
        verify_parameters(ssm)
        sys.exit(0)
    else:
        print("\n✗ Some parameters failed to create")
        sys.exit(1)


if __name__ == "__main__":
    main()
