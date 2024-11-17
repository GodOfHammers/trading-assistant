// frontend/src/components/Portfolio/PositionTracker.tsx

import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { TrendingUp, TrendingDown, DollarSign, Percent } from 'lucide-react';

interface Position {
  symbol: string;
  quantity: number;
  entryPrice: number;
  currentPrice: number;
  stopLoss: number;
  takeProfit: number;
  unrealizedPnL: number;
  unrealizedPnLPercent: number;
  averageCost: number;
  marketValue: number;
  timestamp: string;
}

interface PositionTrackerProps {
  positions: Position[];
  onPositionClick: (symbol: string) => void;
  onModifyPosition: (symbol: string, action: 'increase' | 'decrease' | 'close') => void;
}

const PositionTracker: React.FC<PositionTrackerProps> = ({
  positions,
  onPositionClick,
  onModifyPosition,
}) => {
  const getTotalPnL = () => {
    return positions.reduce((sum, pos) => sum + pos.unrealizedPnL, 0);
  };

  const getTotalValue = () => {
    return positions.reduce((sum, pos) => sum + pos.marketValue, 0);
  };

  return (
    <Card>
      <CardHeader>
        <div className="flex justify-between items-center">
          <CardTitle>Active Positions</CardTitle>
          <div className="text-sm">
            Total P&L: 
            <span className={`ml-2 font-bold ${
              getTotalPnL() >= 0 ? 'text-green-600' : 'text-red-600'
            }`}>
              ${getTotalPnL().toFixed(2)}
            </span>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {positions.map((position) => (
            <div
              key={position.symbol}
              className="border rounded-lg p-4 cursor-pointer hover:bg-gray-50"
              onClick={() => onPositionClick(position.symbol)}
            >
              <div className="flex justify-between items-start mb-3">
                <div>
                  <h3 className="font-semibold text-lg">{position.symbol}</h3>
                  <div className="text-sm text-gray-500">
                    {position.quantity} shares @ ${position.averageCost.toFixed(2)}
                  </div>
                </div>
                <div className={`flex items-center ${
                  position.unrealizedPnL >= 0 ? 'text-green-600' : 'text-red-600'
                }`}>
                  {position.unrealizedPnL >= 0 ? (
                    <TrendingUp className="h-4 w-4 mr-1" />
                  ) : (
                    <TrendingDown className="h-4 w-4 mr-1" />
                  )}
                  ${Math.abs(position.unrealizedPnL).toFixed(2)}
                  <span className="text-sm ml-1">
                    ({position.unrealizedPnLPercent.toFixed(2)}%)
                  </span>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 mb-3">
                <div>
                  <div className="text-sm text-gray-500">Market Value</div>
                  <div className="font-medium">
                    ${position.marketValue.toFixed(2)}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-gray-500">Current Price</div>
                  <div className="font-medium">
                    ${position.currentPrice.toFixed(2)}
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 mb-4">
                <div>
                  <div className="text-sm text-gray-500">Stop Loss</div>
                  <div className="font-medium text-red-600">
                    ${position.stopLoss.toFixed(2)}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-gray-500">Take Profit</div>
                  <div className="font-medium text-green-600">
                    ${position.takeProfit.toFixed(2)}
                  </div>
                </div>
              </div>

              <div className="flex gap-2">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onModifyPosition(position.symbol, 'increase');
                  }}
                  className="px-3 py-1 text-sm rounded bg-green-100 text-green-800 hover:bg-green-200"
                >
                  Add
                </button>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onModifyPosition(position.symbol, 'decrease');
                  }}
                  className="px-3 py-1 text-sm rounded bg-yellow-100 text-yellow-800 hover:bg-yellow-200"
                >
                  Reduce
                </button>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onModifyPosition(position.symbol, 'close');
                  }}
                  className="px-3 py-1 text-sm rounded bg-red-100 text-red-800 hover:bg-red-200"
                >
                  Close
                </button>
              </div>
            </div>
          ))}

          {positions.length === 0 && (
            <div className="text-center py-6 text-gray-500">
              No active positions
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default PositionTracker;