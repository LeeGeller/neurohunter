"""Ollama LLM client."""

import httpx


class OllamaClient:
    """Client for interacting with the Ollama LLM API."""

    def __init__(self, base_url: str, model: str) -> None:
        """Initialize the OllamaClient with the base URL and model name."""
        self.base_url = base_url
        self.model = model
        self.client = httpx.AsyncClient()

    async def generate(self, promt: str) -> str:
        """Generate text using the Ollama LLM API."""

        payload = {
            "model": self.model,
            "prompt": promt,
            "stream": False,
        }

        response = await self.client.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timout=120.0
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]

    async def close(self) -> None:
        """Close the HTTP client."""
        await self.client.aclose()
