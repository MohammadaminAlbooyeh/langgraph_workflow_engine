from __future__ import annotations
from typing import Any, Optional
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class WorkflowScheduler:
    def __init__(self):
        self._scheduled: dict[str, dict] = {}

    def schedule(self, workflow_id: str, cron_expression: str, config: Optional[dict] = None) -> str:
        schedule_id = f"sched_{workflow_id}"
        self._scheduled[schedule_id] = {
            "workflow_id": workflow_id,
            "cron": cron_expression,
            "config": config or {},
            "active": True,
        }
        logger.info(f"Scheduled workflow {workflow_id} with cron {cron_expression}")
        return schedule_id

    def cancel_schedule(self, schedule_id: str) -> bool:
        if schedule_id in self._scheduled:
            self._scheduled[schedule_id]["active"] = False
            logger.info(f"Cancelled schedule {schedule_id}")
            return True
        return False

    def get_scheduled(self) -> list[dict]:
        return [s for s in self._scheduled.values() if s["active"]]

    def get_schedule(self, schedule_id: str) -> Optional[dict]:
        return self._scheduled.get(schedule_id)

    def clear(self):
        self._scheduled.clear()
