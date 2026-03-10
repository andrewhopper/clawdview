#!/usr/bin/env python3
"""
Grace Period Validator

Detects file creation but waits before reminding, checking for evidence
that the action was taken (e.g., S3 publish).

Usage:
  python3 grace_period_validator.py watch <file> --timeout 30
  python3 grace_period_validator.py check <file>
"""

import argparse
import json
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# ============================================================================
# Configuration
# ============================================================================

def get_hostname():
    """Get normalized hostname for machine-specific files"""
    import socket
    hostname = socket.gethostname()
    # Normalize: remove .local, hyphens, dots
    return hostname.replace('.local', '').replace('-', '').replace('.', '')

REPO_ROOT = Path(__file__).parent.parent.parent
HOSTNAME = get_hostname()
PENDING_FILE = REPO_ROOT / ".guardrails" / ".pending_validations.json"
LOG_FILE = REPO_ROOT / ".guardrails" / f".supervisor-{HOSTNAME}.log"

PUBLISHABLE_EXTENSIONS = {".html", ".pdf", ".svg", ".zip", ".mp3", ".mp4"}
DEFAULT_TIMEOUT = 30  # seconds


# ============================================================================
# Data Models
# ============================================================================

@dataclass
class PendingValidation:
    """File waiting for validation after grace period"""
    file_path: str
    created_at: str
    validation_type: str  # "s3_publish", "shared_model", etc.
    timeout_seconds: int
    check_after: str  # ISO timestamp


# ============================================================================
# Evidence Checkers
# ============================================================================

class EvidenceChecker:
    """Base class for checking if action was taken"""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.repo_root = REPO_ROOT

    def has_evidence(self) -> bool:
        """Check if evidence exists"""
        raise NotImplementedError


class S3PublishEvidenceChecker(EvidenceChecker):
    """Check if file was published to S3"""

    def has_evidence(self) -> bool:
        """Check multiple sources for S3 publish evidence"""

        # 1. Check for skip markers
        skip_markers = [".s3-skip", ".no-publish", f"{self.file_path.name}.s3-published"]
        for marker in skip_markers:
            if (self.file_path.parent / marker).exists():
                log(f"Evidence: Skip marker found for {self.file_path.name}")
                return True

        # 2. Check for bookmark file
        bookmarks_dir = self.repo_root / "bookmarks"
        if bookmarks_dir.exists():
            bookmark = bookmarks_dir / f"{self.file_path.stem}.url"
            if bookmark.exists():
                log(f"Evidence: Bookmark found for {self.file_path.name}")
                return True

        # 3. Check git history (recent commits)
        if self._check_git_history():
            log(f"Evidence: Git commit mentions S3 publish for {self.file_path.name}")
            return True

        # 4. Check Claude Code execution log
        if self._check_claude_execution_log():
            log(f"Evidence: Claude execution log shows S3 publish for {self.file_path.name}")
            return True

        # 5. Check bash history
        if self._check_bash_history():
            log(f"Evidence: Bash history shows S3 publish for {self.file_path.name}")
            return True

        log(f"No evidence found for {self.file_path.name}")
        return False

    def _check_git_history(self) -> bool:
        """Check git commits for S3 publish"""
        try:
            # Check last 5 commits
            result = subprocess.run(
                ["git", "log", "-5", "--oneline", "--all"],
                cwd=self.repo_root,
                capture_output=True,
                text=True
            )

            # Look for S3 publish mentions
            if result.returncode == 0:
                log_text = result.stdout.lower()
                filename_lower = self.file_path.name.lower()

                # Check if commit mentions both "s3" and filename
                if "s3" in log_text and filename_lower in log_text:
                    return True

                # Check for "publish" and filename
                if "publish" in log_text and filename_lower in log_text:
                    return True

        except Exception as e:
            log(f"Git history check failed: {e}")

        return False

    def _check_claude_execution_log(self) -> bool:
        """Check Claude Code execution logs"""

        # Check common log locations
        log_locations = [
            self.repo_root / ".claude" / "execution.log",
            self.repo_root / ".claude" / "session.log",
            Path.home() / ".claude" / "logs" / "execution.log",
        ]

        filename = self.file_path.name

        for log_path in log_locations:
            if not log_path.exists():
                continue

            try:
                # Read last 1000 lines (recent activity)
                with open(log_path) as f:
                    lines = f.readlines()[-1000:]
                    log_text = "".join(lines).lower()

                # Look for S3 publish script execution
                if "s3_publish" in log_text and filename.lower() in log_text:
                    return True

                # Look for bash command execution
                if "bash" in log_text and "s3" in log_text and filename.lower() in log_text:
                    return True

            except Exception as e:
                log(f"Failed to read {log_path}: {e}")

        return False

    def _check_bash_history(self) -> bool:
        """Check bash history for S3 publish commands"""

        # Check supervisor log (if it logged bash commands)
        if LOG_FILE.exists():
            try:
                with open(LOG_FILE) as f:
                    lines = f.readlines()[-100:]  # Last 100 lines
                    log_text = "".join(lines).lower()

                filename_lower = self.file_path.name.lower()

                if "s3_publish" in log_text and filename_lower in log_text:
                    return True

            except Exception:
                pass

        return False


