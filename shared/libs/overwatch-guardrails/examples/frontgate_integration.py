#!/usr/bin/env python3
"""
Example: Integrating Overwatch Guardrails into Frontgate
File UUID: 5f9d8e3a-6c7b-4e2f-9a5d-8c7b5e4f3a2c
"""

import json
import sys
from pathlib import Path
from overwatch_guardrails import GuardrailEnforcer, Violation, TechPreferenceValidator

def check_dependency_file(file_path: str, enforcer: GuardrailEnforcer) -> bool:
    """Check package.json or requirements.txt against tech preferences"""

    validator = TechPreferenceValidator(".guardrails/tech-preferences")

    if file_path.endswith("package.json"):
        with open(file_path) as f:
            data = json.load(f)

        for package in data.get("dependencies", {}):
            rank, all_options = validator.check_package(package, "frontend_frameworks")

            if rank is None:
                # Unlisted package
                violation = Violation(
                    rule_id="unapproved-dependency",
                    message=f"Package '{package}' not in approved list",
                    file_path=file_path,
                    alternatives=all_options,
                    severity="not_listed"
                )

                result = enforcer.enforce(
                    rule_id="unapproved-dependency",
                    violation=violation,
                    context=get_context()
                )

                if not result.allowed:
                    if result.requires_approval:
                        print(result.message)
                        if result.alternatives:
                            print(f"\nApproved alternatives:")
                            for alt in result.alternatives:
                                print(f"  - {alt}")

                        response = input("\nApprove this package? [y/N]: ")
                        if response.lower() != 'y':
                            return False
                    else:
                        # BLOCK mode
                        print(result.message)
                        return False

            elif rank > 1:
                # Rank 2-3: show warning
                preferred = validator.get_preferred_alternatives("frontend_frameworks", max_rank=1)
                violation = Violation(
                    rule_id="suboptimal-dependency",
                    message=f"Using '{package}' (rank {rank}). Preferred: {preferred[0]['name']}",
                    file_path=file_path,
                    alternatives=[p['name'] for p in preferred],
                    severity=f"rank_{rank}"
                )

                result = enforcer.enforce(
                    rule_id="suboptimal-dependency",
                    violation=violation,
                    context=get_context()
                )

                if result.mode.value == "warn":
                    print(f"⚠️  {result.message}")

    return True

def get_context() -> dict:
    """Build context from environment"""
    phase = read_project_phase()
    return {
        "phase": phase,
        "project_type": detect_project_type(),
        "environment": "development"
    }

def read_project_phase() -> str:
    """Read phase from .project file"""
    if Path(".project").exists():
        with open(".project") as f:
            for line in f:
                if line.startswith("phase:"):
                    return f"phase_{line.split(':')[1].strip()}"
    return "unknown"

def detect_project_type() -> str:
    """Detect project type"""
    if Path(".project").exists():
        content = Path(".project").read_text()
        if "type: spike" in content:
            return "spike"
        if "type: production" in content:
            return "production"
    return "prototype"

def main():
    """Main frontgate hook entry point"""
    if len(sys.argv) < 2:
        sys.exit(0)

    file_path = sys.argv[1]

    # Only check dependency files
    if not file_path.endswith(("package.json", "requirements.txt")):
        sys.exit(0)

    enforcer = GuardrailEnforcer(".guardrails/enforcement-config.yaml")

    if not check_dependency_file(file_path, enforcer):
        sys.exit(1)  # Block the action

    sys.exit(0)  # Allow the action

if __name__ == "__main__":
    main()
