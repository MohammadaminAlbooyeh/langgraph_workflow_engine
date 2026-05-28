from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="DB_")

    url: str = "sqlite+aiosqlite:///./data/workflow_engine.db"
    pool_size: int = 10
    max_overflow: int = 20
    echo: bool = False
    migrate: bool = True
