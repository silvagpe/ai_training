#!/usr/bin/env python
"""End-to-end test of FII portfolio analyzer."""
import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

from schemas import PortfolioInput, PortfolioAsset
from services.portfolio_service import PortfolioService


def print_scenario_header(num, title):
    """Print scenario header."""
    print(f"\n{'='*60}")
    print(f"SCENARIO {num}: {title}")
    print(f"{'='*60}")


def print_analysis_results(analysis, portfolio):
    """Print formatted analysis results."""
    print(f"\n   📊 HOLD ({len(analysis.portfolio_analysis.hold_assets)}):")
    if analysis.portfolio_analysis.hold_assets:
        for asset in analysis.portfolio_analysis.hold_assets:
            print(f"      - {asset.ticker}: {asset.reason}")
    else:
        print(f"      (none)")

    print(f"\n   ✅ BUY ({len(analysis.portfolio_analysis.buy_assets)}):")
    if analysis.portfolio_analysis.buy_assets:
        for asset in analysis.portfolio_analysis.buy_assets:
            print(f"      - {asset.ticker}: Allocation {asset.weight_recommended_pct:.1f}%")
    else:
        print(f"      (none)")

    print(f"\n   ❌ SELL ({len(analysis.portfolio_analysis.sell_assets)}):")
    if analysis.portfolio_analysis.sell_assets:
        for asset in analysis.portfolio_analysis.sell_assets:
            print(f"      - {asset.ticker}")
    else:
        print(f"      (none)")

    # Summary
    final_count = len(analysis.portfolio_analysis.hold_assets) + len(analysis.portfolio_analysis.buy_assets)
    print(f"\n   📈 Final Portfolio: {final_count} FIIs (expected by tier: 3)")

    print(f"\n   🎯 Recommended Allocation:")
    for ticker, weight in analysis.recommended_allocation.items():
        print(f"      - {ticker}: {weight:.1f}%")

    # Diversification
    print(f"\n   💾 Diversification metrics:")
    print(f"      - Herfindahl Index: {analysis.diversification_summary['herfindahl_index']:.0f}")
    print(f"      - Concentration: {analysis.diversification_summary['concentration_level']}")


def main():
    """Run end-to-end tests with multiple scenarios."""
    print("\n" + "="*60)
    print("FII PORTFOLIO ANALYZER — Multi-Scenario End-to-End Test")
    print("="*60)

    service = PortfolioService()

    # ============================================================
    # SCENARIO 1: Portfolio needs rebalance (1 bad asset)
    # ============================================================
    print_scenario_header(1, "Rebalance needed - 1 bad asset, buy 3")
    
    portfolio1 = PortfolioInput(
        client_id="test_client_001",
        current_assets=[
            PortfolioAsset(ticker="KNCR11", quantity=10, current_price=9.66),
        ],
        total_patrimony_brl=100_000,
        monthly_contribution_brl=1_000,
        investment_horizon_months=60,
    )
    print(f"   Input: {len(portfolio1.current_assets)} holding(s), {portfolio1.total_patrimony_brl:,.0f} patrimony")
    
    analysis1 = service.evaluate_portfolio(portfolio1)
    print_analysis_results(analysis1, portfolio1)
    
    expected1 = {
        'hold': 0,
        'sell': 1,
        'buy': 3,
        'final': 3
    }
    actual1 = {
        'hold': len(analysis1.portfolio_analysis.hold_assets),
        'sell': len(analysis1.portfolio_analysis.sell_assets),
        'buy': len(analysis1.portfolio_analysis.buy_assets),
        'final': len(analysis1.portfolio_analysis.hold_assets) + len(analysis1.portfolio_analysis.buy_assets)
    }
    print(f"\n   ✓ Expected: {expected1} / Actual: {actual1}")


    # ============================================================
    # SCENARIO 2: Portfolio already correct (3 recommended holdings)
    # ============================================================
    print_scenario_header(2, "Already correct - 3 recommended FIIs, no action needed")
    
    portfolio2 = PortfolioInput(
        client_id="test_client_002",
        current_assets=[
            PortfolioAsset(ticker="XPML11", quantity=15, current_price=95.50),
            PortfolioAsset(ticker="HGLG11", quantity=20, current_price=134.30),
            PortfolioAsset(ticker="MXRF11", quantity=8, current_price=11.80),
        ],
        total_patrimony_brl=100_000,
        monthly_contribution_brl=1_000,
        investment_horizon_months=60,
    )
    print(f"   Input: {len(portfolio2.current_assets)} holding(s), {portfolio2.total_patrimony_brl:,.0f} patrimony")
    
    analysis2 = service.evaluate_portfolio(portfolio2)
    print_analysis_results(analysis2, portfolio2)
    
    expected2 = {
        'hold': 3,
        'sell': 0,
        'buy': 0,
        'final': 3
    }
    actual2 = {
        'hold': len(analysis2.portfolio_analysis.hold_assets),
        'sell': len(analysis2.portfolio_analysis.sell_assets),
        'buy': len(analysis2.portfolio_analysis.buy_assets),
        'final': len(analysis2.portfolio_analysis.hold_assets) + len(analysis2.portfolio_analysis.buy_assets)
    }
    print(f"\n   ✓ Expected: {expected2} / Actual: {actual2}")


    # ============================================================
    # SCENARIO 3: Partial holdings - 1 good, 1 bad, buy 2
    # ============================================================
    print_scenario_header(3, "Partial match - 1 hold + 1 sell, buy 2 more")
    
    portfolio3 = PortfolioInput(
        client_id="test_client_003",
        current_assets=[
            PortfolioAsset(ticker="XPML11", quantity=20, current_price=95.50),  # Good (hold)
            PortfolioAsset(ticker="BCFF11", quantity=10, current_price=8.50),   # Bad (sell)
        ],
        total_patrimony_brl=100_000,
        monthly_contribution_brl=1_000,
        investment_horizon_months=60,
    )
    print(f"   Input: {len(portfolio3.current_assets)} holding(s), {portfolio3.total_patrimony_brl:,.0f} patrimony")
    
    analysis3 = service.evaluate_portfolio(portfolio3)
    print_analysis_results(analysis3, portfolio3)
    
    expected3 = {
        'hold': 1,
        'sell': 1,
        'buy': 2,
        'final': 3
    }
    actual3 = {
        'hold': len(analysis3.portfolio_analysis.hold_assets),
        'sell': len(analysis3.portfolio_analysis.sell_assets),
        'buy': len(analysis3.portfolio_analysis.buy_assets),
        'final': len(analysis3.portfolio_analysis.hold_assets) + len(analysis3.portfolio_analysis.buy_assets)
    }
    print(f"\n   ✓ Expected: {expected3} / Actual: {actual3}")


    # ============================================================
    # SUMMARY
    # ============================================================
    print("\n" + "="*60)
    print("✓ All end-to-end scenarios completed successfully!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
