from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class LLMClient(ABC):
    """Abstract base class for LLM clients."""

    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Send a chat completion request."""
        pass

class OpenAIClient(LLMClient):
    def __init__(self, model: str = "gpt-4o"):
        from openai import OpenAI
        self.client = OpenAI()
        self.model = model

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content

class AnthropicClient(LLMClient):
    def __init__(self, model: str = "claude-3-5-sonnet-20241022"):
        from anthropic import Anthropic
        self.client = Anthropic()
        self.model = model

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        # Anthropic uses 'system' separately
        system = None
        filtered_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system = msg["content"]
            else:
                filtered_messages.append(msg)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=kwargs.get("max_tokens", 4096),
            system=system,
            messages=filtered_messages
        )
        return response.content[0].text

class GoogleClient(LLMClient):
    """Google Generative AI client (Gemini)."""

    def __init__(self, model: str = "gemini-3-flash-preview"):
        import google.generativeai as genai
        api_key = os.getenv("GOOGLE_API_KEY")
        print(f"Using Google API Key: {'****' + api_key[-4:] if api_key else 'None'}")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

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
        response = self.model.generate_content(prompt)
        return response.text
    
class GroqClient(LLMClient):
    """
    Groq client - FASTEST FREE INFERENCE.

    Free tier: 30 RPM for Llama 3.1 70B
    Signup: https://console.groq.com/
    """

    def __init__(self, model: str = "llama-3.3-70b-versatile"):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("Install openai: pip install openai")

        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable not set")

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        self._model_name = model

    @property
    def model_name(self) -> str:
        return self._model_name

    def chat(self, messages: List[Dict]) -> str:
        """Send messages using OpenAI-compatible API."""
        response = self.client.chat.completions.create(
            model=self._model_name,
            messages=messages,
            max_tokens=4096
        )
        return response.choices[0].message.content

class OllamaClient(LLMClient):
    """
    Ollama client - COMPLETELY FREE/LOCAL.

    No API key needed, runs on your machine.
    Install: https://ollama.ai/
    Then: ollama pull llama3.1:8b
    """

    def __init__(self, model: str = "llama3.1:8b", base_url: str = "http://localhost:11434/v1"):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("Install openai: pip install openai")

        self.client = OpenAI(
            api_key="ollama",  # Required but not used
            base_url=base_url
        )
        self._model_name = model

    @property
    def model_name(self) -> str:
        return self._model_name

    def chat(self, messages: List[Dict]) -> str:
        """Send messages to local Ollama server."""
        response = self.client.chat.completions.create(
            model=self._model_name,
            messages=messages
        )
        return response.choices[0].message.content

def get_llm_client(provider: str = "anthropic") -> LLMClient:
    """Factory function to get the appropriate LLM client."""
    providers = {
        "openai": OpenAIClient,
        "anthropic": AnthropicClient,
        "google": GoogleClient,
        "groq": GroqClient,
        "ollama": OllamaClient
    }

    if provider not in providers:
        raise ValueError(f"Unknown provider: {provider}. Choose from: {list(providers.keys())}")

    return providers[provider]()

# Usage example
# if __name__ == "__main__":
#     client = get_llm_client("ollama")  # or "openai"

#     messages = [
#         {"role": "system", "content": "You are a helpful coding assistant."},
#         {"role": "user", "content": "Write a function to reverse a string."}
#     ]

#     response = client.chat(messages)
#     print(response)