#!/usr/bin/env python3
# File UUID: 6c4e8a2f-9b3d-4f1e-8a5c-7d2e0f4b6a9c
"""
project-file — Unified CLI for reading and writing .project files.

Replaces bespoke YAML/JSON parsing scattered across 40+ tools.
Handles both YAML and JSON .project formats transparently.

Usage:
    project-file get <path> <field>              Read a field
    project-file set <path> <field> <value>      Set a field (creates file if missing)
    project-file set <path> <field> --json <val> Set a structured field (array/object)
    project-file batch-set <path> k=v k=v ...    Set multiple fields in one read-write
    project-file init <path> [--field=val ...]   Create a new .project file
    project-file dump <path>                     Dump entire file as JSON
    project-file exists <path>                   Exit 0 if .project exists, 1 otherwise
    project-file validate <path>                 Validate against schema

Examples (from bash scripts):
    name=$(project-file get ./my-project name)
    project-file set ./my-project status GRADUATED
    project-file set ./my-project tech_stack --json '["Next.js","TypeScript"]'
    project-file set ./my-project repository https://github.com/owner/repo
    project-file init ./my-project --name=foo --classification=personal --phase=8
"""

import sys
import os
import json
import argparse
import uuid as uuid_lib
from datetime import datetime, timezone
from pathlib import Path

# Try PyYAML first, fall back to basic parser
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


# ─────────────────────────────────────────────
# File I/O — handles both YAML and JSON
# ─────────────────────────────────────────────

def _detect_format(content: str) -> str:
    """Detect if content is JSON or YAML."""
    stripped = content.lstrip()
    if stripped.startswith("{"):
        return "json"
    return "yaml"


def read_project(project_path: str) -> dict:
    """Read a .project file, auto-detecting JSON or YAML format."""
    pfile = _resolve_path(project_path)
    if not pfile.exists():
        return {}

    content = pfile.read_text(encoding="utf-8")
    if not content.strip():
        return {}

    fmt = _detect_format(content)

    if fmt == "json":
        return json.loads(content)

    if HAS_YAML:
        return yaml.safe_load(content) or {}

    # Fallback: simple line-based YAML parser (handles flat key: value only)
    return _parse_yaml_fallback(content)


def write_project(project_path: str, data: dict) -> None:
    """Write a .project file in YAML format (preferred)."""
    pfile = _resolve_path(project_path)
    pfile.parent.mkdir(parents=True, exist_ok=True)

    # Preserve File UUID comment if present
    file_uuid_line = ""
    if pfile.exists():
        existing = pfile.read_text(encoding="utf-8")
        for line in existing.splitlines():
            if line.startswith("# File UUID:"):
                file_uuid_line = line + "\n"
                break

    if HAS_YAML:
        # Custom representer to avoid YAML anchors and get clean output
        class CleanDumper(yaml.SafeDumper):
            pass

        def str_representer(dumper, data):
            if "\n" in data:
                return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
            return dumper.represent_scalar("tag:yaml.org,2002:str", data)

        CleanDumper.add_representer(str, str_representer)

        yaml_str = yaml.dump(
            data,
            Dumper=CleanDumper,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
        )
        pfile.write_text(file_uuid_line + yaml_str, encoding="utf-8")
    else:
        # Fallback: write simple YAML manually
        lines = [file_uuid_line] if file_uuid_line else []
        for key, value in data.items():
            if isinstance(value, list):
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f"  - {item}")
            elif isinstance(value, dict):
                lines.append(f"{key}:")
                for k, v in value.items():
                    lines.append(f"  {k}: {_yaml_quote(v)}")
            else:
                lines.append(f"{key}: {_yaml_quote(value)}")
        pfile.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _resolve_path(project_path: str) -> Path:
    """Resolve to the .project file, whether given a dir or file path."""
    p = Path(project_path)
    if p.is_dir():
        return p / ".project"
    if p.name == ".project":
        return p
    # Assume it's a directory that doesn't exist yet
    return p / ".project"


def _try_int(s: str):
    """Try to parse a string as an integer (handles negatives). Returns int or original string."""
    try:
        return int(s)
    except ValueError:
        return s


def _yaml_quote(value) -> str:
    """Quote a value for YAML output if needed."""
    if value is None:
        return '""'
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    s = str(value)
    # Quote if contains special chars; escape internal double quotes
    if any(c in s for c in ":{}[]#&*!|>'\"%@`"):
        return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'
    return s


