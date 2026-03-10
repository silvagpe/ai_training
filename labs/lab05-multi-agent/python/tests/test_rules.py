"""Tests for portfolio rules and validation."""
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from domain.portfolio_rules import PortfolioRules
from domain.diversification import DiversificationRules
from schemas.fii import FII


def test_fii_eligibility():
    """Test FII eligibility rules."""
    print("\n=== Testing FII Eligibility Rules ===")

    # Eligible FII
    eligible_fii = FII(
        ticker="TEST11",
        name="Test Fund",
        fund_type="tijolo",
        segment="test",
        inception_date=datetime.now().date() - timedelta(days=365 * 6),
        avg_daily_volume_brl=5_000_000,
        net_equity_brl=2_000_000_000,
        is_top_50=True,
        dy_12m_pct=10.0,
        price_to_book=1.0,
    )

    result = PortfolioRules.check_fii_eligibility(eligible_fii)
    print(f"✓ Eligible FII: {result.eligible}")
    assert result.eligible, "Should be eligible"

    # Ineligible FII (too young)
    young_fii = FII(
        ticker="YOUNG11",
        name="Young Fund",
        fund_type="papel",
        segment="test",
        inception_date=datetime.now().date() - timedelta(days=365 * 2),
        avg_daily_volume_brl=5_000_000,
        net_equity_brl=2_000_000_000,
        is_top_50=True,
        dy_12m_pct=10.0,
        price_to_book=1.0,
    )

    result = PortfolioRules.check_fii_eligibility(young_fii)
    print(f"✓ Young FII ineligible: {not result.eligible}")
    assert not result.eligible, "Should not be eligible (too young)"

    print("✓ All eligibility tests passed!\n")


def test_diversification():
    """Test diversification rules."""
    print("\n=== Testing Diversification Rules ===")

    # Test portfolio count suggestion
    counts = DiversificationRules.suggest_fii_count(50_000)  # Small
    print(f"✓ Small patrimony (50k): {counts} FIIs")
    assert counts[0] == 3, "Should suggest 3 FIIs for small portfolio"

    counts = DiversificationRules.suggest_fii_count(200_000)  # Medium
    print(f"✓ Medium patrimony (200k): {counts} FIIs")
    assert counts[0] == 5, "Should suggest 5 FIIs for medium portfolio"

    counts = DiversificationRules.suggest_fii_count(500_000)  # Large
    print(f"✓ Large patrimony (500k): {counts} FIIs")
    assert counts[0] >= 5, "Should suggest 5-10 FIIs for large portfolio"

    print("✓ All diversification tests passed!\n")


def test_herfindahl():
    """Test concentration index."""
    print("\n=== Testing Herfindahl Index ===")

    # Create test FIIs
    fiis = []
    for i in range(5):
        fiis.append(
            FII(
                ticker=f"TST{i}11",
                name=f"Test {i}",
                fund_type="tijolo",
                segment="test",
                inception_date=datetime.now().date() - timedelta(days=365 * 10),
                avg_daily_volume_brl=2_000_000,
                net_equity_brl=1_500_000_000,
                is_top_50=True,
                dy_12m_pct=10.0,
                price_to_book=1.0,
            )
        )

    index = DiversificationRules.calculate_herfindahl_index(fiis)
    print(f"✓ 5 equal assets Herfindahl index: {index:.0f}")
    assert index < 2500, "Should be low concentration"

    # Concentrated portfolio (1 asset)
    index_concentrated = DiversificationRules.calculate_herfindahl_index(fiis[:1])
    print(f"✓ 1 asset Herfindahl index: {index_concentrated:.0f}")
    assert index_concentrated > 9000, "Should be high concentration"

    print("✓ All Herfindahl tests passed!\n")


if __name__ == "__main__":
    test_fii_eligibility()
    test_diversification()
    test_herfindahl()
    print("=" * 50)
    print("✓ All tests passed!")
    print("=" * 50)
