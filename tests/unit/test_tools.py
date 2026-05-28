import pytest
from backend.langgraph_engine.tools.built_in_tools import BuiltInTools
from backend.langgraph_engine.tools.custom_tools import CustomTools
from backend.langgraph_engine.tools.tool_registry import ToolRegistry


def test_built_in_tools_list():
    tools = BuiltInTools.list_tools()
    assert len(tools) > 0
    names = [t["name"] for t in tools]
    assert "current_datetime" in names
    assert "calculate" in names
    assert "format_text" in names


def test_built_in_calculate():
    result = BuiltInTools.execute("calculate", expression="2 + 2")
    assert result == 4


def test_built_in_format_text():
    result = BuiltInTools.execute("format_text", text="Hello World", case="upper")
    assert result == "HELLO WORLD"
    result = BuiltInTools.execute("format_text", text="Hello World", case="lower")
    assert result == "hello world"


def test_built_in_datetime():
    result = BuiltInTools.execute("current_datetime")
    assert isinstance(result, str)


def test_built_in_tool_not_found():
    with pytest.raises(ValueError):
        BuiltInTools.execute("nonexistent")


def test_custom_tools_register_and_execute():
    ct = CustomTools()
    ct.register("greet", lambda name: f"Hello {name}!", "Greets a person")
    result = ct.execute("greet", **{"name": "World"})
    assert result == "Hello World!"


def test_custom_tools_list():
    ct = CustomTools()
    ct.register("test_fn", lambda: True, "A test")
    tools = ct.list_tools()
    assert any(t["name"] == "test_fn" for t in tools)


def test_custom_tools_unregister():
    ct = CustomTools()
    ct.register("temp", lambda: None)
    assert ct.unregister("temp") is True
    assert ct.unregister("temp") is False


def test_tool_registry():
    reg = ToolRegistry()
    tools = reg.list_tools()
    assert len(tools) > 0
    result = reg.execute("calculate", expression="3 * 4")
    assert result == 12


def test_tool_registry_get_tool():
    reg = ToolRegistry()
    tool = reg.get_tool("calculate")
    assert tool is not None
    assert tool["name"] == "calculate"


def test_tool_registry_custom():
    reg = ToolRegistry()
    reg.register_custom("double", lambda x: x * 2, "Doubles a number", [{"name": "x", "type": "number"}])
    result = reg.execute("double", x=5)
    assert result == 10
