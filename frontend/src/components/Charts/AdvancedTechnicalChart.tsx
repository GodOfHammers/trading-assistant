// frontend/src/components/Charts/AdvancedTechnicalChart.tsx

import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import {
  LineChart, Line, BarChart, Bar, ComposedChart,
  XAxis, YAxis, Tooltip, Legend, ResponsiveContainer,
  Area, Brush, ReferenceLine
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
  bollinger_upper?: number;
  bollinger_lower?: number;
  predicted_price?: number;
}

interface TechnicalChartProps {
  data: ChartData[];
  symbol: string;
  predictions?: boolean;
  onTimeframeChange?: (timeframe: string) => void;
  onIndicatorToggle?: (indicator: string) => void;
}

const AdvancedTechnicalChart: React.FC<TechnicalChartProps> = ({
  data,
  symbol,
  predictions = false,
  onTimeframeChange,
  onIndicatorToggle
}) => {
  const [activeIndicators, setActiveIndicators] = useState({
    sma20: true,
    sma50: true,
    sma200: false,
    volume: true,
    rsi: true,
    macd: true,
    bollinger: true
  });

  const [timeframe, setTimeframe] = useState('1M');

  const formatDate = (date: string) => {
    return new Date(date).toLocaleDateString();
  };

  const formatPrice = (price: number) => {
    return `$${price.toFixed(2)}`;
  };

  const formatVolume = (volume: number) => {
    if (volume >= 1000000000) return `${(volume / 1000000000).toFixed(1)}B`;
    if (volume >= 1000000) return `${(volume / 1000000).toFixed(1)}M`;
    if (volume >= 1000) return `${(volume / 1000).toFixed(1)}K`;
    return volume.toString();
  };

  const handleIndicatorToggle = (indicator: string) => {
    setActiveIndicators(prev => ({
      ...prev,
      [indicator]: !prev[indicator]
    }));
    onIndicatorToggle?.(indicator);
  };

  const handleTimeframeChange = (newTimeframe: string) => {
    setTimeframe(newTimeframe);
    onTimeframeChange?.(newTimeframe);
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <div className="flex justify-between items-center">
          <CardTitle>{symbol} Technical Analysis</CardTitle>
          <div className="flex gap-2">
            {['1D', '1W', '1M', '3M', '1Y'].map(tf => (
              <button
                key={tf}
                onClick={() => handleTimeframeChange(tf)}
                className={`px-3 py-1 rounded text-sm ${
                  timeframe === tf 
                    ? 'bg-blue-500 text-white' 
                    : 'bg-gray-100 hover:bg-gray-200'
                }`}
              >
                {tf}
              </button>
            ))}
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {/* Price Chart */}
          <div className="h-[400px]">
            <ResponsiveContainer width="100%" height="100%">
              <ComposedChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                <XAxis dataKey="date" tickFormatter={formatDate} />
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
                    if (name === 'Volume') return [formatVolume(value), name];
                    return [formatPrice(value), name];
                  }}
                />
                <Legend />

                {/* Candlesticks/Price */}
                <Line
                  type="linear"
                  dataKey="price"
                  stroke="#2563eb"
                  dot={false}
                  yAxisId="price"
                  name="Price"
                />

                {/* Moving Averages */}
                {activeIndicators.sma20 && (
                  <Line
                    type="linear"
                    dataKey="sma20"
                    stroke="#10b981"
                    dot={false}
                    yAxisId="price"
                    name="SMA 20"
                  />
                )}
                {activeIndicators.sma50 && (
                  <Line
                    type="linear"
                    dataKey="sma50"
                    stroke="#f59e0b"
                    dot={false}
                    yAxisId="price"
                    name="SMA 50"
                  />
                )}
                {activeIndicators.sma200 && (
                  <Line
                    type="linear"
                    dataKey="sma200"
                    stroke="#ef4444"
                    dot={false}
                    yAxisId="price"
                    name="SMA 200"
                  />
                )}

                {/* Bollinger Bands */}
                {activeIndicators.bollinger && (
                  <>
                    <Line
                      type="linear"
                      dataKey="bollinger_upper"
                      stroke="#9333ea"
                      strokeDasharray="5 5"
                      dot={false}
                      yAxisId="price"
                      name="Bollinger Upper"
                    />
                    <Line
                      type="linear"
                      dataKey="bollinger_lower"
                      stroke="#9333ea"
                      strokeDasharray="5 5"
                      dot={false}
                      yAxisId="price"
                      name="Bollinger Lower"
                    />
                  </>
                )}

                {/* Predictions */}
                {predictions && (
                  <Line
                    type="linear"
                    dataKey="predicted_price"
                    stroke="#dc2626"
                    strokeWidth={2}
                    dot={true}
                    yAxisId="price"
                    name="Predicted"
                  />
                )}

                {/* Volume */}
                {activeIndicators.volume && (
                  <Bar
                    dataKey="volume"
                    fill="#93c5fd"
                    yAxisId="volume"
                    opacity={0.3}
                    name="Volume"
                  />
                )}

                <Brush dataKey="date" height={30} stroke="#8884d8" />
              </ComposedChart>
            </ResponsiveContainer>
          </div>

          {/* RSI Chart */}
          {activeIndicators.rsi && (
            <div className="h-[200px]">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                  <XAxis dataKey="date" tickFormatter={formatDate} />
                  <YAxis domain={[0, 100]} />
                  <Tooltip labelFormatter={formatDate} />
                  <Legend />
                  <ReferenceLine y={70} strokeDasharray="3 3" stroke="#ef4444" />
                  <ReferenceLine y={30} strokeDasharray="3 3" stroke="#10b981" />
                  <Line
                    type="linear"
                    dataKey="rsi"
                    stroke="#8b5cf6"
                    dot={false}
                    name="RSI"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* MACD Chart */}
          {activeIndicators.macd && (
            <div className="h-[200px]">
              <ResponsiveContainer width="100%" height="100%">
                <ComposedChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                  <XAxis dataKey="date" tickFormatter={formatDate} />
                  <YAxis />
                  <Tooltip labelFormatter={formatDate} />
                  <Legend />
                  <Line
                    type="linear"
                    dataKey="macd"
                    stroke="#2563eb"
                    dot={false}
                    name="MACD"
                  />
                  <Line
                    type="linear"
                    dataKey="macd_signal"
                    stroke="#f59e0b"
                    dot={false}
                    name="Signal"
                  />
                  <Bar
                    dataKey="macd_hist"
                    fill="#10b981"
                    name="Histogram"
                  />
                </ComposedChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* Indicator Toggle Buttons */}
          <div className="flex flex-wrap gap-2">
            {Object.entries(activeIndicators).map(([indicator, active]) => (
              <button
                key={indicator}
                onClick={() => handleIndicatorToggle(indicator)}
                className={`px-3 py-1 rounded text-sm ${
                  active 
                    ? 'bg-blue-500 text-white' 
                    : 'bg-gray-100 hover:bg-gray-200'
                }`}
              >
                {indicator.toUpperCase()}
              </button>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default AdvancedTechnicalChart;