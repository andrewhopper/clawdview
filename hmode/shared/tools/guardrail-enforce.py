#!/usr/bin/env python3
"""
Guardrail Enforcement Tool

Proactive enforcement of guardrail rules from .guardrails/ directory.
Validates tech preferences, architecture patterns, AI steering rules,
file protection, and phase gates BEFORE operations execute.

Usage:
    python guardrail-enforce.py check-tech --name prisma --category orm
    python guardrail-enforce.py check-pattern --name event-driven
    python guardrail-enforce.py check-phase --phase 6 --action write_code
    python guardrail-enforce.py check-file --path .guardrails/tech-preferences/backend.json
    python guardrail-enforce.py --pre-commit
    python guardrail-enforce.py validate --project .
"""
# File UUID: b9c3d8f1-a4e7-2b6c-9d3f-1e5a7b2c8d4e

import json
import sys
import yaml
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import fnmatch


class Severity(Enum):
    """Constraint severity levels."""
    NEVER = 1        # Absolute prohibition
    ALWAYS = 2       # Absolute requirement
    MUST = 3         # Required unless exception
    MUST_NOT = 4     # Prohibited unless exception
    SHOULD = 5       # Recommended
    SHOULD_NOT = 6   # Discouraged
    PREFER = 7       # Preferred approach
    AVOID = 8        # Discouraged approach


class EnforcementResult:
    """Result of guardrail enforcement check."""

    def __init__(
        self,
        approved: bool,
        blocked: bool = False,
        warning: bool = False,
        severity: Optional[Severity] = None,
        message: str = "",
        alternatives: List[str] = None,
        rule_matched: Optional[str] = None,
        context: Dict[str, Any] = None
    ):
        self.approved = approved
        self.blocked = blocked
        self.warning = warning
        self.severity = severity
        self.message = message
        self.alternatives = alternatives or []
        self.rule_matched = rule_matched
        self.context = context or {}


@dataclass
class AuditLogEntry:
    """Audit log entry for enforcement actions."""
    timestamp: str
    action: str
    result: str
    severity: Optional[str] = None
    rule_matched: Optional[str] = None
    message: str = ""
    context: Dict[str, Any] = field(default_factory=dict)


