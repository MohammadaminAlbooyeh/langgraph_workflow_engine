from typing import Any, Optional
from backend.langgraph_engine.edges.base_edge import BaseEdge
from backend.models.edge import Edge, EdgeType, EdgeCondition


class ConditionalEdge(BaseEdge):
    condition: EdgeCondition
    alternative_target_id: Optional[str] = None

    def evaluate(self, state: dict[str, Any]) -> str:
        field_value = state.get(self.condition.field)
        if self.condition.operator == "equals":
            result = field_value == self.condition.value
        elif self.condition.operator == "contains":
            result = self.condition.value in str(field_value)
        elif self.condition.operator == "gt":
            result = field_value is not None and field_value > self.condition.value
        elif self.condition.operator == "exists":
            result = field_value is not None
        else:
            result = True

        return self.target_id if result else (self.alternative_target_id or self.target_id)

    def to_edge_model(self) -> Edge:
        return Edge(
            id=self.id,
            source_id=self.source_id,
            target_id=self.target_id,
            type=EdgeType.CONDITIONAL,
            label=self.label,
            condition=self.condition,
            metadata=self.metadata,
        )
