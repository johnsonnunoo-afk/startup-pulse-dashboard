"""
charts.py — Matplotlib chart exports for Startup.OS.
Saves publication-quality PNGs to ./output/
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Theme ──────────────────────────────────────────────────────────────────
BG      = "#0D0F14"
SURFACE = "#161920"
ACCENT1 = "#6EE7B7"   # teal  — revenue
ACCENT2 = "#F87171"   # coral — expenses
ACCENT3 = "#93C5FD"   # blue  — profit
ACCENT4 = "#FCD34D"   # amber — CAC
MUTED   = "#6B7280"
TEXT    = "#E5E7EB"

COLORS_PIE = [ACCENT1, ACCENT3, ACCENT2, MUTED]

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


def _save(name: str):
    path = f"output/{name}.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close()
    print(f"   ✓  {path}")


# ── Chart 1: Revenue vs Expenses ──────────────────────────────────────────
def plot_revenue_vs_expenses(monthly: list[dict]):
    labels   = [m["month"]   for m in monthly]
    revenue  = [m["revenue"] / 1_000 for m in monthly]
    expenses = [m["expenses"]/ 1_000 for m in monthly]
    x = np.arange(len(labels))
    w = 0.38

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.set_facecolor(SURFACE)

    bars_r = ax.bar(x - w/2, revenue,  w, color=ACCENT1, alpha=0.9, label="Revenue")
    bars_e = ax.bar(x + w/2, expenses, w, color=ACCENT2, alpha=0.9, label="Expenses")

    ax.set_title("Revenue vs Expenses — Last 12 Months (USD '000)",
                 fontsize=13, color=TEXT, pad=16)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=35, ha="right", fontsize=8)
    ax.set_ylabel("USD (thousands)")
    ax.yaxis.grid(True)
    ax.set_axisbelow(True)
    ax.legend(framealpha=0)

    _save("01_revenue_vs_expenses")


# ── Chart 2: Revenue by Product (donut) ───────────────────────────────────
def plot_revenue_by_product(products: list[dict]):
    labels  = [p["name"]   for p in products]
    amounts = [p["amount"] for p in products]
    colors  = COLORS_PIE

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_facecolor(BG)
    fig.patch.set_facecolor(BG)

    wedges, texts, autotexts = ax.pie(
        amounts,
        labels=labels,
        colors=colors,
        autopct="%1.0f%%",
        startangle=90,
        pctdistance=0.78,
        wedgeprops={"width": 0.52, "edgecolor": BG, "linewidth": 2},
    )
    for t in texts:
        t.set_color(TEXT)
        t.set_fontsize(11)
    for at in autotexts:
        at.set_color(BG)
        at.set_fontsize(9)
        at.set_fontweight("bold")

    ax.set_title("Revenue by Product — Current Quarter",
                 fontsize=13, color=TEXT, pad=20)

    # centre label
    total = sum(amounts)
    ax.text(0, 0, f"${total/1_000:.0f}K", ha="center", va="center",
            fontsize=20, fontweight="bold", color=TEXT)

    _save("02_revenue_by_product")


# ── Chart 3: Net Profit line ───────────────────────────────────────────────
def plot_net_profit(monthly: list[dict]):
    labels = [m["month"]  for m in monthly]
    profit = [m["profit"] / 1_000 for m in monthly]
    x = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.fill_between(x, profit, alpha=0.18, color=ACCENT3)
    ax.plot(x, profit, color=ACCENT3, linewidth=2.2, marker="o",
            markersize=5, markerfacecolor=BG)

    ax.set_title("Net Profit — Monthly Contribution (USD '000)",
                 fontsize=13, color=TEXT, pad=16)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=35, ha="right", fontsize=8)
    ax.set_ylabel("USD (thousands)")
    ax.yaxis.grid(True)
    ax.set_axisbelow(True)

    _save("03_net_profit")


# ── Chart 4: CAC trend line ───────────────────────────────────────────────
def plot_cac_trend(monthly: list[dict]):
    labels = [m["month"] for m in monthly]
    cac    = [m["cac"]   for m in monthly]
    x = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.fill_between(x, cac, alpha=0.15, color=ACCENT4)
    ax.plot(x, cac, color=ACCENT4, linewidth=2.2, marker="s",
            markersize=5, markerfacecolor=BG)

    ax.set_title("Customer Acquisition Cost — 12-Month Trend (USD)",
                 fontsize=13, color=TEXT, pad=16)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=35, ha="right", fontsize=8)
    ax.set_ylabel("CAC (USD)")
    ax.yaxis.grid(True)
    ax.set_axisbelow(True)

    _save("04_cac_trend")