def _parse_yaml_fallback(content: str) -> dict:
    """Minimal YAML parser for flat key: value files. No PyYAML needed."""
    data = {}
    current_list_key = None

    for line in content.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # List item
        if stripped.startswith("- ") and current_list_key:
            val = stripped[2:].strip().strip('"').strip("'")
            data[current_list_key].append(val)
            continue

        # Key: value
        if ":" in stripped:
            key, _, val = stripped.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")

            if not val:
                # Could be a list or nested object — treat as empty list for now
                data[key] = []
                current_list_key = key
            else:
                # Parse common types
                if val.lower() == "true":
                    data[key] = True
                elif val.lower() == "false":
                    data[key] = False
                else:
                    parsed = _try_int(val)
                    data[key] = parsed
                    current_list_key = None

    return data


# ─────────────────────────────────────────────
# Commands
# ─────────────────────────────────────────────

def cmd_get(args):
    """Read a single field from .project."""
    data = read_project(args.path)
    if not data:
        sys.exit(1)

    # Support dotted paths: graduation.github_repo
    value = data
    for part in args.field.split("."):
        if isinstance(value, dict) and part in value:
            value = value[part]
        else:
            sys.exit(1)  # Field not found — silent exit with code 1

    # Output
    if isinstance(value, (list, dict)):
        print(json.dumps(value))
    elif isinstance(value, bool):
        print("true" if value else "false")
    else:
        print(value)


def cmd_set(args):
    """Set a field in .project (creates file if needed)."""
    data = read_project(args.path)

    # Parse value
    if args.json_value is not None:
        value = json.loads(args.json_value)
    elif args.value.lower() == "true":
        value = True
    elif args.value.lower() == "false":
        value = False
    else:
        parsed = _try_int(args.value)
        value = parsed

    # Support dotted paths for setting nested fields
    parts = args.field.split(".")
    target = data
    for part in parts[:-1]:
        if part not in target or not isinstance(target[part], dict):
            target[part] = {}
        target = target[part]
    target[parts[-1]] = value

    # Auto-update updated_at / updated
    ts_field = "updated_at" if "updated_at" in data else "updated"
    if args.field not in (ts_field,):
        data[ts_field] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    write_project(args.path, data)


def cmd_init(args):
    """Create a new .project file with required fields."""
    pfile = _resolve_path(args.path)
    if pfile.exists() and not args.force:
        print(f"Error: {pfile} already exists. Use --force to overwrite.", file=sys.stderr)
        sys.exit(1)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    new_uuid = str(uuid_lib.uuid4())

    data = {
        "id": args.name or Path(args.path).name,
        "name": args.name or Path(args.path).name,
        "description": "",
        "type": "prototype",
        "classification": "personal",
        "phase": 8,
        "status": "active",
        "created": now,
        "updated": now,
    }

    # Apply --field=value overrides
    if args.fields:
        for field_spec in args.fields:
            if "=" in field_spec:
                key, _, val = field_spec.partition("=")
                key = key.lstrip("-")
                if val.lower() in ("true", "false"):
                    data[key] = val.lower() == "true"
                else:
                    parsed = _try_int(val)
                    data[key] = parsed

    # Seed the UUID comment line so write_project preserves it
    pfile.parent.mkdir(parents=True, exist_ok=True)
    pfile.write_text(f"# File UUID: {new_uuid}\n", encoding="utf-8")

    # Delegate to write_project (single serialization path)
    write_project(args.path, data)
    print(pfile)


def cmd_dump(args):
    """Dump entire .project as JSON."""
    data = read_project(args.path)
    if not data:
        sys.exit(1)
    print(json.dumps(data, indent=2, default=str))


def cmd_exists(args):
    """Check if .project file exists. Exit 0=yes, 1=no."""
    pfile = _resolve_path(args.path)
    sys.exit(0 if pfile.exists() else 1)


