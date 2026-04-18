# Startup.OS — Performance Dashboard

> A Python showcase of the [Startup.OS](https://startup-pulse-peek.lovable.app/) performance dashboard — built with Lovable.

This repo demonstrates the data layer and visualisation logic behind the dashboard: revenue, profit, burn, CAC, product splits, and a live transaction feed — all generated in Python.

---

## 🖥️ Live Project

👉 **[startup-pulse-peek.lovable.app](https://startup-pulse-peek.lovable.app/)**

Built with [Lovable](https://lovable.dev) — a React/TypeScript frontend with real-time charts and an animated transaction feed.

---

## 📁 Project Structure

```
startup_os/
├── dashboard.py        # Entry point
├── data.py             # Simulated KPI & transaction data
├── charts.py           # Matplotlib chart exports
├── terminal.py         # Rich terminal console
├── requirements.txt
└── output/             # Generated PNGs (after --export)
```

---

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/startup-os-dashboard.git
cd startup-os-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the terminal dashboard
python dashboard.py

# 4. Export charts to ./output/
python dashboard.py --export

# 5. Watch the animated live-feed demo
python dashboard.py --demo
```

---

## 📊 Charts Generated

| File | Description |
|---|---|
| `01_revenue_vs_expenses.png` | Grouped bar — last 12 months |
| `02_revenue_by_product.png` | Donut chart — current quarter |
| `03_net_profit.png` | Line chart — monthly profit |
| `04_cac_trend.png` | Line chart — customer acquisition cost |

---

## 🛠️ Stack

| Layer | Tech |
|---|---|
| Frontend (live app) | React · TypeScript · Tailwind · Lovable |
| Data simulation | Python · NumPy |
| Charts | Matplotlib |
| Terminal UI | Rich |

---

## 📝 Notes

All figures are simulated for demonstration purposes and do not represent real business data.

---

*Made with ❤️ using [Lovable](https://lovable.dev) + Python*
