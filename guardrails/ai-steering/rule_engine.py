#!/usr/bin/env python3
"""
Decoupled Rule Engine for Deterministic AI Validation

Provides a pluggable architecture for enforcing communication standards,
SDLC rules, and other deterministic constraints on AI behavior.

Architecture:
    Rule (abstract base) → Concrete rules (ResponseFormatRule, PhaseGateRule, etc.)
    RuleEngine → Orchestrates multiple rules
    ValidationContext → Provides context to rules (response text, tool args, etc.)

Usage:
    # Create engine with rules
    engine = RuleEngine()
    engine.register_rule(ResponseFormatRule())
    engine.register_rule(PhaseGateRule())

    # Validate
    context = ValidationContext(response_text="...")
    result = engine.validate(context)

    if not result.is_valid:
        print(result.violations)
"""
# File UUID: d9f3e6a4-7b2c-4e8d-9f1a-3c5b7d9e4f2a

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


# ============================================================================
# Enums & Data Classes
# ============================================================================

class RuleSeverity(Enum):
    """Severity level of rule violations."""
    BLOCKER = "blocker"      # Blocks execution (exit 1)
    WARNING = "warning"      # Shows warning, allows execution
    INFO = "info"            # Informational only


class ValidationContext(Enum):
    """Context in which validation is performed."""
    RESPONSE = "response"           # AI response text
    PRE_TOOL = "pre_tool"          # Before tool execution
    POST_TOOL = "post_tool"        # After tool execution
    FILE_WRITE = "file_write"      # File write operation
    PHASE_TRANSITION = "phase_transition"  # SDLC phase change


@dataclass
class RuleViolation:
    """Represents a single rule violation."""
    rule_name: str
    severity: RuleSeverity
    message: str
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        """Format violation for display."""
        icon = {
            RuleSeverity.BLOCKER: "⛔",
            RuleSeverity.WARNING: "⚠️",
            RuleSeverity.INFO: "ℹ️",
        }[self.severity]

        return f"{icon} [{self.rule_name}] {self.message}"


@dataclass
class ValidationResult:
    """Result of running validation rules."""
    is_valid: bool
    violations: List[RuleViolation] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def has_blockers(self) -> bool:
        """Check if any violations are blockers."""
        return any(v.severity == RuleSeverity.BLOCKER for v in self.violations)

    @property
    def has_warnings(self) -> bool:
        """Check if any violations are warnings."""
        return any(v.severity == RuleSeverity.WARNING for v in self.violations)

    def format_violations(self) -> str:
        """Format all violations for display."""
        if not self.violations:
            return ""

        lines = ["━" * 60]
        lines.append("RULE VIOLATIONS DETECTED")
        lines.append("━" * 60)

        for violation in self.violations:
            lines.append("")
            lines.append(str(violation))
            if violation.context:
                for key, value in violation.context.items():
                    lines.append(f"  {key}: {value}")

        lines.append("━" * 60)
        return "\n".join(lines)


@dataclass
class ValidationInput:
    """Input data for validation."""
    context_type: ValidationContext
    data: Dict[str, Any] = field(default_factory=dict)

    # Common fields (not all rules need all fields)
    response_text: Optional[str] = None
    tool_name: Optional[str] = None
    tool_args: Optional[Dict[str, Any]] = None
    file_path: Optional[Path] = None
    phase: Optional[float] = None


# ============================================================================
# Abstract Base Rule
# ============================================================================

class Rule(ABC):
    """
    Abstract base class for all validation rules.

    Subclasses must implement:
    - name: Unique identifier for the rule
    - description: Human-readable description
    - severity: Default severity level
    - applicable_contexts: Which contexts this rule applies to
    - validate(): Core validation logic
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique identifier for this rule."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description of what this rule enforces."""
        pass

    @property
    @abstractmethod
    def severity(self) -> RuleSeverity:
        """Default severity level for violations."""
        pass

    @property
    @abstractmethod
    def applicable_contexts(self) -> List[ValidationContext]:
        """List of contexts where this rule applies."""
        pass

    @abstractmethod
    def validate(self, input_data: ValidationInput) -> Optional[RuleViolation]:
        """
        Validate input against this rule.

        Args:
            input_data: Context and data to validate

        Returns:
            RuleViolation if rule is violated, None if valid
        """
        pass

    def is_applicable(self, context: ValidationContext) -> bool:
        """Check if rule applies to given context."""
        return context in self.applicable_contexts


# ============================================================================
# Rule Engine
# ============================================================================

