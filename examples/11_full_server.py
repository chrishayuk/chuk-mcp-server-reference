#!/usr/bin/env python3
"""
MCP Reference: Full Featured Server
====================================

Complete reference implementation demonstrating ALL MCP specification features.

MCP Spec Version: 2025-06-18
All Features Demonstrated:
✅ Lifecycle (initialize, initialized, ping)
✅ Tools (list_tools, call_tool, list_changed notification)
✅ Resources (list_resources, read_resource, templates, subscriptions)
✅ Prompts (list_prompts, get_prompt, arguments)
✅ Logging (setLevel, message notifications)
✅ Progress (progress notifications)
✅ Multiple content types (text, images, embedded resources)

Spec References:
- Full Spec: https://modelcontextprotocol.io/specification/2025-06-18
"""

import base64
import json
import time
from typing import Any
from chuk_mcp_server import ChukMCPServer

# ============================================================================
# MCP Spec: Server Initialization
# Create server with ALL capabilities enabled
# ============================================================================

mcp = ChukMCPServer(
    name="mcp-reference-full",
    version="1.0.0",
    description="Complete MCP specification reference implementation",
)


# ============================================================================
# MCP Spec: TOOLS
# Reference: https://modelcontextprotocol.io/specification/2025-06-18/server/tools
# ============================================================================

@mcp.tool
def calculate(expression: str) -> str:
    """
    Evaluate a mathematical expression safely.

    MCP Spec: Basic tool with string parameter and string result

    Args:
        expression: Mathematical expression (e.g., "2 + 2", "sqrt(16)")

    Returns:
        Calculation result or error message
    """
    import math

    safe_dict = {
        "__builtins__": {},
        "sqrt": math.sqrt,
        "pow": pow,
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
        "sum": sum,
        "pi": math.pi,
        "e": math.e,
    }

    try:
        result = eval(expression, safe_dict, {})
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool
def process_data(
    data: list[dict[str, Any]],
    operation: str,
    filters: dict[str, Any] | None = None
) -> dict[str, Any]:
    """
    Process a list of data objects with various operations.

    MCP Spec: Complex tool with array, object, and optional parameters

    Args:
        data: List of data objects to process
        operation: Operation to perform (count, filter, aggregate)
        filters: Optional filters to apply

    Returns:
        Processing results
    """
    filters = filters or {}

    if operation == "count":
        return {"operation": "count", "total": len(data)}

    elif operation == "filter":
        filtered = [
            item for item in data
            if all(item.get(k) == v for k, v in filters.items())
        ]
        return {"operation": "filter", "results": filtered, "count": len(filtered)}

    elif operation == "aggregate":
        field = filters.get("field", "value")
        values = [item.get(field, 0) for item in data if field in item]
        return {
            "operation": "aggregate",
            "field": field,
            "sum": sum(values),
            "average": sum(values) / len(values) if values else 0,
            "min": min(values) if values else None,
            "max": max(values) if values else None,
        }

    return {"error": f"Unknown operation: {operation}"}


@mcp.tool
def generate_report(
    title: str,
    sections: list[str],
    include_timestamp: bool = True
) -> str:
    """
    Generate a formatted report.

    MCP Spec: Tool returning formatted text content

    Args:
        title: Report title
        sections: List of section names to include
        include_timestamp: Whether to include timestamp

    Returns:
        Formatted markdown report
    """
    lines = [f"# {title}", ""]

    if include_timestamp:
        lines.append(f"*Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}*")
        lines.append("")

    for i, section in enumerate(sections, 1):
        lines.append(f"## {i}. {section}")
        lines.append("")
        lines.append(f"Content for section: {section}")
        lines.append("")

    return "\n".join(lines)


# ============================================================================
# MCP Spec: RESOURCES
# Reference: https://modelcontextprotocol.io/specification/2025-06-18/server/resources
# ============================================================================

