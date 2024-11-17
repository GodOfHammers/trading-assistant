// src/components/Dashboard/StockList.tsx

import React, { useEffect, useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@ui/card';
import { 
  TrendingUp, TrendingDown, Bell, Info, 
  AlertTriangle, Activity 
} from 'lucide-react';
import type { StockData } from '../../types/stock';
import { Sparklines, SparklinesLine, SparklinesBars } from 'react-sparklines';
import { Tooltip } from "../../components/ui/tooltip";
import { Badge } from '../ui/badge';

interface StockListProps {
  stocks: StockData[];
  onSelect: (symbol: string) => void;
  selectedStock: string | null;
}

const StockList: React.FC<StockListProps> = ({ stocks, onSelect, selectedStock }) => {
  const [sortedStocks, setSortedStocks] = useState<StockData[]>([]);
  const [sortConfig, setSortConfig] = useState({
    key: 'score',
    direction: 'desc'
  });

  useEffect(() => {
    const sorted = [...stocks].sort((a, b) => {
      if (sortConfig.key === 'score') {
        return sortConfig.direction === 'desc' ? 
          b.score - a.score : a.score - b.score;
      }
      return 0;
    });
    setSortedStocks(sorted);
  }, [stocks, sortConfig]);

  const getRiskColor = (risk: number) => {
    if (risk < 0.3) return 'bg-green-100 text-green-800';
    if (risk < 0.7) return 'bg-yellow-100 text-yellow-800';
    return 'bg-red-100 text-red-800';
  };

  const formatVolume = (volume: number) => {
    if (volume >= 1e9) return `${(volume / 1e9).toFixed(1)}B`;
    if (volume >= 1e6) return `${(volume / 1e6).toFixed(1)}M`;
    if (volume >= 1e3) return `${(volume / 1e3).toFixed(1)}K`;
    return volume.toString();
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>Top Bullish Stocks</span>
          <div className="flex items-center space-x-2">
            <select
              className="text-sm border rounded px-2 py-1"
              onChange={(e) => setSortConfig({
                key: e.target.value,
                direction: sortConfig.direction
              })}
            >
              <option value="score">Score</option>
              <option value="change">% Change</option>
              <option value="volume">Volume</option>
            </select>
            <button
              onClick={() => setSortConfig({
                ...sortConfig,
                direction: sortConfig.direction === 'asc' ? 'desc' : 'asc'
              })}
              className="text-sm px-2 py-1 border rounded"
            >
              {sortConfig.direction === 'asc' ? '↑' : '↓'}
            </button>
          </div>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {sortedStocks.map((stock) => (
            <div
              key={stock.symbol}
              onClick={() => onSelect(stock.symbol)}
              className={`cursor-pointer rounded-lg border p-4 hover:bg-gray-50 
                transition-all duration-200 ${
                selectedStock === stock.symbol ? 'border-blue-500 bg-blue-50' : ''
              }`}
            >
              <div className="flex justify-between items-start mb-2">
                <div>
                  <div className="flex items-center space-x-2">
                    <h3 className="text-lg font-semibold">{stock.symbol}</h3>
                    <Badge variant="outline" className="text-xs">
                      Rank #{stock.rank}
                    </Badge>
                  </div>
                  <div className="flex items-center space-x-2 mt-1">
                    <p className="text-sm font-medium">
                      ${stock.current_price.toFixed(2)}
                    </p>
                    <span className="text-xs text-gray-500">
                      Vol: {formatVolume(stock.volume)}
                    </span>
                  </div>
                </div>
                <div className="flex flex-col items-end">
                  <div
                    className={`flex items-center ${
                      stock.change_percent >= 0 ? 'text-green-600' : 'text-red-600'
                    }`}
                  >
                    {stock.change_percent >= 0 ? (
                      <TrendingUp className="h-4 w-4 mr-1" />
                    ) : (
                      <TrendingDown className="h-4 w-4 mr-1" />
                    )}
                    {Math.abs(stock.change_percent).toFixed(2)}%
                  </div>
                  <div className="flex items-center space-x-2 mt-1">
                    <Tooltip content="Set Alert">
                      <Bell className="h-4 w-4 text-gray-400 hover:text-gray-600 cursor-pointer" />
                    </Tooltip>
                    <Tooltip content="Technical Analysis">
                      <Activity className="h-4 w-4 text-gray-400 hover:text-gray-600 cursor-pointer" />
                    </Tooltip>
                  </div>
                </div>
              </div>

              {/* Price History Sparkline */}
              <div className="mt-3 mb-2 h-12">
                <Sparklines data={stock.price_history} margin={5}>
                  <SparklinesLine
                    style={{
                      stroke: stock.change_percent >= 0 ? '#16a34a' : '#dc2626',
                      fill: 'none',
                      strokeWidth: 2
                    }}
                  />
                </Sparklines>
              </div>

              {/* Volume Sparkline */}
              <div className="h-8 mb-2 opacity-50">
                <Sparklines data={stock.historical_data.map(d => d.volume)}>
                  <SparklinesBars
                    style={{
                      fill: '#6b7280',
                    }}
                  />
                </Sparklines>
              </div>

              <div className="flex items-center justify-between mt-2">
                <div
                  className={`inline-block px-2 py-1 rounded text-sm font-medium ${
                    stock.recommendation.action === 'STRONG_BUY'
                      ? 'bg-green-100 text-green-800'
                      : stock.recommendation.action === 'BUY'
                      ? 'bg-blue-100 text-blue-800'
                      : stock.recommendation.action === 'SELL'
                      ? 'bg-red-100 text-red-800'
                      : 'bg-yellow-100 text-yellow-800'
                  }`}
                >
                  {stock.recommendation.action}
                  <span className="ml-1 text-xs">
                    ({(stock.recommendation.confidence * 100).toFixed()}%)
                  </span>
                </div>

                <div className="flex items-center space-x-2">
                  <Tooltip content="Risk Level">
                    <div className={`px-2 py-1 rounded text-xs ${
                      getRiskColor(stock.risk_assessment.risk_level)
                    }`}>
                      Risk: {(stock.risk_assessment.risk_level * 100).toFixed()}%
                    </div>
                  </Tooltip>
                  <Tooltip content="Sentiment Score">
                    <div className={`px-2 py-1 rounded text-xs ${
                      stock.sentiment.score > 0.6
                        ? 'bg-green-100 text-green-800'
                        : 'bg-gray-100 text-gray-800'
                    }`}>
                      Sentiment: {(stock.sentiment.score * 100).toFixed()}%
                    </div>
                  </Tooltip>
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default StockList;