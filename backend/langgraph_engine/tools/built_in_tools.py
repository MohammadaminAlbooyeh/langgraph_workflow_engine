from __future__ import annotations
import ast
import operator
from typing import Any
from datetime import datetime, timezone


def current_datetime() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_eval(expression: str) -> float:
    allowed_ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.Mod: operator.mod,
        ast.FloorDiv: operator.floordiv,
    }

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant: {node.value}")
        elif isinstance(node, ast.UnaryOp):
            return allowed_ops[type(node.op)](_eval(node.operand))
        elif isinstance(node, ast.BinOp):
            return allowed_ops[type(node.op)](_eval(node.left), _eval(node.right))
        else:
            raise ValueError(f"Unsupported expression: {type(node).__name__}")

    parsed = ast.parse(expression, mode="eval")
    return _eval(parsed.body)


def calculate(expression: str) -> float:
    return _safe_eval(expression)


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
