from dataclasses import dataclass

import httpx

from app.core.config import get_settings


@dataclass
class LLMResponse:
    text: str
    provider: str
    model: str


class ModelRouter:
    async def complete(self, prompt: str) -> LLMResponse:
        settings = get_settings()
        if settings.offline_mode or settings.llm_provider.lower() == "ollama":
            return await self._complete_ollama(prompt)
        if settings.openai_api_key:
            return await self._complete_openai_compatible(prompt)
        return LLMResponse(
            text="No LLM provider key is configured; deterministic agent fallback was used.",
            provider="fallback",
            model="none",
        )

    async def _complete_openai_compatible(self, prompt: str) -> LLMResponse:
        settings = get_settings()
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {settings.openai_api_key}"},
                json={
                    "model": settings.openai_model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.2,
                },
            )
            response.raise_for_status()
            payload = response.json()
            return LLMResponse(
                text=payload["choices"][0]["message"]["content"],
                provider="openai",
                model=settings.openai_model,
            )

    async def _complete_ollama(self, prompt: str) -> LLMResponse:
        settings = get_settings()
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                f"{settings.ollama_base_url}/api/generate",
                json={"model": settings.ollama_model, "prompt": prompt, "stream": False},
            )
            response.raise_for_status()
            payload = response.json()
            return LLMResponse(
                text=payload.get("response", ""),
                provider="ollama",
                model=settings.ollama_model,
            )

