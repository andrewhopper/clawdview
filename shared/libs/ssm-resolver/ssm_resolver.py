#!/usr/bin/env python3
# File UUID: 7c3e9b2f-1a4d-4e8f-9c2a-5d6e7f8a9b0c

"""
SSM Parameter Store Hierarchical Resolver (Python)

Provides automatic fallback chain for SSM parameters:
1. Project-specific: /{account}/{env}/{project}/{category}/{key}
2. Environment-shared: /{account}/{env}/{category}/{key}
3. Account-shared: /{account}/{category}/{key}
4. Global-shared: /shared/{category}/{key}

Usage:
    from ssm_resolver import SSMResolver

    resolver = SSMResolver(
        account_type='work',
        environment='dev',
        project='gocoder'
    )

    # Resolve with fallback
    client_id = resolver.resolve('auth', 'google-client-id')

    # Write parameter
    resolver.write('auth', 'cognito-client-id', 'us-east-1_ABC123')
"""

import boto3
from typing import Literal, Optional
from dataclasses import dataclass

AccountType = Literal['work', 'personal', 'shared']
Environment = Literal['dev', 'prod', 'beta', 'staging']
ParameterScope = Literal['project', 'environment', 'account', 'shared']


@dataclass
class SSMResolverConfig:
    """Configuration for SSM resolver"""
    account_type: AccountType
    environment: Environment
    project: str
    region: str = 'us-east-1'


class SSMResolver:
    """
    SSM Parameter Resolver with Hierarchical Fallback

    Automatically resolves parameters using fallback chain from most specific
    to most general scope.
    """

    def __init__(
        self,
        account_type: AccountType,
        environment: Environment,
        project: str,
        region: str = 'us-east-1',
        debug: bool = False
    ):
        self.config = SSMResolverConfig(
            account_type=account_type,
            environment=environment,
            project=project,
            region=region
        )
        self.client = boto3.client('ssm', region_name=region)
        self.debug = debug
        self._cache: dict[str, str] = {}

    def resolve(
        self,
        category: str,
        key: str,
        required: bool = False,
        use_cache: bool = True
    ) -> Optional[str]:
        """
        Resolve parameter with automatic fallback chain

        Args:
            category: Category path (e.g., 'auth', 'auth/cognito')
            key: Parameter key (e.g., 'client-id')
            required: Raise exception if not found
            use_cache: Use cached value if available

        Returns:
            Parameter value or None if not found

        Raises:
            ValueError: If required=True and parameter not found
        """
        cache_key = f"{category}/{key}"

        if use_cache and cache_key in self._cache:
            if self.debug:
                print(f"[SSMResolver] Cache hit: {cache_key}")
            return self._cache[cache_key]

        paths = self._build_fallback_chain(category, key)

        if self.debug:
            print(f"[SSMResolver] Resolving {category}/{key}")
            print(f"[SSMResolver] Fallback chain:")
            for p in paths:
                print(f"  - {p}")

        for path in paths:
            try:
                response = self.client.get_parameter(Name=path, WithDecryption=True)
                value = response['Parameter']['Value']

                if self.debug:
                    print(f"[SSMResolver] Found at: {path}")

                self._cache[cache_key] = value
                return value

            except self.client.exceptions.ParameterNotFound:
                if self.debug:
                    print(f"[SSMResolver] Not found at: {path}")
                continue
            except Exception as e:
                if self.debug:
                    print(f"[SSMResolver] Error at {path}: {e}")
                continue

        if required:
            raise ValueError(
                f"Required SSM parameter not found: {category}/{key}\n"
                f"Tried paths:\n" + "\n".join(f"  - {p}" for p in paths)
            )

        if self.debug:
            print(f"[SSMResolver] Not found in any fallback path (returning None)")

        return None

    def write(
        self,
        category: str,
        key: str,
        value: str,
        scope: ParameterScope = 'project',
        secure: bool = False,
        description: Optional[str] = None,
        overwrite: bool = True
    ) -> None:
        """
        Write parameter to SSM

        Args:
            category: Category path
            key: Parameter key
            value: Parameter value
            scope: Parameter scope (where to write)
            secure: Use SecureString type
            description: Custom description
            overwrite: Overwrite if exists
        """
        path = self.path(category, key, scope)

        if description is None:
            description = self._generate_description(category, key, scope)

        param_type = 'SecureString' if secure else 'String'

        try:
            self.client.put_parameter(
                Name=path,
                Value=value,
                Type=param_type,
                Description=description,
                Overwrite=overwrite
            )

            if self.debug:
                print(f"[SSMResolver] Wrote {param_type}: {path}")

            # Update cache
            cache_key = f"{category}/{key}"
            self._cache[cache_key] = value

        except Exception as e:
            raise ValueError(f"Failed to write parameter {path}: {e}")

    def path(
        self,
        category: str,
        key: str,
        scope: ParameterScope = 'project'
    ) -> str:
        """
        Generate SSM parameter path for given scope

        Args:
            category: Category path (e.g., 'auth', 'auth/cognito')
            key: Parameter key
            scope: Parameter scope

        Returns:
            Full SSM parameter path
        """
        full_key = f"{category}/{key}"

        if scope == 'project':
            return f"/{self.config.account_type}/{self.config.environment}/{self.config.project}/{full_key}"
        elif scope == 'environment':
            return f"/{self.config.account_type}/{self.config.environment}/{full_key}"
        elif scope == 'account':
            return f"/{self.config.account_type}/{full_key}"
        elif scope == 'shared':
            return f"/shared/{full_key}"
        else:
            raise ValueError(f"Invalid scope: {scope}")

    def _build_fallback_chain(self, category: str, key: str) -> list[str]:
        """Build fallback path chain (most specific to most general)"""
        return [
            self.path(category, key, 'project'),
            self.path(category, key, 'environment'),
            self.path(category, key, 'account'),
            self.path(category, key, 'shared'),
        ]

    def _generate_description(
        self,
        category: str,
        key: str,
        scope: ParameterScope
    ) -> str:
        """Generate description for parameter"""
        return (
            f"[{self.config.account_type}/{self.config.environment}/"
            f"{self.config.project}] {category}/{key} ({scope})"
        )

    def clear_cache(self) -> None:
        """Clear parameter cache"""
        self._cache.clear()


# Convenience functions

def create_resolver(
    account_type: AccountType,
    environment: Environment,
    project: str,
    region: str = 'us-east-1',
    debug: bool = False
) -> SSMResolver:
    """Create SSM resolver"""
    return SSMResolver(
        account_type=account_type,
        environment=environment,
        project=project,
        region=region,
        debug=debug
    )


if __name__ == '__main__':
    # Example usage
    import sys

    if len(sys.argv) < 5:
        print("Usage: ssm_resolver.py <account> <env> <project> <category> <key>")
        print("Example: ssm_resolver.py work dev gocoder auth google-client-id")
        sys.exit(1)

    account = sys.argv[1]
    env = sys.argv[2]
    project = sys.argv[3]
    category = sys.argv[4]
    key = sys.argv[5]

    resolver = SSMResolver(
        account_type=account,  # type: ignore
        environment=env,  # type: ignore
        project=project,
        debug=True
    )

    value = resolver.resolve(category, key)
    if value:
        print(f"\nResolved value: {value}")
    else:
        print(f"\nParameter not found")
        sys.exit(1)
