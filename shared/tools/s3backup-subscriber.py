#!/usr/bin/env python3
"""S3 Backup Subscriber - Event-driven incremental backups via Overwatch

Subscribes to file change events from the Overwatch file watcher and triggers
incremental S3 backups using Merkle tree change detection.

Architecture:
    file_watcher → ZMQ (5556) → s3backup_subscriber → s3backup.py → S3

Features:
    - Debounced batching (waits for quiet period before backup)
    - Configurable batch limits
    - Integrates with Overwatch menubar (logs parsed events)
    - Falls back to scheduled backup if no events

Usage:
    python s3backup_subscriber.py                    # Use defaults
    python s3backup_subscriber.py --debounce 30     # 30s debounce
    python s3backup_subscriber.py --dry-run         # Don't actually backup

Events logged (for menubar):
    - S3BackupStarted: Starting backup of N files
    - S3BackupComplete: Backed up N files (X MB) in Ys
    - S3BackupSkipped: No changes detected
"""

import sys
import time
import logging
import argparse
import subprocess
import threading
from pathlib import Path
from datetime import datetime
from collections import deque
from typing import Optional

# Add ZeroMQ subscriber to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
TOOLS_DIR = Path(__file__).resolve().parent

# Try multiple possible ZMQ library locations
zmq_paths = [
    PROJECT_ROOT / "projects/personal/active/lib-zeromq-pubsub-python-8fff4/python",
    PROJECT_ROOT / "projects/shared/active/lib-event-publisher-aws-sns-outbox-90167/../proto-zeromq-pubsub-8fff4-001/python",
]

for zmq_path in zmq_paths:
    if zmq_path.exists():
        sys.path.insert(0, str(zmq_path))
        break

# Configure logging - format that menubar can parse
LOG_DIR = PROJECT_ROOT / "logs" / "overwatch"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "s3backup.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - s3backup - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('s3backup')


class S3BackupSubscriber:
    """Subscribes to file events and triggers incremental S3 backups."""

    def __init__(
        self,
        config_path: Optional[str] = None,
        debounce_seconds: int = 60,
        max_batch_size: int = 100,
        dry_run: bool = False,
        backup_path: Optional[str] = None,
    ):
        self.config_path = config_path or str(TOOLS_DIR / "s3backup-config.yaml")
        self.debounce_seconds = debounce_seconds
        self.max_batch_size = max_batch_size
        self.dry_run = dry_run
        self.backup_path = backup_path or str(PROJECT_ROOT)

        # Batch tracking
        self.pending_files: deque = deque(maxlen=1000)
        self.last_event_time = 0.0
        self.last_backup_time = 0.0
        self.backup_lock = threading.Lock()
        self.running = True

        # Stats
        self.total_backups = 0
        self.total_files_backed_up = 0

    def handle_file_event(self, topic: str, event) -> None:
        """Handle incoming file change events."""
        try:
            payload = event.payload
            file_path = payload.get("file_path", "")
            change_type = payload.get("change_type", "unknown")
            file_name = payload.get("file_name", "")

            # Skip backup-related files to avoid loops
            if "s3backup" in file_path or ".manifest" in file_path:
                return

            # Add to pending batch
            self.pending_files.append({
                "path": file_path,
                "name": file_name,
                "change": change_type,
                "time": time.time(),
            })
            self.last_event_time = time.time()

            logger.debug(f"📥 Queued: {change_type} {file_name}")

            # Check if we should trigger immediate backup (batch limit)
            if len(self.pending_files) >= self.max_batch_size:
                logger.info(f"📦 Batch limit reached ({self.max_batch_size} files)")
                self._trigger_backup("batch_limit")

        except Exception as e:
            logger.error(f"❌ Error handling event: {e}")

    def _trigger_backup(self, reason: str = "debounce") -> None:
        """Trigger an S3 backup."""
        with self.backup_lock:
            if not self.pending_files and reason != "scheduled":
                logger.info("⏭️  S3BackupSkipped: No changes detected")
                return

            num_files = len(self.pending_files)
            logger.info(f"📤 S3BackupStarted: {num_files} files queued ({reason})")

            start_time = time.time()

            # Build command
            cmd = [
                sys.executable,
                str(TOOLS_DIR / "s3backup.py"),
                "--config", self.config_path,
                "--path", self.backup_path,
            ]

            if self.dry_run:
                cmd.append("--dry-run")

            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=600,  # 10 minute timeout
                )

                elapsed = time.time() - start_time

                if result.returncode == 0:
                    # Parse output for stats
                    output = result.stdout
                    files_uploaded = self._parse_upload_count(output)
                    size_mb = self._parse_upload_size(output)

                    logger.info(
                        f"✅ S3BackupComplete: {files_uploaded} files "
                        f"({size_mb:.1f} MB) in {elapsed:.1f}s"
                    )

                    self.total_backups += 1
                    self.total_files_backed_up += files_uploaded
                else:
                    logger.error(f"❌ S3BackupFailed: {result.stderr[:200]}")

            except subprocess.TimeoutExpired:
                logger.error("❌ S3BackupTimeout: Backup exceeded 10 minutes")
            except Exception as e:
                logger.error(f"❌ S3BackupError: {e}")

            # Clear pending files
            self.pending_files.clear()
            self.last_backup_time = time.time()

    def _parse_upload_count(self, output: str) -> int:
        """Parse number of files uploaded from s3backup output."""
        import re
        match = re.search(r"Uploaded (\d+) files", output)
        if match:
            return int(match.group(1))
        # Fallback: count [N/M] patterns
        matches = re.findall(r"\[(\d+)/\d+\]", output)
        return len(matches) if matches else 0

    def _parse_upload_size(self, output: str) -> float:
        """Parse total size uploaded from s3backup output."""
        import re
        match = re.search(r"(\d+\.?\d*)\s*MB", output)
        return float(match.group(1)) if match else 0.0

    def debounce_checker(self) -> None:
        """Background thread that triggers backup after quiet period."""
        while self.running:
            time.sleep(5)  # Check every 5 seconds

            if not self.pending_files:
                continue

            time_since_last_event = time.time() - self.last_event_time

            if time_since_last_event >= self.debounce_seconds:
                logger.info(
                    f"⏰ Debounce triggered ({self.debounce_seconds}s quiet period)"
                )
                self._trigger_backup("debounce")

    def scheduled_backup(self, interval_hours: int = 2) -> None:
        """Background thread for scheduled backups as safety net."""
        interval_seconds = interval_hours * 3600

        while self.running:
            time.sleep(60)  # Check every minute

            time_since_backup = time.time() - self.last_backup_time

            if time_since_backup >= interval_seconds:
                logger.info(f"🕐 Scheduled backup ({interval_hours}h interval)")
                self._trigger_backup("scheduled")

    def stop(self) -> None:
        """Stop the subscriber."""
        self.running = False
        logger.info(
            f"📊 Session stats: {self.total_backups} backups, "
            f"{self.total_files_backed_up} files"
        )