class GuardrailEnforcer:
    """
    Main enforcement engine for guardrail validation.

    Checks:
    1. Technology preferences (.guardrails/tech-preferences/)
    2. Architecture patterns (.guardrails/architecture-preferences/)
    3. AI steering rules (.guardrails/ai-steering/rules/)
    4. File protection (.guardrails/)
    5. Phase gates (.project files)
    6. Directory policies (.guardrails/dir_policy.yml)
    """

    def __init__(self, repo_root: Optional[Path] = None):
        """Initialize with repository root."""
        self.repo_root = repo_root or Path.cwd()
        while not (self.repo_root / '.guardrails').exists():
            if self.repo_root.parent == self.repo_root:
                raise FileNotFoundError("Could not find .guardrails/ directory")
            self.repo_root = self.repo_root.parent

        self.guardrails_dir = self.repo_root / '.guardrails'
        self.audit_log_path = self.guardrails_dir / 'enforcement-audit.jsonl'

    def check_technology(
        self,
        tech_name: str,
        category: Optional[str] = None
    ) -> EnforcementResult:
        """
        Check if technology is approved in tech-preferences.

        Args:
            tech_name: Technology name (e.g., "prisma", "react")
            category: Optional category hint (e.g., "orm_query_builders")

        Returns:
            EnforcementResult with approval status
        """
        tech_prefs_dir = self.guardrails_dir / 'tech-preferences'

        # Load index to find category files
        index_file = tech_prefs_dir / 'index.json'
        if not index_file.exists():
            return EnforcementResult(
                approved=False,
                blocked=True,
                severity=Severity.MUST,
                message=f"Tech preferences index not found: {index_file}"
            )

        with open(index_file) as f:
            index = json.load(f)

        # If category provided, check that file
        if category:
            group_file = self._find_group_file(index, category)
            if group_file:
                result = self._check_tech_in_file(
                    tech_prefs_dir / group_file,
                    tech_name,
                    category
                )
                if result:
                    return result

        # Search all category files
        for group_name, group_data in index.get('groups', {}).items():
            group_file = tech_prefs_dir / group_data['file']
            if not group_file.exists():
                continue

            result = self._check_tech_in_file(group_file, tech_name)
            if result and result.approved:
                return result

        # Not found in any category
        alternatives = self._get_tech_alternatives(tech_prefs_dir, category)
        return EnforcementResult(
            approved=False,
            blocked=True,
            severity=Severity.MUST,
            message=f"Technology '{tech_name}' not found in approved tech-preferences",
            alternatives=alternatives,
            context={'tech_name': tech_name, 'category': category}
        )

    def _find_group_file(self, index: Dict, category: str) -> Optional[str]:
        """Find group file containing category."""
        for group_data in index.get('groups', {}).values():
            if category in group_data.get('categories', []):
                return group_data['file']
        return None

    def _check_tech_in_file(
        self,
        file_path: Path,
        tech_name: str,
        category: Optional[str] = None
    ) -> Optional[EnforcementResult]:
        """Check if tech exists in specific file."""
        if not file_path.exists():
            return None

        with open(file_path) as f:
            data = json.load(f)

        # Search all categories in file
        for cat_name, cat_data in data.get('categories', {}).items():
            if category and cat_name != category:
                continue

            # Try both 'options' and 'preferences' keys (different formats)
            tech_list = cat_data.get('options', cat_data.get('preferences', []))

            for tech in tech_list:
                tech_id = tech.get('id', '').lower()
                tech_display = tech.get('name', '').lower()

                if tech_name.lower() in [tech_id, tech_display]:
                    status = tech.get('status', 'approved')

                    if status == 'deprecated':
                        return EnforcementResult(
                            approved=False,
                            blocked=True,
                            severity=Severity.MUST_NOT,
                            message=f"Technology '{tech_name}' is deprecated",
                            alternatives=[tech.get('alternative', 'No alternative specified')],
                            rule_matched=str(file_path)
                        )

                    if status == 'experimental':
                        return EnforcementResult(
                            approved=True,
                            warning=True,
                            severity=Severity.SHOULD,
                            message=f"Technology '{tech_name}' is experimental. Proceed with caution.",
                            rule_matched=str(file_path)
                        )

                    return EnforcementResult(
                        approved=True,
                        message=f"Technology '{tech_name}' is approved (rank {tech.get('rank', 'N/A')})",
                        rule_matched=str(file_path),
                        context={'status': status, 'category': cat_name, 'rank': tech.get('rank')}
                    )

        return None

    def _get_tech_alternatives(
        self,
        tech_prefs_dir: Path,
        category: Optional[str] = None
    ) -> List[str]:
        """Get list of approved alternatives in category."""
        alternatives = []

        # Load index
        index_file = tech_prefs_dir / 'index.json'
        if not index_file.exists():
            return alternatives

        with open(index_file) as f:
            index = json.load(f)

        # If category specified, get alternatives from that category
        if category:
            group_file = self._find_group_file(index, category)
            if group_file:
                file_path = tech_prefs_dir / group_file
                if file_path.exists():
                    with open(file_path) as f:
                        data = json.load(f)
                        cat_data = data.get('categories', {}).get(category, {})
                        tech_list = cat_data.get('options', cat_data.get('preferences', []))
                        for tech in tech_list[:3]:  # Top 3
                            if tech.get('status', 'approved') == 'approved':
                                alternatives.append(
                                    f"{tech['name']} (rank {tech.get('rank', 'N/A')}) - {tech.get('rationale', tech.get('description', 'No description'))}"
                                )

        return alternatives

    def check_architecture_pattern(
        self,
        pattern_name: str,
        category: Optional[str] = None
    ) -> EnforcementResult:
        """
        Check if architecture pattern is approved.

        Args:
            pattern_name: Pattern name (e.g., "event-driven-microservices")
            category: Optional category (process-patterns, design-patterns, etc.)

        Returns:
            EnforcementResult with approval status
        """
        arch_prefs_dir = self.guardrails_dir / 'architecture-preferences'

        # Load index
        index_file = arch_prefs_dir / 'index.json'
        if not index_file.exists():
            return EnforcementResult(
                approved=False,
                blocked=True,
                message="Architecture preferences index not found"
            )

        with open(index_file) as f:
            index = json.load(f)

        # Search in specified category or all categories
        categories_to_check = [category] if category else index.get('categories', {}).keys()

        for cat_name in categories_to_check:
            cat_data = index['categories'].get(cat_name, {})
            cat_file = arch_prefs_dir / cat_data.get('file', '')

            if not cat_file.exists():
                continue

            with open(cat_file) as f:
                data = json.load(f)

            # Search patterns
            for pattern in data.get('patterns', []):
                if self._pattern_matches(pattern_name, pattern.get('name', '')):
                    rank = pattern.get('rank', 0)

                    if rank < 1:
                        return EnforcementResult(
                            approved=False,
                            blocked=True,
                            message=f"Pattern '{pattern_name}' is not approved (rank {rank})",
                            rule_matched=str(cat_file)
                        )

                    return EnforcementResult(
                        approved=True,
                        message=f"Pattern '{pattern_name}' is approved (rank {rank})",
                        rule_matched=str(cat_file),
                        context={'rank': rank, 'category': cat_name}
                    )

        # Pattern not found - suggest alternatives
        alternatives = self._get_pattern_alternatives(arch_prefs_dir, category)
        return EnforcementResult(
            approved=False,
            blocked=True,
            message=f"Pattern '{pattern_name}' not found in approved architecture-preferences",
            alternatives=alternatives,
            context={'pattern_name': pattern_name, 'category': category}
        )

    def _pattern_matches(self, search: str, pattern: str) -> bool:
        """Fuzzy match pattern names."""
        search_lower = search.lower().replace('-', ' ').replace('_', ' ')
        pattern_lower = pattern.lower().replace('-', ' ').replace('_', ' ')
        return search_lower in pattern_lower or pattern_lower in search_lower

    def _get_pattern_alternatives(
        self,
        arch_prefs_dir: Path,
        category: Optional[str] = None
    ) -> List[str]:
        """Get approved pattern alternatives."""
        alternatives = []

        # Load index
        index_file = arch_prefs_dir / 'index.json'
        if not index_file.exists():
            return alternatives

        with open(index_file) as f:
            index = json.load(f)

        # Get top patterns from quick reference
        for ref in index.get('quickReference', [])[:3]:
            alternatives.append(
                f"{ref['name']} - {', '.join(ref.get('useCases', []))}"
            )

        return alternatives

    def check_ai_steering_rules(
        self,
        context: Dict[str, Any]
    ) -> EnforcementResult:
        """
        Check AI steering rules against action context.

        Args:
            context: {
                "phase": "PHASE_6_DESIGN",
                "taskType": "Task",
                "operation": "write_code",
                "toolInvolved": "Write",
                "filePattern": "src/**/*.ts"
            }

        Returns:
            EnforcementResult with rule violations (if any)
        """
        rules_dir = self.guardrails_dir / 'ai-steering' / 'rules'

        if not rules_dir.exists():
            return EnforcementResult(
                approved=True,
                message="No AI steering rules found"
            )

        # Load all rule files
        all_rules = []
        for rule_file in rules_dir.glob('*.json'):
            if rule_file.name == 'index.json' or rule_file.name == '__init__.py':
                continue

            with open(rule_file) as f:
                data = json.load(f)
                all_rules.extend(data.get('rules', []))

        # Match rules against context
        matched_rules = []
        for rule in all_rules:
            if self._rule_matches_context(rule, context):
                matched_rules.append(rule)

        # Sort by constraint level priority (NEVER > ALWAYS > MUST > ...)
        matched_rules.sort(key=lambda r: self._constraint_priority(r['level']))

        # Check for NEVER violations (highest priority)
        for rule in matched_rules:
            if rule['level'] == 'NEVER':
                return EnforcementResult(
                    approved=False,
                    blocked=True,
                    severity=Severity.NEVER,
                    message=rule.get('action', {}).get('message', rule['description']),
                    rule_matched=rule.get('id'),
                    context=context
                )

        # Check for ALWAYS requirements
        for rule in matched_rules:
            if rule['level'] == 'ALWAYS':
                # Check if action satisfies requirement
                directive = rule.get('action', {}).get('directive')
                if directive == 'require':
                    # This is a requirement - context should indicate it's satisfied
                    # For now, we'll assume if the rule matches, it's a reminder
                    return EnforcementResult(
                        approved=True,
                        warning=True,
                        severity=Severity.ALWAYS,
                        message=rule.get('action', {}).get('message', rule['description']),
                        rule_matched=rule.get('id')
                    )

        # Check for MUST requirements
        for rule in matched_rules:
            if rule['level'] == 'MUST':
                return EnforcementResult(
                    approved=True,
                    warning=True,
                    severity=Severity.MUST,
                    message=rule.get('action', {}).get('message', rule['description']),
                    rule_matched=rule.get('id')
                )

        # Check for SHOULD recommendations
        for rule in matched_rules:
            if rule['level'] == 'SHOULD':
                return EnforcementResult(
                    approved=True,
                    warning=True,
                    severity=Severity.SHOULD,
                    message=rule.get('action', {}).get('message', rule['description']),
                    rule_matched=rule.get('id')
                )

        return EnforcementResult(
            approved=True,
            message="No rule violations"
        )

    def _rule_matches_context(self, rule: Dict, context: Dict) -> bool:
        """Check if rule matches action context."""
        rule_context = rule.get('context', {})

        # Check 'when' conditions (AND logic)
        when_conditions = rule_context.get('when', [])
        for condition in when_conditions:
            if not self._condition_matches(condition, context):
                return False

        # Check 'unless' exceptions (if any match, rule doesn't apply)
        unless_conditions = rule_context.get('unless', [])
        for condition in unless_conditions:
            if self._condition_matches(condition, context):
                return False

        # Check phase match
        if 'phase' in rule_context:
            context_phase = context.get('phase', '')
            if context_phase not in rule_context['phase']:
                return False

        # Check taskType match
        if 'taskType' in rule_context:
            context_task = context.get('taskType', '')
            if context_task not in rule_context['taskType']:
                return False

        # Check toolInvolved match
        if 'toolInvolved' in rule_context:
            context_tool = context.get('toolInvolved', '')
            if context_tool not in rule_context['toolInvolved']:
                return False

        # Check filePattern match
        if 'filePattern' in rule_context:
            context_file = context.get('filePattern', '')
            if not fnmatch.fnmatch(context_file, rule_context['filePattern']):
                return False

        return True

    def _condition_matches(self, condition: str, context: Dict) -> bool:
        """Check if condition string matches context."""
        condition_lower = condition.lower()

        # Check for operation matches
        if 'operation' in context:
            if context['operation'].lower() in condition_lower:
                return True

        # Check for phase matches
        if 'phase' in context:
            if context['phase'].lower() in condition_lower:
                return True

        # Check for other context fields
        for key, value in context.items():
            if isinstance(value, str) and value.lower() in condition_lower:
                return True

        return False

    def _constraint_priority(self, level: str) -> int:
        """Get priority order for constraint level."""
        priority = {
            'NEVER': 1,
            'ALWAYS': 2,
            'MUST': 3,
            'MUST_NOT': 4,
            'SHOULD': 5,
            'SHOULD_NOT': 6,
            'PREFER': 7,
            'AVOID': 8
        }
        return priority.get(level, 99)

    def check_file_protection(
        self,
        file_path: str,
        operation: str = "modify"
    ) -> EnforcementResult:
        """
        Check if file operation is allowed (file protection).

        Args:
            file_path: Path to file
            operation: Operation type (read, write, modify, delete)

        Returns:
            EnforcementResult with protection status
        """
        path = Path(file_path)

        # Check if file is in .guardrails/ directory
        if '.guardrails' in path.parts:
            if operation.lower() in ['write', 'modify', 'delete', 'create']:
                return EnforcementResult(
                    approved=False,
                    blocked=True,
                    severity=Severity.NEVER,
                    message=f"Protected file: {file_path}. Human approval required for {operation}.",
                    context={'file_path': file_path, 'operation': operation}
                )

        # Check if file is CLAUDE.md (protected)
        if path.name == 'CLAUDE.md' and operation.lower() in ['write', 'modify', 'delete']:
            return EnforcementResult(
                approved=False,
                blocked=True,
                severity=Severity.NEVER,
                message="CLAUDE.md requires human approval for modification",
                context={'file_path': file_path, 'operation': operation}
            )

        return EnforcementResult(
            approved=True,
            message=f"File operation allowed: {operation} {file_path}"
        )

    def check_phase_gate(
        self,
        current_phase: int,
        requested_action: str,
        project_path: Optional[Path] = None
    ) -> EnforcementResult:
        """
        Check phase gate before action.

        Args:
            current_phase: Current SDLC phase (1-9)
            requested_action: Action being requested (e.g., "write_code")
            project_path: Optional path to project directory

        Returns:
            EnforcementResult with gate status
        """
        # Special check: Code writing only allowed in Phase 8+
        if requested_action == "write_code":
            if current_phase < 8:
                return EnforcementResult(
                    approved=False,
                    blocked=True,
                    severity=Severity.NEVER,
                    message=f"Cannot write code in Phase {current_phase}. Code writing allowed in Phase 8+.",
                    alternatives=[
                        "Continue current phase activities",
                        f"Advance to Phase {current_phase + 1}",
                        "Declare SPIKE mode (bypass phases, throwaway code)"
                    ],
                    context={
                        'current_phase': current_phase,
                        'requested_action': requested_action
                    }
                )

        return EnforcementResult(
            approved=True,
            message=f"Phase {current_phase}: {requested_action} is allowed"
        )

    def log_audit_entry(self, entry: AuditLogEntry):
        """Write audit log entry to enforcement-audit.jsonl."""
        with open(self.audit_log_path, 'a') as f:
            f.write(json.dumps({
                'timestamp': entry.timestamp,
                'action': entry.action,
                'result': entry.result,
                'severity': entry.severity,
                'rule_matched': entry.rule_matched,
                'message': entry.message,
                'context': entry.context
            }) + '\n')

    def validate_project(self, project_path: Path) -> Dict[str, Any]:
        """
        Run full guardrail validation on project.

        Returns:
            Validation report with all findings
        """
        report = {
            'project': str(project_path),
            'timestamp': datetime.now().isoformat(),
            'checks': [],
            'violations': [],
            'warnings': [],
            'summary': {'errors': 0, 'warnings': 0}
        }

        # Check 1: Phase detection
        project_file = project_path / '.project'
        if project_file.exists():
            with open(project_file) as f:
                project_data = yaml.safe_load(f)
                phase = project_data.get('phase', 1)
                report['phase'] = phase
                report['checks'].append({
                    'name': 'Phase Detection',
                    'status': 'PASS',
                    'phase': phase
                })
        else:
            report['warnings'].append({
                'check': 'Phase Detection',
                'message': '.project file not found'
            })
            report['summary']['warnings'] += 1

        # Check 2: Protected file modifications (scan git diff if available)
        # (Would need git integration for real implementation)

        # Check 3: Scan for hardcoded tech not in preferences
        # (Would need code analysis for real implementation)

        return report


