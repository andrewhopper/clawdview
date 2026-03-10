#!/usr/bin/env python3
"""
Numbered Options Rule - Enforce CLAUDE.md Section 3.4

Rule: ALL choices presented to users MUST be numbered [1], [2], [3], etc.
"""
# File UUID: f4a7b9d2-6e3c-4d8b-9f2a-3c5b7d9e4f6a

import re
from typing import List, Optional

import sys
from pathlib import Path

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
# Detection Patterns
# ============================================================================

# Patterns indicating user needs to make a choice
CHOICE_INDICATORS = [
    r"would you like to",
    r"would you like me to",
    r"should I",
    r"do you want",
    r"which (?:one|option)",
    r"what would you prefer",
    r"how would you like",
    r"select one",
    r"choose",
    r"options:",
    r"alternatives:",
    r"you can:",
]

# Pattern for properly numbered options
NUMBERED_OPTION_PATTERN = r"\[(\d+)\]\s+[A-Z]"

# Patterns that indicate this is NOT a choice situation
FALSE_POSITIVE_PATTERNS = [
    r"would you like to see",
    r"would you like more details",
    r"should I continue",
    r"should I proceed",
]


# ============================================================================
# Helper Functions
# ============================================================================

def has_choice_indicator(text: str) -> bool:
    """Check if text contains indicators that user needs to make a choice."""
    text_lower = text.lower()

    # Check for false positives first
    for pattern in FALSE_POSITIVE_PATTERNS:
        if re.search(pattern, text_lower, re.IGNORECASE):
            return False

    # Check for choice indicators
    for pattern in CHOICE_INDICATORS:
        if re.search(pattern, text_lower, re.IGNORECASE):
            return True

    return False


def has_numbered_options(text: str) -> tuple[bool, List[str]]:
    """
    Check if text has properly numbered options [1], [2], [3].

    Returns: (has_numbers, options_found)
    """
    matches = re.findall(NUMBERED_OPTION_PATTERN, text)
    options = [f"[{num}]" for num in matches]
    return len(matches) >= 2, options


def extract_last_paragraph(text: str) -> str:
    """Extract the last paragraph (where options usually appear)."""
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    return paragraphs[-1] if paragraphs else ""


# ============================================================================
# Rule Implementation
# ============================================================================

class NumberedOptionsRule(Rule):
    """
    Enforce numbered options format from CLAUDE.md Section 3.4.

    When AI presents multiple choices to the user, they MUST be formatted as:
    [1] First option
    [2] Second option
    [3] Third option

    Invalid formats:
    - Bullet points (-, *, •)
    - Parentheses (1), (2)
    - Plain numbered lists (1., 2.)
    - Letter lists (A., B.)
    """

    @property
    def name(self) -> str:
        return "numbered_options"

    @property
    def description(self) -> str:
        return "Enforce [1], [2], [3] format for multiple choice options (CLAUDE.md Section 3.4)"

    @property
    def severity(self) -> RuleSeverity:
        return RuleSeverity.WARNING  # Non-blocking by default

    @property
    def applicable_contexts(self) -> List[ValidationContext]:
        return [ValidationContext.RESPONSE]

    def validate(self, input_data: ValidationInput) -> Optional[RuleViolation]:
        """
        Validate that response uses numbered options when presenting choices.

        Args:
            input_data: Must contain response_text

        Returns:
            RuleViolation if choices present but not numbered, None if valid
        """
        if not input_data.response_text:
            return None

        response_text = input_data.response_text

        # Check if response requires numbered options
        if not has_choice_indicator(response_text):
            return None  # No choice, no violation

        # Check if response has numbered options
        has_numbers, options = has_numbered_options(response_text)

        if has_numbers:
            return None  # Valid format

        # VIOLATION: Choice indicators present but no numbered options
        last_para = extract_last_paragraph(response_text)

        message = f"""
Section 3.4 "Numbered Options" violation

ALL choices presented to users MUST be numbered.

Detected: Response contains choice indicators but no [1], [2], [3] format.

Last paragraph:
{last_para[:200]}{'...' if len(last_para) > 200 else ''}

Required format:
[1] First option - brief description
[2] Second option - brief description
[3] Third option - brief description

Reference: CLAUDE.md Section 3.4
        """.strip()

        return RuleViolation(
            rule_name=self.name,
            severity=self.severity,
            message=message,
            context={
                "last_paragraph": last_para,
                "has_choice_indicators": True,
                "has_numbered_options": False,
            }
        )
