"""
Startup.OS — Performance Dashboard
===================================
A Python showcase of the Startup.OS dashboard metrics.
Generates charts, prints a live terminal console, and exports a report.

Usage:
    python dashboard.py              # Full dashboard
    python dashboard.py --export     # Export charts + PDF report
    python dashboard.py --demo       # Animated terminal demo
    python dashboard.py --loop       # Continuous refresh mode (for Render)
"""

import argparse
import os
import sys
import time
import random
from datetime import datetime, timezone, timedelta

import data
import charts
import terminal


def main():
    parser = argparse.ArgumentParser(
        description="Startup.OS Performance Dashboard"
    )
    parser.add_argument(
        "--export", action="store_true",
        help="Export charts and generate report"
    )
    parser.add_argument(
        "--demo", action="store_true",
        help="Run animated terminal demo"
    )
    parser.add_argument(
        "--loop", action="store_true",
        help="Continuously refresh the dashboard every 60 seconds (for Render)"
    )
    args = parser.parse_args()

    # Load simulated data
    metrics = data.generate_metrics()
    transactions = data.generate_transactions()
    monthly = data.generate_monthly_series()
    products = data.generate_product_revenue()

    if args.demo:
        terminal.run_demo(metrics, transactions, monthly)
    elif args.export:
        print("\n📊  Startup.OS — Exporting charts...\n")
        os.makedirs("output", exist_ok=True)
        charts.plot_revenue_vs_expenses(monthly)
        charts.plot_revenue_by_product(products)
        charts.plot_net_profit(monthly)
        charts.plot_cac_trend(monthly)
        print("\n✅  Charts saved to ./output/")
        terminal.print_summary(metrics, transactions)
    elif args.loop:
        refresh_interval = 60
        print(f"🔄  Startup.OS — Continuous mode (refreshing every {refresh_interval}s)\n")
        while True:
            metrics = data.generate_metrics()
            transactions = data.generate_transactions()
            monthly = data.generate_monthly_series()
            products = data.generate_product_revenue()
            terminal.print_dashboard(metrics, transactions, monthly, products)
            print(f"\n⏳  Next refresh in {refresh_interval}s — {datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}\n")
            sys.stdout.flush()
            time.sleep(refresh_interval)
    else:
        terminal.print_dashboard(metrics, transactions, monthly, products)


if __name__ == "__main__":
    main()
