# backend/core/portfolio_optimizer.py

from scipy.optimize import minimize
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class PortfolioAllocation:
    symbols: List[str]
    weights: np.ndarray
    expected_return: float
    volatility: float
    sharpe_ratio: float
    max_drawdown: float

class PortfolioOptimizer:
    def __init__(self, risk_free_rate: float = 0.02):
        self.risk_free_rate = risk_free_rate
        
    def optimize(self, returns_data: pd.DataFrame, 
                constraints: Dict = None) -> PortfolioAllocation:
        """
        Optimize portfolio using Black-Litterman model with market views.
        """
        n_assets = len(returns_data.columns)
        
        # Calculate mean returns and covariance
        mean_returns = returns_data.mean() * 252  # Annualize returns
        cov_matrix = returns_data.cov() * 252  # Annualize covariance
        
        # Initial weights
        init_weights = np.array([1/n_assets] * n_assets)
        
        # Constraints
        bounds = [(0, 1) for _ in range(n_assets)]  # No short selling
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}  # Weights sum to 1
        ]
        
        # Add custom constraints if provided
        if constraints:
            if 'min_weight' in constraints:
                bounds = [(constraints['min_weight'], 1) for _ in range(n_assets)]
            if 'max_weight' in constraints:
                bounds = [(b[0], min(b[1], constraints['max_weight'])) 
                         for b in bounds]
        
        # Optimize for Sharpe Ratio
        result = minimize(
            self._negative_sharpe_ratio,
            init_weights,
            args=(mean_returns, cov_matrix),
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        optimal_weights = result.x
        portfolio_return = np.sum(mean_returns * optimal_weights)
        portfolio_std = np.sqrt(np.dot(optimal_weights.T, 
                                     np.dot(cov_matrix, optimal_weights)))
        sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_std
        
        # Calculate max drawdown
        portfolio_returns = np.sum(returns_data * optimal_weights, axis=1)
        cumulative_returns = (1 + portfolio_returns).cumprod()
        rolling_max = cumulative_returns.expanding(min_periods=1).max()
        drawdowns = (rolling_max - cumulative_returns) / rolling_max
        max_drawdown = drawdowns.max()
        
        return PortfolioAllocation(
            symbols=list(returns_data.columns),
            weights=optimal_weights,
            expected_return=portfolio_return,
            volatility=portfolio_std,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown
        )
    
    def _negative_sharpe_ratio(self, weights: np.ndarray, 
                             mean_returns: np.ndarray, 
                             cov_matrix: np.ndarray) -> float:
        """Calculate negative Sharpe ratio for minimization."""
        portfolio_return = np.sum(mean_returns * weights)
        portfolio_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        return -(portfolio_return - self.risk_free_rate) / portfolio_std
    
    def generate_efficient_frontier(self, returns_data: pd.DataFrame, 
                                 n_points: int = 100) -> List[Dict]:
        """Generate efficient frontier points."""
        min_ret = min(returns_data.mean() * 252)
        max_ret = max(returns_data.mean() * 252)
        target_returns = np.linspace(min_ret, max_ret, n_points)
        
        efficient_portfolios = []
        
        for target_return in target_returns:
            portfolio = self._optimize_for_return(returns_data, target_return)
            efficient_portfolios.append({
                'return': portfolio.expected_return,
                'volatility': portfolio.volatility,
                'sharpe_ratio': portfolio.sharpe_ratio,
                'weights': portfolio.weights.tolist(),
                'max_drawdown': portfolio.max_drawdown
            })
        
        return efficient_portfolios
    
    def _optimize_for_return(self, returns_data: pd.DataFrame, 
                           target_return: float) -> PortfolioAllocation:
        """Optimize portfolio for a specific target return."""
        n_assets = len(returns_data.columns)
        mean_returns = returns_data.mean() * 252
        cov_matrix = returns_data.cov() * 252
        
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
            {'type': 'eq', 'fun': lambda x: np.sum(mean_returns * x) - target_return}
        ]
        
        bounds = [(0, 1) for _ in range(n_assets)]
        init_weights = np.array([1/n_assets] * n_assets)
        
        result = minimize(
            lambda w: np.sqrt(np.dot(w.T, np.dot(cov_matrix, w))),
            init_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        optimal_weights = result.x
        portfolio_std = np.sqrt(np.dot(optimal_weights.T, 
                                     np.dot(cov_matrix, optimal_weights)))
        sharpe_ratio = (target_return - self.risk_free_rate) / portfolio_std
        
        # Calculate max drawdown
        portfolio_returns = np.sum(returns_data * optimal_weights, axis=1)
        cumulative_returns = (1 + portfolio_returns).cumprod()
        rolling_max = cumulative_returns.expanding(min_periods=1).max()
        drawdowns = (rolling_max - cumulative_returns) / rolling_max
        max_drawdown = drawdowns.max()
        
        return PortfolioAllocation(
            symbols=list(returns_data.columns),
            weights=optimal_weights,
            expected_return=target_return,
            volatility=portfolio_std,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown
        )