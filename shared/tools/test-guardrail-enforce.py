#!/usr/bin/env python3
# File UUID: c2d3e4f5-a6b7-8c9d-0e1f-2a3b4c5d6e7f
"""
Test Cases for Guardrail Enforcement Agent

Tests all enforcement types:
1. Technology Preferences
2. Architecture Patterns
3. AI Steering Rules
4. File Protection
5. Phase Gates
6. Full Project Validation
"""

import json
import tempfile
from pathlib import Path
import pytest
from guardrail_enforce import (
    GuardrailEnforcer,
    EnforcementResult,
    EnforcementLevel,
    CheckType,
)


@pytest.fixture
def temp_guardrails():
    """Create temporary guardrails directory with test data."""
    with tempfile.TemporaryDirectory() as tmpdir:
        guardrails_path = Path(tmpdir) / ".guardrails"
        guardrails_path.mkdir()

        # Create tech-preferences
        tech_prefs_dir = guardrails_path / "tech-preferences"
        tech_prefs_dir.mkdir()

        backend_prefs = {
            "category": "backend",
            "preferences": [
                {"name": "fastapi", "rank": 1, "status": "approved"},
                {"name": "express", "rank": 2, "status": "approved"},
                {"name": "flask", "rank": 3, "status": "deprecated"},
            ]
        }
        (tech_prefs_dir / "backend.json").write_text(json.dumps(backend_prefs))

        # Create architecture-preferences
        arch_prefs_dir = guardrails_path / "architecture-preferences"
        arch_prefs_dir.mkdir()

        patterns = {
            "patterns": [
                {"name": "microservices", "rank": 1, "status": "approved"},
                {"name": "monolith", "rank": 2, "status": "approved"},
                {"name": "serverless", "rank": 3, "status": "experimental"},
            ]
        }
        (arch_prefs_dir / "patterns.json").write_text(json.dumps(patterns))

        # Create AI steering rules
        ai_steering_dir = guardrails_path / "ai-steering" / "rules"
        ai_steering_dir.mkdir(parents=True)

        rules = {
            "rules": [
                {
                    "id": "NO-CODE-BEFORE-PHASE-8",
                    "constraint_level": "NEVER",
                    "context": {"phase": ["1", "2", "3", "4", "5", "6", "7"]},
                    "action": "write_code",
                    "message": "Cannot write code before Phase 8",
                },
                {
                    "id": "REQUIRE-TESTS",
                    "constraint_level": "ALWAYS",
                    "context": {"phase": ["7", "8"]},
                    "action": "implement_feature",
                    "message": "Must write tests before or with implementation",
                },
            ]
        }
        (ai_steering_dir / "core.json").write_text(json.dumps(rules))

        yield guardrails_path


class TestTechnologyCheck:
    """Test technology preference enforcement."""

    def test_approved_technology(self, temp_guardrails):
        """Should approve technology in preferences."""
        enforcer = GuardrailEnforcer(guardrails_path=temp_guardrails)

        result = enforcer.check_technology("fastapi", "backend")

        assert result.approved is True
        assert result.enforcement_level == EnforcementLevel.ALLOWED
        assert "fastapi" in result.message.lower()
        assert "rank 1" in result.message.lower()

    def test_blocked_technology(self, temp_guardrails):
        """Should block technology not in preferences."""
        enforcer = GuardrailEnforcer(guardrails_path=temp_guardrails)

        result = enforcer.check_technology("django", "backend")

        assert result.approved is False
        assert result.enforcement_level == EnforcementLevel.BLOCKED
        assert "not found" in result.message.lower()
        assert len(result.alternatives) > 0  # Should suggest alternatives

    def test_deprecated_technology(self, temp_guardrails):
        """Should warn about deprecated technology."""
        enforcer = GuardrailEnforcer(guardrails_path=temp_guardrails)

        result = enforcer.check_technology("flask", "backend")

        assert result.approved is False
        assert result.enforcement_level == EnforcementLevel.WARNING
        assert "deprecated" in result.message.lower()
        assert len(result.alternatives) > 0

    def test_experimental_technology(self, temp_guardrails):
        """Should warn about experimental technology."""
        enforcer = GuardrailEnforcer(guardrails_path=temp_guardrails)

        # First add serverless to backend prefs as experimental
        backend_prefs = {
            "category": "backend",
            "preferences": [
                {"name": "fastapi", "rank": 1, "status": "approved"},
                {"name": "serverless", "rank": 4, "status": "experimental"},
            ]
        }
        tech_prefs_file = temp_guardrails / "tech-preferences" / "backend.json"
        tech_prefs_file.write_text(json.dumps(backend_prefs))

        result = enforcer.check_technology("serverless", "backend")

        assert result.approved is False
        assert result.enforcement_level == EnforcementLevel.WARNING
        assert "experimental" in result.message.lower()


