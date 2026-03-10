"""Greet command - example simple command."""

import click
from rich.console import Console
from rich.panel import Panel

console = Console()


@click.command()
@click.argument("name")
@click.option("-l", "--loud", is_flag=True, help="Greet loudly")
@click.pass_context
def greet(ctx: click.Context, name: str, loud: bool) -> None:
    """Greet a user by NAME."""
    greeting = f"Hello, {name}!"

    if loud:
        console.print(Panel(greeting.upper(), style="bold green"))
    else:
        console.print(f"[green]{greeting}[/green]")
