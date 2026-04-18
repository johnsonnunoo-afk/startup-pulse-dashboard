"""
analysis/analysis_charts.py
============================
Matplotlib charts for all extended analysis modules.
Saves PNGs to ./output/analysis/
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

BG      = "#0D0F14"
SURFACE = "#161920"
ACCENT1 = "#6EE7B7"
ACCENT2 = "#F87171"
ACCENT3 = "#93C5FD"
ACCENT4 = "#FCD34D"
MUTED   = "#6B7280"
TEXT    = "#E5E7EB"

plt.rcParams.update({
    "figure.facecolor":  BG,
    "axes.facecolor":    SURFACE,
    "axes.edgecolor":    MUTED,
    "axes.labelcolor":   TEXT,
    "xtick.color":       MUTED,
    "ytick.color":       MUTED,
    "text.color":        TEXT,
    "grid.color":        "#1F2937",
    "grid.linestyle":    "--",
    "grid.linewidth":    0.6,
    "font.family":       "monospace",
    "axes.spines.top":   False,
    "axes.spines.right": False,
})

OUT = "output/analysis"


def _save(name):
    os.makedirs(OUT, exist_ok=True)
    path = f"{OUT}/{name}.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close()
    print(f"   ✓  {path}")


# ── 1. Cohort Retention Curve ─────────────────────────────────────────────
def plot_cohort_retention(cohort: list[dict]):
    months     = [r["month"]     for r in cohort]
    retention  = [r["retention"] for r in cohort]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.fill_between(months, retention, alpha=0.18, color=ACCENT1)
    ax.plot(months, retention, color=ACCENT1, linewidth=2.2,
            marker="o", markersize=5, markerfacecolor=BG)
    ax.axhline(50, color=MUTED, linewidth=0.8, linestyle=":")
    ax.set_title("Cohort Retention Curve", fontsize=13, color=TEXT, pad=16)
    ax.set_xlabel("Month")
    ax.set_ylabel("Customers Retained (%)")
    ax.yaxis.grid(True)
    ax.set_axisbelow(True)
    _save("01_cohort_retention")


# ── 2. 3-Scenario Revenue Forecast ───────────────────────────────────────
def plot_revenue_forecast(forecast: dict, historical_mrr: list[float]):
    fig, ax = plt.subplots(figsize=(12, 6))

    # Historical
    hist_x = list(range(-len(historical_mrr), 0))
    ax.plot(hist_x, [v / 1000 for v in historical_mrr],
            color=TEXT, linewidth=1.8, linestyle="--", label="Historical", alpha=0.6)

    # Scenarios
    for key, sc in forecast.items():
        x   = list(range(1, len(sc["series"]) + 1))
        mrr = [m["mrr"] / 1000 for m in sc["series"]]
        ax.plot(x, mrr, color=sc["color"], linewidth=2.2, label=sc["label"])
        ax.fill_between(x, mrr, alpha=0.08, color=sc["color"])
        ax.annotate(f"${sc['final_arr']/1_000_000:.2f}M ARR",
                    xy=(x[-1], mrr[-1]),
                    xytext=(5, 0), textcoords="offset points",
                    color=sc["color"], fontsize=8)

    ax.axvline(0, color=MUTED, linewidth=0.8, linestyle=":")
    ax.set_title("12-Month Revenue Forecast — Bear / Base / Bull",
                 fontsize=13, color=TEXT, pad=16)
    ax.set_xlabel("Months from today")
    ax.set_ylabel("MRR (USD '000)")
    ax.yaxis.grid(True)
    ax.set_axisbelow(True)
    ax.legend(framealpha=0)
    _save("02_revenue_forecast")


# ── 3. Monte Carlo Burn Distribution ─────────────────────────────────────
def plot_monte_carlo(mc: dict):
    dist = np.array(mc["distribution"])

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(dist, bins=40, color=ACCENT3, alpha=0.75, edgecolor=BG)
    ax.axvline(mc["p10"], color=ACCENT2, linewidth=1.5, linestyle="--",
               label=f"P10: {mc['p10']} mo")
    ax.axvline(mc["p50"], color=ACCENT4, linewidth=1.8,
               label=f"P50: {mc['p50']} mo")
    ax.axvline(mc["p90"], color=ACCENT1, linewidth=1.5, linestyle="--",
               label=f"P90: {mc['p90']} mo")

    ax.set_title(f"Monte Carlo Burn Simulation (n={mc['simulations']:,})",
                 fontsize=13, color=TEXT, pad=16)
    ax.set_xlabel("Months until cash runs out")
    ax.set_ylabel("Simulations")
    ax.yaxis.grid(True)
    ax.set_axisbelow(True)
    ax.legend(framealpha=0)
    _save("03_monte_carlo_burn")


# ── 4. Gross Margin by Product ────────────────────────────────────────────
def plot_gross_margin(gm_data: list[dict]):
    products = [d["product"]    for d in gm_data]
    revenue  = [d["revenue"]    for d in gm_data]
    cogs     = [d["cogs"]       for d in gm_data]
    gp       = [d["gross_profit"] for d in gm_data]
    x = np.arange(len(products))
    w = 0.28

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(x - w, revenue, w, color=ACCENT3, alpha=0.85, label="Revenue")
    ax.bar(x,     cogs,    w, color=ACCENT2, alpha=0.85, label="COGS")
    ax.bar(x + w, gp,      w, color=ACCENT1, alpha=0.85, label="Gross Profit")

    for i, d in enumerate(gm_data):
        ax.text(i + w, d["gross_profit"] + 200, f"{d['margin_pct']}%",
                ha="center", fontsize=8, color=ACCENT1)

    ax.set_title("Gross Margin by Product Line", fontsize=13, color=TEXT, pad=16)
    ax.set_xticks(x)
    ax.set_xticklabels(products)
    ax.set_ylabel("USD")
    ax.yaxis.grid(True)
    ax.set_axisbelow(True)
    ax.legend(framealpha=0)
    _save("04_gross_margin_by_product")


# ── 5. Expense Breakdown ──────────────────────────────────────────────────
def plot_expense_breakdown(breakdown: list[dict]):
    cats    = [d["category"]  for d in breakdown]
    amounts = [d["amount"]    for d in breakdown]
    colors  = [ACCENT1, ACCENT3, ACCENT4, ACCENT2, MUTED]

    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    wedges, texts, autotexts = ax.pie(
        amounts, labels=cats, colors=colors,
        autopct="%1.0f%%", startangle=90,
        pctdistance=0.78,
        wedgeprops={"width": 0.52, "edgecolor": BG, "linewidth": 2},
    )
    for t in texts:     t.set_color(TEXT); t.set_fontsize(11)
    for at in autotexts: at.set_color(BG); at.set_fontsize(9); at.set_fontweight("bold")

    ax.set_title("Expense Breakdown by Category", fontsize=13, color=TEXT, pad=20)
    total = sum(amounts)
    ax.text(0, 0, f"${total/1_000:.0f}K", ha="center", va="center",
            fontsize=18, fontweight="bold", color=TEXT)
    _save("05_expense_breakdown")


# ── 6. CAC Extrapolation ──────────────────────────────────────────────────
def plot_cac_extrapolation(series: list[dict]):
    actual   = [s for s in series if s["type"] == "actual"]
    forecast = [s for s in series if s["type"] == "forecast"]

    xa = list(range(len(actual)))
    xf = list(range(len(actual) - 1, len(actual) + len(forecast)))

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(xa, [s["cac"] for s in actual], color=ACCENT4,
            linewidth=2.2, marker="o", markersize=5, markerfacecolor=BG, label="Actual")
    ax.plot(xf, [actual[-1]["cac"]] + [s["cac"] for s in forecast],
            color=ACCENT2, linewidth=2, linestyle="--",
            marker="s", markersize=4, markerfacecolor=BG, label="Forecast")
    ax.axvline(len(actual) - 1, color=MUTED, linewidth=0.8, linestyle=":")

    labels = [s["month"] for s in actual] + [s["month"] for s in forecast]
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=35, ha="right", fontsize=8)
    ax.set_title("CAC Trend & 6-Month Extrapolation", fontsize=13, color=TEXT, pad=16)
    ax.set_ylabel("CAC (USD)")
    ax.yaxis.grid(True)
    ax.set_axisbelow(True)
    ax.legend(framealpha=0)
    _save("06_cac_extrapolation")


# ── 7. LTV:CAC Ratio Visual ───────────────────────────────────────────────
def plot_ltv_cac(ltv_cac_data: dict):
    ltv = ltv_cac_data["ltv"]
    cac = ltv_cac_data["cac"]

    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.barh(["CAC", "LTV"], [cac, ltv],
                   color=[ACCENT2, ACCENT1], alpha=0.85, height=0.4)
    ax.axvline(cac * 3, color=ACCENT4, linewidth=1.5, linestyle="--",
               label="3x CAC benchmark")

    for bar, val in zip(bars, [cac, ltv]):
        ax.text(val + 20, bar.get_y() + bar.get_height() / 2,
                f"${val:,.0f}", va="center", fontsize=11, color=TEXT)

    ratio = ltv_cac_data["ratio"]
    ax.set_title(f"LTV : CAC  =  {ratio:.1f}x  ({ltv_cac_data['health'].upper()})",
                 fontsize=13, color=TEXT, pad=16)
    ax.xaxis.grid(True)
    ax.set_axisbelow(True)
    ax.legend(framealpha=0)
    _save("07_ltv_cac")
