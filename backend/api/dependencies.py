from fastapi import Depends
from backend.api.auth import verify_api_key as _verify_api_key

verify_api_key = Depends(_verify_api_key)
