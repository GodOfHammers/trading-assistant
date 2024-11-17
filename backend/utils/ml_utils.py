# backend/utils/ml_utils.py

import numpy as np
from sklearn.preprocessing import MinMaxScaler
from typing import List, Dict, Tuple
import pandas as pd
from datetime import datetime, timedelta

class MLUtils:
    def __init__(self):
        self.scaler = MinMaxScaler()
    
    def prepare_features(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare features for ML models."""
        # Technical indicators
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df['RSI'] = self._calculate_rsi(df['Close'])
        
        # Target variable (next day return)
        df['Target'] = df['Close'].shift(-1) / df['Close'] - 1
        
        # Feature selection
        features = ['SMA_20', 'SMA_50', 'RSI', 'Volume']
        target = 'Target'
        
        # Remove NaN values
        df = df.dropna()
        
        X = df[features].values
        y = df[target].values
        
        return X, y
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index."""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    def normalize_data(self, data: np.ndarray) -> np.ndarray:
        """Normalize data using MinMaxScaler."""
        return self.scaler.fit_transform(data)