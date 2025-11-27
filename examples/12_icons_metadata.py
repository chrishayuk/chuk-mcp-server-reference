#!/usr/bin/env python3
"""
MCP Reference: Icons and Metadata (2025-11-25)
================================================

⚠️  REFERENCE IMPLEMENTATION - NOT YET FUNCTIONAL
This demonstrates how icons SHOULD work per MCP 2025-11-25 spec.
Currently, icons are embedded in docstrings and emoji responses only.
Actual icon metadata fields require chuk-mcp-server updates.

MCP Spec Version: 2025-11-25
Reference Features:
- Icons for tools (shown via emojis in docstrings)
- Icons for resources (shown via emojis in responses)
- Icons for prompts (shown via emojis in output)
- Implementation description field (works - server has description)

Spec References:
- Icons: https://modelcontextprotocol.io/specification/2025-11-25 (SEP-973)

STATUS: Icons are currently text/emoji only. The spec defines icon fields
        that chuk-mcp-server doesn't yet support. This shows the intended API.
"""

from typing import Any
from chuk_mcp_server import ChukMCPServer

# ============================================================================
# MCP Spec 2025-11-25: Server with Implementation Description
# New: description field in Implementation interface
# ============================================================================

mcp = ChukMCPServer(
    name="icons-metadata-reference",
    version="1.0.0",
    description="MCP server demonstrating icons and metadata features from 2025-11-25 specification",
)


# ============================================================================
# MCP Spec 2025-11-25: Tools with Icons
# New: icon field in Tool definition
# ============================================================================

# Note: chuk-mcp-server may not yet support icon parameter
# This demonstrates the intended usage per spec

@mcp.tool
def calculator(expression: str) -> str:
    """
    Calculate mathematical expressions.

    Icon: 🧮 (U+1F9EE ABACUS)

    MCP Spec 2025-11-25: Tools can now include icon metadata
    Icons help users visually identify tools in MCP clients.

    Args:
        expression: Math expression to evaluate

    Returns:
        Calculation result
    """
    import math

    safe_dict = {
        "__builtins__": {},
        "sqrt": math.sqrt,
        "pow": pow,
        "abs": abs,
        "pi": math.pi,
        "e": math.e,
    }

    try:
        result = eval(expression, safe_dict, {})
        return f"🧮 {expression} = {result}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


@mcp.tool
def search_web(query: str, max_results: int = 5) -> dict[str, Any]:
    """
    Search the web for information.

    Icon: 🔍 (U+1F50D LEFT-POINTING MAGNIFYING GLASS)

    MCP Spec 2025-11-25: Visual icon improves UX

    Args:
        query: Search query
        max_results: Maximum number of results

    Returns:
        Search results
    """
    # Simulated search results
    return {
        "icon": "🔍",
        "query": query,
        "results": [
            {
                "title": f"Result {i+1} for '{query}'",
                "url": f"https://example.com/result-{i+1}",
                "snippet": f"This is result {i+1} about {query}",
            }
            for i in range(max_results)
        ],
    }


@mcp.tool
def send_email(to: str, subject: str, body: str) -> dict[str, Any]:
    """
    Send an email message.

    Icon: 📧 (U+1F4E7 E-MAIL)

    MCP Spec 2025-11-25: Email icon clearly indicates purpose

    Args:
        to: Recipient email address
        subject: Email subject
        body: Email body

    Returns:
        Send status
    """
    return {
        "icon": "📧",
        "status": "sent",
        "to": to,
        "subject": subject,
        "message_id": f"<msg-{hash(to + subject)}>",
    }


@mcp.tool
def create_document(title: str, content: str, format: str = "markdown") -> dict[str, Any]:
    """
    Create a new document.

    Icon: 📄 (U+1F4C4 PAGE FACING UP)

    MCP Spec 2025-11-25: Document icon for file operations

    Args:
        title: Document title
        content: Document content
        format: Document format (markdown, html, text)

    Returns:
        Created document info
    """
    return {
        "icon": "📄",
        "title": title,
        "format": format,
        "size": len(content),
        "created": True,
    }


# ============================================================================
# MCP Spec 2025-11-25: Resources with Icons
# New: icon field in Resource definition
# ============================================================================

@mcp.resource("config://settings", mime_type="application/json")
def settings_resource() -> dict[str, Any]:
    """
    Server configuration settings.

    Icon: ⚙️ (U+2699 GEAR)

    MCP Spec 2025-11-25: Gear icon indicates configuration
    """
    return {
        "icon": "⚙️",
        "name": "Server Settings",
        "settings": {
            "max_requests": 1000,
            "timeout": 30,
            "debug": False,
        },
    }


@mcp.resource("data://users", mime_type="application/json")
def users_resource() -> dict[str, Any]:
    """
    User directory.

    Icon: 👥 (U+1F465 BUSTS IN SILHOUETTE)

    MCP Spec 2025-11-25: People icon for user data
    """
    return {
        "icon": "👥",
        "users": [
            {"id": 1, "name": "Alice", "role": "admin"},
            {"id": 2, "name": "Bob", "role": "user"},
            {"id": 3, "name": "Charlie", "role": "user"},
        ],
    }


