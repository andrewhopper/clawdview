#!/usr/bin/env python3
"""
Deterministic Hook Engine

Pattern-based rule system that injects steering guidance into Claude conversations.
Rules are loaded from hooks-rules.yaml.

Usage:
    python hook-engine.py check-file <path>
    python hook-engine.py check-output <text>
    python hook-engine.py check-deployment <type> <data>
"""

# File UUID: 4f2a8c9d-6b3e-4a7f-8d1c-9e2b5f7a3c6d

import os
import sys
import re
import yaml
from pathlib import Path
from typing import Optional, Dict, List, Any
from dataclasses import dataclass


@dataclass
class HookMatch:
    """Result from a pattern match"""
    matched: bool
    rule_name: str
    inject_text: str
    metadata: Dict[str, Any]


class HookEngine:
    """Pattern-based hook engine"""

    def __init__(self, rules_path: Optional[Path] = None):
        if rules_path is None:
            # Default to hooks-rules.yaml in same directory
            rules_path = Path(__file__).parent / "hooks-rules.yaml"

        with open(rules_path) as f:
            self.rules = yaml.safe_load(f)

        self.version = self.rules.get("version", "unknown")

    def check_file_created(self, file_path: str) -> Optional[HookMatch]:
        """Check if a file creation matches any rules"""
        path = Path(file_path)

        # Check file generation rules
        for rule in self.rules.get("file_generation", []):
            pattern = rule["pattern"]
            if re.match(pattern, str(path)):
                # Check conditions if specified
                if "condition" in rule:
                    if not self._eval_condition(rule["condition"], path):
                        continue

                # Prepare metadata
                metadata = self._gather_file_metadata(path)

                # Format inject text
                inject_text = rule["inject"].format(**metadata)

                return HookMatch(
                    matched=True,
                    rule_name=rule["name"],
                    inject_text=inject_text,
                    metadata=metadata
                )

        # Check code event rules (test files)
        for rule in self.rules.get("code_events", []):
            if rule.get("type") == "file_created":
                pattern = rule["pattern"]
                if re.match(pattern, str(path)):
                    metadata = self._gather_file_metadata(path)
                    metadata["framework"] = self._detect_test_framework(path)

                    inject_text = rule["inject"].format(**metadata)

                    return HookMatch(
                        matched=True,
                        rule_name=rule["name"],
                        inject_text=inject_text,
                        metadata=metadata
                    )

        return None

    def check_file_modified(self, file_path: str) -> Optional[HookMatch]:
        """Check if a file modification matches any rules"""
        path = Path(file_path)

        # Check code event rules (dependencies)
        for rule in self.rules.get("code_events", []):
            if rule.get("type") == "file_modified":
                pattern = rule["pattern"]
                if re.match(pattern, str(path)):
                    metadata = {
                        "path": str(path),
                        "package_manager": self._detect_package_manager(path)
                    }

                    inject_text = rule["inject"].format(**metadata)

                    return HookMatch(
                        matched=True,
                        rule_name=rule["name"],
                        inject_text=inject_text,
                        metadata=metadata
                    )

        return None

    def check_command_output(self, output: str) -> Optional[HookMatch]:
        """Check if command output matches any error/warning patterns"""
        # Check error rules
        for rule in self.rules.get("errors", []):
            if rule.get("type") == "command_output":
                pattern = rule["pattern"]
                match = re.search(pattern, output, re.IGNORECASE)
                if match:
                    metadata = {"output": output[:200]}  # First 200 chars

                    # Extract specific info based on pattern
                    if "port" in rule["name"].lower():
                        port_match = re.search(r":(\d+)", output)
                        if port_match:
                            metadata["port"] = port_match.group(1)

                    inject_text = rule["inject"].format(**metadata)

                    return HookMatch(
                        matched=True,
                        rule_name=rule["name"],
                        inject_text=inject_text,
                        metadata=metadata
                    )

        # Check special cases
        for rule in self.rules.get("special_cases", []):
            if rule.get("type") == "command_output":
                pattern = rule["pattern"]
                if re.search(pattern, output, re.IGNORECASE):
                    metadata = {"output": output[:200]}

                    inject_text = rule["inject"].format(**metadata)

                    return HookMatch(
                        matched=True,
                        rule_name=rule["name"],
                        inject_text=inject_text,
                        metadata=metadata
                    )

        # Check infrastructure hooks
        for rule in self.rules.get("infrastructure", []):
            if rule.get("type") == "command_output":
                pattern = rule["pattern"]
                if re.search(pattern, output, re.IGNORECASE):
                    metadata = {"output": output[:200]}

                    inject_text = rule["inject"].format(**metadata)

                    return HookMatch(
                        matched=True,
                        rule_name=rule["name"],
                        inject_text=inject_text,
                        metadata=metadata
                    )

        return None

    def check_deployment(self, deployment_type: str, data: Dict[str, Any]) -> Optional[HookMatch]:
        """Check if a deployment matches any rules"""
        for rule in self.rules.get("deployment", []):
            # Check if deployment type matches rule pattern
            if deployment_type in rule["pattern"]:
                # Use provided data for formatting
                metadata = data.copy()

                inject_text = rule["inject"].format(**metadata)

                return HookMatch(
                    matched=True,
                    rule_name=rule["name"],
                    inject_text=inject_text,
                    metadata=metadata
                )

        return None

    def _gather_file_metadata(self, path: Path) -> Dict[str, Any]:
        """Gather metadata about a file"""
        metadata = {
            "path": str(path),
            "filename": path.name,
            "extension": path.suffix
        }

        try:
            stat = path.stat()
            size_bytes = stat.st_size
            metadata["size_bytes"] = size_bytes
            metadata["size_kb"] = size_bytes / 1024
            metadata["size_mb"] = size_bytes / (1024 * 1024)
        except:
            metadata["size_bytes"] = 0
            metadata["size_kb"] = 0
            metadata["size_mb"] = 0

        # For buildinfo.json, parse content
        if path.name == "buildinfo.json":
            try:
                import json
                with open(path) as f:
                    buildinfo = json.load(f)
                metadata["git_hash"] = buildinfo.get("git", {}).get("hash", "unknown")[:7]
                metadata["branch"] = buildinfo.get("git", {}).get("branch", "unknown")
                metadata["timestamp"] = buildinfo.get("deployment", {}).get("timestamp", "unknown")
            except:
                pass

        return metadata

    def _eval_condition(self, condition_name: str, path: Path) -> bool:
        """Evaluate a condition (simplified)"""
        conditions = self.rules.get("conditions", {})

        if condition_name == "is_standalone_mockup":
            try:
                with open(path) as f:
                    content = f.read(2000)
                indicators = ["<!DOCTYPE html>", "<html", "mockup", "Asset:", "Design System:"]
                component_indicators = ["export default", "import React"]
                has_standalone = any(ind in content for ind in indicators)
                has_component = any(ind in content for ind in component_indicators)
                return has_standalone and not has_component
            except:
                return False

        elif condition_name == "is_component":
            try:
                with open(path) as f:
                    content = f.read(2000)
                indicators = ["export default", "import React", ".tsx", ".jsx"]
                return any(ind in content for ind in indicators)
            except:
                return False

        elif condition_name == "size_lt_10mb":
            try:
                size_mb = path.stat().st_size / (1024 * 1024)
                return size_mb < 10
            except:
                return False

        elif condition_name == "size_gte_10mb":
            try:
                size_mb = path.stat().st_size / (1024 * 1024)
                return size_mb >= 10
            except:
                return False

        elif condition_name == "file_gt_100mb":
            try:
                size_mb = path.stat().st_size / (1024 * 1024)
                return size_mb > 100
            except:
                return False

        return False

    def _detect_test_framework(self, path: Path) -> str:
        """Detect test framework from file path/content"""
        name = path.name.lower()

        if "test_" in name or name.startswith("test"):
            return "pytest"
        elif ".test.ts" in name or ".test.js" in name:
            return "jest/vitest"
        elif ".spec.ts" in name or ".spec.js" in name:
            return "jest/vitest"
        elif "cucumber" in name or ".feature" in name:
            return "cucumber"

        return "unknown"

    def _detect_package_manager(self, path: Path) -> str:
        """Detect package manager from file name"""
        name = path.name.lower()

        if "package.json" in name:
            # Check for pnpm-lock.yaml or yarn.lock in same dir
            if (path.parent / "pnpm-lock.yaml").exists():
                return "pnpm"
            elif (path.parent / "yarn.lock").exists():
                return "yarn"
            else:
                return "npm"
        elif "requirements.txt" in name or "Pipfile" in name:
            return "pip/pipenv"
        elif "go.mod" in name:
            return "go mod"
        elif "Cargo.toml" in name:
            return "cargo"

        return "unknown"


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]
    engine = HookEngine()

    if command == "check-file":
        if len(sys.argv) < 3:
            print("Usage: hook-engine.py check-file <path>")
            sys.exit(1)

        file_path = sys.argv[2]

        # Try file created
        result = engine.check_file_created(file_path)
        if not result:
            # Try file modified
            result = engine.check_file_modified(file_path)

        if result:
            print(f"✓ Matched: {result.rule_name}")
            print(f"\nInject into conversation:\n")
            print(result.inject_text)
        else:
            print("No hooks matched")

    elif command == "check-output":
        if len(sys.argv) < 3:
            print("Usage: hook-engine.py check-output <text>")
            sys.exit(1)

        output = " ".join(sys.argv[2:])
        result = engine.check_command_output(output)

        if result:
            print(f"✓ Matched: {result.rule_name}")
            print(f"\nInject into conversation:\n")
            print(result.inject_text)
        else:
            print("No hooks matched")

    elif command == "check-deployment":
        if len(sys.argv) < 3:
            print("Usage: hook-engine.py check-deployment <type> [key=value ...]")
            print("Example: hook-engine.py check-deployment amplify url=https://example.com branch=main")
            sys.exit(1)

        deployment_type = sys.argv[2]

        # Parse key=value pairs
        data = {}
        for arg in sys.argv[3:]:
            if "=" in arg:
                key, value = arg.split("=", 1)
                data[key] = value

        result = engine.check_deployment(deployment_type, data)

        if result:
            print(f"✓ Matched: {result.rule_name}")
            print(f"\nInject into conversation:\n")
            print(result.inject_text)
        else:
            print("No hooks matched")

    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
