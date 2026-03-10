#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
# File UUID: 7c4e8f2a-9b1d-4e6c-a3f5-8d2c1e0b9a7f
"""
URL Health Check Tool

Checks if a URL returns HTTP 200 and validates response body
doesn't contain error patterns.

Usage:
    check_url.py <url> [options]
    check_url.py http://localhost:3456/ --forbidden "error,failed,404"
    check_url.py http://localhost:5173/ --required "Portfolio"
    check_url.py http://localhost:3456/ --json

Options:
    --forbidden, -f    Comma-separated patterns that should NOT appear (case-insensitive)
    --required, -r     Comma-separated patterns that MUST appear (case-insensitive)
    --timeout, -t      Request timeout in seconds (default: 5)
    --status, -s       Expected HTTP status code (default: 200)
    --json, -j         Output results as JSON
    --verbose, -v      Show response details

Exit Codes:
    0 - Health check passed
    1 - Health check failed
    2 - Connection error or timeout
"""

import sys
import json
import argparse
import urllib.request
import urllib.error
from typing import List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


# Default patterns that indicate errors in web apps
DEFAULT_FORBIDDEN_PATTERNS = [
    # General errors
    "error",
    "failed",
    "exception",
    # HTTP errors
    "404",
    "500",
    "502",
    "503",
    # Vite/build errors
    "plugin:vite",
    "Cannot find module",
    "Module not found",
    "Require stack",
    "fix the code to dismiss",
    "hmr.overlay",
    # React errors
    "Uncaught Error",
    "React error",
    "Minified React error",
    # JS errors
    "SyntaxError",
    "TypeError",
    "ReferenceError",
    "undefined is not",
    "is not defined",
    "is not a function",
    # Build tool errors
    "postcss",
    "webpack",
    "esbuild",
    "rollup",
    # Stack traces
    "at Function",
    "at Module",
    "at Object",
    "node_modules",
]


@dataclass
class HealthCheckResult:
    """Result of a URL health check"""
    url: str
    healthy: bool
    status_code: Optional[int]
    message: str
    timestamp: str
    details: dict

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)


def check_url(
    url: str,
    forbidden_patterns: List[str] = None,
    required_patterns: List[str] = None,
    expected_status: int = 200,
    timeout: int = 5
) -> HealthCheckResult:
    """
    Check URL health with content validation.

    Args:
        url: URL to check
        forbidden_patterns: Patterns that should NOT appear in response
        required_patterns: Patterns that MUST appear in response
        expected_status: Expected HTTP status code
        timeout: Request timeout in seconds

    Returns:
        HealthCheckResult with check details
    """
    forbidden_patterns = forbidden_patterns or []
    required_patterns = required_patterns or []

    result = HealthCheckResult(
        url=url,
        healthy=False,
        status_code=None,
        message="",
        timestamp=datetime.now().isoformat(),
        details={}
    )

    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "OverwatchHealthCheck/1.0"}
        )

        with urllib.request.urlopen(req, timeout=timeout) as response:
            result.status_code = response.getcode()
            result.details["content_type"] = response.headers.get("Content-Type", "unknown")
            result.details["content_length"] = response.headers.get("Content-Length", "unknown")

            # Check status code
            if result.status_code != expected_status:
                result.message = f"HTTP {result.status_code} (expected {expected_status})"
                return result

            # Read body for pattern checks
            body = ""
            if forbidden_patterns or required_patterns:
                body = response.read().decode("utf-8", errors="ignore")
                body_lower = body.lower()
                result.details["body_length"] = len(body)

                # Check forbidden patterns
                for pattern in forbidden_patterns:
                    if pattern.lower() in body_lower:
                        result.message = f"Found forbidden pattern: '{pattern}'"
                        result.details["found_forbidden"] = pattern
                        return result

                # Check required patterns
                for pattern in required_patterns:
                    if pattern.lower() not in body_lower:
                        result.message = f"Missing required pattern: '{pattern}'"
                        result.details["missing_required"] = pattern
                        return result

            # All checks passed
            result.healthy = True
            result.message = f"HTTP {result.status_code} OK"

            if forbidden_patterns:
                result.details["forbidden_checked"] = len(forbidden_patterns)
            if required_patterns:
                result.details["required_checked"] = len(required_patterns)

    except urllib.error.HTTPError as e:
        result.status_code = e.code
        result.message = f"HTTP {e.code}: {e.reason}"

    except urllib.error.URLError as e:
        result.message = f"Connection failed: {e.reason}"

    except TimeoutError:
        result.message = f"Timeout after {timeout}s"

    except Exception as e:
        result.message = f"Error: {str(e)}"

    return result


def main():
    parser = argparse.ArgumentParser(
        description="URL health check with content validation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s http://localhost:3456/
  %(prog)s http://localhost:5173/ --forbidden "error,failed"
  %(prog)s http://api.example.com/health --required "status.*ok"
  %(prog)s http://localhost:3456/ --json
        """
    )

    parser.add_argument("url", help="URL to check")
    parser.add_argument(
        "--forbidden", "-f",
        help="Comma-separated forbidden patterns (case-insensitive)"
    )
    parser.add_argument(
        "--strict", "-S",
        action="store_true",
        help="Use default forbidden patterns (errors, build failures, stack traces)"
    )
    parser.add_argument(
        "--required", "-r",
        help="Comma-separated required patterns (case-insensitive)"
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=5,
        help="Timeout in seconds (default: 5)"
    )
    parser.add_argument(
        "--status", "-s",
        type=int,
        default=200,
        help="Expected HTTP status (default: 200)"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output as JSON"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show response details"
    )

    args = parser.parse_args()

    # Parse patterns
    forbidden = [p.strip() for p in args.forbidden.split(",")] if args.forbidden else []
    required = [p.strip() for p in args.required.split(",")] if args.required else []

    # Add default patterns if --strict
    if args.strict:
        forbidden = list(set(forbidden + DEFAULT_FORBIDDEN_PATTERNS))

    # Run check
    result = check_url(
        url=args.url,
        forbidden_patterns=forbidden,
        required_patterns=required,
        expected_status=args.status,
        timeout=args.timeout
    )

    # Output
    if args.json:
        print(result.to_json())
    else:
        if result.healthy:
            print(f"✅ {result.url}")
            print(f"   {result.message}")
        else:
            print(f"❌ {result.url}")
            print(f"   {result.message}")

        if args.verbose and result.details:
            print(f"   Details: {json.dumps(result.details)}")

    # Exit code
    if result.healthy:
        sys.exit(0)
    elif result.status_code is None:
        sys.exit(2)  # Connection error
    else:
        sys.exit(1)  # Check failed


if __name__ == "__main__":
    main()
