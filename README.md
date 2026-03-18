# quant-observability

Performance tracking, metrics, and alerts for trading strategies.

## Overview

This repository provides tools for monitoring trading strategy performance:

- **Metrics** - Sharpe, Sortino, max drawdown, win rate, profit factor
- **Alerts** - Drawdown, volatility, profit factor alerts
- **Dashboards** - Equity curves, P&L charts (template structure)

## Installation

```bash
cd quant-observability
uv sync
```

## Usage

### Calculate Metrics

```python
from quant_observability.metrics import calculate_metrics

# After backtesting
result = backtest_engine.run(data, strategy)

metrics = calculate_metrics(
    equity_curve=result.equity_curve,
    trades=result.trades
)

print(f"Sharpe: {metrics['sharpe_ratio']:.2f}")
print(f"Max Drawdown: {metrics['max_drawdown']:.2%}")
```

### Use Alert System

```python
from quant_observability.alerts import DrawdownAlert, VolatilityAlert, CompositeAlertManager

# Create alert manager
manager = CompositeAlertManager()
manager.add_alert(DrawdownAlert(threshold=0.15))
manager.add_alert(VolatilityAlert(threshold=0.05))

# Check alerts
state = {"equity": 9000, "volatility": 0.03}
alerts = manager.check(state)

for alert in alerts:
    print(f"{alert['type']}: {alert['message']}")
```

## API Reference

### Metrics

- `calculate_sharpe()` - Annualized Sharpe ratio
- `calculate_sortino()` - Sortino ratio
- `calculate_max_drawdown()` - Maximum drawdown
- `calculate_profit_factor()` - Profit factor
- `calculate_win_rate()` - Win rate
- `calculate_metrics()` - Comprehensive metrics

### Alerts

- `DrawdownAlert` - Trigger when drawdown exceeds threshold
- `VolatilityAlert` - Trigger when volatility spikes
- `CompositeAlertManager` - Manage multiple alert types

## License

MIT
