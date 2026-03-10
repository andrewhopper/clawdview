#!/usr/bin/env python3
"""
Comprehensive test suite for rule_engine.py

Tests the core RuleEngine class, Rule interface, and integration.
"""
# File UUID: a9c4f7e2-6d3b-4e8c-9f1a-3c5b7d9e4f2a

import pytest
from pathlib import Path
from rule_engine import (
    Rule,
    RuleEngine,
    RuleSeverity,
    RuleViolation,
    ValidationContext,
    ValidationInput,
    ValidationResult,
)


# ============================================================================
# Mock Rules for Testing
# ============================================================================

class AlwaysPassRule(Rule):
    """Mock rule that always passes."""

    @property
    def name(self) -> str:
        return "always_pass"

    @property
    def description(self) -> str:
        return "Always passes validation"

    @property
    def severity(self) -> RuleSeverity:
        return RuleSeverity.INFO

    @property
    def applicable_contexts(self):
        return [ValidationContext.RESPONSE]

    def validate(self, input_data):
        return None  # No violation


class AlwaysFailRule(Rule):
    """Mock rule that always fails."""

    @property
    def name(self) -> str:
        return "always_fail"

    @property
    def description(self) -> str:
        return "Always fails validation"

    @property
    def severity(self) -> RuleSeverity:
        return RuleSeverity.WARNING

    @property
    def applicable_contexts(self):
        return [ValidationContext.RESPONSE]

    def validate(self, input_data):
        return RuleViolation(
            rule_name=self.name,
            severity=self.severity,
            message="This rule always fails",
            context={"test": True}
        )


class BlockerRule(Rule):
    """Mock rule that blocks execution."""

    @property
    def name(self) -> str:
        return "blocker"

    @property
    def description(self) -> str:
        return "Blocks execution"

    @property
    def severity(self) -> RuleSeverity:
        return RuleSeverity.BLOCKER

    @property
    def applicable_contexts(self):
        return [ValidationContext.PRE_TOOL]

    def validate(self, input_data):
        return RuleViolation(
            rule_name=self.name,
            severity=self.severity,
            message="Blocked by blocker rule"
        )


class ContextSpecificRule(Rule):
    """Rule that only applies to specific context."""

    @property
    def name(self) -> str:
        return "context_specific"

    @property
    def description(self) -> str:
        return "Only applies to FILE_WRITE context"

    @property
    def severity(self) -> RuleSeverity:
        return RuleSeverity.WARNING

    @property
    def applicable_contexts(self):
        return [ValidationContext.FILE_WRITE]

    def validate(self, input_data):
        return RuleViolation(
            rule_name=self.name,
            severity=self.severity,
            message="Context-specific violation"
        )


class ThrowingRule(Rule):
    """Rule that raises an exception."""

    @property
    def name(self) -> str:
        return "throwing"

    @property
    def description(self) -> str:
        return "Raises exception during validation"

    @property
    def severity(self) -> RuleSeverity:
        return RuleSeverity.WARNING

    @property
    def applicable_contexts(self):
        return [ValidationContext.RESPONSE]

    def validate(self, input_data):
        raise ValueError("Intentional test error")


# ============================================================================
# Test RuleViolation
# ============================================================================

class TestRuleViolation:
    """Test RuleViolation data class."""

    def test_create_violation(self):
        violation = RuleViolation(
            rule_name="test_rule",
            severity=RuleSeverity.WARNING,
            message="Test violation"
        )

        assert violation.rule_name == "test_rule"
        assert violation.severity == RuleSeverity.WARNING
        assert violation.message == "Test violation"
        assert violation.context == {}

    def test_violation_with_context(self):
        violation = RuleViolation(
            rule_name="test_rule",
            severity=RuleSeverity.BLOCKER,
            message="Test violation",
            context={"key": "value", "count": 5}
        )

        assert violation.context["key"] == "value"
        assert violation.context["count"] == 5

    def test_violation_str_format(self):
        violation = RuleViolation(
            rule_name="test_rule",
            severity=RuleSeverity.WARNING,
            message="Test violation"
        )

        str_repr = str(violation)
        assert "test_rule" in str_repr
        assert "Test violation" in str_repr
        assert "⚠️" in str_repr  # Warning icon


# ============================================================================
# Test ValidationResult
# ============================================================================

