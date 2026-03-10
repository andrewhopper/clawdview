"""Create command - create new domain from template."""

import shutil
from datetime import datetime
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel

from ..registry import Registry

console = Console()


@click.command()
@click.argument("name")
@click.option("-d", "--description", prompt=True, help="Domain description")
@click.option(
    "-s",
    "--status",
    type=click.Choice(["development", "production"]),
    default="development",
    help="Initial status",
)
@click.option("--dry-run", is_flag=True, help="Show what would be created without creating")
@click.pass_context
def create(
    ctx: click.Context,
    name: str,
    description: str,
    status: str,
    dry_run: bool,
) -> None:
    """Create a new domain from template.

    NAME should be lowercase with hyphens (e.g., 'user-profile', 'inventory').
    """
    registry: Registry = ctx.obj["registry"]
    domains_root: Path = ctx.obj["domains_root"]

    # Validate name format
    if not _is_valid_name(name):
        console.print("[red]Invalid domain name.[/red]")
        console.print("Use lowercase letters, numbers, and hyphens (e.g., 'user-profile')")
        raise SystemExit(1)

    # Check if domain already exists
    if registry.get_domain(name) is not None:
        console.print(f"[red]Domain '{name}' already exists.[/red]")
        raise SystemExit(1)

    target_dir = domains_root / name
    if target_dir.exists():
        console.print(f"[red]Directory '{name}' already exists.[/red]")
        raise SystemExit(1)

    template_dir = domains_root / "_template"
    if not template_dir.exists():
        console.print("[red]Template directory not found.[/red]")
        raise SystemExit(1)

    if dry_run:
        _show_dry_run(name, description, status, target_dir)
        return

    # Copy template
    shutil.copytree(template_dir, target_dir)

    # Update schema.yaml
    schema_path = target_dir / "schema.yaml"
    if schema_path.exists():
        _update_schema(schema_path, name, description, status)

    # Update README.md
    readme_path = target_dir / "README.md"
    if readme_path.exists():
        _update_readme(readme_path, name, description)

    console.print(Panel(
        f"[green]Domain '{name}' created successfully![/green]\n\n"
        f"Location: [cyan]{target_dir.relative_to(domains_root.parent.parent.parent)}[/cyan]\n\n"
        "Next steps:\n"
        f"  1. Edit [cyan]{name}/schema.yaml[/cyan] to define entities\n"
        "  2. Add to [cyan]registry.yaml[/cyan]\n"
        "  3. Run [cyan]domain validate {name}[/cyan] to verify",
        title="Created",
        expand=False
    ))

    # Show registry entry hint
    console.print("\n[dim]Add to registry.yaml:[/dim]")
    console.print(f"""
  {name}:
    status: {status}
    version: "0.1.0"
    description: "{description}"
    owner: platform
    entities: []
""")


def _is_valid_name(name: str) -> bool:
    """Check if domain name is valid."""
    if not name:
        return False
    if name.startswith("-") or name.endswith("-"):
        return False
    return all(c.islower() or c.isdigit() or c == "-" for c in name)


def _show_dry_run(name: str, description: str, status: str, target_dir: Path) -> None:
    """Show what would be created."""
    console.print("[yellow]Dry run - no files created[/yellow]\n")
    console.print(f"Would create domain: [cyan]{name}[/cyan]")
    console.print(f"  Description: {description}")
    console.print(f"  Status: {status}")
    console.print(f"  Directory: {target_dir}")
    console.print("\nFiles that would be created:")
    console.print("  - schema.yaml")
    console.print("  - README.md")


def _update_schema(path: Path, name: str, description: str, status: str) -> None:
    """Update schema.yaml with domain info."""
    content = path.read_text()
    today = datetime.now().strftime("%Y-%m-%d")

    replacements = {
        "DOMAIN_NAME": name,
        "DOMAIN_DESCRIPTION": description,
        "YYYY-MM-DD": today,
        "status: development": f"status: {status}",
    }

    for old, new in replacements.items():
        content = content.replace(old, new)

    path.write_text(content)


def _update_readme(path: Path, name: str, description: str) -> None:
    """Update README.md with domain info."""
    content = path.read_text()

    replacements = {
        "DOMAIN_NAME": name,
        "DOMAIN_DESCRIPTION": description,
    }

    for old, new in replacements.items():
        content = content.replace(old, new)

    path.write_text(content)
