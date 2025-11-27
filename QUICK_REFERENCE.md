# MCP Quick Reference

Fast reference for the Model Context Protocol specification.

## Examples at a Glance

| Example | Features | Tools | Resources | Prompts | Use When |
|---------|----------|-------|-----------|---------|----------|
| `01_minimal.py` | Basic | 1 | 0 | 0 | Learning basics |
| `02_tools_basic.py` | All tool types | 10 | 0 | 0 | Understanding parameters |
| `11_full_server.py` | Everything | 3 | 4 | 3 | Complete reference |

## Run Examples

```bash
uv run examples/01_minimal.py      # Start learning here
uv run examples/02_tools_basic.py  # See all parameter types
uv run examples/11_full_server.py  # See complete implementation
```

## MCP Protocol Messages

### Lifecycle
```
Client → Server: initialize
Server → Client: {protocolVersion, capabilities, serverInfo}
Client → Server: initialized (notification)
Client ↔ Server: ping
```

### Tools
```
Client → Server: tools/list
Server → Client: {tools: [{name, description, inputSchema}]}

Client → Server: tools/call {name, arguments}
Server → Client: {content: [{type, text/data}]}
```

### Resources
```
Client → Server: resources/list
Server → Client: {resources: [{uri, name, mimeType}]}

Client → Server: resources/read {uri}
Server → Client: {contents: [{uri, mimeType, text/blob}]}
```

### Prompts
```
Client → Server: prompts/list
Server → Client: {prompts: [{name, description, arguments}]}

Client → Server: prompts/get {name, arguments}
Server → Client: {messages: [{role, content}]}
```

## Basic Server Template

```python
from chuk_mcp_server import ChukMCPServer

mcp = ChukMCPServer(name="my-server", version="1.0.0")

@mcp.tool
def my_tool(param: str) -> str:
    """Tool description."""
    return f"Result: {param}"

@mcp.resource("config://settings")
def settings() -> dict:
    """Resource description."""
    return {"key": "value"}

@mcp.prompt
def my_prompt(topic: str) -> str:
    """Prompt description."""
    return f"Explain: {topic}"

mcp.run()
```

## Parameter Types

| Type | Python | JSON Schema | Example |
|------|--------|-------------|---------|
| String | `str` | `"type": "string"` | `name: str` |
| Integer | `int` | `"type": "integer"` | `count: int` |
| Number | `float` | `"type": "number"` | `amount: float` |
| Boolean | `bool` | `"type": "boolean"` | `enabled: bool` |
| Array | `list[T]` | `"type": "array"` | `items: list[str]` |
| Object | `dict` | `"type": "object"` | `data: dict[str, Any]` |
| Optional | `T \| None` | Not in required | `name: str \| None = None` |

## Content Types

```python
# Text content
{"type": "text", "text": "..."}

# Image content
{"type": "image", "data": "base64...", "mimeType": "image/png"}

# Embedded resource
{"type": "resource", "resource": {...}}
```

## Error Codes

| Code | Meaning | When |
|------|---------|------|
| -32700 | Parse error | Invalid JSON |
| -32600 | Invalid request | Missing required fields |
| -32601 | Method not found | Unknown method |
| -32602 | Invalid params | Wrong parameters |
| -32603 | Internal error | Server error |

## Spec Versions

| Version | Date | Key Features |
|---------|------|--------------|
| 2024-11-05 | Nov 2024 | Initial release - tools, resources, prompts |
| 2025-06-18 | Jun 2025 | Core spec - templates, subscriptions, progress |
| 2025-11-25 | Nov 2025 | Tasks, Enterprise IdP |

## Testing

```bash
# Validate examples work
uv run pytest tests/test_examples.py

# Protocol compliance
uv run pytest tests/test_protocol_compliance.py

# Interactive demo
uv run python tests/spec_compliance_demo.py --start-server
```

## MCP Inspector

```bash
# Terminal 1: Start server
uv run examples/11_full_server.py

# Terminal 2: Run inspector
npx @modelcontextprotocol/inspector
```

Configure:
- URL: `http://localhost:8000/mcp`
- Transport: HTTP

## Capabilities

```python
# Server advertises
{
  "capabilities": {
    "tools": {"listChanged": True},
    "resources": {"subscribe": True, "listChanged": True},
    "prompts": {"listChanged": True},
    "logging": {}
  }
}

# Client advertises
{
  "capabilities": {
    "sampling": {},
    "roots": {"listChanged": True}
  }
}
```

## File Organization

```
examples/     # Working code
specs/        # Version docs
tests/        # Validation
├── test_examples.py          # Example tests
├── test_protocol_compliance.py  # Protocol tests
└── spec_compliance_demo.py   # Interactive demo
```

## Common Tasks

```bash
# Change port
mcp.run(port=3000)

# Debug mode
mcp.run(debug=True)

# STDIO transport
mcp.run_stdio()

# Get server info
info = mcp.info()
```

## Resources

- [MCP Spec](https://modelcontextprotocol.io/specification/)
- [chuk-mcp-server](../chuk-mcp-server)
- [Examples Guide](examples/README.md)
- [Getting Started](GETTING_STARTED.md)
- [Full Summary](SUMMARY.md)

---

**Quick Start**: Run `examples/01_minimal.py` and connect with MCP Inspector!
