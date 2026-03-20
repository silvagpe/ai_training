"""AI Code Review Bot - FastAPI application."""
import hashlib
import hmac
import json
import logging
import os
import time
import uuid
from collections import defaultdict, deque
from typing import Deque, Dict, List, Optional

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

from analyzer import AnalysisResult, CodeAnalyzer
from llm_client import get_llm_client

# Load environment variables
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("code-review-bot")

SUPPORTED_LANGUAGES = {"python", "javascript", "typescript", "java", "go", "rust"}
SUPPORTED_FOCUS = {"bug", "security", "performance", "style", "maintainability"}
SUPPORTED_PR_ACTIONS = {"opened", "reopened", "synchronize", "ready_for_review", "edited"}
MAX_CODE_LENGTH = int(os.getenv("MAX_CODE_LENGTH", "30000"))
MAX_BATCH_FILES = int(os.getenv("MAX_BATCH_FILES", "20"))
MAX_BATCH_TOTAL_LENGTH = int(os.getenv("MAX_BATCH_TOTAL_LENGTH", "120000"))


class SlidingWindowRateLimiter:
    """Simple in-memory sliding-window limiter."""

    def __init__(self, max_requests: int, window_seconds: int) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._hits: Dict[str, Deque[float]] = defaultdict(deque)

    def allow(self, key: str) -> bool:
        now = time.time()
        bucket = self._hits[key]
        cutoff = now - self.window_seconds

        while bucket and bucket[0] <= cutoff:
            bucket.popleft()

        if len(bucket) >= self.max_requests:
            return False

        bucket.append(now)
        return True


