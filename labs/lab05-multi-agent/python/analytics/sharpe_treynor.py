"""Sharpe and Treynor ratio calculations."""
import math
import statistics
from typing import List, Optional
from ..config.settings import SHARPE_RISK_FREE_RATE


class RiskMetrics:
    """Calculate risk-adjusted return metrics."""

    @staticmethod
    def calculate_volatility(returns_pct: List[float]) -> float:
        """Calculate standard deviation of returns (volatility).
        
        Args:
            returns_pct: List of returns as percentages
            
        Returns:
            Volatility as percentage (annualized if monthly data)
        """
        if len(returns_pct) < 2:
            return 0

        # Calculate standard deviation
        std_dev = statistics.stdev(returns_pct)

        # Annualize if monthly data (12 months)
        return std_dev * math.sqrt(12)

    @staticmethod
    def calculate_sharpe_ratio(
        returns_pct: List[float],
        risk_free_rate_annual_pct: Optional[float] = None,
    ) -> float:
        """Calculate Sharpe ratio.
        
        Sharpe = (Portfolio Return - Risk-Free Rate) / Volatility
        
        Args:
            returns_pct: List of monthly returns (%)
            risk_free_rate_annual_pct: Annual risk-free rate (%), defaults to SHARPE_RISK_FREE_RATE
            
        Returns:
            Sharpe ratio (higher is better)
        """
        if risk_free_rate_annual_pct is None:
            risk_free_rate_annual_pct = SHARPE_RISK_FREE_RATE

        if len(returns_pct) < 2:
            return 0

        # Average return (annualized)
        avg_return = statistics.mean(returns_pct) * 12

        # Volatility (annualized)
        volatility = RiskMetrics.calculate_volatility(returns_pct)

        if volatility == 0:
            return 0

        return (avg_return - risk_free_rate_annual_pct) / volatility

    @staticmethod
    def calculate_treynor_ratio(
        portfolio_returns_pct: List[float],
        benchmark_returns_pct: List[float],
        risk_free_rate_annual_pct: Optional[float] = None,
    ) -> float:
        """Calculate Treynor ratio.
        
        Treynor = (Portfolio Return - Risk-Free Rate) / Beta
        
        Where Beta = Covariance(portfolio, benchmark) / Variance(benchmark)
        
        Args:
            portfolio_returns_pct: List of portfolio monthly returns (%)
            benchmark_returns_pct: List of benchmark monthly returns (%)
            risk_free_rate_annual_pct: Annual risk-free rate (%)
            
        Returns:
            Treynor ratio (higher is better)
        """
        if risk_free_rate_annual_pct is None:
            risk_free_rate_annual_pct = SHARPE_RISK_FREE_RATE

        if len(portfolio_returns_pct) < 2 or len(benchmark_returns_pct) < 2:
            return 0

        # Calculate Beta
        beta = RiskMetrics.calculate_beta(portfolio_returns_pct, benchmark_returns_pct)

        if beta == 0:
            return 0

        # Average return (annualized)
        avg_return = statistics.mean(portfolio_returns_pct) * 12

        return (avg_return - risk_free_rate_annual_pct) / beta

    @staticmethod
    def calculate_beta(
        portfolio_returns_pct: List[float], benchmark_returns_pct: List[float]
    ) -> float:
        """Calculate portfolio beta (systematic risk).
        
        Beta = Covariance(portfolio, benchmark) / Variance(benchmark)
        
        Args:
            portfolio_returns_pct: List of portfolio monthly returns (%)
            benchmark_returns_pct: List of benchmark monthly returns (%)
            
        Returns:
            Beta (1.0 = same volatility as benchmark)
        """
        if len(portfolio_returns_pct) != len(benchmark_returns_pct) or len(portfolio_returns_pct) < 2:
            return 1.0

        n = len(benchmark_returns_pct)
        portfolio_mean = statistics.mean(portfolio_returns_pct)
        benchmark_mean = statistics.mean(benchmark_returns_pct)

        # Covariance
        covariance = sum(
            (portfolio_returns_pct[i] - portfolio_mean)
            * (benchmark_returns_pct[i] - benchmark_mean)
            for i in range(n)
        ) / (n - 1)

        # Benchmark variance
        benchmark_variance = sum(
            (benchmark_returns_pct[i] - benchmark_mean) ** 2 for i in range(n)
        ) / (n - 1)

        if benchmark_variance == 0:
            return 1.0

        return covariance / benchmark_variance

    @staticmethod
    def calculate_correlation(series1: List[float], series2: List[float]) -> float:
        """Calculate Pearson correlation between two series."""
        if len(series1) != len(series2) or len(series1) < 2:
            return 0

        mean1 = statistics.mean(series1)
        mean2 = statistics.mean(series2)

        numerator = sum(
            (series1[i] - mean1) * (series2[i] - mean2) for i in range(len(series1))
        )
        std1 = statistics.stdev(series1)
        std2 = statistics.stdev(series2)

        if std1 == 0 or std2 == 0:
            return 0

        return numerator / (std1 * std2 * len(series1))
