#!/usr/bin/env python3
"""
Phase Checker - SDLC Phase Gate Enforcement

Blocks code file writes if project is not in Phase 8+ (IMPLEMENTATION).

This enforces the "NO CODE BEFORE PHASE 8" rule from the SDLC process.

Usage:
    # Check if file write is allowed
    python3 phase_checker.py check /path/to/file.ts

    # Check status of current directory's project
    python3 phase_checker.py status

Exit codes:
    0 = Allowed (Phase 8+, non-code file, or no .project)
    1 = Blocked (Phase < 8 and code file)
"""
# File UUID: 7c3d8f91-2e4a-4b7f-9c2d-1e5a8b3c7d9f

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

try:
    import yaml
except ImportError:
    # Fallback for environments without PyYAML
    yaml = None

# ============================================================================
# Configuration
# ============================================================================

REPO_ROOT = Path(__file__).parent.parent.parent

def get_hostname():
    """Get normalized hostname for machine-specific files"""
    import socket
    hostname = socket.gethostname()
    return hostname.replace('.local', '').replace('-', '').replace('.', '')

HOSTNAME = get_hostname()
LOG_FILE = REPO_ROOT / ".guardrails" / f".phase_checker-{HOSTNAME}.log"

# Code file extensions that require Phase 8+
CODE_EXTENSIONS = {
    # Python
    ".py", ".pyi", ".pyx",
    # JavaScript/TypeScript
    ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs",
    # Systems languages
    ".c", ".h", ".cpp", ".hpp", ".cc", ".hh", ".cxx",
    ".rs", ".go",
    # JVM
    ".java", ".kt", ".kts", ".scala", ".clj",
    # .NET
    ".cs", ".fs", ".vb",
    # Ruby/PHP
    ".rb", ".php",
    # Swift/Objective-C
    ".swift", ".m", ".mm",
    # Scripting
    ".sh", ".bash", ".zsh", ".fish", ".ps1",
    ".pl", ".pm",  # Perl
    ".lua",
    # Other
    ".zig", ".nim", ".v", ".odin",
    ".ex", ".exs",  # Elixir
    ".erl", ".hrl",  # Erlang
    ".hs", ".lhs",  # Haskell
    ".ml", ".mli",  # OCaml
    ".r", ".R",  # R
    ".jl",  # Julia
    ".dart",
    ".vue", ".svelte",  # Framework-specific
}

# Files always allowed (config, docs, data)
ALWAYS_ALLOWED_EXTENSIONS = {
    ".md", ".mdx", ".txt", ".rst",
    ".yaml", ".yml", ".json", ".toml", ".ini", ".cfg",
    ".env", ".env.local", ".env.example",
    ".gitignore", ".dockerignore", ".prettierrc", ".eslintrc",
    ".css", ".scss", ".sass", ".less",
    ".html", ".htm",  # Usually templates/static
    ".svg", ".png", ".jpg", ".jpeg", ".gif", ".ico", ".webp",
    ".lock",  # Lock files
    ".log",
}

# Special filenames always allowed
ALWAYS_ALLOWED_FILENAMES = {
    "Makefile", "Dockerfile", "Containerfile",
    ".project", ".gitignore", ".dockerignore",
    "package.json", "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    "requirements.txt", "pyproject.toml", "setup.py", "setup.cfg",
    "Cargo.toml", "Cargo.lock",
    "go.mod", "go.sum",
    "tsconfig.json", "jsconfig.json",
    ".env", ".env.local", ".env.example",
    "README.md", "LICENSE", "CHANGELOG.md",
    "CLAUDE.md", ".cursorrules", ".clinerules",
}

# Phase required for code files
MINIMUM_CODE_PHASE = 8


# ============================================================================
# Logging
# ============================================================================

