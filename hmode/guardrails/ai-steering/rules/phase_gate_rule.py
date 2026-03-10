#!/usr/bin/env python3
"""
Phase Gate Rule - Enforce SDLC phase restrictions

Rule: NO code files until Phase 8 (Implementation)
"""
# File UUID: a6c9d3e4-7b2f-4d8c-9f1a-3c5b7d9e4f2a

import subprocess
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
# Configuration
# ============================================================================

REPO_ROOT = Path(__file__).parent.parent.parent.parent
PHASE_CHECKER = REPO_ROOT / ".guardrails" / "ai-steering" / "phase_checker.py"

MINIMUM_CODE_PHASE = 8


# ============================================================================
# Rule Implementation
# ============================================================================

class PhaseGateRule(Rule):
    """
    Enforce SDLC phase gate for code file writes.

    Blocks writes to code files (*.py, *.ts, *.js, etc.) unless:
    - Project is in Phase 8+ (Implementation)
    - OR declared as SPIKE mode (throwaway prototype)
    - OR no .project file exists (edge case)

    Non-code files (config, docs, data) are always allowed.
    """

    @property
    def name(self) -> str:
        return "phase_gate"

    @property
    def description(self) -> str:
        return "Enforce Phase 8+ requirement for code file writes (SDLC gate)"

    @property
    def severity(self) -> RuleSeverity:
        return RuleSeverity.BLOCKER  # Blocks execution

    @property
    def applicable_contexts(self) -> List[ValidationContext]:
        return [
            ValidationContext.FILE_WRITE,
            ValidationContext.PRE_TOOL,
        ]

    def validate(self, input_data: ValidationInput) -> Optional[RuleViolation]:
        """
        Validate that code file writes are only in Phase 8+.

        Args:
            input_data: Must contain file_path

        Returns:
            RuleViolation if phase < 8 and file is code, None if allowed
        """
        if not input_data.file_path:
            return None

        file_path = input_data.file_path

        # Call phase_checker.py via subprocess
        try:
            result = subprocess.run(
                ["uv", "run", "python", str(PHASE_CHECKER), "check", str(file_path)],
                capture_output=True,
                text=True,
                timeout=5,
                cwd=REPO_ROOT
            )

            if result.returncode != 0:
                # Phase gate blocked
                message = result.stdout + result.stderr

                return RuleViolation(
                    rule_name=self.name,
                    severity=self.severity,
                    message=message,
                    context={
                        "file_path": str(file_path),
                        "checker_output": message,
                    }
                )

            # Allowed
            return None

        except subprocess.TimeoutExpired:
            # Allow on timeout (don't block work)
            return None

        except Exception as e:
            # Allow on error (don't block work)
            # But log warning
            return RuleViolation(
                rule_name=self.name,
                severity=RuleSeverity.WARNING,
                message=f"Phase gate check failed: {e}",
                context={
                    "file_path": str(file_path),
                    "error": str(e),
                }
            )
