"""Recommended portfolio models."""
from pydantic import BaseModel
from typing import List, Optional


class RecommendedFII(BaseModel):
    """Single FII in recommended portfolio."""
    ticker: str
    name: str
    segment: str
    fund_type: str
    action: str  # "BUY", "HOLD", "SELL"
    recommended_weight_pct: float
    price_to_book: float
    dy_pct: float
    last_price: float
    rationale: Optional[str] = None


class RecommendedPortfolio(BaseModel):
    """Portfolio recommendation template."""
    as_of: str  # ISO date
    portfolio_profile: str  # "conservador_diversificado", etc
    total_weight_pct: float
    recommendations: List[RecommendedFII]
