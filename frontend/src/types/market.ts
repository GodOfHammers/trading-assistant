// frontend/src/types/market.ts

export interface MarketIndicator {
    name: string;
    value: number | string;
    signal: 'bullish' | 'bearish' | 'neutral';
    interpretation: string;
  }
  
  export interface SectorData {
    sector: string;
    performance: number;
    marketCap: number;
    momentum: number;
    strength: number;
  }
  
  export interface MarketBreadthData {
    date: string;
    advanceDecline: number;
    indexValue: number;
    newHighs: number;
    newLows: number;
  }
  
  export interface MarketAnalysisData {
    marketTechnicals: MarketIndicator[];
    sectorPerformance: SectorData[];
    breadthHistory: MarketBreadthData[];
    sectorCorrelations: number[][];
    sectorList: string[];
    sectorRotation: {
      date: string;
      cyclical: number;
      defensive: number;
      technology: number;
      financial: number;
    }[];
    maAnalysis: {
      date: string;
      price: number;
      sma50: number;
      sma200: number;
    }[];
  }