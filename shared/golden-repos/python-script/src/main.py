"""Main entry point for the Python script template."""

import sys
from typing import Annotated, Optional

import typer
from rich.console import Console

from .config import get_settings
from .logging_config import configure_logging, get_logger

app = typer.Typer(
    name="python-script",
    help="Gold standard Python script template",
    add_completion=False,
)
console = Console()


@app.command()
def run(
    input_file: Annotated[
        Optional[str],
        typer.Argument(help="Input file to process"),
    ] = None,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable verbose output"),
    ] = False,
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", "-n", help="Simulate without making changes"),
    ] = False,
) -> None:
    """Run the main script logic."""
    settings = get_settings()

    # Override log level if verbose
    if verbose:
        settings.log_level = "DEBUG"

    configure_logging(settings)
    log = get_logger("main", dry_run=dry_run)

    log.info("Starting script", app_env=settings.app_env)

    try:
        settings.ensure_dirs()

        if input_file:
            log.info("Processing input file", file=input_file)
            # Add your processing logic here
            process_file(input_file, settings, dry_run=dry_run)
        else:
            log.info("No input file provided, running default action")
            # Add default action here

        log.info("Script completed successfully")

    except Exception as e:
        log.exception("Script failed", error=str(e))
        raise typer.Exit(code=1) from e


def process_file(file_path: str, settings, dry_run: bool = False) -> None:
    """Process a single file."""
    log = get_logger("process_file", file=file_path)

    if dry_run:
        log.info("Dry run: would process file")
        return

    # Add your file processing logic here
    log.debug("Processing file")
    console.print(f"[green]Processed:[/green] {file_path}")


@app.command()
def version() -> None:
    """Show version information."""
    console.print("[bold]python-script-template[/bold] v0.1.0")


if __name__ == "__main__":
    app()