class TestValidationResult:
    """Test ValidationResult data class."""

    def test_valid_result(self):
        result = ValidationResult(is_valid=True, violations=[])

        assert result.is_valid
        assert not result.has_blockers
        assert not result.has_warnings
        assert result.violations == []

    def test_result_with_warnings(self):
        violation = RuleViolation(
            rule_name="test",
            severity=RuleSeverity.WARNING,
            message="Warning"
        )

        result = ValidationResult(is_valid=True, violations=[violation])

        assert result.is_valid
        assert result.has_warnings
        assert not result.has_blockers

    def test_result_with_blockers(self):
        violation = RuleViolation(
            rule_name="test",
            severity=RuleSeverity.BLOCKER,
            message="Blocked"
        )

        result = ValidationResult(is_valid=False, violations=[violation])

        assert not result.is_valid
        assert result.has_blockers
        assert not result.has_warnings

    def test_format_violations(self):
        violations = [
            RuleViolation(
                rule_name="rule1",
                severity=RuleSeverity.WARNING,
                message="First violation"
            ),
            RuleViolation(
                rule_name="rule2",
                severity=RuleSeverity.BLOCKER,
                message="Second violation"
            ),
        ]

        result = ValidationResult(is_valid=False, violations=violations)
        formatted = result.format_violations()

        assert "RULE VIOLATIONS DETECTED" in formatted
        assert "rule1" in formatted
        assert "rule2" in formatted
        assert "First violation" in formatted
        assert "Second violation" in formatted


# ============================================================================
# Test ValidationInput
# ============================================================================

class TestValidationInput:
    """Test ValidationInput data class."""

    def test_create_basic_input(self):
        input_data = ValidationInput(
            context_type=ValidationContext.RESPONSE
        )

        assert input_data.context_type == ValidationContext.RESPONSE
        assert input_data.response_text is None
        assert input_data.tool_name is None

    def test_create_full_input(self):
        input_data = ValidationInput(
            context_type=ValidationContext.PRE_TOOL,
            response_text="Test response",
            tool_name="Write",
            tool_args={"file_path": "/test/file.py"},
            file_path=Path("/test/file.py"),
            phase=8.0
        )

        assert input_data.context_type == ValidationContext.PRE_TOOL
        assert input_data.response_text == "Test response"
        assert input_data.tool_name == "Write"
        assert input_data.file_path == Path("/test/file.py")
        assert input_data.phase == 8.0


# ============================================================================
# Test RuleEngine
# ============================================================================

class TestRuleEngine:
    """Test RuleEngine orchestrator."""

    def test_create_engine(self):
        engine = RuleEngine()
        assert engine.rules == []

    def test_register_rule(self):
        engine = RuleEngine()
        rule = AlwaysPassRule()

        engine.register_rule(rule)

        assert len(engine.rules) == 1
        assert engine.rules[0] == rule

    def test_register_multiple_rules(self):
        engine = RuleEngine()

        engine.register_rule(AlwaysPassRule())
        engine.register_rule(AlwaysFailRule())

        assert len(engine.rules) == 2

    def test_unregister_rule(self):
        engine = RuleEngine()
        engine.register_rule(AlwaysPassRule())
        engine.register_rule(AlwaysFailRule())

        removed = engine.unregister_rule("always_pass")

        assert removed
        assert len(engine.rules) == 1
        assert engine.rules[0].name == "always_fail"

    def test_unregister_nonexistent_rule(self):
        engine = RuleEngine()

        removed = engine.unregister_rule("nonexistent")

        assert not removed

    def test_get_all_rules(self):
        engine = RuleEngine()
        engine.register_rule(AlwaysPassRule())
        engine.register_rule(AlwaysFailRule())

        rules = engine.get_rules()

        assert len(rules) == 2

    def test_get_rules_by_context(self):
        engine = RuleEngine()
        engine.register_rule(AlwaysPassRule())  # RESPONSE context
        engine.register_rule(BlockerRule())  # PRE_TOOL context

        response_rules = engine.get_rules(ValidationContext.RESPONSE)
        tool_rules = engine.get_rules(ValidationContext.PRE_TOOL)

        assert len(response_rules) == 1
        assert response_rules[0].name == "always_pass"
        assert len(tool_rules) == 1
        assert tool_rules[0].name == "blocker"


# ============================================================================
# Test Validation Execution
# ============================================================================

