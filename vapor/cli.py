import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime, timedelta
from vapor.costs import get_cost_and_usage, get_daily_costs, get_forecast

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
@click.option('--forecast', is_flag=True, help='Show month-end forecast')
@click.option('--days', default=None, type=int, help='Show daily breakdown for last N days')
@click.pass_context
def main(ctx, profile, forecast, days):
    """vapor — AWS cost visibility in your terminal."""
    if ctx.invoked_subcommand is None:
        run(profile, forecast, days)


def run(profile, forecast, days):
    console.print()
    console.print(Panel.fit(
        "[bold cyan]⚡ vapor[/bold cyan]  [dim]AWS cost visibility[/dim]",
        border_style="cyan"
    ))
    console.print()

    try:
        # MTD summary
        groups, total = get_cost_and_usage(profile)
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

        if visible:
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

        # forecast row
        if forecast:
            fc = get_forecast(profile)
            if fc is not None:
                fc_color = get_cost_color(fc)
                table.add_row(
                    "[bold white]Forecasted (EOM)[/bold white]",
                    f"[bold {fc_color}]${fc:.4f}[/bold {fc_color}]"
                )

        console.print(table)
        console.print()

        # daily breakdown
        if days:
            daily = get_daily_costs(profile, days)
            daily_table = Table(
                title=f"Daily Breakdown — last {days} days",
                border_style="bright_black",
                header_style="bold cyan"
            )
            daily_table.add_column("Date", style="white", min_width=15)
            daily_table.add_column("Cost (USD)", justify="right", min_width=12)

            for day in daily:
                date = day['TimePeriod']['Start']
                amount = float(day['Total']['UnblendedCost']['Amount'])
                color = get_cost_color(amount)
                daily_table.add_row(date, f"[{color}]${amount:.4f}[/{color}]")

            console.print(daily_table)
            console.print()

    except Exception as e:
        console.print(f"[bold red]error:[/bold red] {e}")