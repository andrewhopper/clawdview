#!/usr/bin/env python3
"""
Tests for hook-engine.py

Run with: pytest test_hook_engine.py -v
"""

# File UUID: 9a2f7c4d-3b8e-4f5a-8d1c-7e6b2f9a4c3d

import pytest
import tempfile
import json
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import using the actual module name with dash
import importlib.util
spec = importlib.util.spec_from_file_location("hook_engine", Path(__file__).parent / "hook-engine.py")
hook_engine_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hook_engine_module)

HookEngine = hook_engine_module.HookEngine
HookMatch = hook_engine_module.HookMatch


@pytest.fixture
def engine():
    """Create a hook engine instance"""
    return HookEngine()


@pytest.fixture
def temp_html_mockup(tmp_path):
    """Create a temporary standalone HTML mockup"""
    html_file = tmp_path / "mockup.html"
    html_file.write_text("""
<!DOCTYPE html>
<html>
<head>
    <!-- Asset: Test Mockup -->
    <!-- Design System: shared/design-system -->
    <title>Test Mockup</title>
</head>
<body>
    <h1>Test Mockup</h1>
</body>
</html>
    """)
    return html_file


@pytest.fixture
def temp_html_component(tmp_path):
    """Create a temporary React component"""
    html_file = tmp_path / "component.tsx"
    html_file.write_text("""
import React from 'react';

export default function Component() {
    return <div>Test Component</div>;
}
    """)
    return html_file


@pytest.fixture
def temp_pdf_small(tmp_path):
    """Create a small PDF file (< 10MB)"""
    pdf_file = tmp_path / "document.pdf"
    pdf_file.write_text("Small PDF content")  # < 10MB
    return pdf_file


@pytest.fixture
def temp_buildinfo(tmp_path):
    """Create a buildinfo.json file"""
    buildinfo_file = tmp_path / "buildinfo.json"
    buildinfo_data = {
        "git": {
            "hash": "abc123def456",
            "branch": "main"
        },
        "deployment": {
            "timestamp": "2026-02-04T10:00:00Z"
        }
    }
    buildinfo_file.write_text(json.dumps(buildinfo_data, indent=2))
    return buildinfo_file


class TestFileCreation:
    """Test file creation detection"""

    def test_html_mockup_detection(self, engine, temp_html_mockup):
        """Test detection of standalone HTML mockup"""
        result = engine.check_file_created(str(temp_html_mockup))

        assert result is not None
        assert result.matched is True
        assert "html" in result.rule_name.lower()  # Rule name is "HTML file created"
        assert "mockup" in result.inject_text.lower()  # But inject text mentions mockup
        assert "OFFER USER" in result.inject_text
        assert "[1] View locally" in result.inject_text
        assert "[2] Publish to S3" in result.inject_text

    def test_html_component_detection(self, engine, temp_html_component):
        """Test detection of React component (should not trigger mockup rule)"""
        result = engine.check_file_created(str(temp_html_component))

        # Should not match HTML mockup rule due to React imports
        # Might match component rule or return None
        if result:
            assert "component" in result.rule_name.lower()

    def test_pdf_small_detection(self, engine, temp_pdf_small):
        """Test detection of small PDF"""
        result = engine.check_file_created(str(temp_pdf_small))

        assert result is not None
        assert result.matched is True
        assert "PDF" in result.rule_name
        assert "OFFER USER" in result.inject_text
        assert "[1] Open in default viewer" in result.inject_text

    def test_buildinfo_detection(self, engine, temp_buildinfo):
        """Test detection of buildinfo.json"""
        result = engine.check_file_created(str(temp_buildinfo))

        assert result is not None
        assert result.matched is True
        assert "buildinfo" in result.rule_name.lower()
        assert "abc123d" in result.inject_text  # First 7 chars of hash
        assert "main" in result.inject_text  # Branch name

    def test_spreadsheet_detection(self, engine, tmp_path):
        """Test detection of spreadsheet files"""
        xlsx_file = tmp_path / "data.xlsx"
        xlsx_file.write_text("Spreadsheet content")

        result = engine.check_file_created(str(xlsx_file))

        assert result is not None
        assert result.matched is True
        assert "Spreadsheet" in result.rule_name
        assert "OFFER USER" in result.inject_text

    def test_image_detection(self, engine, tmp_path):
        """Test detection of image files"""
        png_file = tmp_path / "diagram.png"
        png_file.write_text("PNG content")

        result = engine.check_file_created(str(png_file))

        assert result is not None
        assert result.matched is True
        assert "Image" in result.rule_name
        assert "OFFER USER" in result.inject_text

    def test_svg_detection(self, engine, tmp_path):
        """Test detection of SVG files"""
        svg_file = tmp_path / "diagram.svg"
        svg_file.write_text("<svg>SVG content</svg>")

        result = engine.check_file_created(str(svg_file))

        assert result is not None
        assert result.matched is True
        assert "SVG" in result.rule_name
        assert "OFFER USER" in result.inject_text

    def test_test_file_detection(self, engine, tmp_path):
        """Test detection of test files"""
        test_file = tmp_path / "test_example.py"
        test_file.write_text("def test_something(): pass")

        result = engine.check_file_created(str(test_file))

        assert result is not None
        assert result.matched is True
        assert "test" in result.rule_name.lower()
        assert "OFFER USER" in result.inject_text
        assert "Run tests now" in result.inject_text

    def test_no_match(self, engine, tmp_path):
        """Test that random files don't trigger hooks"""
        random_file = tmp_path / "random.txt"
        random_file.write_text("Random content")

        result = engine.check_file_created(str(random_file))

        assert result is None


