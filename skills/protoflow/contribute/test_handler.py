#!/usr/bin/env python3
"""
Test the contribution workflow handler.
File UUID: 4e8f9c2d-7b3a-4f5e-9d1c-6a4e8f7b2c3e
"""

import json
import subprocess
import sys
from pathlib import Path


def test_handler():
    """Test the handler with sample arguments."""
    handler_path = Path(__file__).parent / "handler.py"

    # Test 1: No arguments (interactive mode simulation)
    print("Test 1: Interactive mode")
    print("-" * 60)
    result = subprocess.run(
        [str(handler_path)],
        capture_output=True,
        text=True
    )
    print(f"Exit code: {result.returncode}")
    print(f"Output:\n{result.stdout}")
    if result.stderr:
        print(f"Errors:\n{result.stderr}")
    print()

    # Test 2: With arguments
    print("Test 2: With arguments")
    print("-" * 60)
    args = {
        "description": "Fix S3 upload timeout",
        "type": "bug-fix",
        "issue": "1234"
    }
    result = subprocess.run(
        [str(handler_path), json.dumps(args)],
        capture_output=True,
        text=True
    )
    print(f"Exit code: {result.returncode}")
    print(f"Output:\n{result.stdout}")
    if result.stderr:
        print(f"Errors:\n{result.stderr}")

    # Parse and validate output
    try:
        output = json.loads(result.stdout)
        print("\nParsed output:")
        print(json.dumps(output, indent=2))

        if output.get("status") == "ready":
            print("\n✅ Handler test passed!")
            print(f"   Sandbox: {output['sandbox']}")
            print(f"   Branch: {output['branch']}")
        else:
            print("\n❌ Handler test failed!")
            print(f"   Error: {output.get('error')}")
    except json.JSONDecodeError as e:
        print(f"\n❌ Failed to parse output as JSON: {e}")


if __name__ == "__main__":
    test_handler()