@mcp.resource("docs://api-reference", mime_type="text/markdown")
def api_docs_resource() -> str:
    """
    API documentation.

    Icon: 📚 (U+1F4DA BOOKS)

    MCP Spec 2025-11-25: Books icon for documentation
    """
    return """# API Reference 📚

## Endpoints

### Calculator API
- Icon: 🧮
- Calculate math expressions

### Search API
- Icon: 🔍
- Search the web

### Email API
- Icon: 📧
- Send emails

### Documents API
- Icon: 📄
- Create and manage documents
"""


@mcp.resource("stats://server", mime_type="application/json")
def stats_resource() -> dict[str, Any]:
    """
    Server statistics.

    Icon: 📊 (U+1F4CA BAR CHART)

    MCP Spec 2025-11-25: Chart icon for statistics
    """
    import time

    return {
        "icon": "📊",
        "uptime": time.time(),
        "requests_total": 12345,
        "requests_per_second": 42,
        "tools_count": len(mcp.get_tools()),
        "resources_count": len(mcp.get_resources()),
    }


# ============================================================================
# MCP Spec 2025-11-25: Prompts with Icons
# New: icon field in Prompt definition
# ============================================================================

@mcp.prompt
def code_review(language: str, code: str) -> str:
    """
    Review code for quality and best practices.

    Icon: 🔍 (U+1F50D LEFT-POINTING MAGNIFYING GLASS)

    MCP Spec 2025-11-25: Magnifying glass for code review

    Args:
        language: Programming language
        code: Code to review

    Returns:
        Code review prompt
    """
    return f"""🔍 Code Review Request

Language: {language}

Please review the following code for:
- Code quality and best practices
- Potential bugs
- Performance issues
- Security concerns

Code:
```{language}
{code}
```

Provide specific recommendations for improvement.
"""


@mcp.prompt
def write_tests(code: str, framework: str = "pytest") -> str:
    """
    Generate unit tests for code.

    Icon: 🧪 (U+1F9EA TEST TUBE)

    MCP Spec 2025-11-25: Test tube for testing prompts

    Args:
        code: Code to test
        framework: Testing framework

    Returns:
        Test generation prompt
    """
    return f"""🧪 Unit Test Generation

Framework: {framework}

Please generate comprehensive unit tests for:

```python
{code}
```

Include:
- Happy path tests
- Edge cases
- Error handling
- Mock external dependencies
"""


@mcp.prompt
def debug_error(error_message: str, code_context: str) -> str:
    """
    Help debug an error.

    Icon: 🐛 (U+1F41B BUG)

    MCP Spec 2025-11-25: Bug icon for debugging

    Args:
        error_message: The error message
        code_context: Code where error occurred

    Returns:
        Debugging prompt
    """
    return f"""🐛 Debug Assistant

Error: {error_message}

Context:
```
{code_context}
```

Please help:
1. Identify the root cause
2. Explain why this error occurred
3. Provide a fix
4. Suggest how to prevent similar errors
"""


# ============================================================================
# Server Execution
# ============================================================================

def main() -> None:
    """Run the icons and metadata reference server."""
    print("🎨 Icons and Metadata MCP Reference Server")
    print("=" * 70)
    print()
    print("MCP Spec: 2025-11-25 (New Features)")
    print()
    print("New in 2025-11-25:")
    print("  ✨ Icons for tools (visual identification)")
    print("  ✨ Icons for resources (better UX)")
    print("  ✨ Icons for prompts (clearer purpose)")
    print("  ✨ Implementation description field")
    print()

    tools = mcp.get_tools()
    resources = mcp.get_resources()
    prompts = mcp.get_prompts()

    print(f"🔧 Tools with Icons ({len(tools)}):")
    for tool in tools:
        # Extract icon from docstring (示范 - actual implementation would add icon field)
        icon = "🔧"  # Default
        if "calculator" in tool.name:
            icon = "🧮"
        elif "search" in tool.name:
            icon = "🔍"
        elif "email" in tool.name:
            icon = "📧"
        elif "document" in tool.name:
            icon = "📄"
        print(f"   {icon} {tool.name}")

    print()
    print(f"📦 Resources with Icons ({len(resources)}):")
    for resource in resources:
        icon = "📦"  # Default
        if "settings" in resource.uri:
            icon = "⚙️"
        elif "users" in resource.uri:
            icon = "👥"
        elif "docs" in resource.uri:
            icon = "📚"
        elif "stats" in resource.uri:
            icon = "📊"
        print(f"   {icon} {resource.uri}")

    print()
    print(f"💬 Prompts with Icons ({len(prompts)}):")
    for prompt in prompts:
        icon = "💬"  # Default
        if "review" in prompt.name:
            icon = "🔍"
        elif "test" in prompt.name:
            icon = "🧪"
        elif "debug" in prompt.name:
            icon = "🐛"
        print(f"   {icon} {prompt.name}")

    print()
    print("=" * 70)
    print()
    print("Note: Icon support depends on chuk-mcp-server updates.")
    print("This example demonstrates the intended usage per MCP 2025-11-25.")
    print("Icons are currently embedded in responses and documentation.")
    print()
    print("Running on http://localhost:8000")
    print("MCP endpoint: http://localhost:8000/mcp")
    print()

    mcp.run(host="localhost", port=8000)


if __name__ == "__main__":
    main()
