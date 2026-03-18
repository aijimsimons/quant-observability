"""Performance metrics for trading strategies."""

from datetime import timedelta
from typing import Protocol

import polars as pl


def calculate_sharpe(returns: pl.Series, risk_free_rate: float = 0.02) -> float:
    """Calculate annualized Sharpe ratio."""
    if len(returns) == 0:
        return 0.0
    mean_return = returns.mean()
    std_return = returns.std()
    if std_return == 0:
        return 0.0
    return (mean_return / std_return * 252**0.5)


def calculate_sortino(returns: pl.Series, risk_free_rate: float = 0.02) -> float:
    """Calculate Sortino ratio."""
    if len(returns) == 0:
        return 0.0
    mean_return = returns.mean()
    negative_returns = returns.filter(returns < 0)
    if len(negative_returns) == 0:
        return 0.0
    std_negative = negative_returns.std()
    if std_negative == 0:
        return 0.0
    return (mean_return - risk_free_rate/252) / std_negative * 252**0.5


def calculate_max_drawdown(equity: pl.Series) -> float:
    """Calculate maximum drawdown."""
    if len(equity) == 0:
        return 0.0
    cumulative = equity.cum_max()
    drawdown = (cumulative - equity) / cumulative
    return drawdown.max()


def calculate_profit_factor(trades: list) -> float:
    """Calculate profit factor."""
    if len(trades) == 0:
        return 0.0
    wins = [t.get("pnl", 0) for t in trades if t.get("pnl", 0) > 0]
    losses = [abs(t.get("pnl", 0)) for t in trades if t.get("pnl", 0) < 0]
    total_wins = sum(wins)
    total_losses = sum(losses)
    if total_losses == 0:
        return total_wins if total_wins > 0 else 0.0
    return total_wins / total_losses


def calculate_win_rate(trades: list) -> float:
    """Calculate win rate."""
    if len(trades) == 0:
        return 0.0
    wins = sum(1 for t in trades if t.get("pnl", 0) > 0)
    return wins / len(trades)


def calculate_metrics(equity_curve: pl.DataFrame, trades: list = None) -> dict:
    """Calculate comprehensive metrics."""
    equity_curve = equity_curve.with_columns(
        (pl.col("equity") / pl.col("equity").shift(1) - 1).alias("returns")
    )
    returns = equity_curve["returns"].drop_nulls()
    
    initial_equity = equity_curve["equity"].first() if len(equity_curve) > 0 else 0
    final_equity = equity_curve["equity"].last() if len(equity_curve) > 0 else 0
    total_return = (final_equity - initial_equity) / initial_equity if initial_equity else 0
    
    return {
        "initial_equity": initial_equity,
        "final_equity": final_equity,
        "total_return": total_return,
        "annualized_return": returns.mean() * 252 if len(returns) > 0 else 0,
        "sharpe_ratio": calculate_sharpe(returns),
        "sortino_ratio": calculate_sortino(returns),
        "max_drawdown": calculate_max_drawdown(equity_curve["equity"]),
        "num_trades": len(trades) if trades else 0,
        "win_rate": calculate_win_rate(trades) if trades else 0,
        "profit_factor": calculate_profit_factor(trades) if trades else 0,
    }