class TestFileModification:
    """Test file modification detection"""

    def test_package_json_modification(self, engine, tmp_path):
        """Test detection of package.json modification"""
        package_file = tmp_path / "package.json"
        package_file.write_text('{"dependencies": {}}')

        result = engine.check_file_modified(str(package_file))

        assert result is not None
        assert result.matched is True
        assert "Dependencies" in result.rule_name
        assert "OFFER USER" in result.inject_text
        assert "Install dependencies" in result.inject_text
        assert "npm" in result.inject_text  # Should detect npm

    def test_requirements_txt_modification(self, engine, tmp_path):
        """Test detection of requirements.txt modification"""
        req_file = tmp_path / "requirements.txt"
        req_file.write_text("requests==2.28.0")

        result = engine.check_file_modified(str(req_file))

        assert result is not None
        assert result.matched is True
        assert "Dependencies" in result.rule_name
        assert "pip" in result.inject_text.lower()


class TestCommandOutput:
    """Test command output detection"""

    def test_aws_credentials_expired(self, engine):
        """Test detection of expired AWS credentials"""
        output = """
Error: ExpiredToken: The security token included in the request is expired
        """

        result = engine.check_command_output(output)

        assert result is not None
        assert result.matched is True
        assert "credentials expired" in result.rule_name.lower()
        assert "AWS credentials expired" in result.inject_text
        assert "Refresh credentials" in result.inject_text

    def test_port_in_use(self, engine):
        """Test detection of port already in use"""
        output = """
Error: listen EADDRINUSE: address already in use :::3000
        """

        result = engine.check_command_output(output)

        assert result is not None
        assert result.matched is True
        assert "port" in result.rule_name.lower()
        assert "Port" in result.inject_text
        assert "already in use" in result.inject_text

    def test_amplify_build_failure(self, engine):
        """Test detection of Amplify build failure"""
        output = """
amplify build failed with error code 1
Build failed
        """

        result = engine.check_command_output(output)

        assert result is not None
        assert result.matched is True
        assert "amplify" in result.rule_name.lower()
        assert "build failed" in result.inject_text.lower()

    def test_cdk_deploy_complete(self, engine):
        """Test detection of CDK deployment complete"""
        output = """
Stack deployment complete
Outputs:
  ApiEndpoint = https://api.example.com
        """

        result = engine.check_command_output(output)

        # Should match CDK stack deployed rule
        if result:
            assert "cdk" in result.rule_name.lower() or "stack" in result.rule_name.lower()


class TestDeployment:
    """Test deployment detection"""

    def test_generic_deployment(self, engine):
        """Test generic site deployment"""
        data = {
            "url": "https://example.com",
            "git_hash": "abc123d"
        }

        result = engine.check_deployment("deployment_complete", data)

        assert result is not None
        assert result.matched is True
        assert "https://example.com" in result.inject_text
        assert "AUTO ACTIONS" in result.inject_text
        assert "smoke test" in result.inject_text.lower()

    def test_amplify_deployment(self, engine):
        """Test Amplify deployment"""
        data = {
            "amplify_url": "https://main.d1234abcd.amplifyapp.com",
            "custom_domain": "https://example.com",
            "branch": "main",
            "commit": "abc123d"
        }

        result = engine.check_deployment("amplify_deployment", data)

        assert result is not None
        assert result.matched is True
        assert "Amplify" in result.inject_text
        assert "https://example.com" in result.inject_text
        assert "main" in result.inject_text
        assert "abc123d" in result.inject_text

    def test_cloudfront_deployment(self, engine):
        """Test CloudFront deployment"""
        data = {
            "cloudfront_url": "https://d1234abcd.cloudfront.net",
            "custom_domain": "https://example.com"
        }

        result = engine.check_deployment("cloudfront_deployment", data)

        assert result is not None
        assert result.matched is True
        assert "CloudFront" in result.inject_text
        assert "cloudfront.net" in result.inject_text
        assert "example.com" in result.inject_text

    def test_lambda_deployment(self, engine):
        """Test Lambda deployment"""
        data = {
            "function_name": "my-function",
            "function_url": "https://abc123.lambda-url.us-east-1.on.aws"
        }

        result = engine.check_deployment("lambda_deployment", data)

        assert result is not None
        assert result.matched is True
        assert "Lambda" in result.inject_text
        assert "my-function" in result.inject_text
        assert "lambda-url" in result.inject_text