def main():
    parser = argparse.ArgumentParser(
        description="S3 Backup Subscriber - Event-driven incremental backups",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--config", "-c",
        default=str(TOOLS_DIR / "s3backup-config.yaml"),
        help="Path to s3backup config file",
    )
    parser.add_argument(
        "--path", "-p",
        default=str(PROJECT_ROOT),
        help="Path to backup (default: project root)",
    )
    parser.add_argument(
        "--debounce", "-d",
        type=int,
        default=60,
        help="Debounce period in seconds (default: 60)",
    )
    parser.add_argument(
        "--batch-size", "-b",
        type=int,
        default=100,
        help="Max batch size before immediate backup (default: 100)",
    )
    parser.add_argument(
        "--schedule", "-s",
        type=int,
        default=2,
        help="Scheduled backup interval in hours (default: 2)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't actually upload to S3",
    )
    parser.add_argument(
        "--zmq-host",
        default="tcp://127.0.0.1:5555",
        help="ZMQ subscriber endpoint (default: tcp://127.0.0.1:5555)",
    )

    args = parser.parse_args()

    print("=" * 70)
    print("S3 Backup Subscriber - Event-driven Incremental Backups")
    print("=" * 70)
    print()
    print(f"Config:      {args.config}")
    print(f"Backup path: {args.path}")
    print(f"Debounce:    {args.debounce}s")
    print(f"Batch size:  {args.batch_size} files")
    print(f"Schedule:    every {args.schedule}h")
    print(f"Dry run:     {args.dry_run}")
    print(f"ZMQ:         {args.zmq_host}")
    print()
    print("=" * 70)
    print()

    # Initialize subscriber
    backup_sub = S3BackupSubscriber(
        config_path=args.config,
        debounce_seconds=args.debounce,
        max_batch_size=args.batch_size,
        dry_run=args.dry_run,
        backup_path=args.path,
    )

    # Start background threads
    debounce_thread = threading.Thread(
        target=backup_sub.debounce_checker,
        daemon=True,
        name="debounce-checker",
    )
    debounce_thread.start()

    schedule_thread = threading.Thread(
        target=lambda: backup_sub.scheduled_backup(args.schedule),
        daemon=True,
        name="scheduled-backup",
    )
    schedule_thread.start()

    # Connect to ZMQ
    try:
        from subscriber import Subscriber
        from events import DomainEvent

        logger.info(f"📡 Connecting to ZMQ at {args.zmq_host}...")
        subscriber = Subscriber(args.zmq_host, subscriber_name="s3backup")
        subscriber.subscribe("file-events")

        logger.info("✅ S3 Backup Subscriber started!")
        logger.info("   Listening for file change events...")
        logger.info("   Press Ctrl+C to stop")
        logger.info("")

        # Start listening
        subscriber.listen(backup_sub.handle_file_event)

    except ImportError as e:
        logger.error(f"❌ ZMQ library not found: {e}")
        logger.error("   Falling back to scheduled-only mode")
        logger.info("   Will backup every {args.schedule} hours")

        # Run in scheduled-only mode
        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            pass

    except KeyboardInterrupt:
        logger.info("\n🛑 Stopping S3 Backup Subscriber...")
        backup_sub.stop()
        logger.info("✅ Stopped")


if __name__ == "__main__":
    main()
