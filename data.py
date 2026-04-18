"""
data.py — Simulated business data for Startup.OS dashboard.
All figures are generated for demo purposes.
"""

import random
from datetime import datetime, timedelta


PRODUCTS = [
    {"name": "Filly Suite",     "color": "#6EE7B7"},
    {"name": "Aegis Security",  "color": "#93C5FD"},
    {"name": "Filly API",       "color": "#FCA5A5"},
    {"name": "Other",           "color": "#D1D5DB"},
]

CUSTOMERS = [
    "Northwind Labs", "Helio Studio", "Vector Capital",
    "Quantum Forge",  "Lumen Works",   "Ridge & Co.",
    "Apex Dynamics",  "Nova Systems",  "Drift Analytics",
    "Prism Ventures",
]

STATUSES = ["paid", "paid", "paid", "pending", "failed"]


def generate_metrics():
    """Top-line KPIs matching the live dashboard."""
    return {
        "revenue_ytd":   1_160_500,
        "revenue_mom":      178_400,
        "revenue_growth":      18.4,
        "profit_ytd":      638_800,
        "profit_margin":      55.0,
        "profit_growth":      32.1,
        "expenses_ytd":    521_700,
        "expenses_growth":     6.2,
        "cac":                 156,
        "cac_growth":          9.3,
        "as_of": datetime.utcnow().strftime("%b %d, %H:%M UTC"),
    }


def generate_monthly_series(months: int = 12) -> list[dict]:
    """12-month revenue, expenses, profit, and CAC series."""
    base_revenue  = 70_000
    base_expenses = 40_000
    base_cac      = 130

    series = []
    date = datetime.utcnow().replace(day=1) - timedelta(days=365)

    for i in range(months):
        noise_r = random.uniform(0.95, 1.12)
        noise_e = random.uniform(0.97, 1.05)
        revenue  = int(base_revenue  * (1 + i * 0.04) * noise_r)
        expenses = int(base_expenses * (1 + i * 0.02) * noise_e)
        profit   = revenue - expenses
        cac      = round(base_cac + i * 2.2 + random.uniform(-5, 5), 2)

        series.append({
            "month":    date.strftime("%b %Y"),
            "revenue":  revenue,
            "expenses": expenses,
            "profit":   profit,
            "cac":      cac,
        })
        date = (date.replace(day=28) + timedelta(days=4)).replace(day=1)

    return series


def generate_product_revenue() -> list[dict]:
    """Revenue split by product for current quarter."""
    totals = [78_400, 52_100, 31_200, 16_700]
    total  = sum(totals)
    result = []
    for product, amount in zip(PRODUCTS, totals):
        result.append({
            **product,
            "amount": amount,
            "share":  round(amount / total * 100),
        })
    return result


def generate_transactions(n: int = 12) -> list[dict]:
    """Recent transaction feed."""
    tx_id = 9241
    transactions = []
    prices = [4_800, 1_290, 890, 2_400, 690, 4_800, 3_200, 1_100, 560, 2_950, 780, 4_200]

    for i in range(n):
        product_name = random.choice([p["name"] for p in PRODUCTS[:-1]])
        tier         = random.choice(["", " Pro", " Enterprise", " Standard", " API"])
        transactions.append({
            "id":       f"TX-{tx_id - i}",
            "customer": CUSTOMERS[i % len(CUSTOMERS)],
            "product":  product_name + tier,
            "amount":   prices[i % len(prices)],
            "status":   random.choice(STATUSES),
        })

    return transactions
