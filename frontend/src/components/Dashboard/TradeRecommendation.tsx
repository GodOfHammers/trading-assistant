// frontend/src/components/Dashboard/TradeRecommendation.tsx

import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@ui/card';
import { Alert, AlertTitle, AlertDescription } from '@ui/alert';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@ui/dialog";
import { Button } from "../../components/ui/button";
import { Badge } from "../../components/ui/badge";
import { 
  DollarSign, Target, TrendingUp, TrendingDown, 
  AlertTriangle, Clock, BarChart2, Info 
} from 'lucide-react';
import { Sparklines, SparklinesLine } from 'react-sparklines';

interface TradeRecommendation {
  symbol: string;
  action: 'STRONG_BUY' | 'BUY' | 'SELL' | 'STRONG_SELL' | 'HOLD';
  entryPrice: number;
  stopLoss: number;
  takeProfit: number;
  confidence: number;
  reasoning: string[];
  urgency: 'HIGH' | 'MEDIUM' | 'LOW';
  timeHorizon: string;
  priceHistory: number[];
  riskLevel: number;
  potentialReturn: number;
  volume: number;
  additionalMetrics: {
    rsi: number;
    macd: number;
    volatility: number;
  };
}

interface TradeRecommendationsProps {
  recommendations: TradeRecommendation[];
  onActionClick: (symbol: string, action: string) => Promise<void>;
}

