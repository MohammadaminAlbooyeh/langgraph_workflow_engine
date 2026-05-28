from pydantic import BaseModel
from typing import Optional


class LLMConfigModel(BaseModel):
    provider: str = "openai"
    model: str = "gpt-4-turbo-preview"
    temperature: float = 0.7
    max_tokens: int = 4096
    api_key: Optional[str] = None
    endpoint: Optional[str] = None
