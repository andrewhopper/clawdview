#!/usr/bin/env python3
"""Wrapper for Lambda streaming approval with auto-open in Chrome."""
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Union

LAMBDA_URL = "https://hwxtyo3untyxcpfshuvv6crlha0wikdr.lambda-url.us-east-1.on.aws"
REPO_ROOT = Path(__file__).parent.parent.parent
APPROVAL_SCRIPT = REPO_ROOT / "projects/personal/lambda-streaming-approval/iot-core/cli/approval_iot.py"


def ask_human(template: str, data: dict, timeout: int = 300, auto_open: bool = True) -> Union[dict, str]:
    """Ask human via Lambda streaming approval.

    Args:
        template: Template name (single-choice, multi-choice, approve-deny, etc.)
        data: Template data dict
        timeout: Timeout in seconds
        auto_open: Automatically open URL in Chrome

    Returns:
        Response from human (parsed from JSON if possible)
    """
    cmd = [
        "uv", "run", "--project", str(REPO_ROOT),
        "python3", str(APPROVAL_SCRIPT),
        "--url", LAMBDA_URL,
        "--template", template,
        "--data", json.dumps(data),
        "--timeout", str(timeout),
    ]

    # Run command with streaming output to catch URL and auto-open
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        url_opened = False
        output_lines = []

        # Stream output and look for URL to open
        for line in iter(process.stdout.readline, ''):
            if not line:
                break

            output_lines.append(line)
            print(line, end='')  # Print to console

            # Auto-open URL in Chrome when detected
            if auto_open and not url_opened:
                url_match = re.search(r'url:\s*(https://[^\s]+)', line)
                if url_match:
                    url = url_match.group(1)
                    subprocess.run(['open', '-a', 'Google Chrome', url], check=False)
                    url_opened = True

        process.wait()

        # Extract decision from output
        # Look for "parsed decision = " or "done, decision = " lines
        for line in output_lines:
            if 'parsed decision =' in line or 'done, decision =' in line:
                # Extract JSON after the equals sign
                parts = line.split('=', 1)
                if len(parts) == 2:
                    decision_str = parts[1].strip()
                    try:
                        return json.loads(decision_str)
                    except json.JSONDecodeError:
                        return decision_str

        # Fallback: look for the last non-log line
        for line in reversed(output_lines):
            line = line.strip()
            # Skip empty lines and log lines with timestamps
            if not line or line.startswith('['):
                continue
            # Try to parse as JSON
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                if line and not line.startswith('wait:') and not line.startswith('V2:'):
                    return line

        return "error: no response found"

    except Exception as e:
        return f"error: {e}"


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Ask human via Lambda streaming approval")
    parser.add_argument("--template", required=True, help="Template name")
    parser.add_argument("--data", required=True, help="Template data as JSON string")
    parser.add_argument("--timeout", type=int, default=300, help="Timeout in seconds")
    parser.add_argument("--no-open", action="store_true", help="Don't auto-open in Chrome")

    args = parser.parse_args()

    try:
        data = json.loads(args.data)
    except json.JSONDecodeError as e:
        print(f"error: Invalid JSON in --data: {e}", file=sys.stderr)
        sys.exit(1)

    result = ask_human(args.template, data, args.timeout, not args.no_open)
    print(json.dumps(result) if isinstance(result, dict) else result)


if __name__ == "__main__":
    main()