const TradeRecommendations: React.FC<TradeRecommendationsProps> = ({ 
  recommendations, 
  onActionClick 
}) => {
  const [selectedTrade, setSelectedTrade] = useState<TradeRecommendation | null>(null);
  const [isExecuting, setIsExecuting] = useState<string | null>(null);
  const [showDialog, setShowDialog] = useState(false);

  const handleTradeAction = async (symbol: string, action: string) => {
    try {
      setIsExecuting(symbol);
      await onActionClick(symbol, action);
      setIsExecuting(null);
    } catch (error) {
      console.error('Trade execution failed:', error);
      setIsExecuting(null);
    }
  };

  const formatVolume = (volume: number) => {
    if (volume >= 1e9) return `${(volume / 1e9).toFixed(1)}B`;
    if (volume >= 1e6) return `${(volume / 1e6).toFixed(1)}M`;
    if (volume >= 1e3) return `${(volume / 1e3).toFixed(1)}K`;
    return volume.toString();
  };

  const getActionColor = (action: string) => {
    switch (action) {
      case 'STRONG_BUY': return 'bg-green-600 hover:bg-green-700';
      case 'BUY': return 'bg-emerald-600 hover:bg-emerald-700';
      case 'SELL': return 'bg-red-600 hover:bg-red-700';
      case 'STRONG_SELL': return 'bg-rose-600 hover:bg-rose-700';
      default: return 'bg-gray-600 hover:bg-gray-700';
    }
  };

  const getUrgencyColor = (urgency: string) => {
    switch (urgency) {
      case 'HIGH': return 'bg-red-100 text-red-800';
      case 'MEDIUM': return 'bg-yellow-100 text-yellow-800';
      case 'LOW': return 'bg-blue-100 text-blue-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const renderTradeDetails = (trade: TradeRecommendation) => (
    <DialogContent className="max-w-2xl">
      <DialogHeader>
        <DialogTitle>Trade Details - {trade.symbol}</DialogTitle>
      </DialogHeader>
      <div className="space-y-4 p-4">
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          <div>
            <div className="text-sm text-gray-500">Entry Price</div>
            <div className="text-lg font-semibold">${trade.entryPrice.toFixed(2)}</div>
          </div>
          <div>
            <div className="text-sm text-gray-500">Stop Loss</div>
            <div className="text-lg font-semibold text-red-600">
              ${trade.stopLoss.toFixed(2)}
            </div>
          </div>
          <div>
            <div className="text-sm text-gray-500">Target</div>
            <div className="text-lg font-semibold text-green-600">
              ${trade.takeProfit.toFixed(2)}
            </div>
          </div>
        </div>

        <div className="border rounded-lg p-4">
          <h4 className="text-sm font-medium mb-2">Technical Indicators</h4>
          <div className="grid grid-cols-3 gap-4">
            <div>
              <div className="text-sm text-gray-500">RSI</div>
              <div className="font-medium">{trade.additionalMetrics.rsi.toFixed(2)}</div>
            </div>
            <div>
              <div className="text-sm text-gray-500">MACD</div>
              <div className="font-medium">{trade.additionalMetrics.macd.toFixed(2)}</div>
            </div>
            <div>
              <div className="text-sm text-gray-500">Volatility</div>
              <div className="font-medium">
                {trade.additionalMetrics.volatility.toFixed(2)}%
              </div>
            </div>
          </div>
        </div>

        <div className="space-y-2">
          <h4 className="text-sm font-medium">Analysis Reasoning</h4>
          {trade.reasoning.map((reason, idx) => (
            <div key={idx} className="flex items-start gap-2 text-sm">
              <div className="mt-1">•</div>
              <div>{reason}</div>
            </div>
          ))}
        </div>

        <div className="mt-4">
          <Button
            className={`w-full ${getActionColor(trade.action)}`}
            onClick={() => handleTradeAction(trade.symbol, trade.action)}
            disabled={!!isExecuting}
          >
            {isExecuting === trade.symbol ? (
              <div className="flex items-center">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2" />
                Executing...
              </div>
            ) : (
              `Execute ${trade.action}`
            )}
          </Button>
        </div>
      </div>
    </DialogContent>
  );

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Target className="h-5 w-5" />
            Trade Recommendations
          </div>
          <Badge variant="outline" className="ml-2">
            {recommendations.length} Active
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {recommendations.map((rec) => (
            <div 
              key={rec.symbol}
              className="border rounded-lg p-4 bg-white shadow-sm hover:shadow-md transition-shadow"
            >
              <div className="flex justify-between items-start mb-3">
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="font-semibold text-lg">{rec.symbol}</h3>
                    <Badge className={getUrgencyColor(rec.urgency)}>
                      {rec.urgency}
                    </Badge>
                  </div>
                  <div className="text-sm text-gray-600">
                    Volume: {formatVolume(rec.volume)}
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => {
                      setSelectedTrade(rec);
                      setShowDialog(true);
                    }}
                  >
                    <Info className="h-4 w-4 mr-1" />
                    Details
                  </Button>
                  <Button
                    className={getActionColor(rec.action)}
                    size="sm"
                    onClick={() => handleTradeAction(rec.symbol, rec.action)}
                    disabled={!!isExecuting}
                  >
                    {rec.action}
                  </Button>
                </div>
              </div>

              <div className="mb-3">
                <Sparklines data={rec.priceHistory} width={200} height={50}>
                  <SparklinesLine
                    style={{
                      stroke: rec.action.includes('BUY') ? '#16a34a' : '#dc2626',
                      strokeWidth: 2,
                      fill: 'none'
                    }}
                  />
                </Sparklines>
              </div>

              <div className="grid grid-cols-4 gap-4 mb-3 text-sm">
                <div>
                  <div className="text-gray-500">Entry</div>
                  <div className="font-medium">${rec.entryPrice.toFixed(2)}</div>
                </div>
                <div>
                  <div className="text-gray-500">Stop</div>
                  <div className="font-medium text-red-600">
                    ${rec.stopLoss.toFixed(2)}
                  </div>
                </div>
                <div>
                  <div className="text-gray-500">Target</div>
                  <div className="font-medium text-green-600">
                    ${rec.takeProfit.toFixed(2)}
                  </div>
                </div>
                <div>
                  <div className="text-gray-500">Return</div>
                  <div className="font-medium text-blue-600">
                    {rec.potentialReturn.toFixed(1)}%
                  </div>
                </div>
              </div>

              {rec.confidence < 0.7 && (
                <Alert className="mt-3" variant="destructive">
                  <AlertTriangle className="h-4 w-4" />
                  <AlertTitle>High Risk Trade</AlertTitle>
                  <AlertDescription>
                    Confidence: {(rec.confidence * 100).toFixed(0)}%
                  </AlertDescription>
                </Alert>
              )}
            </div>
          ))}
        </div>
      </CardContent>

      {/* Trade Details Dialog */}
      <Dialog open={showDialog} onOpenChange={setShowDialog}>
        {selectedTrade && renderTradeDetails(selectedTrade)}
      </Dialog>
    </Card>
  );
};

export default TradeRecommendations;