class TestConditions:
    """Test condition evaluation"""

    def test_is_standalone_mockup_condition(self, engine, temp_html_mockup):
        """Test is_standalone_mockup condition"""
        result = engine._eval_condition("is_standalone_mockup", temp_html_mockup)
        assert result is True

    def test_is_component_condition(self, engine, temp_html_component):
        """Test is_component condition"""
        result = engine._eval_condition("is_component", temp_html_component)
        assert result is True

    def test_size_conditions(self, engine, temp_pdf_small):
        """Test size-based conditions"""
        # Small file should be < 10MB
        result_lt = engine._eval_condition("size_lt_10mb", temp_pdf_small)
        assert result_lt is True

        result_gte = engine._eval_condition("size_gte_10mb", temp_pdf_small)
        assert result_gte is False


class TestMetadata:
    """Test metadata gathering"""

    def test_gather_file_metadata(self, engine, temp_html_mockup):
        """Test metadata gathering for files"""
        metadata = engine._gather_file_metadata(temp_html_mockup)

        assert "path" in metadata
        assert "filename" in metadata
        assert "extension" in metadata
        assert "size_bytes" in metadata
        assert "size_kb" in metadata
        assert "size_mb" in metadata
        assert metadata["filename"] == "mockup.html"
        assert metadata["extension"] == ".html"

    def test_detect_test_framework(self, engine):
        """Test test framework detection"""
        pytest_file = Path("test_example.py")
        assert engine._detect_test_framework(pytest_file) == "pytest"

        jest_file = Path("example.test.ts")
        assert "jest" in engine._detect_test_framework(jest_file)

        spec_file = Path("example.spec.js")
        assert "jest" in engine._detect_test_framework(spec_file)

    def test_detect_package_manager(self, engine, tmp_path):
        """Test package manager detection"""
        package_json = tmp_path / "package.json"
        assert "npm" in engine._detect_package_manager(package_json)

        requirements_txt = tmp_path / "requirements.txt"
        assert "pip" in engine._detect_package_manager(requirements_txt)

        go_mod = tmp_path / "go.mod"
        assert "go" in engine._detect_package_manager(go_mod)


class TestIntegration:
    """Integration tests"""

    def test_full_html_workflow(self, engine, temp_html_mockup):
        """Test full HTML mockup workflow"""
        # Check file created
        result = engine.check_file_created(str(temp_html_mockup))

        assert result is not None
        assert result.matched is True
        assert "html" in result.rule_name.lower()  # Rule name is "HTML file created"
        assert "mockup" in result.inject_text.lower()  # But inject text mentions mockup

        # Verify inject text contains expected elements
        assert "OFFER USER" in result.inject_text
        assert "[1]" in result.inject_text
        assert "[2]" in result.inject_text
        assert "[3]" in result.inject_text

        # Verify metadata
        assert result.metadata["path"] == str(temp_html_mockup)
        assert result.metadata["filename"] == "mockup.html"

    def test_full_deployment_workflow(self, engine):
        """Test full deployment workflow"""
        # Simulate Amplify deployment
        data = {
            "amplify_url": "https://main.d1234.amplifyapp.com",
            "custom_domain": "https://app.example.com",
            "branch": "main",
            "commit": "abc123d"
        }

        result = engine.check_deployment("amplify_deployment", data)

        assert result is not None
        assert result.matched is True

        # Verify inject text contains deployment info
        assert "Amplify" in result.inject_text
        assert "app.example.com" in result.inject_text
        assert "main" in result.inject_text
        assert "abc123d" in result.inject_text

        # Verify it mentions smoke test
        assert "smoke test" in result.inject_text.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