class ReviewRequest(BaseModel):
    """Single-code review request."""

    code: str = Field(..., min_length=1, max_length=MAX_CODE_LENGTH)
    language: str = Field(default="python")
    focus: Optional[List[str]] = None

    @field_validator("language")
    @classmethod
    def validate_language(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized not in SUPPORTED_LANGUAGES:
            raise ValueError(
                f"Unsupported language '{value}'. Supported: {sorted(SUPPORTED_LANGUAGES)}"
            )
        return normalized

    @field_validator("focus")
    @classmethod
    def validate_focus(cls, value: Optional[List[str]]) -> Optional[List[str]]:
        if value is None:
            return value

        cleaned: List[str] = []
        for item in value:
            normalized = item.strip().lower()
            if normalized not in SUPPORTED_FOCUS:
                raise ValueError(
                    f"Unsupported focus '{item}'. Supported: {sorted(SUPPORTED_FOCUS)}"
                )
            cleaned.append(normalized)
        return cleaned


class BatchFileRequest(BaseModel):
    """Single file payload for batch review."""

    path: str = Field(..., min_length=1, max_length=500)
    code: str = Field(..., min_length=1, max_length=MAX_CODE_LENGTH)
    language: str = Field(default="python")

    @field_validator("language")
    @classmethod
    def validate_language(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized not in SUPPORTED_LANGUAGES:
            raise ValueError(
                f"Unsupported language '{value}'. Supported: {sorted(SUPPORTED_LANGUAGES)}"
            )
        return normalized


class BatchReviewRequest(BaseModel):
    """Batch review request payload."""

    files: List[BatchFileRequest] = Field(..., min_length=1, max_length=MAX_BATCH_FILES)
    focus: Optional[List[str]] = None

    @field_validator("focus")
    @classmethod
    def validate_focus(cls, value: Optional[List[str]]) -> Optional[List[str]]:
        if value is None:
            return value

        cleaned: List[str] = []
        for item in value:
            normalized = item.strip().lower()
            if normalized not in SUPPORTED_FOCUS:
                raise ValueError(
                    f"Unsupported focus '{item}'. Supported: {sorted(SUPPORTED_FOCUS)}"
                )
            cleaned.append(normalized)
        return cleaned


class BatchReviewItem(BaseModel):
    """Single batch review item result."""

    path: str
    language: str
    result: AnalysisResult


class BatchMetrics(BaseModel):
    """Batch review metrics."""

    files_reviewed: int
    total_issues: int


class BatchReviewResponse(BaseModel):
    """Batch review response."""

    summary: str
    results: List[BatchReviewItem]
    metrics: BatchMetrics


provider = os.getenv("LLM_PROVIDER", "anthropic")
llm = get_llm_client(provider)
analyzer = CodeAnalyzer(llm)

app = FastAPI(
    title="AI Code Review Bot",
    description="Automated code review API with structured findings",
    version="2.0.0",
)

allowed_origins = [origin.strip() for origin in os.getenv("ALLOWED_ORIGINS", "*").split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

review_limiter = SlidingWindowRateLimiter(
    max_requests=int(os.getenv("REVIEW_RATE_LIMIT_PER_MINUTE", "20")),
    window_seconds=60,
)
webhook_limiter = SlidingWindowRateLimiter(
    max_requests=int(os.getenv("WEBHOOK_RATE_LIMIT_PER_MINUTE", "30")),
    window_seconds=60,
)
processed_deliveries: Deque[str] = deque(maxlen=2000)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log request duration and status with request id."""
    request_id = request.headers.get("X-Request-Id", str(uuid.uuid4()))
    request.state.request_id = request_id
    start = time.time()

    response = await call_next(request)
    latency_ms = (time.time() - start) * 1000
    logger.info(
        "request_completed method=%s path=%s status=%s latency_ms=%.2f request_id=%s",
        request.method,
        request.url.path,
        response.status_code,
        latency_ms,
        request_id,
    )
    response.headers["X-Request-Id"] = request_id
    return response


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Consistent HTTP exception format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "path": request.url.path,
            "request_id": getattr(request.state, "request_id", None),
        },
    )


@app.exception_handler(Exception)
async def unexpected_exception_handler(request: Request, exc: Exception):
    """Fallback exception handler."""
    logger.exception("Unhandled exception", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "status_code": 500,
            "path": request.url.path,
            "request_id": getattr(request.state, "request_id", None),
        },
    )


def _review_api_key() -> str:
    key = os.getenv("REVIEW_API_KEY")
    if not key:
        raise HTTPException(
            status_code=500,
            detail="Server missing REVIEW_API_KEY configuration",
        )
    return key


def _webhook_secret() -> str:
    secret = os.getenv("WEBHOOK_SECRET_KEY")
    if not secret:
        raise HTTPException(
            status_code=500,
            detail="Server missing WEBHOOK_SECRET_KEY configuration",
        )
    return secret


def verify_github_signature(payload: bytes, signature_header: str, secret: str) -> bool:
    """Validate GitHub signature using HMAC SHA-256."""
    if not signature_header:
        return False

    try:
        algo, signature = signature_header.split("=", 1)
    except ValueError:
        return False

    if algo != "sha256":
        return False

    expected = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


async def require_api_key(x_api_key: Optional[str] = Header(default=None, alias="X-API-Key")) -> None:
    """Require API key for manual review endpoints."""
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key header")

    if not hmac.compare_digest(x_api_key, _review_api_key()):
        raise HTTPException(status_code=401, detail="Invalid API key")


def _check_review_rate_limit(identity: str) -> None:
    if not review_limiter.allow(identity):
        raise HTTPException(status_code=429, detail="Rate limit exceeded for review endpoint")


@app.post("/review", response_model=AnalysisResult, dependencies=[Depends(require_api_key)])
async def review_code(request: ReviewRequest, raw_request: Request):
    """Review one code snippet and return structured feedback."""
    client_id = raw_request.headers.get("X-Client-Id") or raw_request.headers.get("X-API-Key", "unknown")
    _check_review_rate_limit(client_id)

    try:
        return analyzer.analyze(request.code, request.language, request.focus)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=f"LLM provider error: {exc}") from exc
    except ValueError as exc:
        raise HTTPException(status_code=502, detail=f"Invalid model response: {exc}") from exc


@app.post("/review/batch", response_model=BatchReviewResponse, dependencies=[Depends(require_api_key)])
async def review_batch(request: BatchReviewRequest, raw_request: Request):
    """Review multiple files in a single request."""
    client_id = raw_request.headers.get("X-Client-Id") or raw_request.headers.get("X-API-Key", "unknown")
    _check_review_rate_limit(client_id)

    total_size = sum(len(item.code) for item in request.files)
    if total_size > MAX_BATCH_TOTAL_LENGTH:
        raise HTTPException(
            status_code=413,
            detail=f"Batch payload too large. Max total size is {MAX_BATCH_TOTAL_LENGTH} chars",
        )

    results: List[BatchReviewItem] = []
    total_issues = 0
    for item in request.files:
        try:
            analysis = analyzer.analyze(item.code, item.language, request.focus)
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=f"LLM provider error: {exc}") from exc
        except ValueError as exc:
            raise HTTPException(status_code=502, detail=f"Invalid model response: {exc}") from exc

        total_issues += len(analysis.issues)
        results.append(BatchReviewItem(path=item.path, language=item.language, result=analysis))

    return BatchReviewResponse(
        summary=f"Reviewed {len(results)} files with {total_issues} total issues.",
        results=results,
        metrics=BatchMetrics(files_reviewed=len(results), total_issues=total_issues),
    )


@app.post("/webhook/github")
async def github_webhook(request: Request):
    """Receive GitHub webhooks and validate signatures."""
    payload_bytes = await request.body()
    signature_header = request.headers.get("X-Hub-Signature-256", "")
    delivery_id = request.headers.get("X-GitHub-Delivery", "")
    event = request.headers.get("X-GitHub-Event", "")

    if not verify_github_signature(payload_bytes, signature_header, _webhook_secret()):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")

    if delivery_id and delivery_id in processed_deliveries:
        return {"status": "ignored", "reason": "duplicate_delivery", "delivery_id": delivery_id}

    try:
        payload = json.loads(payload_bytes.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail="Invalid webhook JSON payload") from exc

    repository = payload.get("repository", {}).get("full_name", "unknown")
    if not webhook_limiter.allow(repository):
        raise HTTPException(status_code=429, detail="Rate limit exceeded for webhook")

    if event != "pull_request":
        return {"status": "ignored", "reason": "unsupported_event", "event": event}

    action = payload.get("action")
    if action not in SUPPORTED_PR_ACTIONS:
        return {
            "status": "ignored",
            "reason": "unsupported_action",
            "event": event,
            "action": action,
        }

    pr_number = payload.get("pull_request", {}).get("number")
    if not pr_number:
        raise HTTPException(status_code=400, detail="Missing pull request number in payload")

    if delivery_id:
        processed_deliveries.append(delivery_id)

    logger.info(
        "webhook_received event=%s action=%s repository=%s pr=%s delivery_id=%s",
        event,
        action,
        repository,
        pr_number,
        delivery_id,
    )

    return {
        "status": "accepted",
        "event": event,
        "action": action,
        "repository": repository,
        "pull_request": pr_number,
        "delivery_id": delivery_id,
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "provider": provider,
        "supported_languages": sorted(SUPPORTED_LANGUAGES),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
