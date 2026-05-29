from __future__ import annotations
import asyncio
from typing import Optional, Callable, Any
from datetime import datetime, timezone
from croniter import croniter
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class WorkflowScheduler:
    def __init__(self):
        self._scheduled: dict[str, dict] = {}
        self._task: Optional[asyncio.Task] = None
        self._trigger: Optional[Callable[[str, dict], Any]] = None

    def set_trigger(self, trigger: Callable[[str, dict], Any]):
        self._trigger = trigger

    def schedule(self, workflow_id: str, cron_expression: str, config: Optional[dict] = None) -> str:
        schedule_id = f"sched_{workflow_id}"
        cron_iter = croniter(cron_expression, datetime.now(timezone.utc))
        next_run = cron_iter.get_next(datetime)
        self._scheduled[schedule_id] = {
            "workflow_id": workflow_id,
            "cron": cron_expression,
            "cron_iter": cron_iter,
            "next_run": next_run,
            "config": config or {},
            "active": True,
        }
        logger.info(f"Scheduled workflow {workflow_id} with cron {cron_expression}, next run: {next_run.isoformat()}")
        return schedule_id

    def cancel_schedule(self, schedule_id: str) -> bool:
        if schedule_id in self._scheduled:
            self._scheduled[schedule_id]["active"] = False
            logger.info(f"Cancelled schedule {schedule_id}")
            return True
        return False

    def get_scheduled(self) -> list[dict]:
        return [
            {"workflow_id": s["workflow_id"], "cron": s["cron"], "next_run": s["next_run"].isoformat(), "active": s["active"]}
            for s in self._scheduled.values()
        ]

    def get_schedule(self, schedule_id: str) -> Optional[dict]:
        s = self._scheduled.get(schedule_id)
        if not s:
            return None
        return {
            "workflow_id": s["workflow_id"],
            "cron": s["cron"],
            "next_run": s["next_run"].isoformat(),
            "active": s["active"],
        }

    async def start(self):
        if self._task is not None:
            return
        self._task = asyncio.create_task(self._run_loop())
        logger.info("Scheduler background loop started")

    async def stop(self):
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None
            logger.info("Scheduler background loop stopped")

    async def _run_loop(self):
        try:
            while True:
                now = datetime.now(timezone.utc)
                for schedule_id, entry in list(self._scheduled.items()):
                    if not entry["active"]:
                        continue
                    if now >= entry["next_run"]:
                        logger.info(f"Triggering scheduled workflow: {entry['workflow_id']}")
                        if self._trigger:
                            try:
                                await self._trigger(entry["workflow_id"], entry["config"])
                            except Exception as e:
                                logger.error(f"Failed to trigger workflow {entry['workflow_id']}: {e}")
                        entry["cron_iter"].get_next(datetime)
                        entry["next_run"] = entry["cron_iter"].get_current(datetime)
                        logger.info(f"Next run for {entry['workflow_id']}: {entry['next_run'].isoformat()}")
                await asyncio.sleep(15)
        except asyncio.CancelledError:
            logger.info("Scheduler loop cancelled")

    def clear(self):
        self._scheduled.clear()
