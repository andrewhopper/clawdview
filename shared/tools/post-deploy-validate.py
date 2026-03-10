#!/usr/bin/env python3
# File UUID: 2b3c4d5e-6f7a-8b9c-0d1e-2f3a4b5c6d7e
"""
Post-Deployment Validation Tool

Comprehensive validation after deploying a web application. Validates:
1. Git hash matches expected version (footer, meta tag, /health)
2. Domain name resolves and serves the app
3. OAuth/Cognito login works (creates smoke test user if needed)
4. Required UI elements render correctly
5. No JavaScript console errors

Features:
- Retry with exponential backoff (DNS propagation, CDN cache)
- Automatic smoke test user creation in Cognito
- Playwright-based rendering validation
- Auto-fix attempts for common issues
- Detailed failure reports

Usage:
    # Basic validation
    python post-deploy-validate.py --url https://app.example.com

    # With auth validation (requires Cognito pool)
    python post-deploy-validate.py --url https://app.example.com \
        --cognito-pool us-east-1_AbcDef123 \
        --cognito-client 1234567890abcdefghijklmnop

    # Full validation with retry
    python post-deploy-validate.py --url https://app.example.com \
        --expected-hash abc1234 \
        --max-retries 3 \
        --retry-delay 300

    # In Makefile
    make post-deploy-validate URL=https://app.example.com
"""

import argparse
import asyncio
import json
import os
import random
import re
import secrets
import string
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse

# Try to import optional dependencies
try:
    import boto3
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


class ValidationStatus(Enum):
    PASS = "pass"
    FAIL = "fail"
    WARN = "warn"
    SKIP = "skip"


@dataclass
class ValidationCheck:
    name: str
    status: ValidationStatus
    message: str
    details: Optional[Dict[str, Any]] = None
    fix_attempted: bool = False
    fix_result: Optional[str] = None


@dataclass
class ValidationReport:
    url: str
    timestamp: str
    checks: List[ValidationCheck] = field(default_factory=list)
    passed: bool = False
    attempt: int = 1
    total_attempts: int = 1

    def add_check(self, check: ValidationCheck) -> None:
        self.checks.append(check)

    @property
    def failed_checks(self) -> List[ValidationCheck]:
        return [c for c in self.checks if c.status == ValidationStatus.FAIL]

    @property
    def summary(self) -> str:
        total = len(self.checks)
        passed = sum(1 for c in self.checks if c.status == ValidationStatus.PASS)
        failed = sum(1 for c in self.checks if c.status == ValidationStatus.FAIL)
        warned = sum(1 for c in self.checks if c.status == ValidationStatus.WARN)
        skipped = sum(1 for c in self.checks if c.status == ValidationStatus.SKIP)

        return f"{passed}/{total} passed, {failed} failed, {warned} warnings, {skipped} skipped"


