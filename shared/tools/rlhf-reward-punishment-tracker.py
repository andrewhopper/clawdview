#!/usr/bin/env python3
"""
Error Tracking CLI Tool

Quick CLI for logging errors to RLHF punishment signals.
Automatically generates UUIDs and timestamps.

Usage:
  track-error.py new "description" [--category cat1,cat2] [--type "error_type"]
  track-error.py list [--limit N]
  track-error.py show UUID_OR_ID
"""
# File UUID: a3f8b2c1-9d4e-4f7a-8b2c-1e5a9c3d7f4b

import argparse
import uuid
import yaml
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any


def get_repo_root() -> Path:
    """Find repository root by looking for CLAUDE.md"""
    current = Path.cwd()
    while current != current.parent:
        if (current / "CLAUDE.md").exists():
            return current
        current = current.parent
    raise RuntimeError("Not in hopperlabs repository (no CLAUDE.md found)")


def get_punishments_dir() -> Path:
    """Get punishments directory from config"""
    repo_root = get_repo_root()
    return repo_root / "data" / "rlhf" / "signals" / "punishments"


def generate_error_id(punishments_dir: Path) -> str:
    """Generate next sequential error ID for today"""
    today = datetime.now().strftime("%Y%m%d")

    # Find all errors from today
    pattern = f"*{today}*.yaml"
    existing = list(punishments_dir.glob(pattern))

    # Extract sequence numbers
    sequences = []
    for file in existing:
        parts = file.stem.split("-")
        if len(parts) >= 2 and parts[0] == today:
            # Format: YYYYMMDD-descriptive-slug_uuid
            sequences.append(1)
        elif len(parts) >= 3 and parts[1] == today:
            # Format: ERR-YYYYMMDD-NNNN_uuid or BUG-YYYYMMDD-NNNN_uuid
            try:
                seq = int(parts[2].split("_")[0])
                sequences.append(seq)
            except (ValueError, IndexError):
                pass

    # Get next sequence number (default to 1 if none found)
    next_seq = max(sequences, default=0) + 1

    return f"ERR-{today}-{next_seq:04d}"


def generate_filename(description: str, error_uuid: str) -> str:
    """Generate filename from description and UUID (first 8 chars)"""
    today = datetime.now().strftime("%Y%m%d")

    # Create slug from description (lowercase, hyphens, alphanumeric only)
    slug = "".join(c if c.isalnum() or c == " " else "" for c in description.lower())
    slug = "-".join(slug.split())[:50]  # Max 50 chars

    # Use first 8 chars of UUID
    uuid_short = error_uuid[:8]

    return f"{today}-{slug}_{uuid_short}.yaml"


