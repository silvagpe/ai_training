"""Portfolio evaluation service."""
from typing import List, Dict
from ..schemas import (
    PortfolioInput,
    PortfolioAsset,
    AssetEligibility,
    AnalysisOutput,
    AnalyticsMetrics,
)
from ..domain.portfolio_rules import PortfolioRules
from ..domain.diversification import DiversificationRules
from ..domain.recommendation import RecommendationEngine
from ..data.providers.fii_snapshot_provider import FIISnapshotProvider
from ..analytics.projection import PortfolioProjection
from ..analytics.sharpe_treynor import RiskMetrics
from ..analytics.benchmark_ifix import BenchmarkComparison
from ..config.settings import SHARPE_RISK_FREE_RATE


class PortfolioService:
    """Main service for portfolio evaluation."""

    def __init__(self):
        self.fii_provider = FIISnapshotProvider()
        self.recommendation_engine = RecommendationEngine()

    def evaluate_portfolio(self, portfolio: PortfolioInput) -> AnalysisOutput:
        """Complete portfolio evaluation workflow.
        
        Returns: Structured analysis with recommendations and analytics.
        """
        # Load available FIIs
        fii_snapshot = self.fii_provider.load()

        # 1. Check eligibility of all available FIIs
        eligible_fiis = PortfolioRules.get_eligible_fiis(fii_snapshot.fiis)

        # 2. Suggest portfolio based on patrimonio
        min_count, max_count = DiversificationRules.suggest_fii_count(
            portfolio.total_patrimony_brl
        )
        suggested_fiis = DiversificationRules.suggest_balanced_portfolio(
            eligible_fiis, target_count=min_count
        )

        # 3. Compare client's portfolio with recommendations
        portfolio_recommendation = self.recommendation_engine.compare_portfolios(
            portfolio.current_assets
        )

        # 4. Build recommended allocation
        recommended_allocation = DiversificationRules.allocate_weights_by_yield(
            suggested_fiis
        )

        # 5. Calculate diversification metrics
        type_distribution = DiversificationRules.get_type_distribution(suggested_fiis)
        herfindahl = DiversificationRules.calculate_herfindahl_index(suggested_fiis)

        diversification_summary = {
            "type_distribution": type_distribution,
            "herfindahl_index": herfindahl,
            "suggested_fii_count": len(suggested_fiis),
            "concentration_level": "alta" if herfindahl > 5000 else "media" if herfindahl > 2500 else "baixa",
        }

        # 6. Calculate analytics (optional)
        analytics = None
        if portfolio.current_assets:
            analytics = self._calculate_analytics(portfolio, suggested_fiis)

        # 7. Build output
        return AnalysisOutput(
            portfolio_analysis=portfolio_recommendation,
            diversification_summary=diversification_summary,
            recommended_allocation=recommended_allocation,
            analytics=analytics,
            executive_summary="",  # Will be filled by Writer agent
            detailed_report="",  # Will be filled by Writer agent
        )

    def _calculate_analytics(self, portfolio: PortfolioInput, suggested_fiis) -> AnalyticsMetrics:
        """Calculate Sharpe, Treynor, and projections."""
        fii_snapshot = self.fii_provider.load()

        # Get first available FII's returns for estimation
        portfolio_returns = []
        if fii_snapshot.fiis:
            first_fii = fii_snapshot.fiis[0]
            if first_fii.monthly_returns_pct:
                portfolio_returns = first_fii.monthly_returns_pct

        # Get IFIX benchmark
        ifix_provider = self.fii_provider.get_returns  # Placeholder
        ifix_benchmark = BenchmarkComparison.get_ifix_benchmark()
        benchmark_returns = ifix_benchmark["returns"]

        # Calculate metrics
        sharpe = None
        treynor = None
        volatility = None

        if portfolio_returns:
            volatility = RiskMetrics.calculate_volatility(portfolio_returns)
            sharpe = RiskMetrics.calculate_sharpe_ratio(
                portfolio_returns, SHARPE_RISK_FREE_RATE
            )

            if len(benchmark_returns) >= len(portfolio_returns):
                treynor = RiskMetrics.calculate_treynor_ratio(
                    portfolio_returns,
                    benchmark_returns[: len(portfolio_returns)],
                    SHARPE_RISK_FREE_RATE,
                )

        # Project 5-year growth
        projected_value = None
        if portfolio.monthly_contribution_brl and portfolio_returns:
            avg_return = sum(portfolio_returns) / len(portfolio_returns)
            projection = PortfolioProjection.project_portfolio(
                initial_value_brl=portfolio.total_patrimony_brl,
                monthly_contribution_brl=portfolio.monthly_contribution_brl,
                monthly_return_pct=avg_return,
                months=portfolio.investment_horizon_months or 60,
            )
            projected_value = projection["final_value"]

        return AnalyticsMetrics(
            sharpe_ratio=sharpe,
            treynor_ratio=treynor,
            portfolio_volatility_pct=volatility,
            benchmark_comparison=BenchmarkComparison.compare_returns(
                portfolio_returns, benchmark_returns
            ),
            projected_value_5y_brl=projected_value,
        )
