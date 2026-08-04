"""Ollama LLM client."""

import httpx


class OllamaClient:
    """Client for interacting with the Ollama LLM API."""

    def __init__(self, base_url: str, model: str) -> None:
        """Initialize the OllamaClient with the base URL and model name."""
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.client = httpx.AsyncClient()

    async def generate(self, prompt: str) -> str:
        """Generate text using the Ollama LLM API."""

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "think": False,

        }

        response = await self.client.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=120.0
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]

    async def close(self) -> None:
        """Close the HTTP client."""
        await self.client.aclose()


class VacancyFeaturesService:
    """Vacancy features extraction service using Ollama LLM."""

    def __init__(self, llm_client: OllamaClient) -> None:
        self.llm_client = llm_client
