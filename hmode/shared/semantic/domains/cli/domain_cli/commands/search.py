"""Search command - search domains by keyword."""

import click
from rich.console import Console
from rich.table import Table

from ..registry import Registry

console = Console()


@click.command()
@click.argument("query")
@click.option("-l", "--limit", default=10, help="Max results to show")
@click.pass_context
def search(ctx: click.Context, query: str, limit: int) -> None:
    """Search domains by name, description, or entities.

    QUERY is the search term (case-insensitive).

    Examples:
        domain search payment
        domain search user
        domain search "text to speech"
    """
    registry: Registry = ctx.obj["registry"]
    results = registry.search_domains(query)

    if not results:
        console.print(f"[yellow]No domains found matching '{query}'[/yellow]")
        console.print("\nTry a different search term or run [cyan]domain list[/cyan]")
        return

    # Limit results
    if len(results) > limit:
        results = results[:limit]
        truncated = True
    else:
        truncated = False

    table = Table(title=f"Search Results for '{query}'")
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Status", style="yellow")
    table.add_column("Description", max_width=50)
    table.add_column("Match", style="dim")

    for domain in results:
        # Determine what matched
        match_type = _get_match_type(domain, query)

        status_style = {
            "production": "green",
            "development": "yellow",
            "deprecated": "red",
        }.get(domain.status, "white")

        table.add_row(
            domain.name,
            f"[{status_style}]{domain.status}[/{status_style}]",
            domain.description[:50] + "..." if len(domain.description) > 50 else domain.description,
            match_type,
        )

    console.print(table)

    if truncated:
        console.print(f"\n[dim]Showing {limit} of more results. Use --limit to see more.[/dim]")

    console.print(f"\n[dim]Use [cyan]domain show <name>[/cyan] for details[/dim]")


def _get_match_type(domain, query: str) -> str:
    """Determine what field matched the query."""
    query_lower = query.lower()

    if query_lower in domain.name.lower():
        return "name"

    if query_lower in domain.description.lower():
        return "description"

    for entity in domain.entities:
        if query_lower in entity.lower():
            return f"entity: {entity}"

    return "unknown"
