"""
terminal.py — Rich terminal output for Startup.OS dashboard.
Provides a styled console view and an animated live-feed demo.
"""

import time
import random
import sys

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.columns import Columns
    from rich.text import Text
    from rich.live import Live
    from rich.layout import Layout
    from rich import box
    RICH = True
except ImportError:
    RICH = False


console = Console() if RICH else None


# ── Helpers ───────────────────────────────────────────────────────────────
def _fmt_usd(n: int) -> str:
    return f"${n:,.0f}"

def _pct(n: float, arrow: bool = True) -> str:
    sign = "▲" if n >= 0 else "▼"
    return f"{sign} {abs(n):.1f}%" if arrow else f"{n:.1f}%"


# ── Metric card (plain text fallback) ─────────────────────────────────────
def _plain_card(label, value, sub, growth):
    sign = "+" if growth >= 0 else ""
    print(f"  {label}")
    print(f"    {value}  ({sign}{growth:.1f}%)")
    print(f"    {sub}\n")


# ── Main dashboard ─────────────────────────────────────────────────────────
def print_dashboard(metrics, transactions, monthly, products):
    if not RICH:
        _plain_dashboard(metrics, transactions, monthly, products)
        return

    console.rule("[bold cyan]STARTUP.OS  ·  Performance Console[/bold cyan]")
    console.print(f"  [dim]As of {metrics['as_of']}  ·  Fiscal Year 2025[/dim]\n")

    # ── KPI row ──
    kpi_panels = [
        Panel(
            f"[bold green]{_fmt_usd(metrics['revenue_ytd'])}[/bold green]\n"
            f"[dim]{_fmt_usd(metrics['revenue_mom'])} this month[/dim]\n"
            f"[cyan]{_pct(metrics['revenue_growth'])} YoY[/cyan]",
            title="[bold]Revenue YTD[/bold]", border_style="green"
        ),
        Panel(
            f"[bold blue]{_fmt_usd(metrics['profit_ytd'])}[/bold blue]\n"
            f"[dim]{metrics['profit_margin']:.1f}% margin[/dim]\n"
            f"[cyan]{_pct(metrics['profit_growth'])} YoY[/cyan]",
            title="[bold]Net Profit YTD[/bold]", border_style="blue"
        ),
        Panel(
            f"[bold red]{_fmt_usd(metrics['expenses_ytd'])}[/bold red]\n"
            f"[dim]Burn under control[/dim]\n"
            f"[cyan]{_pct(metrics['expenses_growth'])} YoY[/cyan]",
            title="[bold]Expenses YTD[/bold]", border_style="red"
        ),
        Panel(
            f"[bold yellow]{_fmt_usd(metrics['cac'])}[/bold yellow]\n"
            f"[dim]per new customer[/dim]\n"
            f"[cyan]{_pct(metrics['cac_growth'])} MoM[/cyan]",
            title="[bold]CAC (Current)[/bold]", border_style="yellow"
        ),
    ]
    console.print(Columns(kpi_panels, equal=True))

    # ── Revenue by product ──
    console.print("\n[bold]Revenue by Product — Current Quarter[/bold]")
    prod_table = Table(box=box.SIMPLE, show_header=True, header_style="bold dim")
    prod_table.add_column("Product",  style="cyan",  no_wrap=True)
    prod_table.add_column("Amount",   style="green", justify="right")
    prod_table.add_column("Share",    style="white", justify="right")
    prod_table.add_column("Bar",      style="dim",   no_wrap=True)
    for p in products:
        bar = "█" * (p["share"] // 3)
        prod_table.add_row(p["name"], _fmt_usd(p["amount"]), f"{p['share']}%", bar)
    console.print(prod_table)

    # ── Monthly sparkline ──
    console.print("[bold]Revenue — Last 12 Months (sparkline)[/bold]")
    vals = [m["revenue"] for m in monthly]
    lo, hi = min(vals), max(vals)
    blocks = " ▁▂▃▄▅▆▇█"
    spark  = "".join(blocks[int((v - lo) / (hi - lo) * 8)] for v in vals)
    console.print(f"  [green]{spark}[/green]  "
                  f"[dim]{monthly[0]['month']} → {monthly[-1]['month']}[/dim]\n")

    # ── Transactions ──
    print_summary(metrics, transactions)


def print_summary(metrics, transactions):
    if not RICH:
        print("\nRecent Transactions:")
        for tx in transactions[:6]:
            print(f"  {tx['id']}  {tx['customer']:<18} ${tx['amount']:>6,}  {tx['status']}")
        return

    console.print("[bold]Recent Transactions — Live Feed[/bold]")
    tx_table = Table(box=box.SIMPLE_HEAD, show_header=True, header_style="bold dim")
    tx_table.add_column("ID",       style="dim",    no_wrap=True)
    tx_table.add_column("Customer", style="white",  no_wrap=True)
    tx_table.add_column("Product",  style="cyan",   no_wrap=True)
    tx_table.add_column("Amount",   style="green",  justify="right")
    tx_table.add_column("Status",   justify="center")

    STATUS_STYLE = {"paid": "bold green", "pending": "yellow", "failed": "bold red"}
    for tx in transactions[:8]:
        style = STATUS_STYLE.get(tx["status"], "white")
        tx_table.add_row(
            tx["id"], tx["customer"], tx["product"],
            _fmt_usd(tx["amount"]),
            Text(tx["status"], style=style),
        )
    console.print(tx_table)
    console.rule("[dim]STARTUP.OS · v1.0 · All figures simulated for demo purposes[/dim]")


# ── Animated demo ──────────────────────────────────────────────────────────
def run_demo(metrics, transactions, monthly):
    if not RICH:
        print("Install `rich` for the animated demo: pip install rich")
        print_dashboard_plain(metrics, transactions)
        return

    console.rule("[bold cyan]STARTUP.OS · LIVE DEMO[/bold cyan]")
    console.print("[dim]Streaming simulated transactions...[/dim]\n")
    time.sleep(0.5)

    products_list = ["Filly Suite Pro", "Aegis Enterprise", "Filly API", "Aegis Standard"]
    customers     = ["Northwind Labs", "Helio Studio", "Vector Capital",
                     "Quantum Forge", "Lumen Works", "Ridge & Co."]
    statuses      = ["paid", "paid", "paid", "pending", "failed"]
    tx_id         = 9242

    STATUS_STYLE = {"paid": "bold green", "pending": "yellow", "failed": "bold red"}

    for i in range(10):
        status  = random.choice(statuses)
        amount  = random.choice([690, 890, 1290, 2400, 3200, 4800])
        product = random.choice(products_list)
        cust    = random.choice(customers)
        s_style = STATUS_STYLE[status]

        console.print(
            f"  [dim]TX-{tx_id + i}[/dim]  "
            f"[white]{cust:<18}[/white]  "
            f"[cyan]{product:<22}[/cyan]  "
            f"[green]{_fmt_usd(amount):>8}[/green]  "
            f"[{s_style}]{status}[/{s_style}]"
        )
        time.sleep(random.uniform(0.3, 0.9))

    console.print()
    console.rule("[dim]End of demo stream[/dim]")
    console.print()
    print_summary(metrics, transactions[:5])


# ── Plain fallback ─────────────────────────────────────────────────────────
def _plain_dashboard(metrics, transactions, monthly, products):
    print("\n" + "=" * 60)
    print("  STARTUP.OS — Performance Console")
    print("=" * 60)
    print(f"  As of {metrics['as_of']}\n")

    _plain_card("Revenue YTD",  _fmt_usd(metrics["revenue_ytd"]),
                f"{_fmt_usd(metrics['revenue_mom'])} this month",
                metrics["revenue_growth"])
    _plain_card("Net Profit YTD", _fmt_usd(metrics["profit_ytd"]),
                f"{metrics['profit_margin']}% margin",
                metrics["profit_growth"])
    _plain_card("Expenses YTD", _fmt_usd(metrics["expenses_ytd"]),
                "Burn under control",
                metrics["expenses_growth"])
    _plain_card("CAC", _fmt_usd(metrics["cac"]),
                "per new customer",
                metrics["cac_growth"])

    print("\nRevenue by Product:")
    for p in products:
        print(f"  {p['name']:<20}  {_fmt_usd(p['amount'])}  ({p['share']}%)")

    print("\nRecent Transactions:")
    for tx in transactions[:6]:
        print(f"  {tx['id']}  {tx['customer']:<18}  ${tx['amount']:>6,}  {tx['status']}")
    print("\n" + "=" * 60)