def create_error(
    description: str,
    categories: List[str],
    error_type: str,
    context: str = "",
    root_cause: str = "",
    artifact_urls: List[str] = None,
    prior_messages: List[str] = None
) -> Dict[str, Any]:
    """Create new error tracking entry"""
    punishments_dir = get_punishments_dir()
    punishments_dir.mkdir(parents=True, exist_ok=True)

    # Generate UUID and ID
    error_uuid = str(uuid.uuid4())
    error_id = generate_error_id(punishments_dir)
    timestamp = datetime.now().isoformat() + "Z"

    # Create error data
    error_data = {
        "id": error_id.lower().replace("-", "_"),
        "uuid": error_uuid,
        "timestamp": timestamp,
        "category": categories if categories else ["other"],
        "error_type": error_type,
        "description": description,
        "context": context or "See conversation history",
        "root_cause": root_cause or "To be analyzed",
        "prevention": "To be documented",
        "severity": "medium",
        "status": "documented",
        "prior_messages": prior_messages or [],
        "artifact_urls": artifact_urls or [],
        "notes": [],
        "created_at": timestamp,
        "updated_at": timestamp
    }

    # Generate filename and save
    filename = generate_filename(description, error_uuid)
    filepath = punishments_dir / filename

    with open(filepath, "w") as f:
        yaml.dump(error_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    return {
        "uuid": error_uuid,
        "id": error_id,
        "filepath": str(filepath),
        "filename": filename
    }


def find_error_file(identifier: str, punishments_dir: Path) -> Optional[Path]:
    """Find error file by UUID or ID"""
    # Try as UUID (check filename or file content)
    for file in punishments_dir.glob("*.yaml"):
        if identifier[:8] in file.stem or identifier in file.stem:
            return file

        # Check file content
        try:
            with open(file) as f:
                data = yaml.safe_load(f)
                if data.get("uuid") == identifier or data.get("id") == identifier:
                    return file
        except Exception:
            continue

    return None


def list_errors(limit: int = 10) -> List[Dict[str, Any]]:
    """List recent errors"""
    punishments_dir = get_punishments_dir()

    errors = []
    for file in sorted(punishments_dir.glob("*.yaml"), reverse=True)[:limit]:
        try:
            with open(file) as f:
                data = yaml.safe_load(f)
                errors.append({
                    "uuid": data.get("uuid", "N/A"),
                    "id": data.get("id", "N/A"),
                    "description": data.get("description", "")[:80],
                    "status": data.get("status", "N/A"),
                    "timestamp": data.get("timestamp", "N/A"),
                    "filename": file.name
                })
        except Exception as e:
            print(f"Warning: Could not read {file.name}: {e}", file=sys.stderr)

    return errors


def show_error(identifier: str) -> Dict[str, Any]:
    """Show full error details"""
    punishments_dir = get_punishments_dir()
    filepath = find_error_file(identifier, punishments_dir)

    if not filepath:
        raise ValueError(f"Error not found: {identifier}")

    with open(filepath) as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(
        description="Error Tracking CLI - Quick RLHF punishment signal logging",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create new error
  track-error.py new "Failed to use AWS CDK" --category tech-standard --type "Tool selection error"

  # Create with multiple categories
  track-error.py new "Coded before Phase 8" --category sdlc-violation,confirmation-protocol

  # List recent errors
  track-error.py list --limit 20

  # Show full error details
  track-error.py show a3f8b2c1
"""
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # New error command
    new_parser = subparsers.add_parser("new", help="Create new error entry")
    new_parser.add_argument("description", help="Brief error description")
    new_parser.add_argument("--category", "-c", help="Comma-separated categories (e.g., sdlc-violation,tech-standard)")
    new_parser.add_argument("--type", "-t", default="Workflow error", help="Error type classification")
    new_parser.add_argument("--context", help="Error context details")
    new_parser.add_argument("--root-cause", help="Root cause analysis")

    # List errors command
    list_parser = subparsers.add_parser("list", help="List recent errors")
    list_parser.add_argument("--limit", "-l", type=int, default=10, help="Number of errors to show")

    # Show error command
    show_parser = subparsers.add_parser("show", help="Show full error details")
    show_parser.add_argument("identifier", help="Error UUID or ID")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "new":
            categories = args.category.split(",") if args.category else []
            result = create_error(
                description=args.description,
                categories=categories,
                error_type=args.type,
                context=args.context or "",
                root_cause=args.root_cause or ""
            )
            print(f"✓ Error logged successfully")
            print(f"  UUID: {result['uuid']}")
            print(f"  ID: {result['id']}")
            print(f"  File: {result['filename']}")

        elif args.command == "list":
            errors = list_errors(limit=args.limit)
            if not errors:
                print("No errors found")
            else:
                print(f"\nRecent {len(errors)} errors:\n")
                for i, error in enumerate(errors, 1):
                    print(f"{i}. {error['id']} ({error['uuid'][:8]})")
                    print(f"   {error['description']}")
                    print(f"   Status: {error['status']} | {error['timestamp']}")
                    print()

        elif args.command == "show":
            error = show_error(args.identifier)
            print(yaml.dump(error, default_flow_style=False, sort_keys=False))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
