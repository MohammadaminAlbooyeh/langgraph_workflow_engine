from __future__ import annotations
from typing import Any, Optional
from datetime import datetime
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class ApprovalManager:
    def __init__(self):
        self._pending_approvals: dict[str, dict] = {}

    def request_approval(self, execution_id: str, node_id: str, context: Optional[dict] = None) -> str:
        approval_id = f"apr_{execution_id}_{node_id}"
        self._pending_approvals[approval_id] = {
            "id": approval_id,
            "execution_id": execution_id,
            "node_id": node_id,
            "context": context or {},
            "status": "pending",
            "created_at": datetime.utcnow(),
            "decided_at": None,
            "decided_by": None,
        }
        logger.info(f"Approval requested: {approval_id}")
        return approval_id

    async def approve(self, approval_id: str, user: str) -> bool:
        approval = self._pending_approvals.get(approval_id)
        if not approval or approval["status"] != "pending":
            return False
        approval["status"] = "approved"
        approval["decided_at"] = datetime.utcnow()
        approval["decided_by"] = user
        logger.info(f"Approval granted: {approval_id} by {user}")
        return True

    async def reject(self, approval_id: str, user: str, reason: Optional[str] = None) -> bool:
        approval = self._pending_approvals.get(approval_id)
        if not approval or approval["status"] != "pending":
            return False
        approval["status"] = "rejected"
        approval["decided_at"] = datetime.utcnow()
        approval["decided_by"] = user
        approval["reason"] = reason
        logger.info(f"Approval rejected: {approval_id} by {user}")
        return True

    def get_pending(self) -> list[dict]:
        return [a for a in self._pending_approvals.values() if a["status"] == "pending"]

    def get_approval(self, approval_id: str) -> Optional[dict]:
        return self._pending_approvals.get(approval_id)
