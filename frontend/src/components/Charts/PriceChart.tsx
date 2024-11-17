import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface PriceData {
  date: string;
  price: number;
}

interface PriceChartProps {
  symbol: string;
  data: PriceData[];
}

const PriceChart: React.FC<PriceChartProps> = ({ symbol, data }) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{symbol} Price History</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-[400px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="date" 
                tickFormatter={(value) => new Date(value).toLocaleDateString()}
              />
              <YAxis 
                domain={['auto', 'auto']}
                tickFormatter={(value) => `$${value.toFixed(2)}`}
              />
              <Tooltip 
                labelFormatter={(label) => new Date(label).toLocaleDateString()}
                formatter={(value: any) => [`$${value.toFixed(2)}`, 'Price']}
              />
              <Line
                type="monotone"
                dataKey="price"
                stroke="#2563eb"
                strokeWidth={2}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
};

export default PriceChart;