def log(message: str):
    """Write to log file."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")


# ============================================================================
# Project Detection
# ============================================================================

def find_project_file(file_path: Path) -> Optional[Path]:
    """
    Find .project file by walking up from file location.

    Returns the first .project file found, or None.
    """
    # Start from the file's directory
    current = file_path.parent if file_path.is_file() else file_path

    # Don't search above repo root
    while current >= REPO_ROOT:
        project_file = current / ".project"
        if project_file.exists():
            return project_file

        parent = current.parent
        if parent == current:
            break
        current = parent

    return None


def parse_project_file(project_file: Path) -> Tuple[Optional[float], Optional[str], Optional[str]]:
    """
    Parse .project file and extract phase info.

    Returns: (phase_number, phase_name, project_name)
    """
    if yaml is None:
        # Fallback: simple line parsing
        try:
            content = project_file.read_text()
            phase = None
            phase_name = None
            project_name = None

            for line in content.splitlines():
                if line.startswith("phase:"):
                    try:
                        phase = float(line.split(":", 1)[1].strip())
                    except ValueError:
                        pass
                elif line.startswith("phase_name:"):
                    phase_name = line.split(":", 1)[1].strip().strip('"\'')
                elif line.startswith("name:"):
                    project_name = line.split(":", 1)[1].strip().strip('"\'')

            return phase, phase_name, project_name
        except Exception as e:
            log(f"Error parsing .project (fallback): {e}")
            return None, None, None

    try:
        with open(project_file) as f:
            data = yaml.safe_load(f)

        phase = data.get("phase")
        if isinstance(phase, str):
            try:
                phase = float(phase)
            except ValueError:
                phase = None

        phase_name = data.get("phase_name")
        project_name = data.get("name") or data.get("id")

        return phase, phase_name, project_name
    except Exception as e:
        log(f"Error parsing .project: {e}")
        return None, None, None


# ============================================================================
# File Classification
# ============================================================================

def is_code_file(file_path: Path) -> bool:
    """
    Determine if a file is a code file that requires Phase 8+.

    Returns True if file is code, False if config/docs/data.
    """
    filename = file_path.name
    suffix = file_path.suffix.lower()

    # Check filename exemptions first
    if filename in ALWAYS_ALLOWED_FILENAMES:
        return False

    # Check extension exemptions
    if suffix in ALWAYS_ALLOWED_EXTENSIONS:
        return False

    # Check if it's a code extension
    if suffix in CODE_EXTENSIONS:
        return True

    # Default: not code (allow by default for unknown types)
    return False


# ============================================================================
# Phase Validation
# ============================================================================

def check_phase_gate(file_path: Path) -> Tuple[bool, str]:
    """
    Check if file write is allowed based on project phase.

    Returns: (allowed, message)
    """
    file_path = Path(file_path).resolve()

    # Always allow non-code files
    if not is_code_file(file_path):
        log(f"ALLOW (non-code): {file_path}")
        return True, ""

    # Find project file
    project_file = find_project_file(file_path)

    if not project_file:
        # No .project file - this is an edge case
        # Could be a quick task or untracked work
        log(f"ALLOW (no .project): {file_path}")
        return True, ""

    # Parse phase
    phase, phase_name, project_name = parse_project_file(project_file)

    if phase is None:
        log(f"ALLOW (no phase field): {file_path}")
        return True, ""

    # Check phase gate
    if phase >= MINIMUM_CODE_PHASE:
        log(f"ALLOW (Phase {phase}): {file_path}")
        return True, ""

    # BLOCKED - Phase < 8
    log(f"BLOCKED (Phase {phase}): {file_path}")

    message = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⛔ PHASE GATE: Code file blocked

Project: {project_name or 'Unknown'}
Current Phase: {phase} ({phase_name or 'Unknown'})
Required Phase: 8+ (IMPLEMENTATION)
File: {file_path.name}

Cannot write code in Phase {int(phase)}.
The 9-phase SDLC requires planning/design before code.

Options:
  [1] Continue Phase {int(phase)} activities ({phase_name})
  [2] Advance to Phase 8 (update .project file)
  [3] Declare SPIKE mode (throwaway prototype, max 3 days)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    return False, message.strip()


def get_project_status() -> str:
    """Get status of current directory's project."""
    project_file = find_project_file(Path.cwd())

    if not project_file:
        return "No .project file found in current directory or parents."

    phase, phase_name, project_name = parse_project_file(project_file)

    phase_display = phase if phase is not None else "undefined"
    phase_name_display = phase_name or "Unknown"
    project_display = project_name or "Unknown"

    code_allowed = "✅ Yes" if (phase is not None and phase >= MINIMUM_CODE_PHASE) else "❌ No (requires Phase 8+)"

    return f"""
Project: {project_display}
Phase: {phase_display} ({phase_name_display})
Code Writing: {code_allowed}
.project: {project_file}
""".strip()


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="SDLC Phase Gate Enforcement")
    parser.add_argument("command", choices=["check", "status"],
                       help="Command to execute")
    parser.add_argument("file", nargs="?", type=Path,
                       help="File path to check (for 'check' command)")

    args = parser.parse_args()

    if args.command == "check":
        if not args.file:
            print("Error: file argument required for 'check' command")
            return 1

        allowed, message = check_phase_gate(args.file)

        if not allowed:
            print(message)
            return 1

        return 0

    elif args.command == "status":
        print(get_project_status())
        return 0


if __name__ == "__main__":
    sys.exit(main())
