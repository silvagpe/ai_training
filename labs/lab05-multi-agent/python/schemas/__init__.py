"""Schemas for FII portfolio analyzer."""
from .fii import FII, FIISnapshot
from .portfolio import PortfolioInput, PortfolioAsset
from .analysis import (
    AssetEligibility,
    AssetAnalysis,
    PortfolioRecommendation,
    RecommendationAction,
    AnalysisOutput,
    AnalyticsMetrics,
)
from .recommendation import RecommendedFII, RecommendedPortfolio

__all__ = [
    "FII",
    "FIISnapshot",
    "PortfolioInput",
    "PortfolioAsset",
    "AssetEligibility",
    "AssetAnalysis",
    "PortfolioRecommendation",
    "RecommendationAction",
    "AnalysisOutput",
    "AnalyticsMetrics",
    "RecommendedFII",
    "RecommendedPortfolio",
]
