# Rule Engine System Guide

**File UUID:** c9e4f7a2-6d3b-4e8c-9f1a-3c5b7d9e4f2a
**Created:** 2026-02-02
**Purpose:** Comprehensive guide to the decoupled rule engine architecture

## 1.0 Overview

The Rule Engine provides a pluggable, decoupled architecture for enforcing communication standards, SDLC rules, and deterministic validation of AI behavior.

### 1.1 Key Benefits

**Decoupling:**
- Rules are independent, self-contained modules
- Easy to add, remove, or modify rules without touching core engine
- No tight coupling between rules

**Deterministic:**
- Consistent, reproducible validation results
- Ideal for testing, regression detection, and benchmarking
- Clear pass/fail criteria

**Extensible:**
- Simple Rule interface to implement
- Support for multiple validation contexts (response, file, tool, etc.)
- Configurable severity levels (BLOCKER, WARNING, INFO)

**Observable:**
- Comprehensive logging
- Violation tracking with context
- Aggregated results with metadata

### 1.2 Architecture Diagram

```
┌────────────────────────────────────────────────────────────┐
│                     Rule Engine System                     │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌──────────────┐     ┌──────────────┐                    │
│  │   Frontgate  │────▶│ Rule Engine  │                    │
│  │   Hook V2    │     │              │                    │
│  └──────────────┘     └──────┬───────┘                    │
│                              │                             │
│                              ▼                             │
│         ┌────────────────────────────────────┐            │
│         │       Registered Rules             │            │
│         ├────────────────────────────────────┤            │
│         │                                    │            │
│         │  • NumberedOptionsRule   (WARN)   │            │
│         │  • PhaseGateRule         (BLOCK)  │            │
│         │  • OneQuestionRule       (WARN)   │            │
│         │  • NoApologiesRule       (INFO)   │            │
│         │  • CitationCountRule     (INFO)   │            │
│         │  • ...custom rules...             │            │
│         │                                    │            │
│         └────────────────────────────────────┘            │
│                              │                             │
│                              ▼                             │
│         ┌────────────────────────────────────┐            │
│         │      ValidationResult               │            │
│         ├────────────────────────────────────┤            │
│         │                                    │            │
│         │  • is_valid: bool                 │            │
│         │  • violations: List[RuleViolation]│            │
│         │  • metadata: Dict                 │            │
│         │                                    │            │
│         └────────────────────────────────────┘            │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## 2.0 Core Components

### 2.1 Rule (Abstract Base Class)

All validation rules inherit from the `Rule` abstract base class.

**Required properties:**
- `name`: Unique identifier (e.g., "numbered_options")
- `description`: Human-readable description
- `severity`: BLOCKER | WARNING | INFO
- `applicable_contexts`: List of contexts where rule applies

**Required method:**
- `validate(input_data: ValidationInput) -> Optional[RuleViolation]`

**Example:**
```python
from rule_engine import Rule, RuleSeverity, RuleViolation, ValidationContext

class MyCustomRule(Rule):
    @property
    def name(self) -> str:
        return "my_rule"

    @property
    def description(self) -> str:
        return "Checks for X in Y context"

    @property
    def severity(self) -> RuleSeverity:
        return RuleSeverity.WARNING

    @property
    def applicable_contexts(self) -> List[ValidationContext]:
        return [ValidationContext.RESPONSE]

    def validate(self, input_data: ValidationInput) -> Optional[RuleViolation]:
        if not input_data.response_text:
            return None

        # Check for violation
        if "bad pattern" in input_data.response_text:
            return RuleViolation(
                rule_name=self.name,
                severity=self.severity,
                message="Found bad pattern in response",
                context={"pattern": "bad pattern"}
            )

        return None  # No violation
