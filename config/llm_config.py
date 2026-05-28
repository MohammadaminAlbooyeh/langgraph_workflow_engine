from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class LLMConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="LLM_")

    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4-turbo-preview"
    openai_temperature: float = 0.7
    openai_max_tokens: int = 4096

    anthropic_api_key: Optional[str] = None
    anthropic_model: str = "claude-3-opus-20240229"
    anthropic_temperature: float = 0.7
    anthropic_max_tokens: int = 4096

    local_endpoint: Optional[str] = None
    local_model: Optional[str] = None
    local_temperature: float = 0.7
    local_max_tokens: int = 2048

    default_provider: str = "openai"
