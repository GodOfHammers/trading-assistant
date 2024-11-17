# backend/core/profit_analyzer.py

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from typing import Dict, Optional
import asyncio
from datetime import datetime, timedelta

class DynamicProfitAnalyzer:
    def __init__(self):
        self.model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=4
        )
        self.min_threshold = 0.015  # 1.5% minimum profit threshold
        self.max_threshold = 0.10   # 10% maximum profit threshold
        
    async def calculate_dynamic_threshold(
        self,
        symbol: str,
        historical_data: pd.DataFrame,
        news_sentiment: float,
        market_volatility: float
    ) -> Dict:
        """Calculate dynamic profit threshold based on multiple factors."""
        
        try:
            # Calculate base threshold from historical volatility
            daily_returns = historical_data['Close'].pct_change()
            historical_volatility = daily_returns.std()
            
            # Adjust based on market conditions
            base_threshold = self._calculate_base_threshold(historical_volatility)
            
            # Adjust for news sentiment (-1 to 1 scale)
            sentiment_adjustment = self._adjust_for_sentiment(news_sentiment)
            
            # Adjust for current market volatility
            volatility_adjustment = self._adjust_for_volatility(market_volatility)
            
            # Calculate final threshold
            final_threshold = base_threshold * (1 + sentiment_adjustment) * (1 + volatility_adjustment)
            
            # Ensure threshold is within bounds
            final_threshold = max(min(final_threshold, self.max_threshold), self.min_threshold)
            
            return {
                'threshold': final_threshold,
                'base_threshold': base_threshold,
                'sentiment_impact': sentiment_adjustment,
                'volatility_impact': volatility_adjustment,
                'confidence': self._calculate_confidence(historical_data)
            }
            
        except Exception as e:
            logging.error(f"Error calculating threshold: {str(e)}")
            return {'threshold': self.min_threshold, 'error': str(e)}
    
    def _calculate_base_threshold(self, volatility: float) -> float:
        """Calculate base threshold from historical volatility."""
        # Higher volatility = higher potential returns = higher threshold
        base = np.clip(volatility * 2, self.min_threshold, self.max_threshold)
        return base
    
    def _adjust_for_sentiment(self, sentiment: float) -> float:
        """Adjust threshold based on news sentiment."""
        # Positive sentiment = lower threshold (easier to take profits)
        # Negative sentiment = higher threshold (wait for stronger confirmation)
        return -0.2 * sentiment  # -20% to +20% adjustment
    
    def _adjust_for_volatility(self, current_volatility: float) -> float:
        """Adjust threshold based on current market volatility."""
        # Higher current volatility = higher threshold
        vol_factor = current_volatility / 0.02  # normalize against 2% baseline
        return np.clip(vol_factor - 1, -0.2, 0.2)  # -20% to +20% adjustment
    
    def _calculate_confidence(self, data: pd.DataFrame) -> float:
        """Calculate confidence level in the threshold calculation."""
        # More data and more consistent patterns = higher confidence
        return min(len(data) / 252, 1.0)  # Max confidence after 1 year of data