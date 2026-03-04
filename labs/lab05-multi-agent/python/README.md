# FII Portfolio Analyzer — Multi-Agent System

An intelligent **Brazilian Real Estate Investment Fund (FII)** portfolio analysis system using AI agents coordinated by a supervisor.

## 🎯 Features

- ✅ **Eligibility Validation**: Evaluates each FII against strict rules (age, volume, patrimony, top 50)
- 📊 **Diversification Analysis**: Calculates concentration (Herfindahl), distribution by type (Real Estate/Papers/Mixed)
- 🤖 **Multi-Agent Recommendations**: Researcher, Writer, and Reviewer collaborate using LLM (Google Gemini)
- 📈 **Financial Metrics**: Sharpe, Treynor, growth projection, IFIX comparison
- 💡 **Markdown Reports**: Clear recommendations with traceable justifications

## 📁 Project Structure

```
python/
├── config/settings.py               # Constants and configuration
├── schemas/                          # Pydantic models (input/output)
│   ├── fii.py                       # FII data model
│   ├── portfolio.py                 # Client portfolio input
│   ├── analysis.py                  # Structured analysis output
│   └── recommendation.py            # Recommendation data
├── domain/                          # Pure business logic (deterministic)
│   ├── portfolio_rules.py           # Eligibility validation (5 rules)
│   ├── diversification.py           # Diversification calculation
│   └── recommendation.py            # Recommendation engine
├── data/                            # Data layer
│   ├── providers/
│   │   └── fii_snapshot_provider.py # Loads JSON with FIIs
│   └── snapshots/                   # Local data (JSON)
│       ├── fii_snapshot.json        # Eligible FIIs catalog
│       ├── ifix_5y.json             # IFIX 5-year historical series
│       └── recommended_portfolio.json # Recommended portfolio
├── analytics/                       # Analysis layer
│   ├── projection.py                # Growth projection with contributions
│   ├── sharpe_treynor.py           # Risk-return indices
│   └── benchmark_ifix.py           # Benchmark comparison
├── services/                        # Layer orchestration
│   └── portfolio_service.py         # End-to-end analysis flow
├── agents.py                        # Agents (Researcher, Writer, Reviewer)
├── supervisor.py                    # Multi-agent coordinator
├── llm_client.py                    # LLM client (Google Gemini default)
├── main.py                          # FastAPI
├── tests/                           # Tests
│   ├── test_rules.py               # Eligibility and diversification tests
│   ├── test_analytics.py           # Sharpe, Treynor, projection tests
│   └── test_e2e.py                 # End-to-end test
└── requirements-fii.txt            # Dependencies
```

## 🚀 Quick Start

### 1. Installation

```bash
cd /mnt/dados/projetos/taller/ai_training/labs/lab05-multi-agent/python

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements-fii.txt
```

### 2. Configure LLM (Google Gemini)

```bash
export GOOGLE_API_KEY="your-key-here"
export LLM_PROVIDER="google"  # or "anthropic", "openai"
```

### 3. Tests

```bash
# Business rules test
python3 tests/test_rules.py

# Analytics test
python3 tests/test_analytics.py

# End-to-end test (no LLM)
python3 tests/test_e2e.py
```

### 4. API

```bash
# Start server
uvicorn main:app --reload --port 8000

# Open documentation
curl http://localhost:8000/docs
```

### 5. Update `fii_snapshot.json` from CSV

Use this single command to regenerate the snapshot from `FIIs - lista investidor 10 - Página1.csv`:

```bash
cd /Users/silvagpe/projetos/taller/ai_training/labs/lab05-multi-agent/python \
  && source .venv/bin/activate \
  && python scripts/update_fii_snapshot_from_csv.py
```

Script location: `scripts/update_fii_snapshot_from_csv.py`
Output file: `data/snapshots/fii_snapshot.json`

## 📡 API Endpoints

### `POST /analyze` — Analyze Portfolio

**Request:**
```json
{
  "client_id": "client_001",
  "current_assets": [
    {
      "ticker": "KNCR11",
      "quantity": 10,
      "current_price": 9.66,
      "entry_date": "2024-01-01"
    }
  ],
  "total_patrimony_brl": 100000,
  "monthly_contribution_brl": 1000,
  "investment_horizon_months": 60
}
```

**Response:**
```json
{
  "analysis": {
    "portfolio_analysis": {
      "hold_assets": [...],
      "buy_assets": [...],
      "sell_assets": [...]
    },
    "diversification_summary": {...},
    "recommended_allocation": {...},
    "analytics": {
      "sharpe_ratio": 1.25,
      "treynor_ratio": 0.18,
      "portfolio_volatility_pct": 8.5,
      "projected_value_5y_brl": 145000
    }
  },
  "executive_summary": "Your portfolio is very concentrated...",
  "detailed_report": "# Portfolio Analysis Report...",
  "review_feedback": "Recommendation validated..."
}
```

### `GET /health` — Health Check

```bash
curl http://localhost:8000/health
```

## 🔧 Business Rules (Domain Layer)

