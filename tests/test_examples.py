#!/usr/bin/env python3
"""
Tests for MCP Reference Server Examples

Validates that all examples are working correctly and comply with MCP spec.
"""

import importlib.util
import sys
from pathlib import Path


def load_example_module(example_name: str):
    """Load an example module dynamically."""
    example_path = Path(__file__).parent.parent / "examples" / example_name
    spec = importlib.util.spec_from_file_location(example_name, example_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load {example_name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[example_name] = module
    spec.loader.exec_module(module)
    return module


class TestMinimalExample:
    """Test the minimal example (01_minimal.py)."""

    def test_minimal_server_exists(self):
        """Test that minimal example can be loaded."""
        module = load_example_module("01_minimal.py")
        assert hasattr(module, "mcp")
        assert hasattr(module, "main")

    def test_minimal_has_tools(self):
        """Test that minimal example has registered tools."""
        module = load_example_module("01_minimal.py")
        tools = module.mcp.get_tools()
        assert len(tools) >= 1
        assert any(tool.name == "hello" for tool in tools)

    def test_minimal_tool_hello(self):
        """Test the hello tool from minimal example."""
        module = load_example_module("01_minimal.py")
        result = module.hello("Test")
        assert "Hello, Test!" in result


class TestBasicToolsExample:
    """Test the basic tools example (02_tools_basic.py)."""

    def test_basic_tools_server_exists(self):
        """Test that basic tools example can be loaded."""
        module = load_example_module("02_tools_basic.py")
        assert hasattr(module, "mcp")
        assert hasattr(module, "main")

    def test_basic_tools_count(self):
        """Test that basic tools example has multiple tools."""
        module = load_example_module("02_tools_basic.py")
        tools = module.mcp.get_tools()
        # Should have many tools demonstrating different parameter types
        assert len(tools) >= 5

    def test_string_tools(self):
        """Test string parameter tools."""
        module = load_example_module("02_tools_basic.py")

        # Test echo
        assert module.echo("test") == "test"

        # Test greet
        assert "Hello, World!" in module.greet("World")
        assert "Hi, Alice!" in module.greet("Alice", "Hi")

    def test_numeric_tools(self):
        """Test numeric parameter tools."""
        module = load_example_module("02_tools_basic.py")

        # Test add
        assert module.add(2, 3) == 5
        assert module.add(-1, 1) == 0

        # Test multiply
        assert module.multiply(3.0, 4.0) == 12.0
        assert module.multiply(2.5, 2.0) == 5.0

    def test_boolean_tools(self):
        """Test boolean parameter tools."""
        module = load_example_module("02_tools_basic.py")

        # Test format_text
        assert module.format_text("hello", uppercase=True) == "HELLO"
        assert module.format_text("hello", reverse=True) == "olleh"
        assert module.format_text("hello", uppercase=True, reverse=True) == "OLLEH"

    def test_array_tools(self):
        """Test array parameter tools."""
        module = load_example_module("02_tools_basic.py")

        # Test sum_numbers
        assert module.sum_numbers([1, 2, 3, 4, 5]) == 15
        assert module.sum_numbers([]) == 0

        # Test join_strings
        assert module.join_strings(["a", "b", "c"]) == "a, b, c"
        assert module.join_strings(["x", "y"], " - ") == "x - y"

    def test_object_tools(self):
        """Test object parameter tools."""
        module = load_example_module("02_tools_basic.py")

        # Test create_user
        result = module.create_user({
            "name": "Alice",
            "email": "alice@example.com",
            "age": 30
        })
        assert "Alice" in result
        assert "alice@example.com" in result

    def test_mixed_parameter_tools(self):
        """Test tools with mixed parameter types."""
        module = load_example_module("02_tools_basic.py")

        # Test advanced_calculator
        result = module.advanced_calculator("sum", [1.0, 2.0, 3.0])
        assert result == 6.0

        result = module.advanced_calculator("average", [2.0, 4.0, 6.0])
        assert result == 4.0

        result = module.advanced_calculator("sum", [1.5, 2.5], round_result=True, decimal_places=0)
        assert result == 4.0


class TestFullServerExample:
    """Test the full server example (11_full_server.py)."""

    def test_full_server_exists(self):
        """Test that full server example can be loaded."""
        module = load_example_module("11_full_server.py")
        assert hasattr(module, "mcp")
        assert hasattr(module, "main")

    def test_full_server_has_tools(self):
        """Test that full server has tools registered."""
        module = load_example_module("11_full_server.py")
        tools = module.mcp.get_tools()
        assert len(tools) >= 1

    def test_full_server_has_resources(self):
        """Test that full server has resources registered."""
        module = load_example_module("11_full_server.py")
        resources = module.mcp.get_resources()
        assert len(resources) >= 1

    def test_full_server_has_prompts(self):
        """Test that full server has prompts registered."""
        module = load_example_module("11_full_server.py")
        prompts = module.mcp.get_prompts()
        assert len(prompts) >= 1

    def test_calculate_tool(self):
        """Test the calculate tool."""
        module = load_example_module("11_full_server.py")
        result = module.calculate("2 + 2")
        assert "4" in result

    def test_process_data_tool(self):
        """Test the process_data tool."""
        module = load_example_module("11_full_server.py")

        # Test count operation
        result = module.process_data([{"a": 1}, {"b": 2}], "count")
        assert result["total"] == 2

    def test_generate_report_tool(self):
        """Test the generate_report tool."""
        module = load_example_module("11_full_server.py")
        result = module.generate_report("Test Report", ["Section 1", "Section 2"])
        assert "Test Report" in result
        assert "Section 1" in result
        assert "Section 2" in result


class TestSpecCompliance:
    """Test MCP specification compliance across examples."""

    def test_all_examples_have_mcp_server(self):
        """Test that all examples have a ChukMCPServer instance."""
        examples = [
            "01_minimal.py",
            "02_tools_basic.py",
            "11_full_server.py",
        ]

        for example in examples:
            module = load_example_module(example)
            assert hasattr(module, "mcp"), f"{example} missing mcp instance"
            assert module.mcp is not None, f"{example} mcp instance is None"

    def test_all_examples_have_main(self):
        """Test that all examples have a main function."""
        examples = [
            "01_minimal.py",
            "02_tools_basic.py",
            "11_full_server.py",
        ]

        for example in examples:
            module = load_example_module(example)
            assert hasattr(module, "main"), f"{example} missing main function"
            assert callable(module.main), f"{example} main is not callable"

    def test_tools_have_descriptions(self):
        """Test that all tools have descriptions (docstrings)."""
        module = load_example_module("11_full_server.py")
        tools = module.mcp.get_tools()

        for tool in tools:
            assert tool.description, f"Tool {tool.name} missing description"
            assert len(tool.description) > 0, f"Tool {tool.name} has empty description"

    def test_tools_have_valid_schemas(self):
        """Test that all tools have valid input schemas."""
        module = load_example_module("02_tools_basic.py")
        tools = module.mcp.get_tools()

        for tool in tools:
            # Tools should have parameters list
            assert hasattr(tool, "parameters"), f"Tool {tool.name} missing parameters"

            # Each parameter should have required attributes
            for param in tool.parameters:
                assert hasattr(param, "name"), f"Parameter missing name in {tool.name}"
                assert hasattr(param, "type"), f"Parameter missing type in {tool.name}"
                assert hasattr(param, "required"), f"Parameter missing required in {tool.name}"
