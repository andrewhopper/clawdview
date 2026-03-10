"""Show command - display domain details."""

import click
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

from ..registry import Registry

console = Console()


@click.command()
@click.argument("name")
@click.option("--schema", is_flag=True, help="Show full schema YAML")
@click.pass_context
def show(ctx: click.Context, name: str, schema: bool) -> None:
    """Show details for a specific domain.

    NAME is the domain name (e.g., 'auth', 'finance', 'email').
    """
    registry: Registry = ctx.obj["registry"]
    domain = registry.get_domain(name)

    if domain is None:
        console.print(f"[red]Domain '{name}' not found.[/red]")
        console.print("\nRun [cyan]domain list[/cyan] to see available domains.")
        raise SystemExit(1)

    if schema:
        _show_schema(registry, name)
        return

    # Build domain info panel
    status_color = {"production": "green", "development": "yellow", "deprecated": "red"}.get(
        domain.status, "white"
    )

    info_lines = [
        f"[bold]Version:[/bold]     {domain.version}",
        f"[bold]Status:[/bold]      [{status_color}]{domain.status}[/{status_color}]",
        f"[bold]Owner:[/bold]       {domain.owner}",
        f"[bold]Description:[/bold] {domain.description}",
    ]

    # Dependencies
    if domain.dependencies:
        deps = (
            ", ".join(domain.dependencies)
            if isinstance(domain.dependencies, list)
            else ", ".join(domain.dependencies)
        )
        info_lines.append(f"[bold]Dependencies:[/bold] {deps}")

    console.print(Panel("\n".join(info_lines), title=f"[cyan]{domain.name}[/cyan]", expand=False))

    # Entities table
    if domain.entities:
        table = Table(title="Entities", show_header=False, box=None)
        table.add_column("Entity", style="green")

        # Show in columns (3 per row)
        for i in range(0, len(domain.entities), 3):
            row = domain.entities[i : i + 3]
            while len(row) < 3:
                row.append("")
            table.add_row(*row)

        console.print(table)

    # Actions table
    if domain.actions:
        table = Table(title="Actions", show_header=False, box=None)
        table.add_column("Action", style="yellow")

        for i in range(0, len(domain.actions), 3):
            row = domain.actions[i : i + 3]
            while len(row) < 3:
                row.append("")
            table.add_row(*row)

        console.print(table)

    # Enums table
    if domain.enums:
        table = Table(title="Enums", show_header=False, box=None)
        table.add_column("Enum", style="magenta")

        for i in range(0, len(domain.enums), 3):
            row = domain.enums[i : i + 3]
            while len(row) < 3:
                row.append("")
            table.add_row(*row)

        console.print(table)

    # Schema path hint
    schema_path = registry.get_domain_schema_path(name)
    if schema_path:
        console.print(f"\n[dim]Schema: {schema_path.relative_to(registry.domains_root)}[/dim]")
        console.print("[dim]Use --schema to view full schema[/dim]")


def _show_schema(registry: Registry, name: str) -> None:
    """Show full schema YAML for domain."""
    schema_path = registry.get_domain_schema_path(name)

    if schema_path is None:
        console.print(f"[yellow]No schema file found for '{name}'[/yellow]")
        return

    with open(schema_path) as f:
        content = f.read()

    syntax = Syntax(content, "yaml", theme="monokai", line_numbers=True)
    console.print(Panel(syntax, title=f"[cyan]{schema_path.name}[/cyan]", expand=False))