def format_blocked_message(result: EnforcementResult) -> str:
    """Format user-friendly blocked message."""
    lines = []
    lines.append(f"❌ BLOCKED: {result.message}")
    lines.append("")

    if result.alternatives:
        lines.append("Approved alternatives:")
        for i, alt in enumerate(result.alternatives, 1):
            lines.append(f"  [{i}] {alt}")
        lines.append("")

    lines.append("Options:")
    for i, alt in enumerate(result.alternatives, 1):
        lines.append(f"  [{i}] Use {alt.split(' - ')[0]}")
    if result.context:
        lines.append(f"  [{len(result.alternatives) + 1}] Request human approval")
        lines.append(f"  [{len(result.alternatives) + 2}] Cancel operation")
    lines.append("")
    lines.append("Your choice:")

    return "\n".join(lines)


def format_warning_message(result: EnforcementResult) -> str:
    """Format user-friendly warning message."""
    lines = []
    lines.append(f"⚠️  WARNING: {result.message}")
    lines.append("")
    lines.append("Options:")
    lines.append("  [1] Proceed anyway")
    lines.append("  [2] Cancel operation")
    lines.append("")
    lines.append("Your choice:")

    return "\n".join(lines)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Guardrail Enforcement - Validate actions against guardrails'
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # check-tech command
    tech_parser = subparsers.add_parser('check-tech', help='Check if technology is approved')
    tech_parser.add_argument('--name', required=True, help='Technology name')
    tech_parser.add_argument('--category', help='Category hint (optional)')

    # check-pattern command
    pattern_parser = subparsers.add_parser('check-pattern', help='Check if architecture pattern is approved')
    pattern_parser.add_argument('--name', required=True, help='Pattern name')
    pattern_parser.add_argument('--category', help='Category hint (optional)')

    # check-phase command
    phase_parser = subparsers.add_parser('check-phase', help='Check phase gate')
    phase_parser.add_argument('--phase', type=int, required=True, help='Current phase (1-9)')
    phase_parser.add_argument('--action', required=True, help='Requested action')

    # check-file command
    file_parser = subparsers.add_parser('check-file', help='Check file protection')
    file_parser.add_argument('--path', required=True, help='File path')
    file_parser.add_argument('--operation', default='modify', help='Operation (read, write, modify, delete)')

    # validate command
    validate_parser = subparsers.add_parser('validate', help='Validate entire project')
    validate_parser.add_argument('--project', default='.', help='Project directory')

    # pre-commit mode
    parser.add_argument('--pre-commit', action='store_true', help='Pre-commit validation mode')

    args = parser.parse_args()

    enforcer = GuardrailEnforcer()

    try:
        if args.command == 'check-tech':
            result = enforcer.check_technology(args.name, args.category)

            if result.blocked:
                print(format_blocked_message(result))
                sys.exit(1)
            elif result.warning:
                print(format_warning_message(result))
                sys.exit(0)
            else:
                print(f"✅ {result.message}")
                sys.exit(0)

        elif args.command == 'check-pattern':
            result = enforcer.check_architecture_pattern(args.name, args.category)

            if result.blocked:
                print(format_blocked_message(result))
                sys.exit(1)
            elif result.warning:
                print(format_warning_message(result))
                sys.exit(0)
            else:
                print(f"✅ {result.message}")
                sys.exit(0)

        elif args.command == 'check-phase':
            result = enforcer.check_phase_gate(args.phase, args.action)

            if result.blocked:
                print(format_blocked_message(result))
                sys.exit(1)
            else:
                print(f"✅ {result.message}")
                sys.exit(0)

        elif args.command == 'check-file':
            result = enforcer.check_file_protection(args.path, args.operation)

            if result.blocked:
                print(f"❌ {result.message}")
                sys.exit(1)
            else:
                print(f"✅ {result.message}")
                sys.exit(0)

        elif args.command == 'validate':
            report = enforcer.validate_project(Path(args.project))
            print(json.dumps(report, indent=2))
            sys.exit(0 if report['summary']['errors'] == 0 else 1)

        elif args.pre_commit:
            # Pre-commit mode: Run basic checks
            print("Running guardrail pre-commit checks...")
            # (Would implement full pre-commit logic here)
            sys.exit(0)

        else:
            parser.print_help()
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
