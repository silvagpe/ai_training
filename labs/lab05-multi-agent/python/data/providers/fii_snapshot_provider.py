"""Data providers for FII snapshots."""
import json
from pathlib import Path
from typing import Optional
from ..schemas import FIISnapshot, RecommendedPortfolio


class FIISnapshotProvider:
    """Load FII snapshot from JSON."""

    def __init__(self, snapshot_path: Optional[str] = None):
        if snapshot_path is None:
            # Default to data/snapshots/fii_snapshot.json relative to this file
            snapshot_path = Path(__file__).parent.parent / "snapshots" / "fii_snapshot.json"
        self.snapshot_path = Path(snapshot_path)

    def load(self) -> FIISnapshot:
        """Load and parse FII snapshot."""
        with open(self.snapshot_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return FIISnapshot(**data)

    def get_by_ticker(self, ticker: str) -> Optional[dict]:
        """Get single FII by ticker."""
        snapshot = self.load()
        for fii in snapshot.fiis:
            if fii.ticker == ticker:
                return fii.model_dump()
        return None


class IFIXProvider:
    """Load IFIX benchmark data from JSON."""

    def __init__(self, ifix_path: Optional[str] = None):
        if ifix_path is None:
            ifix_path = Path(__file__).parent.parent / "snapshots" / "ifix_5y.json"
        self.ifix_path = Path(ifix_path)

    def load(self) -> dict:
        """Load IFIX data."""
        with open(self.ifix_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_returns(self) -> list:
        """Get list of monthly returns (%)."""
        data = self.load()
        return [s["return_pct"] for s in data["series"]]

    def get_series_dates(self) -> list:
        """Get list of dates."""
        data = self.load()
        return [s["date"] for s in data["series"]]


class RecommendedPortfolioProvider:
    """Load recommended portfolio template."""

    def __init__(self, portfolio_path: Optional[str] = None):
        if portfolio_path is None:
            portfolio_path = Path(__file__).parent.parent / "snapshots" / "recommended_portfolio.json"
        self.portfolio_path = Path(portfolio_path)

    def load(self) -> RecommendedPortfolio:
        """Load and parse recommended portfolio."""
        with open(self.portfolio_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return RecommendedPortfolio(**data)

    def get_tickers(self) -> list:
        """Get list of recommended tickers."""
        portfolio = self.load()
        return [rec["ticker"] for rec in portfolio.recommendations]
