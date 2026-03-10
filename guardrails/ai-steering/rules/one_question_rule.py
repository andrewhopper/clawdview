#!/usr/bin/env python3
"""
One Question Rule - Enforce CLAUDE.md Section 3.2

Rule: NEVER batch multiple questions. Ask ONE, wait for response, then next.
"""
# File UUID: b8d4f6a2-7c3e-4d9b-9f2a-3c5b7d9e4f1a

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
# Detection Patterns
# ============================================================================

# Question ending patterns
QUESTION_PATTERNS = [
    r'\?',  # Question mark
    r'(?:should|would|could|can|do) (?:you|I)',  # Modal questions
    r'(?:what|when|where|why|how|which|who)',  # Wh- questions
]


# ============================================================================
# Helper Functions
# ============================================================================

def count_questions(text: str) -> tuple[int, List[str]]:
    """
    Count the number of questions in text.

    Returns: (count, question_samples)
    """
    # Split into sentences (rough approximation)
    sentences = re.split(r'[.!?]+', text)
    questions = []

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        # Check if sentence is a question
        is_question = False

        # Check for question mark
        if '?' in sentence:
            is_question = True

        # Check for question patterns
        for pattern in QUESTION_PATTERNS:
            if re.search(pattern, sentence, re.IGNORECASE):
                is_question = True
                break

        if is_question:
            questions.append(sentence[:100])  # Sample first 100 chars

    return len(questions), questions


def extract_questions(text: str) -> List[str]:
    """Extract all questions from text."""
    _, questions = count_questions(text)
    return questions


# ============================================================================
# Rule Implementation
# ============================================================================

class OneQuestionRule(Rule):
    """
    Enforce "One Question at a Time" from CLAUDE.md Section 3.2.

    AI should ask ONE question, wait for user response, then ask next.
    Batching multiple questions in a single response is prohibited.

    Valid:
    - "Which deployment strategy would you prefer?"
    - "Should I proceed with Phase 8?"

    Invalid:
    - "Which strategy? Also, what's your timeline? And do you need CI/CD?"
    - Multiple questions in sequence without waiting for answer

    Note: Numbered options (e.g., [1], [2], [3]) count as ONE question.
    """

    @property
    def name(self) -> str:
        return "one_question"

    @property
    def description(self) -> str:
        return "Enforce one question at a time (CLAUDE.md Section 3.2)"

    @property
    def severity(self) -> RuleSeverity:
        return RuleSeverity.WARNING  # Non-blocking by default

    @property
    def applicable_contexts(self) -> List[ValidationContext]:
        return [ValidationContext.RESPONSE]

    def validate(self, input_data: ValidationInput) -> Optional[RuleViolation]:
        """
        Validate that response contains at most one question.

        Args:
            input_data: Must contain response_text

        Returns:
            RuleViolation if multiple questions detected, None if valid
        """
        if not input_data.response_text:
            return None

        response_text = input_data.response_text

        # Count questions
        question_count, questions = count_questions(response_text)

        # Allow 0 or 1 question
        if question_count <= 1:
            return None

        # VIOLATION: Multiple questions detected
        message = f"""
Section 3.2 "One Question at a Time" violation

NEVER batch multiple questions. Ask ONE, wait for response, then next.

Detected: {question_count} questions in a single response.

Questions found:
"""
        for i, q in enumerate(questions[:5], 1):  # Show max 5
            message += f"\n{i}. {q}{'...' if len(q) >= 100 else ''}"

        if question_count > 5:
            message += f"\n... and {question_count - 5} more"

        message += """

Recommended:
- Ask the most important question first
- Wait for user response
- Then ask follow-up questions based on answer

Reference: CLAUDE.md Section 3.2
        """.strip()

        return RuleViolation(
            rule_name=self.name,
            severity=self.severity,
            message=message,
            context={
                "question_count": question_count,
                "questions": questions,
            }
        )
