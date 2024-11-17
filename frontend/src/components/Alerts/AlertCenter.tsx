// frontend/src/components/Alerts/AlertCenter.tsx

import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Alert, AlertTitle, AlertDescription } from '../ui/alert';
import { Bell, AlertTriangle, TrendingUp, TrendingDown, DollarSign } from 'lucide-react';

interface TradeAlert {
  id: string;
  type: 'ENTRY' | 'EXIT' | 'STOP_LOSS' | 'TAKE_PROFIT' | 'PRICE_ALERT';
  symbol: string;
  message: string;
  price: number;
  timestamp: string;
  priority: 'HIGH' | 'MEDIUM' | 'LOW';
  acknowledged: boolean;
}

interface AlertCenterProps {
  alerts: TradeAlert[];
  onAcknowledge: (alertId: string) => void;
  onClear: (alertId: string) => void;
}

const AlertCenter: React.FC<AlertCenterProps> = ({ 
  alerts, 
  onAcknowledge, 
  onClear 
}) => {
  const getPriorityStyles = (priority: string) => {
    switch (priority) {
      case 'HIGH':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'MEDIUM':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'LOW':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getAlertIcon = (type: string) => {
    switch (type) {
      case 'ENTRY':
        return <TrendingUp className="h-5 w-5" />;
      case 'EXIT':
        return <TrendingDown className="h-5 w-5" />;
      case 'STOP_LOSS':
        return <AlertTriangle className="h-5 w-5" />;
      case 'TAKE_PROFIT':
        return <DollarSign className="h-5 w-5" />;
      default:
        return <Bell className="h-5 w-5" />;
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Bell className="h-5 w-5" />
          Trade Alerts
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {alerts.map((alert) => (
            <div
              key={alert.id}
              className={`border rounded-lg p-4 ${getPriorityStyles(alert.priority)} ${
                alert.acknowledged ? 'opacity-60' : ''
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-3">
                  {getAlertIcon(alert.type)}
                  <div>
                    <div className="font-semibold">
                      {alert.symbol} - ${alert.price}
                    </div>
                    <div className="text-sm mt-1">{alert.message}</div>
                    <div className="text-xs mt-2">
                      {new Date(alert.timestamp).toLocaleString()}
                    </div>
                  </div>
                </div>
                <div className="flex gap-2">
                  {!alert.acknowledged && (
                    <button
                      onClick={() => onAcknowledge(alert.id)}
                      className="text-sm px-3 py-1 rounded-md bg-white bg-opacity-50 hover:bg-opacity-75"
                    >
                      Acknowledge
                    </button>
                  )}
                  <button
                    onClick={() => onClear(alert.id)}
                    className="text-sm px-3 py-1 rounded-md bg-white bg-opacity-50 hover:bg-opacity-75"
                  >
                    Clear
                  </button>
                </div>
              </div>
            </div>
          ))}

          {alerts.length === 0 && (
            <div className="text-center py-6 text-gray-500">
              No active alerts
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default AlertCenter;