# backend/core/risk_manager.py

import numpy as np
import pandas as pd
from typing import Dict, Optional
from datetime import datetime
import logging

class RiskManager:
    def __init__(self):
        self.max_position_size = 0.02  # 2% of portfolio per position
        self.max_total_risk = 0.05     # 5% total portfolio risk
        self.min_stop_distance = 0.02   # 2% minimum stop loss distance
        self.positions = {}
        
    async def assess_risk(self, symbol: str, data: pd.DataFrame) -> Dict:
        """Assess risk level for a symbol."""
        try:
            # Calculate volatility
            returns = data['close'].pct_change()
            volatility = returns.std() * np.sqrt(252)  # Annualized
            
            # Calculate drawdown
            rolling_max = data['close'].rolling(window=252, min_periods=1).max()
            drawdown = (data['close'] - rolling_max) / rolling_max
            max_drawdown = abs(drawdown.min())
            
            # Volume analysis
            volume_trend = self._analyze_volume_trend(data)
            
            # Market correlation
            market_correlation = await self._calculate_market_correlation(symbol, data)
            
            # Combined risk score (0-1, higher = more risky)
            risk_score = self._calculate_risk_score(
                volatility,
                max_drawdown,
                volume_trend,
                market_correlation
            )
            
            return {
                'risk_level': risk_score,
                'volatility': volatility,
                'max_drawdown': max_drawdown,
                'volume_trend': volume_trend,
                'market_correlation': market_correlation
            }
            
        except Exception as e:
            logging.error(f"Risk assessment error: {str(e)}")
            return {'risk_level': 1.0}  # Maximum risk on error
    
    async def calculate_position_size(
        self,
        symbol: str,
        account_size: float = 100000  # Default 100k portfolio
    ) -> float:
        """Calculate safe position size based on risk parameters."""
        try:
            # Get current positions risk
            current_risk = sum(pos['risk'] for pos in self.positions.values())
            
            # Available risk budget
            available_risk = self.max_total_risk - current_risk
            
            if available_risk <= 0:
                return 0  # No new positions allowed
            
            # Calculate position size based on volatility and available risk
            position_size = min(
                account_size * self.max_position_size,
                account_size * available_risk
            )
            
            return position_size
            
        except Exception as e:
            logging.error(f"Position size calculation error: {str(e)}")
            return 0
    
    async def calculate_stop_loss(
        self,
        symbol: str,
        entry_price: float
    ) -> float:
        """Calculate optimal stop loss level."""
        try:
            # Get historical volatility
            volatility = (await self.assess_risk(symbol, None))['volatility']
            
            # Calculate stop distance based on volatility
            stop_distance = max(
                self.min_stop_distance,
                volatility * 2  # 2x daily volatility
            )
            
            # Calculate stop price
            stop_price = entry_price * (1 - stop_distance)
            
            return stop_price
            
        except Exception as e:
            logging.error(f"Stop loss calculation error: {str(e)}")
            return entry_price * (1 - self.min_stop_distance)
    
    def _analyze_volume_trend(self, data: pd.DataFrame) -> float:
        """Analyze volume trend strength."""
        try:
            # Calculate volume moving averages
            volume_ma_short = data['volume'].rolling(window=5).mean()
            volume_ma_long = data['volume'].rolling(window=20).mean()
            
            # Calculate trend strength (-1 to 1)
            trend = (volume_ma_short - volume_ma_long) / volume_ma_long
            
            return trend.iloc[-1]
            
        except Exception as e:
            logging.error(f"Volume trend analysis error: {str(e)}")
            return 0
    
    async def _calculate_market_correlation(
        self,
        symbol: str,
        data: pd.DataFrame
    ) -> float:
        """Calculate correlation with broader market."""
        try:
            # Get market data (e.g., XJO for ASX)
            market_data = await self._get_market_data()
            
            if market_data is None:
                return 0.5  # Neutral correlation on error
            
            # Calculate correlation
            correlation = data['close'].pct_change().corr(
                market_data['close'].pct_change()
            )
            
            return correlation
            
        except Exception as e:
            logging.error(f"Market correlation calculation error: {str(e)}")
            return 0.5
    
    def _calculate_risk_score(
        self,
        volatility: float,
        max_drawdown: float,
        volume_trend: float,
        market_correlation: float
    ) -> float:
        """Calculate combined risk score."""
        try:
            # Normalize components
            vol_score = min(volatility / 0.4, 1)  # Cap at 40% volatility
            dd_score = min(max_drawdown / 0.3, 1)  # Cap at 30% drawdown
            vol_trend_score = abs(volume_trend)
            corr_score = abs(market_correlation)
            
            # Weighted combination
            risk_score = (
                vol_score * 0.4 +
                dd_score * 0.3 +
                vol_trend_score * 0.2 +
                corr_score * 0.1
            )
            
            return min(max(risk_score, 0), 1)  # Ensure 0-1 range
            
        except Exception as e:
            logging.error(f"Risk score calculation error: {str(e)}")
            return 1.0  # Maximum risk on error
    
    async def _get_market_data(self) -> Optional[pd.DataFrame]:
        """Get market index data."""
        try:
            # Implement market data fetching (e.g., XJO for ASX)
            # This is a placeholder - implement actual data fetching
            return None
            
        except Exception as e:
            logging.error(f"Market data fetching error: {str(e)}")
            return None