from pydantic import BaseModel, Field
from typing import Any, Optional
from backend.models.node import Node, NodeType, NodeConfig


class BaseNode(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    config: NodeConfig = Field(default_factory=NodeConfig)
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    async def execute(self, inputs: dict[str, Any], context: Optional[dict] = None) -> dict[str, Any]:
        raise NotImplementedError("Subclasses must implement execute")

    def to_node_model(self) -> Node:
        return Node(
            id=self.id,
            type=self._get_node_type(),
            name=self.name,
            description=self.description,
            config=self.config,
            inputs=self.inputs,
            outputs=self.outputs,
            metadata=self.metadata,
        )

    def _get_node_type(self) -> NodeType:
        return NodeType.CUSTOM
