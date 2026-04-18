"""
analysis/customer_intelligence.py
==================================
LTV:CAC ratio, churn, cohort retention, and payback period.
"""

import numpy as np


def ltv_cac(avg_revenue_per_customer: float, gross_margin_pct: float,
            monthly_churn_rate: float, cac: float) -> dict:
    """
    LTV:CAC ratio — the core SaaS health metric.
    Benchmark: ratio > 3x is healthy; > 5x is excellent.
    """
    if monthly_churn_rate <= 0:
        ltv = float("inf")
    else:
        avg_lifetime_months = 1 / monthly_churn_rate
        ltv = avg_revenue_per_customer * gross_margin_pct * avg_lifetime_months

    ratio = ltv / cac if cac > 0 else float("inf")
    health = (
        "poor"      if ratio < 1
        else "weak" if ratio < 3
        else "good" if ratio < 5
        else "excellent"
    )
    return {
        "ltv":                    round(ltv, 2),
        "cac":                    round(cac, 2),
        "ratio":                  round(ratio, 2),
        "health":                 health,
        "avg_lifetime_months":    round(1 / monthly_churn_rate, 1) if monthly_churn_rate > 0 else None,
        "gross_margin_pct":       round(gross_margin_pct * 100, 1),
    }


def payback_period(cac: float, avg_monthly_revenue: float,
                   gross_margin_pct: float) -> dict:
    """Months to recover CAC from gross profit."""
    monthly_gp = avg_monthly_revenue * gross_margin_pct
    if monthly_gp <= 0:
        return {"error": "Monthly gross profit must be positive"}
    months = cac / monthly_gp
    health = (
        "excellent" if months < 12
        else "good"    if months < 18
        else "caution" if months < 24
        else "poor"
    )
    return {
        "months":  round(months, 1),
        "health":  health,
        "cac":     round(cac, 2),
        "monthly_gross_profit": round(monthly_gp, 2),
    }


def cohort_retention(initial_customers: int, monthly_churn_rate: float,
                     periods: int = 12) -> list[dict]:
    """Simulate cohort retention curve over N months."""
    rows = []
    remaining = initial_customers
    for i in range(periods + 1):
        churned = round(remaining * monthly_churn_rate) if i > 0 else 0
        remaining = max(0, remaining - churned)
        rows.append({
            "month":      i,
            "customers":  remaining,
            "retention":  round(remaining / initial_customers * 100, 1),
            "churned":    churned,
        })
    return rows


def churn_analysis(monthly_churn_rate: float,
                   arr: float) -> dict:
    """Annual revenue impact of churn."""
    annual_churn_rate = 1 - (1 - monthly_churn_rate) ** 12
    arr_at_risk       = arr * annual_churn_rate
    return {
        "monthly_churn_pct": round(monthly_churn_rate * 100, 2),
        "annual_churn_pct":  round(annual_churn_rate * 100, 1),
        "arr_at_risk":       round(arr_at_risk, 2),
        "arr":               round(arr, 2),
    }
