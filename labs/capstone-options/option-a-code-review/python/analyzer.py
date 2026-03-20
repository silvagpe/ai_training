"""Code Analyzer implementation."""
import json
from typing import Optional, List, Literal

from pydantic import BaseModel, Field, ValidationError

from prompts import (
    CODE_REVIEW_SYSTEM,
    USER_REVIEW_PROMPT_TEMPLATE,
    SECURITY_FOCUS_PROMPT,
    PERFORMANCE_FOCUS_PROMPT,
    build_focus_instruction,
)
from llm_client import LLMClient


class Issue(BaseModel):
    """Represents a code issue."""
    severity: Literal["critical", "high", "medium", "low"]
    line: Optional[int] = None
    category: Literal["bug", "security", "performance", "style", "maintainability"]
    description: str
    suggestion: str


class Metrics(BaseModel):
    """Code quality metrics."""
    overall_score: int = Field(ge=1, le=10)
    complexity: Literal["low", "medium", "high"]
    maintainability: Literal["poor", "fair", "good", "excellent"]


class AnalysisResult(BaseModel):
    """Structured analysis result."""
    summary: str
    issues: List[Issue]
    suggestions: List[str]
    metrics: Metrics


class CodeAnalyzer:
    """LLM-powered code analyzer."""

    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
        self.system_prompt = CODE_REVIEW_SYSTEM

    def analyze(
        self,
        code: str,
        language: str = "python",
        focus: Optional[List[str]] = None,
    ) -> AnalysisResult:
        """Analyze code and return structured result."""
        user_prompt = USER_REVIEW_PROMPT_TEMPLATE.format(
            language=language,
            code=code,
            focus_instruction=build_focus_instruction(focus),
        )

        response = self.llm.chat([
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ])

        return self._parse_response(response)

    def analyze_security(self, code: str, language: str = "python") -> AnalysisResult:
        """Security-focused analysis."""
        user_prompt = USER_REVIEW_PROMPT_TEMPLATE.format(
            language=language,
            code=code,
            focus_instruction=SECURITY_FOCUS_PROMPT,
        )

        response = self.llm.chat([
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ])

        return self._parse_response(response)

    def analyze_performance(self, code: str, language: str = "python") -> AnalysisResult:
        """Performance-focused analysis."""
        user_prompt = USER_REVIEW_PROMPT_TEMPLATE.format(
            language=language,
            code=code,
            focus_instruction=PERFORMANCE_FOCUS_PROMPT,
        )

        response = self.llm.chat([
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ])

        return self._parse_response(response)

    @staticmethod
    def _extract_json_payload(response: str) -> str:
        """Extract JSON payload from plain text or fenced markdown response."""
        cleaned = response.strip()
        if cleaned.startswith("{") and cleaned.endswith("}"):
            return cleaned

        if "```json" in cleaned:
            return cleaned.split("```json", 1)[1].split("```", 1)[0].strip()

        if "```" in cleaned:
            return cleaned.split("```", 1)[1].split("```", 1)[0].strip()

        return cleaned

    def _parse_response(self, response: str) -> AnalysisResult:
        """Parse LLM response into structured result."""
        payload = self._extract_json_payload(response)

        try:
            data = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise ValueError("Model returned invalid JSON") from exc

        try:
            return AnalysisResult(**data)
        except ValidationError as exc:
            raise ValueError("Model response does not match expected schema") from exc
