#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pyyaml",
# ]
# ///
"""
RLHF Tracker - Log positive and negative AI behavior signals

Usage:
    # Log negative behavior (punishment)
    uv run shared/tools/rlhf_tracker.py punish --description "Used pip instead of uv" --category tech-standard

    # Log positive behavior (reward)
    uv run shared/tools/rlhf_tracker.py reward --description "Batched all file reads in parallel" --category efficiency

    # List recent signals
    uv run shared/tools/rlhf_tracker.py list --type punishments --limit 10
    uv run shared/tools/rlhf_tracker.py list --type rewards --limit 10
"""

# File UUID: a7f3b2c1-4e5d-4a8f-9b0c-1d2e3f4a5b6c

import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Literal
import uuid
import yaml

# Load config
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH = REPO_ROOT / "shared" / "config.yaml"

# Setup logging (LOG-001, LOG-002, LOG-003)
LOG_DIR = REPO_ROOT / "logs" / "tools"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "rlhf_tracker.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

with open(CONFIG_PATH) as f:
    config = yaml.safe_load(f)

PUNISHMENTS_DIR = REPO_ROOT / config["rlhf"]["punishments_dir"]
REWARDS_DIR = REPO_ROOT / config["rlhf"]["rewards_dir"]


def generate_id(signal_type: Literal["punishment", "reward"]) -> tuple[str, str]:
    """Generate UUID and human-readable ID."""
    signal_uuid = uuid.uuid4().hex[:8]
    today = datetime.now().strftime("%Y%m%d")

    # Count existing files for today
    prefix = "ERR" if signal_type == "punishment" else "NICE"
    target_dir = PUNISHMENTS_DIR if signal_type == "punishment" else REWARDS_DIR

    existing = list(target_dir.glob(f"{prefix}-{today}-*.yaml"))
    sequence = len(existing) + 1

    human_id = f"{prefix}-{today}-{sequence:04d}"
    return signal_uuid, human_id


def log_punishment(
    description: str,
    category: list[str],
    context: str = "",
    root_cause: str = "",
    prevention: str = "",
) -> Path:
    """Log negative behavior signal (punishment)."""
    logger.info("Logging punishment signal")
    logger.debug("Categories: %s", category)

    signal_uuid, human_id = generate_id("punishment")
    timestamp = datetime.now().isoformat()

    data = {
        "uuid": signal_uuid,
        "id": human_id,
        "timestamp": timestamp,
        "category": category,
        "description": description,
        "context": context or "Manual log via rlhf_tracker.py",
        "root_cause": root_cause or "User-identified violation",
        "prevention": prevention or "Added to error log for pattern recognition",
        "severity": "medium",
        "status": "logged",
        "created_at": timestamp,
        "updated_at": timestamp,
    }

    PUNISHMENTS_DIR.mkdir(parents=True, exist_ok=True)
    filepath = PUNISHMENTS_DIR / f"{human_id}_{signal_uuid}.yaml"

    with open(filepath, "w") as f:
        yaml.dump(data, f, sort_keys=False, default_flow_style=False)

    logger.info("Punishment logged: %s", filepath.name)
    return filepath


def log_reward(
    description: str,
    category: str,
    pattern: str = "",
    context: str = "",
    tags: list[str] = None,
) -> Path:
    """Log positive behavior signal (reward)."""
    logger.info("Logging reward signal")
    logger.debug("Category: %s, Tags: %s", category, tags)

    signal_uuid, human_id = generate_id("reward")
    timestamp = datetime.now().isoformat()

    data = {
        "uuid": signal_uuid,
        "id": human_id,
        "timestamp": timestamp,
        "category": category,
        "description": description,
        "pattern": pattern or "Identified positive behavior",
        "context": context or "Manual log via rlhf_tracker.py",
        "tags": tags or [],
    }

    REWARDS_DIR.mkdir(parents=True, exist_ok=True)
    filepath = REWARDS_DIR / f"{human_id}_{signal_uuid}.yaml"

    with open(filepath, "w") as f:
        yaml.dump(data, f, sort_keys=False, default_flow_style=False)

    logger.info("Reward logged: %s", filepath.name)
    return filepath


def list_signals(
    signal_type: Literal["punishments", "rewards"],
    limit: int = 10,
) -> list[dict]:
    """List recent signals."""
    logger.info("Listing %s signals (limit: %d)", signal_type, limit)
    target_dir = PUNISHMENTS_DIR if signal_type == "punishments" else REWARDS_DIR

    if not target_dir.exists():
        logger.warning("Signal directory does not exist: %s", target_dir)
        return []

    files = sorted(target_dir.glob("*.yaml"), key=lambda p: p.stat().st_mtime, reverse=True)
    signals = []

    for filepath in files[:limit]:
        with open(filepath) as f:
            data = yaml.safe_load(f)
            signals.append(data)

    logger.info("Found %d signals", len(signals))
    return signals


def main():
    parser = argparse.ArgumentParser(description="RLHF Tracker - Log AI behavior signals")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Punish command
    punish_parser = subparsers.add_parser("punish", help="Log negative behavior")
    punish_parser.add_argument("--description", required=True, help="What went wrong")
    punish_parser.add_argument(
        "--category",
        required=True,
        action="append",
        help="Violation category (can be specified multiple times)",
    )
    punish_parser.add_argument("--context", default="", help="Situation context")
    punish_parser.add_argument("--root-cause", default="", help="Why it happened")
    punish_parser.add_argument("--prevention", default="", help="How to prevent")

    # Reward command
    reward_parser = subparsers.add_parser("reward", help="Log positive behavior")
    reward_parser.add_argument("--description", required=True, help="What went well")
    reward_parser.add_argument(
        "--category",
        required=True,
        choices=["ux", "efficiency", "accuracy", "proactivity", "communication", "following-rules"],
        help="Category of positive behavior",
    )
    reward_parser.add_argument("--pattern", default="", help="Reusable pattern")
    reward_parser.add_argument("--context", default="", help="Situation context")
    reward_parser.add_argument("--tags", nargs="*", default=[], help="Tags")

    # List command
    list_parser = subparsers.add_parser("list", help="List recent signals")
    list_parser.add_argument(
        "--type",
        required=True,
        choices=["punishments", "rewards"],
        help="Signal type",
    )
    list_parser.add_argument("--limit", type=int, default=10, help="Number to show")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    logger.info("Command invoked: %s", args.command)

    if args.command == "punish":
        filepath = log_punishment(
            description=args.description,
            category=args.category,
            context=args.context,
            root_cause=args.root_cause,
            prevention=args.prevention,
        )
        print(f"✅ Punishment logged: {filepath.name}")
        print(f"📁 Location: {filepath}")

    elif args.command == "reward":
        filepath = log_reward(
            description=args.description,
            category=args.category,
            pattern=args.pattern,
            context=args.context,
            tags=args.tags,
        )
        print(f"✅ Reward logged: {filepath.name}")
        print(f"📁 Location: {filepath}")

    elif args.command == "list":
        signals = list_signals(args.type, args.limit)

        if not signals:
            print(f"No {args.type} found.")
            sys.exit(0)

        print(f"\n📊 Recent {args.type.upper()} (last {len(signals)}):\n")

        for signal in signals:
            print(f"ID: {signal.get('id', 'N/A')}")
            print(f"Date: {signal.get('timestamp', 'N/A')}")

            if args.type == "punishments":
                print(f"Category: {', '.join(signal.get('category', []))}")
            else:
                print(f"Category: {signal.get('category', 'N/A')}")

            print(f"Description: {signal.get('description', 'N/A')}")
            print("-" * 60)


if __name__ == "__main__":
    main()
