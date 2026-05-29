from __future__ import annotations
from prometheus_client import Counter, Histogram, Gauge, generate_latest, REGISTRY
from fastapi import Response
from backend.utils.logger import get_logger

logger = get_logger(__name__)

workflow_executions_total = Counter(
    "workflow_executions_total",
    "Total number of workflow executions",
    ["status"],
)

workflow_execution_duration = Histogram(
    "workflow_execution_duration_seconds",
    "Duration of workflow executions in seconds",
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0, 120.0],
)

node_executions_total = Counter(
    "node_executions_total",
    "Total number of node executions",
    ["node_type", "status"],
)

node_execution_duration = Histogram(
    "node_execution_duration_seconds",
    "Duration of node executions in seconds",
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0],
)

active_workflows = Gauge(
    "active_workflows",
    "Number of currently active workflows",
)

active_executions = Gauge(
    "active_executions",
    "Number of currently running executions",
)

errors_total = Counter(
    "workflow_errors_total",
    "Total number of workflow errors",
    ["error_type"],
)


async def metrics_endpoint():
    return Response(content=generate_latest(REGISTRY), media_type="text/plain")


def record_workflow_execution(status: str, duration_ms: float):
    workflow_executions_total.labels(status=status).inc()
    workflow_execution_duration.observe(duration_ms / 1000.0)


def record_node_execution(node_type: str, status: str, duration_ms: float):
    node_executions_total.labels(node_type=node_type, status=status).inc()
    node_execution_duration.observe(duration_ms / 1000.0)


def set_active_workflows(count: int):
    active_workflows.set(count)


def set_active_executions(count: int):
    active_executions.set(count)


def record_error(error_type: str):
    errors_total.labels(error_type=error_type).inc()
