#!/usr/bin/env python3
"""
Verify Domain Usage Skill - Python Implementation

File UUID: 5f9e2b4a-7c3d-4e1f-a8b6-3d1e9c2f6a8b
"""

import sys
import subprocess
from pathlib import Path


def main():
    """Execute the domain usage verification script."""
    # Get the monorepo root (where shared/ exists)
    skill_dir = Path(__file__).resolve().parent
    repo_root = skill_dir.parent.parent.parent

    # Path to the verification script
    script_path = repo_root / "shared" / "tools" / "verify-domain-usage.py"

    if not script_path.exists():
        print(f"Error: Script not found at {script_path}", file=sys.stderr)
        return 1

    # Execute the script with all arguments passed through
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)] + sys.argv[1:],
            check=False
        )
        return result.returncode
    except Exception as e:
        print(f"Error executing script: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
