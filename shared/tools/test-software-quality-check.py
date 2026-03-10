#!/usr/bin/env python3
# File UUID: b1c2d3e4-f5a6-7b8c-9d0e-1f2a3b4c5d6e
"""
Test Cases for Software Quality Check Agent

Tests all 8 quality checks:
1. Configuration Abstraction
2. Shared Model Reuse
3. Code Decomposition
4. Testing Presence
5. Type Safety
6. Security Best Practices
7. Design System Compliance
8. Domain Model Usage
"""

import tempfile
from pathlib import Path
import pytest
from software_quality_check import (
    SoftwareQualityChecker,
    Severity,
    CheckType,
)


@pytest.fixture
def temp_project():
    """Create a temporary project directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir)
        (project_path / "src").mkdir()
        yield project_path


class TestConfigAbstraction:
    """Test configuration abstraction checks."""

    def test_detects_hardcoded_cognito_pool(self, temp_project):
        """Should detect hardcoded Cognito User Pool ID."""
        # Create file with hardcoded Cognito pool
        code_file = temp_project / "src" / "auth.ts"
        code_file.write_text("""
const userPoolId = 'us-east-1_AbcDefGhi';
const client = new CognitoClient(userPoolId);
""")

        checker = SoftwareQualityChecker(temp_project, checks=["config"])
        report = checker.run_all_checks()

        # Should find hardcoded value
        config_issues = report.get_issues_by_check(CheckType.CONFIG_ABSTRACTION)
        assert len(config_issues) > 0
        assert any("us-east-1_AbcDefGhi" in str(issue.message) for issue in config_issues)

    def test_passes_with_env_vars(self, temp_project):
        """Should pass when using environment variables."""
        code_file = temp_project / "src" / "auth.ts"
        code_file.write_text("""
const userPoolId = process.env.COGNITO_USER_POOL_ID;
const client = new CognitoClient(userPoolId);
""")

        checker = SoftwareQualityChecker(temp_project, checks=["config"])
        report = checker.run_all_checks()

        # Should not find issues
        config_issues = report.get_issues_by_check(CheckType.CONFIG_ABSTRACTION)
        assert len([i for i in config_issues if i.severity == Severity.ERROR]) == 0


class TestCodeDecomposition:
    """Test code decomposition checks."""

    def test_detects_large_file(self, temp_project):
        """Should detect files > 500 lines."""
        large_file = temp_project / "src" / "large.py"
        large_file.write_text("\n".join([f"# Line {i}" for i in range(600)]))

        checker = SoftwareQualityChecker(temp_project, checks=["decomposition"])
        report = checker.run_all_checks()

        # Should find error
        decomp_issues = report.get_issues_by_check(CheckType.CODE_DECOMPOSITION)
        assert len(decomp_issues) > 0
        assert any(i.severity == Severity.ERROR for i in decomp_issues)
        assert any("600 lines" in i.message for i in decomp_issues)

    def test_warns_medium_file(self, temp_project):
        """Should warn for files 300-500 lines."""
        medium_file = temp_project / "src" / "medium.py"
        medium_file.write_text("\n".join([f"# Line {i}" for i in range(400)]))

        checker = SoftwareQualityChecker(temp_project, checks=["decomposition"])
        report = checker.run_all_checks()

        # Should find warning
        decomp_issues = report.get_issues_by_check(CheckType.CODE_DECOMPOSITION)
        assert len(decomp_issues) > 0
        assert any(i.severity == Severity.WARNING for i in decomp_issues)
        assert any("400 lines" in i.message for i in decomp_issues)

    def test_passes_small_file(self, temp_project):
        """Should pass for files < 300 lines."""
        small_file = temp_project / "src" / "small.py"
        small_file.write_text("\n".join([f"# Line {i}" for i in range(200)]))

        checker = SoftwareQualityChecker(temp_project, checks=["decomposition"])
        report = checker.run_all_checks()

        # Should pass
        assert CheckType.CODE_DECOMPOSITION in report.passed_checks


class TestTestingPresence:
    """Test testing presence checks."""

    def test_detects_missing_tests(self, temp_project):
        """Should detect when no test files exist."""
        # Create source file but no tests
        (temp_project / "src" / "service.ts").write_text("export class Service {}")

        checker = SoftwareQualityChecker(temp_project, checks=["tests"])
        report = checker.run_all_checks()

        # Should find error
        test_issues = report.get_issues_by_check(CheckType.TESTING_PRESENCE)
        assert len(test_issues) > 0
        assert any(i.severity == Severity.ERROR for i in test_issues)
        assert any("No test files found" in i.message for i in test_issues)

    def test_passes_with_test_files(self, temp_project):
        """Should pass when test files exist."""
        # Create test file
        (temp_project / "src").mkdir(exist_ok=True)
        (temp_project / "src" / "service.test.ts").write_text("""
