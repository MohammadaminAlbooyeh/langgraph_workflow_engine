from __future__ import annotations
from typing import Any, Optional
from backend.langgraph_engine.supervision.approval_manager import ApprovalManager
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class HumanInLoop:
    def __init__(self):
        self._approval_manager = ApprovalManager()

    @property
    def approval_manager(self):
        return self._approval_manager

    async def request_input(self, execution_id: str, node_id: str, prompt: str, schema: Optional[dict] = None) -> str:
        approval_id = self._approval_manager.request_approval(execution_id, node_id, {
            "prompt": prompt,
            "schema": schema or {},
            "type": "input_request",
        })
        logger.info(f"Human input requested: {approval_id}")
        return approval_id

    async def submit_input(self, approval_id: str, user: str, data: dict) -> bool:
        return await self._approval_manager.approve(approval_id, user)

    async def pause_for_review(self, execution_id: str, node_id: str, context: dict) -> str:
        approval_id = self._approval_manager.request_approval(execution_id, node_id, {
            **context,
            "type": "review_pause",
        })
        logger.info(f"Workflow paused for review: {approval_id}")
        return approval_id
