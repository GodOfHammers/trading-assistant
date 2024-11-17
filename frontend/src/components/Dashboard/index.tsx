// frontend/src/components/Dashboard/index.tsx

import React, { useState, useEffect, useCallback } from 'react';
import { Card, CardContent } from '@ui/card'; // Updated import using alias
import StockList from './StockList';
import TechnicalChart from '../Charts/TechnicalChart';
import AnalysisPanel from './AnalysisPanel';
import MarketAnalysis from './MarketAnalysis';
import TradeRecommendations from './TradeRecommendation';
import { stockApi } from '../../services/api';
import { wsService } from '../../services/websocket';
import { Store } from 'react-notifications-component';
import 'react-notifications-component/dist/theme.css';
import type { StockData, MarketData } from '../../types/stock';
import { AlertCircle, TrendingUp, Activity, BarChart2 } from 'lucide-react';

// Notification helper
const notify = (
  title: string,
  message: string,
  type: 'success' | 'danger' | 'info' | 'warning'
) => {
  Store.addNotification({
    title,
    message,
    type,
    insert: 'top',
    container: 'top-right',
    animationIn: ['animate__animated', 'animate__fadeIn'],
    animationOut: ['animate__animated', 'animate__fadeOut'],
    dismiss: {
      duration: 5000,
      onScreen: true,
    },
  });
};

const Dashboard: React.FC = () => {
  // State Management
  const [selectedStock, setSelectedStock] = useState<string | null>(null);
  const [stocksData, setStocksData] = useState<StockData[]>([]);
  const [marketData, setMarketData] = useState<MarketData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState('stocks');

  // Fetch Data
  const fetchStocksData = useCallback(async () => {
    try {
      setLoading(true);
      const [opportunities, market] = await Promise.all([
        stockApi.getTopOpportunities(),
        stockApi.getMarketData(),
      ]);

      setStocksData(opportunities);
      setMarketData(market);
      setError(null);
    } catch (err) {
      console.error('Error fetching data:', err);
      setError('Failed to fetch market data');
      notify('Error', 'Failed to fetch market data', 'danger');
    } finally {
      setLoading(false);
    }
  }, []);

  // WebSocket Setup
  useEffect(() => {
    wsService.connect();

    // Subscribe to real-time updates
    wsService.subscribe('stockUpdate', handleStockUpdate);
    wsService.subscribe('marketUpdate', handleMarketUpdate);

    // Initial data fetch
    fetchStocksData();

    // Refresh data periodically
    const interval = setInterval(fetchStocksData, 60000);

    return () => {
      clearInterval(interval);
      wsService.unsubscribe('stockUpdate', handleStockUpdate);
      wsService.unsubscribe('marketUpdate', handleMarketUpdate);
      wsService.disconnect();
    };
  }, [fetchStocksData]);

  // Update Handlers
  const handleStockUpdate = (data: StockData) => {
    setStocksData((prevStocks) => {
      const updatedStocks = prevStocks.map((stock) =>
        stock.symbol === data.symbol ? { ...stock, ...data } : stock
      );

      if (Math.abs(data.change_percent) > 5) {
        notify(
          'Significant Price Movement',
          `${data.symbol} has moved ${data.change_percent.toFixed(2)}%`,
          'info'
        );
      }

      return updatedStocks;
    });
  };

  const handleMarketUpdate = (data: MarketData) => {
    setMarketData((prevData) => ({ ...prevData, ...data }));
  };

  // Trade Action Handler
  const handleTradeAction = async (symbol: string, action: string) => {
    try {
      await stockApi.executeTrade({ symbol, action });
      notify('Trade Executed', `${action} order placed for ${symbol}`, 'success');
    } catch (err) {
      notify('Trade Error', 'Failed to execute trade. Please try again.', 'danger');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold">Stock Trading Dashboard</h1>
          {loading ? (
            <div className="flex items-center">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500 mr-2" />
              <span className="text-sm text-gray-500">Updating...</span>
            </div>
          ) : error ? (
            <div className="flex items-center text-red-500">
              <AlertCircle className="h-4 w-4 mr-2" />
              <span className="text-sm">{error}</span>
            </div>
          ) : null}
        </div>

        {/* Navigation */}
        <div className="flex space-x-2 border-b border-gray-200 mb-6">
          <button
            onClick={() => setActiveTab('stocks')}
            className={`flex items-center px-4 py-2 text-sm font-medium rounded-t-lg ${
              activeTab === 'stocks'
                ? 'text-blue-600 bg-blue-50 border-b-2 border-blue-600'
                : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
            }`}
          >
            <TrendingUp className="h-4 w-4 mr-2" />
            Stocks
          </button>
          <button
            onClick={() => setActiveTab('market')}
            className={`flex items-center px-4 py-2 text-sm font-medium rounded-t-lg ${
              activeTab === 'market'
                ? 'text-blue-600 bg-blue-50 border-b-2 border-blue-600'
                : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
            }`}
          >
            <BarChart2 className="h-4 w-4 mr-2" />
            Market Analysis
          </button>
          <button
            onClick={() => setActiveTab('trades')}
            className={`flex items-center px-4 py-2 text-sm font-medium rounded-t-lg ${
              activeTab === 'trades'
                ? 'text-blue-600 bg-blue-50 border-b-2 border-blue-600'
                : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
            }`}
          >
            <Activity className="h-4 w-4 mr-2" />
            Trade Recommendations
          </button>
        </div>

        {/* Content */}
        {activeTab === 'stocks' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 space-y-6">
              {selectedStock ? (
                <>
                  <TechnicalChart
                    symbol={selectedStock}
                    data={
                      stocksData.find((s) => s.symbol === selectedStock)?.historical_data || []
                    }
                  />
                  <AnalysisPanel
                    data={stocksData.find((s) => s.symbol === selectedStock)}
                  />
                </>
              ) : (
                <Card>
                  <CardContent className="p-12 text-center text-gray-500">
                    Select a stock to view detailed analysis
                  </CardContent>
                </Card>
              )}
            </div>
            <div>
              <StockList
                stocks={stocksData}
                onSelect={setSelectedStock}
                selectedStock={selectedStock}
              />
            </div>
          </div>
        )}

        {activeTab === 'market' && marketData && <MarketAnalysis data={marketData} />}

        {activeTab === 'trades' && (
          <TradeRecommendations
            recommendations={stocksData
              .filter((stock) => stock.recommendation.action !== 'HOLD')
              .map((stock) => ({
                symbol: stock.symbol,
                action: stock.recommendation.action,
                entryPrice: stock.recommendation.entryPrice,
                stopLoss: stock.recommendation.stopLoss,
                takeProfit: stock.recommendation.takeProfit,
                confidence: stock.recommendation.confidence,
                reasoning: stock.recommendation.reasons,
                urgency: stock.recommendation.urgency,
              }))}
            onActionClick={handleTradeAction}
          />
        )}
      </div>
    </div>
  );
};

export default Dashboard;