// frontend/src/services/api.ts

import axios from 'axios';
import type { StockData, HistoricalDataPoint } from '../types/stock';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
});

interface ApiResponse {
  symbol: string;
  current_price: number;
  price_change: number;
  price_change_percentage: number;
  recommendation: {
    action: string;
    confidence: number;
    entry_price: number;
    stop_loss: number;
    take_profit: number;
    time_horizon: string;
    reasons: string[];
  };
  technical_analysis: {
    trend: string;
    strength: string;
    signals: {
      sma20: number;
      sma50: number;
      sma200: number;
      rsi: number;
      macd: number;
      macd_signal: number;
    };
  };
  historical_data: Array<{
    date: string;
    price: number;
    volume: number;
    sma20?: number;
    sma50?: number;
    sma200?: number;
    rsi?: number;
  }>;
}

export const stockApi = {
  async getStockAnalysis(symbol: string): Promise<StockData> {
    try {
      const { data } = await api.get(`/stocks/${symbol}/analyze`);
      return data;
    } catch (error) {
      console.error(`Error fetching analysis for ${symbol}:`, error);
      throw error;
    }
  },
  async getTopOpportunities(): Promise<StockData[]> {
    try {
      const { data } = await api.get('/stocks/opportunities');
      return data;
    } catch (error) {
      console.error('Error fetching top opportunities:', error);
      throw error;
    }
  },
};