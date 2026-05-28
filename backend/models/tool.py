from __future__ import annotations
from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel, Field


class ToolType(str, Enum):
    BUILTIN = "builtin"
    CUSTOM = "custom"
    API = "api"
    DATABASE = "database"
    FILE = "file"
    CODE = "code"


class ToolParameter(BaseModel):
    name: str
    type: str = "string"
    description: Optional[str] = None
    required: bool = True
    default: Any = None


class Tool(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    type: ToolType = ToolType.BUILTIN
    parameters: list[ToolParameter] = Field(default_factory=list)
    handler: Optional[str] = None
    code: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)
