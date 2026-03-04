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
        eligible_fiis: List[FII], target_count: int = 5
    ) -> List[FII]:
        """Suggest balanced portfolio with diversification rules.
        
        Prefers Tijolo type, avoids concentration.
        """
        if not eligible_fiis:
            return []

        # Sort by type preference and dividend yield
        def sort_key(fii):
            type_preference = 0 if fii.fund_type == PREFERENCE_TYPE else 1
            return (type_preference, -fii.dy_12m_pct)  # negative for descending DY

        sorted_fiis = sorted(eligible_fiis, key=sort_key)

        # Select target_count FIIs
        selected = sorted_fiis[:target_count]

        # Check type diversity
        distribution = DiversificationRules.get_type_distribution(selected)

        # Ensure no single type > MAX_SINGLE_TYPE_PCT
        for fund_type in distribution:
            if distribution[fund_type] > MAX_SINGLE_TYPE_PCT:
                # Rebalance: replace lowest DY in that type with highest DY from other type
                type_fiis = [f for f in selected if f.fund_type == fund_type]
                worst_fii = min(type_fiis, key=lambda f: f.dy_12m_pct)

                other_fiis = [f for f in sorted_fiis if f not in selected]
                best_other = None
                for fii in other_fiis:
                    if fii.fund_type != fund_type:
                        best_other = fii
                        break

                if best_other:
                    selected.remove(worst_fii)
                    selected.append(best_other)

        return selected

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
