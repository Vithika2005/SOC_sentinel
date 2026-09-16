# ai-orchestrator/app/core/llm_client.py
"""
Singleton wrapper around the Anthropic client (your notes: #4 Singleton ->
DB conn, Redis client, Qdrant client -- same idea applies to the LLM client).
Every agent node calls through this instead of constructing its own client.
"""
import ollama
from app.config import settings


class LLMClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = ollama.Client(host=settings.ollama_base_url)
            cls._instance.model = settings.ollama_model
        return cls._instance

    def complete_json(self, system: str, user: str, max_tokens: int = 1024) -> str:
        response = self.client.chat(
            model=self.model,
            format="json",
            options={"num_predict": max_tokens, "temperature": 0},
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        return response["message"]["content"]


llm_client = LLMClient()