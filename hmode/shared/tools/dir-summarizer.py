#!/usr/bin/env python3
"""
Smart Directory Summarizer - Analyze a project directory using Ollama

Intelligently samples files while respecting context limits and excluding noise.
Uses tree-sitter AST parsing for accurate code signature extraction.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from typing import Generator

# Import AST extractor (with graceful fallback)
try:
    from ast_extractor import extract_signatures, get_extractor_status, TREE_SITTER_AVAILABLE
except ImportError:
    # Fallback if ast_extractor not found
    TREE_SITTER_AVAILABLE = False
    def extract_signatures(path, content, include_imports=False):
        return None  # Will use legacy extraction
    def get_extractor_status():
        return {"tree_sitter_available": False}

# Directories to always skip
EXCLUDE_DIRS = {
    "node_modules", "__pycache__", ".git", ".svn", ".hg",
    "venv", ".venv", "env", ".env", ".tox", ".nox",
    "dist", "build", "_build", ".next", ".nuxt",
    "coverage", ".coverage", "htmlcov", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", ".eslintcache",
    "vendor", "bower_components", ".cargo", "target",
    ".terraform", ".serverless", "cdk.out",
    ".idea", ".vscode", ".DS_Store",
    "eggs", "*.egg-info", ".eggs",
}

# Files to always skip
EXCLUDE_FILES = {
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    "poetry.lock", "Pipfile.lock", "composer.lock",
    "Cargo.lock", "Gemfile.lock", "bun.lockb",
    ".gitignore", ".dockerignore", ".eslintignore",
}

# High-value "indicator" files (read these first, in priority order)
README_FILES = [
    "README.md", "README.rst", "README.txt", "README",
    "CLAUDE.md", "PROJECT.md", "CONTRIBUTING.md", "ARCHITECTURE.md",
]

# Project manifest/model files (second priority)
MANIFEST_FILES = [
    "package.json", "pyproject.toml", "setup.py", "setup.cfg",
    "Cargo.toml", "go.mod", "go.sum", "pom.xml", "build.gradle",
    "Gemfile", "requirements.txt", "environment.yml",
    "composer.json", "mix.exs", "Project.toml",
    ".project", "project.clj", "build.sbt",
]

# Infrastructure/config files (third priority)
INFRA_FILES = [
    "docker-compose.yml", "docker-compose.yaml", "Dockerfile",
    "Makefile", "justfile", "Taskfile.yml",
    "serverless.yml", "template.yaml", "cdk.json",
    "terraform.tf", "main.tf",
]

INDICATOR_FILES = README_FILES + MANIFEST_FILES + INFRA_FILES

# Extensions worth sampling
CODE_EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs",
    ".java", ".kt", ".rb", ".php", ".swift", ".c", ".cpp",
    ".h", ".cs", ".scala", ".clj", ".ex", ".exs",
}

DOC_EXTENSIONS = {".md", ".rst", ".txt"}
CONFIG_EXTENSIONS = {".json", ".yaml", ".yml", ".toml", ".ini", ".cfg"}


def should_exclude_dir(name: str) -> bool:
    """Check if directory should be excluded."""
    return name in EXCLUDE_DIRS or name.startswith(".")


def should_exclude_file(name: str) -> bool:
    """Check if file should be excluded."""
    return name in EXCLUDE_FILES


def get_file_priority(path: Path) -> int:
    """Higher = more important. Returns 0 if should skip."""
    name = path.name
    suffix = path.suffix.lower()

    # READMEs are highest priority - these tell us what the project is
    if name in README_FILES:
        return 100

    # Manifest/model files are second - these define the project structure
    if name in MANIFEST_FILES:
        return 95

    # Infrastructure files
    if name in INFRA_FILES:
        return 85

    # Entry points
    if name in ("main.py", "index.js", "index.ts", "app.py", "server.py", "main.go", "main.rs"):
        return 70

    # Other documentation
    if suffix in DOC_EXTENSIONS:
        return 60

    # Config files
    if suffix in CONFIG_EXTENSIONS:
        return 50

    # Source code (lowest priority - only if space remains)
    if suffix in CODE_EXTENSIONS:
        return 30

    return 0


def walk_directory(root: Path) -> Generator[Path, None, None]:
    """Walk directory, skipping excluded paths."""
    for dirpath, dirnames, filenames in os.walk(root):
        # Filter out excluded directories in-place
        dirnames[:] = [d for d in dirnames if not should_exclude_dir(d)]

        for filename in filenames:
            if not should_exclude_file(filename):
                yield Path(dirpath) / filename


def extract_structure(root: Path, max_items: int = 100) -> str:
    """Get directory tree structure."""
    lines = []
    count = 0

    for path in sorted(walk_directory(root)):
        if count >= max_items:
            lines.append(f"... and more files (truncated at {max_items})")
            break
        rel_path = path.relative_to(root)
        lines.append(str(rel_path))
        count += 1

    return "\n".join(lines)


def extract_code_skeleton_legacy(content: str, max_lines: int = 50) -> str:
    """Legacy: Extract just imports, class/function definitions from code (heuristic)."""
    important_lines = []
    lines = content.split("\n")

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Skip imports (we want signatures, not deps)
        if stripped.startswith(("import ", "from ", "require(")):
            continue

        # Keep exports (public API indicator)
        if stripped.startswith("export "):
            important_lines.append(line)
        # Keep class/function definitions
        elif stripped.startswith(("class ", "def ", "async def ", "function ", "async function ",
                                   "pub fn ", "fn ", "type ", "interface ", "struct ", "enum ")):
            important_lines.append(line)
        # Keep decorators
        elif stripped.startswith("@"):
            important_lines.append(line)
        # Keep docstrings (first line only)
        elif stripped.startswith(('"""', "'''")):
            if len(important_lines) < max_lines:
                # Get just the first line of docstring
                important_lines.append(line)

        if len(important_lines) >= max_lines:
            important_lines.append("# ... (truncated)")
            break

    return "\n".join(important_lines)


