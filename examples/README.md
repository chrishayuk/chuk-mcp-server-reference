# MCP Reference Examples

Complete examples demonstrating every feature of the Model Context Protocol specification.

## Quick Start

```bash
# Install dependencies
cd chuk-mcp-server-reference
pip install -r requirements.txt

# Run any example
python examples/01_minimal.py
```

## Example Catalog

### 01_minimal.py - Simplest MCP Server
The absolute minimum to create an MCP server.

**Features:**
- Single tool
- Basic lifecycle
- Minimal configuration

**MCP Spec:** Lifecycle, Tools (basic)

**Run:**
```bash
python examples/01_minimal.py
```

### 02_tools_basic.py - Tool Parameter Types
Demonstrates all tool parameter types from the MCP spec.

**Features:**
- String, integer, float, boolean parameters
- Arrays and objects
- Required vs optional
- Default values
- Tool introspection

**MCP Spec:** Tools (comprehensive parameter types)

**Run:**
```bash
python examples/02_tools_basic.py
```

### 11_full_server.py - Complete Reference (2025-06-18)
The ultimate reference - ALL MCP 2025-06-18 features in one server.

**Features:**
- ✅ All tool types
- ✅ All resource types (JSON, Markdown)
- ✅ All prompt types
- ✅ Logging
- ✅ Progress notifications
- ✅ Multiple content types

**MCP Spec:** Complete 2025-06-18 specification

**Run:**
```bash
python examples/11_full_server.py
```

### 12_icons_metadata.py - Icons and Metadata (2025-11-25)
⚠️ **REFERENCE IMPLEMENTATION** - Shows how icons SHOULD work per spec.
Currently icons are embedded as text/emojis in docstrings and responses only.

**Reference Features:**
- 🎨 Icons for tools (🧮 📧 🔍 📄) - as emojis in responses
- 🎨 Icons for resources (⚙️ 👥 📚 📊) - as emojis in responses
- 🎨 Icons for prompts (🔍 🧪 🐛) - as emojis in responses
- ✨ Implementation description field (works - server has description)

**MCP Spec:** 2025-11-25 (SEP-973 - Icons)

**What's Missing:**
- Actual icon metadata fields in tools/list response (needs chuk-mcp-server)
- Icon fields in resources/list and prompts/list (needs chuk-mcp-server)
- MCP clients displaying icons from metadata (needs client support)

**Run:**
```bash
python examples/12_icons_metadata.py
```

### 13_enhanced_elicitation.py - Enhanced Elicitation (2025-11-25)
⚠️ **REFERENCE IMPLEMENTATION** - Shows how enhanced elicitation SHOULD work.
Most features are documented in docstrings only. Default values work!

**Reference Features:**
- 🔗 URL mode elicitation (SEP-1036) - documented in docstrings
- 📋 Titled enums with descriptions (SEP-1330) - documented in docstrings
- 📋 Untitled enums for simple lists - documented in docstrings
- ✅ Single-select enums - documented in docstrings
- ☑️ Multi-select enums - list[] parameters
- 🎯 Default values for primitives (SEP-1034) - ✅ WORKS (Python defaults)

**MCP Spec:** 2025-11-25 (Enhanced Elicitation)

