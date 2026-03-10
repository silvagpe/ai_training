"""Portfolio input models."""
from pydantic import BaseModel
from typing import List, Optional


class PortfolioAsset(BaseModel):
    """Single asset in client's portfolio."""
    ticker: str
    quantity: float  # Number of shares/units
    current_price: float  # Current price in BRL
    entry_date: Optional[str] = None  # ISO date


class PortfolioInput(BaseModel):
    """Client portfolio for analysis."""
    client_id: Optional[str] = None
    current_assets: List[PortfolioAsset]  # Assets client currently holds
    total_patrimony_brl: float  # Total investable patrimony
    monthly_contribution_brl: Optional[float] = None  # Monthly contribution amount
    investment_horizon_months: Optional[int] = 60  # Default: 5 years


class PortfolioAnalysisRequest(BaseModel):
    """Request to analyze a portfolio."""
    portfolio: PortfolioInput
    include_projection: bool = True
    include_analytics: bool = True
    max_recommendations: Optional[int] = None  # Override default count
