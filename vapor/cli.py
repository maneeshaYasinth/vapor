import click
from rich.console import Console
from rich.table import Table
from datetime import datetime
from vapor.costs import get_cost_and_usage

console = Console()


@click.group(invoke_without_command=True)
@click.option('--profile', default=None, help='AWS profile name')
@click.pass_context
def main(ctx, profile):
    """vapor — AWS cost visibility in your terminal."""
    if ctx.invoked_subcommand is None:
        run(profile)


def run(profile):
    console.print(f"\n[bold cyan]⚡ vapor[/bold cyan] — [dim]fetching costs...[/dim]\n")

    try:
        groups, total = get_cost_and_usage(profile)
    except Exception as e:
        console.print(f"[bold red]error:[/bold red] {e}")
        return

    if not groups:
        console.print("[yellow]no cost data available for this period.[/yellow]")
        return

    month = datetime.today().strftime('%B %Y')
    table = Table(title=f"AWS Cost Summary — {month}", border_style="cyan")
    table.add_column("Service", style="cyan", no_wrap=True)
    table.add_column("Cost (USD)", justify="right", style="green")

    for group in sorted(groups, key=lambda x: float(x['Metrics']['UnblendedCost']['Amount']), reverse=True):
        service = group['Keys'][0]
        amount = float(group['Metrics']['UnblendedCost']['Amount'])
        if amount > 0.001:
            table.add_row(service, f"${amount:.4f}")

    table.add_section()
    table.add_row("[bold]Total MTD[/bold]", f"[bold green]${total:.4f}[/bold green]")

    console.print(table)