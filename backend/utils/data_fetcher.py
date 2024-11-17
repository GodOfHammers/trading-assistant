# backend/utils/data_fetcher.py

import aiohttp
import pandas as pd
import yfinance as yf
from typing import Dict, List, Optional
import logging
from datetime import datetime, timedelta

class DataFetcher:
    def __init__(self):
        self.alpha_vantage_key = "YOUR_ALPHA_VANTAGE_KEY"
        self.news_api_key = "YOUR_NEWS_API_KEY"
        self.session = None
    
    async def init_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession()
    
    async def fetch_stock_data(self, symbol: str) -> pd.DataFrame:
        """Fetch stock data from Yahoo Finance."""
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period="1y")
            return data
        except Exception as e:
            logging.error(f"Error fetching stock data for {symbol}: {e}")
            raise
    
    async def fetch_alpha_vantage_news(self, symbol: str) -> List[Dict]:
        """Fetch news from Alpha Vantage."""
        await self.init_session()
        url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={symbol}&apikey={self.alpha_vantage_key}"
        
        try:
            async with self.session.get(url) as response:
                data = await response.json()
                return data.get('feed', [])
        except Exception as e:
            logging.error(f"Error fetching Alpha Vantage news: {e}")
            return []
    
    async def fetch_real_time_price(self, symbol: str) -> Dict:
        """Fetch real-time price data."""
        try:
            stock = yf.Ticker(symbol)
            data = stock.info
            return {
                'price': data.get('regularMarketPrice', 0),
                'change': data.get('regularMarketChangePercent', 0),
                'volume': data.get('regularMarketVolume', 0)
            }
        except Exception as e:
            logging.error(f"Error fetching real-time price for {symbol}: {e}")
            raise