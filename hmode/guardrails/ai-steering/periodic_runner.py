#!/usr/bin/env python3
"""
Periodic Validation Runner

Tracks turns and runs validation every N turns.
Integrates with Claude Code hooks and git workflow.

State is stored in .guardrails/.validation_state.json

Usage:
  python3 periodic_runner.py increment      # Increment turn counter
  python3 periodic_runner.py check          # Check if validation should run
  python3 periodic_runner.py run            # Run validation now
  python3 periodic_runner.py reset          # Reset turn counter
  python3 periodic_runner.py status         # Show current state
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
import subprocess

# ============================================================================
# Configuration
# ============================================================================

REPO_ROOT = Path(__file__).parent.parent.parent
STATE_FILE = REPO_ROOT / ".guardrails" / ".validation_state.json"
CONFIG_FILE = REPO_ROOT / ".guardrails" / "ai-steering" / "validate_periodic_config.yaml"
VALIDATOR_SCRIPT = REPO_ROOT / ".guardrails" / "ai-steering" / "validate_periodic.py"


# ============================================================================
# State Management
# ============================================================================

class ValidationState:
    """Manages validation state"""

    def __init__(self):
        self.state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        """Load state from JSON file"""
        if not STATE_FILE.exists():
            return {
                "turn_count": 0,
                "last_validation": None,
                "last_validation_result": None,
                "total_validations": 0,
                "total_violations": 0
            }

        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except Exception:
            return self._load_state.__defaults__[0]

    def _save_state(self):
        """Save state to JSON file"""
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, 'w') as f:
            json.dump(self.state, f, indent=2)

    def increment_turn(self) -> int:
        """Increment turn counter"""
        self.state["turn_count"] = self.state.get("turn_count", 0) + 1
        self._save_state()
        return self.state["turn_count"]

    def reset_turn_counter(self):
        """Reset turn counter to 0"""
        self.state["turn_count"] = 0
        self._save_state()

    def should_validate(self, frequency: int) -> bool:
        """Check if validation should run"""
        return self.state.get("turn_count", 0) % frequency == 0

    def record_validation(self, result: Dict[str, Any]):
        """Record validation execution"""
        self.state["last_validation"] = datetime.now().isoformat()
        self.state["last_validation_result"] = result
        self.state["total_validations"] = self.state.get("total_validations", 0) + 1
        self.state["total_violations"] = self.state.get("total_violations", 0) + result.get("violations", 0)
        self.reset_turn_counter()
        self._save_state()

    def get_status(self) -> Dict[str, Any]:
        """Get current state"""
        return self.state


# ============================================================================
# Configuration Management
# ============================================================================

def load_config() -> Dict[str, Any]:
    """Load configuration from YAML file"""
    if not CONFIG_FILE.exists():
        # Default config
        return {
            "frequency": {"turns": 5},
            "strictness": {"level": "moderate", "failOnErrors": True, "failOnWarnings": False},
            "output": {"format": "stylish"}
        }

    try:
        import yaml
        with open(CONFIG_FILE) as f:
            return yaml.safe_load(f)
    except ImportError:
        # Fallback: basic parsing
        with open(CONFIG_FILE) as f:
            content = f.read()
            # Extract turns frequency (simple regex)
            import re
            match = re.search(r'turns:\s*(\d+)', content)
            turns = int(match.group(1)) if match else 5
            return {"frequency": {"turns": turns}}


# ============================================================================
# Validation Runner
# ============================================================================

def run_validation(config: Dict[str, Any]) -> Dict[str, Any]:
    """Execute validation script"""
    try:
        # Build command
        cmd = ["python3", str(VALIDATOR_SCRIPT)]

        # Add flags based on config
        strictness = config.get("strictness", {})
        if strictness.get("failOnWarnings"):
            cmd.append("--strict")

        output = config.get("output", {})
        if output.get("format") == "json":
            cmd.append("--json")

        # Run validation
        result = subprocess.run(
            cmd,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True
        )

        # Parse result
        violations = 0
        warnings = 0
        errors = 0

        if output.get("format") == "json":
            try:
                data = json.loads(result.stdout)
                violations = len(data.get("violations", []))
                warnings = data.get("warnings", 0)
                errors = data.get("errors", 0)
            except Exception:
                pass

        return {
            "exit_code": result.returncode,
            "violations": violations,
            "warnings": warnings,
            "errors": errors,
            "output": result.stdout,
            "success": result.returncode == 0
        }

    except Exception as e:
        return {
            "exit_code": 1,
            "violations": 0,
            "warnings": 0,
            "errors": 1,
            "output": f"Validation failed: {str(e)}",
            "success": False
        }


# ============================================================================
# CLI Commands
# ============================================================================

def cmd_increment(state: ValidationState, config: Dict[str, Any]):
    """Increment turn counter"""
    turn = state.increment_turn()
    frequency = config.get("frequency", {}).get("turns", 5)

    print(f"Turn {turn}/{frequency}")

    if state.should_validate(frequency):
        print("⏰ Validation due - running check...")
        return cmd_run(state, config)

    return 0


def cmd_check(state: ValidationState, config: Dict[str, Any]):
    """Check if validation should run"""
    frequency = config.get("frequency", {}).get("turns", 5)
    should_run = state.should_validate(frequency)

    turn = state.state.get("turn_count", 0)
    print(f"Turn: {turn}/{frequency}")
    print(f"Validation due: {'Yes' if should_run else 'No'}")

    return 0 if should_run else 1


def cmd_run(state: ValidationState, config: Dict[str, Any]):
    """Run validation now"""
    print("🔍 Running guardrail validation...")

    result = run_validation(config)

    # Print output
    print(result["output"])

    # Record result
    state.record_validation({
        "violations": result["violations"],
        "warnings": result["warnings"],
        "errors": result["errors"]
    })

    # Summary
    if result["success"]:
        print("\n✅ All guardrails validated successfully")
    else:
        print(f"\n❌ Validation failed: {result['errors']} errors, {result['warnings']} warnings")

    return result["exit_code"]


def cmd_reset(state: ValidationState):
    """Reset turn counter"""
    state.reset_turn_counter()
    print("✅ Turn counter reset to 0")
    return 0


def cmd_status(state: ValidationState, config: Dict[str, Any]):
    """Show current status"""
    status = state.get_status()
    frequency = config.get("frequency", {}).get("turns", 5)

    print("Validation Status")
    print("=" * 50)
    print(f"Turn count:        {status.get('turn_count', 0)}/{frequency}")
    print(f"Last validation:   {status.get('last_validation', 'Never')}")
    print(f"Total validations: {status.get('total_validations', 0)}")
    print(f"Total violations:  {status.get('total_violations', 0)}")

    last_result = status.get("last_validation_result")
    if last_result:
        print(f"\nLast Result:")
        print(f"  Violations: {last_result.get('violations', 0)}")
        print(f"  Warnings:   {last_result.get('warnings', 0)}")
        print(f"  Errors:     {last_result.get('errors', 0)}")

    return 0


# ============================================================================
# Main CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Periodic validation runner")
    parser.add_argument("command", choices=["increment", "check", "run", "reset", "status"],
                       help="Command to execute")

    args = parser.parse_args()

    # Load state and config
    state = ValidationState()
    config = load_config()

    # Execute command
    if args.command == "increment":
        return cmd_increment(state, config)
    elif args.command == "check":
        return cmd_check(state, config)
    elif args.command == "run":
        return cmd_run(state, config)
    elif args.command == "reset":
        return cmd_reset(state)
    elif args.command == "status":
        return cmd_status(state, config)


if __name__ == "__main__":
    sys.exit(main())
