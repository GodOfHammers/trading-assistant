// frontend/src/components/Dashboard/AnalysisPanel.tsx

import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@ui/card'; // Use alias '@ui'
import { Alert, AlertTitle, AlertDescription } from '@ui/alert'; // Use alias '@ui'
import { 
  TrendingUp, TrendingDown, AlertTriangle, 
  DollarSign, Clock, BarChart2, Activity,
  Target, ArrowUp, ArrowDown
} from 'lucide-react';
import {
  LineChart, Line, BarChart, Bar, 
  ResponsiveContainer, XAxis, YAxis, Tooltip
} from 'recharts';
import type { StockData } from '../../types/stock';

interface AnalysisPanelProps {
  data: StockData;
}

const AnalysisPanel: React.FC<AnalysisPanelProps> = ({ data }) => {
  if (!data) return null;

  const {
    symbol,
    technical_analysis,
    sentiment,
    risk_assessment,
    recommendation,
    profit_potential
  } = data;

  const renderTechnicalIndicators = () => (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {Object.entries(technical_analysis.signals).map(([key, value]) => (
        <div key={key} className="p-3 bg-gray-50 rounded-lg">
          <div className="text-sm text-gray-500 mb-1">{key.toUpperCase()}</div>
          <div className="text-lg font-semibold">
            {typeof value === 'number' ? value.toFixed(2) : value}
          </div>
        </div>
      ))}
    </div>
  );

  const renderSentimentAnalysis = () => (
    <Card className="mt-4">
      <CardHeader>
        <CardTitle className="text-lg">Market Sentiment</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="text-sm">Overall Score</div>
            <div className={`font-semibold ${
              sentiment.score > 0.6 ? 'text-green-600' : 
              sentiment.score < 0.4 ? 'text-red-600' : 
              'text-yellow-600'
            }`}>
              {(sentiment.score * 100).toFixed(0)}%
            </div>
          </div>

          <div className="space-y-2">
            <div className="text-sm font-medium">News Sentiment</div>
            <div className="grid grid-cols-3 gap-2">
              <div className="bg-green-100 p-2 rounded">
                <div className="text-xs text-gray-600">Positive</div>
                <div className="font-medium text-green-700">
                  {(sentiment.news_sentiment.positive * 100).toFixed(0)}%
                </div>
              </div>
              <div className="bg-red-100 p-2 rounded">
                <div className="text-xs text-gray-600">Negative</div>
                <div className="font-medium text-red-700">
                  {(sentiment.news_sentiment.negative * 100).toFixed(0)}%
                </div>
              </div>
              <div className="bg-gray-100 p-2 rounded">
                <div className="text-xs text-gray-600">Neutral</div>
                <div className="font-medium text-gray-700">
                  {(sentiment.news_sentiment.neutral * 100).toFixed(0)}%
                </div>
              </div>
            </div>
          </div>

          <div>
            <div className="text-sm font-medium mb-2">Key Topics</div>
            <div className="flex flex-wrap gap-2">
              {sentiment.key_topics.map((topic, index) => (
                <span key={index} className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">
                  {topic}
                </span>
              ))}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );

  const renderProfitAnalysis = () => (
    <Card className="mt-4">
      <CardHeader>
        <CardTitle className="text-lg">Profit Analysis</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="grid grid-cols-3 gap-4">
            <div>
              <div className="text-sm text-gray-500">Expected Return</div>
              <div className="text-lg font-semibold text-green-600">
                {profit_potential.expected_return.toFixed(2)}%
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-500">Probability</div>
              <div className="text-lg font-semibold">
                {(profit_potential.probability * 100).toFixed(0)}%
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-500">Timeframe</div>
              <div className="text-lg font-semibold">
                {profit_potential.timeframe}
              </div>
            </div>
          </div>

          <div className="space-y-2">
            <div className="text-sm font-medium">Scenario Analysis</div>
            <div className="grid grid-cols-3 gap-2">
              <div className="p-2 border rounded">
                <div className="text-xs text-gray-500">Bullish</div>
                <div className="font-medium text-green-600">
                  ${profit_potential.scenarios.bullish.price.toFixed(2)}
                </div>
                <div className="text-xs text-gray-500">
                  {(profit_potential.scenarios.bullish.probability * 100).toFixed(0)}%
                </div>
              </div>
              <div className="p-2 border rounded">
                <div className="text-xs text-gray-500">Base</div>
                <div className="font-medium">
                  ${profit_potential.scenarios.base.price.toFixed(2)}
                </div>
                <div className="text-xs text-gray-500">
                  {(profit_potential.scenarios.base.probability * 100).toFixed(0)}%
                </div>
              </div>
              <div className="p-2 border rounded">
                <div className="text-xs text-gray-500">Bearish</div>
                <div className="font-medium text-red-600">
                  ${profit_potential.scenarios.bearish.price.toFixed(2)}
                </div>
                <div className="text-xs text-gray-500">
                  {(profit_potential.scenarios.bearish.probability * 100).toFixed(0)}%
                </div>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );

  const renderRiskAssessment = () => (
    <Card className="mt-4">
      <CardHeader>
        <CardTitle className="text-lg">Risk Assessment</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            <div>
              <div className="text-sm text-gray-500">Risk Level</div>
              <div className={`text-lg font-semibold ${
                risk_assessment.risk_level < 0.3 ? 'text-green-600' :
                risk_assessment.risk_level > 0.7 ? 'text-red-600' :
                'text-yellow-600'
              }`}>
                {(risk_assessment.risk_level * 100).toFixed(0)}%
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-500">Beta</div>
              <div className="text-lg font-semibold">
                {risk_assessment.beta.toFixed(2)}
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-500">Sharpe Ratio</div>
              <div className="text-lg font-semibold">
                {risk_assessment.sharpe_ratio.toFixed(2)}
              </div>
            </div>
          </div>

          <div>
            <div className="text-sm font-medium mb-2">Risk Factors</div>
            <div className="space-y-2">
              {Object.entries(risk_assessment.risk_factors).map(([factor, value]) => (
                <div key={factor} className="flex items-center justify-between">
                  <div className="text-sm capitalize">
                    {factor.replace(/_/g, ' ')}
                  </div>
                  <div className={`text-sm font-medium ${
                    value > 0.7 ? 'text-red-600' :
                    value < 0.3 ? 'text-green-600' :
                    'text-yellow-600'
                  }`}>
                    {(value * 100).toFixed(0)}%
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );

  return (
    <div className="space-y-6">
      {/* Trading Recommendation */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            Trading Recommendation
            <span className={`text-sm px-3 py-1 rounded-full ${
              recommendation.action === 'STRONG_BUY' ? 'bg-green-100 text-green-800' :
              recommendation.action === 'BUY' ? 'bg-blue-100 text-blue-800' :
              recommendation.action === 'SELL' ? 'bg-red-100 text-red-800' :
              'bg-yellow-100 text-yellow-800'
            }`}>
              {recommendation.action}
            </span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <div className="text-sm text-gray-500">Entry Price</div>
              <div className="text-lg font-semibold">
                ${recommendation.entryPrice.toFixed(2)}
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-500">Stop Loss</div>
              <div className="text-lg font-semibold text-red-600">
                ${recommendation.stopLoss.toFixed(2)}
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-500">Take Profit</div>
              <div className="text-lg font-semibold text-green-600">
                ${recommendation.takeProfit.toFixed(2)}
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-500">Time Horizon</div>
              <div className="text-lg font-semibold">
                {recommendation.timeHorizon}
              </div>
            </div>
          </div>

          <div className="space-y-2">
            {recommendation.reasons.map((reason, index) => (
              <div key={index} className="flex items-center text-sm">
                <Target className="h-4 w-4 mr-2 text-blue-500" />
                {reason}
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Technical Analysis */}
      {renderTechnicalIndicators()}

      {/* Sentiment Analysis */}
      {renderSentimentAnalysis()}

      {/* Profit Analysis */}
      {renderProfitAnalysis()}

      {/* Risk Assessment */}
      {renderRiskAssessment()}
    </div>
  );
};

export default AnalysisPanel;