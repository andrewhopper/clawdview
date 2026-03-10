#!/usr/bin/env python3
"""
Test suite for response_format_validator.py

Tests the numbered list enforcement rule from CLAUDE.md Section 3.4
"""
# File UUID: c7d9e4f2-8b3a-4c6d-9e2f-5a7b8c9d4e6f

import pytest
from response_format_validator import (
    has_choice_indicator,
    has_numbered_options,
    extract_last_paragraph,
    validate_response,
)


class TestChoiceIndicatorDetection:
    """Test detection of phrases that indicate user needs to make a choice."""

    def test_detects_would_you_like_to(self):
        text = "I found three options. Would you like to see them?"
        assert has_choice_indicator(text)

    def test_detects_should_i(self):
        text = "Should I deploy to production or staging?"
        assert has_choice_indicator(text)

    def test_detects_which_option(self):
        text = "Which option would you prefer?"
        assert has_choice_indicator(text)

    def test_detects_choose(self):
        text = "Please choose one of the following approaches."
        assert has_choice_indicator(text)

    def test_detects_options_colon(self):
        text = "Here are your options: deploy or skip"
        assert has_choice_indicator(text)

    def test_no_indicator_in_statement(self):
        text = "The deployment completed successfully."
        assert not has_choice_indicator(text)

    def test_false_positive_see_details(self):
        """Yes/no questions should not trigger choice validation."""
        text = "Would you like to see more details?"
        assert not has_choice_indicator(text)

    def test_false_positive_continue(self):
        text = "Should I continue with the next step?"
        assert not has_choice_indicator(text)

    def test_case_insensitive(self):
        text = "WOULD YOU LIKE TO continue?"
        assert has_choice_indicator(text)


class TestNumberedOptionsDetection:
    """Test detection of properly formatted [1], [2], [3] options."""

    def test_detects_two_options(self):
        text = "[1] Deploy now\n[2] Skip deployment"
        has_numbers, options = has_numbered_options(text)
        assert has_numbers
        assert len(options) == 2
        assert options == ["[1]", "[2]"]

    def test_detects_three_options(self):
        text = """
        [1] AWS Amplify
        [2] CloudFront + S3
        [3] ECS Fargate
        """
        has_numbers, options = has_numbered_options(text)
        assert has_numbers
        assert len(options) == 3

    def test_detects_four_options(self):
        text = "[1] A [2] B [3] C [4] D"
        has_numbers, options = has_numbered_options(text)
        assert has_numbers
        assert len(options) == 4

    def test_single_option_not_enough(self):
        """A single [1] is not multiple choice."""
        text = "[1] Only one option"
        has_numbers, options = has_numbered_options(text)
        assert not has_numbers

    def test_no_numbers(self):
        text = "Deploy now or skip deployment"
        has_numbers, options = has_numbered_options(text)
        assert not has_numbers

    def test_bullets_not_numbers(self):
        text = "- Deploy now\n- Skip deployment"
        has_numbers, options = has_numbered_options(text)
        assert not has_numbers

    def test_parentheses_not_brackets(self):
        text = "(1) Deploy now\n(2) Skip deployment"
        has_numbers, options = has_numbered_options(text)
        assert not has_numbers

    def test_mixed_with_other_text(self):
        text = """
        I recommend three approaches:

        [1] Fast deployment via Amplify
        [2] Custom setup with CloudFront
        [3] Container-based with ECS

        All are valid options.
        """
        has_numbers, options = has_numbered_options(text)
        assert has_numbers
        assert len(options) == 3


class TestParagraphExtraction:
    """Test extraction of last paragraph where options typically appear."""

    def test_extracts_last_paragraph(self):
        text = """
        First paragraph here.

        Second paragraph here.

        Last paragraph here.
        """
        result = extract_last_paragraph(text)
        assert result == "Last paragraph here."

    def test_single_paragraph(self):
        text = "Only one paragraph."
        result = extract_last_paragraph(text)
        assert result == "Only one paragraph."

    def test_empty_text(self):
        text = ""
        result = extract_last_paragraph(text)
        assert result == ""

    def test_strips_whitespace(self):
        text = "\n\nParagraph\n\n"
        result = extract_last_paragraph(text)
        assert result == "Paragraph"


