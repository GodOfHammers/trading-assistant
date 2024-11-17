// frontend/src/types/stock.ts

export interface HistoricalDataPoint {
  date: string;
  price: number;
  volume: number;
  sma20?: number;
  sma50?: number;
  sma200?: number;
  rsi?: number;
  macd?: number;
  macd_signal?: number;
  bollinger_upper?: number;
  bollinger_lower?: number;
  atr?: number;
}

export interface Recommendation {
  action: 'STRONG_BUY' | 'BUY' | 'HOLD' | 'SELL' | 'STRONG_SELL';
  confidence: number;
  entryPrice: number;
  stopLoss: number;
  takeProfit: number;
  timeHorizon: 'SHORT_TERM' | 'MEDIUM_TERM' | 'LONG_TERM';
  reasons: string[];
  urgency: 'HIGH' | 'MEDIUM' | 'LOW';
}

export interface TechnicalAnalysis {
  trend: 'BULLISH' | 'BEARISH' | 'NEUTRAL';
  strength: 'STRONG' | 'MODERATE' | 'WEAK';
  signals: {
    sma20: number;
    sma50: number;
    sma200: number;
    rsi: number;
    macd: number;
    macd_signal: number;
    bollinger_bands: {
      upper: number;
      middle: number;
      lower: number;
    };
    atr: number;
  };
  support_levels: number[];
  resistance_levels: number[];
}

export interface SentimentAnalysis {
  score: number;
  summary: string;
  key_topics: string[];
  news_sentiment: {
    positive: number;
    negative: number;
    neutral: number;
  };
  social_sentiment: {
    reddit: number;
    twitter: number;
  };
}

export interface RiskAssessment {
  risk_level: number;
  volatility: number;
  beta: number;
  var_95: number;
  sharpe_ratio: number;
  max_drawdown: number;
  risk_factors: {
    market_risk: number;
    sector_risk: number;
    company_specific_risk: number;
  };
}

export interface ProfitPotential {
  expected_return: number;
  probability: number;
  timeframe: string;
  scenarios: {
    bullish: {
      price: number;
      probability: number;
    };
    base: {
      price: number;
      probability: number;
    };
    bearish: {
      price: number;
      probability: number;
    };
  };
}

export interface StockData {
  symbol: string;
  score: number;
  current_price: number;
  change_percent: number;
  volume: number;
  market_cap: number;
  sector: string;
  industry: string;
  historical_data: HistoricalDataPoint[];
  price_history: number[];
  technical_analysis: TechnicalAnalysis;
  sentiment: SentimentAnalysis;
  risk_assessment: RiskAssessment;
  profit_potential: ProfitPotential;
  recommendation: Recommendation;
  rank: number;
  fundamentals: {
    pe_ratio: number;
    pb_ratio: number;
    dividend_yield: number;
    eps_growth: number;
    revenue_growth: number;
  };
  alerts: {
    price_alerts: {
      upper: number;
      lower: number;
    };
    volume_alert: number;
    technical_alerts: string[];
  };
}

export type ChartTimeframe = '1D' | '5D' | '1M' | '3M' | '6M' | '1Y' | '5Y';

export type ChartType = 'LINE' | 'CANDLESTICK' | 'AREA' | 'BAR';

export type ChartIndicator = 
  | 'SMA20' 
  | 'SMA50' 
  | 'SMA200' 
  | 'EMA' 
  | 'VOLUME' 
  | 'RSI' 
  | 'MACD' 
  | 'BOLLINGER' 
  | 'ATR';

export interface ChartIndicators {
  sma20: boolean;
  sma50: boolean;
  sma200: boolean;
  ema: boolean;
  volume: boolean;
  rsi: boolean;
  macd: boolean;
  bollinger: boolean;
  atr: boolean;
}

export interface ChartSettings {
  timeframe: ChartTimeframe;
  type: ChartType;
  indicators: ChartIndicators;
  showGridlines: boolean;
  showTooltips: boolean;
  showLegend: boolean;
  theme: 'LIGHT' | 'DARK';
}

export interface MarketData {
  indices: {
    [key: string]: {
      value: number;
      change: number;
      change_percent: number;
    };
  };
  sectors: {
    [key: string]: {
      performance: number;
      volume: number;
    };
  };
  market_breadth: {
    advancers: number;
    decliners: number;
    unchanged: number;
    new_highs: number;
    new_lows: number;
  };
  volatility: {
    vix: number;
    historical_volatility: number;
  };
}