```

### 2.2 RuleEngine

Orchestrates multiple rules and aggregates results.

**Key methods:**
- `register_rule(rule: Rule)`: Add a rule to the engine
- `unregister_rule(name: str)`: Remove a rule by name
- `get_rules(context: Optional[ValidationContext])`: List rules
- `validate(input_data: ValidationInput) -> ValidationResult`: Run validation

**Example:**
```python
from rule_engine import RuleEngine, ValidationContext, ValidationInput
from rules import NumberedOptionsRule, PhaseGateRule

# Create engine
engine = RuleEngine(log_file=Path(".guardrails/.rule_engine.log"))

# Register rules
engine.register_rule(NumberedOptionsRule())
engine.register_rule(PhaseGateRule())

# Run validation
input_data = ValidationInput(
    context_type=ValidationContext.RESPONSE,
    response_text="Would you like to deploy or skip?"
)

result = engine.validate(input_data)

if not result.is_valid:
    print(result.format_violations())
```

### 2.3 ValidationContext

Enum defining where validation occurs:
- `RESPONSE`: AI response text
- `PRE_TOOL`: Before tool execution
- `POST_TOOL`: After tool execution
- `FILE_WRITE`: File write operation
- `PHASE_TRANSITION`: SDLC phase change

### 2.4 RuleSeverity

Enum defining violation impact:
- `BLOCKER`: Blocks execution (exit 1)
- `WARNING`: Shows warning, allows execution
- `INFO`: Informational only (for evals)

### 2.5 ValidationInput

Container for validation data:
```python
@dataclass
class ValidationInput:
    context_type: ValidationContext
    data: Dict[str, Any] = field(default_factory=dict)

    # Optional fields
    response_text: Optional[str] = None
    tool_name: Optional[str] = None
    tool_args: Optional[Dict[str, Any]] = None
    file_path: Optional[Path] = None
    phase: Optional[float] = None
```

### 2.6 ValidationResult

Container for validation results:
```python
@dataclass
class ValidationResult:
    is_valid: bool
    violations: List[RuleViolation]
    metadata: Dict[str, Any]

    @property
    def has_blockers(self) -> bool

    @property
    def has_warnings(self) -> bool

    def format_violations(self) -> str
```

## 3.0 Built-in Rules

### 3.1 Communication Rules

**NumberedOptionsRule** (CLAUDE.md Section 3.4)
- **Context:** RESPONSE
- **Severity:** WARNING
- **Purpose:** Enforce [1], [2], [3] format for multiple choice options
- **File:** `rules/numbered_options_rule.py`

**OneQuestionRule** (CLAUDE.md Section 3.2)
- **Context:** RESPONSE
- **Severity:** WARNING
- **Purpose:** Detect multiple questions in single response
- **File:** `rules/one_question_rule.py`

### 3.2 SDLC Rules

**PhaseGateRule**
- **Context:** PRE_TOOL, FILE_WRITE
- **Severity:** BLOCKER
- **Purpose:** Block code file writes before Phase 8
- **File:** `rules/phase_gate_rule.py`

### 3.3 Evaluation Rules (INFO severity)

**NoApologiesRule**
- **Purpose:** Detect unnecessary apologies
- **Use case:** Evaluate confidence in responses

**CitationCountRule**
- **Purpose:** Verify citation presence in research
- **Use case:** Evaluate research quality

**ResponseLengthRule**
- **Purpose:** Check response length appropriateness
- **Use case:** Evaluate conciseness

**CodeBlockPresenceRule**
- **Purpose:** Verify code blocks in implementation responses
- **Use case:** Evaluate technical quality

**FilePathFormatRule**
- **Purpose:** Verify absolute paths in file operations
- **Use case:** Evaluate consistency

**File:** `rules/deterministic_eval_rules.py`

## 4.0 Creating Custom Rules

### 4.1 Step-by-Step Guide

**Step 1: Create new rule file**
```bash
touch .guardrails/ai-steering/rules/my_custom_rule.py
```

**Step 2: Implement Rule interface**
```python
#!/usr/bin/env python3
"""My Custom Rule - Description"""
# File UUID: generate-with-uuidgen

