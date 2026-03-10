#!/usr/bin/env python3
"""
Smart Auto-Fix with Severity-Based Actions

Categorizes violations by severity and takes appropriate action:
- CRITICAL/HIGH: Notify user, block if needed
- MEDIUM: Remind AI to handle it
- LOW: Auto-fix silently

Usage:
  python3 smart_autofix.py check <file>     # Check file and return AI reminders
  python3 smart_autofix.py watch            # Watch for file changes
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional
import subprocess

# ============================================================================
# Configuration
# ============================================================================

REPO_ROOT = Path(__file__).parent.parent.parent
REMINDERS_FILE = REPO_ROOT / ".guardrails" / ".ai_reminders.json"
DOMAIN_REGISTRY = REPO_ROOT / "shared" / "semantic" / "domains" / "registry.yaml"
S3_PUBLISH_SCRIPT = REPO_ROOT / "prototypes" / "proto-s3-publish-vayfd-023" / "s3_publish.py"

PUBLISHABLE_EXTENSIONS = {".html", ".pdf", ".svg", ".zip", ".mp3", ".mp4"}


# ============================================================================
# Severity Levels
# ============================================================================

class Severity(Enum):
    """Violation severity levels"""
    LOW = 1       # Auto-fix silently
    MEDIUM = 2    # Remind AI
    HIGH = 3      # Notify user
    CRITICAL = 4  # Block/require confirmation


class ActionType(Enum):
    """Action to take for violation"""
    AUTO_FIX = "auto_fix"           # Fix automatically, no notification
    REMIND_AI = "remind_ai"         # Add reminder for AI to handle
    NOTIFY_USER = "notify_user"     # Show notification to user
    BLOCK = "block"                 # Block until resolved


# ============================================================================
# Violation Types with Severity
# ============================================================================

@dataclass
class ViolationRule:
    """Rule defining violation and how to handle it"""
    id: str
    description: str
    severity: Severity
    action: ActionType
    ai_reminder_template: Optional[str] = None
    user_message_template: Optional[str] = None
    auto_fix_fn: Optional[str] = None


# Violation rules with severity configuration
VIOLATION_RULES = {
    "s3_publish_missing": ViolationRule(
        id="s3_publish_missing",
        description="Publishable file created without S3 publishing",
        severity=Severity.MEDIUM,
        action=ActionType.REMIND_AI,
        ai_reminder_template="⚠️ REMINDER: File '{filename}' is publishable but not published to S3. Prompt user: 'Publish {filename} to S3? [1] Public [2] Temp [3] Private [4] Skip'",
    ),

    "shared_model_not_used": ViolationRule(
        id="shared_model_not_used",
        description="Local type definition exists in shared domains",
        severity=Severity.HIGH,
        action=ActionType.NOTIFY_USER,
        user_message_template="🚨 Type '{type_name}' defined locally but exists in shared/semantic/domains/{domain}/\n\nUse shared model: import {{ {type_name} }} from '@shared/semantic/domains/{domain}'",
        auto_fix_fn="fix_shared_model_import"
    ),

    "url_not_clickable": ViolationRule(
        id="url_not_clickable",
        description="S3 URL not in clickable markdown format",
        severity=Severity.LOW,
        action=ActionType.AUTO_FIX,
        auto_fix_fn="fix_url_format"
    ),

    "tech_not_approved": ViolationRule(
        id="tech_not_approved",
        description="Unapproved technology dependency",
        severity=Severity.HIGH,
        action=ActionType.NOTIFY_USER,
        user_message_template="🚨 Unapproved dependency '{tech_name}' in {file}\n\nCheck .guardrails/tech-preferences/ or request approval"
    ),
}


# ============================================================================
# Violation Detection
# ============================================================================

@dataclass
class Violation:
    """Detected violation"""
    rule_id: str
    file_path: Path
    line_number: Optional[int] = None
    details: Dict = field(default_factory=dict)


class ViolationDetector:
    """Detects violations in files"""

    def __init__(self):
        self.repo_root = REPO_ROOT

    def check_file(self, file_path: Path) -> List[Violation]:
        """Check file for all violations"""
        violations = []

        # Check S3 publishing
        if file_path.suffix in PUBLISHABLE_EXTENSIONS:
            if not self._has_s3_evidence(file_path):
                violations.append(Violation(
                    rule_id="s3_publish_missing",
                    file_path=file_path,
                    details={"filename": file_path.name}
                ))

        # Check shared models (TypeScript only)
        if file_path.suffix == ".ts":
            model_violations = self._check_shared_models(file_path)
            violations.extend(model_violations)

        # Check URL format
        if file_path.suffix in [".md", ".txt"]:
            url_violations = self._check_url_format(file_path)
            violations.extend(url_violations)

        return violations

    def _has_s3_evidence(self, file_path: Path) -> bool:
        """Check if S3 publish evidence exists"""
        skip_markers = [".s3-skip", ".no-publish", f"{file_path.name}.s3-published"]
        for marker in skip_markers:
            if (file_path.parent / marker).exists():
                return True

        # Check bookmarks
        bookmarks_dir = self.repo_root / "bookmarks"
        if bookmarks_dir.exists():
            bookmark = bookmarks_dir / f"{file_path.stem}.url"
            if bookmark.exists():
                return True

        return False

    def _check_shared_models(self, file_path: Path) -> List[Violation]:
        """Check for local types that exist in shared domains"""
        violations = []

        try:
            with open(file_path) as f:
                content = f.read()

            # Find local type definitions
            local_types = re.findall(r'(?:interface|type|class)\s+([A-Z][a-zA-Z0-9]*)', content)

            # Load registry
            registry = self._load_registry()

            for type_name in local_types:
                domain = self._find_domain_for_type(type_name, registry)
                if domain:
                    violations.append(Violation(
                        rule_id="shared_model_not_used",
                        file_path=file_path,
                        details={"type_name": type_name, "domain": domain}
                    ))

        except Exception:
            pass

        return violations

    def _check_url_format(self, file_path: Path) -> List[Violation]:
        """Check for plain S3 URLs"""
        violations = []

        try:
            with open(file_path) as f:
                for line_num, line in enumerate(f, 1):
                    # Find plain S3 URLs (not in markdown)
                    if re.search(r'(?<!\[.*\]\()https://[^/]+\.s3\.[^/]+\.amazonaws\.com/', line):
                        violations.append(Violation(
                            rule_id="url_not_clickable",
                            file_path=file_path,
                            line_number=line_num
                        ))
        except Exception:
            pass

        return violations

    def _load_registry(self) -> Dict[str, List[str]]:
        """Load domain registry"""
        if not DOMAIN_REGISTRY.exists():
            return {}

        try:
            import yaml
            with open(DOMAIN_REGISTRY) as f:
                data = yaml.safe_load(f)
                registry = {}
                for domain in data.get("domains", []):
                    domain_name = domain.get("name")
                    entities = domain.get("entities", [])
                    if domain_name:
                        registry[domain_name] = entities
                return registry
        except Exception:
            return {}

    def _find_domain_for_type(self, type_name: str, registry: Dict) -> Optional[str]:
        """Find domain containing type"""
        for domain, entities in registry.items():
            if type_name in entities:
                return domain
        return None


# ============================================================================
# Action Handlers
# ============================================================================

class ActionHandler:
    """Handles actions based on severity"""

    def __init__(self):
        self.reminders = self._load_reminders()

    def handle_violation(self, violation: Violation) -> str:
        """Handle violation based on its rule"""
        rule = VIOLATION_RULES.get(violation.rule_id)
        if not rule:
            return ""

        if rule.action == ActionType.AUTO_FIX:
            return self._auto_fix(violation, rule)
        elif rule.action == ActionType.REMIND_AI:
            return self._remind_ai(violation, rule)
        elif rule.action == ActionType.NOTIFY_USER:
            return self._notify_user(violation, rule)
        elif rule.action == ActionType.BLOCK:
            return self._block(violation, rule)

        return ""

    def _auto_fix(self, violation: Violation, rule: ViolationRule) -> str:
        """Auto-fix without notification"""
        if rule.auto_fix_fn == "fix_url_format":
            self._fix_url_format(violation)
            return f"✅ Auto-fixed: {rule.description} in {violation.file_path.name}"
        elif rule.auto_fix_fn == "fix_shared_model_import":
            self._fix_shared_model_import(violation)
            return f"✅ Auto-fixed: {rule.description} in {violation.file_path.name}"
        return ""

    def _remind_ai(self, violation: Violation, rule: ViolationRule) -> str:
        """Add reminder for AI to handle"""
        if not rule.ai_reminder_template:
            return ""

        # Format reminder with violation details
        reminder = rule.ai_reminder_template.format(**violation.details)

        # Add to reminders file
        self.reminders.append({
            "rule_id": violation.rule_id,
            "file": str(violation.file_path),
            "reminder": reminder,
            "timestamp": datetime.now().isoformat()
        })
        self._save_reminders()

        # Return reminder for immediate injection
        return reminder

    def _notify_user(self, violation: Violation, rule: ViolationRule) -> str:
        """Notify user of violation"""
        if not rule.user_message_template:
            return ""

        message = rule.user_message_template.format(
            file=violation.file_path.name,
            **violation.details
        )

        # Print to stdout for user to see
        print(f"\n{message}\n")

        return message

    def _block(self, violation: Violation, rule: ViolationRule) -> str:
        """Block until violation resolved"""
        message = self._notify_user(violation, rule)
        print("🚫 Please resolve this violation before continuing.")
        return message

    def _fix_url_format(self, violation: Violation):
        """Fix plain URLs to markdown"""
        try:
            with open(violation.file_path) as f:
                lines = f.readlines()

            for i, line in enumerate(lines):
                for match in re.finditer(r'(?<!\[.*\]\()https://([^/]+\.s3\.[^/]+\.amazonaws\.com/[^\s\)]+)', line):
                    url = match.group(0)
                    filename = url.split('/')[-1]
                    lines[i] = line.replace(url, f"[{filename}]({url})")

            with open(violation.file_path, 'w') as f:
                f.writelines(lines)

        except Exception:
            pass

    def _fix_shared_model_import(self, violation: Violation):
        """Generate import for shared model"""
        try:
            type_name = violation.details.get("type_name")
            domain = violation.details.get("domain")

            if not type_name or not domain:
                return

            with open(violation.file_path) as f:
                lines = f.readlines()

            # Add import at top
            import_line = f"import {{ {type_name} }} from '@shared/semantic/domains/{domain}/generated/typescript';\n"

            # Find where to insert (after existing imports)
            insert_index = 0
            for i, line in enumerate(lines):
                if line.startswith('import '):
                    insert_index = i + 1

            if import_line not in ''.join(lines):
                lines.insert(insert_index, import_line)

                # Comment out local definition
                for i, line in enumerate(lines):
                    if re.search(rf'(?:interface|type|class)\s+{type_name}\b', line):
                        lines[i] = f"// {line.rstrip()}  // Replaced with shared domain import\n"

                with open(violation.file_path, 'w') as f:
                    f.writelines(lines)

        except Exception:
            pass

    def _load_reminders(self) -> List[Dict]:
        """Load AI reminders from file"""
        if not REMINDERS_FILE.exists():
            return []

        try:
            with open(REMINDERS_FILE) as f:
                return json.load(f)
        except Exception:
            return []

    def _save_reminders(self):
        """Save AI reminders to file"""
        REMINDERS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(REMINDERS_FILE, 'w') as f:
            json.dump(self.reminders, f, indent=2)

    def get_active_reminders(self) -> List[str]:
        """Get all active reminders for AI"""
        return [r["reminder"] for r in self.reminders]

    def clear_reminders_for_file(self, file_path: Path):
        """Clear reminders for a specific file"""
        self.reminders = [r for r in self.reminders if r["file"] != str(file_path)]
        self._save_reminders()


# ============================================================================
# Main Engine
# ============================================================================

class SmartAutoFix:
    """Smart auto-fix engine with severity-based actions"""

    def __init__(self):
        self.detector = ViolationDetector()
        self.handler = ActionHandler()

    def check_file(self, file_path: Path) -> Dict:
        """Check file and return results"""
        violations = self.detector.check_file(file_path)

        results = {
            "file": str(file_path),
            "violations_count": len(violations),
            "ai_reminders": [],
            "user_notifications": [],
            "auto_fixes": []
        }

        for violation in violations:
            message = self.handler.handle_violation(violation)

            rule = VIOLATION_RULES.get(violation.rule_id)
            if not rule:
                continue

            if rule.action == ActionType.AUTO_FIX:
                results["auto_fixes"].append(message)
            elif rule.action == ActionType.REMIND_AI:
                results["ai_reminders"].append(message)
            elif rule.action in (ActionType.NOTIFY_USER, ActionType.BLOCK):
                results["user_notifications"].append(message)

        return results

    def get_ai_context_injection(self) -> str:
        """Get text to inject into AI context"""
        reminders = self.handler.get_active_reminders()

        if not reminders:
            return ""

        context = "\n🤖 ACTIVE GUARDRAIL REMINDERS:\n"
        context += "\n".join(f"  {i+1}. {reminder}" for i, reminder in enumerate(reminders))
        context += "\n\nPlease address these reminders in your response.\n"

        return context


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Smart auto-fix with severity levels")
    parser.add_argument("command", choices=["check", "context", "clear"], help="Command to run")
    parser.add_argument("file", nargs="?", type=Path, help="File to check")

    args = parser.parse_args()

    engine = SmartAutoFix()

    if args.command == "check":
        if not args.file:
            print("Error: file argument required for check command")
            return 1

        results = engine.check_file(args.file)

        # Print results
        if results["auto_fixes"]:
            for fix in results["auto_fixes"]:
                print(fix)

        if results["user_notifications"]:
            for notification in results["user_notifications"]:
                print(notification)

        # Output AI reminders as JSON for easy parsing
        if results["ai_reminders"]:
            print("\n📋 AI Reminders (to be injected into context):")
            for reminder in results["ai_reminders"]:
                print(f"  {reminder}")

        return 0

    elif args.command == "context":
        # Get context injection text for AI
        context = engine.get_ai_context_injection()
        if context:
            print(context)
        return 0

    elif args.command == "clear":
        if args.file:
            engine.handler.clear_reminders_for_file(args.file)
            print(f"✅ Cleared reminders for {args.file}")
        else:
            engine.handler.reminders = []
            engine.handler._save_reminders()
            print("✅ Cleared all reminders")
        return 0


if __name__ == "__main__":
    sys.exit(main())
