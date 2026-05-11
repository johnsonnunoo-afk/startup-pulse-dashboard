"""
app.py — Flask web server for Startup.OS Dashboard.
Serves a live HTML dashboard at the root URL.
"""

import os
from flask import Flask, jsonify, render_template_string
import data

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Startup.OS — Performance Dashboard</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: 'Segoe UI', system-ui, sans-serif;
      background: #0f1117;
      color: #e2e8f0;
      min-height: 100vh;
      padding: 2rem;
    }

    header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 2rem;
      flex-wrap: wrap;
      gap: 1rem;
    }

    header h1 {
      font-size: 1.5rem;
      font-weight: 700;
      letter-spacing: .05em;
      color: #7dd3fc;
    }

    header p {
      font-size: .8rem;
      color: #64748b;
    }

    .badge {
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 9999px;
      padding: .25rem .75rem;
      font-size: .75rem;
      color: #94a3b8;
    }

    /* KPI cards */
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 1rem;
      margin-bottom: 2rem;
    }

    .kpi-card {
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 12px;
      padding: 1.25rem 1.5rem;
    }

    .kpi-card .label {
      font-size: .75rem;
      text-transform: uppercase;
      letter-spacing: .08em;
      color: #64748b;
      margin-bottom: .5rem;
    }

    .kpi-card .value {
      font-size: 1.75rem;
      font-weight: 700;
      margin-bottom: .25rem;
    }

    .kpi-card .sub {
      font-size: .8rem;
      color: #94a3b8;
    }

    .kpi-card .growth {
      font-size: .8rem;
      margin-top: .4rem;
      font-weight: 600;
    }

    .up   { color: #34d399; }
    .down { color: #f87171; }
    .warn { color: #fbbf24; }

    .kpi-revenue  .value { color: #34d399; }
    .kpi-profit   .value { color: #60a5fa; }
    .kpi-expenses .value { color: #f87171; }
    .kpi-cac      .value { color: #fbbf24; }

    /* Two-column section */
    .two-col {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1rem;
      margin-bottom: 2rem;
    }

    @media (max-width: 700px) { .two-col { grid-template-columns: 1fr; } }

    .card {
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 12px;
      padding: 1.25rem 1.5rem;
    }

    .card h2 {
      font-size: .85rem;
      text-transform: uppercase;
      letter-spacing: .08em;
      color: #64748b;
      margin-bottom: 1rem;
    }

    /* Product bars */
    .product-row {
      display: flex;
      align-items: center;
      gap: .75rem;
      margin-bottom: .75rem;
    }

    .product-name  { width: 130px; font-size: .85rem; flex-shrink: 0; }
    .product-bar-wrap { flex: 1; background: #0f1117; border-radius: 99px; height: 8px; }
    .product-bar   { height: 8px; border-radius: 99px; }
    .product-pct   { width: 36px; text-align: right; font-size: .8rem; color: #94a3b8; }
    .product-amt   { width: 70px; text-align: right; font-size: .8rem; color: #94a3b8; }

    /* Transactions table */
    .tx-table { width: 100%; border-collapse: collapse; font-size: .85rem; }
    .tx-table th {
      text-align: left;
      color: #475569;
      font-size: .75rem;
      text-transform: uppercase;
      letter-spacing: .07em;
      padding: .5rem .75rem;
      border-bottom: 1px solid #1e293b;
    }
    .tx-table td { padding: .6rem .75rem; border-bottom: 1px solid #1e293b; }
    .tx-table tr:last-child td { border-bottom: none; }

    .status-paid    { color: #34d399; font-weight: 600; }
    .status-pending { color: #fbbf24; font-weight: 600; }
    .status-failed  { color: #f87171; font-weight: 600; }

    footer {
      text-align: center;
      font-size: .75rem;
      color: #334155;
      margin-top: 2rem;
      padding-top: 1rem;
      border-top: 1px solid #1e293b;
    }

    .refresh-btn {
      background: #1e40af;
      color: #bfdbfe;
      border: none;
      border-radius: 8px;
      padding: .4rem 1rem;
      font-size: .8rem;
      cursor: pointer;
      transition: background .2s;
    }
    .refresh-btn:hover { background: #1d4ed8; }
  </style>
</head>
<body>
  <header>
    <div>
      <h1>STARTUP.OS · Performance Dashboard</h1>
      <p>As of {{ metrics.as_of }} &nbsp;·&nbsp; Fiscal Year 2025</p>
    </div>
    <div style="display:flex;align-items:center;gap:.75rem">
      <span class="badge">Live Data</span>
      <button class="refresh-btn" onclick="location.reload()">↻ Refresh</button>
    </div>
  </header>

  <!-- KPI Cards -->
  <div class="kpi-grid">
    <div class="kpi-card kpi-revenue">
      <div class="label">Revenue YTD</div>
      <div class="value">${{ "{:,.0f}".format(metrics.revenue_ytd) }}</div>
      <div class="sub">${{ "{:,.0f}".format(metrics.revenue_mom) }} this month</div>
      <div class="growth up">▲ {{ metrics.revenue_growth }}% YoY</div>
    </div>
    <div class="kpi-card kpi-profit">
      <div class="label">Net Profit YTD</div>
      <div class="value">${{ "{:,.0f}".format(metrics.profit_ytd) }}</div>
      <div class="sub">{{ metrics.profit_margin }}% margin</div>
      <div class="growth up">▲ {{ metrics.profit_growth }}% YoY</div>
    </div>
    <div class="kpi-card kpi-expenses">
      <div class="label">Expenses YTD</div>
      <div class="value">${{ "{:,.0f}".format(metrics.expenses_ytd) }}</div>
      <div class="sub">Burn under control</div>
      <div class="growth {% if metrics.expenses_growth < 10 %}up{% else %}down{% endif %}">
        {{ "▲" if metrics.expenses_growth >= 0 else "▼" }} {{ metrics.expenses_growth }}% YoY
      </div>
    </div>
    <div class="kpi-card kpi-cac">
      <div class="label">CAC (Current)</div>
      <div class="value">${{ "{:,.0f}".format(metrics.cac) }}</div>
      <div class="sub">per new customer</div>
      <div class="growth warn">▲ {{ metrics.cac_growth }}% MoM</div>
    </div>
  </div>

  <div class="two-col">
    <!-- Products -->
    <div class="card">
      <h2>Revenue by Product — Current Quarter</h2>
      {% set colors = ["#34d399","#60a5fa","#f472b6","#94a3b8"] %}
      {% for p in products %}
      <div class="product-row">
        <div class="product-name">{{ p.name }}</div>
        <div class="product-bar-wrap">
          <div class="product-bar" style="width:{{ p.share }}%;background:{{ colors[loop.index0 % 4] }}"></div>
        </div>
        <div class="product-pct">{{ p.share }}%</div>
        <div class="product-amt">${{ "{:,.0f}".format(p.amount) }}</div>
      </div>
      {% endfor %}
    </div>

    <!-- Sparkline (text) -->
    <div class="card">
      <h2>Monthly Revenue Trend — Last 12 Months</h2>
      <div style="overflow-x:auto">
        <table style="width:100%;border-collapse:collapse;font-size:.8rem">
          <tr>
            <th style="text-align:left;color:#475569;padding:.3rem .5rem">Month</th>
            <th style="text-align:right;color:#475569;padding:.3rem .5rem">Revenue</th>
            <th style="text-align:right;color:#475569;padding:.3rem .5rem">Profit</th>
          </tr>
          {% for m in monthly[-6:] %}
          <tr>
            <td style="padding:.3rem .5rem;color:#94a3b8">{{ m.month }}</td>
            <td style="padding:.3rem .5rem;text-align:right;color:#34d399">${{ "{:,.0f}".format(m.revenue) }}</td>
            <td style="padding:.3rem .5rem;text-align:right;color:#60a5fa">${{ "{:,.0f}".format(m.profit) }}</td>
          </tr>
          {% endfor %}
        </table>
      </div>
    </div>
  </div>

  <!-- Transactions -->
  <div class="card" style="margin-bottom:2rem">
    <h2>Recent Transactions — Live Feed</h2>
    <table class="tx-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Customer</th>
          <th>Product</th>
          <th style="text-align:right">Amount</th>
          <th style="text-align:center">Status</th>
        </tr>
      </thead>
      <tbody>
        {% for tx in transactions %}
        <tr>
          <td style="color:#475569">{{ tx.id }}</td>
          <td>{{ tx.customer }}</td>
          <td style="color:#7dd3fc">{{ tx.product }}</td>
          <td style="text-align:right;color:#34d399">${{ "{:,.0f}".format(tx.amount) }}</td>
          <td style="text-align:center">
            <span class="status-{{ tx.status }}">{{ tx.status }}</span>
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>

  <footer>
    STARTUP.OS · v1.0 · All figures simulated for demo purposes
  </footer>

  <script>
    setTimeout(() => location.reload(), 60000);
  </script>
</body>
</html>
"""


@app.route("/")
def index():
    metrics_raw    = data.generate_metrics()
    transactions   = data.generate_transactions()
    monthly        = data.generate_monthly_series()
    products       = data.generate_product_revenue()

    class Obj(dict):
        __getattr__ = dict.__getitem__

    metrics = Obj(metrics_raw)
    return render_template_string(
        HTML,
        metrics=metrics,
        transactions=transactions,
        monthly=monthly,
        products=products,
    )


@app.route("/api/metrics")
def api_metrics():
    return jsonify(data.generate_metrics())


@app.route("/api/transactions")
def api_transactions():
    return jsonify(data.generate_transactions())


@app.route("/healthz")
def health():
    return "ok", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
