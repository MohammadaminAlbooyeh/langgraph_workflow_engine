from __future__ import annotations
from typing import Any, Optional
from backend.utils.exceptions import InvalidGraphError


def validate_workflow(workflow_data: dict) -> list[str]:
    errors = []
    if not workflow_data.get("name"):
        errors.append("Workflow name is required")
    if "nodes" in workflow_data and not isinstance(workflow_data["nodes"], list):
        errors.append("Nodes must be a list")
    if "edges" in workflow_data and not isinstance(workflow_data["edges"], list):
        errors.append("Edges must be a list")
    return errors


def validate_node_config(config: Optional[dict]) -> list[str]:
    errors = []
    if config is None:
        return errors
    if config.get("temperature") is not None:
        temp = config["temperature"]
        if not isinstance(temp, (int, float)) or not 0 <= temp <= 2:
            errors.append("Temperature must be between 0 and 2")
    if config.get("max_tokens") is not None:
        if not isinstance(config["max_tokens"], int) or config["max_tokens"] < 1:
            errors.append("max_tokens must be a positive integer")
    if config.get("retry_count") is not None:
        if not isinstance(config["retry_count"], int) or config["retry_count"] < 0:
            errors.append("retry_count must be a non-negative integer")
    return errors


def validate_edge_condition(condition: Optional[dict]) -> list[str]:
    errors = []
    if condition is None:
        return errors
    if "field" not in condition:
        errors.append("Condition must have a 'field' property")
    if "operator" in condition:
        valid_ops = {"equals", "not_equals", "contains", "gt", "gte", "lt", "lte", "in", "matches", "exists"}
        if condition["operator"] not in valid_ops:
            errors.append(f"Invalid operator: {condition['operator']}. Valid: {valid_ops}")
    return errors
