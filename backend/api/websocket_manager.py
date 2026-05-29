from __future__ import annotations
import json
import asyncio
from typing import Any, Optional
from fastapi import WebSocket
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class ConnectionManager:
    def __init__(self):
        self._connections: dict[str, list[WebSocket]] = {}

    async def connect(self, workflow_id: str, websocket: WebSocket):
        await websocket.accept()
        self._connections.setdefault(workflow_id, []).append(websocket)
        logger.info(f"WebSocket connected for workflow {workflow_id}")

    def disconnect(self, workflow_id: str, websocket: WebSocket):
        conns = self._connections.get(workflow_id, [])
        if websocket in conns:
            conns.remove(websocket)
        if not self._connections.get(workflow_id):
            self._connections.pop(workflow_id, None)
        logger.info(f"WebSocket disconnected for workflow {workflow_id}")

    async def broadcast(self, workflow_id: str, event_type: str, data: dict[str, Any]):
        conns = self._connections.get(workflow_id, [])
        message = json.dumps({"type": event_type, **data})
        stale = []
        for ws in conns:
            try:
                await ws.send_text(message)
            except Exception:
                stale.append(ws)
        for ws in stale:
            self.disconnect(workflow_id, ws)

    async def broadcast_all(self, event_type: str, data: dict[str, Any]):
        for workflow_id in list(self._connections.keys()):
            await self.broadcast(workflow_id, event_type, data)


manager = ConnectionManager()
