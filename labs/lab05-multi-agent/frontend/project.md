Based on the JSONs below, I would like to create an Angular website where the client can input their portfolio and the backend will process the data and provide the analysis results.

ALL website texts must be in English

Framework: angular tailwind

Design: create a single page where at the top the client enters the data, clicks an analyze button, and the system displays the results below separated into information blocks. All website texts must be in English

Frontend location: /mnt/dados/projetos/taller/ai_training/labs/lab05-multi-agent/frontend
Backend location: /mnt/dados/projetos/taller/ai_training/labs/lab05-multi-agent/python


Input Payload
```json
{     
	"client_id": "test_client_001",     
 	"current_assets": [       
	{         
		"ticker": "KNCR11",
		"quantity": 10,
		"current_price": 9.66
	}],
	"total_patrimony_brl": 100000,
	"monthly_contribution_brl": 1000,
	"investment_horizon_months": 60
}
```

Output Payload / Analysis Result
```json
{
	"analysis": {
		"portfolio_analysis": {
			"hold_assets": [],
			"buy_assets": [
				{
					"ticker": "XPML11",
					"name": "Xp Malls Fundos",
					"fund_type": "tijolo",
					"segment": "shoppings_varejo",
					"action": "BUY",
					"current_price": 1.0,
					"dy_pct": 9.98,
					"price_to_book": 1.0,
					"reason": "Recommended by portfolio strategy.",
					"source": "recommended",
					"weight_recommended_pct": 10.0
				},
				{
					"ticker": "HGLG11",
					"name": "Pátria Log",
					"fund_type": "tijolo",
					"segment": "logistica_industria",
					"action": "BUY",
					"current_price": 0.95,
					"dy_pct": 8.35,
					"price_to_book": 0.95,
					"reason": "Recommended by portfolio strategy.",
					"source": "recommended",
					"weight_recommended_pct": 5.0
				},
				{
					"ticker": "MXRF11",
					"name": "Maxi Renda",
					"fund_type": "papel",
					"segment": "hibrido",
					"action": "BUY",
					"current_price": 1.03,
					"dy_pct": 12.28,
					"price_to_book": 1.03,
					"reason": "Recommended by portfolio strategy.",
					"source": "recommended",
					"weight_recommended_pct": 5.0
				},
				{
					"ticker": "PVBI11",
					"name": "Vbi Prime Properties",
					"fund_type": "tijolo",
					"segment": "lajes_corporativas",
					"action": "BUY",
					"current_price": 0.73,
					"dy_pct": 7.15,
					"price_to_book": 0.73,
					"reason": "Recommended by portfolio strategy.",
					"source": "recommended",
					"weight_recommended_pct": 10.0
				},
				{
					"ticker": "VISC11",
					"name": "Vinci Shopping Centers",
					"fund_type": "tijolo",
					"segment": "shoppings_varejo",
					"action": "BUY",
					"current_price": 0.94,
					"dy_pct": 8.79,
					"price_to_book": 0.94,
					"reason": "Recommended by portfolio strategy.",
					"source": "recommended",
					"weight_recommended_pct": 10.0
				},
				{
					"ticker": "XPLG11",
					"name": "Xp Log",
					"fund_type": "tijolo",
					"segment": "logistica_industria",
					"action": "BUY",
					"current_price": 0.96,
					"dy_pct": 9.71,
					"price_to_book": 0.96,
					"reason": "Recommended by portfolio strategy.",
					"source": "recommended",
					"weight_recommended_pct": 10.0
				},
				{
					"ticker": "XPCI11",
					"name": "Xp Credito Imobiliário",
					"fund_type": "papel",
					"segment": "titulos_valores",
					"action": "BUY",
					"current_price": 0.95,
					"dy_pct": 12.94,
					"price_to_book": 0.95,
					"reason": "Recommended by portfolio strategy.",
					"source": "recommended",
					"weight_recommended_pct": 12.5
				},
				{
					"ticker": "KNIP11",
					"name": "Kinea Índice De Preços Fundo",
					"fund_type": "papel",
					"segment": "titulos_valores",
					"action": "BUY",
					"current_price": 0.98,
					"dy_pct": 10.65,
					"price_to_book": 0.98,
					"reason": "Recommended by portfolio strategy.",
					"source": "recommended",
					"weight_recommended_pct": 12.5
				},
				{
					"ticker": "GARE11",
					"name": "Guardian Real Estate",
					"fund_type": "tijolo",
					"segment": "hibrido",
					"action": "BUY",
					"current_price": 0.89,
					"dy_pct": 11.7,
					"price_to_book": 0.89,
					"reason": "Recommended by portfolio strategy.",
					"source": "recommended",
					"weight_recommended_pct": 5.0
				},
				{
					"ticker": "JURO11",
					"name": "Sparta Infra Fic Fi-Infra",
					"fund_type": "misto",
					"segment": "infraestrutura",
					"action": "BUY",
					"current_price": 1.0,
					"dy_pct": 11.71,
					"price_to_book": 1.0,
					"reason": "Recommended by portfolio strategy.",
					"source": "recommended",
					"weight_recommended_pct": 10.0
				},
				{
					"ticker": "KNCA11",
					"name": "Kinea Crédito Agro Fiagro",
					"fund_type": "misto",
					"segment": "fiagros",
					"action": "BUY",
					"current_price": 0.94,
					"dy_pct": 13.91,
					"price_to_book": 0.94,
					"reason": "Recommended by portfolio strategy.",
					"source": "recommended",
					"weight_recommended_pct": 5.0
				},
				{
					"ticker": "SNAG11",
					"name": "Suno Agro",
					"fund_type": "misto",
					"segment": "fiagros",
					"action": "BUY",
					"current_price": 1.04,
					"dy_pct": 13.94,
					"price_to_book": 1.04,
					"reason": "Recommended by portfolio strategy.",
					"source": "recommended",
					"weight_recommended_pct": 5.0
				}
			],
			"sell_assets": [
				{
					"ticker": "KNCR11",
					"name": "Kinea Rendimentos Imobiliários Fundos",
					"fund_type": "papel",
					"segment": "titulos_valores",
					"action": "SELL",
					"current_price": 9.66,
					"dy_pct": 13.77,
					"price_to_book": 1.04,
					"reason": "Not in recommended portfolio. Consider swapping for more attractive alternative.",
					"source": "client_portfolio",
					"weight_recommended_pct": null
				}
			]
		},
		"diversification_summary": {
			"type_distribution": {
				"tijolo": 66.66666666666666,
				"papel": 33.33333333333333
			},
			"herfindahl_index": 3333.3333333333326,
			"suggested_fii_count": 3,
			"concentration_level": "media"
		},
		"recommended_allocation": {
			"TRXF11": 29.831539541413193,
			"GGRC11": 29.73795039775386,
			"HCTR11": 40.430510060832944
		},
		"analytics": {
			"sharpe_ratio": 4.4183626360571235,
			"treynor_ratio": -395.4788801279638,
			"portfolio_volatility_pct": 1.6635121662532941,
			"benchmark_comparison": {
				"portfolio_total_return_pct": 7.642699159499644,
				"benchmark_total_return_pct": -2.3404387239370106,
				"outperformance_pct": 9.983137883436655,
				"portfolio_avg_monthly_pct": 0.6166666666666667,
				"benchmark_avg_monthly_pct": -0.14916666666666675,
				"periods_analyzed": 12
			},
			"projected_value_5y_brl": 217394.18881183726
		},
		"executive_summary": "",
		"detailed_report": ""
	},
	"executive_summary": "Subject: **Strategic Portfolio Optimization: Enhancing Yield and Structural Resilience**\n\nDear Investor,\n\nBased on our latest market analysis and your portfolio’s strategic objectives, we have identified a significant opportunity to optimize your real estate fund (FII) holdings. Your current position shows exceptional risk-adjusted potential (Sharpe Ratio: 4.42), but requires a structural shift to better align with current market leadership and reduce concentration risks.\n\n### 1. Executive Summary\nThe current strategy focuses on pivoting toward a robust \"Core-and-Satellite\" model, maintaining a solid foundation in physical assets (Tijolo) while capturing high-yield opportunities in the Agribusiness and Credit sectors. We recommend a full exit from non-compliant positions to reallocate capital into 12 high-performing assets that balance immediate income with long-term capital preservation.\n\n---\n\n### 2. Action Items\n\n#### **SELL (Exit)**\n*   **KNCR11:** While this fund offers high liquidity, it no longer aligns with our current strategic filters for optimized risk-return. We recommend a complete divestment to free up capital for assets with higher total return potential.\n\n#### **BUY (Strategic Additions)**\nWe are initiating buy orders for the following assets to build a diversified income stream:\n\n**The \"Income Engines\" (Paper/Agri/Infra):**\n*   **SNAG11 & KNCA11 (DY 13.94% & 13.91%):** High-yield Fiagros providing exposure to the resilient Brazilian agribusiness sector.\n*   **MXRF11 (DY 12.28%):** A market favorite for consistent credit premiums.\n*   **XPCI11 (DY 12.94%) & KNIP11 (DY 10.65%):** Solid CRI (Real Estate Credit) portfolios for inflation-plus returns.\n*   **JURO11 (DY 11.71%):** Diversification into Infrastructure bonds (Debêntures) for tax-efficient income.\n\n**The \"Wealth Builders\" (Brick/Physical Assets):**\n*   **Logistics (HGLG11, XPLG11, GARE11):** Ranging from 8.35% to 11.70% DY, these funds provide stability through long-term leases with top-tier tenants.\n*   **Shopping Malls (XPML11, VISC11):** Yielding 9.98% and 8.79% respectively, capturing the rebound in consumer spending.\n*   **Corporate Offices (PVBI11):** Yielding 7.15%, focused on prime \"AAA\" locations in São Paulo.\n\n---\n\n### 3. Diversification Strategy\n\nOur target allocation is structured to protect your capital against volatility while ensuring a monthly cash flow \"floor\":\n\n*   **66.7% Tijolo (Brick):** This majority stake acts as your hedge against inflation. By owning physical assets like warehouses and malls, you benefit from rental increases and property appreciation.\n*   **33.3% Papel/Credit (Paper):** This segment acts as a yield booster. It provides the high double-digit Dividend Yields (averaging 12-13% in this selection) that accelerate your portfolio's compound interest.\n\n**Risk Management Note:** Our analysis shows a high concentration index (HHI 3333). To fix this, it is vital that capital is distributed **proportionally across all 12 recommended assets** rather than concentrated in just 3, ensuring your eggs are not all in one basket.\n\n---\n\n### 4. Next Steps\n\n**Implementation Timeline:**\n*   **Phase 1 (Immediate):** Liquidate KNCR11 and begin purchasing the \"Tijolo\" assets (XPML11, HGLG11, etc.) to lock in current price-to-book (P/VP) opportunities.\n*   **Phase 2 (Next 5 Business Days):** Stagger the entry into high-yield \"Papel\" funds to average out your entry price.\n\n**Rebalancing Schedule:**\n*   **Quarterly Reviews:** We will meet every 90 days to monitor the yield spreads and ensure the portfolio remains within the 66/33% type distribution.\n*   **Performance Monitoring:** We will specifically monitor the Treynor Ratio and fund management reports to ensure the credit quality of the \"Papel\" segment remains pristine.\n\nI am confident that this realignment will provide a more \"armored\" portfolio capable of delivering superior monthly income. Please let me know if you would like to proceed with these orders.\n\nBest regards,\n\n**Your Financial Advisor**",
	"detailed_report": "# FII Portfolio Analysis Report\n## Recommendations\n### ✅ BUY\n- **XPML11** (Xp Malls Fundos): Recommended by portfolio strategy.\n  - Recommended allocation: 10.0%\n- **HGLG11** (Pátria Log): Recommended by portfolio strategy.\n  - Recommended allocation: 5.0%\n- **MXRF11** (Maxi Renda): Recommended by portfolio strategy.\n  - Recommended allocation: 5.0%\n- **PVBI11** (Vbi Prime Properties): Recommended by portfolio strategy.\n  - Recommended allocation: 10.0%\n- **VISC11** (Vinci Shopping Centers): Recommended by portfolio strategy.\n  - Recommended allocation: 10.0%\n- **XPLG11** (Xp Log): Recommended by portfolio strategy.\n  - Recommended allocation: 10.0%\n- **XPCI11** (Xp Credito Imobiliário): Recommended by portfolio strategy.\n  - Recommended allocation: 12.5%\n- **KNIP11** (Kinea Índice De Preços Fundo): Recommended by portfolio strategy.\n  - Recommended allocation: 12.5%\n- **GARE11** (Guardian Real Estate): Recommended by portfolio strategy.\n  - Recommended allocation: 5.0%\n- **JURO11** (Sparta Infra Fic Fi-Infra): Recommended by portfolio strategy.\n  - Recommended allocation: 10.0%\n- **KNCA11** (Kinea Crédito Agro Fiagro): Recommended by portfolio strategy.\n  - Recommended allocation: 5.0%\n- **SNAG11** (Suno Agro): Recommended by portfolio strategy.\n  - Recommended allocation: 5.0%\n### ❌ SELL\n- **KNCR11**: Not in recommended portfolio. Consider swapping for more attractive alternative.\n## Suggested Allocation\n- TRXF11: 29.8%\n- GGRC11: 29.7%\n- HCTR11: 40.4%\n",
	"review_feedback": "As a Portfolio Quality Assurance Specialist, I have reviewed your recommendation against the provided reference data and market standards.\n\n### **1. Compliance Check**\n*   **Asset Eligibility**: **Partial Pass.** The recommendation identifies all assets as \"FIIs\" (Real Estate Investment Funds). However, **SNAG11** and **KNCA11** are **FIAGROs**, and **JURO11** is an **FI-Infra**. While they trade similarly, they are governed by different tax and regulatory frameworks. This should be explicitly clarified to the investor.\n*   **Portfolio Count**: **FAIL.** The Reference Data specifies a `suggested_fii_count: 3`, yet the recommendation proposes **12 assets**. This is a significant breach of the target range provided in the analytics.\n*   **Diversification**: **Inconsistent.** The Reference Data shows a Herfindahl-Index (HHI) of **3333.33** (which indicates high concentration, equivalent to ~3 assets). The recommendation claims to solve this by spreading capital across 12 assets, but it ignores the \"suggested count\" of 3.\n\n### **2. Clarity Check**\n*   **Action Items**: **Pass.** SELL/BUY instructions are clear and categorized by asset type (Tijolo vs. Papel).\n*   **Metrics Accuracy**: **Partial Pass.**\n    *   Dividend Yields (DY) match the reference data.\n    *   **P/VP Mention**: In \"Next Steps,\" you mention locking in \"P/VP opportunities,\" but **no P/VP ratios are actually cited** in the text. An investor cannot verify if an asset is cheap without these numbers.\n*   **Language**: **Pass.** The tone is professional, authoritative, and sophisticated.\n\n### **3. Consistency Check**\n*   **The \"Treynor Ratio\" Contradiction (CRITICAL)**: The recommendation describes the portfolio as having \"exceptional risk-adjusted potential.\" However, the Reference Data shows a **Treynor Ratio of -395.48**. A negative Treynor Ratio usually indicates that the portfolio return is lower than the risk-free rate (or has a negative Beta). It is mathematically contradictory to call a negative Treynor portfolio \"pristine\" or \"exceptional.\"\n*   **Strategic Logic**: You recommend selling **KNCR11** (a premier Credit/CDI fund) while simultaneously initiating a buy for **KNIP11** and **XPCI11** (also Credit funds). The justification that KNCR11 \"no longer aligns with strategic filters\" is vague, especially since the \"Income Engines\" section suggests a high appetite for credit.\n\n### **4. Feedback & Improvements**\n\n#### **Specific Suggestions:**\n1.  **Reconcile the Asset Count**: If the target count is 3 (as per data), why are 12 being recommended? If 12 is the correct strategy, the Reference Data must be updated. If 3 is the rule, you must select the top 3 and cut the rest.\n2.  **Correct Asset Nomenclature**: Do not label SNAG11, KNCA11, and JURO11 as FIIs. Use the term \"Listed Funds\" or \"Yield Assets\" to include FIAGROs and FI-Infra.\n3.  **Address the Treynor Ratio**: A negative Treynor Ratio is a red flag. If this is an error in the analytics, fix the data. If the data is correct, you cannot market this portfolio as \"high quality\" without explaining why the risk-adjusted return is currently negative.\n4.  **Add P/VP Data**: Since you mention Price-to-Book (P/VP) in the implementation phase, include the values (e.g., *HGLG11: P/VP 1.02*) to justify the \"BUY\" rating.\n\n#### **Overall Quality Rating: 5/10**\n*The recommendation is well-written and looks professional, but it contains **major analytical contradictions** regarding the Treynor Ratio and Asset Count that could mislead an investor.*\n\n#### **Is the recommendation actionable?**\n**No.** Not until the discrepancy between the \"Suggested Count: 3\" and the \"Recommended: 12\" is resolved. An investor would not know whether to buy all 12 or just 3.\n\n---\n**Flagged Issues:**\n*   **Inconsistency:** Suggested count 3 vs. recommended 12.\n*   **Analytical Error:** Marketing a negative Treynor Ratio as \"exceptional.\"\n*   **Tax/Legal Mislabeling:** Calling FIAGRO/FI-Infra \"FIIs.\""
}
```
