# backend/core/advanced_indicators.py

import numpy as np
import pandas as pd
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class TechnicalFeatures:
    """Container for technical indicators."""
    price_data: np.ndarray
    volume_data: np.ndarray
    momentum: np.ndarray
    volatility: np.ndarray
    trend: np.ndarray
    cycles: np.ndarray

class AdvancedTechnicalIndicators:
    @staticmethod
    def calculate_all(data: pd.DataFrame) -> Dict[str, np.ndarray]:
        """Calculate comprehensive technical indicators."""
        indicators = {}
        
        # Trend Indicators
        indicators.update(AdvancedTechnicalIndicators._calculate_trend_indicators(data))
        
        # Momentum Indicators
        indicators.update(AdvancedTechnicalIndicators._calculate_momentum_indicators(data))
        
        # Volatility Indicators
        indicators.update(AdvancedTechnicalIndicators._calculate_volatility_indicators(data))
        
        # Volume Indicators
        indicators.update(AdvancedTechnicalIndicators._calculate_volume_indicators(data))
        
        # Cycle Indicators
        indicators.update(AdvancedTechnicalIndicators._calculate_cycle_indicators(data))
        
        return indicators

    @staticmethod
    def _calculate_trend_indicators(data: pd.DataFrame) -> Dict[str, np.ndarray]:
        """Calculate trend-following indicators."""
        indicators = {}
        
        # Multiple SMAs
        for period in [10, 20, 50, 100, 200]:
            indicators[f'SMA_{period}'] = data['Close'].rolling(window=period).mean()
        
        # Multiple EMAs
        for period in [12, 26, 50, 200]:
            indicators[f'EMA_{period}'] = data['Close'].ewm(span=period, adjust=False).mean()
        
        # VWAP (Volume Weighted Average Price)
        indicators['VWAP'] = (data['Close'] * data['Volume']).cumsum() / data['Volume'].cumsum()
        
        # ADX (Average Directional Index)
        high = data['High']
        low = data['Low']
        close = data['Close']
        
        # TR (True Range)
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        
        # +DM and -DM
        plus_dm = high.diff()
        minus_dm = low.diff()
        plus_dm[plus_dm < 0] = 0
        minus_dm[minus_dm > 0] = 0
        
        # Smooth TR and DM
        period = 14
        tr_smooth = tr.rolling(period).sum()
        plus_dm_smooth = plus_dm.rolling(period).sum()
        minus_dm_smooth = minus_dm.rolling(period).sum()
        
        # Calculate +DI and -DI
        plus_di = 100 * plus_dm_smooth / tr_smooth
        minus_di = 100 * minus_dm_smooth / tr_smooth
        
        # Calculate ADX
        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
        indicators['ADX'] = dx.rolling(period).mean()
        
        return indicators

    @staticmethod
    def _calculate_momentum_indicators(data: pd.DataFrame) -> Dict[str, np.ndarray]:
        """Calculate momentum-based indicators."""
        indicators = {}
        
        # RSI
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        indicators['RSI'] = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = data['Close'].ewm(span=12, adjust=False).mean()
        exp2 = data['Close'].ewm(span=26, adjust=False).mean()
        indicators['MACD'] = exp1 - exp2
        indicators['MACD_Signal'] = indicators['MACD'].ewm(span=9, adjust=False).mean()
        indicators['MACD_Hist'] = indicators['MACD'] - indicators['MACD_Signal']
        
        # Stochastic Oscillator
        low_min = data['Low'].rolling(14).min()
        high_max = data['High'].rolling(14).max()
        indicators['K_Fast'] = 100 * (data['Close'] - low_min) / (high_max - low_min)
        indicators['D_Fast'] = indicators['K_Fast'].rolling(3).mean()
        indicators['K_Slow'] = indicators['D_Fast']
        indicators['D_Slow'] = indicators['K_Slow'].rolling(3).mean()
        
        # ROC (Rate of Change)
        n = 12
        indicators['ROC'] = ((data['Close'] - data['Close'].shift(n)) / 
                           data['Close'].shift(n)) * 100
        
        # MFI (Money Flow Index)
        typical_price = (data['High'] + data['Low'] + data['Close']) / 3
        money_flow = typical_price * data['Volume']
        
        positive_flow = money_flow.where(typical_price > typical_price.shift(1), 0)
        negative_flow = money_flow.where(typical_price < typical_price.shift(1), 0)
        
        positive_mf = positive_flow.rolling(14).sum()
        negative_mf = negative_flow.rolling(14).sum()
        
        mfi = 100 - (100 / (1 + positive_mf / negative_mf))
        indicators['MFI'] = mfi
        
        return indicators

    @staticmethod
    def _calculate_volatility_indicators(data: pd.DataFrame) -> Dict[str, np.ndarray]:
        """Calculate volatility indicators."""
        indicators = {}
        
        # Bollinger Bands
        period = 20
        std_dev = 2
        
        indicators['BB_Middle'] = data['Close'].rolling(window=period).mean()
        bb_std = data['Close'].rolling(window=period).std()
        indicators['BB_Upper'] = indicators['BB_Middle'] + std_dev * bb_std
        indicators['BB_Lower'] = indicators['BB_Middle'] - std_dev * bb_std
        indicators['BB_Width'] = (indicators['BB_Upper'] - indicators['BB_Lower']) / indicators['BB_Middle']
        
        # ATR (Average True Range)
        high = data['High']
        low = data['Low']
        close = data['Close']
        
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        indicators['ATR'] = tr.rolling(14).mean()
        
        # Historical Volatility
        returns = np.log(data['Close'] / data['Close'].shift(1))
        indicators['Volatility'] = returns.rolling(window=30).std() * np.sqrt(252)
        
        # Keltner Channels
        typical_price = (high + low + close) / 3
        indicators['KC_Middle'] = typical_price.rolling(20).mean()
        indicators['KC_Upper'] = indicators['KC_Middle'] + (indicators['ATR'] * 2)
        indicators['KC_Lower'] = indicators['KC_Middle'] - (indicators['ATR'] * 2)
        
        return indicators

    @staticmethod
    def _calculate_volume_indicators(data: pd.DataFrame) -> Dict[str, np.ndarray]:
        """Calculate volume-based indicators."""
        indicators = {}
        
        # OBV (On Balance Volume)
        obv = (data['Volume'] * (~data['Close'].diff().le(0) * 2 - 1)).cumsum()
        indicators['OBV'] = obv
        
        # VWAP (Volume Weighted Average Price)
        indicators['VWAP'] = (data['Close'] * data['Volume']).cumsum() / data['Volume'].cumsum()
        
        # Volume SMA
        indicators['Volume_SMA'] = data['Volume'].rolling(window=20).mean()
        
        # Chaikin Money Flow
        mf_multiplier = ((data['Close'] - data['Low']) - (data['High'] - data['Close'])) / (data['High'] - data['Low'])
        mf_volume = mf_multiplier * data['Volume']
        indicators['CMF'] = mf_volume.rolling(20).sum() / data['Volume'].rolling(20).sum()
        
        return indicators

    @staticmethod
    def _calculate_cycle_indicators(data: pd.DataFrame) -> Dict[str, np.ndarray]:
        """Calculate cycle indicators."""
        indicators = {}
        
        # Ehlers Fisher Transform
        high = data['High']
        low = data['Low']
        
        median_price = (high + low) / 2
        period = 10
        
        # Calculate EFT
        value1 = 0.33 * 2 * (median_price - median_price.rolling(period).min()) / (median_price.rolling(period).max() - median_price.rolling(period).min()) - 0.5
        indicators['EFT'] = 0.5 * np.log((1 + value1) / (1 - value1))
        
        # Dominant Cycle
        close = data['Close']
        smooth = (4 * close + 3 * close.shift(1) + 2 * close.shift(2) + close.shift(3)) / 10
        indicators['Dominant_Cycle'] = smooth - smooth.shift(int(period/2))
        
        return indicators