"""FII (Real Estate Investment Fund) data models."""
from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class FII(BaseModel):
    """FII asset representation."""
    ticker: str
    name: str
    fund_type: str  # "tijolo", "papel", "misto"
    segment: str  # e.g., "logistica", "shoppings_varejo", "titulos_valores"
    inception_date: date
    avg_daily_volume_brl: float  # Average daily trading volume in BRL
    net_equity_brl: float  # Net equity in BRL
    is_top_50: bool  # Is in top 50 FIIs by market cap
    dy_12m_pct: float  # 12-month dividend yield
    dy_5y_avg_pct: Optional[float] = None  # 5-year average dividend yield
    price_to_book: float  # P/VP ratio
    return_12m_pct: Optional[float] = None  # 12-month return
    return_24m_pct: Optional[float] = None  # 24-month return
    return_5y_pct: Optional[float] = None  # 5-year return
    monthly_returns_pct: Optional[List[float]] = None  # Monthly returns for volatility calc


class FIISnapshot(BaseModel):
    """Collection of FIIs for a given date."""
    as_of: str  # ISO date string
    source: str  # Data source identifier
    fiis: List[FII]
