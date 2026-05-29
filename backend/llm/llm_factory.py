from __future__ import annotations
from typing import Optional, Any
from backend.llm.llm_config import LLMConfigModel
from config import llm_config


class LLMFactory:
    _instances: dict[str, Any] = {}

    @classmethod
    def create(cls, provider: Optional[str] = None, config: Optional[LLMConfigModel] = None):
        from backend.llm.openai_llm import OpenAILLM
        from backend.llm.claude_llm import ClaudeLLM
        from backend.llm.local_llm import LocalLLM

        provider = provider or llm_config.default_provider
        cache_key = f"{provider}:{id(config)}"

        if cache_key in cls._instances:
            return cls._instances[cache_key]

        if provider == "openai":
            instance = OpenAILLM(config)
        elif provider == "anthropic" or provider == "claude":
            instance = ClaudeLLM(config)
        elif provider == "local":
            instance = LocalLLM(config)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

        cls._instances[cache_key] = instance
        return instance

    @classmethod
    def clear_cache(cls):
        cls._instances.clear()
