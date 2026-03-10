"""Process command - example async command with progress."""

from pathlib import Path
from time import sleep

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from ..logging_config import get_logger

console = Console()
log = get_logger("process")


@click.command()
@click.argument("files", nargs=-1, required=True, type=click.Path(exists=False))
@click.option("-d", "--dry-run", is_flag=True, help="Show what would be processed")
@click.pass_context
def process(ctx: click.Context, files: tuple[str, ...], dry_run: bool) -> None:
    """Process FILES with progress indication."""
    log.debug("Starting process command", files=files, dry_run=dry_run)

    if dry_run:
        console.print("[yellow]Dry run mode - no changes will be made[/yellow]")
        for file in files:
            console.print(f"  Would process: {file}")
        return

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Processing files...", total=len(files))

        for i, file in enumerate(files):
            progress.update(task, description=f"Processing {file} ({i + 1}/{len(files)})")

            # Simulate processing
            sleep(0.5)
            log.info("Processed file", file=file)

            progress.advance(task)

    console.print(f"[green]Successfully processed {len(files)} files[/green]")
