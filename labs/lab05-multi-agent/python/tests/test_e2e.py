#!/usr/bin/env python
"""End-to-end test of FII portfolio analyzer."""
import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent))

from schemas import PortfolioInput, PortfolioAsset
from services.portfolio_service import PortfolioService


def main():
    """Run end-to-end test."""
    print("\n" + "="*60)
    print("FII PORTFOLIO ANALYZER — End-to-End Test")
    print("="*60)

    # Create sample portfolio
    print("\n1. Creating sample portfolio...")
    portfolio = PortfolioInput(
        client_id="test_client_001",
        current_assets=[
            PortfolioAsset(ticker="KNCR11", quantity=10, current_price=9.66),
        ],
        total_patrimony_brl=100_000,
        monthly_contribution_brl=1_000,
        investment_horizon_months=60,
    )
    print(f"   ✓ Portfolio with R${portfolio.total_patrimony_brl:,.0f} created")

    # Run analysis
    print("\n2. Running portfolio analysis...")
    service = PortfolioService()
    analysis = service.evaluate_portfolio(portfolio)
    print(f"   ✓ Analysis complete")

    # Display results
    print("\n3. Analysis Results:")
    print(f"\n   📊 HOLD ({len(analysis.portfolio_analysis.hold_assets)}):")
    for asset in analysis.portfolio_analysis.hold_assets:
        print(f"      - {asset.ticker}: {asset.reason}")

    print(f"\n   ✅ BUY ({len(analysis.portfolio_analysis.buy_assets)}):")
    for asset in analysis.portfolio_analysis.buy_assets:
        print(f"      - {asset.ticker}: Allocation {asset.weight_recommended_pct:.1f}%")

    print(f"\n   ❌ SELL ({len(analysis.portfolio_analysis.sell_assets)}):")
    for asset in analysis.portfolio_analysis.sell_assets:
        print(f"      - {asset.ticker}")

    # Diversification
    print(f"\n   🎯 Diversification:")
    for k, v in analysis.diversification_summary.items():
        print(f"      - {k}: {v}")

    # Recommended allocation
    print(f"\n   📈 Recommended Allocation:")
    for ticker, weight in analysis.recommended_allocation.items():
        print(f"      - {ticker}: {weight:.1f}%")

    # Analytics
    if analysis.analytics:
        print(f"\n   📊 Analytics:")
        if analysis.analytics.sharpe_ratio:
            print(f"      - Sharpe Ratio: {analysis.analytics.sharpe_ratio:.2f}")
        if analysis.analytics.portfolio_volatility_pct:
            print(f"      - Volatility: {analysis.analytics.portfolio_volatility_pct:.2f}%")

    print("\n" + "="*60)
    print("✓ End-to-end test completed successfully!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
