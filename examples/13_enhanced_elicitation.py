#!/usr/bin/env python3
"""
MCP Reference: Enhanced Elicitation (2025-11-25)
=================================================

⚠️  REFERENCE IMPLEMENTATION - NOT YET FUNCTIONAL
This demonstrates how enhanced elicitation SHOULD work per MCP 2025-11-25.
Currently, these features are documented in docstrings only.
Actual elicitation modes require chuk-mcp-server and MCP client updates.

MCP Spec Version: 2025-11-25
Reference Features:
- URL mode elicitation (documented in docstrings)
- Titled/untitled enums (shown in docstrings with descriptions)
- Single-select enums (parameter documentation)
- Multi-select enums (list[] parameters with option docs)
- Default values for primitives (Python defaults - this works!)

Spec References:
- URL Elicitation: SEP-1036
- Enhanced Enums: SEP-1330
- Default Values: SEP-1034
- JSON Schema 2020-12: SEP-1613

STATUS: Default values work! Other features need chuk-mcp-server to expose
        them in the JSON Schema for tools. This shows the intended API.
"""

from typing import Any
from chuk_mcp_server import ChukMCPServer

mcp = ChukMCPServer(
    name="enhanced-elicitation-reference",
    version="1.0.0",
    description="Demonstrates enhanced elicitation features from MCP 2025-11-25",
)


# ============================================================================
# MCP Spec 2025-11-25: Enhanced Enum Support
# New: Titled/untitled, single/multi-select enums (SEP-1330)
# ============================================================================

@mcp.tool
def configure_server(
    log_level: str,
    features: list[str],
    theme: str = "auto",
) -> dict[str, Any]:
    """
    Configure server with enhanced enum elicitation.

    MCP Spec 2025-11-25: Demonstrates:
    - Titled enum (log_level with descriptions)
    - Multi-select enum (features - can select multiple)
    - Single-select with default (theme)

    Args:
        log_level: Logging level (titled enum with descriptions)
            - debug: "Verbose debugging information"
            - info: "General informational messages"
            - warning: "Warning messages for potential issues"
            - error: "Error messages for failures"

        features: Features to enable (multi-select)
            Options: ["caching", "compression", "monitoring", "analytics"]

        theme: UI theme (single-select with default)
            Options: ["light", "dark", "auto"]
            Default: "auto"

    Returns:
        Configuration status
    """
    return {
        "log_level": log_level,
        "features_enabled": features,
        "theme": theme,
        "status": "configured",
    }


# ============================================================================
# MCP Spec 2025-11-25: URL Mode Elicitation (SEP-1036)
# New: Elicit URLs from users with validation
# ============================================================================

@mcp.tool
def fetch_webpage(url: str) -> dict[str, Any]:
    """
    Fetch content from a webpage.

    MCP Spec 2025-11-25: URL mode elicitation
    When eliciting this parameter, clients should:
    - Show URL input field
    - Validate URL format
    - Support https:// and http:// schemes

    Args:
        url: Webpage URL (URL elicitation mode)
            Format: https://example.com/path
            Validation: Must be valid HTTP(S) URL

    Returns:
        Webpage metadata
    """
    # Simulated fetch
    return {
        "url": url,
        "title": f"Page at {url}",
        "content_length": 1024,
        "status": "fetched",
    }


@mcp.tool
def subscribe_feed(
    feed_url: str,
    notification_url: str | None = None,
) -> dict[str, Any]:
    """
    Subscribe to RSS/Atom feed.

    MCP Spec 2025-11-25: Multiple URL elicitation
    Demonstrates eliciting multiple URLs in one tool.

    Args:
        feed_url: RSS/Atom feed URL (required)
        notification_url: Webhook URL for notifications (optional)

    Returns:
        Subscription status
    """
    result: dict[str, Any] = {
        "feed_url": feed_url,
        "subscribed": True,
    }

    if notification_url:
        result["notifications"] = notification_url

    return result


# ============================================================================
# MCP Spec 2025-11-25: Default Values for Primitives (SEP-1034)
# New: String, number, and enum defaults in elicitation
# ============================================================================

