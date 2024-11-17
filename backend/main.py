# backend/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def calculate_rsi(data: pd.Series, periods: int = 14) -> pd.Series:
    """Calculate RSI technical indicator."""
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_macd(data: pd.Series) -> tuple[pd.Series, pd.Series]:
    """Calculate MACD technical indicator."""
    exp1 = data.ewm(span=12, adjust=False).mean()
    exp2 = data.ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal

@app.get("/api/stocks/{symbol}/analyze")
async def analyze_stock(symbol: str):
    try:
        # Fetch stock data using yfinance
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1y")
        
        if hist.empty:
            raise HTTPException(status_code=404, detail=f"No data found for symbol {symbol}")

        # Calculate technical indicators
        hist['RSI'] = calculate_rsi(hist['Close'])
        macd, signal = calculate_macd(hist['Close'])
        hist['MACD'] = macd
        hist['MACD_Signal'] = signal
        
        # Calculate moving averages
        hist['SMA20'] = hist['Close'].rolling(window=20).mean()
        hist['SMA50'] = hist['Close'].rolling(window=50).mean()
        hist['SMA200'] = hist['Close'].rolling(window=200).mean()
        
        # Prepare historical data
        historical_data = []
        for index, row in hist.iterrows():
            historical_data.append({
                "date": index.strftime("%Y-%m-%d"),
                "price": row['Close'],
                "volume": row['Volume'],
                "sma20": row['SMA20'] if not pd.isna(row['SMA20']) else None,
                "sma50": row['SMA50'] if not pd.isna(row['SMA50']) else None,
                "sma200": row['SMA200'] if not pd.isna(row['SMA200']) else None,
                "rsi": row['RSI'] if not pd.isna(row['RSI']) else None,
                "macd": row['MACD'] if not pd.isna(row['MACD']) else None,
                "macd_signal": row['MACD_Signal'] if not pd.isna(row['MACD_Signal']) else None
            })
        
        # Get current price and calculate change
        current_price = hist['Close'][-1]
        prev_price = hist['Close'][-2]
        price_change = current_price - prev_price
        price_change_percentage = (price_change / prev_price) * 100
        
        # Determine trend based on multiple indicators
        trend = "Bullish" if (
            current_price > hist['SMA20'][-1] and 
            hist['SMA20'][-1] > hist['SMA50'][-1] and
            hist['RSI'][-1] > 50
        ) else "Bearish"
        
        # Determine strength based on multiple factors
        strength = "Strong" if (
            abs(price_change_percentage) > 2 and
            abs(hist['RSI'][-1] - 50) > 20
        ) else "Moderate"
        
        # Generate detailed analysis
        return {
            "symbol": symbol,
            "current_price": float(current_price),
            "price_change": float(price_change),
            "price_change_percentage": float(price_change_percentage),
            "recommendation": {
                "action": "BUY" if trend == "Bullish" else "SELL",
                "confidence": 0.8 if abs(price_change_percentage) > 2 else 0.6,
                "entry_price": float(current_price),
                "stop_loss": float(current_price * 0.95),  # 5% stop loss
                "take_profit": float(current_price * 1.1),  # 10% take profit
                "time_horizon": "Medium Term",
                "reasons": [
                    f"Trend is {trend}",
                    f"Momentum is {strength}",
                    f"RSI is {'oversold' if hist['RSI'][-1] < 30 else 'overbought' if hist['RSI'][-1] > 70 else 'neutral'}",
                    f"Price is {'above' if current_price > hist['SMA50'][-1] else 'below'} 50-day moving average"
                ]
            },
            "technical_analysis": {
                "trend": trend,
                "strength": strength,
                "signals": {
                    "sma20": float(hist['SMA20'][-1]),
                    "sma50": float(hist['SMA50'][-1]),
                    "sma200": float(hist['SMA200'][-1]),
                    "rsi": float(hist['RSI'][-1]),
                    "macd": float(hist['MACD'][-1]),
                    "macd_signal": float(hist['MACD_Signal'][-1])
                }
            },
            "historical_data": historical_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Stock Analysis API is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)