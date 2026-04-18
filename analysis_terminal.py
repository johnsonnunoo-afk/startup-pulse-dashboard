"""
analysis/analysis_terminal.py
==============================
Rich terminal output for all extended analysis modules.
"""

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.columns import Columns
    from rich.text import Text
    from rich import box
    RICH = True
except ImportError:
    RICH = False

console = Console() if RICH else None

HEALTH_STYLE = {
    "excellent": "bold green",
    "good":      "green",
    "caution":   "yellow",
    "poor":      "bold red",
    "critical":  "bold red",
    "healthy":   "green",
    "weak":      "yellow",
    "high":      "bold red",
    "medium":    "yellow",
    "low":       "green",
    "profitable": "bold green",
}

def _h(val: str) -> str:
    style = HEALTH_STYLE.get(val, "white")
    return f"[{style}]{val.upper()}[/{style}]" if RICH else val.upper()

def _usd(n: float) -> str:
    return f"${n:,.0f}"


# ── Financial Health ───────────────────────────────────────────────────────
def print_financial_health(runway_data, breakeven_data, growth_data):
    if not RICH:
        print(f"\nRunway: {runway_data['months']} months ({runway_data['status']})")
        print(f"Break-even: {breakeven_data['units_needed']} customers / {_usd(breakeven_data['revenue_needed'])}")
        return

    console.rule("[bold cyan]Financial Health[/bold cyan]")

    panels = [
        Panel(
            f"[bold white]{runway_data['months']} months[/bold white]\n"
            f"Safe until [cyan]{runway_data['safe_until']}[/cyan]\n"
            f"Status: {_h(runway_data['status'])}",
            title="💰 Runway", border_style="cyan"
        ),
        Panel(
            f"[bold white]{runway_data['monthly_burn']:,} / mo burn[/bold white]\n"
            f"Cash on hand: [green]{_usd(runway_data['cash_balance'])}[/green]",
            title="🔥 Burn Rate", border_style="red"
        ),
        Panel(
            f"[bold white]{breakeven_data['units_needed']} customers[/bold white]\n"
            f"Revenue: [green]{_usd(breakeven_data['revenue_needed'])}[/green]\n"
            f"Contribution margin: [cyan]{breakeven_data['contribution_margin_pct']}%[/cyan]",
            title="⚖️  Break-Even", border_style="yellow"
        ),
    ]
    console.print(Columns(panels, equal=True))

    # Growth rates table
    console.print("\n[bold]MoM & QoQ Revenue Growth[/bold]")
    t = Table(box=box.SIMPLE, show_header=True, header_style="bold dim")
    t.add_column("Month")
    t.add_column("Revenue", justify="right", style="green")
    t.add_column("MoM %",   justify="right")
    t.add_column("QoQ %",   justify="right")

    for row in growth_data[-6:]:
        mom_str = (f"[green]▲ {row['mom_pct']}%[/green]" if row["mom_pct"] and row["mom_pct"] >= 0
                   else f"[red]▼ {abs(row['mom_pct'])}%[/red]" if row["mom_pct"]
                   else "[dim]—[/dim]")
        qoq_str = (f"[green]▲ {row['qoq_pct']}%[/green]" if row["qoq_pct"] and row["qoq_pct"] >= 0
                   else f"[red]▼ {abs(row['qoq_pct'])}%[/red]" if row["qoq_pct"]
                   else "[dim]—[/dim]")
        t.add_row(row["month"], _usd(row["revenue"]), mom_str, qoq_str)
    console.print(t)


# ── Customer Intelligence ──────────────────────────────────────────────────
def print_customer_intelligence(ltv_data, payback_data, churn_data, cohort):
    if not RICH:
        print(f"\nLTV: {_usd(ltv_data['ltv'])}  CAC: {_usd(ltv_data['cac'])}  Ratio: {ltv_data['ratio']}x")
        print(f"Payback: {payback_data['months']} months")
        return

    console.rule("[bold cyan]Customer Intelligence[/bold cyan]")

    panels = [
        Panel(
            f"LTV  [bold green]{_usd(ltv_data['ltv'])}[/bold green]\n"
            f"CAC  [bold red]{_usd(ltv_data['cac'])}[/bold red]\n"
            f"Ratio [bold yellow]{ltv_data['ratio']}x[/bold yellow]  {_h(ltv_data['health'])}",
            title="📈 LTV : CAC", border_style="green"
        ),
        Panel(
            f"[bold white]{payback_data['months']} months[/bold white]\n"
            f"Monthly GP: [cyan]{_usd(payback_data['monthly_gross_profit'])}[/cyan]\n"
            f"Status: {_h(payback_data['health'])}",
            title="⏱️  Payback Period", border_style="blue"
        ),
        Panel(
            f"Monthly churn: [bold red]{churn_data['monthly_churn_pct']}%[/bold red]\n"
            f"Annual churn:  [red]{churn_data['annual_churn_pct']}%[/red]\n"
            f"ARR at risk:   [yellow]{_usd(churn_data['arr_at_risk'])}[/yellow]",
            title="📉 Churn Risk", border_style="red"
        ),
    ]
    console.print(Columns(panels, equal=True))

    # Cohort retention snapshot
    console.print("\n[bold]Cohort Retention Snapshot[/bold]")
    t = Table(box=box.SIMPLE, show_header=True, header_style="bold dim")
    t.add_column("Month", justify="right")
    t.add_column("Customers", justify="right", style="white")
    t.add_column("Retained %", justify="right")
    t.add_column("Bar", style="dim")

    for r in cohort[::3]:
        pct  = r["retention"]
        bar  = "█" * int(pct / 5)
        col  = "green" if pct > 70 else "yellow" if pct > 40 else "red"
        t.add_row(str(r["month"]), str(r["customers"]),
                  f"[{col}]{pct}%[/{col}]", bar)
    console.print(t)


