"""Portfolio eligibility and validation rules."""
from datetime import datetime, timedelta
from typing import List, Dict
from schemas import FII, AssetEligibility
from config.settings import (
    MIN_YEARS_EXISTENCE,
    MIN_DAILY_VOLUME_BRL,
    MIN_NET_EQUITY_BRL,
    MAX_TOP_50_RANK,
)


class PortfolioRules:
    """Business rules for portfolio eligibility."""

    @staticmethod
    def check_fii_eligibility(fii: FII) -> AssetEligibility:
        """Check if FII meets all eligibility criteria."""
        rules_passed = []
        rules_failed = []
        fail_reasons = {}

        # Rule 1: Age check (> 5 years)
        years_old = (datetime.now().date() - fii.inception_date).days / 365.25
        if years_old > MIN_YEARS_EXISTENCE:
            rules_passed.append("age_ok")
        else:
            rules_failed.append("insufficient_age")
            fail_reasons["age"] = f"Only {years_old:.1f} years old (need {MIN_YEARS_EXISTENCE}+)"

        # Rule 2: Daily volume check (> 1M BRL)
        if fii.avg_daily_volume_brl >= MIN_DAILY_VOLUME_BRL:
            rules_passed.append("volume_ok")
        else:
            rules_failed.append("low_volume")
            fail_reasons["volume"] = (
                f"Daily volume R${fii.avg_daily_volume_brl:,.0f} < R${MIN_DAILY_VOLUME_BRL:,.0f}"
            )

        # Rule 3: Top 50 check
        if fii.is_top_50:
            rules_passed.append("top50_ok")
        else:
            rules_failed.append("not_in_top_50")
            fail_reasons["top50"] = "Not in top 50 FIIs by market cap"

        # Rule 4: Patrimony check (> 1B BRL)
        if fii.net_equity_brl >= MIN_NET_EQUITY_BRL:
            rules_passed.append("equity_ok")
        else:
            rules_failed.append("low_equity")
            fail_reasons["equity"] = f"Net equity R${fii.net_equity_brl/1e9:.2f}B < R$1B"

        eligible = len(rules_failed) == 0

        return AssetEligibility(
            ticker=fii.ticker,
            eligible=eligible,
            rules_passed=rules_passed,
            rules_failed=rules_failed,
            fail_reasons=fail_reasons,
        )

    @staticmethod
    def check_portfolio_elegibility(fiis: List[FII]) -> Dict[str, AssetEligibility]:
        """Check eligibility for multiple FIIs."""
        return {fii.ticker: PortfolioRules.check_fii_eligibility(fii) for fii in fiis}

    @staticmethod
    def get_eligible_fiis(fiis: List[FII]) -> List[FII]:
        """Get list of eligible FIIs."""
        return [fii for fii in fiis if PortfolioRules.check_fii_eligibility(fii).eligible]

    @staticmethod
    def validate_minimum_days_trading(fii: FII, min_days: int = 365) -> bool:
        """Check if FII has at least minimum days of trading."""
        days_old = (datetime.now().date() - fii.inception_date).days
        return days_old >= min_days