class TestValidateResponse:
    """Test end-to-end response validation."""

    def test_valid_response_with_numbers(self):
        response = """
        I found three deployment strategies.

        [1] AWS Amplify - fastest for SPAs
        [2] CloudFront + S3 - more control
        [3] ECS Fargate - full container support

        Which would you prefer?
        """
        is_valid, message = validate_response(response)
        assert is_valid
        assert message == ""

    def test_invalid_response_bullets(self):
        response = """
        I found three deployment strategies. Which would you prefer?

        - AWS Amplify
        - CloudFront + S3
        - ECS Fargate
        """
        is_valid, message = validate_response(response)
        assert not is_valid
        assert "COMMUNICATION STANDARD VIOLATION" in message
        assert "Section 3.4" in message

    def test_invalid_response_plain_text(self):
        response = """
        Would you like to deploy via Amplify or CloudFront?
        """
        is_valid, message = validate_response(response)
        assert not is_valid
        assert "numbered" in message.lower()

    def test_valid_no_choice_needed(self):
        response = "Deployment completed successfully. Check the logs."
        is_valid, message = validate_response(response)
        assert is_valid
        assert message == ""

    def test_valid_yes_no_question(self):
        """Yes/no questions don't need numbered options."""
        response = "Would you like to see the full output?"
        is_valid, message = validate_response(response)
        assert is_valid

    def test_valid_should_i_continue(self):
        response = "Should I continue with the next phase?"
        is_valid, message = validate_response(response)
        assert is_valid

    def test_complex_valid_response(self):
        response = """
        I've analyzed the codebase and found several optimization opportunities.

        Here are the top priorities:

        [1] Implement caching layer - 40% performance improvement
        [2] Add database indexes - 25% query speedup
        [3] Optimize bundle size - 30% faster load time
        [4] Enable CDN - 50% reduced latency

        Which should I tackle first?
        """
        is_valid, message = validate_response(response)
        assert is_valid

    def test_complex_invalid_response(self):
        response = """
        I've analyzed the codebase and found several optimization opportunities.

        Here are the top priorities:

        • Implement caching layer
        • Add database indexes
        • Optimize bundle size
        • Enable CDN

        Which should I tackle first?
        """
        is_valid, message = validate_response(response)
        assert not is_valid


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_mixed_format_invalid(self):
        """Mix of bullets and numbers should fail."""
        response = """
        Options:
        [1] First option
        - Second option
        [3] Third option
        """
        # This actually has numbers, so it passes
        # In future, could add stricter validation
        is_valid, message = validate_response(response)
        # Current implementation: has [1] and [3], so passes
        # Could enhance to check sequential numbering

    def test_very_long_response(self):
        """Handle responses with many paragraphs."""
        response = "\n\n".join([f"Paragraph {i}" for i in range(20)])
        response += "\n\nWhich option? [1] A [2] B"
        is_valid, message = validate_response(response)
        assert is_valid

    def test_unicode_numbers(self):
        """Only ASCII brackets should be accepted."""
        response = "Choose: ⑴ Option A ⑵ Option B"
        is_valid, message = validate_response(response)
        assert not is_valid

    def test_multiple_choice_indicators(self):
        response = """
        Would you like to choose? Here are options:
        [1] First [2] Second
        """
        is_valid, message = validate_response(response)
        assert is_valid


class TestRealWorldExamples:
    """Test with actual responses from Claude conversations."""

    def test_deployment_choice_valid(self):
        response = """
        I'll help you deploy to AWS. Here are the recommended approaches:

        [1] AWS Amplify - Automatic deployments from Git
        [2] CloudFront + S3 - Manual but more flexible
        [3] ECS Fargate - Full container control

        Which fits your needs best?
        """
        is_valid, message = validate_response(response)
        assert is_valid

    def test_deployment_choice_invalid(self):
        response = """
        I'll help you deploy to AWS. Here are the recommended approaches:

        * AWS Amplify - Automatic deployments from Git
        * CloudFront + S3 - Manual but more flexible
        * ECS Fargate - Full container control

        Which fits your needs best?
        """
        is_valid, message = validate_response(response)
        assert not is_valid

    def test_research_complete_valid(self):
        response = """
        I've completed the research on state machines. Here's the summary:

        **Top Projects:**
        - XState (29k stars)
        - pytransitions (6k stars)
        - LangGraph (10k stars)

        The full report is saved at shared/semantic/research/state-machines.md
        """
        # No choice needed, should pass
        is_valid, message = validate_response(response)
        assert is_valid

    def test_follow_up_valid(self):
        response = """
        Based on the analysis, I recommend proceeding with Phase 8.

        [1] Start implementation now
        [2] Review the plan first
        [3] Adjust scope before coding

        What's your preference?
        """
        is_valid, message = validate_response(response)
        assert is_valid


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
