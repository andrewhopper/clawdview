#!/usr/bin/env python3
"""
Contribution workflow handler - creates sandbox and manages GitLab MR process.
File UUID: 7f4d9c2e-8b5a-4f3e-9d1c-6a7e8f4b3c2d
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
import uuid

# Add shared libs to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "shared" / "libs"))


class ContributionWorkflow:
    """Manages the external contribution workflow."""

    def __init__(self, args: Dict[str, Any]):
        self.args = args
        self.sandbox_base = Path("/tmp/claude-contributions")
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load contribution configuration."""
        config_path = Path(__file__).parent / "contribute-config.yaml"
        if config_path.exists():
            import yaml
            with open(config_path) as f:
                return yaml.safe_load(f)
        return self._default_config()

    def _default_config(self) -> Dict[str, Any]:
        """Default configuration if none exists."""
        return {
            "repository": {
                "upstream": {
                    "url": "https://gitlab.com/protoflow/protoflow",
                    "namespace": "protoflow",
                    "project": "protoflow",
                    "default_branch": "main"
                }
            },
            "contributions": {
                "auto_fork": True,
                "branch_prefix": "contrib",
                "require_tests": True,
                "auto_labels": ["contribution", "needs-review"]
            },
            "sandbox": {
                "base_path": "/tmp/claude-contributions",
                "keep_count": 5,
                "auto_clean_after_days": 7
            }
        }

    def run(self) -> Dict[str, Any]:
        """Execute the contribution workflow."""
        try:
            # Create sandbox
            sandbox = self._create_sandbox()
            print(f"✓ Created sandbox: {sandbox}")

            # Clone repository
            self._clone_repo(sandbox)
            print(f"✓ Cloned repository")

            # Create contribution branch
            branch_name = self._create_branch(sandbox)
            print(f"✓ Created branch: {branch_name}")

            # Return context for Claude to continue
            return {
                "status": "ready",
                "sandbox": str(sandbox),
                "branch": branch_name,
                "next_steps": [
                    "Make your changes to the code",
                    "Review changes with 'git diff'",
                    "Commit changes",
                    "Push to fork",
                    "Create merge request"
                ]
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "troubleshooting": self._get_troubleshooting(e)
            }

    def _create_sandbox(self) -> Path:
        """Create isolated sandbox directory."""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        sandbox_id = str(uuid.uuid4())[:8]
        sandbox = self.sandbox_base / f"{timestamp}-{sandbox_id}"
        sandbox.mkdir(parents=True, exist_ok=True)
        return sandbox

    def _clone_repo(self, sandbox: Path) -> None:
        """Clone repository into sandbox."""
        repo_url = self.args.get("repo") or self.config["repository"]["upstream"]["url"]
        subprocess.run(
            ["git", "clone", repo_url, str(sandbox)],
            check=True,
            capture_output=True
        )

    def _create_branch(self, sandbox: Path) -> str:
        """Create contribution branch."""
        prefix = self.config["contributions"]["branch_prefix"]
        date = datetime.now().strftime("%Y%m%d")
        topic = self._generate_topic_slug()
        branch_name = f"{prefix}-{date}-{topic}"

        subprocess.run(
            ["git", "checkout", "-b", branch_name],
            cwd=sandbox,
            check=True,
            capture_output=True
        )

        return branch_name

    def _generate_topic_slug(self) -> str:
        """Generate topic slug from description or type."""
        description = self.args.get("description", "")
        contrib_type = self.args.get("type", "contribution")

        if description:
            # Create slug from description
            slug = description.lower()
            slug = "".join(c if c.isalnum() or c == " " else "" for c in slug)
            slug = "-".join(slug.split()[:4])  # Max 4 words
            return slug
        else:
            return contrib_type

    def _get_troubleshooting(self, error: Exception) -> list:
        """Get troubleshooting steps based on error."""
        error_str = str(error).lower()

        if "authentication" in error_str or "401" in error_str:
            return [
                "Check GitLab personal access token is set",
                "Verify token has correct scopes (api, read_repository, write_repository)",
                "Check token hasn't expired"
            ]
        elif "not found" in error_str or "404" in error_str:
            return [
                "Verify repository URL is correct",
                "Check you have access to the repository",
                "Ensure repository exists"
            ]
        elif "permission" in error_str or "403" in error_str:
            return [
                "Check you have permission to access this repository",
                "Verify token has required scopes",
                "Contact repository owner for access"
            ]
        else:
            return [
                "Check internet connection",
                "Verify GitLab is accessible",
                "Review error message for specific details"
            ]


def main():
    """Main entry point."""
    # Parse arguments from stdin (JSON format from Claude Code)
    if len(sys.argv) > 1:
        # Arguments passed as JSON string
        args = json.loads(sys.argv[1])
    else:
        # Interactive mode
        args = {}

    workflow = ContributionWorkflow(args)
    result = workflow.run()

    # Output result as JSON for Claude Code to parse
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
