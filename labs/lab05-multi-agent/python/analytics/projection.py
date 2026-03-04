"""Portfolio projection calculations."""
import math
from typing import Dict, List


class PortfolioProjection:
    """Calculate future portfolio value with monthly contributions."""

    @staticmethod
    def project_portfolio(
        initial_value_brl: float,
        monthly_contribution_brl: float,
        monthly_return_pct: float,
        months: int,
    ) -> Dict[str, float]:
        """Project portfolio growth over time.

        Args:
            initial_value_brl: Starting portfolio value
            monthly_contribution_brl: Monthly contribution amount
            monthly_return_pct: Average monthly return (as %)
            months: Number of months to project

        Returns:
            {
                'initial_value': starting value,
                'total_contributions': sum of contributions,
                'final_value': ending value,
                'total_return': absolute gain,
                'return_pct': return percentage
            }
        """
        monthly_return_decimal = monthly_return_pct / 100.0
        current_value = initial_value_brl

        for i in range(months):
            # Add monthly contribution at start of period
            current_value += monthly_contribution_brl
            # Apply monthly return
            current_value *= 1 + monthly_return_decimal

        total_contributions = initial_value_brl + (monthly_contribution_brl * months)
        total_return = current_value - total_contributions
        return_pct = (total_return / total_contributions * 100) if total_contributions > 0 else 0

        return {
            "initial_value": initial_value_brl,
            "total_contributions": total_contributions,
            "final_value": current_value,
            "total_return": total_return,
            "return_pct": return_pct,
        }

    @staticmethod
    def project_dual_scenarios(
        initial_value_brl: float,
        monthly_contribution_brl: float,
        base_monthly_return_pct: float,
        months: int,
        conservative_factor: float = 0.7,
    ) -> Dict[str, Dict]:
        """Project both base and conservative scenarios.
        
        Args:
            conservative_factor: Multiplier for conservative scenario (0.7 = 70% of base return)
        
        Returns:
            {
                'base_scenario': {...projection...},
                'conservative_scenario': {...projection...}
            }
        """
        base = PortfolioProjection.project_portfolio(
            initial_value_brl,
            monthly_contribution_brl,
            base_monthly_return_pct,
            months,
        )

        conservative_return = base_monthly_return_pct * conservative_factor
        conservative = PortfolioProjection.project_portfolio(
            initial_value_brl,
            monthly_contribution_brl,
            conservative_return,
            months,
        )

        return {
            "base_scenario": base,
            "conservative_scenario": conservative,
            "difference_brl": base["final_value"] - conservative["final_value"],
        }

    @staticmethod
    def calculate_cagr(
        initial_value: float, final_value: float, years: float
    ) -> float:
        """Calculate Compound Annual Growth Rate.
        
        Returns: CAGR as percentage
        """
        if initial_value <= 0 or years <= 0:
            return 0
        return ((final_value / initial_value) ** (1 / years) - 1) * 100
