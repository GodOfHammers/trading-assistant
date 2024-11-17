# backend/models/profit_model.py

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
import numpy as np

class ProfitThreshold(BaseModel):
    base_threshold: float = Field(ge=0.0, le=1.0)
    adjusted_threshold: float = Field(ge=0.0, le=1.0)
    confidence: float = Field(ge=0.0, le=1.0)
    factors: Dict[str, float]
    last_update: datetime
    
    class Config:
        schema_extra = {
            "example": {
                "base_threshold": 0.02,
                "adjusted_threshold": 0.025,
                "confidence": 0.85,
                "factors": {
                    "volatility": 0.01,
                    "sentiment": 0.005,
                    "market_condition": 0.01
                }
            }
        }

class ProfitAnalysis(BaseModel):
    symbol: str
    current_price: float
    entry_price: float
    quantity: float
    unrealized_profit: float
    profit_percentage: float
    profit_threshold: ProfitThreshold
    risk_metrics: Dict[str, float]
    technical_signals: Dict[str, str]
    recommendation: str
    confidence: float
    timestamp: datetime
    
    def calculate_metrics(self):
        """Calculate profit metrics."""
        self.unrealized_profit = (self.current_price - self.entry_price) * self.quantity
        self.profit_percentage = ((self.current_price - self.entry_price) / self.entry_price) * 100

class TradeHistory(BaseModel):
    symbol: str
    entry_price: float
    exit_price: float
    quantity: float
    entry_date: datetime
    exit_date: datetime
    profit: float
    profit_percentage: float
    hold_duration: float  # in days
    trade_type: str  # 'long' or 'short'
    exit_reason: str
    
    def calculate_metrics(self):
        """Calculate trade metrics."""
        self.profit = (self.exit_price - self.entry_price) * self.quantity
        self.profit_percentage = ((self.exit_price - self.entry_price) / self.entry_price) * 100
        self.hold_duration = (self.exit_date - self.entry_date).total_seconds() / 86400  # Convert to days

class ProfitHistory(BaseModel):
    trades: List[TradeHistory]
    total_trades: int
    profitable_trades: int
    win_rate: float
    average_profit: float
    average_loss: float
    profit_factor: float
    max_drawdown: float
    sharpe_ratio: float
    
    def calculate_statistics(self):
        """Calculate trading statistics."""
        if not self.trades:
            return
            
        profits = [t.profit for t in self.trades]
        self.total_trades = len(profits)
        self.profitable_trades = sum(1 for p in profits if p > 0)
        self.win_rate = self.profitable_trades / self.total_trades if self.total_trades > 0 else 0
        
        gains = [p for p in profits if p > 0]
        losses = [p for p in profits if p < 0]
        
        self.average_profit = np.mean(gains) if gains else 0
        self.average_loss = abs(np.mean(losses)) if losses else 0
        self.profit_factor = (sum(gains) / abs(sum(losses))) if losses else float('inf')
        
        # Calculate drawdown
        cumulative = np.cumsum(profits)
        peak = np.maximum.accumulate(cumulative)
        drawdown = (peak - cumulative) / peak
        self.max_drawdown = np.max(drawdown) if len(drawdown) > 0 else 0
        
        # Calculate Sharpe ratio (assuming risk-free rate of 0.02)
        returns = [t.profit_percentage / 100 for t in self.trades]
        excess_returns = np.array(returns) - 0.02 / 252  # Daily risk-free rate
        self.sharpe_ratio = np.sqrt(252) * np.mean(excess_returns) / np.std(excess_returns) if len(returns) > 0 else 0