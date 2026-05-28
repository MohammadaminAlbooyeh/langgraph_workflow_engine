from functools import lru_cache
from config import settings, database_config, llm_config, langraph_config, logging_config


@lru_cache
def get_config():
    return {
        "app": settings,
        "database": database_config,
        "llm": llm_config,
        "langraph": langraph_config,
        "logging": logging_config,
    }
