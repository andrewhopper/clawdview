"""List command - list all domains from registry."""

import click
from rich.console import Console
from rich.table import Table

from ..registry import Registry

console = Console()


@click.command("list")
@click.option(
    "-s",
    "--status",
    type=click.Choice(["production", "development", "deprecated", "all"]),
    default="all",
    help="Filter by status",
)
@click.option("--stats", is_flag=True, help="Show registry statistics")
@click.pass_context
def list_cmd(ctx: click.Context, status: str, stats: bool) -> None:
    """List all registered domain models."""
    registry: Registry = ctx.obj["registry"]

    if stats:
        _show_stats(registry)
        return

    status_filter = None if status == "all" else status
    domains = registry.list_domains(status=status_filter)

    if not domains:
        console.print("[yellow]No domains found.[/yellow]")
        return

    table = Table(title=f"Domain Models ({len(domains)})")
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Version", style="green")
    table.add_column("Status", style="yellow")
    table.add_column("Entities", justify="right")
    table.add_column("Description", max_width=40)

    for domain in domains:
        status_style = _get_status_style(domain.status)
        table.add_row(
            domain.name,
            domain.version,
            f"[{status_style}]{domain.status}[/{status_style}]",
            str(len(domain.entities)),
            domain.description[:40] + "..." if len(domain.description) > 40 else domain.description,
        )

    console.print(table)
    console.print(f"\n[dim]Registry v{registry.version} | Updated: {registry.updated}[/dim]")


def _show_stats(registry: Registry) -> None:
    """Show registry statistics."""
    stats = registry.get_stats()

    console.print("\n[bold]Domain Registry Statistics[/bold]\n")
    console.print(f"  Total domains:  [cyan]{stats['total']}[/cyan]")
    console.print(f"  Production:     [green]{stats['production']}[/green]")
    console.print(f"  Development:    [yellow]{stats['development']}[/yellow]")
    console.print(f"  Deprecated:     [red]{stats['deprecated']}[/red]")
    if stats["other"] > 0:
        console.print(f"  Other:          [dim]{stats['other']}[/dim]")
    console.print(f"\n  Registry version: {registry.version}")
    console.print(f"  Last updated:     {registry.updated}")


def _get_status_style(status: str) -> str:
    """Get Rich style for status."""
    return {
        "production": "green",
        "development": "yellow",
        "deprecated": "red",
    }.get(status, "dim")
