"""CLI entry point using Click."""

import click
from rich.console import Console

from .commands.greet import greet
from .commands.process import process
from .config import get_settings
from .logging_config import configure_logging, get_logger

console = Console()


@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
@click.pass_context
def cli(ctx: click.Context, verbose: bool) -> None:
    """Gold standard Python CLI template."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose

    settings = get_settings()
    configure_logging(settings, verbose=verbose)


# Register commands
cli.add_command(greet)
cli.add_command(process)


def main() -> None:
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
