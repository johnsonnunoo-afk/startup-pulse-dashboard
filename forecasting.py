"""
analysis/forecasting.py
========================
3-scenario revenue forecast, Monte Carlo burn simulation,
and CAC trend extrapolation.
"""

import numpy as np
import random


SCENARIOS = {
    "bear": {"growth_rate": 0.03,  "label": "Bear  🐻", "color": "#F87171"},
    "base": {"growth_rate": 0.07,  "label": "Base  📊", "color": "#93C5FD"},
    "bull": {"growth_rate": 0.12,  "label": "Bull  🚀", "color": "#6EE7B7"},
}


def revenue_forecast(latest_mrr: float, months: int = 12) -> dict:
    """
    Project MRR over N months under bear / base / bull scenarios.
    Returns monthly series for each scenario.
    """
    results = {}
    for key, cfg in SCENARIOS.items():
        series = []
        mrr = latest_mrr
        for i in range(1, months + 1):
            mrr = mrr * (1 + cfg["growth_rate"])
            series.append({"month": i, "mrr": round(mrr)})
        results[key] = {
            "label":       cfg["label"],
            "color":       cfg["color"],
            "growth_rate": cfg["growth_rate"],
            "series":      series,
            "final_mrr":   series[-1]["mrr"],
            "final_arr":   series[-1]["mrr"] * 12,
        }
    return results


def monte_carlo_burn(cash_balance: float, monthly_burn: float,
                     burn_volatility: float = 0.10,
                     simulations: int = 1_000,
                     months: int = 24) -> dict:
    """
    Monte Carlo simulation of cash runway.
    burn_volatility: std dev as fraction of monthly burn (e.g. 0.10 = 10%).
    Returns distribution of runway outcomes.
    """
    rng = np.random.default_rng(42)
    runways = []

    for _ in range(simulations):
        cash    = cash_balance
        ran_out = months  # default: survived full period
        for m in range(months):
            burn = monthly_burn * (1 + rng.normal(0, burn_volatility))
            burn = max(burn, 0)
            cash -= burn
            if cash <= 0:
                ran_out = m + 1
                break
        runways.append(ran_out)

    runways = np.array(runways)
    return {
        "simulations":    simulations,
        "months_horizon": months,
        "p10":            int(np.percentile(runways, 10)),
        "p50":            int(np.percentile(runways, 50)),
        "p90":            int(np.percentile(runways, 90)),
        "mean":           round(float(np.mean(runways)), 1),
        "pct_survive":    round(float(np.mean(runways == months)) * 100, 1),
        "distribution":   runways.tolist(),
    }


def cac_extrapolation(monthly_series: list[dict],
                      forecast_months: int = 6) -> list[dict]:
    """
    Linear regression on historical CAC to project future trend.
    """
    cac_vals = [m["cac"] for m in monthly_series]
    x        = np.arange(len(cac_vals))
    slope, intercept = np.polyfit(x, cac_vals, 1)

    # Historical points
    history = [
        {"month": m["month"], "cac": m["cac"], "type": "actual"}
        for m in monthly_series
    ]

    # Forecast
    last_x = len(cac_vals)
    from datetime import datetime, timedelta
    last_date = datetime.strptime(monthly_series[-1]["month"], "%b %Y")
    forecast = []
    for i in range(1, forecast_months + 1):
        projected_cac = slope * (last_x + i) + intercept
        next_date     = (last_date.replace(day=28) + timedelta(days=4 * i)).replace(day=1)
        # rough month step
        y, mo = divmod(last_date.month - 1 + i, 12)
        next_mo = datetime(last_date.year + y, mo + 1, 1)
        forecast.append({
            "month": next_mo.strftime("%b %Y"),
            "cac":   round(max(0, projected_cac), 2),
            "type":  "forecast",
        })

    return history + forecast