import sys
from pathlib import Path
from typing import List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))

from rule_engine import (
    Rule,
    RuleSeverity,
    RuleViolation,
    ValidationContext,
    ValidationInput,
)


class MyCustomRule(Rule):
    @property
    def name(self) -> str:
        return "my_custom_rule"

    @property
    def description(self) -> str:
        return "Description of what this rule checks"

    @property
    def severity(self) -> RuleSeverity:
        return RuleSeverity.WARNING

    @property
    def applicable_contexts(self) -> List[ValidationContext]:
        return [ValidationContext.RESPONSE]

    def validate(self, input_data: ValidationInput) -> Optional[RuleViolation]:
        # Implement validation logic
        if condition_violated:
            return RuleViolation(
                rule_name=self.name,
                severity=self.severity,
                message="Violation message",
                context={"key": "value"}
            )

        return None  # No violation
```

**Step 3: Register in `rules/__init__.py`**
```python
from .my_custom_rule import MyCustomRule

__all__ = [
    "NumberedOptionsRule",
    "PhaseGateRule",
    "OneQuestionRule",
    "MyCustomRule",  # Add here
]
```

**Step 4: Register in frontgate_v2.py**
```python
def create_engine() -> RuleEngine:
    engine = RuleEngine(log_file=LOG_FILE)

    engine.register_rule(PhaseGateRule())
    engine.register_rule(NumberedOptionsRule())
    engine.register_rule(OneQuestionRule())
    engine.register_rule(MyCustomRule())  # Add here

    return engine
```

### 4.2 Rule Design Best Practices

**1. Single Responsibility**
- Each rule checks ONE thing
- Don't combine multiple validations in one rule

**2. Clear Violation Messages**
- Explain what was violated
- Show expected format
- Reference documentation (e.g., "CLAUDE.md Section X.Y")

**3. Rich Context**
- Include relevant data in `context` dict
- Helps with debugging and analytics

**4. Performance**
- Keep validation fast (<100ms per rule)
- Use regex sparingly
- Cache expensive computations

**5. False Positive Handling**
- Think through edge cases
- Add exception patterns if needed

**6. Configurability**
- Use `__init__` parameters for thresholds
- Example: `CitationCountRule(min_citations=5)`

## 5.0 Hook Integration

### 5.1 Frontgate V2 Architecture

The new `frontgate_v2.py` integrates the rule engine:

```python
# frontgate_v2.py

def create_engine() -> RuleEngine:
    """Create and configure the rule engine."""
    engine = RuleEngine(log_file=LOG_FILE)

    # Register rules
    engine.register_rule(PhaseGateRule())  # BLOCKER
    engine.register_rule(NumberedOptionsRule())  # WARNING
    engine.register_rule(OneQuestionRule())  # WARNING

    return engine


def validate_pre_tool(engine: RuleEngine, tool_name: str, tool_input: dict) -> bool:
    """Validate before tool execution (can BLOCK)."""
    if tool_name not in FILE_TOOLS:
        return True

    file_path = Path(tool_input.get("file_path"))

    input_data = ValidationInput(
        context_type=ValidationContext.PRE_TOOL,
        tool_name=tool_name,
        tool_args=tool_input,
        file_path=file_path,
    )

    result = engine.validate(input_data)

    if not result.is_valid:
        print(result.format_violations())
        return False  # BLOCK

    return True  # ALLOW
