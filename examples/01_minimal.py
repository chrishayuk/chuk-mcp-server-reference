#!/usr/bin/env python3
"""
MCP Reference: Minimal Server
==============================

The simplest possible MCP server demonstrating the bare minimum requirements.

MCP Spec Version: 2025-06-18
Features Demonstrated:
- Initialize/lifecycle
- Single tool definition
- Basic JSON-RPC handling

Spec References:
- Lifecycle: https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle
- Tools: https://modelcontextprotocol.io/specification/2025-06-18/server/tools
"""

from chuk_mcp_server import ChukMCPServer

# Create server instance
# chuk-mcp-server handles all protocol implementation
mcp = ChukMCPServer(
    name="minimal-mcp-server",
    version="1.0.0",
)


# ============================================================================
# MCP Spec: tools/call
# Defines a single tool that the LLM can invoke
# ============================================================================

@mcp.tool
def hello(name: str = "World") -> str:
    """
    Say hello to someone.

    This demonstrates the minimum viable tool:
    - Has a name (function name)
    - Has a description (docstring)
    - Has parameters with types (name: str)
    - Returns a value

    Args:
        name: Name of the person to greet

    Returns:
        A greeting message
    """
    return f"Hello, {name}!"


# ============================================================================
# Server Execution
# ============================================================================

def main() -> None:
    """Run the minimal MCP server."""
    print("🚀 Minimal MCP Reference Server")
    print("=" * 50)
    print(f"Server: {mcp.server_info.name}")
    print(f"Version: {mcp.server_info.version}")
    print()
    print("Features:")
    print("  ✅ Lifecycle (initialize, ping)")
    print("  ✅ Tools (1 tool: hello)")
    print()
    print("MCP Spec: 2025-06-18")
    print("=" * 50)
    print()
    print("Running on http://localhost:8000")
    print("MCP endpoint: http://localhost:8000/mcp")
    print()
    print("Test with MCP Inspector:")
    print("  npx @modelcontextprotocol/inspector")
    print()

    # Run server - chuk-mcp-server handles:
    # - JSON-RPC 2.0 protocol
    # - initialize/initialized handshake
    # - tools/list request
    # - tools/call request
    # - ping request
    # - All error handling
    mcp.run(host="localhost", port=8000)


if __name__ == "__main__":
    main()
