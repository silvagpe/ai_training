"""Diversification rules and suggestions."""
from typing import List, Dict, Tuple
from schemas import FII
from config.settings import (
    PATRIMONIO_TIERS,
    FUND_TYPES,
    PREFERENCE_TYPE,
    MIN_TYPES_IN_PORTFOLIO,
    MAX_SINGLE_TYPE_PCT,
)


class DiversificationRules:
    """Rules for portfolio diversification."""

    @staticmethod
    def suggest_fii_count(patrimonio_brl: float) -> Tuple[int, int]:
        """Suggest range of FIIs based on patrimonio.
        
        Returns:
            (min_count, max_count) tuple
        """
        for tier_name, tier_config in PATRIMONIO_TIERS.items():
            if "max" in tier_config:
                if patrimonio_brl <= tier_config["max"]:
                    count_or_range = tier_config["fii_count"]
                    if isinstance(count_or_range, tuple):
                        return count_or_range
                    else:
                        return (count_or_range, count_or_range)

        # Default for large
        return (5, 10)

    @staticmethod
    def get_type_distribution(fiis: List[FII]) -> Dict[str, float]:
        """Get distribution of fund types (%) in a portfolio."""
        if not fiis:
            return {}

        type_counts = {}
        for fii in fiis:
            type_counts[fii.fund_type] = type_counts.get(fii.fund_type, 0) + 1

        total = len(fiis)
        return {k: (v / total * 100) for k, v in type_counts.items()}

    @staticmethod
    def calculate_herfindahl_index(fiis: List[FII]) -> float:
        """Calculate Herfindahl concentration index.
        
        Range: 0 (perfect diversity) to 10,000 (full concentration).
        """
        if not fiis:
            return 0

        summary = {}
        for fii in fiis:
            summary[fii.ticker] = summary.get(fii.ticker, 0) + 1

        total = len(fiis)
        return sum((count / total * 100) ** 2 for count in summary.values())

    @staticmethod
    def suggest_balanced_portfolio(
        eligible_fiis: List[FII], 
        target_count: int = 5,
        recommended_fiis: List[FII] = None
    ) -> List[FII]:
        """Suggest balanced portfolio using recommended portfolio.
        
        If recommended_fiis provided, uses those (respecting target_count limit).
        Otherwise, returns eligible_fiis truncated to target_count.
        
        Args:
            eligible_fiis: List of eligible FIIs
            target_count: Maximum number of FIIs to include
            recommended_fiis: Pre-selected recommended FIIs to use
            
        Returns:
            Selected FIIs (up to target_count)
        """
        # Use recommended portfolio if provided
        if recommended_fiis:
            return recommended_fiis[:target_count]
        
        # Fallback: use eligible FIIs up to target_count
        if not eligible_fiis:
            return []
        
        return eligible_fiis[:target_count]

    @staticmethod
    def allocate_weights(fiis: List[FII]) -> Dict[str, float]:
        """Allocate equal weights to portfolioembers.
        
        Returns: {ticker: weight_pct}
        """
        if not fiis:
            return {}

        weight = 100.0 / len(fiis)
        return {fii.ticker: weight for fii in fiis}

    @staticmethod
    def allocate_weights_by_yield(fiis: List[FII]) -> Dict[str, float]:
        """Allocate weights proportional to dividend yield.
        
        Returns: {ticker: weight_pct}
        """
        if not fiis:
            return {}

        total_dy = sum(fii.dy_12m_pct for fii in fiis)
        if total_dy == 0:
            return DiversificationRules.allocate_weights(fiis)

        return {fii.ticker: (fii.dy_12m_pct / total_dy * 100) for fii in fiis}
