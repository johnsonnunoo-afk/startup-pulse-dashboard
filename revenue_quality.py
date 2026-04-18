"""
analysis/revenue_quality.py
============================
MRR/ARR, NRR, revenue concentration, and expansion revenue.
"""


def mrr_arr(monthly_series: list[dict]) -> dict:
    """Most recent MRR and annualised ARR."""
    latest_mrr = monthly_series[-1]["revenue"]
    arr        = latest_mrr * 12
    return {
        "mrr": latest_mrr,
        "arr": arr,
        "arr_label": f"${arr / 1_000_000:.2f}M",
    }


def expansion_revenue(monthly_series: list[dict]) -> list[dict]:
    """
    Simulated expansion revenue (upsell / cross-sell).
    Modelled as 15–25 % of incremental revenue growth MoM.
    """
    rows = []
    for i in range(1, len(monthly_series)):
        delta = monthly_series[i]["revenue"] - monthly_series[i - 1]["revenue"]
        expansion = max(0, round(delta * 0.20))
        rows.append({
            "month":     monthly_series[i]["month"],
            "new_mrr":   monthly_series[i]["revenue"],
            "expansion": expansion,
            "delta":     delta,
        })
    return rows


def revenue_concentration(transactions: list[dict],
                          top_n: int = 3) -> dict:
    """
    How much revenue comes from the top-N customers.
    Risk flag if top-3 > 50 % of total.
    """
    from collections import defaultdict
    customer_rev = defaultdict(float)
    for tx in transactions:
        if tx["status"] == "paid":
            customer_rev[tx["customer"]] += tx["amount"]

    total    = sum(customer_rev.values())
    sorted_c = sorted(customer_rev.items(), key=lambda x: x[1], reverse=True)
    top      = sorted_c[:top_n]
    top_rev  = sum(v for _, v in top)
    pct      = round(top_rev / total * 100, 1) if total else 0

    return {
        "total_revenue":     round(total, 2),
        "top_customers":     [{"customer": k, "revenue": round(v, 2)} for k, v in top],
        "top_n_revenue":     round(top_rev, 2),
        "concentration_pct": pct,
        "risk":              "high" if pct > 50 else "medium" if pct > 35 else "low",
    }


def net_revenue_retention(base_mrr: float, expansion: float,
                          contraction: float, churn: float) -> dict:
    """
    NRR = (base + expansion - contraction - churn) / base.
    Benchmark: > 100 % means growth even without new customers.
    """
    nrr = (base_mrr + expansion - contraction - churn) / base_mrr * 100
    health = (
        "excellent" if nrr >= 120
        else "good"    if nrr >= 100
        else "caution" if nrr >= 85
        else "poor"
    )
    return {
        "nrr_pct":    round(nrr, 1),
        "health":     health,
        "base_mrr":   base_mrr,
        "expansion":  expansion,
        "contraction": contraction,
        "churn_mrr":  churn,
    }
