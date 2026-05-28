from pydantic_settings import BaseSettings, SettingsConfigDict


class LoggingConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="LOG_")

    level: str = "INFO"
    format: str = "json"
    output_file: str = "logs/workflow_engine.log"
    retention_days: int = 30
    enable_structlog: bool = True