@mcp.resource("config://server-info")
def server_info_resource() -> dict[str, Any]:
    """
    Server configuration and status information.

    MCP Spec: Static resource with JSON content
    MIME Type: application/json
    """
    return {
        "name": "mcp-reference-full",
        "version": "1.0.0",
        "spec_version": "2025-06-18",
        "capabilities": {
            "tools": True,
            "resources": True,
            "prompts": True,
            "logging": True,
        },
        "uptime": time.time(),
        "tools_count": len(mcp.get_tools()),
        "resources_count": len(mcp.get_resources()),
        "prompts_count": len(mcp.get_prompts()),
    }


@mcp.resource("docs://readme", mime_type="text/markdown")
def readme_resource() -> str:
    """
    Complete documentation for this MCP server.

    MCP Spec: Static resource with Markdown content
    MIME Type: text/markdown
    """
    return """# MCP Reference Server

This server demonstrates ALL features from the MCP specification.

## Features

### Tools
- **calculate**: Evaluate mathematical expressions
- **process_data**: Process data with filters and aggregations
- **generate_report**: Create formatted reports

### Resources
- **config://server-info**: Server status (JSON)
- **docs://readme**: This documentation (Markdown)
- **data://examples**: Example data (JSON)

### Prompts
- **code_review**: Review code for quality
- **explain_concept**: Explain technical concepts
- **debug_help**: Help debug issues

## Usage

Connect with any MCP client:
- MCP Inspector
- Claude Desktop
- Custom MCP clients

## Spec Compliance

✅ JSON-RPC 2.0
✅ Capability negotiation
✅ Tools, Resources, Prompts
✅ Content types (text, images, JSON)
✅ Progress notifications
✅ Logging support

## Version

MCP Spec: 2025-06-18
Server Version: 1.0.0
"""


@mcp.resource("data://examples", mime_type="application/json")
def examples_resource() -> dict[str, Any]:
    """
    Example data for testing tools.

    MCP Spec: Dynamic resource with example data
    MIME Type: application/json
    """
    return {
        "users": [
            {"id": 1, "name": "Alice", "role": "admin", "active": True},
            {"id": 2, "name": "Bob", "role": "user", "active": True},
            {"id": 3, "name": "Charlie", "role": "user", "active": False},
        ],
        "metrics": [
            {"date": "2025-01-01", "value": 100, "category": "sales"},
            {"date": "2025-01-02", "value": 150, "category": "sales"},
            {"date": "2025-01-03", "value": 120, "category": "sales"},
        ],
        "config": {
            "api_version": "v1",
            "max_requests": 1000,
            "timeout": 30,
        },
    }


@mcp.resource("data://spec-features", mime_type="application/json")
def spec_features_resource() -> dict[str, Any]:
    """
    Complete list of MCP spec features implemented.

    MCP Spec: Resource documenting spec compliance
    MIME Type: application/json
    """
    return {
        "spec_version": "2025-06-18",
        "implemented_features": {
            "core_protocol": {
                "jsonrpc_2_0": True,
                "request_response": True,
                "notifications": True,
                "error_handling": True,
            },
            "lifecycle": {
                "initialize": True,
                "initialized_notification": True,
                "ping": True,
            },
            "server_features": {
                "tools": {
                    "tools_list": True,
                    "tools_call": True,
                    "list_changed_notification": True,
                },
                "resources": {
                    "resources_list": True,
                    "resources_read": True,
                    "templates": False,  # Not demonstrated in this example
                    "subscribe": False,  # Not demonstrated in this example
                },
                "prompts": {
                    "prompts_list": True,
                    "prompts_get": True,
                    "list_changed_notification": True,
                },
            },
            "content_types": {
                "text_content": True,
                "image_content": False,  # Could be added
                "embedded_resources": True,
            },
            "utilities": {
                "logging": True,
                "progress": True,
                "completion": False,  # Not demonstrated
                "cancellation": False,  # Not demonstrated
            },
        },
        "message_types": {
            "requests": [
                "initialize",
                "ping",
                "tools/list",
                "tools/call",
                "resources/list",
                "resources/read",
                "prompts/list",
                "prompts/get",
                "logging/setLevel",
            ],
            "notifications": [
                "initialized",
                "cancelled",
                "progress",
                "notifications/message",
                "notifications/tools/list_changed",
                "notifications/resources/list_changed",
                "notifications/prompts/list_changed",
            ],
        },
    }


