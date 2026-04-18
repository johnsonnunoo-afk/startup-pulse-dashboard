"""
analysis/operational.py
========================
Gross margin by product, expense breakdown, headcount efficiency.
"""


EXPENSE_CATEGORIES = {
    "Payroll":       0.55,
    "Infrastructure": 0.12,
    "Marketing":     0.18,
    "G&A":           0.10,
    "Other":         0.05,
}


def gross_margin_by_product(products: list[dict],
                             cost_pct: dict | None = None) -> list[dict]:
    """
    Gross margin per product line.
    cost_pct: dict of {product_name: cogs_as_fraction_of_revenue}
    """
    default_cogs = {
        "Filly Suite":    0.28,
        "Aegis Security": 0.35,
        "Filly API":      0.18,
        "Other":          0.40,
    }
    cogs = cost_pct or default_cogs
    results = []
    for p in products:
        cogs_pct  = cogs.get(p["name"], 0.30)
        cogs_amt  = p["amount"] * cogs_pct
        gp        = p["amount"] - cogs_amt
        gm_pct    = gp / p["amount"] * 100
        results.append({
            "product":    p["name"],
            "revenue":    p["amount"],
            "cogs":       round(cogs_amt),
            "gross_profit": round(gp),
            "margin_pct": round(gm_pct, 1),
        })
    return results


def expense_breakdown(total_expenses: float) -> list[dict]:
    """Split total expenses by category using fixed ratios."""
    return [
        {
            "category": cat,
            "amount":   round(total_expenses * pct),
            "share_pct": round(pct * 100, 1),
        }
        for cat, pct in EXPENSE_CATEGORIES.items()
    ]


def headcount_efficiency(revenue_ytd: float,
                         headcount: int) -> dict:
    """Revenue per employee — higher is better."""
    rev_per_head = revenue_ytd / headcount if headcount else 0
    benchmark    = 150_000          # typical SaaS early-stage benchmark
    health = (
        "excellent" if rev_per_head >= benchmark * 1.5
        else "good"    if rev_per_head >= benchmark
        else "caution" if rev_per_head >= benchmark * 0.6
        else "poor"
    )
    return {
        "revenue_ytd":       revenue_ytd,
        "headcount":         headcount,
        "revenue_per_head":  round(rev_per_head),
        "benchmark":         benchmark,
        "health":            health,
        "vs_benchmark_pct":  round((rev_per_head / benchmark - 1) * 100, 1),
    }
