"""FII Portfolio Analyzer API."""
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from dotenv import load_dotenv
from supervisor import SupervisorAgent
from llm_client import get_llm_client
from schemas import PortfolioInput, PortfolioAsset, AnalysisOutput

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="FII Portfolio Analyzer",
    description="Multi-agent system for Brazilian Real Estate Investment Fund portfolio analysis",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LLM and Supervisor
provider = os.getenv("LLM_PROVIDER", "google")
llm = get_llm_client(provider)
supervisor = SupervisorAgent(llm)


@app.post("/analyze")
async def analyze_portfolio(request: PortfolioInput) -> Dict:
    """Analyze a FII portfolio and return recommendations.
    
    Args:
        request: Portfolio with current assets, patrimony, and contribution info
        
    Returns:
        Analysis with recommendations, metrics, and detailed report
    """
    try:
        result = supervisor.run(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "provider": provider}
async def health():
    return {"status": "healthy", "provider": provider}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