```

### 5.2 Switching from V1 to V2

**Option A: Symlink (Recommended)**
```bash
cd .claude/hooks
mv frontgate.py frontgate_v1.py
ln -s frontgate_v2.py frontgate.py
```

**Option B: Direct replacement**
```bash
cd .claude/hooks
cp frontgate.py frontgate_v1_backup.py
cp frontgate_v2.py frontgate.py
```

**Option C: Test in parallel**
```bash
# Keep both, test V2 separately
cd .claude/hooks
# V1 remains as frontgate.py
# V2 tested via: python frontgate_v2.py < input.json
```

### 5.3 Backward Compatibility

Frontgate V2 maintains backward compatibility with V1:
- Still calls legacy validators (grace_period, batch_detector, design_system)
- Same hook event handling (PreToolUse, PostToolUse)
- Same exit code behavior (0=allow, 1=block)

## 6.0 Deterministic Evaluation

### 6.1 Running Evals

**Evaluate a single response:**
```bash
python .guardrails/ai-steering/rules/deterministic_eval_rules.py eval \
  --response "Your AI response text here"
```

**List available eval rules:**
```bash
python .guardrails/ai-steering/rules/deterministic_eval_rules.py list
```

### 6.2 Batch Evaluation

```python
#!/usr/bin/env python3
"""Batch evaluation script"""

from pathlib import Path
from rule_engine import RuleEngine, ValidationContext, ValidationInput
from rules.deterministic_eval_rules import create_eval_suite

# Create engine with eval rules
engine = RuleEngine()
for rule in create_eval_suite():
    engine.register_rule(rule)

# Load test responses
responses = [
    "Response 1 text...",
    "Response 2 text...",
    "Response 3 text...",
]

# Run evaluations
results = []
for i, response in enumerate(responses):
    input_data = ValidationInput(
        context_type=ValidationContext.RESPONSE,
        response_text=response
    )

    result = engine.validate(input_data)
    results.append({
        "id": i,
        "is_valid": result.is_valid,
        "violations": [v.rule_name for v in result.violations]
    })

# Analyze results
pass_rate = sum(1 for r in results if r["is_valid"]) / len(results)
print(f"Pass rate: {pass_rate:.1%}")
```

### 6.3 Regression Detection

Use evaluation rules to detect regressions:

```python
# Save baseline results
baseline = {
    "no_apologies": 0.95,  # 95% pass rate
    "citation_count": 0.80,
    "response_length": 0.90,
}

# Run evals on new version
current = run_eval_suite(test_responses)

# Compare
for rule_name, baseline_rate in baseline.items():
    current_rate = current[rule_name]
    delta = current_rate - baseline_rate

    if delta < -0.05:  # 5% regression threshold
        print(f"REGRESSION: {rule_name} dropped {abs(delta):.1%}")
```

### 6.4 Benchmarking

Compare rule engine performance:

```python
import time

responses = load_test_dataset(n=100)

start = time.time()
for response in responses:
    result = engine.validate(ValidationInput(
        context_type=ValidationContext.RESPONSE,
        response_text=response
    ))
elapsed = time.time() - start

print(f"Validated {len(responses)} responses in {elapsed:.2f}s")
print(f"Average: {elapsed/len(responses)*1000:.1f}ms per response")
```

## 7.0 Testing

### 7.1 Running Tests

**Run all tests:**
```bash
cd .guardrails/ai-steering
pytest test_response_format_validator.py -v
```

**Run specific test class:**
```bash
pytest test_response_format_validator.py::TestValidateResponse -v
```

**Run with coverage:**
```bash
pytest test_response_format_validator.py --cov=response_format_validator --cov-report=html
```

### 7.2 Test Structure

```python
# test_my_custom_rule.py

import pytest
from rules.my_custom_rule import MyCustomRule
from rule_engine import ValidationContext, ValidationInput


class TestMyCustomRule:
    def setup_method(self):
        self.rule = MyCustomRule()

    def test_violation_detected(self):
        input_data = ValidationInput(
            context_type=ValidationContext.RESPONSE,
            response_text="bad pattern present"
        )

        violation = self.rule.validate(input_data)

        assert violation is not None
        assert violation.rule_name == "my_custom_rule"
        assert "bad pattern" in violation.message

    def test_no_violation(self):
        input_data = ValidationInput(
            context_type=ValidationContext.RESPONSE,
            response_text="good pattern present"
        )

        violation = self.rule.validate(input_data)

        assert violation is None

    def test_edge_case_empty_text(self):
        input_data = ValidationInput(
            context_type=ValidationContext.RESPONSE,
            response_text=""
        )

        violation = self.rule.validate(input_data)

        assert violation is None  # Should handle gracefully
