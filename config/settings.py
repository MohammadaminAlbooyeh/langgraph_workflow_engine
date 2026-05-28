from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_")

    app_name: str = "LangGraph Workflow Engine"
    app_version: str = "0.1.0"
    debug: bool = False
    environment: str = "development"
    secret_key: str = "change-me-in-production"
    allowed_origins: list[str] = ["*"]
    api_prefix: str = "/api/v1"
    host: str = "0.0.0.0"
    port: int = 8000
