# backend/core/cross_validator.py

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from sklearn.model_selection import TimeSeriesSplit
from .backtester import AdvancedBacktester
from datetime import datetime, timedelta

class TimeSeriesValidator:
    def __init__(self, n_splits: int = 5, test_size: int = 60):
        self.n_splits = n_splits
        self.test_size = test_size
        self.backtester = AdvancedBacktester()
        
    def validate(self, model, data: pd.DataFrame) -> Dict:
        """Perform time series cross-validation."""
        tscv = TimeSeriesSplit(n_splits=self.n_splits)
        results = []
        
        for train_idx, test_idx in tscv.split(data):
            train_data = data.iloc[train_idx]
            test_data = data.iloc[test_idx]
            
            # Train model on this fold
            model.fit(train_data)
            
            # Backtest on test data
            fold_results = self.backtester.run_backtest(model, train_data, test_data)
            results.append(fold_results)
        
        return self._aggregate_results(results)
    
    def _aggregate_results(self, results: List[Dict]) -> Dict:
        """Aggregate results across all folds."""
        metrics = {
            'sharpe_ratio': [],
            'sortino_ratio': [],
            'max_drawdown': [],
            'total_return': [],
            'win_rate': [],
            'profit_factor': []
        }
        
        for result in results:
            metrics['sharpe_ratio'].append(result.sharpe_ratio)
            metrics['sortino_ratio'].append(result.sortino_ratio)
            metrics['max_drawdown'].append(result.max_drawdown)
            metrics['total_return'].append(result.total_return)
            metrics['win_rate'].append(result.win_rate)
            metrics['profit_factor'].append(result.profit_factor)
        
        return {
            'mean_sharpe': np.mean(metrics['sharpe_ratio']),
            'std_sharpe': np.std(metrics['sharpe_ratio']),
            'mean_sortino': np.mean(metrics['sortino_ratio']),
            'std_sortino': np.std(metrics['sortino_ratio']),
            'mean_drawdown': np.mean(metrics['max_drawdown']),
            'std_drawdown': np.std(metrics['max_drawdown']),
            'mean_return': np.mean(metrics['total_return']),
            'std_return': np.std(metrics['total_return']),
            'mean_win_rate': np.mean(metrics['win_rate']),
            'mean_profit_factor': np.mean(metrics['profit_factor'])
        }