# ============================================================================
# Grace Period Manager
# ============================================================================

class GracePeriodManager:
    """Manages pending validations with grace periods"""

    def __init__(self):
        self.pending_file = PENDING_FILE

    def add_pending(self, file_path: Path, validation_type: str, timeout: int = DEFAULT_TIMEOUT):
        """Add file to pending validations"""

        pending = self._load_pending()

        check_after = datetime.now() + timedelta(seconds=timeout)

        validation = PendingValidation(
            file_path=str(file_path),
            created_at=datetime.now().isoformat(),
            validation_type=validation_type,
            timeout_seconds=timeout,
            check_after=check_after.isoformat()
        )

        pending.append(validation.__dict__)
        self._save_pending(pending)

        log(f"Added pending validation: {file_path.name} (check after {timeout}s)")

    def check_due(self) -> List[Dict]:
        """Check for validations that are due"""

        pending = self._load_pending()
        now = datetime.now()

        due = []
        remaining = []

        for item in pending:
            check_after = datetime.fromisoformat(item["check_after"])

            if now >= check_after:
                # Grace period expired
                due.append(item)
            else:
                # Still waiting
                remaining.append(item)

        # Save remaining validations
        self._save_pending(remaining)

        return due

    def _load_pending(self) -> List[Dict]:
        """Load pending validations"""
        if not self.pending_file.exists():
            return []

        try:
            with open(self.pending_file) as f:
                return json.load(f)
        except Exception:
            return []

    def _save_pending(self, pending: List[Dict]):
        """Save pending validations"""
        self.pending_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.pending_file, 'w') as f:
            json.dump(pending, f, indent=2)


# ============================================================================
# Grace Period Validator
# ============================================================================

class GracePeriodValidator:
    """Main validator with grace period"""

    def __init__(self):
        self.manager = GracePeriodManager()

    def watch_file(self, file_path: Path, timeout: int = DEFAULT_TIMEOUT):
        """Start watching file with grace period"""

        # Determine validation type
        if file_path.suffix in PUBLISHABLE_EXTENSIONS:
            validation_type = "s3_publish"
        elif file_path.suffix == ".ts":
            validation_type = "shared_model"
        else:
            log(f"No validation needed for {file_path.name}")
            return

        # Add to pending validations
        self.manager.add_pending(file_path, validation_type, timeout)

        log(f"Watching {file_path.name} for {timeout} seconds...")

    def check_due_validations(self) -> List[str]:
        """Check validations where grace period has expired"""

        due = self.manager.check_due()
        reminders = []

        for item in due:
            file_path = Path(item["file_path"])
            validation_type = item["validation_type"]

            log(f"Grace period expired for {file_path.name}, checking evidence...")

            # Check if action was taken
            has_evidence = False

            if validation_type == "s3_publish":
                checker = S3PublishEvidenceChecker(file_path)
                has_evidence = checker.has_evidence()

            if not has_evidence:
                # No evidence found, create reminder
                reminder = self._create_reminder(file_path, validation_type)
                reminders.append(reminder)
                log(f"Reminder created for {file_path.name}")
            else:
                log(f"Evidence found, no reminder needed for {file_path.name}")

        return reminders

    def _create_reminder(self, file_path: Path, validation_type: str) -> str:
        """Create reminder text"""

        if validation_type == "s3_publish":
            return (
                f"⚠️ REMINDER: File '{file_path.name}' was created {DEFAULT_TIMEOUT} seconds ago "
                f"but not published to S3.\n"
                f"Prompt user: 'Publish {file_path.name} to S3? [1] Public [2] Temp [3] Private [4] Skip'"
            )
        elif validation_type == "shared_model":
            return (
                f"⚠️ REMINDER: File '{file_path.name}' may have local types that exist in shared domains.\n"
                f"Check shared/semantic/domains/registry.yaml"
            )
        else:
            return f"⚠️ REMINDER: Validation needed for {file_path.name}"


# ============================================================================
# Utilities
# ============================================================================

def log(message: str):
    """Write to log file"""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] [GracePeriod] {message}\n")


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Grace period validator")
    parser.add_argument("command", choices=["watch", "check"], help="Command")
    parser.add_argument("file", nargs="?", type=Path, help="File to watch")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="Timeout in seconds")

    args = parser.parse_args()

    validator = GracePeriodValidator()

    if args.command == "watch":
        if not args.file:
            print("Error: file argument required")
            return 1

        validator.watch_file(args.file, args.timeout)
        print(f"⏱️  Watching {args.file.name} for {args.timeout} seconds...")

    elif args.command == "check":
        reminders = validator.check_due_validations()

        if reminders:
            print("🤖 GRACE PERIOD EXPIRED - REMINDERS:")
            for reminder in reminders:
                print(f"\n{reminder}")
        else:
            print("✅ No reminders needed")

    return 0


if __name__ == "__main__":
    sys.exit(main())
