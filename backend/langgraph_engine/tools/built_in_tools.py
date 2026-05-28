from __future__ import annotations
from typing import Any
from datetime import datetime


def current_datetime() -> str:
    return datetime.utcnow().isoformat()


def calculate(expression: str) -> float:
    safe_globals = {"__builtins__": {}}
    safe_locals = {}
    return eval(expression, safe_globals, safe_locals)


def format_text(text: str, case: str = "lower") -> str:
    if case == "upper":
        return text.upper()
    elif case == "lower":
        return text.lower()
    elif case == "title":
        return text.title()
    return text


class BuiltInTools:
    _tools = {
        "current_datetime": {
            "name": "current_datetime",
            "description": "Get the current UTC date and time",
            "handler": current_datetime,
            "parameters": [],
        },
        "calculate": {
            "name": "calculate",
            "description": "Evaluate a mathematical expression",
            "handler": calculate,
            "parameters": [
                {"name": "expression", "type": "string", "description": "Math expression", "required": True},
            ],
        },
        "format_text": {
            "name": "format_text",
            "description": "Format text to upper/lower/title case",
            "handler": format_text,
            "parameters": [
                {"name": "text", "type": "string", "description": "Input text", "required": True},
                {"name": "case", "type": "string", "description": "Case: upper/lower/title", "required": False, "default": "lower"},
            ],
        },
    }

    @classmethod
    def list_tools(cls) -> list[dict]:
        return list(cls._tools.values())

    @classmethod
    def get_tool(cls, name: str) -> dict | None:
        return cls._tools.get(name)

    @classmethod
    def execute(cls, name: str, **kwargs) -> Any:
        tool = cls._tools.get(name)
        if not tool:
            raise ValueError(f"Built-in tool '{name}' not found")
        return tool["handler"](**kwargs)
