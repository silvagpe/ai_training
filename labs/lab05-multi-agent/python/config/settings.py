"""Configuration and constants for FII portfolio analyzer."""

# Eligibility Rules
MIN_YEARS_EXISTENCE = 5
MIN_DAILY_VOLUME_BRL = 1_000_000  # 1 million BRL
MIN_NET_EQUITY_BRL = 1_000_000_000  # 1 billion BRL
MAX_TOP_50_RANK = 50

# Portfolio Sizing Rules (by client patrimony)
PATRIMONIO_TIERS = {
    "small": {"max": 100_000, "fii_count": 3},
    "medium": {"min": 100_000, "max": 300_000, "fii_count": 5},
    "large": {"min": 300_000, "max": float("inf"), "fii_count": (5, 10)},
}

# Fund Types
FUND_TYPES = ["tijolo", "papel", "misto"]
PREFERENCE_TYPE = "tijolo"  # Preferred type for diversification

# Diversification Rules
MIN_TYPES_IN_PORTFOLIO = 2  # At least 2 different types
MAX_SINGLE_TYPE_PCT = 70  # Max 70% in single type

# Comparison & Analytics
SHARPE_RISK_FREE_RATE = 0.05  # 5% annual risk-free rate
IFIX_BENCHMARK_SYMBOL = "IFIX"

# LLM Configuration
DEFAULT_LLM_PROVIDER = "google"
DEFAULT_LLM_MODEL = "gemini-2.0-flash"
LLM_MAX_TOKENS = 4096
LLM_TEMPERATURE = 0.7

# API Configuration
API_PORT = 8000
API_HOST = "0.0.0.0"

# Data Paths
DATA_SNAPSHOT_DIR = "./data/snapshots"
FII_SNAPSHOT_FILE = "fii_snapshot.json"
IFIX_SNAPSHOT_FILE = "ifix_5y.json"
RECOMMENDED_PORTFOLIO_FILE = "recommended_portfolio.json"
