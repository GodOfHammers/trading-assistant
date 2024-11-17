# backend/core/backtester.py

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from .advanced_indicators import AdvancedTechnicalIndicators

@dataclass
class TradeResult:
    entry_date: datetime
    exit_date: datetime
    entry_price: float
    exit_price: float
    position_size: float
    pnl: float
    pnl_percentage: float
    max_drawdown: float
    holding_period: int
    trade_type: str  # 'LONG' or 'SHORT'

@dataclass
class BacktestResult:
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    avg_profit: float
    avg_loss: float
    profit_factor: float
    sharpe_ratio: float
    sortino_ratio: float
    max_drawdown: float
    total_return: float
    annualized_return: float
    trades: List[TradeResult]

class AdvancedBacktester:
    def __init__(self, 
                 initial_capital: float = 100000.0,
                 position_size: float = 0.02,  # 2% of capital per trade
                 max_positions: int = 5):
        self.initial_capital = initial_capital
        self.position_size = position_size
        self.max_positions = max_positions
        self.technical_indicators = AdvancedTechnicalIndicators()

    def run_backtest(self, model, data: pd.DataFrame, validation_data: pd.DataFrame) -> BacktestResult:
        """Run comprehensive backtest of the trading strategy."""
        trades = []
        capital = self.initial_capital
        positions = {}
        max_drawdown = 0
        peak_capital = capital
        daily_returns = []

        # Prepare features for both training and validation periods
        train_features = self.technical_indicators.calculate_all(data)
        val_features = self.technical_indicators.calculate_all(validation_data)

        for date, row in validation_data.iterrows():
            # Update positions and capital
            closed_positions = self._update_positions(positions, row, date)
            for pos in closed_positions:
                capital += pos.pnl
                trades.append(pos)
                if capital > peak_capital:
                    peak_capital = capital
                drawdown = (peak_capital - capital) / peak_capital
                max_drawdown = max(max_drawdown, drawdown)

            # Get new signals if we have capacity
            if len(positions) < self.max_positions:
                features = self._prepare_features(val_features, date)
                signal = model.predict_single(features)
                
                if self._should_enter_trade(signal, positions):
                    position_capital = capital * self.position_size
                    entry_price = row['Close']
                    size = position_capital / entry_price
                    
                    positions[date] = {
                        'type': 'LONG' if signal > 0 else 'SHORT',
                        'size': size,
                        'entry_price': entry_price,
                        'entry_date': date,
                        'stop_loss': self._calculate_stop_loss(entry_price, signal),
                        'take_profit': self._calculate_take_profit(entry_price, signal)
                    }

            # Calculate daily return
            daily_return = (capital - self.initial_capital) / self.initial_capital
            daily_returns.append(daily_return)

        # Calculate performance metrics
        results = self._calculate_performance_metrics(trades, daily_returns)
        return results

    def _update_positions(self, positions: Dict, current_data: pd.Series, 
                         current_date: datetime) -> List[TradeResult]:
        """Update open positions and return closed ones."""
        closed_positions = []
        positions_to_remove = []

        for entry_date, position in positions.items():
            # Check stop loss and take profit
            if position['type'] == 'LONG':
                if current_data['Low'] <= position['stop_loss']:
                    # Stop loss hit
                    closed_positions.append(self._close_position(position, position['stop_loss'], 
                                                              current_date, 'Stop Loss'))
                    positions_to_remove.append(entry_date)
                elif current_data['High'] >= position['take_profit']:
                    # Take profit hit
                    closed_positions.append(self._close_position(position, position['take_profit'], 
                                                              current_date, 'Take Profit'))
                    positions_to_remove.append(entry_date)
            else:  # SHORT position
                if current_data['High'] >= position['stop_loss']:
                    closed_positions.append(self._close_position(position, position['stop_loss'], 
                                                              current_date, 'Stop Loss'))
                    positions_to_remove.append(entry_date)
                elif current_data['Low'] <= position['take_profit']:
                    closed_positions.append(self._close_position(position, position['take_profit'], 
                                                              current_date, 'Take Profit'))
                    positions_to_remove.append(entry_date)

        # Remove closed positions
        for date in positions_to_remove:
            del positions[date]

        return closed_positions

    def _close_position(self, position: Dict, exit_price: float, 
                       exit_date: datetime, reason: str) -> TradeResult:
        """Close a position and calculate its results."""
        if position['type'] == 'LONG':
            pnl = (exit_price - position['entry_price']) * position['size']
            pnl_percentage = (exit_price - position['entry_price']) / position['entry_price'] * 100
        else:  # SHORT
            pnl = (position['entry_price'] - exit_price) * position['size']
            pnl_percentage = (position['entry_price'] - exit_price) / position['entry_price'] * 100

        return TradeResult(
            entry_date=position['entry_date'],
            exit_date=exit_date,
            entry_price=position['entry_price'],
            exit_price=exit_price,
            position_size=position['size'],
            pnl=pnl,
            pnl_percentage=pnl_percentage,
            max_drawdown=0,  # Will be calculated later
            holding_period=(exit_date - position['entry_date']).days,
            trade_type=position['type']
        )

    def _calculate_performance_metrics(self, trades: List[TradeResult], 
                                    daily_returns: List[float]) -> BacktestResult:
        """Calculate comprehensive performance metrics."""
        if not trades:
            return BacktestResult(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, [])

        # Basic trade metrics
        winning_trades = len([t for t in trades if t.pnl > 0])
        losing_trades = len([t for t in trades if t.pnl < 0])
        
        # Calculate averages
        profits = [t.pnl for t in trades if t.pnl > 0]
        losses = [t.pnl for t in trades if t.pnl < 0]
        avg_profit = np.mean(profits) if profits else 0
        avg_loss = abs(np.mean(losses)) if losses else 0
        
        # Risk metrics
        daily_returns = np.array(daily_returns)
        risk_free_rate = 0.02  # Assume 2% annual risk-free rate
        excess_returns = daily_returns - (risk_free_rate / 252)
        
        sharpe_ratio = np.sqrt(252) * np.mean(excess_returns) / np.std(excess_returns) if len(excess_returns) > 0 else 0
        downside_returns = np.array([r for r in excess_returns if r < 0])
        sortino_ratio = np.sqrt(252) * np.mean(excess_returns) / np.std(downside_returns) if len(downside_returns) > 0 else 0
        
        # Calculate max drawdown
        cumulative_returns = np.cumprod(1 + daily_returns)
        peak = np.maximum.accumulate(cumulative_returns)
        drawdowns = (peak - cumulative_returns) / peak
        max_drawdown = np.max(drawdowns)
        
        return BacktestResult(
            total_trades=len(trades),
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            win_rate=winning_trades / len(trades) if trades else 0,
            avg_profit=avg_profit,
            avg_loss=avg_loss,
            profit_factor=sum(profits) / abs(sum(losses)) if losses else float('inf'),
            sharpe_ratio=sharpe_ratio,
            sortino_ratio=sortino_ratio,
            max_drawdown=max_drawdown,
            total_return=cumulative_returns[-1] - 1,
            annualized_return=((1 + cumulative_returns[-1]) ** (252 / len(daily_returns))) - 1,
            trades=trades
        )