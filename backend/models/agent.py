from __future__ import annotations
from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel, Field


class AgentCapability(str, Enum):
    REASONING = "reasoning"
    PLANNING = "planning"
    CODING = "coding"
    RESEARCH = "research"
    ANALYSIS = "analysis"
    CREATIVE = "creative"
    TOOL_USE = "tool_use"
    CONVERSATION = "conversation"


class AgentConfig(BaseModel):
    provider: str = "openai"
    model: str = "gpt-4-turbo-preview"
    temperature: float = 0.7
    max_tokens: int = 4096
    system_prompt: Optional[str] = None
    capabilities: list[AgentCapability] = Field(default_factory=list)
    max_retries: int = 3
    timeout: int = 60
    tools: list[str] = Field(default_factory=list)


class Agent(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    config: AgentConfig = Field(default_factory=AgentConfig)
    is_active: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)
