"""Supervisor agent that coordinates workers for FII portfolio analysis."""
import json
from typing import Dict, Optional
from agents import ResearcherAgent, WriterAgent, ReviewerAgent
from schemas import PortfolioInput, AnalysisOutput
from services.portfolio_service import PortfolioService

SUPERVISOR_PROMPT = """You are a portfolio supervisor managing a team of financial specialists.
Your job for FII (Real Estate Investment Fund) portfolio analysis:

Team:
- Researcher: Analyzes eligibility, rules compliance, diversification
- Writer: Transforms analysis into clear recommendations
- Reviewer: Quality checks the final recommendation

Workflow:
1. Researcher interprets the portfolio data and rules
2. Writer creates the recommendation narrative
3. Reviewer validates everything is correct

For each step, output:
DELEGATE: [agent_name]
TASK: [specific task]

When all work is done, output:
FINAL: [consolidated result]"""


class SupervisorAgent:
    """Supervisor coordinating FII portfolio analysis."""

    def __init__(self, llm_client):
        self.llm = llm_client
        self.portfolio_service = PortfolioService()

        # Initialize workers
        self.workers = {
            "Researcher": ResearcherAgent(llm_client),
            "Writer": WriterAgent(llm_client),
            "Reviewer": ReviewerAgent(llm_client)
        }

        self.results: Dict[str, str] = {}
        self.analysis_output: Optional[AnalysisOutput] = None

    def run(self, portfolio_input: PortfolioInput, max_iterations: int = 5) -> Dict:
        """Run FII portfolio analysis workflow.
        
        Args:
            portfolio_input: Client portfolio data
            max_iterations: Max LLM calls before forcing final output
            
        Returns:
            {
                'analysis': AnalysisOutput (structured data),
                'executive_summary': narrative from writer,
                'detailed_report': full markdown report,
                'review_feedback': reviewer comments
            }
        """
        # Step 0: Run domain logic (deterministic rules)
        self.analysis_output = self.portfolio_service.evaluate_portfolio(portfolio_input)

        # Prepare context for agents
        context = self._prepare_context()

        # Step 1: Researcher analyzes
        researcher_task = "Analyze this portfolio data and identify key issues: eligibility failures, concentration risks, diversification gaps, and risk profile."
        researcher_result = self.workers["Researcher"].execute(
            researcher_task, context
        )
        self.results["researcher"] = researcher_result

        # Step 2: Writer creates recommendation
        writer_task = f"""Using the researcher's analysis, create a clear client recommendation with:
- Executive summary
- Action items for each asset (HOLD/BUY/SELL)
- Diversification strategy
- Next steps

Analysis context:
{context}

Researcher insights:
{researcher_result}"""

        writer_result = self.workers["Writer"].execute(writer_task)
        self.results["writer"] = writer_result

        # Step 3: Reviewer validates
        reviewer_task = f"""Review this recommendation for accuracy and clarity:
- Are all recommended FIIs eligible?
- Is diversification correct?
- Are explanations clear and consistent?

Recommendation:
{writer_result}

Reference data:
{context}"""

        reviewer_result = self.workers["Reviewer"].execute(reviewer_task)
        self.results["reviewer"] = reviewer_result

        # Package final output
        return {
            "analysis": self.analysis_output.model_dump(),
            "executive_summary": writer_result,
            "detailed_report": self._build_markdown_report(),
            "review_feedback": reviewer_result,
        }

    def _prepare_context(self) -> str:
        """Prepare structured context for agents."""
        if not self.analysis_output:
            return ""

        context_parts = []

        # Recommendations summary
        context_parts.append("=== PORTFOLIO RECOMMENDATIONS ===")
        context_parts.append(f"HOLD ({len(self.analysis_output.portfolio_analysis.hold_assets)} assets)")
        for asset in self.analysis_output.portfolio_analysis.hold_assets:
            context_parts.append(f"  - {asset.ticker}: DY {asset.dy_pct:.2f}%, P/VP {asset.price_to_book:.2f}")

        context_parts.append(f"\nBUY ({len(self.analysis_output.portfolio_analysis.buy_assets)} assets):")
        for asset in self.analysis_output.portfolio_analysis.buy_assets:
            context_parts.append(f"  - {asset.ticker}: DY {asset.dy_pct:.2f}%, {asset.reason}")

        context_parts.append(f"\nSELL ({len(self.analysis_output.portfolio_analysis.sell_assets)} assets):")
        for asset in self.analysis_output.portfolio_analysis.sell_assets:
            context_parts.append(f"  - {asset.ticker}: {asset.reason}")

        # Diversification
        context_parts.append("\n=== DIVERSIFICATION ===")
        for k, v in self.analysis_output.diversification_summary.items():
            context_parts.append(f"{k}: {v}")

        # Analytics
        if self.analysis_output.analytics:
            context_parts.append("\n=== ANALYTICS ===")
            if self.analysis_output.analytics.sharpe_ratio:
                context_parts.append(f"Sharpe Ratio: {self.analysis_output.analytics.sharpe_ratio:.2f}")
            if self.analysis_output.analytics.treynor_ratio:
                context_parts.append(f"Treynor Ratio: {self.analysis_output.analytics.treynor_ratio:.2f}")

        return "\n".join(context_parts)

    def _build_markdown_report(self) -> str:
        """Build detailed markdown report."""
        if not self.analysis_output:
            return ""

        parts = []
        parts.append("# FII Portfolio Analysis Report\n")

        # Recommendations
        parts.append("## Recommendations\n")
        
        if self.analysis_output.portfolio_analysis.hold_assets:
            parts.append("### 🔒 HOLD\n")
            for asset in self.analysis_output.portfolio_analysis.hold_assets:
                parts.append(f"- **{asset.ticker}** ({asset.name}): {asset.reason}\n")

        if self.analysis_output.portfolio_analysis.buy_assets:
            parts.append("### ✅ BUY\n")
            for asset in self.analysis_output.portfolio_analysis.buy_assets:
                parts.append(f"- **{asset.ticker}** ({asset.name}): {asset.reason}\n")
                if asset.weight_recommended_pct:
                    parts.append(f"  - Recommended allocation: {asset.weight_recommended_pct:.1f}%\n")

        if self.analysis_output.portfolio_analysis.sell_assets:
            parts.append("### ❌ SELL\n")
            for asset in self.analysis_output.portfolio_analysis.sell_assets:
                parts.append(f"- **{asset.ticker}**: {asset.reason}\n")

        # Allocation
        parts.append("## Suggested Allocation\n")
        for ticker, weight in self.analysis_output.recommended_allocation.items():
            parts.append(f"- {ticker}: {weight:.1f}%\n")

        return "".join(parts)
