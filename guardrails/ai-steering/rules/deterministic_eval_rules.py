#!/usr/bin/env python3
"""
Deterministic Evaluation Rules

Example rules demonstrating how to use the rule engine for deterministic
evaluation of AI behavior, responses, and outputs.

These rules can be used for:
- Automated testing of AI responses
- Regression detection
- Quality assurance
- Benchmarking
"""
# File UUID: e8f4a9c2-6d3b-4e7c-9f1a-2b4c6d8e9f7a

import re
import sys
from pathlib import Path
from typing import List, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from rule_engine import (
    Rule,
    RuleSeverity,
    RuleViolation,
    ValidationContext,
    ValidationInput,
)


# ============================================================================
# Rule 1: No Apologies
# ============================================================================

class NoApologiesRule(Rule):
    """
    Detect unnecessary apologies in AI responses.

    AI should be helpful and direct without excessive apologies.
    Phrases like "I apologize", "Sorry", "Unfortunately" should be minimized.

    Used for: Evaluating confidence and directness in AI responses.
    """

    APOLOGY_PATTERNS = [
        r"i apologize",
        r"i'm sorry",
        r"sorry about",
        r"my apologies",
        r"unfortunately",
    ]

    @property
    def name(self) -> str:
        return "no_apologies"

    @property
    def description(self) -> str:
        return "Detect unnecessary apologies in responses (eval rule)"

    @property
    def severity(self) -> RuleSeverity:
        return RuleSeverity.INFO  # For evaluation only

    @property
    def applicable_contexts(self) -> List[ValidationContext]:
        return [ValidationContext.RESPONSE]

    def validate(self, input_data: ValidationInput) -> Optional[RuleViolation]:
        if not input_data.response_text:
            return None

        text_lower = input_data.response_text.lower()
        apologies_found = []

        for pattern in self.APOLOGY_PATTERNS:
            matches = re.findall(pattern, text_lower)
            apologies_found.extend(matches)

        if not apologies_found:
            return None  # No apologies, good

        message = f"""
Evaluation: Unnecessary apologies detected

Found {len(apologies_found)} apology phrase(s):
{', '.join(set(apologies_found))}

AI should be direct and confident. Consider rephrasing without apologies.
        """.strip()

        return RuleViolation(
            rule_name=self.name,
            severity=self.severity,
            message=message,
            context={
                "apology_count": len(apologies_found),
                "apologies": apologies_found,
            }
        )


# ============================================================================
# Rule 2: Citation Count
# ============================================================================

class CitationCountRule(Rule):
    """
    Count citations/references in research responses.

    For research tasks, AI should provide citations to sources.
    This rule evaluates citation density.

    Used for: Evaluating quality of research outputs.
    """

    CITATION_PATTERNS = [
        r'\[(\d+)\]',  # [1], [2] numeric citations
        r'\(https?://[^\)]+\)',  # (https://example.com)
        r'Source:',  # Explicit source labels
        r'Reference:',
    ]

    def __init__(self, min_citations: int = 3):
        """
        Args:
            min_citations: Minimum expected citations for research responses
        """
        self.min_citations = min_citations

    @property
    def name(self) -> str:
        return "citation_count"

    @property
    def description(self) -> str:
        return f"Evaluate research quality by citation count (min: {self.min_citations})"

    @property
    def severity(self) -> RuleSeverity:
        return RuleSeverity.INFO

    @property
    def applicable_contexts(self) -> List[ValidationContext]:
        return [ValidationContext.RESPONSE]

    def validate(self, input_data: ValidationInput) -> Optional[RuleViolation]:
        if not input_data.response_text:
            return None

        # Only check if response seems to be research-related
        text_lower = input_data.response_text.lower()
        is_research = any(kw in text_lower for kw in [
            "research", "analysis", "study", "source", "according to"
        ])

        if not is_research:
            return None  # Not a research response

        # Count citations
        citation_count = 0
        for pattern in self.CITATION_PATTERNS:
            matches = re.findall(pattern, input_data.response_text, re.IGNORECASE)
            citation_count += len(matches)

        if citation_count >= self.min_citations:
            return None  # Sufficient citations

        message = f"""
Evaluation: Insufficient citations in research response

Expected: {self.min_citations}+ citations
Found: {citation_count} citation(s)

Research responses should include citations to sources.
        """.strip()

        return RuleViolation(
            rule_name=self.name,
            severity=self.severity,
            message=message,
            context={
                "citation_count": citation_count,
                "min_expected": self.min_citations,
            }
        )


# ============================================================================
# Rule 3: Response Length
# ============================================================================

class ResponseLengthRule(Rule):
    """
    Evaluate response length appropriateness.

    Responses should be concise but complete. This rule flags responses
    that are too short (missing detail) or too long (verbose).

    Used for: Evaluating conciseness and completeness.
    """

    def __init__(self, min_words: int = 20, max_words: int = 500):
        """
        Args:
            min_words: Minimum expected word count
            max_words: Maximum expected word count
        """
        self.min_words = min_words
        self.max_words = max_words

    @property
    def name(self) -> str:
        return "response_length"

    @property
    def description(self) -> str:
        return f"Evaluate response length ({self.min_words}-{self.max_words} words)"

    @property
    def severity(self) -> RuleSeverity:
        return RuleSeverity.INFO

    @property
    def applicable_contexts(self) -> List[ValidationContext]:
        return [ValidationContext.RESPONSE]

    def validate(self, input_data: ValidationInput) -> Optional[RuleViolation]:
        if not input_data.response_text:
            return None

        # Count words (rough approximation)
        words = input_data.response_text.split()
        word_count = len(words)

        if self.min_words <= word_count <= self.max_words:
            return None  # Appropriate length

        if word_count < self.min_words:
            issue = "too short"
            recommendation = "Add more detail or explanation"
        else:
            issue = "too long"
            recommendation = "Consider condensing or using brevity gate"

        message = f"""
Evaluation: Response length {issue}

Word count: {word_count}
Expected range: {self.min_words}-{self.max_words}

{recommendation}
        """.strip()

        return RuleViolation(
            rule_name=self.name,
            severity=self.severity,
            message=message,
            context={
                "word_count": word_count,
                "min_expected": self.min_words,
                "max_expected": self.max_words,
            }
        )


