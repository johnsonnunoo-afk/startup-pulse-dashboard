"""
analysis_runner.py
==================
Runs all extended business intelligence analysis for Startup.OS.

Usage:
    python analysis_runner.py              # Terminal output only
    python analysis_runner.py --export     # Terminal + chart exports
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import data
from analysis import financial_health, customer_intelligence
from analysis import revenue_quality, operational, forecasting
from analysis import analysis_terminal as term
from analysis import analysis_charts   as acharts


# ── Assumptions ───────────────────────────────────────────────────────────
CASH_BALANCE          = 2_400_000    # current cash on hand
MONTHLY_BURN          = 43_475       # avg monthly expenses
FIXED_COSTS           = 30_000       # fixed monthly costs
VARIABLE_COST_PCT     = 0.28         # variable cost as % of revenue
AVG_REVENUE_PER_CUST  = 1_290        # avg monthly revenue per customer
GROSS_MARGIN_PCT      = 0.72         # blended gross margin
MONTHLY_CHURN         = 0.025        # 2.5% monthly churn
HEADCOUNT             = 12           # current team size
NRR_EXPANSION         = 8_500
NRR_CONTRACTION       = 2_200
NRR_CHURN_MRR         = 3_800


def main():
    parser = argparse.ArgumentParser(description="Startup.OS Extended Analysis")
    parser.add_argument("--export", action="store_true",
                        help="Export charts to ./output/analysis/")
    args = parser.parse_args()

    # ── Load base data ──
    metrics      = data.generate_metrics()
    transactions = data.generate_transactions(n=50)
    monthly      = data.generate_monthly_series()
    products     = data.generate_product_revenue()

    # ── Run all analyses ──

    # Financial Health
    runway_data    = financial_health.runway(CASH_BALANCE, MONTHLY_BURN)
    breakeven_data = financial_health.breakeven(FIXED_COSTS, VARIABLE_COST_PCT,
                                                AVG_REVENUE_PER_CUST)
    growth_data    = financial_health.growth_rates(monthly)

    # Customer Intelligence
    ltv_data     = customer_intelligence.ltv_cac(AVG_REVENUE_PER_CUST, GROSS_MARGIN_PCT,
                                                  MONTHLY_CHURN, metrics["cac"])
    payback_data = customer_intelligence.payback_period(metrics["cac"],
                                                        AVG_REVENUE_PER_CUST, GROSS_MARGIN_PCT)
    churn_data   = customer_intelligence.churn_analysis(MONTHLY_CHURN, metrics["revenue_ytd"])
    cohort       = customer_intelligence.cohort_retention(200, MONTHLY_CHURN)

    # Revenue Quality
    mrr_data           = revenue_quality.mrr_arr(monthly)
    expansion_data     = revenue_quality.expansion_revenue(monthly)
    concentration_data = revenue_quality.revenue_concentration(transactions)
    nrr_data           = revenue_quality.net_revenue_retention(
                             mrr_data["mrr"], NRR_EXPANSION, NRR_CONTRACTION, NRR_CHURN_MRR)

    # Operational
    gm_data      = operational.gross_margin_by_product(products)
    expense_data = operational.expense_breakdown(metrics["expenses_ytd"])
    hc_data      = operational.headcount_efficiency(metrics["revenue_ytd"], HEADCOUNT)

    # Forecasting
    forecast_data = forecasting.revenue_forecast(mrr_data["mrr"])
    mc_data       = forecasting.monte_carlo_burn(CASH_BALANCE, MONTHLY_BURN)
    cac_extrap    = forecasting.cac_extrapolation(monthly)

    # ── Terminal output ──
    term.print_financial_health(runway_data, breakeven_data, growth_data)
    term.print_customer_intelligence(ltv_data, payback_data, churn_data, cohort)
    term.print_revenue_quality(mrr_data, nrr_data, concentration_data)
    term.print_operational(gm_data, expense_data, hc_data)
    term.print_forecasting(forecast_data, mc_data, cac_extrap)

    # ── Chart exports ──
    if args.export:
        print("\n📊  Exporting analysis charts...\n")
        os.makedirs("output/analysis", exist_ok=True)
        acharts.plot_cohort_retention(cohort)
        acharts.plot_revenue_forecast(forecast_data, [m["revenue"] for m in monthly])
        acharts.plot_monte_carlo(mc_data)
        acharts.plot_gross_margin(gm_data)
        acharts.plot_expense_breakdown(expense_data)
        acharts.plot_cac_extrapolation(cac_extrap)
        acharts.plot_ltv_cac(ltv_data)
        print("\n✅  Charts saved to ./output/analysis/")


if __name__ == "__main__":
    main()
