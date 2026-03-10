#!/usr/bin/env python3
"""
Response Format Validator - Enforce Communication Standards

Validates AI responses against CLAUDE.md Section 3.4 "Numbered Options".
ALL choices presented to users MUST be numbered [1], [2], [3], etc.

Usage:
    # Check if response follows numbered list rule
    python3 response_format_validator.py check "<response_text>"

    # Interactive mode - paste response
    python3 response_format_validator.py check

Exit codes:
    0 = Valid (numbered lists present when needed)
    1 = Invalid (missing numbered lists for choices)
"""
# File UUID: a8f2b9c4-3d7e-4f6a-9c1d-2e5f8b4c7d9e

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Tuple, List

# ============================================================================
# Configuration
# ============================================================================

REPO_ROOT = Path(__file__).parent.parent.parent

def get_hostname():
    """Get normalized hostname for machine-specific files"""
    import socket
    hostname = socket.gethostname()
    return hostname.replace('.local', '').replace('-', '').replace('.', '')

HOSTNAME = get_hostname()
LOG_FILE = REPO_ROOT / ".guardrails" / f".response_validator-{HOSTNAME}.log"

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
NUMBERED_OPTION_PATTERN = r"\[(\d+)\]\s+[A-Z]"  # [1] Option, [2] Another

# Patterns that indicate this is NOT a choice situation
FALSE_POSITIVE_PATTERNS = [
    r"would you like to see",  # Followed by single yes/no
    r"would you like more details",
    r"should I continue",
    r"should I proceed",
]


# ============================================================================
# Logging
# ============================================================================

def log(message: str):
    """Write to log file."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")


# ============================================================================
# Validation Logic
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


def has_numbered_options(text: str) -> Tuple[bool, List[str]]:
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


def validate_response(response_text: str) -> Tuple[bool, str]:
    """
    Validate response follows numbered list rule.

    Returns: (is_valid, message)
    """
    # Check if response requires numbered options
    if not has_choice_indicator(response_text):
        log("No choice indicators found - validation passed")
        return True, ""

    # Check if response has numbered options
    has_numbers, options = has_numbered_options(response_text)

    if has_numbers:
        log(f"Numbered options found: {options}")
        return True, ""

    # VIOLATION: Choice indicators present but no numbered options
    log("VIOLATION: Choice indicators without numbered options")

    # Extract context for error message
    last_para = extract_last_paragraph(response_text)

    message = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  COMMUNICATION STANDARD VIOLATION

Rule: Section 3.4 "Numbered Options"
ALL choices presented to users MUST be numbered.

Detected: Response contains choice indicators but no [1], [2], [3] format.

Last paragraph:
{last_para[:200]}...

Required format:
[1] First option - brief description
[2] Second option - brief description
[3] Third option - brief description

Reference: CLAUDE.md Section 3.4
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    return False, message.strip()


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Response Format Validator")
    parser.add_argument("command", choices=["check"],
                       help="Command to execute")
    parser.add_argument("text", nargs="?",
                       help="Response text to check (or read from stdin)")

    args = parser.parse_args()

    if args.command == "check":
        # Get response text
        if args.text:
            response_text = args.text
        else:
            # Read from stdin
            response_text = sys.stdin.read()

        # Validate
        is_valid, message = validate_response(response_text)

        if not is_valid:
            print(message)
            return 1

        return 0


if __name__ == "__main__":
    sys.exit(main())