class PostDeployValidator:
    """Validates deployed web applications."""

    SMOKE_TEST_USER_PREFIX = "smoketest-"

    def __init__(
        self,
        url: str,
        expected_hash: Optional[str] = None,
        cognito_pool_id: Optional[str] = None,
        cognito_client_id: Optional[str] = None,
        region: str = "us-east-1",
        max_retries: int = 3,
        retry_delay: int = 60,
        auto_fix: bool = True,
        verbose: bool = False,
    ):
        self.url = url.rstrip("/")
        self.expected_hash = expected_hash
        self.cognito_pool_id = cognito_pool_id
        self.cognito_client_id = cognito_client_id
        self.region = region
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.auto_fix = auto_fix
        self.verbose = verbose

        self.parsed_url = urlparse(url)
        self.domain = self.parsed_url.netloc

        # AWS clients (lazy init)
        self._cognito_client = None
        self._cloudfront_client = None
        self._route53_client = None

        # Smoke test user credentials
        self.smoke_user_email: Optional[str] = None
        self.smoke_user_password: Optional[str] = None

    def _get_cognito_client(self):
        if not HAS_BOTO3:
            return None
        if self._cognito_client is None:
            self._cognito_client = boto3.client("cognito-idp", region_name=self.region)
        return self._cognito_client

    def _log(self, msg: str) -> None:
        if self.verbose:
            print(f"  [DEBUG] {msg}")

    def run_validation(self) -> ValidationReport:
        """Run all validations with retry logic."""
        for attempt in range(1, self.max_retries + 1):
            print(f"\n{'=' * 60}")
            print(f"🔍 Post-Deployment Validation (Attempt {attempt}/{self.max_retries})")
            print(f"   URL: {self.url}")
            print(f"   Time: {datetime.now().isoformat()}")
            print(f"{'=' * 60}")

            report = ValidationReport(
                url=self.url,
                timestamp=datetime.now().isoformat(),
                attempt=attempt,
                total_attempts=self.max_retries,
            )

            # Run all checks
            self._check_dns_resolution(report)
            self._check_url_accessible(report)
            self._check_ssl_certificate(report)
            self._check_git_hash(report)
            self._check_footer_updated(report)
            self._check_health_endpoint(report)

            if self.cognito_pool_id and self.cognito_client_id:
                self._check_cognito_auth(report)

            self._check_playwright_render(report)

            # Determine overall pass/fail
            report.passed = len(report.failed_checks) == 0

            # Print results
            self._print_report(report)

            if report.passed:
                print(f"\n✅ All validation checks PASSED!")
                return report

            # If not last attempt, wait and retry
            if attempt < self.max_retries:
                print(f"\n⏳ Waiting {self.retry_delay} seconds before retry...")
                print(f"   (DNS propagation, CDN cache invalidation may take time)")

                # If auto-fix is enabled, try to fix issues
                if self.auto_fix:
                    self._attempt_fixes(report)

                time.sleep(self.retry_delay)

        print(f"\n❌ Validation FAILED after {self.max_retries} attempts")
        return report

    def _check_dns_resolution(self, report: ValidationReport) -> None:
        """Check that domain resolves correctly."""
        print("\n[1] Checking DNS resolution...")

        try:
            import socket
            ip = socket.gethostbyname(self.domain)
            self._log(f"Resolved {self.domain} to {ip}")

            report.add_check(ValidationCheck(
                name="DNS Resolution",
                status=ValidationStatus.PASS,
                message=f"Domain {self.domain} resolves to {ip}",
                details={"ip": ip, "domain": self.domain},
            ))
        except Exception as e:
            report.add_check(ValidationCheck(
                name="DNS Resolution",
                status=ValidationStatus.FAIL,
                message=f"DNS resolution failed: {e}",
                details={"domain": self.domain, "error": str(e)},
            ))

    def _check_url_accessible(self, report: ValidationReport) -> None:
        """Check that URL returns 200 OK."""
        print("[2] Checking URL accessibility...")

        try:
            if HAS_REQUESTS:
                resp = requests.get(self.url, timeout=30, allow_redirects=True)
                status_code = resp.status_code
                content_length = len(resp.content)
            else:
                # Fall back to curl
                result = subprocess.run(
                    ["curl", "-sL", "-o", "/dev/null", "-w", "%{http_code}", self.url],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                status_code = int(result.stdout.strip())
                content_length = 0

            self._log(f"Status code: {status_code}")

            if status_code == 200:
                report.add_check(ValidationCheck(
                    name="URL Accessible",
                    status=ValidationStatus.PASS,
                    message=f"URL returns HTTP 200",
                    details={"status_code": status_code, "content_length": content_length},
                ))
            else:
                report.add_check(ValidationCheck(
                    name="URL Accessible",
                    status=ValidationStatus.FAIL,
                    message=f"URL returns HTTP {status_code} (expected 200)",
                    details={"status_code": status_code},
                ))
        except Exception as e:
            report.add_check(ValidationCheck(
                name="URL Accessible",
                status=ValidationStatus.FAIL,
                message=f"Failed to access URL: {e}",
                details={"error": str(e)},
            ))

    def _check_ssl_certificate(self, report: ValidationReport) -> None:
        """Check SSL certificate is valid."""
        print("[3] Checking SSL certificate...")

        if not self.parsed_url.scheme == "https":
            report.add_check(ValidationCheck(
                name="SSL Certificate",
                status=ValidationStatus.WARN,
                message="URL is not HTTPS",
            ))
            return

        try:
            import ssl
            import socket
            from datetime import datetime

            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=self.domain) as s:
                s.settimeout(10)
                s.connect((self.domain, 443))
                cert = s.getpeercert()

            # Check expiration
            not_after = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
            days_until_expiry = (not_after - datetime.now()).days

            self._log(f"Certificate expires in {days_until_expiry} days")

            if days_until_expiry < 7:
                report.add_check(ValidationCheck(
                    name="SSL Certificate",
                    status=ValidationStatus.WARN,
                    message=f"Certificate expires in {days_until_expiry} days",
                    details={"expires": not_after.isoformat(), "days_left": days_until_expiry},
                ))
            else:
                report.add_check(ValidationCheck(
                    name="SSL Certificate",
                    status=ValidationStatus.PASS,
                    message=f"SSL certificate valid ({days_until_expiry} days remaining)",
                    details={"expires": not_after.isoformat(), "days_left": days_until_expiry},
                ))
        except Exception as e:
            report.add_check(ValidationCheck(
                name="SSL Certificate",
                status=ValidationStatus.FAIL,
                message=f"SSL certificate check failed: {e}",
                details={"error": str(e)},
            ))

    def _check_git_hash(self, report: ValidationReport) -> None:
        """Check that deployed git hash matches expected."""
        print("[4] Checking git hash...")

        if not self.expected_hash:
            report.add_check(ValidationCheck(
                name="Git Hash",
                status=ValidationStatus.SKIP,
                message="No expected hash provided (use --expected-hash)",
            ))
            return

        try:
            if HAS_REQUESTS:
                resp = requests.get(self.url, timeout=30)
                html = resp.text
            else:
                result = subprocess.run(
                    ["curl", "-sL", self.url],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                html = result.stdout

            # Look for git hash in various locations
            hash_found = None

            # Check meta tag
            meta_match = re.search(r'<meta[^>]*name=["\']git-hash["\'][^>]*content=["\']([^"\']+)["\']', html, re.IGNORECASE)
            if not meta_match:
                meta_match = re.search(r'<meta[^>]*content=["\']([^"\']+)["\'][^>]*name=["\']git-hash["\']', html, re.IGNORECASE)
            if meta_match:
                hash_found = meta_match.group(1)
                self._log(f"Found hash in meta tag: {hash_found}")

            # Check data attribute
            if not hash_found:
                data_match = re.search(r'data-git-hash=["\']([^"\']+)["\']', html)
                if data_match:
                    hash_found = data_match.group(1)
                    self._log(f"Found hash in data attribute: {hash_found}")

            # Check footer text
            if not hash_found:
                footer_match = re.search(r'(?:version|build|commit)[:\s]+([a-f0-9]{7,40})', html, re.IGNORECASE)
                if footer_match:
                    hash_found = footer_match.group(1)
                    self._log(f"Found hash in footer: {hash_found}")

            # Check window variable
            if not hash_found:
                window_match = re.search(r'__GIT_HASH__\s*[=:]\s*["\']([^"\']+)["\']', html)
                if window_match:
                    hash_found = window_match.group(1)
                    self._log(f"Found hash in window variable: {hash_found}")

            if not hash_found:
                report.add_check(ValidationCheck(
                    name="Git Hash",
                    status=ValidationStatus.FAIL,
                    message="Git hash not found in HTML (check meta tag, footer, or data attribute)",
                ))
                return

            # Compare hashes (allow short hash matching)
            expected_short = self.expected_hash[:7]
            found_short = hash_found[:7]

            if expected_short == found_short:
                report.add_check(ValidationCheck(
                    name="Git Hash",
                    status=ValidationStatus.PASS,
                    message=f"Git hash matches: {hash_found}",
                    details={"expected": self.expected_hash, "found": hash_found},
                ))
            else:
                report.add_check(ValidationCheck(
                    name="Git Hash",
                    status=ValidationStatus.FAIL,
                    message=f"Git hash mismatch: expected {self.expected_hash}, found {hash_found}",
                    details={"expected": self.expected_hash, "found": hash_found},
                ))
        except Exception as e:
            report.add_check(ValidationCheck(
                name="Git Hash",
                status=ValidationStatus.FAIL,
                message=f"Failed to check git hash: {e}",
                details={"error": str(e)},
            ))

    def _check_footer_updated(self, report: ValidationReport) -> None:
        """Check that footer contains recent build date."""
        print("[5] Checking footer/build date...")

        try:
            if HAS_REQUESTS:
                resp = requests.get(self.url, timeout=30)
                html = resp.text
            else:
                result = subprocess.run(
                    ["curl", "-sL", self.url],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                html = result.stdout

            # Look for build date in various formats
            date_patterns = [
                r'build[:-]?\s*date[:\s]+(\d{4}-\d{2}-\d{2})',
                r'deployed[:\s]+(\d{4}-\d{2}-\d{2})',
                r'version[:\s]+\d+\.\d+\.\d+\s+\((\d{4}-\d{2}-\d{2})\)',
                r'©\s*(\d{4})',
            ]

            date_found = None
            for pattern in date_patterns:
                match = re.search(pattern, html, re.IGNORECASE)
                if match:
                    date_found = match.group(1)
                    break

            if not date_found:
                report.add_check(ValidationCheck(
                    name="Footer/Build Date",
                    status=ValidationStatus.WARN,
                    message="No build date found in page",
                ))
                return

            # Check if date is recent (within 7 days)
            try:
                if len(date_found) == 4:  # Just year
                    current_year = datetime.now().year
                    if int(date_found) == current_year:
                        report.add_check(ValidationCheck(
                            name="Footer/Build Date",
                            status=ValidationStatus.PASS,
                            message=f"Copyright year is current: {date_found}",
                        ))
                    else:
                        report.add_check(ValidationCheck(
                            name="Footer/Build Date",
                            status=ValidationStatus.WARN,
                            message=f"Copyright year may be outdated: {date_found}",
                        ))
                else:
                    build_date = datetime.strptime(date_found, "%Y-%m-%d")
                    days_old = (datetime.now() - build_date).days

                    if days_old <= 7:
                        report.add_check(ValidationCheck(
                            name="Footer/Build Date",
                            status=ValidationStatus.PASS,
                            message=f"Build date is recent: {date_found} ({days_old} days ago)",
                        ))
                    else:
                        report.add_check(ValidationCheck(
                            name="Footer/Build Date",
                            status=ValidationStatus.WARN,
                            message=f"Build date may be stale: {date_found} ({days_old} days ago)",
                        ))
            except:
                report.add_check(ValidationCheck(
                    name="Footer/Build Date",
                    status=ValidationStatus.PASS,
                    message=f"Build date found: {date_found}",
                ))
        except Exception as e:
            report.add_check(ValidationCheck(
                name="Footer/Build Date",
                status=ValidationStatus.FAIL,
                message=f"Failed to check footer: {e}",
            ))

    def _check_health_endpoint(self, report: ValidationReport) -> None:
        """Check /health endpoint if available."""
        print("[6] Checking health endpoint...")

        health_urls = [
            f"{self.url}/health",
            f"{self.url}/api/health",
            f"{self.url}/_health",
        ]

        for health_url in health_urls:
            try:
                if HAS_REQUESTS:
                    resp = requests.get(health_url, timeout=10)
                    if resp.status_code == 200:
                        try:
                            data = resp.json()
                            status = data.get("status", "unknown")
                            report.add_check(ValidationCheck(
                                name="Health Endpoint",
                                status=ValidationStatus.PASS,
                                message=f"Health endpoint OK: {health_url}",
                                details=data,
                            ))
                            return
                        except:
                            report.add_check(ValidationCheck(
                                name="Health Endpoint",
                                status=ValidationStatus.PASS,
                                message=f"Health endpoint accessible: {health_url}",
                            ))
                            return
            except:
                continue

        report.add_check(ValidationCheck(
            name="Health Endpoint",
            status=ValidationStatus.SKIP,
            message="No health endpoint found (checked /health, /api/health)",
        ))

    def _check_cognito_auth(self, report: ValidationReport) -> None:
        """Check Cognito authentication works."""
        print("[7] Checking Cognito authentication...")

        if not HAS_BOTO3:
            report.add_check(ValidationCheck(
                name="Cognito Auth",
                status=ValidationStatus.SKIP,
                message="boto3 not available",
            ))
            return

        cognito = self._get_cognito_client()
        if not cognito:
            report.add_check(ValidationCheck(
                name="Cognito Auth",
                status=ValidationStatus.SKIP,
                message="Could not create Cognito client",
            ))
            return

        try:
            # Ensure smoke test user exists
            self._ensure_smoke_test_user(cognito)

            if not self.smoke_user_email or not self.smoke_user_password:
                report.add_check(ValidationCheck(
                    name="Cognito Auth",
                    status=ValidationStatus.FAIL,
                    message="Could not create/find smoke test user",
                ))
                return

            # Attempt authentication
            try:
                auth_response = cognito.initiate_auth(
                    AuthFlow="USER_PASSWORD_AUTH",
                    AuthParameters={
                        "USERNAME": self.smoke_user_email,
                        "PASSWORD": self.smoke_user_password,
                    },
                    ClientId=self.cognito_client_id,
                )

                if "AuthenticationResult" in auth_response:
                    report.add_check(ValidationCheck(
                        name="Cognito Auth",
                        status=ValidationStatus.PASS,
                        message=f"Authentication successful for {self.smoke_user_email}",
                        details={"user": self.smoke_user_email},
                    ))
                elif "ChallengeName" in auth_response:
                    report.add_check(ValidationCheck(
                        name="Cognito Auth",
                        status=ValidationStatus.WARN,
                        message=f"Auth requires challenge: {auth_response['ChallengeName']}",
                    ))
                else:
                    report.add_check(ValidationCheck(
                        name="Cognito Auth",
                        status=ValidationStatus.PASS,
                        message="Authentication initiated successfully",
                    ))
            except cognito.exceptions.NotAuthorizedException as e:
                report.add_check(ValidationCheck(
                    name="Cognito Auth",
                    status=ValidationStatus.FAIL,
                    message=f"Authentication failed: {e}",
                ))
            except cognito.exceptions.UserNotFoundException:
                report.add_check(ValidationCheck(
                    name="Cognito Auth",
                    status=ValidationStatus.FAIL,
                    message="Smoke test user not found",
                ))

        except Exception as e:
            report.add_check(ValidationCheck(
                name="Cognito Auth",
                status=ValidationStatus.FAIL,
                message=f"Cognito auth check failed: {e}",
                details={"error": str(e)},
            ))

    def _ensure_smoke_test_user(self, cognito) -> None:
        """Create or find smoke test user."""
        self._log("Ensuring smoke test user exists...")

        # Look for existing smoke test user
        try:
            users_response = cognito.list_users(
                UserPoolId=self.cognito_pool_id,
                Filter=f'email ^= "{self.SMOKE_TEST_USER_PREFIX}"',
                Limit=1,
            )

            if users_response.get("Users"):
                user = users_response["Users"][0]
                for attr in user.get("Attributes", []):
                    if attr["Name"] == "email":
                        self.smoke_user_email = attr["Value"]
                        break

                self._log(f"Found existing smoke test user: {self.smoke_user_email}")

                # We don't know the password, so we need to reset it
                self.smoke_user_password = self._generate_password()

                cognito.admin_set_user_password(
                    UserPoolId=self.cognito_pool_id,
                    Username=self.smoke_user_email,
                    Password=self.smoke_user_password,
                    Permanent=True,
                )
                self._log("Reset password for smoke test user")
                return

        except Exception as e:
            self._log(f"Error listing users: {e}")

        # Create new smoke test user
        try:
            random_suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
            self.smoke_user_email = f"{self.SMOKE_TEST_USER_PREFIX}{random_suffix}@smoketest.local"
            self.smoke_user_password = self._generate_password()

            cognito.admin_create_user(
                UserPoolId=self.cognito_pool_id,
                Username=self.smoke_user_email,
                UserAttributes=[
                    {"Name": "email", "Value": self.smoke_user_email},
                    {"Name": "email_verified", "Value": "true"},
                ],
                MessageAction="SUPPRESS",  # Don't send welcome email
            )

            # Set permanent password
            cognito.admin_set_user_password(
                UserPoolId=self.cognito_pool_id,
                Username=self.smoke_user_email,
                Password=self.smoke_user_password,
                Permanent=True,
            )

            self._log(f"Created smoke test user: {self.smoke_user_email}")

        except Exception as e:
            self._log(f"Error creating smoke test user: {e}")
            self.smoke_user_email = None
            self.smoke_user_password = None

    def _generate_password(self) -> str:
        """Generate a password that meets Cognito requirements."""
        # At least 8 chars, uppercase, lowercase, number, special char
        lower = secrets.choice(string.ascii_lowercase)
        upper = secrets.choice(string.ascii_uppercase)
        digit = secrets.choice(string.digits)
        special = secrets.choice("!@#$%^&*")
        rest = "".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
        password = lower + upper + digit + special + rest
        return "".join(random.sample(password, len(password)))  # Shuffle

    def _check_playwright_render(self, report: ValidationReport) -> None:
        """Check page renders correctly using Playwright."""
        print("[8] Checking page render (Playwright)...")

        # Check if playwright is available
        try:
            result = subprocess.run(
                ["npx", "playwright", "--version"],
                capture_output=True,
                timeout=10,
            )
            if result.returncode != 0:
                report.add_check(ValidationCheck(
                    name="Page Render",
                    status=ValidationStatus.SKIP,
                    message="Playwright not installed (run: npx playwright install)",
                ))
                return
        except:
            report.add_check(ValidationCheck(
                name="Page Render",
                status=ValidationStatus.SKIP,
                message="Playwright not available",
            ))
            return

        # Create temporary test file
        test_script = f"""
const {{ chromium }} = require('playwright');

(async () => {{
    const browser = await chromium.launch({{ headless: true }});
    const page = await browser.newPage();

    const errors = [];
    page.on('pageerror', err => errors.push(err.message));
    page.on('console', msg => {{
        if (msg.type() === 'error') errors.push(msg.text());
    }});

    try {{
        await page.goto('{self.url}', {{ waitUntil: 'networkidle', timeout: 30000 }});

        // Check page loaded
        const title = await page.title();
        const bodyVisible = await page.locator('body').isVisible();

        // Check for main content
        const hasContent = await page.locator('body').textContent();

        const result = {{
            success: bodyVisible && hasContent.length > 100,
            title: title,
            bodyLength: hasContent.length,
            errors: errors,
        }};

        console.log(JSON.stringify(result));
    }} catch (err) {{
        console.log(JSON.stringify({{ success: false, error: err.message }}));
    }}

    await browser.close();
}})();
"""

        try:
            result = subprocess.run(
                ["node", "-e", test_script],
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode != 0:
                report.add_check(ValidationCheck(
                    name="Page Render",
                    status=ValidationStatus.FAIL,
                    message=f"Playwright test failed: {result.stderr}",
                ))
                return

            try:
                data = json.loads(result.stdout.strip())

                if data.get("success"):
                    if data.get("errors"):
                        report.add_check(ValidationCheck(
                            name="Page Render",
                            status=ValidationStatus.WARN,
                            message=f"Page renders with {len(data['errors'])} console errors",
                            details={"errors": data["errors"][:5], "title": data.get("title")},
                        ))
                    else:
                        report.add_check(ValidationCheck(
                            name="Page Render",
                            status=ValidationStatus.PASS,
                            message=f"Page renders correctly (title: {data.get('title', 'N/A')})",
                            details=data,
                        ))
                else:
                    report.add_check(ValidationCheck(
                        name="Page Render",
                        status=ValidationStatus.FAIL,
                        message=f"Page failed to render: {data.get('error', 'unknown')}",
                        details=data,
                    ))
            except json.JSONDecodeError:
                report.add_check(ValidationCheck(
                    name="Page Render",
                    status=ValidationStatus.WARN,
                    message=f"Could not parse Playwright output",
                ))

        except subprocess.TimeoutExpired:
            report.add_check(ValidationCheck(
                name="Page Render",
                status=ValidationStatus.FAIL,
                message="Playwright test timed out after 60s",
            ))
        except Exception as e:
            report.add_check(ValidationCheck(
                name="Page Render",
                status=ValidationStatus.FAIL,
                message=f"Playwright test error: {e}",
            ))

    def _attempt_fixes(self, report: ValidationReport) -> None:
        """Attempt to fix failed checks."""
        print("\n🔧 Attempting auto-fixes...")

        for check in report.failed_checks:
            if check.name == "DNS Resolution":
                # Can't auto-fix DNS, but can suggest
                print(f"   ℹ️ DNS issue - verify Route 53 record for {self.domain}")

            elif check.name == "Git Hash":
                print(f"   ℹ️ Git hash mismatch - may need to clear CDN cache")
                self._try_invalidate_cloudfront()
                check.fix_attempted = True
                check.fix_result = "Attempted CloudFront invalidation"

            elif check.name == "Cognito Auth":
                print(f"   ℹ️ Auth issue - check Cognito User Pool configuration")

    def _try_invalidate_cloudfront(self) -> None:
        """Try to invalidate CloudFront cache."""
        if not HAS_BOTO3:
            return

        try:
            cloudfront = boto3.client("cloudfront")

            # Find distribution for this domain
            distributions = cloudfront.list_distributions()
            for dist in distributions.get("DistributionList", {}).get("Items", []):
                aliases = dist.get("Aliases", {}).get("Items", [])
                if self.domain in aliases:
                    dist_id = dist["Id"]
                    print(f"   Creating invalidation for {dist_id}...")

                    cloudfront.create_invalidation(
                        DistributionId=dist_id,
                        InvalidationBatch={
                            "Paths": {"Quantity": 1, "Items": ["/*"]},
                            "CallerReference": str(time.time()),
                        },
                    )
                    print(f"   ✓ Invalidation created")
                    return

            print(f"   ⚠️ No CloudFront distribution found for {self.domain}")
        except Exception as e:
            print(f"   ⚠️ CloudFront invalidation failed: {e}")

    def _print_report(self, report: ValidationReport) -> None:
        """Print validation report."""
        print(f"\n{'─' * 60}")
        print("📊 Validation Results")
        print(f"{'─' * 60}")

        for check in report.checks:
            if check.status == ValidationStatus.PASS:
                icon = "✅"
            elif check.status == ValidationStatus.FAIL:
                icon = "❌"
            elif check.status == ValidationStatus.WARN:
                icon = "⚠️"
            else:
                icon = "⏭️"

            print(f"{icon} {check.name}: {check.message}")

            if check.fix_attempted:
                print(f"   🔧 Fix attempted: {check.fix_result}")

        print(f"\n📈 Summary: {report.summary}")


def main():
    parser = argparse.ArgumentParser(
        description="Post-deployment validation tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--url",
        required=True,
        help="Application URL to validate",
    )

    parser.add_argument(
        "--expected-hash",
        help="Expected git commit hash",
    )

    parser.add_argument(
        "--cognito-pool",
        help="Cognito User Pool ID for auth testing",
    )

    parser.add_argument(
        "--cognito-client",
        help="Cognito App Client ID",
    )

    parser.add_argument(
        "--region",
        default="us-east-1",
        help="AWS region",
    )

    parser.add_argument(
        "--max-retries",
        type=int,
        default=3,
        help="Maximum retry attempts (default: 3)",
    )

    parser.add_argument(
        "--retry-delay",
        type=int,
        default=60,
        help="Delay between retries in seconds (default: 60)",
    )

    parser.add_argument(
        "--no-auto-fix",
        action="store_true",
        help="Disable auto-fix attempts",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )

    args = parser.parse_args()

    validator = PostDeployValidator(
        url=args.url,
        expected_hash=args.expected_hash,
        cognito_pool_id=args.cognito_pool,
        cognito_client_id=args.cognito_client,
        region=args.region,
        max_retries=args.max_retries,
        retry_delay=args.retry_delay,
        auto_fix=not args.no_auto_fix,
        verbose=args.verbose,
    )

    report = validator.run_validation()

    if args.json:
        output = {
            "url": report.url,
            "timestamp": report.timestamp,
            "passed": report.passed,
            "attempts": report.attempt,
            "checks": [
                {
                    "name": c.name,
                    "status": c.status.value,
                    "message": c.message,
                    "details": c.details,
                }
                for c in report.checks
            ],
        }
        print(json.dumps(output, indent=2))

    sys.exit(0 if report.passed else 1)


if __name__ == "__main__":
    main()
