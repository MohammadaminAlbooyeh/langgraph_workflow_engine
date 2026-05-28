from __future__ import annotations
from typing import Optional
from langchain_community.chat_models import ChatOpenAI
from backend.llm.llm_config import LLMConfigModel
from config import llm_config


class LocalLLM:
    def __init__(self, config: Optional[LLMConfigModel] = None):
        cfg = config or LLMConfigModel(
            provider="local",
            model=llm_config.local_model or "local-model",
            temperature=llm_config.local_temperature,
            max_tokens=llm_config.local_max_tokens,
            endpoint=llm_config.local_endpoint,
        )
        self._client = ChatOpenAI(
            model=cfg.model,
            temperature=cfg.temperature,
            max_tokens=cfg.max_tokens,
            base_url=cfg.endpoint,
            api_key="not-needed",
        )

    @property
    def client(self):
        return self._client

    async def invoke(self, messages: list[dict], **kwargs) -> str:
        response = await self._client.ainvoke(messages, **kwargs)
        return response.content

    async def stream(self, messages: list[dict], **kwargs):
        async for chunk in self._client.astream(messages, **kwargs):
            yield chunk.content
