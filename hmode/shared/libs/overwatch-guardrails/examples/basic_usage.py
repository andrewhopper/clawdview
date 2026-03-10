#!/usr/bin/env python3
"""
Basic usage example for Overwatch Guardrails
File UUID: 4e8c9f2a-7d6b-4e3f-8a5c-9b7d4e6f2a3b
"""

from overwatch_guardrails import GuardrailEnforcer, Violation, EnforcementMode

def main():
    # Initialize enforcer with config
    enforcer = GuardrailEnforcer(".guardrails/enforcement-config.yaml")

    # Example 1: Check unapproved dependency (APPROVAL_REQUIRED)
    violation = Violation(
        rule_id="unapproved-dependency",
        message="Package 'angular' not in approved list",
        file_path="package.json",
        alternatives=["Next.js 15.x (rank 1)", "Vite + React (rank 2)", "Expo SDK 51+ (rank 3)"],
        severity="not_listed"
    )

    result = enforcer.enforce(
        rule_id="unapproved-dependency",
        violation=violation,
        context={"phase": "phase_8", "project_type": "prototype"}
    )

    print(f"Mode: {result.mode}")
    print(f"Allowed: {result.allowed}")
    print(f"Message: {result.message}")

    if result.requires_approval:
        response = input("Approve? [y/N]: ")
        if response.lower() != 'y':
            print("Blocked")
            return

    # Example 2: Check rank 2 dependency (WARN)
    violation2 = Violation(
        rule_id="suboptimal-dependency",
        message="Using Vite + React (rank 2). Preferred: Next.js 15.x",
        file_path="package.json",
        alternatives=["Next.js 15.x (rank 1)"],
        severity="rank_2_3"
    )

    result2 = enforcer.enforce(
        rule_id="suboptimal-dependency",
        violation=violation2,
        context={"phase": "phase_8"}
    )

    print(f"\nMode: {result2.mode}")
    print(f"Message: {result2.message}")
    # WARN mode: shows message but allows

if __name__ == "__main__":
    main()
