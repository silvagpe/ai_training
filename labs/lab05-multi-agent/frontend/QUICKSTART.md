# Quick Start Guide - FII Portfolio Analyzer

## Getting Started

This guide will help you run the FII Portfolio Analyzer application locally.

### Step 1: Start the Backend API

```bash
cd /mnt/dados/projetos/taller/ai_training/labs/lab05-multi-agent/python

# Activate virtual environment (if you have one)
source .venv/bin/activate

# Or create one if needed
# python -m venv .venv && source .venv/bin/activate

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Set environment variables
export GOOGLE_API_KEY="your-google-api-key"  # Or use another LLM provider
export LLM_PROVIDER="google"  # Options: google, anthropic, openai

# Start the server
uvicorn main:app --reload --port 8000
```

The API will be available at: `http://localhost:8000`

### Step 2: Start the Frontend Application

Open a new terminal:

```bash
cd /mnt/dados/projetos/taller/ai_training/labs/lab05-multi-agent/frontend/portfolio-analyzer

# Install dependencies
npm install

# Start development server
npm start
```

The frontend will be available at: `http://localhost:4200`

### Step 3: Use the Application

1. Open your browser to `http://localhost:4200`
2. Fill in the portfolio form:
   - **Client ID**: (optional) e.g., "client_001"
   - **Total Patrimony**: e.g., 100000 (BRL)
   - **Monthly Contribution**: (optional) e.g., 1000 (BRL)
   - **Investment Horizon**: e.g., 60 (months)
   - **Current Assets**: Add at least one asset
     - Ticker: e.g., "KNCR11"
     - Quantity: e.g., 10
     - Current Price: e.g., 9.66
3. Click "Analyze Portfolio"
4. Wait for the analysis (may take 30-60 seconds due to AI processing)
5. Review the comprehensive results

## Test Data

Use this sample data for testing:

```json
{
  "client_id": "test_client_001",
  "total_patrimony_brl": 100000,
  "monthly_contribution_brl": 1000,
  "investment_horizon_months": 60,
  "current_assets": [
    {
      "ticker": "KNCR11",
      "quantity": 10,
      "current_price": 9.66
    }
  ]
}
```

## Troubleshooting

### Backend Issues

- **Error: GOOGLE_API_KEY not set**: Export the environment variable with your API key
- **Port 8000 already in use**: Change the port with `--port 8001`
- **Module not found**: Run `pip install -r requirements.txt`

### Frontend Issues

- **Port 4200 already in use**: The Angular CLI will automatically try 4201, 4202, etc.
- **CORS errors**: Make sure the backend is running and CORS is enabled (already configured)
- **Build errors**: Delete `node_modules` and run `npm install` again
- **Missing dependencies**: Run `npm install`

### Analysis Takes Too Long

The analysis may take 30-90 seconds because:
- The backend uses AI agents (Researcher, Writer, Reviewer)
- Multiple LLM calls are made for comprehensive analysis
- This is expected behavior for the multi-agent system

## Features to Explore

1. **Portfolio Actions**: View Buy/Hold/Sell recommendations with detailed reasoning
2. **Analytics Metrics**: Check Sharpe ratio, Treynor ratio, and volatility
3. **Benchmark Comparison**: See how your portfolio compares to IFIX
4. **Diversification**: Review asset type distribution and concentration
5. **Executive Summary**: Read AI-generated investment advice
6. **Detailed Report**: Expand to see comprehensive analysis
7. **Quality Review**: Check the QA agent's feedback on recommendations

## API Documentation

Once the backend is running, visit:
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

## Next Steps

- Try different asset combinations
- Experiment with various patrimony levels
- Compare results with different investment horizons
- Review the multi-agent workflow in the backend code
- Customize the UI theme in Tailwind CSS

Enjoy analyzing your FII portfolio! 📊