```

### 7.3 Integration Tests

```python
def test_engine_with_multiple_rules():
    """Test rule engine with multiple rules."""
    from rule_engine import RuleEngine
    from rules import NumberedOptionsRule, OneQuestionRule

    engine = RuleEngine()
    engine.register_rule(NumberedOptionsRule())
    engine.register_rule(OneQuestionRule())

    # Response with multiple violations
    input_data = ValidationInput(
        context_type=ValidationContext.RESPONSE,
        response_text="""
        Would you like to deploy?
        Also, what's your timeline?
        And do you need CI/CD?

        - Option A
        - Option B
        """
    )

    result = engine.validate(input_data)

    assert not result.is_valid
    assert len(result.violations) == 2  # Two rules violated
    assert result.has_warnings
```

## 8.0 Logging & Debugging

### 8.1 Log File Location

```
.guardrails/.frontgate_v2.log
.guardrails/.rule_engine.log
```

### 8.2 Log Format

```
[2026-02-02 14:35:22] Registered rule: phase_gate
[2026-02-02 14:35:22] Registered rule: numbered_options
[2026-02-02 14:35:22] Hook called: tool=Write event=PreToolUse
[2026-02-02 14:35:22] Running 2 rules for pre_tool
[2026-02-02 14:35:22] Rule phase_gate: PASSED
[2026-02-02 14:35:22] Rule numbered_options: N/A (wrong context)
[2026-02-02 14:35:22] Hook completed: tool=Write
```

### 8.3 Debugging Tips

**1. Enable verbose logging**
```python
engine = RuleEngine(log_file=LOG_FILE)
engine.log("Custom debug message")
```

**2. Check rule applicability**
```python
rule = NumberedOptionsRule()
print(f"Applies to RESPONSE? {rule.is_applicable(ValidationContext.RESPONSE)}")
```

**3. Test rule in isolation**
```python
rule = NumberedOptionsRule()
input_data = ValidationInput(
    context_type=ValidationContext.RESPONSE,
    response_text="test"
)
result = rule.validate(input_data)
print(f"Violation: {result}")
```

**4. Examine violation context**
```python
if result.violations:
    for v in result.violations:
        print(f"Rule: {v.rule_name}")
        print(f"Context: {v.context}")
```

## 9.0 Performance Considerations

### 9.1 Benchmarks

Current performance (M1 MacBook Pro):
- Single rule validation: ~0.5-2ms
- Full engine (5 rules): ~5-10ms
- Pattern matching rules: ~1-3ms
- Subprocess rules (phase_checker): ~50-100ms

### 9.2 Optimization Strategies

**1. Rule ordering**
- Register fast rules first (BLOCKER rules early)
- Expensive rules last

**2. Context filtering**
- Only run applicable rules
- Engine automatically filters by context

**3. Caching**
```python
class CachedRule(Rule):
    def __init__(self):
        self._cache = {}

    def validate(self, input_data: ValidationInput):
        cache_key = hash(input_data.response_text)
        if cache_key in self._cache:
            return self._cache[cache_key]

        result = self._do_validation(input_data)
        self._cache[cache_key] = result
        return result
```

**4. Parallel execution** (future enhancement)
```python
# Run independent rules in parallel
from concurrent.futures import ThreadPoolExecutor

def validate_parallel(self, input_data: ValidationInput):
    applicable_rules = self.get_rules(input_data.context_type)

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(rule.validate, input_data)
            for rule in applicable_rules
        ]

        violations = [f.result() for f in futures if f.result()]

    return ValidationResult(...)
