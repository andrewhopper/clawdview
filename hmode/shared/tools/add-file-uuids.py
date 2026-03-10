#!/usr/bin/env python3
"""
Add UUIDs to linked files based on file-links.yaml registry.

For markdown files: adds uuid field to YAML frontmatter
For code files: adds uuid comment to header
"""

import yaml
import os
import re
from pathlib import Path

REPO_ROOT = Path("/home/user/protoflow")
REGISTRY_PATH = REPO_ROOT / ".claude" / "file-links.yaml"


def load_registry() -> dict:
    """Load the file links registry."""
    with open(REGISTRY_PATH) as f:
        return yaml.safe_load(f)


def get_file_extension(path: str) -> str:
    """Get file extension."""
    return Path(path).suffix.lower()


def add_uuid_to_markdown(filepath: Path, uuid: str) -> bool:
    """Add uuid to markdown file frontmatter."""
    if not filepath.exists():
        print(f"  SKIP (not found): {filepath}")
        return False

    content = filepath.read_text()

    # Check if already has uuid
    if re.search(r'^uuid:\s*\S+', content, re.MULTILINE):
        print(f"  SKIP (has uuid): {filepath}")
        return False

    # Check for YAML frontmatter
    if content.startswith('---'):
        # Find end of frontmatter
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if match:
            frontmatter = match.group(1)
            # Add uuid after first line of frontmatter
            lines = frontmatter.split('\n')
            lines.insert(0, f"uuid: {uuid}")
            new_frontmatter = '\n'.join(lines)
            new_content = f"---\n{new_frontmatter}\n---{content[match.end():]}"
            filepath.write_text(new_content)
            print(f"  ADDED: {filepath}")
            return True
    else:
        # No frontmatter, add it
        new_content = f"---\nuuid: {uuid}\n---\n\n{content}"
        filepath.write_text(new_content)
        print(f"  ADDED (new frontmatter): {filepath}")
        return True

    return False


def add_uuid_to_code(filepath: Path, uuid: str, comment_prefix: str) -> bool:
    """Add uuid comment to code file header."""
    if not filepath.exists():
        print(f"  SKIP (not found): {filepath}")
        return False

    content = filepath.read_text()

    # Check if already has uuid
    if f"uuid: {uuid}" in content or f"uuid:{uuid}" in content:
        print(f"  SKIP (has uuid): {filepath}")
        return False

    # For files with shebang, add after shebang
    if content.startswith('#!'):
        lines = content.split('\n')
        lines.insert(1, f"{comment_prefix} uuid: {uuid}")
        new_content = '\n'.join(lines)
    else:
        # Add at top
        new_content = f"{comment_prefix} uuid: {uuid}\n{content}"

    filepath.write_text(new_content)
    print(f"  ADDED: {filepath}")
    return True


def add_uuid_to_file(target_path: str, uuid: str) -> bool:
    """Add UUID to a file based on its type."""
    # Handle relative paths
    if target_path.startswith('/'):
        filepath = Path(target_path)
    else:
        filepath = REPO_ROOT / target_path

    # Skip directories and non-existent files
    if not filepath.exists() or filepath.is_dir():
        print(f"  SKIP (dir/missing): {target_path}")
        return False

    ext = get_file_extension(target_path)

    if ext == '.md':
        return add_uuid_to_markdown(filepath, uuid)
    elif ext in ['.py']:
        return add_uuid_to_code(filepath, uuid, '#')
    elif ext in ['.js', '.ts', '.tsx', '.jsx']:
        return add_uuid_to_code(filepath, uuid, '//')
    elif ext in ['.sh', '.bash']:
        return add_uuid_to_code(filepath, uuid, '#')
    elif ext in ['.yaml', '.yml']:
        return add_uuid_to_code(filepath, uuid, '#')
    else:
        print(f"  SKIP (unsupported ext {ext}): {target_path}")
        return False


def main():
    print("Loading registry...")
    registry = load_registry()

    links = registry.get('links', {})
    print(f"Found {len(links)} links\n")

    added = 0
    skipped = 0

    for uid, info in links.items():
        target = info.get('target_path', '')
        status = info.get('status', 'valid')

        # Skip broken links
        if status == 'broken':
            print(f"  SKIP (broken): {uid}")
            skipped += 1
            continue

        # Skip release symlinks (they point to directories)
        if target.startswith('releases/'):
            print(f"  SKIP (release dir): {uid}")
            skipped += 1
            continue

        print(f"Processing {uid}...")
        if add_uuid_to_file(target, uid):
            added += 1
        else:
            skipped += 1

    print(f"\n{'='*60}")
    print(f"SUMMARY: Added {added} UUIDs, Skipped {skipped}")


if __name__ == "__main__":
    main()
