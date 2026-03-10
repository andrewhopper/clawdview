#!/usr/bin/env python3
"""
Batch Operation Detector

Handles bulk file generation intelligently:
1. Pre-flight declaration: AI declares intent to generate N files
2. Auto-detection: Detects rapid file creation (batch mode)
3. Batch validation: Checks all files together after batch completes

Usage:
  # Pre-flight declaration
  python3 batch_detector.py declare --count 100 --type html

  # Check if batch is active
  python3 batch_detector.py check

  # Complete batch (triggers validation)
  python3 batch_detector.py complete

  # Auto-detect from file creation rate
  python3 batch_detector.py track <file>
"""

import argparse
import json
import sys
import time
from dataclasses import dataclass, field
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
BATCH_STATE_FILE = REPO_ROOT / ".guardrails" / ".batch_operation.json"
LOG_FILE = REPO_ROOT / ".guardrails" / f".supervisor-{HOSTNAME}.log"

# Auto-detection thresholds
RAPID_CREATION_THRESHOLD = 3  # 3+ files in 10 seconds = batch mode
RAPID_CREATION_WINDOW = 10  # seconds
BATCH_IDLE_TIMEOUT = 30  # No files for 30s = batch complete


# ============================================================================
# Data Models
# ============================================================================

@dataclass
class BatchOperation:
    """Batch operation state"""
    active: bool
    declared: bool  # Was it pre-declared by AI?
    auto_detected: bool  # Auto-detected from rapid creation?
    file_type: str  # "html", "pdf", etc.
    expected_count: Optional[int]
    actual_count: int
    files: List[str] = field(default_factory=list)
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_file_at: str = field(default_factory=lambda: datetime.now().isoformat())


# ============================================================================
# Batch Detector
# ============================================================================

