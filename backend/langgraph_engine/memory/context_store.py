from __future__ import annotations
from typing import Any, Optional
from datetime import datetime, timezone


class ContextStore:
    def __init__(self):
        self._store: dict[str, dict] = {}

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        self._store[key] = {
            "value": value,
            "timestamp": datetime.now(timezone.utc),
            "ttl": ttl,
        }

    def get(self, key: str, default: Any = None) -> Any:
        entry = self._store.get(key)
        if entry is None:
            return default
        if entry["ttl"]:
            age = (datetime.now(timezone.utc) - entry["timestamp"]).total_seconds()
            if age > entry["ttl"]:
                del self._store[key]
                return default
        return entry["value"]

    def delete(self, key: str) -> bool:
        return self._store.pop(key, None) is not None

    def exists(self, key: str) -> bool:
        return self.get(key) is not None

    def clear(self):
        self._store.clear()

    def keys(self) -> list[str]:
        return list(self._store.keys())
