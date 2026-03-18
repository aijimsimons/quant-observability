"""Performance metrics calculations."""

from typing import Protocol

import polars as pl


class PerformanceMetrics(Protocol):
    """Protocol for performance metrics."""
    
    def calculate(self, equity_curve: pl.DataFrame) -> dict:
        """Calculate performance metrics."""
        ...


def calculate_sharpe(equity: pl.Series) -> float:
    """Calculate annualized Sharpe ratio."""
    returns = equity.pct_change().drop_nulls()
    mean_return = returns.mean()
    std_return = returns.std()
    return (mean_return / std_return * 252**0.5) if std_return else 0.0


def calculate_max_drawdown(equity: pl.Series) -> float:
    """Calculate maximum drawdown."""
    cumulative = equity.cum_max()
    drawdown = (cumulative - equity) / cumulative
    return drawdown.max() if drawdown.len() > 0 else 0.0


def calculate_sortino(equity: pl.Series, risk_free_rate: float = 0.02) -> float:
    """Calculate Sortino ratio."""
    returns = equity.pct_change().drop_nulls()
    mean_return = returns.mean()
    
    negative_returns = returns.filter(returns < 0)
    std_negative = negative_returns.std() if len(negative_returns) > 0 else 0
    
    if std_negative == 0:
        return 0.0
    
    return (mean_return - risk_free_rate/252) / std_negative * 252**0.5