class BatchDetector:
    """Detects and manages batch operations"""

    def __init__(self):
        self.state_file = BATCH_STATE_FILE

    def declare_batch(self, count: int, file_type: str):
        """Pre-flight: AI declares intent to generate batch"""

        batch = BatchOperation(
            active=True,
            declared=True,
            auto_detected=False,
            file_type=file_type,
            expected_count=count,
            actual_count=0
        )

        self._save_state(batch)
        log(f"Batch declared: {count} {file_type} files")

        return {
            "status": "batch_active",
            "message": f"✅ Batch mode active: Expecting {count} {file_type} files. Grace periods paused."
        }

    def track_file(self, file_path: Path):
        """Track file creation, auto-detect batch mode"""

        state = self._load_state()

        if not state:
            # No batch active, check if we should auto-detect
            state = self._check_auto_detect(file_path)
        else:
            # Batch already active, add to tracking
            state.files.append(str(file_path))
            state.actual_count += 1
            state.last_file_at = datetime.now().isoformat()

            self._save_state(state)
            log(f"Batch tracking: {state.actual_count}/{state.expected_count or '?'} files")

        return state

    def _check_auto_detect(self, file_path: Path) -> Optional[BatchOperation]:
        """Auto-detect batch mode from rapid file creation"""

        # Load recent file creation history
        history = self._get_recent_files()
        history.append({
            "file": str(file_path),
            "timestamp": datetime.now().isoformat()
        })

        # Keep only files from last RAPID_CREATION_WINDOW seconds
        cutoff = datetime.now() - timedelta(seconds=RAPID_CREATION_WINDOW)
        recent = [
            f for f in history
            if datetime.fromisoformat(f["timestamp"]) > cutoff
        ]

        # Save updated history
        self._save_file_history(recent)

        # Check if rapid creation (threshold met)
        if len(recent) >= RAPID_CREATION_THRESHOLD:
            # Auto-enable batch mode!
            log(f"Auto-detected batch: {len(recent)} files in {RAPID_CREATION_WINDOW}s")

            batch = BatchOperation(
                active=True,
                declared=False,
                auto_detected=True,
                file_type=file_path.suffix.lstrip('.'),
                expected_count=None,
                actual_count=len(recent),
                files=[f["file"] for f in recent]
            )

            self._save_state(batch)

            return batch

        return None

    def check_active(self) -> Dict:
        """Check if batch is active"""

        state = self._load_state()

        if not state:
            return {"active": False}

        # Check if batch timed out (no files for BATCH_IDLE_TIMEOUT)
        last_file_time = datetime.fromisoformat(state.last_file_at)
        idle_time = (datetime.now() - last_file_time).total_seconds()

        if idle_time > BATCH_IDLE_TIMEOUT:
            log(f"Batch idle timeout: {idle_time}s since last file")
            return self.complete_batch()

        return {
            "active": True,
            "declared": state.declared,
            "auto_detected": state.auto_detected,
            "expected_count": state.expected_count,
            "actual_count": state.actual_count,
            "idle_seconds": int(idle_time)
        }

    def complete_batch(self) -> Dict:
        """Mark batch as complete and trigger validation"""

        state = self._load_state()

        if not state:
            return {"status": "no_batch"}

        log(f"Batch complete: {state.actual_count} files")

        # Trigger validation for all files in batch
        result = {
            "status": "batch_complete",
            "files": state.files,
            "count": state.actual_count,
            "expected": state.expected_count,
            "message": self._generate_completion_message(state)
        }

        # Clear batch state
        self._clear_state()

        return result

    def _generate_completion_message(self, state: BatchOperation) -> str:
        """Generate message for batch completion"""

        if state.declared:
            return (
                f"✅ Batch generation complete: {state.actual_count} {state.file_type} files created.\n"
                f"Would you like to publish all files to S3?\n"
                f"  [1] Publish all (bulk operation)\n"
                f"  [2] Skip all\n"
                f"  [3] Select individually"
            )
        elif state.auto_detected:
            return (
                f"📦 Detected bulk file creation: {state.actual_count} {state.file_type} files.\n"
                f"Publish all to S3?\n"
                f"  [1] Yes (bulk)\n"
                f"  [2] No"
            )
        else:
            return f"Batch complete: {state.actual_count} files"

    def _load_state(self) -> Optional[BatchOperation]:
        """Load batch state"""
        if not self.state_file.exists():
            return None

        try:
            with open(self.state_file) as f:
                data = json.load(f)
                return BatchOperation(**data)
        except Exception:
            return None

    def _save_state(self, state: BatchOperation):
        """Save batch state"""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump(state.__dict__, f, indent=2)

    def _clear_state(self):
        """Clear batch state"""
        if self.state_file.exists():
            self.state_file.unlink()

    def _get_recent_files(self) -> List[Dict]:
        """Get recent file creation history"""
        history_file = self.state_file.parent / f".file_history-{HOSTNAME}.json"

        if not history_file.exists():
            return []

        try:
            with open(history_file) as f:
                return json.load(f)
        except Exception:
            return []

    def _save_file_history(self, history: List[Dict]):
        """Save file creation history"""
        history_file = self.state_file.parent / f".file_history-{HOSTNAME}.json"
        history_file.parent.mkdir(parents=True, exist_ok=True)

        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)


# ============================================================================
# Utilities
# ============================================================================

def log(message: str):
    """Write to log file"""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] [BatchDetector] {message}\n")


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Batch operation detector")
    parser.add_argument("command", choices=["declare", "track", "check", "complete"],
                       help="Command to execute")
    parser.add_argument("file", nargs="?", type=Path, help="File to track")
    parser.add_argument("--count", type=int, help="Expected file count")
    parser.add_argument("--type", help="File type (html, pdf, etc.)")

    args = parser.parse_args()

    detector = BatchDetector()

    if args.command == "declare":
        if not args.count or not args.type:
            print("Error: --count and --type required for declare")
            return 1

        result = detector.declare_batch(args.count, args.type)
        print(result["message"])

    elif args.command == "track":
        if not args.file:
            print("Error: file argument required")
            return 1

        state = detector.track_file(args.file)

        if state and state.active:
            if state.declared:
                print(f"📦 Batch mode active: {state.actual_count}/{state.expected_count} files")
            elif state.auto_detected:
                print(f"📦 Auto-detected batch: {state.actual_count} files")

    elif args.command == "check":
        result = detector.check_active()

        if result.get("active"):
            print(f"📦 Batch active: {result['actual_count']} files")
            if result.get("declared"):
                print(f"   Expected: {result['expected_count']}")
            print(f"   Idle: {result['idle_seconds']}s")
        else:
            print("No batch active")

    elif args.command == "complete":
        result = detector.complete_batch()

        if result.get("status") == "batch_complete":
            print(result["message"])
        else:
            print("No batch to complete")

    return 0


if __name__ == "__main__":
    sys.exit(main())