**What Works:**
- Default values for parameters (Python's default values are exposed)

**What's Missing:**
- URL elicitation mode in JSON Schema (needs chuk-mcp-server)
- Titled enum support in schema (needs chuk-mcp-server)
- MCP clients recognizing elicitation modes (needs client support)

**Tools:**
- `configure_server` - Titled enums + multi-select + defaults
- `fetch_webpage` - URL mode elicitation
- `subscribe_feed` - Multiple URL fields
- `create_project` - Default values (string, number, enum)
- `set_priority` - Untitled enum (simple list)
- `deploy_application` - All features combined

**Run:**
```bash
python examples/13_enhanced_elicitation.py
```

### 14_spec_2025_11_25.py - Complete 2025-11-25 Reference
⚠️ **REFERENCE IMPLEMENTATION** - Complete 2025-11-25 spec reference.
Shows all new features as they should work when fully implemented.

**Reference Features:**
- 📋 Icons and metadata (SEP-973) - emojis in text
- 📋 Enhanced elicitation (SEP-1036, SEP-1330, SEP-1034) - docs only
- ✅ Implementation description - WORKS (server has description field)
- 📋 JSON Schema 2020-12 (SEP-1613) - referenced in docs

**MCP Spec:** Complete 2025-11-25 specification reference

**Registered Components:**
- 🔧 Tools: 4 (calculate, search, fetch_url, configure)
- 📦 Resources: 3 (settings, stats, spec docs)
- 💬 Prompts: 3 (code_review, write_documentation, ai_assistant)

**What Works:**
- Server description field (implementation description)
- Default values for parameters

**What's Missing (needs chuk-mcp-server updates):**
- Icon metadata fields in responses
- URL elicitation mode in schemas
- Titled enum support
- Tool calling in sampling (also needs client)
- Tasks (experimental, needs persistence)
- Enhanced Auth (needs OAuth infrastructure)

**Run:**
```bash
python examples/14_spec_2025_11_25.py
```

## Testing with MCP Inspector

All examples work with MCP Inspector for visual testing:

```bash
# Terminal 1: Run server
python examples/11_full_server.py

# Terminal 2: Run inspector
npx @modelcontextprotocol/inspector
```

Then configure:
- **Transport Type:** HTTP
- **URL:** `http://localhost:8000/mcp`

Or for STDIO:
- **Transport Type:** STDIO
- **Command:** `python examples/11_full_server.py`

## Example Structure

Each example follows this pattern:

```python
#!/usr/bin/env python3
"""
MCP Reference: Example Name
============================

Description of what this example demonstrates.

MCP Spec Version: 2025-06-18
Features Demonstrated:
- Feature 1
- Feature 2

Spec References:
- Link to spec section
"""

from chuk_mcp_server import ChukMCPServer

# Create server
mcp = ChukMCPServer(name="example")

# Register tools, resources, prompts
@mcp.tool
def example_tool() -> str:
    """Tool description."""
    return "result"

# Run server
if __name__ == "__main__":
    mcp.run()
```

## Spec Compliance

Every example includes:
- ✅ MCP spec version number
- ✅ Feature checklist
- ✅ Spec reference URLs
- ✅ Inline documentation mapping to spec sections

## Learning Path

Recommended order for learning MCP:

### MCP 2025-06-18 (Core Specification)
1. **01_minimal.py** - Understand the basics
2. **02_tools_basic.py** - Learn tool parameters
3. **11_full_server.py** - See complete 2025-06-18 implementation

### MCP 2025-11-25 (Latest Specification)
4. **12_icons_metadata.py** - Learn icons and metadata
5. **13_enhanced_elicitation.py** - Understand enhanced input
6. **14_spec_2025_11_25.py** - See complete 2025-11-25 implementation

## Testing Examples

```bash
# Run all tests
pytest tests/

# Test specific example
pytest tests/test_tools.py -v

# Test with coverage
pytest --cov=examples --cov-report=html
```

## Example Outputs

### Minimal Server
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

### Full Server
```
🌟 COMPLETE MCP REFERENCE SERVER
======================================================================

📋 MCP Specification: 2025-06-18
🔧 All Features Implemented

CAPABILITIES:
  ✅ Core Protocol (JSON-RPC 2.0)
  ✅ Lifecycle (initialize, initialized, ping)
  ✅ Tools (list, call, notifications)
  ✅ Resources (list, read)
  ✅ Prompts (list, get)
  ✅ Logging (setLevel, message notifications)
  ✅ Progress (progress notifications)

REGISTERED COMPONENTS:
  🔧 Tools: 3
     • calculate
     • process_data
     • generate_report
  📦 Resources: 4
     • config://server-info
     • docs://readme
     • data://examples
     • data://spec-features
  💬 Prompts: 3
     • code_review
     • explain_concept
     • debug_help
```

## Protocol Messages

Examples demonstrate proper JSON-RPC 2.0 message formatting.

### Tool Call Example
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "calculate",
    "arguments": {
      "expression": "2 + 2"
    }
  }
}
```

### Response Example
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "2 + 2 = 4"
      }
    ]
  }
}
```

## Customization

All examples can be customized:

```python
# Change port
mcp.run(host="0.0.0.0", port=3000)

# Enable debug mode
mcp.run(debug=True)

# STDIO transport
mcp.run_stdio()
```

## Resources

- [MCP Specification](https://modelcontextprotocol.io/specification/)
- [chuk-mcp-server Docs](https://github.com/your-org/chuk-mcp-server)
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector)
- [JSON-RPC 2.0](https://www.jsonrpc.org/specification)
