"""LLM client abstraction for Code Analyzer."""
import os
from abc import ABC, abstractmethod
from typing import List, Dict


class LLMClient(ABC):
    """Abstract base class for LLM clients."""

    @abstractmethod
    def chat(self, messages: List[Dict[str, str]]) -> str:
        """Send messages and return response content."""
        pass


def _timeout_seconds() -> float:
    """Return configured LLM timeout in seconds."""
    raw_timeout = os.getenv("LLM_TIMEOUT_SECONDS", "30")
    try:
        timeout = float(raw_timeout)
    except ValueError as exc:
        raise ValueError("LLM_TIMEOUT_SECONDS must be numeric") from exc
    if timeout <= 0:
        raise ValueError("LLM_TIMEOUT_SECONDS must be greater than 0")
    return timeout


class AnthropicClient(LLMClient):
    """Anthropic Claude client."""

    def __init__(self, model: str = "claude-3-5-sonnet-20241022"):
        from anthropic import Anthropic
        self.client = Anthropic(timeout=_timeout_seconds())
        self.model = model

    def chat(self, messages: List[Dict[str, str]]) -> str:
        system = None
        filtered = []
        for m in messages:
            if m["role"] == "system":
                system = m["content"]
            else:
                filtered.append(m)

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=system,
                messages=filtered
            )
            return response.content[0].text
        except Exception as exc:
            raise RuntimeError(f"Anthropic request failed: {exc}") from exc


class OpenAIClient(LLMClient):
    """OpenAI client."""

    def __init__(self, model: str = "gpt-4o"):
        from openai import OpenAI
        self.client = OpenAI(timeout=_timeout_seconds())
        self.model = model

    def chat(self, messages: List[Dict[str, str]]) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            content = response.choices[0].message.content
            if not content:
                raise RuntimeError("OpenAI returned empty content")
            return content
        except Exception as exc:
            raise RuntimeError(f"OpenAI request failed: {exc}") from exc


class GoogleClient(LLMClient):
    """Google Generative AI client (Gemini)."""

    def __init__(self, model: str = "gemini-3-flash-preview"):
        import google.generativeai as genai
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)
        self.timeout = _timeout_seconds()

    def chat(self, messages: List[Dict[str, str]]) -> str:
        # Extract system and build prompt
        system = ""
        history = []
        user_message = ""

        for m in messages:
            if m["role"] == "system":
                system = m["content"]
            elif m["role"] == "user":
                user_message = m["content"]
            elif m["role"] == "assistant":
                history.append({"role": "model", "parts": [m["content"]]})

        prompt = f"{system}\n\n{user_message}" if system else user_message
        try:
            response = self.model.generate_content(
                prompt,
                request_options={"timeout": self.timeout}
            )
            if not response or not getattr(response, "text", None):
                raise RuntimeError("Google client returned empty response")
            return response.text
        except Exception as exc:
            raise RuntimeError(f"Google request failed: {exc}") from exc


def get_llm_client(provider: str = "anthropic") -> LLMClient:
    """Factory function to create LLM client."""
    providers = {
        "anthropic": AnthropicClient,
        "openai": OpenAIClient,
        "google": GoogleClient,
    }

    if provider not in providers:
        raise ValueError(f"Unknown provider: {provider}. Available: {list(providers.keys())}")

    return providers[provider]()
