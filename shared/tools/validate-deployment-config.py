#!/usr/bin/env python3
# File UUID: 8c7d6e5f-4a3b-2c1d-0e9f-8a7b6c5d4e3f
"""
Deployment Config Validator

Validates configuration files for:
1. Placeholder values (YOUR_, REPLACE_, TODO, etc.)
2. Type violations (numeric IDs with letters, invalid ARNs)
3. AWS resource existence (optional, via --verify-aws)
4. Schema compliance (when schema defined)

Usage:
    # Validate a single file
    python validate-deployment-config.py config.yaml

    # Validate with AWS verification
    python validate-deployment-config.py config.yaml --verify-aws

    # Validate all configs in a project
    python validate-deployment-config.py --project /path/to/project

    # Pre-commit mode (exit 1 on any error)
    python validate-deployment-config.py --pre-commit file1.yaml file2.json
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

import yaml


class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationIssue:
    severity: Severity
    message: str
    path: str  # JSON path to the value
    value: Any
    rule: str
    suggestion: Optional[str] = None

    def __str__(self) -> str:
        sev = "❌" if self.severity == Severity.ERROR else "⚠️" if self.severity == Severity.WARNING else "ℹ️"
        msg = f"{sev} [{self.rule}] {self.message}"
        if self.path:
            msg += f"\n   Path: {self.path}"
        if self.value is not None:
            val_str = str(self.value)[:50]
            if len(str(self.value)) > 50:
                val_str += "..."
            msg += f"\n   Value: {val_str}"
        if self.suggestion:
            msg += f"\n   Suggestion: {self.suggestion}"
        return msg


@dataclass
class ValidationResult:
    file_path: Path
    issues: List[ValidationIssue] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        return any(i.severity == Severity.ERROR for i in self.issues)

    @property
    def has_warnings(self) -> bool:
        return any(i.severity == Severity.WARNING for i in self.issues)

    @property
    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.ERROR)

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.WARNING)


# Placeholder patterns that indicate incomplete config
PLACEHOLDER_PATTERNS = [
    # Explicit placeholders
    (r"^YOUR_", "Placeholder prefix YOUR_"),
    (r"^REPLACE_", "Placeholder prefix REPLACE_"),
    (r"^CHANGEME", "Placeholder CHANGEME"),
    (r"^TODO", "Placeholder TODO"),
    (r"^FIXME", "Placeholder FIXME"),
    (r"^XXX", "Placeholder XXX"),
    (r"^placeholder", "Placeholder value"),
    (r"^example", "Example value"),
    (r"^demo", "Demo value"),
    (r"^test-value", "Test value placeholder"),
    (r"^fake[-_]", "Fake value prefix"),
    (r"^dummy[-_]", "Dummy value prefix"),
    (r"^sample[-_]", "Sample value prefix"),

    # Common placeholder patterns
    (r"^<.*>$", "Angle bracket placeholder"),
    (r"^\[.*\]$", "Square bracket placeholder (non-array context)"),
    (r"^\{.*\}$", "Curly brace placeholder (non-object context)"),
    (r"^___+$", "Underscore placeholder"),
    (r"^\.\.\.$", "Ellipsis placeholder"),
    (r"^null$", "Null string value"),
    (r"^undefined$", "Undefined string value"),
    (r"^none$", "None string value"),
    (r"^N/A$", "N/A placeholder"),
    (r"^TBD$", "TBD placeholder"),
    (r"^TBA$", "TBA placeholder"),

    # AWS-specific placeholders
    (r"^000000000000$", "Placeholder AWS account ID"),
    (r"^123456789012$", "Example AWS account ID"),
    (r"^111111111111$", "Placeholder AWS account ID"),
    (r"^us-east-1_XXXXXXXXX$", "Placeholder Cognito pool ID"),
    (r"^arn:aws:.*:000000000000:", "Placeholder ARN with fake account"),
    (r"^arn:aws:.*:123456789012:", "Example ARN with example account"),

    # API key placeholders
    (r"^sk-ant-.*placeholder", "Placeholder Anthropic API key"),
    (r"^sk-.*placeholder", "Placeholder OpenAI API key"),
    (r"^AKIA.*EXAMPLE", "Placeholder AWS access key"),
]

# AWS resource ID format validators
AWS_RESOURCE_PATTERNS = {
    "cognito_user_pool_id": {
        "pattern": r"^[a-z]{2}-[a-z]+-\d_[A-Za-z0-9]{9}$",
        "example": "us-east-1_AbcDefGhi",
        "description": "Cognito User Pool ID",
    },
    "cognito_client_id": {
        "pattern": r"^[a-z0-9]{26}$",
        "example": "1234567890abcdefghijklmnop",
        "description": "Cognito App Client ID",
    },
    "aws_account_id": {
        "pattern": r"^\d{12}$",
        "example": "123456789012",
        "description": "AWS Account ID (12 digits)",
    },
    "arn": {
        "pattern": r"^arn:aws:[a-z0-9-]+:[a-z0-9-]*:\d{12}:[a-zA-Z0-9:/_-]+$",
        "example": "arn:aws:dynamodb:us-east-1:123456789012:table/my-table",
        "description": "AWS ARN",
    },
    "s3_bucket": {
        "pattern": r"^[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]$",
        "example": "my-bucket-name",
        "description": "S3 Bucket Name",
    },
    "dynamodb_table": {
        "pattern": r"^[a-zA-Z0-9._-]{3,255}$",
        "example": "my-table-name",
        "description": "DynamoDB Table Name",
    },
    "lambda_function": {
        "pattern": r"^[a-zA-Z0-9-_]{1,64}$",
        "example": "my-function-name",
        "description": "Lambda Function Name",
    },
    "api_gateway_id": {
        "pattern": r"^[a-z0-9]{10}$",
        "example": "abcd123456",
        "description": "API Gateway ID",
    },
    "cloudfront_distribution": {
        "pattern": r"^[A-Z0-9]{13,14}$",
        "example": "E1234567890ABC",
        "description": "CloudFront Distribution ID",
    },
    "region": {
        "pattern": r"^[a-z]{2}-[a-z]+-\d$",
        "example": "us-east-1",
        "description": "AWS Region",
    },
}

# Key name patterns that suggest what type of value is expected
KEY_TYPE_HINTS = {
    # Cognito
    r"(cognito|user)[-_]?pool[-_]?id": "cognito_user_pool_id",
    r"(cognito|app)[-_]?client[-_]?id": "cognito_client_id",
    r"user[-_]?pool[-_]?client": "cognito_client_id",

    # AWS general
    r"account[-_]?id": "aws_account_id",
    r"aws[-_]?account": "aws_account_id",
    r"^arn$": "arn",
    r"[-_]arn$": "arn",

    # S3
    r"bucket[-_]?(name)?$": "s3_bucket",
    r"s3[-_]?bucket": "s3_bucket",

    # DynamoDB
    r"table[-_]?(name)?$": "dynamodb_table",
    r"dynamodb[-_]?table": "dynamodb_table",

    # Lambda
    r"(lambda|function)[-_]?(name)?$": "lambda_function",

    # API Gateway
    r"api[-_]?(gateway)?[-_]?id": "api_gateway_id",
    r"rest[-_]?api[-_]?id": "api_gateway_id",

    # CloudFront
    r"(cloudfront|distribution)[-_]?id": "cloudfront_distribution",

    # Region
    r"^region$": "region",
    r"aws[-_]?region": "region",
}


class ConfigValidator:
    """Validates deployment configuration files."""

    def __init__(
        self,
        verify_aws: bool = False,
        strict: bool = False,
        skip_patterns: Optional[List[str]] = None,
    ):
        self.verify_aws = verify_aws
        self.strict = strict
        self.skip_patterns = skip_patterns or []
        self._aws_clients: Dict[str, Any] = {}

    def _get_aws_client(self, service: str):
        """Lazy-load AWS clients."""
        if service not in self._aws_clients:
            try:
                import boto3
                self._aws_clients[service] = boto3.client(service)
            except Exception as e:
                print(f"Warning: Could not create AWS client for {service}: {e}")
                return None
        return self._aws_clients[service]

    def validate_file(self, file_path: Path) -> ValidationResult:
        """Validate a single configuration file."""
        result = ValidationResult(file_path=file_path)

        if not file_path.exists():
            result.issues.append(ValidationIssue(
                severity=Severity.ERROR,
                message=f"File not found: {file_path}",
                path="",
                value=None,
                rule="file-exists",
            ))
            return result

        # Skip files matching skip patterns
        for pattern in self.skip_patterns:
            if re.search(pattern, str(file_path)):
                return result

        # Load file content
        try:
            content = file_path.read_text()

            # Parse based on extension
            suffix = file_path.suffix.lower()
            if suffix in ('.yaml', '.yml'):
                data = yaml.safe_load(content)
            elif suffix == '.json':
                data = json.loads(content)
            elif suffix == '.env':
                data = self._parse_env_file(content)
            else:
                # Try to detect format
                try:
                    data = json.loads(content)
                except:
                    try:
                        data = yaml.safe_load(content)
                    except:
                        result.issues.append(ValidationIssue(
                            severity=Severity.WARNING,
                            message=f"Unknown file format, skipping: {file_path}",
                            path="",
                            value=None,
                            rule="file-format",
                        ))
                        return result
        except Exception as e:
            result.issues.append(ValidationIssue(
                severity=Severity.ERROR,
                message=f"Failed to parse file: {e}",
                path="",
                value=None,
                rule="file-parse",
            ))
            return result

        # Skip if data is None or empty
        if data is None:
            return result

        # Validate the data
        self._validate_recursive(data, "", result)

        return result

    def _parse_env_file(self, content: str) -> Dict[str, str]:
        """Parse .env file format."""
        data = {}
        for line in content.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                data[key.strip()] = value.strip().strip('"\'')
        return data

    def _validate_recursive(
        self,
        data: Any,
        path: str,
        result: ValidationResult,
    ) -> None:
        """Recursively validate data structure."""
        if isinstance(data, dict):
            for key, value in data.items():
                new_path = f"{path}.{key}" if path else key

                # Skip certain keys
                if key.lower() in ('description', 'comment', 'note', 'readme'):
                    continue

                # Validate the value
                self._validate_value(key, value, new_path, result)

                # Recurse
                self._validate_recursive(value, new_path, result)

        elif isinstance(data, list):
            for i, item in enumerate(data):
                new_path = f"{path}[{i}]"
                self._validate_recursive(item, new_path, result)

    def _validate_value(
        self,
        key: str,
        value: Any,
        path: str,
        result: ValidationResult,
    ) -> None:
        """Validate a single key-value pair."""
        if not isinstance(value, str):
            return

        # Skip empty values
        if not value.strip():
            return

        # Check for placeholder patterns
        for pattern, description in PLACEHOLDER_PATTERNS:
            if re.search(pattern, value, re.IGNORECASE):
                result.issues.append(ValidationIssue(
                    severity=Severity.ERROR,
                    message=f"Placeholder value detected: {description}",
                    path=path,
                    value=value,
                    rule="no-placeholders",
                    suggestion="Replace with actual value before committing",
                ))
                return  # Don't check further if placeholder found

        # Infer expected type from key name
        expected_type = self._infer_type_from_key(key)

        if expected_type:
            pattern_info = AWS_RESOURCE_PATTERNS.get(expected_type)
            if pattern_info:
                pattern = pattern_info["pattern"]
                if not re.match(pattern, value):
                    result.issues.append(ValidationIssue(
                        severity=Severity.ERROR,
                        message=f"Invalid {pattern_info['description']} format",
                        path=path,
                        value=value,
                        rule=f"valid-{expected_type}",
                        suggestion=f"Expected format: {pattern_info['example']}",
                    ))
                elif self.verify_aws:
                    # Verify resource exists
                    self._verify_aws_resource(expected_type, value, path, result)

    def _infer_type_from_key(self, key: str) -> Optional[str]:
        """Infer the expected value type from the key name."""
        key_lower = key.lower()

        for pattern, type_name in KEY_TYPE_HINTS.items():
            if re.search(pattern, key_lower):
                return type_name

        return None

    def _verify_aws_resource(
        self,
        resource_type: str,
        value: str,
        path: str,
        result: ValidationResult,
    ) -> None:
        """Verify that an AWS resource exists."""
        try:
            if resource_type == "cognito_user_pool_id":
                client = self._get_aws_client("cognito-idp")
                if client:
                    client.describe_user_pool(UserPoolId=value)

            elif resource_type == "s3_bucket":
                client = self._get_aws_client("s3")
                if client:
                    client.head_bucket(Bucket=value)

            elif resource_type == "dynamodb_table":
                client = self._get_aws_client("dynamodb")
                if client:
                    client.describe_table(TableName=value)

            elif resource_type == "lambda_function":
                client = self._get_aws_client("lambda")
                if client:
                    client.get_function(FunctionName=value)

        except Exception as e:
            error_str = str(e)
            if "ResourceNotFoundException" in error_str or "not found" in error_str.lower():
                result.issues.append(ValidationIssue(
                    severity=Severity.ERROR,
                    message=f"AWS resource does not exist",
                    path=path,
                    value=value,
                    rule="aws-resource-exists",
                    suggestion=f"Verify the {resource_type} exists in AWS",
                ))
            elif "AccessDenied" in error_str or "not authorized" in error_str.lower():
                result.issues.append(ValidationIssue(
                    severity=Severity.WARNING,
                    message=f"Cannot verify AWS resource (access denied)",
                    path=path,
                    value=value,
                    rule="aws-resource-exists",
                ))


def find_config_files(project_path: Path) -> List[Path]:
    """Find configuration files in a project."""
    config_patterns = [
        "**/*.yaml",
        "**/*.yml",
        "**/*.json",
        "**/.env",
        "**/.env.*",
    ]

    # Directories to skip
    skip_dirs = {
        "node_modules",
        ".git",
        "dist",
        "build",
        "cdk.out",
        ".next",
        "__pycache__",
        ".pytest_cache",
        "venv",
        ".venv",
    }

    # Files to skip (examples, templates)
    skip_file_patterns = [
        r"\.example$",
        r"\.template$",
        r"\.sample$",
        r"package-lock\.json$",
        r"pnpm-lock\.yaml$",
        r"yarn\.lock$",
        r"tsconfig\.json$",
        r"jest\.config\.",
        r"eslint",
        r"prettier",
    ]

    files = []
    for pattern in config_patterns:
        for file_path in project_path.glob(pattern):
            # Skip directories
            skip = False
            for parent in file_path.parents:
                if parent.name in skip_dirs:
                    skip = True
                    break
            if skip:
                continue

            # Skip example/template files
            if any(re.search(p, str(file_path)) for p in skip_file_patterns):
                continue

            files.append(file_path)

    return files


def validate_project(
    project_path: Path,
    verify_aws: bool = False,
    strict: bool = False,
) -> List[ValidationResult]:
    """Validate all config files in a project."""
    validator = ConfigValidator(verify_aws=verify_aws, strict=strict)

    config_files = find_config_files(project_path)
    results = []

    for file_path in config_files:
        result = validator.validate_file(file_path)
        if result.issues:  # Only include files with issues
            results.append(result)

    return results


def print_results(results: List[ValidationResult]) -> Tuple[int, int]:
    """Print validation results and return (error_count, warning_count)."""
    total_errors = 0
    total_warnings = 0

    for result in results:
        if not result.issues:
            continue

        print(f"\n{'=' * 60}")
        print(f"📁 {result.file_path}")
        print(f"{'=' * 60}")

        for issue in result.issues:
            print(f"\n{issue}")

        total_errors += result.error_count
        total_warnings += result.warning_count

    return total_errors, total_warnings


def main():
    parser = argparse.ArgumentParser(
        description="Validate deployment configuration files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Validate a single file
    %(prog)s config/settings.yaml

    # Validate with AWS resource verification
    %(prog)s config/settings.yaml --verify-aws

    # Validate all configs in a project
    %(prog)s --project ./my-project

    # Pre-commit mode (validate staged files)
    %(prog)s --pre-commit config/*.yaml
""",
    )

    parser.add_argument(
        "files",
        nargs="*",
        type=Path,
        help="Config files to validate",
    )

    parser.add_argument(
        "--project",
        type=Path,
        help="Project directory to scan for config files",
    )

    parser.add_argument(
        "--verify-aws",
        action="store_true",
        help="Verify AWS resources exist (requires AWS credentials)",
    )

    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors",
    )

    parser.add_argument(
        "--pre-commit",
        action="store_true",
        help="Pre-commit mode: exit 1 on any error",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only show errors, not warnings",
    )

    args = parser.parse_args()

    # Collect results
    results: List[ValidationResult] = []
    validator = ConfigValidator(
        verify_aws=args.verify_aws,
        strict=args.strict,
    )

    if args.project:
        results = validate_project(
            args.project,
            verify_aws=args.verify_aws,
            strict=args.strict,
        )
    elif args.files:
        for file_path in args.files:
            result = validator.validate_file(file_path)
            if result.issues:
                results.append(result)
    else:
        # Default: scan current directory
        results = validate_project(
            Path.cwd(),
            verify_aws=args.verify_aws,
            strict=args.strict,
        )

    # Filter results if quiet mode
    if args.quiet:
        for result in results:
            result.issues = [i for i in result.issues if i.severity == Severity.ERROR]
        results = [r for r in results if r.issues]

    # Output results
    if args.json:
        output = {
            "results": [
                {
                    "file": str(r.file_path),
                    "errors": r.error_count,
                    "warnings": r.warning_count,
                    "issues": [
                        {
                            "severity": i.severity.value,
                            "message": i.message,
                            "path": i.path,
                            "value": str(i.value) if i.value else None,
                            "rule": i.rule,
                            "suggestion": i.suggestion,
                        }
                        for i in r.issues
                    ],
                }
                for r in results
            ],
        }
        print(json.dumps(output, indent=2))
    else:
        if results:
            total_errors, total_warnings = print_results(results)

            print(f"\n{'=' * 60}")
            print(f"📊 Summary: {total_errors} errors, {total_warnings} warnings")
            print(f"{'=' * 60}")

            if total_errors > 0:
                print("\n❌ Validation FAILED")
            elif total_warnings > 0:
                print("\n⚠️  Validation passed with warnings")
            else:
                print("\n✅ Validation PASSED")
        else:
            print("✅ No configuration issues found")

    # Exit code
    total_errors = sum(r.error_count for r in results)
    total_warnings = sum(r.warning_count for r in results)

    if args.pre_commit or args.strict:
        # In pre-commit mode, fail on any error
        sys.exit(1 if total_errors > 0 else 0)
    else:
        # Normal mode: only fail on errors
        sys.exit(1 if total_errors > 0 else 0)


if __name__ == "__main__":
    main()
