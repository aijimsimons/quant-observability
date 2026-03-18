# quant-observability

Performance tracking, metrics, and dashboards for trading strategies.

## Features

- Real-time P&L tracking
- Strategy performance metrics (Sharpe, Sortino, max drawdown)
- Equity curves
- Signal quality metrics
- Alert system

## Architecture

```
observability/
├── metrics/          # Strategy metrics calculations
├── dashboards/       # Grafana/Prometheus configs
├── alerts/           # Alert rules
└── web/              # Web interface
```
