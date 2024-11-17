// frontend/src/components/Dashboard/MarketAnalysis.tsx

import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@ui/tabs';
import {
  LineChart, Line, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, Tooltip, Legend, ResponsiveContainer, Area, 
  AreaChart, Scatter, ComposedChart, TreeMap
} from 'recharts';
import { 
  TrendingUp, TrendingDown, AlertTriangle, 
  Activity, DollarSign, BarChart2, ArrowUp, ArrowDown 
} from 'lucide-react';
import type { MarketData } from '../../types/stock';
import { HeatMapGrid } from 'react-grid-heatmap';

interface MarketAnalysisProps {
  data: MarketData;
  onSectorSelect?: (sector: string) => void;
}

const MarketAnalysis: React.FC<MarketAnalysisProps> = ({ data, onSectorSelect }) => {
  const [activeTab, setActiveTab] = useState('overview');
  const [timeframe, setTimeframe] = useState('1D');

  const COLORS = ['#10B981', '#EF4444', '#F59E0B', '#3B82F6', '#8B5CF6'];
  const TIMEFRAMES = ['1D', '1W', '1M', '3M', '6M', '1Y'];

  const formatPercentage = (value: number) => `${value.toFixed(2)}%`;
  const formatNumber = (value: number) => value.toLocaleString();
  const formatCurrency = (value: number) => 
    new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value);

  const renderMarketOverview = () => (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {/* Market Summary */}
      <Card className="md:col-span-2">
        <CardHeader>
          <CardTitle className="text-lg flex justify-between items-center">
            <span>Market Summary</span>
            <div className="flex space-x-2">
              {TIMEFRAMES.map((tf) => (
                <button
                  key={tf}
                  onClick={() => setTimeframe(tf)}
                  className={`px-2 py-1 text-sm rounded ${
                    timeframe === tf 
                      ? 'bg-blue-100 text-blue-800' 
                      : 'hover:bg-gray-100'
                  }`}
                >
                  {tf}
                </button>
              ))}
            </div>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
            {Object.entries(data.indices).map(([name, index]) => (
              <div key={name} className="p-4 border rounded-lg">
                <div className="text-sm text-gray-500">{name}</div>
                <div className="text-xl font-bold">{formatNumber(index.value)}</div>
                <div className={`flex items-center text-sm ${
                  index.change >= 0 ? 'text-green-600' : 'text-red-600'
                }`}>
                  {index.change >= 0 ? (
                    <ArrowUp className="h-4 w-4 mr-1" />
                  ) : (
                    <ArrowDown className="h-4 w-4 mr-1" />
                  )}
                  {formatPercentage(index.change_percent)}
                </div>
              </div>
            ))}
          </div>

          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <ComposedChart data={data.indexHistory}>
                <XAxis dataKey="timestamp" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Area
                  type="monotone"
                  dataKey="value"
                  fill="#3B82F6"
                  stroke="#2563EB"
                  fillOpacity={0.1}
                />
                <Bar dataKey="volume" fill="#6B7280" opacity={0.3} />
              </ComposedChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      {/* Market Breadth */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Market Breadth</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="text-center p-4 bg-green-50 rounded-lg">
                <div className="text-2xl font-bold text-green-600">
                  {formatNumber(data.market_breadth.advancers)}
                </div>
                <div className="text-sm text-gray-600">Advancing</div>
              </div>
              <div className="text-center p-4 bg-red-50 rounded-lg">
                <div className="text-2xl font-bold text-red-600">
                  {formatNumber(data.market_breadth.decliners)}
                </div>
                <div className="text-sm text-gray-600">Declining</div>
              </div>
            </div>

            <div className="h-[200px]">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={[
                      { name: 'Advancers', value: data.market_breadth.advancers },
                      { name: 'Decliners', value: data.market_breadth.decliners },
                      { name: 'Unchanged', value: data.market_breadth.unchanged }
                    ]}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={80}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    <Cell fill="#10B981" />
                    <Cell fill="#EF4444" />
                    <Cell fill="#6B7280" />
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>

            <div className="grid grid-cols-2 gap-4 text-center">
              <div>
                <div className="text-sm text-gray-500">New Highs</div>
                <div className="text-lg font-bold text-green-600">
                  {data.market_breadth.new_highs}
                </div>
              </div>
              <div>
                <div className="text-sm text-gray-500">New Lows</div>
                <div className="text-lg font-bold text-red-600">
                  {data.market_breadth.new_lows}
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Volatility Metrics */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Volatility</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 border rounded-lg">
                <div className="text-sm text-gray-500">VIX</div>
                <div className={`text-2xl font-bold ${
                  data.volatility.vix > 20 ? 'text-red-600' : 'text-green-600'
                }`}>
                  {data.volatility.vix.toFixed(2)}
                </div>
              </div>
              <div className="p-4 border rounded-lg">
                <div className="text-sm text-gray-500">Historical Vol</div>
                <div className="text-2xl font-bold">
                  {formatPercentage(data.volatility.historical_volatility)}
                </div>
              </div>
            </div>

            <div className="h-[200px]">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data.volatility_history}>
                  <XAxis dataKey="timestamp" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="vix"
                    stroke="#EF4444"
                    dot={false}
                  />
                  <Line
                    type="monotone"
                    dataKey="historical"
                    stroke="#6B7280"
                    dot={false}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Sector Performance */}
      <Card className="md:col-span-2">
        <CardHeader>
          <CardTitle className="text-lg">Sector Performance</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-[400px]">
            <ResponsiveContainer width="100%" height="100%">
              <TreeMap
                data={Object.entries(data.sectors).map(([sector, data]) => ({
                  name: sector,
                  size: data.volume,
                  value: data.performance
                }))}
                dataKey="size"
                aspectRatio={4 / 3}
                stroke="#fff"
                fill="#8884d8"
                content={({ root, depth, x, y, width, height, name, value }) => (
                  <g>
                    <rect
                      x={x}
                      y={y}
                      width={width}
                      height={height}
                      style={{
                        fill: value >= 0 ? '#10B981' : '#EF4444',
                        opacity: Math.abs(value) / 5
                      }}
                    />
                    <text
                      x={x + width / 2}
                      y={y + height / 2}
                      textAnchor="middle"
                      fill="#fff"
                      fontSize={14}
                    >
                      {name}
                      <tspan x={x + width / 2} y={y + height / 2 + 20}>
                        {formatPercentage(value)}
                      </tspan>
                    </text>
                  </g>
                )}
              />
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>
    </div>
  );

  return (
    <div className="space-y-4">
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="overview">
            <BarChart2 className="h-4 w-4 mr-2" />
            Market Overview
          </TabsTrigger>
          <TabsTrigger value="sectors">
            <Activity className="h-4 w-4 mr-2" />
            Sector Analysis
          </TabsTrigger>
          <TabsTrigger value="technicals">
            <TrendingUp className="h-4 w-4 mr-2" />
            Technical Overview
          </TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="mt-4">
          {renderMarketOverview()}
        </TabsContent>

        <TabsContent value="sectors" className="mt-4">
          {/* Implement sector analysis view */}
        </TabsContent>

        <TabsContent value="technicals" className="mt-4">
          {/* Implement technical analysis view */}
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default MarketAnalysis;