def extract_code_skeleton(path: Path, content: str, max_lines: int = 50) -> str:
    """Extract code skeleton - uses AST if available, falls back to heuristics."""
    # Try AST extraction first
    if TREE_SITTER_AVAILABLE:
        try:
            signatures = extract_signatures(path, content, include_imports=False)
            if signatures:
                lines = signatures.split("\n")
                if len(lines) > max_lines:
                    return "\n".join(lines[:max_lines]) + "\n# ... (truncated)"
                return signatures
        except Exception:
            pass  # Fall through to legacy

    # Fallback to legacy heuristic extraction
    return extract_code_skeleton_legacy(content, max_lines)


def gather_context(root: Path, max_chars: int = 15000) -> str:
    """Gather smart context from directory."""
    root = Path(root).resolve()
    context_parts = []
    chars_used = 0

    # 1. Directory structure (budget: 2000 chars)
    structure = extract_structure(root, max_items=80)
    structure_section = f"=== FILE STRUCTURE ===\n{structure}\n"
    context_parts.append(structure_section)
    chars_used += len(structure_section)

    # 2. Collect and prioritize files
    files_with_priority = []
    for path in walk_directory(root):
        priority = get_file_priority(path)
        if priority > 0:
            files_with_priority.append((priority, path))

    # Sort by priority (highest first)
    files_with_priority.sort(key=lambda x: -x[0])

    # 3. Read files in priority order
    context_parts.append("\n=== KEY FILES ===\n")
    chars_used += 20

    for priority, path in files_with_priority:
        remaining = max_chars - chars_used
        if remaining < 500:
            break

        try:
            content = path.read_text(errors="ignore")
        except Exception:
            continue

        rel_path = path.relative_to(root)

        # For code files, extract skeleton if too long
        if path.suffix in CODE_EXTENSIONS and len(content) > 1000:
            content = extract_code_skeleton(path, content, max_lines=40)
            method = "AST" if TREE_SITTER_AVAILABLE else "heuristic"
            header = f"\n--- {rel_path} ({method} skeleton) ---\n"
        else:
            # Truncate if needed
            if len(content) > remaining - 100:
                content = content[:remaining - 100] + "\n... (truncated)"
            header = f"\n--- {rel_path} ---\n"

        section = header + content + "\n"
        if chars_used + len(section) > max_chars:
            # Try truncating more aggressively
            available = max_chars - chars_used - len(header) - 50
            if available > 200:
                section = header + content[:available] + "\n... (truncated)\n"
            else:
                break

        context_parts.append(section)
        chars_used += len(section)

    return "".join(context_parts)


def summarize_with_ollama(context: str, model: str = "llama3.2") -> str:
    """Send context to Ollama for summarization."""
    prompt = f"""Analyze this project directory and provide a concise summary:

1. **What is this?** (1-2 sentences)
2. **Tech stack** (languages, frameworks, key dependencies)
3. **Main components** (3-5 bullet points)
4. **Purpose/Goal** (what problem does it solve?)

Be concise and factual. Base your analysis only on the provided content.

{context}"""

    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.stdout.strip()
    except FileNotFoundError:
        return "ERROR: Ollama not found. Install from https://ollama.ai"
    except subprocess.TimeoutExpired:
        return "ERROR: Ollama timed out"
    except Exception as e:
        return f"ERROR: {e}"


def main():
    parser = argparse.ArgumentParser(description="Summarize a directory using Ollama")
    parser.add_argument("directory", nargs="?", default=".", help="Directory to analyze")
    parser.add_argument("-m", "--model", default="gpt-oss:20b", help="Ollama model to use")
    parser.add_argument("-c", "--max-chars", type=int, default=15000, help="Max context chars")
    parser.add_argument("--context-only", action="store_true", help="Print context without calling Ollama")
    parser.add_argument("--status", action="store_true", help="Show extractor status")
    parser.add_argument("-o", "--output", help="Save summary to file")
    args = parser.parse_args()

    # Show status and exit
    if args.status:
        status = get_extractor_status()
        print("AST Extractor Status:")
        print(f"  tree-sitter available: {status['tree_sitter_available']}")
        if status['tree_sitter_available']:
            print(f"  AST languages: {', '.join(status['supported_languages'])}")
        print(f"  Fallback languages: {', '.join(status.get('fallback_languages', []))}")
        sys.exit(0)

    directory = Path(args.directory).resolve()
    if not directory.is_dir():
        print(f"Error: {directory} is not a directory", file=sys.stderr)
        sys.exit(1)

    extractor = "AST" if TREE_SITTER_AVAILABLE else "heuristic"
    print(f"Analyzing: {directory} (using {extractor} extraction)", file=sys.stderr)
    context = gather_context(directory, max_chars=args.max_chars)
    print(f"Context gathered: {len(context)} chars", file=sys.stderr)

    if args.context_only:
        print(context)
        return

    print(f"Sending to Ollama ({args.model})...", file=sys.stderr)
    summary = summarize_with_ollama(context, model=args.model)

    if args.output:
        Path(args.output).write_text(summary)
        print(f"Summary saved to: {args.output}", file=sys.stderr)
    else:
        print("\n" + "=" * 60)
        print(summary)


if __name__ == "__main__":
    main()
