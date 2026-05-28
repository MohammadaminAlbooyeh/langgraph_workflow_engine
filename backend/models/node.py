from __future__ import annotations
from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel, Field


class NodeType(str, Enum):
    AGENT = "agent"
    LLM = "llm"
    INPUT = "input"
    OUTPUT = "output"
    DECISION = "decision"
    ROUTER = "router"
    CONDITIONAL = "conditional"
    LOOP = "loop"
    SWITCH = "switch"
    TRANSFORMER = "transformer"
    VALIDATOR = "validator"
    TEXT_PROCESSOR = "text_processor"
    CUSTOM = "custom"
    AGGREGATE = "aggregate"
    MERGE = "merge"
    COMBINE = "combine"


class NodeConfig(BaseModel):
    provider: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    prompt_template: Optional[str] = None
    system_prompt: Optional[str] = None
    input_schema: Optional[dict[str, Any]] = None
    output_schema: Optional[dict[str, Any]] = None
    timeout: Optional[int] = None
    retry_count: int = 3
    retry_delay: int = 1
    custom_attributes: dict[str, Any] = Field(default_factory=dict)


class Node(BaseModel):
    id: str
    type: NodeType
    name: str
    description: Optional[str] = None
    config: NodeConfig = Field(default_factory=NodeConfig)
    position: dict[str, float] = Field(default_factory=lambda: {"x": 0.0, "y": 0.0})
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
