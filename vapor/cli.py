import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from datetime import datetime
from vapor.costs import get_cost_and_usage

console = Console()


def get_cost_color(amount):
    if amount == 0:
        return "dim"
    elif amount < 5:
        return "green"
    elif amount < 20:
        return "yellow"
    else:
        return "red"


@click.group(invoke_without_command=True)
@click.option('--profile', default=None, help='AWS profile name')
@click.pass_context
def main(ctx, profile):
    """vapor — AWS cost visibility in your terminal."""
    if ctx.invoked_subcommand is None:
        run(profile)


def run(profile):
    console.print()
    console.print(Panel.fit(
        "[bold cyan]⚡ vapor[/bold cyan]  [dim]AWS cost visibility[/dim]",
        border_style="cyan"
    ))
    console.print()

    try:
        groups, total = get_cost_and_usage(profile)
    except Exception as e:
        console.print(f"[bold red]error:[/bold red] {e}")
        return

    month = datetime.today().strftime('%B %Y')
    table = Table(
        title=f"Cost Summary — {month}",
        border_style="bright_black",
        header_style="bold cyan",
        show_lines=False
    )
    table.add_column("Service", style="white", no_wrap=True, min_width=30)
    table.add_column("Cost (USD)", justify="right", min_width=12)

    visible = [g for g in groups if float(g['Metrics']['UnblendedCost']['Amount']) > 0.001]

    if not visible:
        console.print("[dim]no charges found for this period.[/dim]\n")
    else:
        for group in sorted(visible, key=lambda x: float(x['Metrics']['UnblendedCost']['Amount']), reverse=True):
            service = group['Keys'][0]
            amount = float(group['Metrics']['UnblendedCost']['Amount'])
            color = get_cost_color(amount)
            table.add_row(service, f"[{color}]${amount:.4f}[/{color}]")

    table.add_section()
    total_color = get_cost_color(total)
    table.add_row(
        "[bold white]Total MTD[/bold white]",
        f"[bold {total_color}]${total:.4f}[/bold {total_color}]"
    )

    console.print(table)
    console.print()