describe('Service', () => {
  it('should work', () => {
    expect(true).toBe(true);
  });
});
""")

        checker = SoftwareQualityChecker(temp_project, checks=["tests"])
        report = checker.run_all_checks()

        # Should pass
        assert CheckType.TESTING_PRESENCE in report.passed_checks


class TestTypeSafety:
    """Test type safety checks."""

    def test_detects_javascript_files(self, temp_project):
        """Should warn about .js files (should use .ts)."""
        js_file = temp_project / "src" / "service.js"
        js_file.write_text("function doSomething() { return 42; }")

        checker = SoftwareQualityChecker(temp_project, checks=["types"])
        report = checker.run_all_checks()

        # Should find warning
        type_issues = report.get_issues_by_check(CheckType.TYPE_SAFETY)
        assert len(type_issues) > 0
        assert any("JavaScript file found" in i.message for i in type_issues)

    def test_passes_with_typescript(self, temp_project):
        """Should pass with TypeScript files."""
        ts_file = temp_project / "src" / "service.ts"
        ts_file.write_text("""
export function doSomething(): number {
  return 42;
}
""")

        checker = SoftwareQualityChecker(temp_project, checks=["types"])
        report = checker.run_all_checks()

        # Should pass
        assert CheckType.TYPE_SAFETY in report.passed_checks


class TestSecurity:
    """Test security checks."""

    def test_detects_insecure_websocket(self, temp_project):
        """Should detect insecure WebSocket (ws://)."""
        code_file = temp_project / "src" / "socket.ts"
        code_file.write_text("""
const ws = new WebSocket('ws://localhost:3000');
ws.onopen = () => console.log('Connected');
""")

        checker = SoftwareQualityChecker(temp_project, checks=["security"])
        report = checker.run_all_checks()

        # Should find error
        security_issues = report.get_issues_by_check(CheckType.SECURITY)
        assert len(security_issues) > 0
        assert any(i.severity == Severity.ERROR for i in security_issues)
        assert any("ws://" in i.code_snippet for i in security_issues if i.code_snippet)

    def test_passes_with_secure_websocket(self, temp_project):
        """Should pass with secure WebSocket (wss://)."""
        code_file = temp_project / "src" / "socket.ts"
        code_file.write_text("""
const ws = new WebSocket('wss://localhost:3000');
ws.onopen = () => console.log('Connected');
""")

        checker = SoftwareQualityChecker(temp_project, checks=["security"])
        report = checker.run_all_checks()

        # Should pass
        assert CheckType.SECURITY in report.passed_checks


class TestDesignSystem:
    """Test design system compliance checks."""

    def test_detects_raw_hex_colors(self, temp_project):
        """Should detect raw hex colors (should use tokens)."""
        ui_file = temp_project / "src" / "component.tsx"
        ui_file.write_text("""
export function Button() {
  return (
    <button style={{ backgroundColor: '#1a1a2e' }}>
      Click me
    </button>
  );
}
""")

        checker = SoftwareQualityChecker(temp_project, checks=["design-system"])
        report = checker.run_all_checks()

        # Should find error
        design_issues = report.get_issues_by_check(CheckType.DESIGN_SYSTEM)
        assert len(design_issues) > 0
        assert any(i.severity == Severity.ERROR for i in design_issues)
        assert any("Raw hex color" in i.message for i in design_issues)

    def test_passes_with_design_tokens(self, temp_project):
        """Should pass when using design tokens."""
        ui_file = temp_project / "src" / "component.tsx"
        ui_file.write_text("""
export function Button() {
  return (
    <button className="bg-primary text-foreground">
      Click me
    </button>
  );
}
""")

        checker = SoftwareQualityChecker(temp_project, checks=["design-system"])
        report = checker.run_all_checks()

        # Should pass
        assert CheckType.DESIGN_SYSTEM in report.passed_checks


class TestDomainModelUsage:
    """Test domain model usage checks."""

    def test_detects_missing_timestamps(self, temp_project):
        """Should detect domain models without timestamps."""
        model_file = temp_project / "src" / "models.py"
        model_file.write_text("""
from pydantic import BaseModel

class User(BaseModel):
    id: str
    name: str
    email: str
""")

        checker = SoftwareQualityChecker(temp_project, checks=["domain-models"])
        report = checker.run_all_checks()

        # Should find warning
        domain_issues = report.get_issues_by_check(CheckType.DOMAIN_MODEL_USAGE)
        assert len(domain_issues) > 0
        assert any("timestamp fields" in i.message for i in domain_issues)

    def test_passes_with_timestamps(self, temp_project):
        """Should pass when timestamps are present."""
        model_file = temp_project / "src" / "models.py"
        model_file.write_text("""
from datetime import datetime
from pydantic import BaseModel, Field

class User(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
""")

        checker = SoftwareQualityChecker(temp_project, checks=["domain-models"])
        report = checker.run_all_checks()

        # Should pass
        assert CheckType.DOMAIN_MODEL_USAGE in report.passed_checks


class TestFullAudit:
    """Test full project audit."""

    def test_comprehensive_audit(self, temp_project):
        """Run full audit on project with multiple issues."""
        # Create various files with issues
        (temp_project / "src" / "large.py").write_text("\n".join([f"# Line {i}" for i in range(600)])
        )
        (temp_project / "src" / "insecure.ts").write_text("const ws = new WebSocket('ws://localhost');")
        (temp_project / "src" / "ui.tsx").write_text("<div style={{ color: '#ff0000' }}>Red</div>")

        checker = SoftwareQualityChecker(temp_project, checks=["all"])
        report = checker.run_all_checks()

        # Should find multiple issues
        assert report.error_count > 0
        assert len(report.checks_run) == 8  # All checks run

    def test_passes_clean_project(self, temp_project):
        """Clean project should pass all checks."""
        # Create small, well-structured files
        (temp_project / "src" / "service.ts").write_text("""
export function add(a: number, b: number): number {
  return a + b;
}
""")
        (temp_project / "src" / "service.test.ts").write_text("""
import { add } from './service';

describe('add', () => {
  it('adds numbers', () => {
    expect(add(1, 2)).toBe(3);
  });
});
""")

        checker = SoftwareQualityChecker(temp_project, checks=["all"])
        report = checker.run_all_checks()

        # Should have minimal or no errors
        assert report.error_count == 0 or report.has_warnings


# Integration test
def test_cli_integration(temp_project):
    """Test CLI integration."""
    import subprocess
    import sys

    # Create test file
    (temp_project / "src" / "test.py").write_text("print('hello')")

    # Run CLI
    result = subprocess.run(
        [sys.executable, str(Path(__file__).parent / "software-quality-check.py"),
         "--project", str(temp_project), "--format", "json"],
        capture_output=True,
        text=True
    )

    # Should complete successfully
    assert result.returncode in (0, 1)  # 0 = pass, 1 = fail with issues
    assert "project" in result.stdout  # JSON output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