class RuleEngine:
    """
    Orchestrates multiple validation rules.

    Responsibilities:
    - Register and manage rules
    - Run applicable rules for a given context
    - Aggregate results
    - Provide logging and debugging
    """

    def __init__(self, log_file: Optional[Path] = None):
        """
        Initialize rule engine.

        Args:
            log_file: Optional path to log validation results
        """
        self.rules: List[Rule] = []
        self.log_file = log_file

    def register_rule(self, rule: Rule) -> None:
        """Register a rule with the engine."""
        self.rules.append(rule)
        self.log(f"Registered rule: {rule.name}")

    def unregister_rule(self, rule_name: str) -> bool:
        """
        Unregister a rule by name.

        Returns:
            True if rule was found and removed, False otherwise
        """
        initial_count = len(self.rules)
        self.rules = [r for r in self.rules if r.name != rule_name]
        removed = len(self.rules) < initial_count

        if removed:
            self.log(f"Unregistered rule: {rule_name}")

        return removed

    def get_rules(self, context: Optional[ValidationContext] = None) -> List[Rule]:
        """
        Get all rules, optionally filtered by context.

        Args:
            context: If provided, only return rules applicable to this context

        Returns:
            List of rules
        """
        if context is None:
            return self.rules

        return [r for r in self.rules if r.is_applicable(context)]

    def validate(self, input_data: ValidationInput) -> ValidationResult:
        """
        Run all applicable rules against input data.

        Args:
            input_data: Context and data to validate

        Returns:
            ValidationResult with aggregated violations
        """
        violations = []
        applicable_rules = self.get_rules(input_data.context_type)

        self.log(f"Running {len(applicable_rules)} rules for {input_data.context_type.value}")

        for rule in applicable_rules:
            try:
                violation = rule.validate(input_data)
                if violation:
                    violations.append(violation)
                    self.log(f"Rule {rule.name}: VIOLATED")
                else:
                    self.log(f"Rule {rule.name}: PASSED")

            except Exception as e:
                # Rule execution failed - log error but continue
                self.log(f"Rule {rule.name}: ERROR - {e}")
                violations.append(RuleViolation(
                    rule_name=rule.name,
                    severity=RuleSeverity.WARNING,
                    message=f"Rule execution failed: {e}",
                    context={"error": str(e)}
                ))

        # Determine overall validity
        has_blockers = any(v.severity == RuleSeverity.BLOCKER for v in violations)
        is_valid = not has_blockers

        return ValidationResult(
            is_valid=is_valid,
            violations=violations,
            metadata={
                "context": input_data.context_type.value,
                "rules_checked": len(applicable_rules),
                "timestamp": datetime.now().isoformat(),
            }
        )

    def log(self, message: str) -> None:
        """Write log message."""
        if not self.log_file:
            return

        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.log_file, "a") as f:
            f.write(f"[{timestamp}] {message}\n")


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    """CLI entry point for rule engine."""
    import argparse
    import json

    parser = argparse.ArgumentParser(description="AI Validation Rule Engine")
    parser.add_argument("command", choices=["validate", "list-rules"],
                       help="Command to execute")
    parser.add_argument("--context", choices=[c.value for c in ValidationContext],
                       help="Validation context")
    parser.add_argument("--input", type=str,
                       help="JSON string with input data")
    parser.add_argument("--rules", nargs="+",
                       help="Specific rules to run (default: all)")

    args = parser.parse_args()

    if args.command == "list-rules":
        # This would be populated by importing concrete rules
        print("Available rules:")
        print("  - numbered_options: Enforce [1], [2], [3] format")
        print("  - phase_gate: Enforce SDLC phase restrictions")
        print("  - (Import concrete rules to see full list)")
        return 0

    elif args.command == "validate":
        if not args.context or not args.input:
            print("Error: --context and --input required for validate")
            return 1

        # Parse input
        try:
            input_dict = json.loads(args.input)
        except json.JSONDecodeError:
            print("Error: --input must be valid JSON")
            return 1

        # Create validation input
        context_type = ValidationContext(args.context)
        input_data = ValidationInput(
            context_type=context_type,
            data=input_dict,
            response_text=input_dict.get("response_text"),
            tool_name=input_dict.get("tool_name"),
            tool_args=input_dict.get("tool_args"),
            file_path=Path(input_dict["file_path"]) if "file_path" in input_dict else None,
            phase=input_dict.get("phase"),
        )

        # Create engine and run validation
        engine = RuleEngine()
        # NOTE: Concrete rules would be registered here
        result = engine.validate(input_data)

        # Output results
        if not result.is_valid:
            print(result.format_violations())
            return 1

        return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