class TestValidationExecution:
    """Test rule engine validation execution."""

    def test_validate_with_passing_rule(self):
        engine = RuleEngine()
        engine.register_rule(AlwaysPassRule())

        input_data = ValidationInput(
            context_type=ValidationContext.RESPONSE,
            response_text="Test"
        )

        result = engine.validate(input_data)

        assert result.is_valid
        assert len(result.violations) == 0

    def test_validate_with_failing_rule(self):
        engine = RuleEngine()
        engine.register_rule(AlwaysFailRule())

        input_data = ValidationInput(
            context_type=ValidationContext.RESPONSE,
            response_text="Test"
        )

        result = engine.validate(input_data)

        # WARNING violations don't mark result as invalid (only BLOCKER does)
        assert result.is_valid
        assert len(result.violations) == 1
        assert result.violations[0].rule_name == "always_fail"
        assert result.has_warnings

    def test_validate_with_blocker(self):
        engine = RuleEngine()
        engine.register_rule(BlockerRule())

        input_data = ValidationInput(
            context_type=ValidationContext.PRE_TOOL,
            tool_name="Write"
        )

        result = engine.validate(input_data)

        assert not result.is_valid
        assert result.has_blockers
        assert result.violations[0].severity == RuleSeverity.BLOCKER

    def test_validate_only_runs_applicable_rules(self):
        engine = RuleEngine()
        engine.register_rule(AlwaysPassRule())  # RESPONSE context
        engine.register_rule(ContextSpecificRule())  # FILE_WRITE context

        input_data = ValidationInput(
            context_type=ValidationContext.RESPONSE,
            response_text="Test"
        )

        result = engine.validate(input_data)

        # Only AlwaysPassRule should run (and pass)
        assert result.is_valid
        assert len(result.violations) == 0

    def test_validate_with_multiple_violations(self):
        engine = RuleEngine()
        engine.register_rule(AlwaysFailRule())
        engine.register_rule(AlwaysFailRule())  # Same rule twice

        input_data = ValidationInput(
            context_type=ValidationContext.RESPONSE,
            response_text="Test"
        )

        result = engine.validate(input_data)

        # WARNING violations don't mark result as invalid
        assert result.is_valid
        assert len(result.violations) == 2
        assert result.has_warnings

    def test_validate_handles_exception_gracefully(self):
        engine = RuleEngine()
        engine.register_rule(ThrowingRule())
        engine.register_rule(AlwaysPassRule())

        input_data = ValidationInput(
            context_type=ValidationContext.RESPONSE,
            response_text="Test"
        )

        result = engine.validate(input_data)

        # Engine should catch exception and create warning
        assert len(result.violations) == 1
        assert "Rule execution failed" in result.violations[0].message
        assert result.violations[0].severity == RuleSeverity.WARNING


# ============================================================================
# Test Rule Interface
# ============================================================================

class TestRuleInterface:
    """Test Rule abstract base class."""

    def test_rule_is_applicable(self):
        rule = AlwaysPassRule()

        assert rule.is_applicable(ValidationContext.RESPONSE)
        assert not rule.is_applicable(ValidationContext.PRE_TOOL)

    def test_context_specific_rule(self):
        rule = ContextSpecificRule()

        assert rule.is_applicable(ValidationContext.FILE_WRITE)
        assert not rule.is_applicable(ValidationContext.RESPONSE)


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegration:
    """Integration tests for complete workflows."""

    def test_full_validation_flow(self):
        """Test complete validation flow with multiple rules."""
        engine = RuleEngine()

        # Register mix of rules
        engine.register_rule(AlwaysPassRule())
        engine.register_rule(AlwaysFailRule())
        engine.register_rule(ContextSpecificRule())

        # Run validation
        input_data = ValidationInput(
            context_type=ValidationContext.RESPONSE,
            response_text="Test response"
        )

        result = engine.validate(input_data)

        # AlwaysPassRule passes, AlwaysFailRule fails (WARNING), ContextSpecificRule skipped
        # WARNING violations don't mark result as invalid
        assert result.is_valid
        assert len(result.violations) == 1
        assert result.violations[0].rule_name == "always_fail"
        assert result.has_warnings

    def test_blocker_prevents_execution(self):
        """Test that blockers mark result as invalid."""
        engine = RuleEngine()
        engine.register_rule(BlockerRule())

        input_data = ValidationInput(
            context_type=ValidationContext.PRE_TOOL,
            tool_name="Write"
        )

        result = engine.validate(input_data)

        assert not result.is_valid
        assert result.has_blockers

    def test_metadata_tracking(self):
        """Test that validation result includes metadata."""
        engine = RuleEngine()
        engine.register_rule(AlwaysPassRule())

        input_data = ValidationInput(
            context_type=ValidationContext.RESPONSE,
            response_text="Test"
        )

        result = engine.validate(input_data)

        assert "context" in result.metadata
        assert "rules_checked" in result.metadata
        assert "timestamp" in result.metadata
        assert result.metadata["context"] == "response"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