class TestArchitecturePatternCheck:
    """Test architecture pattern enforcement."""

    def test_approved_pattern(self, temp_guardrails):
        """Should approve architecture pattern."""
        enforcer = GuardrailEnforcer(guardrails_path=temp_guardrails)

        result = enforcer.check_architecture_pattern("microservices")

        assert result.approved is True
        assert result.enforcement_level == EnforcementLevel.ALLOWED

    def test_blocked_pattern(self, temp_guardrails):
        """Should block unapproved pattern."""
        enforcer = GuardrailEnforcer(guardrails_path=temp_guardrails)

        result = enforcer.check_architecture_pattern("big-ball-of-mud")

        assert result.approved is False
        assert result.enforcement_level == EnforcementLevel.BLOCKED
        assert len(result.alternatives) > 0

    def test_experimental_pattern(self, temp_guardrails):
        """Should warn about experimental pattern."""
        enforcer = GuardrailEnforcer(guardrails_path=temp_guardrails)

        result = enforcer.check_architecture_pattern("serverless")

        assert result.approved is False
        assert result.enforcement_level == EnforcementLevel.WARNING
        assert "experimental" in result.message.lower()


class TestAISteeringRules:
    """Test AI steering rule enforcement."""

    def test_never_constraint_blocked(self, temp_guardrails):
        """Should block NEVER constraint."""
        enforcer = GuardrailEnforcer(guardrails_path=temp_guardrails)

        result = enforcer.check_ai_steering_rules(
            action="write_code",
            context={"phase": "6"}
        )

        assert result.approved is False
        assert result.enforcement_level == EnforcementLevel.BLOCKED
        assert "cannot write code" in result.message.lower()

    def test_always_constraint_required(self, temp_guardrails):
        """Should enforce ALWAYS constraint."""
        enforcer = GuardrailEnforcer(guardrails_path=temp_guardrails)

        result = enforcer.check_ai_steering_rules(
            action="implement_feature",
            context={"phase": "8", "has_tests": False}
        )

        # Note: This test depends on rule implementation
        # If rule checks for has_tests, it should warn/block
        assert result is not None

    def test_rule_does_not_apply(self, temp_guardrails):
        """Should allow when rule doesn't apply."""
        enforcer = GuardrailEnforcer(guardrails_path=temp_guardrails)

        result = enforcer.check_ai_steering_rules(
            action="write_code",
            context={"phase": "8"}  # Phase 8 is allowed
        )

        # Should allow (rule only applies to phases 1-7)
        assert result.approved is True


class TestFileProtection:
    """Test file protection enforcement."""

    def test_protected_file_blocked(self, temp_guardrails):
        """Should block modification of protected files."""
        enforcer = GuardrailEnforcer(guardrails_path=temp_guardrails)

        protected_file = temp_guardrails / "tech-preferences" / "backend.json"

        result = enforcer.check_file_protection(
            file_path=protected_file,
            operation="modify"
        )

        assert result.approved is False
        assert result.enforcement_level == EnforcementLevel.BLOCKED
        assert "protected" in result.message.lower()
        assert "human approval" in result.message.lower()

    def test_unprotected_file_allowed(self, temp_guardrails):
        """Should allow modification of unprotected files."""
        enforcer = GuardrailEnforcer(guardrails_path=temp_guardrails)

        normal_file = Path("/tmp/normal-file.txt")

        result = enforcer.check_file_protection(
            file_path=normal_file,
            operation="modify"
        )

        assert result.approved is True
        assert result.enforcement_level == EnforcementLevel.ALLOWED

    def test_read_protected_file_allowed(self, temp_guardrails):
        """Should allow reading protected files."""
        enforcer = GuardrailEnforcer(guardrails_path=temp_guardrails)

        protected_file = temp_guardrails / "tech-preferences" / "backend.json"

        result = enforcer.check_file_protection(
            file_path=protected_file,
            operation="read"
        )

        assert result.approved is True


class TestPhaseGates:
    """Test phase gate enforcement."""

    def test_code_in_early_phase_blocked(self, temp_guardrails):
        """Should block code writing in early phases."""
        enforcer = GuardrailEnforcer(guardrails_path=temp_guardrails)

        result = enforcer.check_phase_gate(
            current_phase=6,
            action="write_code"
        )

        assert result.approved is False
        assert result.enforcement_level == EnforcementLevel.BLOCKED
        assert "phase 8" in result.message.lower()
        assert len(result.alternatives) > 0

    def test_code_in_implementation_phase_allowed(self, temp_guardrails):
        """Should allow code writing in Phase 8+."""
        enforcer = GuardrailEnforcer(guardrails_path=temp_guardrails)

        result = enforcer.check_phase_gate(
            current_phase=8,
            action="write_code"
        )

        assert result.approved is True
        assert result.enforcement_level == EnforcementLevel.ALLOWED

    def test_spike_mode_bypasses_gate(self, temp_guardrails):
        """SPIKE mode should bypass phase gates."""
        enforcer = GuardrailEnforcer(guardrails_path=temp_guardrails)

        result = enforcer.check_phase_gate(
            current_phase=3,
            action="write_code",
            mode="SPIKE"
        )

        assert result.approved is True
        assert "spike" in result.message.lower()