```

## 10.0 Future Enhancements

### 10.1 Roadmap

**Phase 1: Core (COMPLETE)**
- ✅ Rule base class and engine
- ✅ Basic rules (numbered options, phase gate, one question)
- ✅ Hook integration (frontgate_v2)
- ✅ Evaluation rules

**Phase 2: Testing & Validation**
- [ ] Comprehensive test suite for all rules
- [ ] Integration tests with frontgate hook
- [ ] Performance benchmarks
- [ ] Edge case coverage

**Phase 3: Advanced Features**
- [ ] LLM-based validation rules
- [ ] Semantic similarity checks
- [ ] Response quality scoring
- [ ] Auto-fix suggestions

**Phase 4: Developer Experience**
- [ ] Rule generator CLI
- [ ] VSCode extension for rule development
- [ ] Interactive rule debugger
- [ ] Web UI for rule management

### 10.2 Requested Features

**1. LLM-based validation**
```python
class SemanticCoherenceRule(Rule):
    """Use LLM to check response coherence."""

    def validate(self, input_data: ValidationInput):
        # Call Claude Haiku to evaluate coherence
        coherence_score = self._check_coherence(input_data.response_text)

        if coherence_score < 0.7:
            return RuleViolation(...)
```

**2. Response rewriting**
```python
class AutoFixRule(Rule):
    """Rules that can auto-fix violations."""

    def auto_fix(self, input_data: ValidationInput) -> str:
        # Return corrected version
        return self._fix_response(input_data.response_text)
```

**3. Rule chaining**
```python
class ChainedRule(Rule):
    """Rules that depend on other rules."""

    def __init__(self, prerequisite_rules: List[Rule]):
        self.prerequisites = prerequisite_rules

    def validate(self, input_data: ValidationInput):
        # Only run if prerequisites passed
        for rule in self.prerequisites:
            if rule.validate(input_data):
                return None  # Skip this rule

        return self._do_validation(input_data)
```

## 11.0 FAQ

**Q: Can rules block execution?**
A: Yes, if `severity = RuleSeverity.BLOCKER`. Hook will exit with code 1.

**Q: How do I disable a rule temporarily?**
A: `engine.unregister_rule("rule_name")` or comment out in `create_engine()`.

**Q: Can I run rules outside of hooks?**
A: Yes! Create an engine, register rules, call `engine.validate()` anywhere.

**Q: How do I test a rule without running Claude Code?**
A: Write pytest tests or run rule's `validate()` method directly.

**Q: Can rules modify responses?**
A: Not yet. Current design is validation-only. Auto-fix is a future enhancement.

**Q: Are rules run in parallel?**
A: Not yet. Current implementation is sequential. Parallel execution is planned.

**Q: Can I use rules for deterministic testing?**
A: Yes! That's a primary use case. See Section 6.0.

**Q: How do I see why a rule violated?**
A: Check `violation.context` dict for detailed information.

## 12.0 Related Documentation

- **CLAUDE.md** - Main orchestration hub with communication standards
- **SDLC_OVERVIEW** - 9-phase SDLC process
- **ENFORCEMENT.md** - Phase-based enforcement rules
- **frontgate.py** - V1 hook implementation
- **frontgate_v2.py** - V2 with rule engine integration
- **phase_checker.py** - SDLC phase gate validator
- **deterministic-transition-enforcement.md** - Research on state machines and enforcement patterns

## 13.0 Quick Reference

**Create custom rule:**
```python
class MyRule(Rule):
    # Implement: name, description, severity, applicable_contexts, validate()
```

**Register rule:**
```python
engine.register_rule(MyRule())
```

**Run validation:**
```python
result = engine.validate(ValidationInput(...))
if not result.is_valid:
    print(result.format_violations())
```

**Run tests:**
```bash
pytest test_response_format_validator.py -v
```

**Run evals:**
```bash
python rules/deterministic_eval_rules.py eval --response "text"
```

**Check logs:**
```bash
tail -f .guardrails/.frontgate_v2.log
```
