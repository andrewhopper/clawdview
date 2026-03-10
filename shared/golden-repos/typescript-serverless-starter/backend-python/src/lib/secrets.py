"""Secrets Manager utilities with caching."""

import json
from functools import lru_cache
from typing import Any

import boto3
from aws_lambda_powertools import Logger
from aws_xray_sdk.core import patch_all

patch_all()

logger = Logger(service="secrets-manager")

# Cache for secrets (cleared on cold start)
_secrets_cache: dict[str, dict[str, Any]] = {}


@lru_cache(maxsize=10)
def get_secrets_client():
    """Get cached Secrets Manager client."""
    return boto3.client("secretsmanager")


def get_secret(secret_arn: str, force_refresh: bool = False) -> dict[str, Any]:
    """
    Retrieve secret from AWS Secrets Manager.

    Uses in-memory caching to reduce API calls during Lambda execution.

    Args:
        secret_arn: The ARN or name of the secret
        force_refresh: If True, bypass cache and fetch fresh secret

    Returns:
        Dictionary containing the secret values

    Raises:
        ValueError: If secret_arn is empty
        ClientError: If secret cannot be retrieved
    """
    if not secret_arn:
        raise ValueError("secret_arn cannot be empty")

    # Check cache first
    if not force_refresh and secret_arn in _secrets_cache:
        logger.debug("Returning cached secret", extra={"secret_arn": secret_arn})
        return _secrets_cache[secret_arn]

    logger.info("Fetching secret from Secrets Manager", extra={"secret_arn": secret_arn})

    client = get_secrets_client()

    response = client.get_secret_value(SecretId=secret_arn)

    # Parse the secret string
    secret_string = response.get("SecretString", "{}")
    secret_data = json.loads(secret_string)

    # Cache the result
    _secrets_cache[secret_arn] = secret_data

    return secret_data


def clear_cache():
    """Clear the secrets cache. Useful for testing."""
    _secrets_cache.clear()
    get_secrets_client.cache_clear()


def get_api_key(secret_arn: str, key_name: str = "api_key") -> str:
    """
    Convenience function to get a specific API key from a secret.

    Args:
        secret_arn: The ARN or name of the secret
        key_name: The key name within the secret (default: "api_key")

    Returns:
        The API key string

    Raises:
        KeyError: If the key_name is not found in the secret
    """
    secret = get_secret(secret_arn)

    if key_name not in secret:
        raise KeyError(f"Key '{key_name}' not found in secret")

    return secret[key_name]
