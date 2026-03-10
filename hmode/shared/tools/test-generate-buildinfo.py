#!/usr/bin/env python3
# File UUID: 7d2e8f3a-4b5c-6d7e-8f9a-0b1c2d3e4f5a
"""
Tests for generate-buildinfo.py

Run with: pytest shared/tools/test_generate_buildinfo.py -v
"""

import json
import subprocess
import tempfile
from pathlib import Path

import pytest

SCRIPT_PATH = Path(__file__).parent / "generate-buildinfo.py"


class TestGenerateBuildinfo:
    """Test the generate-buildinfo.py script."""

    def test_script_exists(self):
        """Verify the script exists."""
        assert SCRIPT_PATH.exists(), f"Script not found at {SCRIPT_PATH}"

    def test_basic_generation(self, tmp_path):
        """Test basic buildinfo generation without CDK outputs."""
        output_file = tmp_path / "buildinfo.json"

        result = subprocess.run(
            [
                "python3",
                str(SCRIPT_PATH),
                "--output",
                str(output_file),
                "--project-id",
                "test-project-123",
                "--environment",
                "test",
                "--quiet",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"Script failed: {result.stderr}"
        assert output_file.exists(), "Output file was not created"

        with open(output_file) as f:
            buildinfo = json.load(f)

        # Verify structure
        assert "build" in buildinfo
        assert "infrastructure" in buildinfo
        assert "deployment" in buildinfo

        # Verify build section
        assert buildinfo["build"]["projectId"] == "test-project-123"
        assert "gitHash" in buildinfo["build"]
        assert "gitBranch" in buildinfo["build"]
        assert "buildDate" in buildinfo["build"]

        # Verify deployment section
        assert buildinfo["deployment"]["environment"] == "test"
        assert "releaseId" in buildinfo["deployment"]

    def test_with_cdk_outputs(self, tmp_path):
        """Test buildinfo generation with CDK outputs."""
        # Create mock CDK outputs
        cdk_outputs = {
            "MyStack": {
                "CloudFrontDistributionId": "E2ABCD123",
                "CloudFrontDomain": "d123.cloudfront.net",
                "BucketName": "my-bucket-123",
                "BucketArn": "arn:aws:s3:::my-bucket-123",
                "UserPoolId": "us-east-1_abc123",
                "UserPoolArn": "arn:aws:cognito-idp:us-east-1:123456:userpool/us-east-1_abc123",
                "ApiUrl": "https://api.example.com",
            }
        }

        cdk_outputs_file = tmp_path / "outputs.json"
        with open(cdk_outputs_file, "w") as f:
            json.dump(cdk_outputs, f)

        output_file = tmp_path / "buildinfo.json"

        result = subprocess.run(
            [
                "python3",
                str(SCRIPT_PATH),
                "--output",
                str(output_file),
                "--cdk-outputs",
                str(cdk_outputs_file),
                "--project-id",
                "test-with-infra",
                "--environment",
                "prod",
                "--quiet",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"Script failed: {result.stderr}"

        with open(output_file) as f:
            buildinfo = json.load(f)

        # Verify infrastructure ARNs were extracted
        infra = buildinfo["infrastructure"]
        assert infra.get("cloudfrontDistributionId") == "E2ABCD123"
        assert infra.get("cloudfrontDomain") == "d123.cloudfront.net"
        assert infra.get("s3BucketName") == "my-bucket-123"
        assert infra.get("s3BucketArn") == "arn:aws:s3:::my-bucket-123"
        assert infra.get("cognitoUserPoolId") == "us-east-1_abc123"
        assert infra.get("apiUrl") == "https://api.example.com"

    def test_with_stack_filter(self, tmp_path):
        """Test filtering to specific CDK stack."""
        cdk_outputs = {
            "FrontendStack": {
                "BucketName": "frontend-bucket",
            },
            "BackendStack": {
                "ApiUrl": "https://backend.example.com",
            },
        }

        cdk_outputs_file = tmp_path / "outputs.json"
        with open(cdk_outputs_file, "w") as f:
            json.dump(cdk_outputs, f)

        output_file = tmp_path / "buildinfo.json"

        result = subprocess.run(
            [
                "python3",
                str(SCRIPT_PATH),
                "--output",
                str(output_file),
                "--cdk-outputs",
                str(cdk_outputs_file),
                "--stack",
                "FrontendStack",
                "--quiet",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0

        with open(output_file) as f:
            buildinfo = json.load(f)

        # Should only have frontend stack outputs
        infra = buildinfo["infrastructure"]
        assert infra.get("s3BucketName") == "frontend-bucket"
        assert "apiUrl" not in infra

    def test_missing_cdk_outputs_file(self, tmp_path):
        """Test graceful handling of missing CDK outputs file."""
        output_file = tmp_path / "buildinfo.json"
        missing_file = tmp_path / "nonexistent.json"

        result = subprocess.run(
            [
                "python3",
                str(SCRIPT_PATH),
                "--output",
                str(output_file),
                "--cdk-outputs",
                str(missing_file),
                "--quiet",
            ],
            capture_output=True,
            text=True,
        )

        # Should succeed but with empty infrastructure
        assert result.returncode == 0
        assert output_file.exists()

        with open(output_file) as f:
            buildinfo = json.load(f)

        assert buildinfo["infrastructure"] == {}

    def test_creates_parent_directories(self, tmp_path):
        """Test that parent directories are created if needed."""
        output_file = tmp_path / "nested" / "path" / "buildinfo.json"

        result = subprocess.run(
            [
                "python3",
                str(SCRIPT_PATH),
                "--output",
                str(output_file),
                "--quiet",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert output_file.exists()

    def test_git_info_captured(self, tmp_path):
        """Test that git info is captured when in a git repo."""
        output_file = tmp_path / "buildinfo.json"

        result = subprocess.run(
            [
                "python3",
                str(SCRIPT_PATH),
                "--output",
                str(output_file),
                "--quiet",
            ],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,  # Run from repo root
        )

        assert result.returncode == 0

        with open(output_file) as f:
            buildinfo = json.load(f)

        # In a git repo, should have real git info
        build = buildinfo["build"]
        assert build["gitHash"] != "unknown"
        assert build["gitBranch"] != "unknown"
        assert 7 <= len(build["gitHash"]) <= 12  # Short hash (7-12 chars)

    def test_build_date_is_iso_format(self, tmp_path):
        """Test that buildDate is in ISO format."""
        output_file = tmp_path / "buildinfo.json"

        subprocess.run(
            [
                "python3",
                str(SCRIPT_PATH),
                "--output",
                str(output_file),
                "--quiet",
            ],
            capture_output=True,
            text=True,
        )

        with open(output_file) as f:
            buildinfo = json.load(f)

        from datetime import datetime

        # Should parse as ISO format
        build_date = buildinfo["build"]["buildDate"]
        datetime.fromisoformat(build_date.replace("Z", "+00:00"))

    def test_custom_release_id(self, tmp_path):
        """Test custom release ID."""
        output_file = tmp_path / "buildinfo.json"

        subprocess.run(
            [
                "python3",
                str(SCRIPT_PATH),
                "--output",
                str(output_file),
                "--release-id",
                "v1.2.3-custom",
                "--quiet",
            ],
            capture_output=True,
            text=True,
        )

        with open(output_file) as f:
            buildinfo = json.load(f)

        assert buildinfo["deployment"]["releaseId"] == "v1.2.3-custom"


class TestKeyMappings:
    """Test CDK output key normalization."""

    def test_cloudfront_variations(self, tmp_path):
        """Test various CloudFront key patterns are normalized."""
        test_cases = [
            {"CloudFrontDistributionId": "E123"},
            {"DistributionId": "E123"},
            {"CFNDistributionId": "E123"},
        ]

        for outputs in test_cases:
            cdk_file = tmp_path / "outputs.json"
            with open(cdk_file, "w") as f:
                json.dump({"Stack": outputs}, f)

            output_file = tmp_path / "buildinfo.json"
            subprocess.run(
                [
                    "python3",
                    str(SCRIPT_PATH),
                    "--output",
                    str(output_file),
                    "--cdk-outputs",
                    str(cdk_file),
                    "--quiet",
                ],
            )

            with open(output_file) as f:
                buildinfo = json.load(f)

            assert (
                buildinfo["infrastructure"].get("cloudfrontDistributionId") == "E123"
            ), f"Failed for {outputs}"

    def test_s3_variations(self, tmp_path):
        """Test various S3 key patterns are normalized."""
        test_cases = [
            {"BucketName": "my-bucket"},
            {"AssetsBucket": "my-bucket"},
            {"WebsiteBucket": "my-bucket"},
        ]

        for outputs in test_cases:
            cdk_file = tmp_path / "outputs.json"
            with open(cdk_file, "w") as f:
                json.dump({"Stack": outputs}, f)

            output_file = tmp_path / "buildinfo.json"
            subprocess.run(
                [
                    "python3",
                    str(SCRIPT_PATH),
                    "--output",
                    str(output_file),
                    "--cdk-outputs",
                    str(cdk_file),
                    "--quiet",
                ],
            )

            with open(output_file) as f:
                buildinfo = json.load(f)

            assert (
                buildinfo["infrastructure"].get("s3BucketName") == "my-bucket"
            ), f"Failed for {outputs}"

    def test_cognito_variations(self, tmp_path):
        """Test various Cognito key patterns are normalized."""
        cdk_outputs = {
            "Stack": {
                "UserPoolId": "us-east-1_abc",
                "UserPoolClientId": "client123",
                "IdentityPoolId": "us-east-1:identity",
            }
        }

        cdk_file = tmp_path / "outputs.json"
        with open(cdk_file, "w") as f:
            json.dump(cdk_outputs, f)

        output_file = tmp_path / "buildinfo.json"
        subprocess.run(
            [
                "python3",
                str(SCRIPT_PATH),
                "--output",
                str(output_file),
                "--cdk-outputs",
                str(cdk_file),
                "--quiet",
            ],
        )

        with open(output_file) as f:
            buildinfo = json.load(f)

        infra = buildinfo["infrastructure"]
        assert infra.get("cognitoUserPoolId") == "us-east-1_abc"
        assert infra.get("cognitoUserPoolClientId") == "client123"
        assert infra.get("cognitoIdentityPoolId") == "us-east-1:identity"


class TestGoldenRepoIntegration:
    """Test integration with golden repo Makefiles."""

    @pytest.mark.parametrize(
        "golden_repo",
        ["typescript-vite", "typescript-react", "typescript-nextjs"],
    )
    def test_makefile_has_buildinfo_target(self, golden_repo):
        """Verify each golden repo has buildinfo target."""
        makefile = (
            Path(__file__).parent.parent / "golden-repos" / golden_repo / "Makefile"
        )
        assert makefile.exists(), f"Makefile not found for {golden_repo}"

        content = makefile.read_text()
        assert "buildinfo:" in content, f"{golden_repo} missing buildinfo target"
        assert (
            "build-with-info:" in content
        ), f"{golden_repo} missing build-with-info target"
        assert (
            "generate-buildinfo.py" in content
        ), f"{golden_repo} not using generate-buildinfo.py"

    @pytest.mark.parametrize(
        "golden_repo,output_path",
        [
            ("typescript-vite", "dist/buildinfo.json"),
            ("typescript-react", "dist/buildinfo.json"),
            ("typescript-nextjs", "public/buildinfo.json"),
        ],
    )
    def test_correct_output_path(self, golden_repo, output_path):
        """Verify each golden repo outputs to correct location."""
        makefile = (
            Path(__file__).parent.parent / "golden-repos" / golden_repo / "Makefile"
        )
        content = makefile.read_text()
        assert (
            output_path in content
        ), f"{golden_repo} should output to {output_path}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
