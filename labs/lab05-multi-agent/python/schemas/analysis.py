"""Analysis result models."""
from pydantic import BaseModel
from typing import List, Dict, Optional
from enum import Enum


class RecommendationAction(str, Enum):
    """Action recommendation for an asset."""
    HOLD = "HOLD"  # Hold
    BUY = "BUY"  # Buy
    SELL = "SELL"  # Sell


class AssetEligibility(BaseModel):
    """Eligibility check results for a single FII."""
    ticker: str
    eligible: bool
    rules_passed: List[str]  # e.g., ["age_ok", "volume_ok", "equity_ok"]
    rules_failed: List[str]  # e.g., ["not_in_top_50"]
    fail_reasons: Dict[str, str]  # Detailed reasons


class AssetAnalysis(BaseModel):
    """Analysis of a single asset (client's or recommended)."""
    ticker: str
    name: str
    fund_type: str
    segment: str
    action: RecommendationAction
    current_price: float
    dy_pct: float
    price_to_book: float
    reason: str  # LLM-generated explanation
    source: str  # "client_portfolio" or "recommended"
    weight_recommended_pct: Optional[float] = None  # Suggested allocation %


class PortfolioRecommendation(BaseModel):
    """Recommended action on portfolio composition."""
    hold_assets: List[AssetAnalysis]
    buy_assets: List[AssetAnalysis]
    sell_assets: List[AssetAnalysis]


class AnalyticsMetrics(BaseModel):
    """Portfolio analytics (Sharpe, Treynor, comparison)."""
    sharpe_ratio: Optional[float] = None
    treynor_ratio: Optional[float] = None
    portfolio_volatility_pct: Optional[float] = None
    benchmark_comparison: Optional[Dict] = None
    projected_value_5y_brl: Optional[float] = None


class AnalysisOutput(BaseModel):
    """Complete analysis output."""
    portfolio_analysis: PortfolioRecommendation
    diversification_summary: Dict  # Type distribution, concentration metrics
    recommended_allocation: Dict  # { ticker: weight_pct }
    analytics: Optional[AnalyticsMetrics] = None
    executive_summary: str  # LLM-generated narrative summary
    detailed_report: str  # LLM-generated detailed markdown report
