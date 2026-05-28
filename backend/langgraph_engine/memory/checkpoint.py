from __future__ import annotations
from typing import Any, Optional
from datetime import datetime, timezone
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class CheckpointManager:
    def __init__(self):
        self._checkpoints: dict[str, list[dict]] = {}

    def save_checkpoint(self, execution_id: str, state: dict[str, Any], label: Optional[str] = None) -> str:
        checkpoint_id = f"cp_{execution_id}_{len(self._checkpoints.get(execution_id, []))}"
        checkpoint = {
            "id": checkpoint_id,
            "execution_id": execution_id,
            "state": state.copy(),
            "label": label or f"checkpoint_{datetime.now(timezone.utc).isoformat()}",
            "timestamp": datetime.now(timezone.utc),
        }
        self._checkpoints.setdefault(execution_id, []).append(checkpoint)
        logger.info(f"Saved checkpoint {checkpoint_id} for execution {execution_id}")
        return checkpoint_id

    def restore_checkpoint(self, execution_id: str, checkpoint_id: str) -> Optional[dict]:
        checkpoints = self._checkpoints.get(execution_id, [])
        for cp in checkpoints:
            if cp["id"] == checkpoint_id:
                logger.info(f"Restored checkpoint {checkpoint_id}")
                return cp["state"].copy()
        return None

    def list_checkpoints(self, execution_id: str) -> list[dict]:
        return self._checkpoints.get(execution_id, [])

    def clear(self, execution_id: str):
        self._checkpoints.pop(execution_id, None)

    def clear_all(self):
        self._checkpoints.clear()
