#!/usr/bin/env python3
"""
Multi-Context Infrastructure Migration Tool

Migrates existing CDK projects to multi-context, multi-stage infrastructure.
"""

import argparse
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Tuple


class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


def print_header(text: str):
    """Print colored header"""
    print(f"\n{Colors.BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.NC}")
    print(f"{Colors.BLUE}{text}{Colors.NC}")
    print(f"{Colors.BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.NC}\n")


def print_step(step_num: int, total: int, message: str):
    """Print step header"""
    print(f"{Colors.BLUE}[{step_num}/{total}]{Colors.NC} {message}")


def print_success(message: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {message}{Colors.NC}")


def print_warning(message: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.NC}")


def print_error(message: str):
    """Print error message"""
    print(f"{Colors.RED}✗ {message}{Colors.NC}")


class MigrationTool:
    """Main migration tool"""

    def __init__(self, context: str = 'work', project_root: Path = Path.cwd()):
        self.context = context
        self.project_root = project_root
        self.backup_dir = project_root / f".backup-{datetime.now().strftime('%Y%m%d-%H%M')}"
        self.config_dir = project_root / 'config'
        self.golden_repo = self._find_golden_repo()
        self.errors = []
        self.warnings = []

    def _find_golden_repo(self) -> Path | None:
        """Find the golden repo directory"""
        # Try relative path first
        possible_paths = [
            Path(__file__).parent.parent.parent.parent / 'golden-repos' / 'typescript-cdk',
            Path.home() / 'dev' / 'lab' / 'shared' / 'golden-repos' / 'typescript-cdk',
        ]

        for path in possible_paths:
            if path.exists():
                return path

        return None

    def check_prerequisites(self) -> bool:
        """Check if project is suitable for migration"""
        print_step(0, 8, "Checking prerequisites...")

        # Check for config directory
        if not self.config_dir.exists():
            print_error("config/ directory not found")
            print("  Are you in the CDK project root?")
            return False

        # Check for cdk.json
        if not (self.project_root / 'cdk.json').exists():
            print_warning("cdk.json not found. Is this a CDK project?")
            response = input("Continue anyway? (y/N) ").strip().lower()
            if response != 'y':
                return False

        print_success("Prerequisites check passed")
        return True

    def create_backup(self):
        """Create backup of existing configuration"""
        print_step(1, 8, "Creating backup...")

        self.backup_dir.mkdir(parents=True, exist_ok=True)
        backup_config = self.backup_dir / 'config'
        backup_config.mkdir(exist_ok=True)

        # Backup config directory
        if self.config_dir.exists():
            for item in self.config_dir.glob('*.yml'):
                shutil.copy2(item, backup_config)

        # Backup key files
        files_to_backup = [
            ('infra/bin/app.ts', 'app.ts.bak'),
            ('bin/app.ts', 'app.ts.bak'),
            ('Makefile', 'Makefile.bak'),
        ]

        for src, dst in files_to_backup:
            src_path = self.project_root / src
            if src_path.exists():
                shutil.copy2(src_path, self.backup_dir / dst)

        print_success(f"Backup created: {self.backup_dir}")

    def create_context_directory(self):
        """Create context directory structure"""
        print_step(2, 8, "Creating context directory...")

        context_dir = self.config_dir / self.context
        context_dir.mkdir(parents=True, exist_ok=True)

        print_success(f"Created config/{self.context}/")

    def move_configs(self) -> int:
        """Move existing YAML configs to context directory"""
        print_step(3, 8, "Moving existing configurations...")

        context_dir = self.config_dir / self.context
        moved_count = 0

        for yml_file in self.config_dir.glob('*.yml'):
            if yml_file.is_file():
                dest = context_dir / yml_file.name
                shutil.move(str(yml_file), str(dest))
                print(f"  Moved: {yml_file.name} → config/{self.context}/{yml_file.name}")
                moved_count += 1

        if moved_count == 0:
            print_warning("No .yml files found to move")
        else:
            print_success(f"Moved {moved_count} config files")

        return moved_count

    def update_schema(self):
        """Update schema.ts with multi-context support"""
        print_step(4, 8, "Updating schema.ts...")

        schema_path = self.config_dir / 'schema.ts'

        if not schema_path.exists():
            print_warning("config/schema.ts not found")
            return

        # Backup original
        shutil.copy2(schema_path, self.backup_dir / 'schema.ts.bak')

        # Check if already migrated
        content = schema_path.read_text()
        if 'export type Context = string' in content:
            print_warning("schema.ts already appears to be migrated")
            return

        # Try to copy from golden repo
        if self.golden_repo:
            golden_schema = self.golden_repo / 'config' / 'schema.ts'
            if golden_schema.exists():
                shutil.copy2(golden_schema, schema_path)
                print_success("Updated schema.ts (from local golden repo)")
                return

        print_warning("Could not find golden repo schema.ts")
        print("   Please manually update config/schema.ts")
        self.warnings.append("schema.ts needs manual update")

    def update_loader(self):
        """Update loader.ts with multi-context support"""
        print_step(5, 8, "Updating loader.ts...")

        loader_path = self.config_dir / 'loader.ts'

        if not loader_path.exists():
            print_warning("config/loader.ts not found")
            return

        # Backup original
        shutil.copy2(loader_path, self.backup_dir / 'loader.ts.bak')

        # Check if already migrated
        content = loader_path.read_text()
        if 'getContext()' in content:
            print_warning("loader.ts already appears to be migrated")
            return

        # Try to copy from golden repo
        if self.golden_repo:
            golden_loader = self.golden_repo / 'config' / 'loader.ts'
            if golden_loader.exists():
                shutil.copy2(golden_loader, loader_path)
                print_success("Updated loader.ts (from local golden repo)")
                return

        print_warning("Could not find golden repo loader.ts")
        print("   Please manually update config/loader.ts")
        self.warnings.append("loader.ts needs manual update")

    def update_app(self):
        """Update bin/app.ts with multi-context support"""
        print_step(6, 8, "Updating bin/app.ts...")

        # Try both possible locations
        app_paths = [
            self.project_root / 'infra' / 'bin' / 'app.ts',
            self.project_root / 'bin' / 'app.ts',
        ]

        app_path = None
        for path in app_paths:
            if path.exists():
                app_path = path
                break

        if not app_path:
            print_warning("bin/app.ts not found")
            return

        # Check if already migrated
        content = app_path.read_text()
        if 'config.context' in content:
            print_warning("bin/app.ts already appears to be migrated")
            return

        # Update imports
        content = content.replace('getEnvironment', 'getContext, getStage')

        # Update console.log
        content = content.replace(
            "console.log(`\\n🚀 Deploying to: ${config.env.toUpperCase()}`);",
            "console.log(`\\n🚀 Deploying Infrastructure`);\n"
            "console.log(`   Context: ${config.context}`);\n"
            "console.log(`   Stage: ${config.stage}`);"
        )

        app_path.write_text(content)
        print_success("Updated bin/app.ts")

    def update_makefile(self):
        """Update Makefile with multi-context support"""
        print_step(7, 8, "Updating Makefile...")

        makefile_path = self.project_root / 'Makefile'

        if makefile_path.exists():
            # Backup original
            shutil.copy2(makefile_path, self.backup_dir / 'Makefile.bak')

            # Check if already migrated
            content = makefile_path.read_text()
            if 'CONTEXT ?=' in content:
                print_warning("Makefile already appears to be migrated")
                return

        # Try to copy from golden repo
        if self.golden_repo:
            golden_makefile = self.golden_repo / 'Makefile'
            if golden_makefile.exists():
                shutil.copy2(golden_makefile, makefile_path)
                print_success("Updated Makefile (from local golden repo)")
                return

        print_warning("Could not find golden repo Makefile")
        print("   Please manually update Makefile with CONTEXT and STAGE support")
        self.warnings.append("Makefile needs manual update")

    def verify_migration(self) -> Tuple[int, int]:
        """Verify the migration was successful"""
        print_step(8, 8, "Verifying migration...")

        errors = 0
        warnings = 0

        # Check config directory structure
        context_dir = self.config_dir / self.context
        if not context_dir.exists():
            print_error(f"config/{self.context}/ directory missing")
            errors += 1
        else:
            print_success(f"config/{self.context}/ exists")

        # Check for YAML files
        yml_count = len(list(context_dir.glob('*.yml')))
        if yml_count == 0:
            print_error(f"No .yml files in config/{self.context}/")
            errors += 1
        else:
            print_success(f"Found {yml_count} config files")

        # Check schema.ts
        schema_path = self.config_dir / 'schema.ts'
        if schema_path.exists():
            content = schema_path.read_text()
            if 'export type Context' in content:
                print_success("schema.ts updated")
            else:
                print_warning("schema.ts may need manual update")
                warnings += 1

        # Check loader.ts
        loader_path = self.config_dir / 'loader.ts'
        if loader_path.exists():
            content = loader_path.read_text()
            if 'getContext()' in content:
                print_success("loader.ts updated")
            else:
                print_warning("loader.ts may need manual update")
                warnings += 1

        # Check Makefile
        makefile_path = self.project_root / 'Makefile'
        if makefile_path.exists():
            content = makefile_path.read_text()
            if 'CONTEXT ?=' in content:
                print_success("Makefile updated")
            else:
                print_warning("Makefile may need manual update")
                warnings += 1

        return errors, warnings

    def print_next_steps(self):
        """Print next steps for the user"""
        print_header("Next Steps")

        print("1. List available configs:")
        print(f"   {Colors.GREEN}make infra-list{Colors.NC}\n")

        print("2. Test synthesis (doesn't deploy):")
        print(f"   {Colors.GREEN}CONTEXT={self.context} STAGE=dev npx cdk synth{Colors.NC}\n")

        print("3. Deploy to dev:")
        print(f"   {Colors.GREEN}make infra-deploy CONTEXT={self.context} STAGE=dev{Colors.NC}\n")

        print("4. Check status:")
        print(f"   {Colors.GREEN}make infra-status CONTEXT={self.context} STAGE=dev{Colors.NC}\n")

        print("Rollback instructions (if needed):")
        print(f"   {Colors.YELLOW}cp -r {self.backup_dir}/config/* config/{Colors.NC}")
        print(f"   {Colors.YELLOW}cp {self.backup_dir}/app.ts.bak infra/bin/app.ts{Colors.NC}")
        print(f"   {Colors.YELLOW}cp {self.backup_dir}/Makefile.bak Makefile{Colors.NC}\n")

    def run(self) -> int:
        """Run the migration"""
        print_header(f"🚀 Multi-Context Infrastructure Migration\n\nTarget context: {self.context}")

        # Check prerequisites
        if not self.check_prerequisites():
            return 1

        # Run migration steps
        try:
            self.create_backup()
            self.create_context_directory()
            moved = self.move_configs()
            self.update_schema()
            self.update_loader()
            self.update_app()
            self.update_makefile()
            errors, warnings = self.verify_migration()

            # Print results
            print()
            print_header("Migration Results")

            if errors == 0 and warnings == 0:
                print_success("Migration Complete!")
            elif errors == 0:
                print_warning(f"Migration completed with {warnings} warnings")
            else:
                print_error(f"Migration completed with {errors} errors and {warnings} warnings")

            self.print_next_steps()

            return 0 if errors == 0 else 1

        except Exception as e:
            print_error(f"Migration failed: {e}")
            import traceback
            traceback.print_exc()
            return 1


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Migrate CDK project to multi-context infrastructure',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Migrate to 'work' context (default)
  python migrate-to-multi-context.py

  # Migrate to 'personal' context
  python migrate-to-multi-context.py --context personal

  # Migrate project in different directory
  python migrate-to-multi-context.py --project-root /path/to/project
        """
    )

    parser.add_argument(
        '--context',
        default='work',
        help='Target context name (default: work)'
    )

    parser.add_argument(
        '--project-root',
        type=Path,
        default=Path.cwd(),
        help='CDK project root directory (default: current directory)'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without making changes'
    )

    args = parser.parse_args()

    if args.dry_run:
        print_warning("DRY RUN MODE - No changes will be made")
        print()

    tool = MigrationTool(
        context=args.context,
        project_root=args.project_root
    )

    return tool.run()


if __name__ == '__main__':
    sys.exit(main())
