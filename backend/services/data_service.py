# backend/services/data_service.py

import yfinance as yf
import pandas as pd
from typing import Dict, List, Optional
import asyncio
import aiohttp
import logging
from datetime import datetime, timedelta
from ..utils.data_fetcher import DataFetcher
from ..models.stock_model import StockData
from ..models.news_model import NewsData

class DataService:
    def __init__(self):
        self.data_fetcher = DataFetcher()
        self.cache = {}
        self.cache_timeout = 60  # 60 seconds cache
        
    async def get_stock_data(self, symbol: str) -> StockData:
        """Get stock data with caching."""
        try:
            cache_key = f"stock_{symbol}"
            cached = self._get_from_cache(cache_key)
            if cached:
                return cached
            
            # Fetch from Yahoo Finance
            stock = yf.Ticker(symbol)
            hist = stock.history(period="6mo")
            
            # Convert to our model
            stock_data = StockData(
                symbol=symbol,
                history=hist,
                current_price=hist['Close'].iloc[-1],
                volume=hist['Volume'].iloc[-1],
                updated_at=datetime.now()
            )
            
            self._add_to_cache(cache_key, stock_data)
            return stock_data
            
        except Exception as e:
            logging.error(f"Stock data fetch error for {symbol}: {str(e)}")
            raise
    
    async def get_news_data(self, symbol: str) -> List[NewsData]:
        """Get news articles for symbol."""
        try:
            cache_key = f"news_{symbol}"
            cached = self._get_from_cache(cache_key)
            if cached:
                return cached
            
            # Fetch news from multiple sources
            news_items = []
            
            # Alpha Vantage News
            alpha_news = await self.data_fetcher.fetch_alpha_vantage_news(symbol)
            if alpha_news:
                news_items.extend(alpha_news)
            
            # Yahoo Finance News
            yahoo_news = await self.data_fetcher.fetch_yahoo_news(symbol)
            if yahoo_news:
                news_items.extend(yahoo_news)
            
            # Convert to our model
            news_data = [
                NewsData(
                    title=item['title'],
                    content=item['content'],
                    source=item['source'],
                    published_at=item['published_at'],
                    url=item['url']
                )
                for item in news_items
            ]
            
            self._add_to_cache(cache_key, news_data)
            return news_data
            
        except Exception as e:
            logging.error(f"News fetch error for {symbol}: {str(e)}")
            return []
    
    async def get_real_time_price(self, symbol: str) -> Dict:
        """Get real-time price data."""
        try:
            # Fetch from WebSocket if available, otherwise use REST API
            price_data = await self.data_fetcher.fetch_real_time_price(symbol)
            
            return {
                'price': price_data['price'],
                'change': price_data['change'],
                'volume': price_data['volume'],
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Real-time price fetch error for {symbol}: {str(e)}")
            raise
    
    async def get_market_data(self) -> Dict:
        """Get overall market data."""
        try:
            cache_key = "market_data"
            cached = self._get_from_cache(cache_key)
            if cached:
                return cached
            
            # Fetch major indices
            indices = ['^AXJO', '^AORD']  # ASX 200 and All Ordinaries
            market_data = {}
            
            for index in indices:
                data = await self.get_stock_data(index)
                market_data[index] = {
                    'price': data.current_price,
                    'change': data.history['Close'].pct_change().iloc[-1],
                    'volume': data.volume
                }
            
            self._add_to_cache(cache_key, market_data)
            return market_data
            
        except Exception as e:
            logging.error(f"Market data fetch error: {str(e)}")
            raise
    
    def _get_from_cache(self, key: str) -> Optional[any]:
        """Get data from cache if not expired."""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if (datetime.now() - timestamp).seconds < self.cache_timeout:
                return data
            del self.cache[key]
        return None
    
    def _add_to_cache(self, key: str, data: any):
        """Add data to cache."""
        self.cache[key] = (data, datetime.now())