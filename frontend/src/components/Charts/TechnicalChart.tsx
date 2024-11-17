// frontend/src/components/Charts/TechnicalChart.tsx

import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  ComposedChart,
  Bar
} from 'recharts';

interface ChartData {
  date: string;
  price: number;
  volume: number;
  sma20?: number;
  sma50?: number;
  sma200?: number;
  rsi?: number;
  macd?: number;
  macd_signal?: number;
}

type ChartIndicator = 'sma20' | 'sma50' | 'sma200' | 'volume' | 'rsi';

interface Indicators {
  sma20: boolean;
  sma50: boolean;
  sma200: boolean;
  volume: boolean;
  rsi: boolean;
}

interface TechnicalChartProps {
  data: ChartData[];
  symbol: string;
  indicators: Indicators;
  onIndicatorToggle: (indicator: ChartIndicator) => void;
}

const TechnicalChart: React.FC<TechnicalChartProps> = ({
  data,
  symbol,
  indicators,
  onIndicatorToggle
}) => {
  const formatDate = (date: string) => {
    return new Date(date).toLocaleDateString();
  };

  const formatPrice = (price: number) => {
    return `$${price.toFixed(2)}`;
  };

  const formatVolume = (volume: number) => {
    return `${(volume / 1000000).toFixed(1)}M`;
  };

  const indicatorsList: ChartIndicator[] = ['sma20', 'sma50', 'sma200', 'volume', 'rsi'];

  const getIndicatorLabel = (indicator: ChartIndicator): string => {
    switch (indicator) {
      case 'sma20':
        return 'SMA 20';
      case 'sma50':
        return 'SMA 50';
      case 'sma200':
        return 'SMA 200';
      case 'volume':
        return 'Volume';
      case 'rsi':
        return 'RSI';
    }
  };

  return (
    <Card>
      <CardHeader>
        <div className="flex justify-between items-center">
          <CardTitle>{symbol} Technical Analysis</CardTitle>
          <div className="flex gap-2">
            <select className="px-2 py-1 rounded border">
              <option value="1D">1D</option>
              <option value="1W">1W</option>
              <option value="1M">1M</option>
              <option value="3M">3M</option>
              <option value="1Y" selected>1Y</option>
            </select>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {/* Price Chart */}
          <div className="h-[400px]">
            <ResponsiveContainer width="100%" height="100%">
              <ComposedChart data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="date" 
                  tickFormatter={formatDate}
                />
                <YAxis 
                  yAxisId="price"
                  domain={['auto', 'auto']}
                  tickFormatter={formatPrice}
                />
                <YAxis 
                  yAxisId="volume"
                  orientation="right"
                  tickFormatter={formatVolume}
                />
                <Tooltip
                  labelFormatter={formatDate}
                  formatter={(value: any, name: string) => {
                    if (name === 'Volume') return formatVolume(value);
                    return formatPrice(value);
                  }}
                />
                <Legend />

                {/* Price Line */}
                <Line
                  yAxisId="price"
                  type="monotone"
                  dataKey="price"
                  stroke="#2563eb"
                  dot={false}
                  name="Price"
                />

                {/* Moving Averages */}
                {indicators.sma20 && (
                  <Line
                    yAxisId="price"
                    type="monotone"
                    dataKey="sma20"
                    stroke="#10b981"
                    dot={false}
                    name="SMA 20"
                  />
                )}
                {indicators.sma50 && (
                  <Line
                    yAxisId="price"
                    type="monotone"
                    dataKey="sma50"
                    stroke="#f59e0b"
                    dot={false}
                    name="SMA 50"
                  />
                )}
                {indicators.sma200 && (
                  <Line
                    yAxisId="price"
                    type="monotone"
                    dataKey="sma200"
                    stroke="#ef4444"
                    dot={false}
                    name="SMA 200"
                  />
                )}

                {/* Volume */}
                {indicators.volume && (
                  <Bar
                    yAxisId="volume"
                    dataKey="volume"
                    fill="#93c5fd"
                    opacity={0.3}
                    name="Volume"
                  />
                )}
              </ComposedChart>
            </ResponsiveContainer>
          </div>

          {/* RSI Chart */}
          {indicators.rsi && (
            <div className="h-[200px]">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="date" 
                    tickFormatter={formatDate}
                  />
                  <YAxis 
                    domain={[0, 100]}
                    ticks={[30, 50, 70]}
                  />
                  <Tooltip
                    labelFormatter={formatDate}
                  />
                  <Line
                    type="monotone"
                    dataKey="rsi"
                    stroke="#8b5cf6"
                    dot={false}
                    name="RSI"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* Indicator Controls */}
          <div className="flex flex-wrap gap-2">
            {indicatorsList.map((indicator) => (
              <button
                key={indicator}
                onClick={() => onIndicatorToggle(indicator)}
                className={`px-3 py-1 rounded ${
                  indicators[indicator] ? 'bg-blue-100 text-blue-800' : 'bg-gray-100'
                }`}
              >
                {getIndicatorLabel(indicator)}
              </button>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default TechnicalChart;