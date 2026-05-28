from __future__ import annotations
from typing import Any
from datetime import datetime
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class MonitoringService:
    def __init__(self):
        self._metrics: dict[str, list] = {
            "workflow_executions": [],
            "node_executions": [],
            "errors": [],
        }

    def record_execution(self, workflow_id: str, duration_ms: float, status: str):
        self._metrics["workflow_executions"].append({
            "workflow_id": workflow_id,
            "duration_ms": duration_ms,
            "status": status,
            "timestamp": datetime.utcnow(),
        })

    def record_node_execution(self, node_id: str, duration_ms: float, status: str):
        self._metrics["node_executions"].append({
            "node_id": node_id,
            "duration_ms": duration_ms,
            "status": status,
            "timestamp": datetime.utcnow(),
        })

    def record_error(self, error_type: str, message: str):
        self._metrics["errors"].append({
            "type": error_type,
            "message": message,
            "timestamp": datetime.utcnow(),
        })

    def get_metrics(self, metric_type: str | None = None) -> dict:
        if metric_type:
            return {metric_type: self._metrics.get(metric_type, [])}
        return self._metrics

    def get_summary(self) -> dict:
        return {
            "total_executions": len(self._metrics["workflow_executions"]),
            "total_errors": len(self._metrics["errors"]),
            "recent_executions": self._metrics["workflow_executions"][-10:],
        }
