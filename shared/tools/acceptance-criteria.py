#!/usr/bin/env python3
"""
Acceptance Criteria Verification Tool

Auto-generate and verify task completion criteria.
"""
# File UUID: 9a1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d

import sys
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional
import argparse
from datetime import datetime

# Add shared libs to path
sys.path.insert(0, str(Path(__file__).parent.parent / "libs"))

from ask-human import ask_human


class AcceptanceCriteria:
    """Manage acceptance criteria for task verification."""

    def __init__(self, context: Dict[str, Any]):
        """
        Initialize with task context.

        Args:
            context: Task context including:
                - task_type: Type of task (html, api, deployment, etc.)
                - files_affected: List of files created/modified
                - description: Human-readable task description
        """
        self.context = context
        self.criteria: List[Dict[str, Any]] = []

    def generate_criteria(self) -> List[Dict[str, Any]]:
        """Generate acceptance criteria based on context."""
        task_type = self.context.get('task_type', 'unknown')

        # Load appropriate template
        if task_type == 'html':
            self.criteria = self._html_criteria()
        elif task_type == 'api':
            self.criteria = self._api_criteria()
        elif task_type == 'deployment':
            self.criteria = self._deployment_criteria()
        elif task_type == 'code':
            self.criteria = self._code_criteria()
        elif task_type == 'bugfix':
            self.criteria = self._bugfix_criteria()
        else:
            self.criteria = self._generic_criteria()

        return self.criteria

    def _html_criteria(self) -> List[Dict[str, Any]]:
        """Criteria for HTML file generation."""
        file_path = self.context['files_affected'][0]

        return [
            {
                'id': '1',
                'name': 'File renders in browser',
                'type': 'automated',
                'command': f"open -a 'Google Chrome' {file_path}",
                'success': 'Browser opens without errors'
            },
            {
                'id': '2',
                'name': 'No console errors',
                'type': 'manual',
                'prompt': 'Open browser console. Are there any errors?'
            },
            {
                'id': '3',
                'name': 'Design tokens used (no raw hex)',
                'type': 'automated',
                'command': f"grep -n '#[0-9a-fA-F]{{6}}' {file_path}",
                'success': 'No matches found'
            },
            {
                'id': '4',
                'name': 'Interactive elements work',
                'type': 'manual',
                'prompt': 'Test all buttons, forms, and interactive elements'
            },
            {
                'id': '5',
                'name': 'Responsive on mobile/desktop',
                'type': 'manual',
                'prompt': 'Resize browser window. Does layout adapt correctly?'
            }
        ]

    def _api_criteria(self) -> List[Dict[str, Any]]:
        """Criteria for API deployment."""
        api_url = self.context.get('api_url', 'http://localhost:8000')

        return [
            {
                'id': '1',
                'name': 'Endpoint is accessible',
                'type': 'automated',
                'command': f"curl -I {api_url}",
                'success': 'HTTP/2 200'
            },
            {
                'id': '2',
                'name': 'Health check passes',
                'type': 'automated',
                'command': f"curl {api_url}/health",
                'success': '"status":"ok"'
            },
            {
                'id': '3',
                'name': 'Auth required for protected routes',
                'type': 'automated',
                'command': f"curl -I {api_url}/protected",
                'success': 'HTTP/2 401'
            },
            {
                'id': '4',
                'name': 'Test key user flows',
                'type': 'manual',
                'prompt': 'Test primary user workflows end-to-end'
            }
        ]

    def _deployment_criteria(self) -> List[Dict[str, Any]]:
        """Criteria for infrastructure deployment."""
        stack_name = self.context.get('stack_name', '')
        domain = self.context.get('domain', '')

        criteria = []

        if stack_name:
            criteria.append({
                'id': '1',
                'name': 'CloudFormation stack deployed',
                'type': 'automated',
                'command': f"aws cloudformation describe-stacks --stack-name {stack_name} --query 'Stacks[0].StackStatus' --output text",
                'success': 'CREATE_COMPLETE'
            })

        if domain:
            criteria.extend([
                {
                    'id': '2',
                    'name': 'DNS resolves',
                    'type': 'automated',
                    'command': f"dig {domain} +short",
                    'success': 'Returns IP address'
                },
                {
                    'id': '3',
                    'name': 'URL accessible',
                    'type': 'automated',
                    'command': f"curl -I https://{domain}",
                    'success': 'HTTP/2 200'
                },
                {
                    'id': '4',
                    'name': 'Git hash matches deployed version',
                    'type': 'automated',
                    'command': f"curl -s https://{domain}/buildinfo.json | jq -r .git_hash",
                    'success': 'Matches current commit'
                }
            ])

        criteria.append({
            'id': '5',
            'name': 'Core functionality works',
            'type': 'manual',
            'prompt': 'Test main features in deployed environment'
        })

        return criteria

    def _code_criteria(self) -> List[Dict[str, Any]]:
        """Criteria for code changes."""
        return [
            {
                'id': '1',
                'name': 'All tests pass',
                'type': 'automated',
                'command': 'npm test',
                'success': 'All tests passed'
            },
            {
                'id': '2',
                'name': 'Linting passes',
                'type': 'automated',
                'command': 'npm run lint',
                'success': 'No issues found'
            },
            {
                'id': '3',
                'name': 'Type checking passes',
                'type': 'automated',
                'command': 'npm run typecheck',
                'success': 'No errors'
            },
            {
                'id': '4',
                'name': 'Feature works as expected',
                'type': 'manual',
                'prompt': 'Test the new feature manually'
            }
        ]

    def _bugfix_criteria(self) -> List[Dict[str, Any]]:
        """Criteria for bug fixes."""
        return [
            {
                'id': '1',
                'name': 'Original bug no longer reproduces',
                'type': 'manual',
                'prompt': 'Try to reproduce the original bug'
            },
            {
                'id': '2',
                'name': 'All tests pass',
                'type': 'automated',
                'command': 'npm test',
                'success': 'All tests passed'
            },
            {
                'id': '3',
                'name': 'Related features still work',
                'type': 'manual',
                'prompt': 'Test related functionality to ensure no side effects'
            }
        ]

    def _generic_criteria(self) -> List[Dict[str, Any]]:
        """Generic criteria when type is unknown."""
        return [
            {
                'id': '1',
                'name': 'Task completed as described',
                'type': 'manual',
                'prompt': 'Does the output match what was requested?'
            },
            {
                'id': '2',
                'name': 'No errors or warnings',
                'type': 'manual',
                'prompt': 'Check for any errors or unexpected behavior'
            }
        ]

    def present_criteria(self) -> List[str]:
        """Present criteria to user and get selection."""
        if not self.criteria:
            self.generate_criteria()

        # Build options for ask_human
        options = [
            {
                'id': criterion['id'],
                'label': criterion['name'],
                'description': f"{criterion['type'].upper()}: {criterion.get('prompt', criterion.get('command', ''))[:100]}"
            }
            for criterion in self.criteria
        ]

        # Ask user to select criteria
        result = ask_human('multi-choice', {
            'title': f"Acceptance Criteria - {self.context.get('description', 'Task Verification')}",
            'description': 'Select which criteria to verify (uncheck to skip)',
            'options': options
        })

        return result['selected']

    def execute_verification(self, selected_ids: List[str]) -> Dict[str, Any]:
        """Execute verification for selected criteria."""
        results = []

        for criterion in self.criteria:
            if criterion['id'] not in selected_ids:
                results.append({
                    'id': criterion['id'],
                    'name': criterion['name'],
                    'status': 'skipped'
                })
                continue

            if criterion['type'] == 'automated':
                result = self._run_automated_check(criterion)
            else:
                result = self._run_manual_check(criterion)

            results.append(result)

        return self._format_results(results)

    def _run_automated_check(self, criterion: Dict[str, Any]) -> Dict[str, Any]:
        """Execute automated verification command."""
        try:
            output = subprocess.run(
                criterion['command'],
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )

            success_indicator = criterion.get('success', '')
            passed = success_indicator in output.stdout or output.returncode == 0

            return {
                'id': criterion['id'],
                'name': criterion['name'],
                'status': 'pass' if passed else 'fail',
                'output': output.stdout[:200],
                'details': output.stderr if not passed else None
            }
        except subprocess.TimeoutExpired:
            return {
                'id': criterion['id'],
                'name': criterion['name'],
                'status': 'error',
                'error': 'Command timed out after 30 seconds'
            }
        except Exception as e:
            return {
                'id': criterion['id'],
                'name': criterion['name'],
                'status': 'error',
                'error': str(e)
            }

    def _run_manual_check(self, criterion: Dict[str, Any]) -> Dict[str, Any]:
        """Prompt user for manual verification."""
        result = ask_human('approve-deny', {
            'title': criterion['name'],
            'description': criterion.get('prompt', 'Verify this criterion manually')
        })

        return {
            'id': criterion['id'],
            'name': criterion['name'],
            'status': 'pass' if result == 'approved' else 'fail',
            'manual': True
        }

    def _format_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Format verification results."""
        total = len(results)
        passed = sum(1 for r in results if r['status'] == 'pass')
        failed = sum(1 for r in results if r['status'] == 'fail')
        skipped = sum(1 for r in results if r['status'] == 'skipped')
        errors = sum(1 for r in results if r['status'] == 'error')

        return {
            'timestamp': datetime.now().isoformat(),
            'total': total,
            'passed': passed,
            'failed': failed,
            'skipped': skipped,
            'errors': errors,
            'pass_rate': round((passed / total * 100) if total > 0 else 0, 1),
            'results': results
        }


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Acceptance Criteria Verification Tool'
    )
    parser.add_argument(
        '--context',
        required=True,
        help='Task context as JSON string'
    )
    parser.add_argument(
        '--output',
        help='Output file for results (JSON)'
    )

    args = parser.parse_args()

    try:
        context = json.loads(args.context)
    except json.JSONDecodeError:
        print("Error: Invalid JSON in --context parameter", file=sys.stderr)
        sys.exit(1)

    # Create acceptance criteria instance
    ac = AcceptanceCriteria(context)

    # Generate criteria
    criteria = ac.generate_criteria()
    print(f"\nGenerated {len(criteria)} acceptance criteria")

    # Present to user and get selection
    selected_ids = ac.present_criteria()

    if not selected_ids:
        print("\nNo criteria selected. Skipping verification.")
        sys.exit(0)

    # Execute verification
    print(f"\nRunning verification for {len(selected_ids)} criteria...")
    verification_results = ac.execute_verification(selected_ids)

    # Print results
    print("\n" + "=" * 50)
    print("Verification Complete")
    print("=" * 50)
    print(f"\nResults: {verification_results['passed']}/{verification_results['total']} passed ({verification_results['pass_rate']}%)")

    if verification_results['passed'] > 0:
        print(f"\n✅ PASSED ({verification_results['passed']}):")
        for r in verification_results['results']:
            if r['status'] == 'pass':
                print(f"  [{r['id']}] {r['name']}")

    if verification_results['failed'] > 0:
        print(f"\n❌ FAILED ({verification_results['failed']}):")
        for r in verification_results['results']:
            if r['status'] == 'fail':
                print(f"  [{r['id']}] {r['name']}")
                if 'details' in r:
                    print(f"      {r['details']}")

    if verification_results['errors'] > 0:
        print(f"\n⚠️  ERRORS ({verification_results['errors']}):")
        for r in verification_results['results']:
            if r['status'] == 'error':
                print(f"  [{r['id']}] {r['name']}")
                print(f"      {r['error']}")

    # Save results if output file specified
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(json.dumps(verification_results, indent=2))
        print(f"\nResults saved to: {output_path}")

    # Exit with appropriate code
    if verification_results['failed'] > 0 or verification_results['errors'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
