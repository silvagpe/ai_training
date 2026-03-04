"""Portfolio recommendation logic."""
from typing import List, Dict
from schemas import (
    FII,
    PortfolioAsset,
    AssetAnalysis,
    PortfolioRecommendation,
    RecommendationAction,
)
from data.providers.fii_snapshot_provider import (
    FIISnapshotProvider,
    RecommendedPortfolioProvider,
)


class RecommendationEngine:
    """Generate actionable recommendations."""

    def __init__(self):
        self.fii_provider = FIISnapshotProvider()
        self.portfolio_provider = RecommendedPortfolioProvider()

    def compare_portfolios(
        self, client_portfolio: List[PortfolioAsset]
    ) -> PortfolioRecommendation:
        """Compare client's portfolio with recommendations.
        
        Returns actions: HOLD, BUY, SELL.
        """
        # Load snapshots
        fii_snapshot = self.fii_provider.load()
        recommended = self.portfolio_provider.load()

        # Create FII lookup
        fii_lookup = {fii.ticker: fii for fii in fii_snapshot.fiis}

        # Get recommended tickers
        recommended_tickers = {rec.ticker for rec in recommended.recommendations}

        hold_assets = []
        buy_assets = []
        sell_assets = []

        # Analyze client's current holdings
        for asset in client_portfolio:
            if asset.ticker not in fii_lookup:
                # Unknown FII - suggest selling
                sell_assets.append(
                    AssetAnalysis(
                        ticker=asset.ticker,
                        name=f"Unknown ({asset.ticker})",
                        fund_type="unknown",
                        segment="unknown",
                        action=RecommendationAction.SELL,
                        current_price=asset.current_price,
                        dy_pct=0,
                        price_to_book=0,
                        reason="FII not found in snapshot. Consider selling to diversify.",
                        source="client_portfolio",
                    )
                )
                continue

            fii = fii_lookup[asset.ticker]

            if asset.ticker in recommended_tickers:
                # In recommendations - hold
                hold_assets.append(
                    AssetAnalysis(
                        ticker=fii.ticker,
                        name=fii.name,
                        fund_type=fii.fund_type,
                        segment=fii.segment,
                        action=RecommendationAction.HOLD,
                        current_price=asset.current_price,
                        dy_pct=fii.dy_12m_pct,
                        price_to_book=fii.price_to_book,
                        reason=f"Validated fund. {fii.fund_type.capitalize()} of good quality with DY {fii.dy_12m_pct:.2f}%.",
                        source="client_portfolio",
                    )
                )
            else:
                # Not in recommendations - suggest selling
                sell_assets.append(
                    AssetAnalysis(
                        ticker=fii.ticker,
                        name=fii.name,
                        fund_type=fii.fund_type,
                        segment=fii.segment,
                        action=RecommendationAction.SELL,
                        current_price=asset.current_price,
                        dy_pct=fii.dy_12m_pct,
                        price_to_book=fii.price_to_book,
                        reason="Not in recommended portfolio. Consider swapping for more attractive alternative.",
                        source="client_portfolio",
                    )
                )

        # Identify buy opportunities (recommended but not in client's portfolio)
        client_tickers = {asset.ticker for asset in client_portfolio}

        for rec in recommended.recommendations:
            if rec.ticker not in client_tickers:
                fii = fii_lookup[rec.ticker]
                buy_assets.append(
                    AssetAnalysis(
                        ticker=fii.ticker,
                        name=fii.name,
                        fund_type=fii.fund_type,
                        segment=fii.segment,
                        action=RecommendationAction.BUY,
                        current_price=fii.price_to_book,  # Approximation
                        dy_pct=fii.dy_12m_pct,
                        price_to_book=fii.price_to_book,
                        reason=rec.rationale or "Recommended by portfolio strategy.",
                        source="recommended",
                        weight_recommended_pct=rec.recommended_weight_pct,
                    )
                )

        return PortfolioRecommendation(
            hold_assets=hold_assets,
            buy_assets=buy_assets,
            sell_assets=sell_assets,
        )

    @staticmethod
    def build_recommended_allocation(recommended_fiis: List[FII]) -> Dict[str, float]:
        """Build allocation map {ticker: weight_pct}."""
        if not recommended_fiis:
            return {}

        total = len(recommended_fiis)
        return {fii.ticker: (1.0 / total * 100) for fii in recommended_fiis}
