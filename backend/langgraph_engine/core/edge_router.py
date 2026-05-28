from __future__ import annotations
from typing import Any
from backend.models.edge import Edge, EdgeType, EdgeCondition


class EdgeRouter:
    def evaluate_condition(self, condition: EdgeCondition, state: dict[str, Any]) -> bool:
        field_value = state.get(condition.field)

        if condition.operator == "equals":
            return field_value == condition.value
        elif condition.operator == "not_equals":
            return field_value != condition.value
        elif condition.operator == "contains":
            return str(condition.value) in str(field_value)
        elif condition.operator == "gt":
            return field_value is not None and field_value > condition.value
        elif condition.operator == "gte":
            return field_value is not None and field_value >= condition.value
        elif condition.operator == "lt":
            return field_value is not None and field_value < condition.value
        elif condition.operator == "lte":
            return field_value is not None and field_value <= condition.value
        elif condition.operator == "in":
            return field_value in condition.value if isinstance(condition.value, (list, tuple)) else False
        elif condition.operator == "matches":
            import re
            return bool(re.match(str(condition.value), str(field_value)))
        elif condition.operator == "exists":
            return field_value is not None
        return True

    def route(self, edges: list[Edge], state: dict[str, Any]) -> list[Edge]:
        matching = []
        for edge in sorted(edges, key=lambda e: e.priority, reverse=True):
            if edge.type == EdgeType.DIRECT:
                matching.append(edge)
            elif edge.type == EdgeType.CONDITIONAL and edge.condition:
                if self.evaluate_condition(edge.condition, state):
                    matching.append(edge)
            elif edge.type == EdgeType.DYNAMIC:
                matching.append(edge)
            elif edge.type == EdgeType.EVENT:
                matching.append(edge)
        return matching