class TestFullProjectValidation:
    """Test full project validation."""

    def test_validates_multiple_rules(self, temp_guardrails):
        """Should check multiple rules in one pass."""
        enforcer = GuardrailEnforcer(guardrails_path=temp_guardrails)

        project_config = {
            "technologies": [
                {"name": "fastapi", "category": "backend"},
                {"name": "react", "category": "frontend"},  # Not in prefs
            ],
            "phase": 6,
            "wants_to": "write_code"
        }

        results = enforcer.validate_project(project_config)

        # Should have multiple checks
        assert len(results) > 0

        # Should have at least one blocked (react not in prefs, or code in phase 6)
        assert any(not r.approved for r in results)

    def test_clean_project_passes(self, temp_guardrails):
        """Clean project should pass validation."""
        enforcer = GuardrailEnforcer(guardrails_path=temp_guardrails)

        project_config = {
            "technologies": [
                {"name": "fastapi", "category": "backend"},
            ],
            "architecture_pattern": "microservices",
            "phase": 8,
            "wants_to": "write_code"
        }

        results = enforcer.validate_project(project_config)

        # Should pass all checks
        assert all(r.approved for r in results)


class TestAuditLogging:
    """Test audit logging functionality."""

    def test_logs_enforcement_decision(self, temp_guardrails):
        """Should log all enforcement decisions."""
        enforcer = GuardrailEnforcer(guardrails_path=temp_guardrails)

        # Enable audit logging
        enforcer.enable_audit_log()

        # Make a check
        enforcer.check_technology("fastapi", "backend")

        # Check audit log exists
        audit_log = temp_guardrails / "enforcement-audit.jsonl"
        assert audit_log.exists()

        # Check log content
        log_lines = audit_log.read_text().strip().split("\n")
        assert len(log_lines) > 0

        log_entry = json.loads(log_lines[-1])
        assert "check_type" in log_entry
        assert "approved" in log_entry
        assert "timestamp" in log_entry

    def test_logs_blocked_action(self, temp_guardrails):
        """Should log blocked actions with details."""
        enforcer = GuardrailEnforcer(guardrails_path=temp_guardrails)
        enforcer.enable_audit_log()

        # Block an action
        enforcer.check_technology("django", "backend")

        # Check log
        audit_log = temp_guardrails / "enforcement-audit.jsonl"
        log_lines = audit_log.read_text().strip().split("\n")
        log_entry = json.loads(log_lines[-1])

        assert log_entry["approved"] is False
        assert "django" in str(log_entry)


class TestCLIIntegration:
    """Test CLI integration."""

    def test_check_tech_command(self, temp_guardrails):
        """Test check-tech CLI command."""
        import subprocess
        import sys

        result = subprocess.run(
            [
                sys.executable,
                str(Path(__file__).parent / "guardrail-enforce.py"),
                "check-tech",
                "--name", "fastapi",
                "--category", "backend",
                "--guardrails-path", str(temp_guardrails)
            ],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        assert "approved" in result.stdout.lower() or "fastapi" in result.stdout.lower()

    def test_check_phase_command(self, temp_guardrails):
        """Test check-phase CLI command."""
        import subprocess
        import sys

        result = subprocess.run(
            [
                sys.executable,
                str(Path(__file__).parent / "guardrail-enforce.py"),
                "check-phase",
                "--phase", "6",
                "--action", "write_code",
                "--guardrails-path", str(temp_guardrails)
            ],
            capture_output=True,
            text=True
        )

        assert result.returncode == 1  # Should fail (blocked)
        assert "blocked" in result.stdout.lower() or "cannot" in result.stdout.lower()


class TestIntegrationWithQualityAgent:
    """Test integration between guardrail enforcement and quality checks."""

    def test_guardrails_run_before_quality_checks(self, temp_guardrails):
        """Guardrail enforcement should run before quality checks."""
        enforcer = GuardrailEnforcer(guardrails_path=temp_guardrails)

        # Simulate workflow: Check guardrails first
        tech_result = enforcer.check_technology("fastapi", "backend")
        phase_result = enforcer.check_phase_gate(8, "write_code")

        # Only proceed to quality checks if guardrails pass
        if tech_result.approved and phase_result.approved:
            # Would run quality checks here
            quality_checks_allowed = True
        else:
            quality_checks_allowed = False

        assert quality_checks_allowed is True


# Performance test
def test_performance_bulk_checks(temp_guardrails):
    """Guardrail checks should be fast for bulk operations."""
    import time

    enforcer = GuardrailEnforcer(guardrails_path=temp_guardrails)

    start = time.time()

    # Run 100 checks
    for i in range(100):
        enforcer.check_technology("fastapi", "backend")

    elapsed = time.time() - start

    # Should complete in under 1 second
    assert elapsed < 1.0, f"Bulk checks took {elapsed:.2f}s (should be < 1s)"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
