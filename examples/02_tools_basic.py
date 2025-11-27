#!/usr/bin/env python3
"""
MCP Reference: Basic Tools
===========================

Demonstrates all basic tool features from the MCP specification.

MCP Spec Version: 2025-06-18
Features Demonstrated:
- Tools with various parameter types (string, int, float, bool)
- Required vs optional parameters
- Default values
- Arrays and objects
- Tool descriptions via docstrings
- Input schema generation

Spec References:
- Tools: https://modelcontextprotocol.io/specification/2025-06-18/server/tools
- JSON Schema: https://json-schema.org/draft/2020-12/schema
"""

from typing import Any
from chuk_mcp_server import ChukMCPServer

mcp = ChukMCPServer(
    name="basic-tools-reference",
    version="1.0.0",
)


# ============================================================================
# MCP Spec: String Parameters
# Tools can accept string parameters with full type safety
# ============================================================================

@mcp.tool
def echo(message: str) -> str:
    """
    Echo a message back.

    MCP Spec: Required string parameter
    Schema: {"type": "string"}

    Args:
        message: The message to echo

    Returns:
        The same message
    """
    return message


@mcp.tool
def greet(name: str, greeting: str = "Hello") -> str:
    """
    Greet someone with a custom greeting.

    MCP Spec: Required and optional string parameters
    Schema: {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "greeting": {"type": "string"}
        },
        "required": ["name"]
    }

    Args:
        name: Person to greet (required)
        greeting: Greeting to use (optional, default: "Hello")

    Returns:
        Personalized greeting
    """
    return f"{greeting}, {name}!"


# ============================================================================
# MCP Spec: Numeric Parameters
# Integer and float parameters with validation
# ============================================================================

@mcp.tool
def add(a: int, b: int) -> int:
    """
    Add two integers.

    MCP Spec: Integer parameters
    Schema: {"type": "integer"} for both parameters

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b
    """
    return a + b


@mcp.tool
def multiply(x: float, y: float) -> float:
    """
    Multiply two numbers.

    MCP Spec: Number (float) parameters
    Schema: {"type": "number"} for both parameters

    Args:
        x: First number
        y: Second number

    Returns:
        Product of x and y
    """
    return x * y


# ============================================================================
# MCP Spec: Boolean Parameters
# Boolean flags for tool behavior
# ============================================================================

@mcp.tool
def format_text(text: str, uppercase: bool = False, reverse: bool = False) -> str:
    """
    Format text with various options.

    MCP Spec: Boolean parameters for flags
    Schema: {"type": "boolean"}

    Args:
        text: Text to format
        uppercase: Convert to uppercase
        reverse: Reverse the text

    Returns:
        Formatted text
    """
    result = text
    if uppercase:
        result = result.upper()
    if reverse:
        result = result[::-1]
    return result


# ============================================================================
# MCP Spec: Array Parameters
# Lists and arrays as tool inputs
# ============================================================================

@mcp.tool
def sum_numbers(numbers: list[int]) -> int:
    """
    Sum a list of numbers.

    MCP Spec: Array parameter
    Schema: {
        "type": "array",
        "items": {"type": "integer"}
    }

    Args:
        numbers: List of integers to sum

    Returns:
        Sum of all numbers
    """
    return sum(numbers)


@mcp.tool
def join_strings(strings: list[str], separator: str = ", ") -> str:
    """
    Join strings with a separator.

    MCP Spec: Array of strings with optional string parameter
    Schema: {
        "type": "array",
        "items": {"type": "string"}
    }

    Args:
        strings: List of strings to join
        separator: Separator to use

    Returns:
        Joined string
    """
    return separator.join(strings)


# ============================================================================
# MCP Spec: Object Parameters
# Dictionaries and complex objects
# ============================================================================

@mcp.tool
def create_user(user_data: dict[str, Any]) -> str:
    """
    Create a user from provided data.

    MCP Spec: Object parameter with properties
    Schema: {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "email": {"type": "string"},
            "age": {"type": "integer"}
        }
    }

    Args:
        user_data: User information dictionary

    Returns:
        Confirmation message
    """
    name = user_data.get("name", "Unknown")
    email = user_data.get("email", "no-email")
    age = user_data.get("age", "unknown")
    return f"Created user: {name} ({email}), age {age}"


# ============================================================================
# MCP Spec: Multiple Parameter Types
# Tools can mix different types
# ============================================================================

@mcp.tool
def advanced_calculator(
    operation: str,
    numbers: list[float],
    round_result: bool = False,
    decimal_places: int = 2
) -> float:
    """
    Perform various calculations on a list of numbers.

    MCP Spec: Mixed parameter types in a single tool
    Demonstrates: string enum-like, array, boolean, integer with defaults

    Args:
        operation: Operation to perform (sum, average, min, max)
        numbers: List of numbers to operate on
        round_result: Whether to round the result
        decimal_places: Number of decimal places if rounding

    Returns:
        Calculation result
    """
    if operation == "sum":
        result = sum(numbers)
    elif operation == "average":
        result = sum(numbers) / len(numbers) if numbers else 0
    elif operation == "min":
        result = min(numbers) if numbers else 0
    elif operation == "max":
        result = max(numbers) if numbers else 0
    else:
        raise ValueError(f"Unknown operation: {operation}")

    if round_result:
        result = round(result, decimal_places)

    return result


# ============================================================================
# MCP Spec: Tool Metadata
# List all registered tools with their schemas
# ============================================================================

@mcp.tool
def list_tool_info() -> dict[str, Any]:
    """
    Get information about all available tools.

    MCP Spec: Introspection tool showing tool metadata
    This helps clients understand available tools programmatically.

    Returns:
        Dictionary with tool information
    """
    tools = mcp.get_tools()
    return {
        "total_tools": len(tools),
        "tools": [
            {
                "name": tool.name,
                "description": tool.description,
                "parameter_count": len(tool.parameters),
                "parameters": [
                    {
                        "name": param.name,
                        "type": param.type,
                        "required": param.required,
                        "description": param.description,
                    }
                    for param in tool.parameters
                ],
            }
            for tool in tools
        ],
    }


# ============================================================================
# Server Execution
# ============================================================================

def main() -> None:
    """Run the basic tools reference server."""
    print("🔧 Basic Tools MCP Reference Server")
    print("=" * 50)
    print()
    print("Demonstrating MCP Spec Tool Features:")
    print("  ✅ String parameters (required/optional)")
    print("  ✅ Integer parameters")
    print("  ✅ Float parameters")
    print("  ✅ Boolean parameters")
    print("  ✅ Array parameters")
    print("  ✅ Object parameters")
    print("  ✅ Mixed parameter types")
    print("  ✅ Default values")
    print("  ✅ Tool introspection")
    print()

    tools = mcp.get_tools()
    print(f"📚 Available Tools ({len(tools)}):")
    for tool in tools:
        param_count = len(tool.parameters)
        print(f"  • {tool.name} ({param_count} parameters)")

    print()
    print("MCP Spec: 2025-06-18 (tools/list, tools/call)")
    print("=" * 50)
    print()
    print("Running on http://localhost:8000")
    print("MCP endpoint: http://localhost:8000/mcp")
    print()

    mcp.run(host="localhost", port=8000)


if __name__ == "__main__":
    main()
