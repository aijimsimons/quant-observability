"""Alert system for trading strategies."""

from datetime import datetime
from typing import Protocol, Callable

import polars as pl


class Alert(Protocol):
    """Protocol for alerts."""
    
    def check(self, current_state: dict) -> list[dict]:
        """Check if alerts should trigger."""
        ...


class DrawdownAlert:
    """Alert when drawdown exceeds threshold."""
    
    def __init__(self, threshold: float = 0.15):
        self.threshold = threshold
        self.peak = 0.0
    
    def check(self, current_state: dict) -> list[dict]:
        """Check drawdown."""
        equity = current_state.get("equity", 0)
        
        if equity > self.peak:
            self.peak = equity
        
        if self.peak > 0:
            drawdown = (self.peak - equity) / self.peak
            if drawdown >= self.threshold:
                return [{
                    "type": "drawdown",
                    "message": f"Drawdown alert: {drawdown:.2%} (threshold: {self.threshold:.2%})",
                    "timestamp": datetime.now(),
                    "severity": "high" if drawdown > self.threshold * 1.5 else "medium",
                }]
        
        return []


class VolatilityAlert:
    """Alert when volatility spikes."""
    
    def __init__(self, threshold: float = 0.05):
        self.threshold = threshold
        self.rolling_vols: list = []
    
    def check(self, current_state: dict) -> list[dict]:
        """Check volatility."""
        volatility = current_state.get("volatility", 0)
        
        self.rolling_vols.append(volatility)
        if len(self.rolling_vols) > 20:
            self.rolling_vols.pop(0)
        
        avg_vol = sum(self.rolling_vols) / len(self.rolling_vols)
        
        if volatility > avg_vol * 2 and volatility > self.threshold:
            return [{
                "type": "volatility",
                "message": f"Volatility spike: {volatility:.2%} (avg: {avg_vol:.2%})",
                "timestamp": datetime.now(),
                "severity": "medium",
            }]
        
        return []


class ProfitFactorAlert:
    """Alert when profit factor drops."""
    
    def __init__(self, threshold: float = 1.0):
        self.threshold = threshold
    
    def check(self, current_state: dict) -> list[dict]:
        """Check profit factor."""
        profit_factor = current_state.get("profit_factor", 0)
        
        if profit_factor < self.threshold and profit_factor > 0:
            return [{
                "type": "profit_factor",
                "message": f"Profit factor alert: {profit_factor:.2f} (threshold: {self.threshold})",
                "timestamp": datetime.now(),
                "severity": "high",
            }]
        
        return []


class CompositeAlertManager:
    """Manage multiple alert types."""
    
    def __init__(self):
        self.alerts: list[Alert] = []
    
    def add_alert(self, alert: Alert) -> None:
        """Add an alert type."""
        self.alerts.append(alert)
    
    def check(self, current_state: dict) -> list[dict]:
        """Check all alerts."""
        all_alerts = []
        for alert in self.alerts:
            alerts = alert.check(current_state)
            all_alerts.extend(alerts)
        return all_alerts
