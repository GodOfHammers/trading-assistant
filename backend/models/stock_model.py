# backend/models/stock_model.py

from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime
import pandas as pd

class StockData(BaseModel):
    symbol: str
    current_price: float
    history: pd.DataFrame
    volume: int
    market_cap: Optional[float]
    pe_ratio: Optional[float]
    dividend_yield: Optional[float]
    sector: Optional[str]
    updated_at: datetime
    
    class Config:
        arbitrary_types_allowed = True  # For pandas DataFrame

class TechnicalIndicators(BaseModel):
    sma_20: float
    sma_50: float
    sma_200: float
    rsi: float
    macd: Dict[str, float]
    bollinger_bands: Dict[str, float]
    volume_sma: float
    atr: float

class Position(BaseModel):
    symbol: str
    entry_price: float
    quantity: float
    entry_date: datetime
    stop_loss: float
    take_profit: float
    current_price: float
    current_value: float
    profit_loss: float
    profit_loss_percentage: float
    risk_level: float
    technical_indicators: TechnicalIndicators
    last_update: datetime

class Portfolio(BaseModel):
    positions: List[Position]
    total_value: float
    cash_balance: float
    total_profit_loss: float
    total_profit_loss_percentage: float
    risk_exposure: float
    last_update: datetime
    
    def calculate_metrics(self):
        """Calculate portfolio metrics."""
        self.total_value = sum(pos.current_value for pos in self.positions) + self.cash_balance
        total_cost = sum(pos.entry_price * pos.quantity for pos in self.positions)
        self.total_profit_loss = self.total_value - total_cost
        self.total_profit_loss_percentage = (self.total_profit_loss / total_cost * 100) if total_cost > 0 else 0
        self.risk_exposure = sum(pos.risk_level * pos.current_value for pos in self.positions) / self.total_value