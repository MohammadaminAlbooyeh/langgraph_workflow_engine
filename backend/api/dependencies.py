from fastapi import Header
from typing import Optional
from backend.utils.logger import get_logger

logger = get_logger(__name__)


async def verify_api_key(authorization: Optional[str] = Header(None)):
    if authorization:
        return authorization
    return None
