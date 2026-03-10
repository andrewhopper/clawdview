"""CLI entry point using Click."""

from pathlib import Path

import click
from rich.console import Console

from .commands.create import create
from .commands.list_cmd import list_cmd
from .commands.search import search
from .commands.show import show
from .commands.validate import validate
from .registry import Registry

console = Console()


def get_domains_root() -> Path:
    """Get the domains root directory."""
    # CLI is at shared/semantic/domains/cli/
    # Domains root is shared/semantic/domains/
    return Path(__file__).parent.parent.parent


@click.group()
@click.option(
    "-d",
    "--domains-root",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    help="Override domains root directory",
)
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
@click.pass_context
def cli(ctx: click.Context, domains_root: Path | None, verbose: bool) -> None:
    """Domain Model CLI - manage shared semantic domain models.

    List, search, create, and validate domain models in the shared registry.
    """
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose

    if domains_root is None:
        domains_root = get_domains_root()

    ctx.obj["domains_root"] = domains_root
    ctx.obj["registry"] = Registry(domains_root)


# Register commands
cli.add_command(list_cmd, name="list")
cli.add_command(show)
cli.add_command(search)
cli.add_command(create)
cli.add_command(validate)


def main() -> None:
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
