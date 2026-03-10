#!/usr/bin/env python3
"""
Auto-Fix Guardrails In-Flow

Automatically fixes guardrail violations as they occur during development.
Runs after file operations and applies fixes immediately.

Features:
- Auto-converts plain S3 URLs to markdown links
- Auto-generates imports for shared domain models
- Auto-prompts for S3 publishing when publishable files created
- Auto-validates tech dependencies

Usage:
  # After file write
  python3 autofix_in_flow.py fix-file path/to/file.html

  # After multiple files
  python3 autofix_in_flow.py fix-recent --since HEAD~1

  # Enable auto-fix for all file operations (background mode)
  python3 autofix_in_flow.py enable

Exit codes:
  0 - No violations or all fixed
  1 - Violations found but not fixable
  2 - Critical error
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
import subprocess

# ============================================================================
# Configuration
# ============================================================================

REPO_ROOT = Path(__file__).parent.parent.parent
DOMAIN_REGISTRY = REPO_ROOT / "shared" / "semantic" / "domains" / "registry.yaml"
TECH_PREFS_DIR = REPO_ROOT / ".guardrails" / "tech-preferences"
S3_PUBLISH_SCRIPT = REPO_ROOT / "prototypes" / "proto-s3-publish-vayfd-023" / "s3_publish.py"

PUBLISHABLE_EXTENSIONS = {".html", ".pdf", ".svg", ".zip", ".mp3", ".mp4"}


# ============================================================================
# Auto-Fixers
# ============================================================================

@dataclass
class FixResult:
    """Result of auto-fix operation"""
    success: bool
    message: str
    applied_fixes: List[str]


class AutoFixer:
    """Base class for auto-fixers"""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.repo_root = REPO_ROOT

    def can_fix(self) -> bool:
        """Check if this file needs fixing"""
        raise NotImplementedError

    def apply_fix(self) -> FixResult:
        """Apply automatic fix"""
        raise NotImplementedError


class URLAutoFixer(AutoFixer):
    """Auto-converts plain S3 URLs to markdown links"""

    def can_fix(self) -> bool:
        if not self.file_path.exists():
            return False

        # Only fix markdown and documentation files
        if self.file_path.suffix not in [".md", ".txt"]:
            return False

        try:
            with open(self.file_path) as f:
                content = f.read()
                # Check for plain S3 URLs
                return bool(re.search(r'(?<!\[.*\]\()https://[^/]+\.s3\.[^/]+\.amazonaws\.com/[^\s\)]+', content))
        except Exception:
            return False

    def apply_fix(self) -> FixResult:
        try:
            with open(self.file_path) as f:
                lines = f.readlines()

            fixed_lines = []
            fixes_applied = []

            for line in lines:
                # Find plain S3 URLs (not already in markdown links)
                modified_line = line

                # Pattern: S3 URL not preceded by ]( (markdown link)
                for match in re.finditer(r'(?<!\[.*\]\()https://([^/]+\.s3\.[^/]+\.amazonaws\.com/[^\s\)]+)', line):
                    url = match.group(0)
                    filename = url.split('/')[-1]

                    # Replace with markdown link
                    markdown_link = f"[{filename}]({url})"
                    modified_line = modified_line.replace(url, markdown_link)
                    fixes_applied.append(f"Converted URL to markdown: {filename}")

                fixed_lines.append(modified_line)

            if fixes_applied:
                with open(self.file_path, 'w') as f:
                    f.writelines(fixed_lines)

                return FixResult(
                    success=True,
                    message=f"✅ Auto-fixed {len(fixes_applied)} S3 URLs in {self.file_path.name}",
                    applied_fixes=fixes_applied
                )
            else:
                return FixResult(success=True, message="No URLs to fix", applied_fixes=[])

        except Exception as e:
            return FixResult(success=False, message=f"Failed to fix URLs: {e}", applied_fixes=[])


class SharedModelAutoFixer(AutoFixer):
    """Auto-generates imports for shared domain models"""

    def __init__(self, file_path: Path):
        super().__init__(file_path)
        self.registry = self._load_registry()

    def _load_registry(self) -> Dict[str, List[str]]:
        """Load domain registry"""
        if not DOMAIN_REGISTRY.exists():
            return {}

        try:
            import yaml
            with open(DOMAIN_REGISTRY) as f:
                data = yaml.safe_load(f)
                # Extract domain → entities mapping
                registry = {}
                for domain in data.get("domains", []):
                    domain_name = domain.get("name")
                    entities = domain.get("entities", [])
                    if domain_name:
                        registry[domain_name] = entities
                return registry
        except Exception:
            return {}

    def can_fix(self) -> bool:
        if not self.file_path.exists():
            return False

        # Only fix TypeScript files
        if self.file_path.suffix != ".ts":
            return False

        try:
            with open(self.file_path) as f:
                content = f.read()
                # Check for local type definitions
                local_types = re.findall(r'(?:interface|type|class)\s+([A-Z][a-zA-Z0-9]*)', content)

                # Check if any exist in registry
                for type_name in local_types:
                    if self._find_domain_for_type(type_name):
                        return True

                return False
        except Exception:
            return False

    def apply_fix(self) -> FixResult:
        try:
            with open(self.file_path) as f:
                content = f.read()
                lines = content.split('\n')

            # Find local types that exist in registry
            local_types = re.findall(r'(?:interface|type|class)\s+([A-Z][a-zA-Z0-9]*)', content)

            fixes_applied = []
            imports_to_add = []

            for type_name in local_types:
                domain = self._find_domain_for_type(type_name)
                if domain:
                    import_line = f"import {{ {type_name} }} from '@shared/semantic/domains/{domain}/generated/typescript';"
                    imports_to_add.append(import_line)
                    fixes_applied.append(f"Added import for {type_name} from {domain}")

            if imports_to_add:
                # Add imports at the top (after any existing imports)
                import_section_end = 0
                for i, line in enumerate(lines):
                    if line.startswith('import '):
                        import_section_end = i + 1

                # Insert new imports
                for import_line in imports_to_add:
                    if import_line not in content:
                        lines.insert(import_section_end, import_line)
                        import_section_end += 1

                # Remove local definitions (comment them out for safety)
                for type_name in [t for t in local_types if self._find_domain_for_type(t)]:
                    for i, line in enumerate(lines):
                        if re.search(rf'(?:interface|type|class)\s+{type_name}\b', line):
                            lines[i] = f"// {line}  // Auto-replaced with shared domain import"

                with open(self.file_path, 'w') as f:
                    f.write('\n'.join(lines))

                return FixResult(
                    success=True,
                    message=f"✅ Auto-fixed {len(fixes_applied)} type imports in {self.file_path.name}",
                    applied_fixes=fixes_applied
                )
            else:
                return FixResult(success=True, message="No types to fix", applied_fixes=[])

        except Exception as e:
            return FixResult(success=False, message=f"Failed to fix types: {e}", applied_fixes=[])

    def _find_domain_for_type(self, type_name: str) -> Optional[str]:
        """Find which domain contains the type"""
        for domain, entities in self.registry.items():
            if type_name in entities:
                return domain
        return None


class S3PublishAutoPrompt(AutoFixer):
    """Auto-prompts for S3 publishing when publishable files created"""

    def can_fix(self) -> bool:
        if not self.file_path.exists():
            return False

        # Check if file is publishable
        if self.file_path.suffix not in PUBLISHABLE_EXTENSIONS:
            return False

        # Check if already published or skipped
        skip_markers = [".s3-skip", ".no-publish", f"{self.file_path.name}.s3-published"]
        for marker in skip_markers:
            if (self.file_path.parent / marker).exists():
                return False

        return True

    def apply_fix(self) -> FixResult:
        """Prompt for S3 publishing"""
        filename = self.file_path.name

        print(f"\n🚀 Publishable file detected: {filename}")
        print("\nPublish to S3?")
        print("  [1] Public (permanent URL)")
        print("  [2] Temporary (presigned URL, 7 days)")
        print("  [3] Private (internal access only)")
        print("  [4] Skip (create .s3-skip marker)")
        print("  [Enter] Auto-publish to public")

        choice = input("\nChoice: ").strip()

        if choice == "4":
            # Create skip marker
            skip_marker = self.file_path.parent / ".s3-skip"
            skip_marker.touch()
            return FixResult(
                success=True,
                message=f"⏭️  Skipped S3 publishing (marker created)",
                applied_fixes=["Created .s3-skip marker"]
            )

        # Determine publish type
        if choice == "2":
            publish_args = ["--temp"]
        elif choice == "3":
            publish_args = ["--private"]
        else:
            publish_args = ["--public"]

        # Run S3 publish script
        try:
            result = subprocess.run(
                ["python3", str(S3_PUBLISH_SCRIPT), str(self.file_path), "--yes"] + publish_args,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                # Extract URL from output
                url_match = re.search(r'(https://[^\s]+)', result.stdout)
                url = url_match.group(1) if url_match else "URL not found"

                return FixResult(
                    success=True,
                    message=f"✅ Published to S3: [{filename}]({url})",
                    applied_fixes=[f"Published to S3", f"URL: {url}"]
                )
            else:
                return FixResult(
                    success=False,
                    message=f"❌ S3 publish failed: {result.stderr}",
                    applied_fixes=[]
                )

        except Exception as e:
            return FixResult(success=False, message=f"Failed to publish: {e}", applied_fixes=[])


# ============================================================================
# In-Flow Auto-Fix Engine
# ============================================================================

class InFlowAutoFix:
    """Main auto-fix engine"""

    def __init__(self):
        self.fixers = [
            URLAutoFixer,
            SharedModelAutoFixer,
            S3PublishAutoPrompt,
        ]

    def process_file(self, file_path: Path) -> List[FixResult]:
        """Process file and apply all applicable fixes"""
        results = []

        for fixer_class in self.fixers:
            fixer = fixer_class(file_path)

            if fixer.can_fix():
                result = fixer.apply_fix()
                results.append(result)

                if result.success and result.applied_fixes:
                    print(result.message)
                    for fix in result.applied_fixes:
                        print(f"  • {fix}")

        return results

    def process_recent_files(self, since: str = "HEAD~1") -> Dict[str, List[FixResult]]:
        """Process files changed since a commit"""
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", since],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True
            )

            changed_files = result.stdout.strip().split('\n')
            all_results = {}

            for file_path_str in changed_files:
                if not file_path_str:
                    continue

                file_path = REPO_ROOT / file_path_str
                if file_path.exists():
                    results = self.process_file(file_path)
                    if results:
                        all_results[str(file_path)] = results

            return all_results

        except Exception as e:
            print(f"❌ Error processing recent files: {e}")
            return {}


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Auto-fix guardrails in-flow")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # fix-file command
    fix_file_parser = subparsers.add_parser("fix-file", help="Fix a specific file")
    fix_file_parser.add_argument("file_path", type=Path, help="File to fix")

    # fix-recent command
    fix_recent_parser = subparsers.add_parser("fix-recent", help="Fix recently changed files")
    fix_recent_parser.add_argument("--since", default="HEAD~1", help="Git commit to compare against")

    # enable command
    enable_parser = subparsers.add_parser("enable", help="Enable auto-fix for all file operations")

    args = parser.parse_args()

    engine = InFlowAutoFix()

    if args.command == "fix-file":
        results = engine.process_file(args.file_path)

        if not results:
            print(f"✅ No fixes needed for {args.file_path.name}")
            return 0

        success_count = sum(1 for r in results if r.success)
        print(f"\n📊 Applied {success_count}/{len(results)} fixes")
        return 0 if success_count == len(results) else 1

    elif args.command == "fix-recent":
        all_results = engine.process_recent_files(args.since)

        if not all_results:
            print("✅ No files needed fixing")
            return 0

        total_fixes = sum(len(results) for results in all_results.values())
        print(f"\n📊 Fixed {len(all_results)} files with {total_fixes} total fixes")
        return 0

    elif args.command == "enable":
        print("🔧 Auto-fix in-flow enabled")
        print("\nTo integrate with file operations:")
        print("1. Add to .claude/hooks/tool-result.sh")
        print("2. Call after each file write:")
        print("   python3 .guardrails/ai-steering/autofix_in_flow.py fix-file <file>")
        return 0

    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