@mcp.tool
def create_project(
    name: str,
    description: str = "A new project",  # String default
    max_size_mb: int = 100,  # Number default
    visibility: str = "private",  # Enum default
) -> dict[str, Any]:
    """
    Create a new project with smart defaults.

    MCP Spec 2025-11-25: Default values for elicitation
    Clients should pre-populate fields with defaults.

    Args:
        name: Project name (required, no default)
        description: Project description (default: "A new project")
        max_size_mb: Maximum size in MB (default: 100)
        visibility: Project visibility (default: "private")
            Options: ["public", "private", "internal"]

    Returns:
        Created project info
    """
    return {
        "name": name,
        "description": description,
        "max_size_mb": max_size_mb,
        "visibility": visibility,
        "created": True,
    }


# ============================================================================
# MCP Spec 2025-11-25: Untitled Enums
# New: Enums without titles (simple list of values)
# ============================================================================

@mcp.tool
def set_priority(
    task_id: str,
    priority: str,
) -> dict[str, Any]:
    """
    Set task priority.

    MCP Spec 2025-11-25: Untitled enum (simple values)
    Just a list of values without descriptions.

    Args:
        task_id: Task identifier
        priority: Priority level
            Values: ["low", "medium", "high", "critical"]
            (Untitled enum - no descriptions needed)

    Returns:
        Updated task
    """
    return {
        "task_id": task_id,
        "priority": priority,
        "updated": True,
    }


# ============================================================================
# MCP Spec 2025-11-25: Complex Elicitation Example
# Combining multiple new features
# ============================================================================

@mcp.tool
def deploy_application(
    app_url: str,  # URL mode
    environment: str = "staging",  # Enum with default
    regions: list[str] = None,  # Multi-select with default
    notification_webhook: str | None = None,  # Optional URL
    enable_monitoring: bool = True,  # Boolean with default
) -> dict[str, Any]:
    """
    Deploy an application with enhanced elicitation.

    MCP Spec 2025-11-25: Demonstrates multiple new features together:
    - URL mode elicitation
    - Enum with default value
    - Multi-select with defaults
    - Optional URL
    - Boolean with default

    Args:
        app_url: Application repository URL (required URL)
        environment: Deployment environment (default: "staging")
            Options: ["development", "staging", "production"]

        regions: Regions to deploy to (multi-select, default: ["us-west"])
            Options: ["us-west", "us-east", "eu-west", "ap-south"]

        notification_webhook: Webhook for deployment notifications (optional URL)

        enable_monitoring: Enable monitoring (default: True)

    Returns:
        Deployment status
    """
    if regions is None:
        regions = ["us-west"]

    result: dict[str, Any] = {
        "app_url": app_url,
        "environment": environment,
        "regions": regions,
        "monitoring": enable_monitoring,
        "status": "deploying",
    }

    if notification_webhook:
        result["webhook"] = notification_webhook

    return result


# ============================================================================
# Server Execution
# ============================================================================

def main() -> None:
    """Run the enhanced elicitation reference server."""
    print("✨ Enhanced Elicitation MCP Reference Server")
    print("=" * 70)
    print()
    print("MCP Spec: 2025-11-25 (New Features)")
    print()
    print("New Elicitation Features:")
    print("  🔗 URL mode elicitation (SEP-1036)")
    print("  📋 Titled/untitled enums (SEP-1330)")
    print("  ✅ Single-select enums")
    print("  ☑️  Multi-select enums")
    print("  🎯 Default values for primitives (SEP-1034)")
    print()

    tools = mcp.get_tools()
    print(f"🔧 Tools Demonstrating Enhanced Elicitation ({len(tools)}):")
    print()

    demos = {
        "configure_server": "Titled enums + multi-select + defaults",
        "fetch_webpage": "URL mode elicitation",
        "subscribe_feed": "Multiple URL fields",
        "create_project": "Default values (string, number, enum)",
        "set_priority": "Untitled enum (simple list)",
        "deploy_application": "All features combined",
    }

    for tool in tools:
        if tool.name in demos:
            print(f"   • {tool.name}")
            print(f"     → {demos[tool.name]}")

    print()
    print("=" * 70)
    print()
    print("These features improve user experience when eliciting input:")
    print("  • URLs validated and formatted correctly")
    print("  • Enums with helpful descriptions")
    print("  • Multi-select for multiple choices")
    print("  • Smart defaults reduce user input")
    print()
    print("Running on http://localhost:8000")
    print("MCP endpoint: http://localhost:8000/mcp")
    print()

    mcp.run(host="localhost", port=8000)


if __name__ == "__main__":
    main()
