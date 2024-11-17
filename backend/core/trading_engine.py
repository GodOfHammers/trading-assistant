# backend/core/trading_engine.py

import yfinance as yf
import pandas as pd
import numpy as np
from typing import List, Dict
from datetime import datetime, timedelta
from .news_analyzer import NewsAnalyzer
from .profit_analyzer import DynamicProfitAnalyzer
from .risk_manager import RiskManager
from concurrent.futures import ThreadPoolExecutor
import asyncio
import logging

class TradingEngine:
    def __init__(self):
        self.news_analyzer = NewsAnalyzer()
        self.profit_analyzer = DynamicProfitAnalyzer()
        self.risk_manager = RiskManager()
        
        # Major indices to scan
        self.indices = {
            'US': ['^GSPC', '^DJI', '^IXIC'],  # S&P 500, Dow Jones, NASDAQ
            'AU': ['^AXJO'],  # ASX 200
        }
        
        # Minimum criteria for stock selection
        self.min_market_cap = 1e9  # $1B minimum market cap
        self.min_volume = 500000   # Minimum daily volume
        self.min_price = 5         # Minimum stock price

    async def identify_top_opportunities(self, max_stocks: int = 10) -> List[Dict]:
        """Identify top stock opportunities using multiple factors."""
        try:
            # 1. Get constituent stocks from major indices
            all_stocks = await self._get_index_constituents()
            
            # 2. Initial filtering
            filtered_stocks = await self._apply_initial_filters(all_stocks)
            
            # 3. Detailed analysis of remaining stocks
            analysis_results = await self._analyze_stocks(filtered_stocks)
            
            # 4. Rank stocks based on composite score
            ranked_stocks = self._rank_stocks(analysis_results)
            
            # 5. Return top N opportunities
            return ranked_stocks[:max_stocks]
            
        except Exception as e:
            logging.error(f"Error in identify_top_opportunities: {str(e)}")
            raise

    async def _get_index_constituents(self) -> List[str]:
        """Get constituents of major indices."""
        constituents = set()
        
        for region, indices in self.indices.items():
            for index in indices:
                try:
                    index_data = yf.Ticker(index)
                    if region == 'US':
                        # For S&P 500
                        if index == '^GSPC':
                            sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
                            constituents.update(sp500['Symbol'].tolist())
                        # For NASDAQ-100
                        elif index == '^IXIC':
                            nasdaq100 = pd.read_html('https://en.wikipedia.org/wiki/Nasdaq-100')[4]
                            constituents.update(nasdaq100['Ticker'].tolist())
                    elif region == 'AU':
                        # For ASX 200
                        asx200 = pd.read_html('https://en.wikipedia.org/wiki/S%26P/ASX_200')[1]
                        constituents.update(f"{ticker}.AX" for ticker in asx200['ASX code'].tolist())
                        
                except Exception as e:
                    logging.error(f"Error fetching constituents for {index}: {str(e)}")
                    continue
        
        return list(constituents)

    async def _apply_initial_filters(self, symbols: List[str]) -> List[str]:
        """Apply initial filtering criteria."""
        filtered_symbols = []
        
        async def check_stock(symbol: str):
            try:
                stock = yf.Ticker(symbol)
                info = stock.info
                
                # Basic filters
                if (info.get('marketCap', 0) < self.min_market_cap or
                    info.get('regularMarketPrice', 0) < self.min_price or
                    info.get('averageVolume', 0) < self.min_volume):
                    return None
                
                # Additional filters
                if (info.get('regularMarketPrice', 0) > 0 and
                    info.get('trailingPE', float('inf')) < 50 and  # Reasonable P/E
                    info.get('priceToBook', float('inf')) < 10):   # Reasonable P/B
                    return symbol
                    
            except Exception as e:
                logging.error(f"Error filtering {symbol}: {str(e)}")
                return None
        
        # Use ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor(max_workers=10) as executor:
            tasks = [check_stock(symbol) for symbol in symbols]
            results = await asyncio.gather(*tasks)
            filtered_symbols = [r for r in results if r is not None]
        
        return filtered_symbols

    async def _analyze_stocks(self, symbols: List[str]) -> List[Dict]:
        """Perform detailed analysis of filtered stocks."""
        analysis_results = []
        
        for symbol in symbols:
            try:
                # Get stock data
                stock = yf.Ticker(symbol)
                hist = stock.history(period="1y")
                
                if hist.empty:
                    continue
                
                # Technical Analysis
                tech_analysis = await self._perform_technical_analysis(hist)
                
                # News Sentiment Analysis
                news = await self._fetch_news(symbol)
                sentiment = await self.news_analyzer.analyze(news)
                
                # Risk Assessment
                risk = await self.risk_manager.assess_risk(symbol, hist)
                
                # Profit Potential Analysis
                profit_potential = await self.profit_analyzer.calculate_dynamic_threshold(
                    symbol,
                    hist,
                    sentiment['score'],
                    risk['volatility']
                )
                
                # Calculate composite score
                score = self._calculate_composite_score(
                    tech_analysis,
                    sentiment,
                    risk,
                    profit_potential
                )
                
                analysis_results.append({
                    'symbol': symbol,
                    'score': score,
                    'current_price': float(hist['Close'].iloc[-1]),
                    'change_percent': float(((hist['Close'].iloc[-1] / hist['Close'].iloc[-2]) - 1) * 100),
                    'volume': float(hist['Volume'].iloc[-1]),
                    'technical_analysis': tech_analysis,
                    'sentiment': sentiment,
                    'risk_assessment': risk,
                    'profit_potential': profit_potential
                })
                
            except Exception as e:
                logging.error(f"Error analyzing {symbol}: {str(e)}")
                continue
        
        return analysis_results

    def _calculate_composite_score(
        self,
        technical: Dict,
        sentiment: Dict,
        risk: Dict,
        profit: Dict
    ) -> float:
        """Calculate composite score for ranking."""
        try:
            # Weight components
            tech_weight = 0.35
            sentiment_weight = 0.25
            risk_weight = 0.20
            profit_weight = 0.20
            
            # Technical score
            tech_score = (
                technical['trend_strength'] * 0.4 +
                technical['momentum'] * 0.3 +
                technical['support_resistance'] * 0.3
            )
            
            # Normalize and combine scores
            score = (
                tech_score * tech_weight +
                sentiment['score'] * sentiment_weight +
                (1 - risk['risk_level']) * risk_weight +  # Inverse risk
                profit['confidence'] * profit_weight
            )
            
            return float(score)
            
        except Exception as e:
            logging.error(f"Error calculating composite score: {str(e)}")
            return 0.0

    def _rank_stocks(self, analysis_results: List[Dict]) -> List[Dict]:
        """Rank stocks based on composite score."""
        try:
            # Sort by score in descending order
            ranked = sorted(
                analysis_results,
                key=lambda x: x['score'],
                reverse=True
            )
            
            # Add ranking information
            for i, stock in enumerate(ranked):
                stock['rank'] = i + 1
                stock['recommendation'] = self._generate_recommendation(stock)
            
            return ranked
            
        except Exception as e:
            logging.error(f"Error ranking stocks: {str(e)}")
            return []

    def _generate_recommendation(self, stock: Dict) -> Dict:
        """Generate trading recommendation."""
        score = stock['score']
        
        if score >= 0.8:
            action = "STRONG_BUY"
            confidence = 0.9
        elif score >= 0.6:
            action = "BUY"
            confidence = 0.7
        elif score <= 0.2:
            action = "SELL"
            confidence = 0.8
        elif score <= 0.4:
            action = "HOLD"
            confidence = 0.6
        else:
            action = "HOLD"
            confidence = 0.5
            
        return {
            'action': action,
            'confidence': confidence,
            'reasons': self._generate_recommendation_reasons(stock)
        }

    def _generate_recommendation_reasons(self, stock: Dict) -> List[str]:
        """Generate detailed reasons for the recommendation."""
        reasons = []
        
        # Technical Analysis
        if stock['technical_analysis']['trend'] == 'bullish':
            reasons.append(f"Strong bullish trend with {stock['technical_analysis']['strength']} momentum")
        
        # Sentiment
        if stock['sentiment']['score'] > 0.6:
            reasons.append("Positive market sentiment and news coverage")
        
        # Risk
        if stock['risk_assessment']['risk_level'] < 0.3:
            reasons.append("Low risk profile with stable metrics")
        
        # Profit Potential
        if stock['profit_potential']['confidence'] > 0.7:
            reasons.append("High profit potential based on multiple factors")
            
        return reasons