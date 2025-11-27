# Getting Started with MCP Reference Server

Quick start guide to using the MCP reference implementation.

## Installation

```bash
# Clone or navigate to the directory
cd chuk-mcp-server-reference

# Install dependencies
pip install -r requirements.txt
```

## Run Your First Example

```bash
# Run the minimal server
python examples/01_minimal.py
```

You should see:
```
🚀 Minimal MCP Reference Server
==================================================
Server: minimal-mcp-server
Version: 1.0.0

Features:
  ✅ Lifecycle (initialize, ping)
  ✅ Tools (1 tool: hello)

MCP Spec: 2025-06-18
==================================================

Running on http://localhost:8000
MCP endpoint: http://localhost:8000/mcp
```

## Test with MCP Inspector

In another terminal:

```bash
npx @modelcontextprotocol/inspector
```

Configure the inspector:
1. **Transport Type:** HTTP
2. **URL:** `http://localhost:8000/mcp`
3. Click **Connect**

You should now see:
- ✅ Connection established
- 📋 Tools list showing "hello"
- 🎯 Ability to call the hello tool

## Explore More Examples

### Basic Tools (All Parameter Types)
```bash
python examples/02_tools_basic.py
```

**What you'll learn:**
- String, integer, float, boolean parameters
- Arrays and objects
- Required vs optional parameters
- Default values

### Full Server (All Features)
```bash
python examples/11_full_server.py
```

**What you'll learn:**
- Tools, Resources, Prompts
- Multiple content types
- Complex data structures
- Complete spec implementation

## Understanding the Code

### Minimal Example Structure

```python
from chuk_mcp_server import ChukMCPServer

# 1. Create server
mcp = ChukMCPServer(name="my-server", version="1.0.0")

# 2. Define tools
@mcp.tool
def my_tool(param: str) -> str:
    """Tool description."""
    return f"Result: {param}"

# 3. Run server
mcp.run()
```

That's it! The protocol implementation is handled by chuk-mcp-server.

## Key Concepts

### Tools
Functions that LLMs can call. Defined with the `@mcp.tool` decorator.

```python
@mcp.tool
def calculate(expression: str) -> str:
    """Evaluate a math expression."""
    # chuk-mcp-server automatically:
    # - Generates JSON schema from type hints
    # - Validates parameters
    # - Handles errors
    # - Formats responses
    return eval_safely(expression)
```

### Resources
Data that LLMs can read. Defined with the `@mcp.resource` decorator.

```python
@mcp.resource("config://settings")
def get_settings() -> dict:
    """Server configuration."""
    return {"key": "value"}
```

### Prompts
Templates for LLM interactions. Defined with the `@mcp.prompt` decorator.

```python
@mcp.prompt
def code_review(code: str) -> str:
    """Review code for quality."""
    return f"Please review:\n{code}"
```

## Protocol Flow

```
1. Client connects → initialize request
2. Server responds → capabilities
3. Client sends → initialized notification
4. Normal operation:
   - tools/list → get available tools
   - tools/call → execute tools
   - resources/list → get available resources
   - resources/read → read resource content
   - prompts/list → get available prompts
   - prompts/get → get prompt template
```

## What's Handled For You

chuk-mcp-server automatically handles:

- ✅ JSON-RPC 2.0 protocol
- ✅ Message formatting
- ✅ Schema generation
- ✅ Parameter validation
- ✅ Error handling
- ✅ Capability negotiation
- ✅ HTTP/STDIO transport
- ✅ Session management

**You just focus on:**
- Defining your tools, resources, and prompts
- Implementing business logic

## Next Steps

1. **Read the spec documentation**
   - `specs/2025-06-18/README.md` - Core specification
   - `specs/2025-11-25/README.md` - Latest features

2. **Explore examples**
   - `examples/README.md` - Complete example guide
   - `examples/*.py` - Working code

3. **Check spec compliance**
   - `specs/2025-11-25/features.md` - Feature checklist

4. **Run tests**
   ```bash
   pytest tests/
   ```

5. **Build your own server**
   - Copy `examples/01_minimal.py`
   - Add your tools
   - Run and test!

## Common Tasks

### Change Port
```python
mcp.run(port=3000)
```

### Enable Debug Mode
```python
mcp.run(debug=True)
```

### Use STDIO Transport
```python
mcp.run_stdio()
```

### Add Multiple Tools
```python
@mcp.tool
def tool1(x: int) -> int:
    return x * 2

@mcp.tool
def tool2(s: str) -> str:
    return s.upper()

@mcp.tool
def tool3(items: list[str]) -> str:
    return ", ".join(items)
```

## Troubleshooting

### Server Won't Start
- Check port 8000 isn't already in use
- Try a different port: `mcp.run(port=3000)`

### Tool Not Appearing
- Ensure decorator is `@mcp.tool` (not `@tool`)
- Check function has type hints
- Verify function has docstring

### Inspector Won't Connect
- Verify server is running
- Check URL is `http://localhost:8000/mcp`
- Try STDIO transport instead

## Resources

- [MCP Specification](https://modelcontextprotocol.io/specification/)
- [chuk-mcp-server](../chuk-mcp-server)
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector)
- [Examples](./examples/README.md)

## Quick Reference

### Decorators
```python
@mcp.tool              # Define a tool
@mcp.resource(uri)     # Define a resource
@mcp.prompt            # Define a prompt
```

### Parameter Types
```python
str                    # String
int                    # Integer
float                  # Float/number
bool                   # Boolean
list[T]                # Array
dict[str, Any]         # Object
Optional[T]            # Optional parameter
```

### Running
```python
mcp.run()              # HTTP transport (default)
mcp.run_stdio()        # STDIO transport
```

---

**Ready to build?** Start with `examples/01_minimal.py` and grow from there!