# ============================================================================
# Rule 4: Code Block Presence
# ============================================================================

class CodeBlockPresenceRule(Rule):
    """
    Verify presence of code blocks in implementation responses.

    When user requests code, response should include properly formatted
    code blocks with syntax highlighting.

    Used for: Evaluating technical response quality.
    """

    CODE_BLOCK_PATTERN = r'```[\w]*\n[\s\S]*?\n```'

    @property
    def name(self) -> str:
        return "code_block_presence"

    @property
    def description(self) -> str:
        return "Verify code blocks in implementation responses (eval rule)"

    @property
    def severity(self) -> RuleSeverity:
        return RuleSeverity.INFO

    @property
    def applicable_contexts(self) -> List[ValidationContext]:
        return [ValidationContext.RESPONSE]

    def validate(self, input_data: ValidationInput) -> Optional[RuleViolation]:
        if not input_data.response_text:
            return None

        # Check if response is about code/implementation
        text_lower = input_data.response_text.lower()
        is_code_response = any(kw in text_lower for kw in [
            "implement", "function", "class", "code", "script",
            "def ", "const ", "let ", "function ", "class "
        ])

        if not is_code_response:
            return None  # Not a code-related response

        # Check for code blocks
        code_blocks = re.findall(self.CODE_BLOCK_PATTERN, input_data.response_text)

        if code_blocks:
            return None  # Code blocks present

        message = """
Evaluation: Missing code blocks in implementation response

Response discusses code but doesn't include formatted code blocks.

Expected: ```language
          code here
          ```

Use proper markdown code blocks with syntax highlighting.
        """.strip()

        return RuleViolation(
            rule_name=self.name,
            severity=self.severity,
            message=message,
            context={
                "code_block_count": 0,
            }
        )


# ============================================================================
# Rule 5: File Path Format
# ============================================================================

class FilePathFormatRule(Rule):
    """
    Verify file paths use absolute paths, not relative.

    File operations should use absolute paths to avoid ambiguity.

    Used for: Evaluating consistency in file operations.
    """

    @property
    def name(self) -> str:
        return "file_path_format"

    @property
    def description(self) -> str:
        return "Verify file paths are absolute, not relative (eval rule)"

    @property
    def severity(self) -> RuleSeverity:
        return RuleSeverity.INFO

    @property
    def applicable_contexts(self) -> List[ValidationContext]:
        return [ValidationContext.PRE_TOOL, ValidationContext.FILE_WRITE]

    def validate(self, input_data: ValidationInput) -> Optional[RuleViolation]:
        if not input_data.file_path:
            return None

        file_path = input_data.file_path

        if file_path.is_absolute():
            return None  # Absolute path, good

        message = f"""
Evaluation: Relative file path detected

File: {file_path}

File operations should use absolute paths to avoid ambiguity.
Convert to absolute: {file_path.resolve()}
        """.strip()

        return RuleViolation(
            rule_name=self.name,
            severity=self.severity,
            message=message,
            context={
                "file_path": str(file_path),
                "is_absolute": False,
            }
        )


# ============================================================================
# Evaluation Suite
# ============================================================================

def create_eval_suite() -> List[Rule]:
    """
    Create a suite of evaluation rules for deterministic testing.

    Returns:
        List of Rule instances configured for evaluation
    """
    return [
        NoApologiesRule(),
        CitationCountRule(min_citations=3),
        ResponseLengthRule(min_words=20, max_words=500),
        CodeBlockPresenceRule(),
        FilePathFormatRule(),
    ]


# ============================================================================
# CLI for Running Evals
# ============================================================================

def main():
    """CLI for running deterministic evaluations."""
    import argparse

    parser = argparse.ArgumentParser(description="Deterministic AI Evaluation Rules")
    parser.add_argument("command", choices=["list", "eval"],
                       help="Command to execute")
    parser.add_argument("--response", type=str,
                       help="Response text to evaluate")

    args = parser.parse_args()

    if args.command == "list":
        print("Evaluation Rules:")
        for rule in create_eval_suite():
            print(f"  - {rule.name}: {rule.description}")
        return 0

    elif args.command == "eval":
        if not args.response:
            print("Error: --response required for eval")
            return 1

        # Import engine
        from rule_engine import RuleEngine, ValidationContext, ValidationInput

        # Create engine with eval rules
        engine = RuleEngine()
        for rule in create_eval_suite():
            engine.register_rule(rule)

        # Run evaluation
        input_data = ValidationInput(
            context_type=ValidationContext.RESPONSE,
            response_text=args.response
        )

        result = engine.validate(input_data)

        # Print results
        if result.violations:
            print(result.format_violations())
        else:
            print("✅ All evaluation rules passed")

        return 0


if __name__ == "__main__":
    sys.exit(main())
