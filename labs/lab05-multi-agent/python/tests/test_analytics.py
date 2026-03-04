"""Tests for analytics calculations."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from analytics.projection import PortfolioProjection
from analytics.sharpe_treynor import RiskMetrics


def test_projection():
    """Test portfolio projection."""
    print("\n=== Testing Portfolio Projection ===")

    result = PortfolioProjection.project_portfolio(
        initial_value_brl=100_000,
        monthly_contribution_brl=1_000,
        monthly_return_pct=1.0,  # 1% per month
        months=60,
    )

    print(f"✓ Initial: R${result['initial_value']:,.0f}")
    print(f"✓ Total contributions: R${result['total_contributions']:,.0f}")
    print(f"✓ Final value: R${result['final_value']:,.0f}")
    print(f"✓ Return: {result['return_pct']:.1f}%")

    assert result["final_value"] > result["total_contributions"], "Final should exceed contributions"
    print("✓ Projection test passed!\n")


def test_sharpe():
    """Test Sharpe ratio calculation."""
    print("\n=== Testing Sharpe Ratio ===")

    # Mock monthly returns (volatile, but positive on average)
    returns = [0.5, -0.5, 1.0, 0.2, 0.8, -0.3, 0.9, 1.1, 0.6, 0.4, 0.7, 0.5]

    sharpe = RiskMetrics.calculate_sharpe_ratio(returns)
    print(f"✓ Sharpe ratio: {sharpe:.2f}")

    volatility = RiskMetrics.calculate_volatility(returns)
    print(f"✓ Volatility: {volatility:.2f}%")

    assert volatility > 0, "Volatility should be positive"
    print("✓ Sharpe test passed!\n")


def test_beta():
    """Test beta calculation."""
    print("\n=== Testing Beta Calculation ===")

    portfolio = [0.8, 1.2, 0.5, 1.0, 0.9]
    benchmark = [0.6, 1.0, 0.4, 0.8, 0.7]

    beta = RiskMetrics.calculate_beta(portfolio, benchmark)
    print(f"✓ Beta: {beta:.2f}")

    assert beta > 0, "Beta should be positive"
    print("✓ Beta test passed!\n")


if __name__ == "__main__":
    test_projection()
    test_sharpe()
    test_beta()
    print("=" * 50)
    print("✓ All analytics tests passed!")
    print("=" * 50)
