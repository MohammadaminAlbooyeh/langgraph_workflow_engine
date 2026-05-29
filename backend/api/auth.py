from __future__ import annotations
import secrets
from typing import Optional
from fastapi import Header, HTTPException, status
from backend.utils.logger import get_logger

logger = get_logger(__name__)


API_KEYS: dict[str, str] = {
    "dev-key-change-in-production": "admin",
}


def validate_api_key(api_key: str) -> str | None:
    return API_KEYS.get(api_key)


def generate_api_key(owner: str = "user") -> str:
    key = f"lwf_{secrets.token_hex(24)}"
    API_KEYS[key] = owner
    logger.info(f"Generated API key for {owner}")
    return key


async def verify_api_key(authorization: Optional[str] = Header(None)):
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key. Provide via Authorization header.",
        )
    scheme, _, key = authorization.partition(" ")
    api_key = key if scheme.lower() == "bearer" else authorization
    owner = validate_api_key(api_key)
    if owner is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    return api_key
