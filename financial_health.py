"""
analysis/financial_health.py
============================
Runway, break-even, and growth rate analysis.
"""

import numpy as np


def runway(cash_balance: float, monthly_burn: float) -> dict:
    """Months of runway remaining at current burn rate."""
    if monthly_burn <= 0:
        return {"months": float("inf"), "status": "profitable"}
    months = cash_balance / monthly_burn
    status = (
        "critical" if months < 6
        else "caution" if months < 12
        else "healthy"
    )
    return {
        "months":        round(months, 1),
        "cash_balance":  cash_balance,
        "monthly_burn":  monthly_burn,
        "status":        status,
        "safe_until":    _months_from_now(months),
    }


def breakeven(fixed_costs: float, variable_cost_pct: float,
              avg_revenue_per_customer: float) -> dict:
    """Units and revenue needed to cover all costs."""
    contribution_margin = avg_revenue_per_customer * (1 - variable_cost_pct)
    if contribution_margin <= 0:
        return {"error": "Contribution margin must be positive"}
    units    = fixed_costs / contribution_margin
    revenue  = units * avg_revenue_per_customer
    return {
        "units_needed":           round(units),
        "revenue_needed":         round(revenue, 2),
        "contribution_margin":    round(contribution_margin, 2),
        "contribution_margin_pct": round((1 - variable_cost_pct) * 100, 1),
    }


def growth_rates(monthly_series: list[dict]) -> list[dict]:
    """MoM and QoQ revenue growth rates."""
    results = []
    for i, m in enumerate(monthly_series):
        mom = None
        qoq = None
        if i >= 1:
            prev = monthly_series[i - 1]["revenue"]
            mom  = round((m["revenue"] - prev) / prev * 100, 1) if prev else None
        if i >= 3:
            prev3 = monthly_series[i - 3]["revenue"]
            qoq   = round((m["revenue"] - prev3) / prev3 * 100, 1) if prev3 else None
        results.append({
            "month":   m["month"],
            "revenue": m["revenue"],
            "mom_pct": mom,
            "qoq_pct": qoq,
        })
    return results


def _months_from_now(n: float) -> str:
    from datetime import datetime, timedelta
    future = datetime.utcnow() + timedelta(days=n * 30)
    return future.strftime("%b %Y")
