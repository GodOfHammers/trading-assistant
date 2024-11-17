from fastapi import APIRouter, HTTPException
from typing import List
from ..core.trading_engine import TradingEngine

router = APIRouter()
trading_engine = TradingEngine()

@router.get("/stocks/{symbol}/analyze")
async def analyze_stock(symbol: str):
    try:
        analysis = await trading_engine.analyze_investment_opportunity(symbol)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/market/overview")
async def get_market_overview():
    try:
        return {
            "market_sentiment": "Bullish",
            "volatility_index": 15.5,
            "sector_performance": {
                "technology": 2.3,
                "healthcare": -0.5,
                "finance": 1.2
            },
            "market_indices": {
                "S&P500": 4500,
                "NASDAQ": 14000,
                "DOW": 35000
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stocks/{symbol}/realtime")
async def get_realtime_data(symbol: str):
    try:
        data = await trading_engine.fetch_realtime_data(symbol)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stocks/{symbol}/historical")
async def get_historical_data(symbol: str, period: str = "1y"):
    try:
        data = await trading_engine.fetch_historical_data(symbol, period)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # backend/api/routes.py

@router.get("/stocks/opportunities")
async def get_top_opportunities():
    try:
        trading_engine = TradingEngine()
        opportunities = await trading_engine.identify_top_opportunities(max_stocks=5)
        return opportunities
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))