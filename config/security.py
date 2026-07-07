"""Security configuration and utilities."""
from typing import Optional
import secrets
from pydantic_settings import BaseSettings, SettingsConfigDict


class SecurityConfig(BaseSettings):
    """Security-related configuration."""
    model_config = SettingsConfigDict(env_file=".env", env_prefix="SECURITY_")

    secret_key: str = secrets.token_urlsafe(32)
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    require_https: bool = True
    cors_origins: list[str] = []
    allowed_hosts: list[str] = ["*"]
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_period: int = 60
    max_upload_size: int = 10 * 1024 * 1024
    password_min_length: int = 12
    password_require_special_chars: bool = True
    enable_api_key_auth: bool = True
    jwt_enabled: bool = True


def get_security_config() -> SecurityConfig:
    """Get security configuration."""
    return SecurityConfig()


def validate_secret_key(secret_key: str) -> bool:
    """Validate that secret key is secure for production."""
    if len(secret_key) < 32:
        return False
    if "change-this" in secret_key.lower():
        return False
    if "secret" in secret_key.lower() and len(secret_key) < 50:
        return False
    return True


def validate_cors_origins(origins: list[str], environment: str) -> bool:
    """Validate CORS origins for production."""
    if environment != "production":
        return True

    if "*" in origins:
        return False

    for origin in origins:
        if not (origin.startswith("http://") or origin.startswith("https://")):
            return False

    return True


def validate_password_strength(password: str, config: SecurityConfig) -> bool:
    """Validate password strength against config requirements."""
    if len(password) < config.password_min_length:
        return False

    if config.password_require_special_chars:
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if not any(char in special_chars for char in password):
            return False

    return True
