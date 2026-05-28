from pydantic_settings import BaseSettings, SettingsConfigDict


class LangraphConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="GRAPH_")

    max_iterations: int = 100
    max_concurrent_nodes: int = 10
    default_timeout: int = 300
    checkpoint_interval: int = 10
    enable_tracing: bool = True
    recursion_limit: int = 50
