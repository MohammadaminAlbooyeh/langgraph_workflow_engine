from __future__ import annotations
from typing import Optional
from langchain_openai import ChatOpenAI
from backend.llm.llm_config import LLMConfigModel
from config import llm_config


class OpenAILLM:
    def __init__(self, config: Optional[LLMConfigModel] = None):
        cfg = config or LLMConfigModel(
            provider="openai",
            model=llm_config.openai_model,
            temperature=llm_config.openai_temperature,
            max_tokens=llm_config.openai_max_tokens,
            api_key=llm_config.openai_api_key,
        )
        self._client = ChatOpenAI(
            model=cfg.model,
            temperature=cfg.temperature,
            max_tokens=cfg.max_tokens,
            api_key=cfg.api_key,
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
