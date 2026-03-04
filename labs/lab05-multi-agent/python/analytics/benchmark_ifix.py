"""Portfolio vs benchmark comparison."""
import statistics
from typing import Dict, List, Optional
from ..data.providers.fii_snapshot_provider import IFIXProvider


class BenchmarkComparison:
    """Compare portfolio performance vs IFIX benchmark."""

    @staticmethod
    def compare_returns(
        portfolio_returns_pct: List[float],
        benchmark_returns_pct: Optional[List[float]] = None,
    ) -> Dict:
        """Compare portfolio returns vs benchmark (IFIX).
        
        Returns:
            {
                'portfolio_total_return': cumulative %,
                'benchmark_total_return': cumulative %,
                'outperformance': portfolio - benchmark,
                'portfolio_avg_monthly': average monthly %,
                'benchmark_avg_monthly': average monthly %,
            }
        """
        if benchmark_returns_pct is None:
            # Load IFIX data
            ifix_provider = IFIXProvider()
            benchmark_returns_pct = ifix_provider.get_returns()

        # Match lengths (use shorter of two)
        min_len = min(len(portfolio_returns_pct), len(benchmark_returns_pct))
        portfolio = portfolio_returns_pct[:min_len]
        benchmark = benchmark_returns_pct[:min_len]

        # Calculate cumulative returns (compound)
        portfolio_cumulative = BenchmarkComparison._calculate_cumulative_return(portfolio)
        benchmark_cumulative = BenchmarkComparison._calculate_cumulative_return(benchmark)

        return {
            "portfolio_total_return_pct": portfolio_cumulative,
            "benchmark_total_return_pct": benchmark_cumulative,
            "outperformance_pct": portfolio_cumulative - benchmark_cumulative,
            "portfolio_avg_monthly_pct": statistics.mean(portfolio),
            "benchmark_avg_monthly_pct": statistics.mean(benchmark),
            "periods_analyzed": min_len,
        }

    @staticmethod
    def _calculate_cumulative_return(returns_pct: List[float]) -> float:
        """Calculate cumulative return from monthly returns.
        
        Formula: ((1 + r1) * (1 + r2) * ... - 1) * 100
        """
        if not returns_pct:
            return 0

        cumulative = 1.0
        for ret in returns_pct:
            cumulative *= 1 + (ret / 100.0)

        return (cumulative - 1) * 100

    @staticmethod
    def draw_down_analysis(returns_pct: List[float]) -> Dict:
        """Calculate maximum drawdown.
        
        Returns:
            {
                'max_drawdown_pct': worst peak-to-trough decline,
                'current_drawdown_pct': current level vs recent peak
            }
        """
        if not returns_pct or len(returns_pct) < 2:
            return {"max_drawdown_pct": 0, "current_drawdown_pct": 0}

        # Convert returns to cumulative value (starting from 100)
        values = [100.0]
        for ret in returns_pct:
            values.append(values[-1] * (1 + ret / 100.0))

        # Find maximum drawdown
        max_value_so_far = values[0]
        max_drawdown = 0

        for value in values[1:]:
            if value > max_value_so_far:
                max_value_so_far = value
            drawdown = (max_value_so_far - value) / max_value_so_far
            max_drawdown = max(max_drawdown, drawdown)

        # Current drawdown
        current_value = values[-1]
        peak_value = max(values)
        current_drawdown = (peak_value - current_value) / peak_value if peak_value > 0 else 0

        return {
            "max_drawdown_pct": max_drawdown * 100,
            "current_drawdown_pct": current_drawdown * 100,
            "periods_analyzed": len(returns_pct),
        }

    @staticmethod
    def get_ifix_benchmark() -> Dict:
        """Get IFIX 5-year benchmark data."""
        ifix_provider = IFIXProvider()
        data = ifix_provider.load()
        return {
            "index": data["index"],
            "start_date": data["start_date"],
            "end_date": data["end_date"],
            "periods": len(data["series"]),
            "returns": ifix_provider.get_returns(),
        }