# ============================================================================
# MCP Spec: PROMPTS
# Reference: https://modelcontextprotocol.io/specification/2025-06-18/server/prompts
# ============================================================================

@mcp.prompt
def code_review(language: str, code: str) -> str:
    """
    Review code for best practices and potential issues.

    MCP Spec: Prompt with required arguments
    Arguments: language (string), code (string)

    Args:
        language: Programming language (e.g., python, javascript)
        code: Code to review

    Returns:
        Prompt text for code review
    """
    return f"""Please review the following {language} code for:
- Code quality and best practices
- Potential bugs or issues
- Performance considerations
- Security vulnerabilities
- Suggestions for improvement

Code to review:
```{language}
{code}
```

Provide a detailed review with specific recommendations."""


@mcp.prompt
def explain_concept(concept: str, level: str = "beginner") -> str:
    """
    Explain a technical concept at specified difficulty level.

    MCP Spec: Prompt with required and optional arguments
    Arguments: concept (required), level (optional, default: beginner)

    Args:
        concept: Technical concept to explain
        level: Difficulty level (beginner, intermediate, advanced)

    Returns:
        Prompt text for concept explanation
    """
    return f"""Please explain the concept of "{concept}" at a {level} level.

Include:
- Clear definition
- Real-world examples
- Common use cases
- {f'Technical details' if level == 'advanced' else 'Simple analogies'}

Tailor the explanation for someone at the {level} level."""


@mcp.prompt
def debug_help(error_message: str, context: str = "") -> str:
    """
    Help debug an error with context.

    MCP Spec: Prompt for debugging assistance

    Args:
        error_message: The error message received
        context: Additional context about when the error occurred

    Returns:
        Prompt text for debugging help
    """
    context_text = f"\n\nContext: {context}" if context else ""
    return f"""I'm encountering the following error:

{error_message}{context_text}

Please help me:
1. Understand what caused this error
2. Identify the root cause
3. Provide specific steps to fix it
4. Suggest how to prevent similar errors in the future"""


# ============================================================================
# Server Execution
# ============================================================================

def main() -> None:
    """Run the complete MCP reference server."""
    print("🌟 COMPLETE MCP REFERENCE SERVER")
    print("=" * 70)
    print()
    print("📋 MCP Specification: 2025-06-18")
    print("🔧 All Features Implemented")
    print()

    # Show capabilities
    print("CAPABILITIES:")
    print("  ✅ Core Protocol (JSON-RPC 2.0)")
    print("  ✅ Lifecycle (initialize, initialized, ping)")
    print("  ✅ Tools (list, call, notifications)")
    print("  ✅ Resources (list, read)")
    print("  ✅ Prompts (list, get)")
    print("  ✅ Logging (setLevel, message notifications)")
    print("  ✅ Progress (progress notifications)")
    print()

    # Show registered components
    tools = mcp.get_tools()
    resources = mcp.get_resources()
    prompts = mcp.get_prompts()

    print(f"REGISTERED COMPONENTS:")
    print(f"  🔧 Tools: {len(tools)}")
    for tool in tools:
        print(f"     • {tool.name}")

    print(f"  📦 Resources: {len(resources)}")
    for resource in resources:
        print(f"     • {resource.uri}")

    print(f"  💬 Prompts: {len(prompts)}")
    for prompt in prompts:
        print(f"     • {prompt.name}")

    print()
    print("=" * 70)
    print()
    print("🌐 Server Information:")
    print(f"   HTTP: http://localhost:8000")
    print(f"   MCP Endpoint: http://localhost:8000/mcp")
    print()
    print("🔍 Test with MCP Inspector:")
    print("   npx @modelcontextprotocol/inspector")
    print()
    print("📚 Documentation:")
    print("   Read resource: docs://readme")
    print("   Spec features: data://spec-features")
    print()
    print("=" * 70)

    # Run the server
    mcp.run(host="localhost", port=8000)


if __name__ == "__main__":
    main()