def cmd_validate(args):
    """Validate .project against schema (basic checks)."""
    data = read_project(args.path)
    if not data:
        print("Error: file not found or empty", file=sys.stderr)
        sys.exit(1)

    errors = []
    warnings = []

    # Check required fields (accept common aliases)
    required_one_of = [
        (["id"], "id"),
        (["name"], "name"),
        (["status"], "status"),  # warning only — many old projects lack this
        (["phase", "current_phase"], "phase or current_phase"),
    ]
    for fields, label in required_one_of:
        if not any(f in data for f in fields):
            if label == "status":
                warnings.append(f"Missing recommended field: {label}")
            else:
                errors.append(f"Missing required field: {label}")

    # Type checks
    phase_val = data.get("phase") or data.get("current_phase")
    if phase_val is not None and not isinstance(phase_val, (int, str)):
        errors.append(f"phase must be int or string, got {type(phase_val).__name__}")

    # List fields
    for list_field in ["tech_stack", "tags"]:
        if list_field in data and not isinstance(data[list_field], list):
            errors.append(f"{list_field} must be a list, got {type(data[list_field]).__name__}")
    # stack can be list or dict (key-value tech map)
    if "stack" in data and not isinstance(data["stack"], (list, dict)):
        errors.append(f"stack must be a list or dict, got {type(data['stack']).__name__}")

    # Classification check (accept both classification and category)
    valid_classifications = {"personal", "work", "shared", "oss", "unspecified", "archive"}
    class_val = data.get("classification") or data.get("category")
    if class_val and class_val not in valid_classifications:
        errors.append(f"Invalid classification: {class_val} (expected one of {valid_classifications})")

    for w in warnings:
        print(f"  ⚠ {w}", file=sys.stderr)

    if errors:
        for e in errors:
            print(f"  ✗ {e}", file=sys.stderr)
        sys.exit(1)
    else:
        print("  ✓ Valid")


def cmd_batch_set(args):
    """Set multiple fields in one read-write cycle (avoids N+1 process forks)."""
    data = read_project(args.path)

    for pair in args.pairs:
        if "=" not in pair:
            print(f"Error: invalid pair (expected key=value): {pair}", file=sys.stderr)
            sys.exit(1)
        key, _, raw_val = pair.partition("=")

        # Try --json-style structured value
        if raw_val.startswith("[") or raw_val.startswith("{"):
            try:
                value = json.loads(raw_val)
            except json.JSONDecodeError:
                value = raw_val
        elif raw_val.lower() == "true":
            value = True
        elif raw_val.lower() == "false":
            value = False
        else:
            value = _try_int(raw_val)

        # Support dotted paths
        parts = key.split(".")
        target = data
        for part in parts[:-1]:
            if part not in target or not isinstance(target[part], dict):
                target[part] = {}
            target = target[part]
        target[parts[-1]] = value

    # Single timestamp update
    ts_field = "updated_at" if "updated_at" in data else "updated"
    data[ts_field] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    write_project(args.path, data)


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="project-file",
        description="Unified CLI for .project file operations",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # get
    p_get = sub.add_parser("get", help="Read a field value")
    p_get.add_argument("path", help="Project directory or .project file path")
    p_get.add_argument("field", help="Field name (supports dotted paths: graduation.github_repo)")

    # set
    p_set = sub.add_parser("set", help="Set a field value")
    p_set.add_argument("path", help="Project directory or .project file path")
    p_set.add_argument("field", help="Field name (supports dotted paths)")
    p_set.add_argument("value", nargs="?", default="", help="Value to set")
    p_set.add_argument("--json", dest="json_value", help="JSON value for arrays/objects")

    # init
    p_init = sub.add_parser("init", help="Create a new .project file")
    p_init.add_argument("path", help="Project directory")
    p_init.add_argument("--name", help="Project name")
    p_init.add_argument("--force", action="store_true", help="Overwrite existing file")
    # Additional field=value or --field=value args are captured via parse_known_args

    # dump
    p_dump = sub.add_parser("dump", help="Dump entire file as JSON")
    p_dump.add_argument("path", help="Project directory or .project file path")

    # exists
    p_exists = sub.add_parser("exists", help="Check if .project exists (exit code)")
    p_exists.add_argument("path", help="Project directory or .project file path")

    # validate
    p_validate = sub.add_parser("validate", help="Validate against schema")
    p_validate.add_argument("path", help="Project directory or .project file path")

    # batch-set
    p_batch = sub.add_parser("batch-set", help="Set multiple fields in one read-write cycle")
    p_batch.add_argument("path", help="Project directory or .project file path")
    p_batch.add_argument("pairs", nargs="+", help="key=value pairs (supports dotted paths, JSON arrays/objects)")

    args, remaining = parser.parse_known_args()

    # Pass remaining key=value args to init command
    if args.command == "init":
        args.fields = remaining
    elif remaining:
        parser.error(f"unrecognized arguments: {' '.join(remaining)}")

    commands = {
        "get": cmd_get,
        "set": cmd_set,
        "batch-set": cmd_batch_set,
        "init": cmd_init,
        "dump": cmd_dump,
        "exists": cmd_exists,
        "validate": cmd_validate,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
