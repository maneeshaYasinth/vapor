import click
from rich.console import Console

console = Console()

@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    """vapor — AWS cost visibility in your terminal."""
    if ctx.invoked_subcommand is None:
        console.print("[bold cyan]⚡ vapor[/bold cyan] — AWS cost visibility in your terminal")
        console.print("\nrun [bold]vapor --help[/bold] to see available commands")