### FII Eligibility

A FII is eligible if **ALL** criteria are met:

1. **Age**: ≥ 5 years of existence
2. **Volume**: Average daily trading ≥ R$1 million
3. **Patrimony**: Net equity ≥ R$1 billion
4. **Top 50**: Among the 50 largest FIIs by market cap

### Diversification by Patrimony

| Patrimony | Recommended Qty | Distribution |
|-----------|-----------------|--------------|
| < R$100k   | 3 FIIs         | MINIMUM 2 types |
| R$100k–R$300k | 5 FIIs       | Max 70% in one type |
| > R$300k   | 5–10 FIIs      | Preference: Real Estate |

### Weight Allocation

Default: **Weighted by Dividend Yield (DY)**

```
Weight = (FII DY) / (Sum of all DYs) × 100%
```

## 📊 Metrics & Analytics

### Sharpe Ratio

$$\text{Sharpe} = \frac{\text{Average Return} - \text{Risk-Free Rate}}{\text{Volatility}}$$

Interprets: **Excess** return per unit of **total risk**

### Treynor Ratio

$$\text{Treynor} = \frac{\text{Average Return} - \text{Risk-Free Rate}}{\text{Beta}}$$

Interprets: **Excess** return per unit of **systematic risk**

### Growth Projection

```python
Final Value = Initial Value × (1 + r)^n + Monthly Contribution × [(1+r)^n - 1]/r
```

Where `r` = monthly return, `n` = number of months

## 🤖 Multi-Agent Workflow

```
Client (Portfolio Input)
         ↓
    PortfolioService
    (domain + data layers)
         ↓
    SupervisorAgent
         ├─→ ResearcherAgent
         │   ├─→ Query LLM
         │   └─→ Analyze rules compliance
         │
         ├─→ WriterAgent
         │   ├─→ Query LLM
         │   └─→ Generate recommendations
         │
         └─→ ReviewerAgent
             ├─→ Query LLM
             └─→ Validate consistency
         ↓
    AnalysisOutput (JSON)
         ↓
     Client (Recommendation in Markdown)
```

**Responsibility division:**
- **Domain**: Pure business rules (deterministic)
- **Data**: JSON snapshot loading
- **Analytics**: Financial calculations
- **Agents**: Text analysis/synthesis with LLM

## 🧪 Examples

### Simple Test (No LLM)

```python
from schemas import PortfolioInput, PortfolioAsset
from services.portfolio_service import PortfolioService

portfolio = PortfolioInput(
    current_assets=[PortfolioAsset(ticker="KNCR11", quantity=10, current_price=9.66)],
    total_patrimony_brl=100_000,
    monthly_contribution_brl=1_000,
)

service = PortfolioService()
analysis = service.evaluate_portfolio(portfolio)

print(f"HOLD: {len(analysis.portfolio_analysis.hold_assets)}")
print(f"BUY: {len(analysis.portfolio_analysis.buy_assets)}")
print(f"SELL: {len(analysis.portfolio_analysis.sell_assets)}")
```

### API Call with curl

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "current_assets": [{"ticker": "KNCR11", "quantity": 10, "current_price": 9.66}],
    "total_patrimony_brl": 100000,
    "monthly_contribution_brl": 1000
  }'
```

## 📝 Included Data

### fii_snapshot.json

Sample FIIs already loaded:
- **KNCR11** (Papers, Receivables) — 13.77% DY
- **XPML11** (Real Estate, Retail) — 9.97% DY
- **HGLG11** (Real Estate, Logistics) — 8.35% DY
- **MXRF11** (Papers, Receivables) — 12.28% DY
- **VGHF11** (Mixed) — 11.05% DY

### ifix_5y.json

Complete historical series of 60 months (5 years) of IFIX index for benchmarking.

### recommended_portfolio.json

Base recommended portfolio (XPML11, HGLG11, MXRF11, VGHF11) with rationales.

## 🔐 Environment Variables

```bash
GOOGLE_API_KEY        # (Required) Google Gemini API key
LLM_PROVIDER          # (Default: google) Options: google, anthropic, openai
DEFAULT_LLM_MODEL     # (Default: gemini-2.0-flash)
API_PORT              # (Default: 8000)
API_HOST              # (Default: 0.0.0.0)
```

## 📚 Next Steps (Post-MVP)

- [ ] Integration with real-time data APIs (B3, Investidor10)
- [ ] Database persistence
- [ ] Interactive web dashboard
- [ ] Automatic rebalancing alerts
- [ ] Historical portfolio backtesting
- [ ] Support for multiple strategies (aggressive, conservative, etc)

## 📧 Support

For questions or architecture suggestions, consult [project.md](../../project.md).

---

**Version 1.0** | Lab 5 — Capstone Project | March 2026



## Test

```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "test_client_001",
    "current_assets": [
      {
        "ticker": "KNCR11",
        "quantity": 10,
        "current_price": 9.66
      }
    ],
    "total_patrimony_brl": 100000,
    "monthly_contribution_brl": 1000,
    "investment_horizon_months": 60
  }'
```