# ── Revenue Quality ────────────────────────────────────────────────────────
def print_revenue_quality(mrr_data, nrr_data, concentration_data):
    if not RICH:
        print(f"\nMRR: {_usd(mrr_data['mrr'])}  ARR: {mrr_data['arr_label']}")
        print(f"NRR: {nrr_data['nrr_pct']}%  ({nrr_data['health']})")
        return

    console.rule("[bold cyan]Revenue Quality[/bold cyan]")

    panels = [
        Panel(
            f"MRR [bold green]{_usd(mrr_data['mrr'])}[/bold green]\n"
            f"ARR [bold green]{mrr_data['arr_label']}[/bold green]",
            title="📊 MRR / ARR", border_style="green"
        ),
        Panel(
            f"NRR [bold yellow]{nrr_data['nrr_pct']}%[/bold yellow]\n"
            f"Expansion:   [green]+{_usd(nrr_data['expansion'])}[/green]\n"
            f"Churn loss:  [red]-{_usd(nrr_data['churn_mrr'])}[/red]\n"
            f"Health: {_h(nrr_data['health'])}",
            title="🔄 Net Revenue Retention", border_style="yellow"
        ),
        Panel(
            f"Top-3 share: [bold]{concentration_data['concentration_pct']}%[/bold]\n"
            f"Risk: {_h(concentration_data['risk'])}\n"
            f"Top customer: [cyan]{concentration_data['top_customers'][0]['customer']}[/cyan]",
            title="⚠️  Revenue Concentration", border_style="red"
        ),
    ]
    console.print(Columns(panels, equal=True))


# ── Operational ────────────────────────────────────────────────────────────
def print_operational(gm_data, expense_data, hc_data):
    if not RICH:
        print(f"\nRevenue per head: {_usd(hc_data['revenue_per_head'])}")
        return

    console.rule("[bold cyan]Operational Efficiency[/bold cyan]")

    console.print("\n[bold]Gross Margin by Product[/bold]")
    t = Table(box=box.SIMPLE, show_header=True, header_style="bold dim")
    t.add_column("Product", style="cyan")
    t.add_column("Revenue",      justify="right", style="white")
    t.add_column("COGS",         justify="right", style="red")
    t.add_column("Gross Profit", justify="right", style="green")
    t.add_column("Margin %",     justify="right")
    for d in gm_data:
        col = "green" if d["margin_pct"] >= 70 else "yellow" if d["margin_pct"] >= 50 else "red"
        t.add_row(d["product"], _usd(d["revenue"]), _usd(d["cogs"]),
                  _usd(d["gross_profit"]),
                  f"[{col}]{d['margin_pct']}%[/{col}]")
    console.print(t)

    console.print("\n[bold]Headcount Efficiency[/bold]")
    vs = hc_data["vs_benchmark_pct"]
    vs_str = f"[green]+{vs}%[/green]" if vs >= 0 else f"[red]{vs}%[/red]"
    console.print(
        f"  Revenue per head: [bold white]{_usd(hc_data['revenue_per_head'])}[/bold white]  "
        f"vs benchmark {_usd(hc_data['benchmark'])}  ({vs_str})  "
        f"Status: {_h(hc_data['health'])}\n"
    )


# ── Forecasting ────────────────────────────────────────────────────────────
def print_forecasting(forecast, mc, cac_extrap):
    if not RICH:
        for k, sc in forecast.items():
            print(f"{sc['label']}: final ARR ${sc['final_arr']:,}")
        print(f"Monte Carlo P50 runway: {mc['p50']} months")
        return

    console.rule("[bold cyan]Forecasting[/bold cyan]")

    panels = []
    colors = {"bear": "red", "base": "blue", "bull": "green"}
    for key, sc in forecast.items():
        col = colors[key]
        panels.append(Panel(
            f"Growth rate: [{col}]{sc['growth_rate']*100:.0f}% / mo[/{col}]\n"
            f"Final MRR:  [bold]{_usd(sc['final_mrr'])}[/bold]\n"
            f"Final ARR:  [bold]{_usd(sc['final_arr'])}[/bold]",
            title=sc["label"], border_style=col
        ))
    console.print(Columns(panels, equal=True))

    console.print(f"\n[bold]Monte Carlo Burn Simulation[/bold] "
                  f"[dim]({mc['simulations']:,} runs, {mc['months_horizon']}-month horizon)[/dim]")
    console.print(
        f"  P10 (pessimistic): [red]{mc['p10']} months[/red]  "
        f"P50 (median): [yellow]{mc['p50']} months[/yellow]  "
        f"P90 (optimistic): [green]{mc['p90']} months[/green]\n"
        f"  Probability of surviving full horizon: [bold]{mc['pct_survive']}%[/bold]\n"
    )

    console.print("[bold]CAC Forecast (next 6 months)[/bold]")
    t = Table(box=box.SIMPLE, show_header=True, header_style="bold dim")
    t.add_column("Month")
    t.add_column("CAC", justify="right")
    t.add_column("Type")
    for r in cac_extrap[-8:]:
        style = "dim" if r["type"] == "forecast" else "white"
        t.add_row(r["month"], f"[{style}]{_usd(r['cac'])}[/{style}]",
                  "[yellow]forecast[/yellow]" if r["type"] == "forecast" else "[dim]actual[/dim]")
    console.print(t)
