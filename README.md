# MCP Reference Server

A comprehensive reference implementation demonstrating **all features** of the Model Context Protocol (MCP) specification using `chuk-mcp-server`.

![MCP Compliance](https://img.shields.io/badge/MCP%20Spec%202025--06--18-100%25%20Compliant-brightgreen)
![Tests](https://img.shields.io/badge/Tests-16%2F16%20Passing-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)

**🎉 Certified 100% MCP Specification Compliant** - See [COMPLIANCE.md](COMPLIANCE.md)

## Overview

This repository provides complete, working examples of every MCP feature defined in the official specification. It serves as:
- 📚 **Reference Documentation** - See how each MCP feature works
- ✅ **Spec Compliance Examples** - Validate MCP implementations
- 🎓 **Learning Resource** - Understand the MCP protocol
- 🧪 **Testing Tool** - Test MCP clients against spec features

## Specification Versions

| Version | Status | Features |
|---------|--------|----------|
| **2025-06-18** | ✅ **100% Implemented & Tested** | Core spec: Tools, Resources, Prompts, Sampling, Logging |
| **2025-11-25** | 📚 **Reference Examples Only** | Tasks (experimental), Enhanced Auth, Tool Calling in Sampling, Icons, Enhanced Elicitation |
| **2024-11-05** | 📚 **Documented** | Initial specification (superseded by 2025-06-18) |

**⚠️ Important**: MCP 2025-11-25 examples (12, 13, 14) are **reference implementations** showing how the spec SHOULD work. The features are not yet implemented in chuk-mcp-server. Icons are embedded as text/emojis, and elicitation features are documented in docstrings.

**Current Testing**: All compliance tests validate against **MCP 2025-06-18** (core specification)

## MCP Features Demonstrated

### ✅ Core Protocol (JSON-RPC 2.0)
All examples use proper JSON-RPC 2.0 message formatting implemented by chuk-mcp-server.

### ✅ Lifecycle
- `initialize` - Connection and capability negotiation
- `initialized` notification
- `ping` - Health check (bidirectional)

### ✅ Server Capabilities

#### Tools (`tools/list`, `tools/call`)
- Basic tools with various parameter types
- Tools with complex schemas
- Tools with progress reporting
- Tools with error handling
- Dynamic tool registration
- `notifications/tools/list_changed`

#### Resources (`resources/*`)
- Static resources
- Dynamic resources with URI templates
- Resource subscriptions
- Binary resources (images, audio)
- Text resources (markdown, JSON, code)
- `notifications/resources/updated`
- `notifications/resources/list_changed`

#### Prompts (`prompts/list`, `prompts/get`)
- Static prompts
- Prompts with arguments
- Multi-message prompts
- Prompt templates
- `notifications/prompts/list_changed`

### ✅ Client Capabilities

#### Sampling (`sampling/createMessage`)
- Server-initiated LLM requests
- Multi-turn conversations
- System prompts
- Model preferences

#### Roots (`roots/list`)
- Filesystem root queries
- `notifications/roots/list_changed`

### ✅ Utilities

#### Logging (`logging/setLevel`)
- Debug, info, warning, error levels
- `notifications/message` - Log output

#### Progress
- `notifications/progress` - Long-running operation updates
- Progress tokens

#### Completion (`completion/complete`)
- Argument autocompletion
- Context-aware suggestions

#### Cancellation
- `notifications/cancelled` - Request cancellation

## Project Structure

```
chuk-mcp-server-reference/
├── README.md
├── pyproject.toml
├── examples/
│   ├── 01_minimal.py              # Simplest possible MCP server
│   ├── 02_tools_basic.py          # Basic tool examples (all parameter types)
│   ├── 11_full_server.py          # Complete 2025-06-18 reference
│   ├── 12_icons_metadata.py       # Icons and metadata (2025-11-25)
│   ├── 13_enhanced_elicitation.py # Enhanced elicitation (2025-11-25)
│   ├── 14_spec_2025_11_25.py      # Complete 2025-11-25 reference
│   └── README.md
├── specs/
│   ├── 2024-11-05/
│   │   ├── README.md              # Spec version details
│   │   └── features.md            # Feature checklist
│   ├── 2025-06-18/
│   │   ├── README.md
│   │   └── features.md
│   └── 2025-11-25/
│       ├── README.md
│       └── features.md
└── tests/
    ├── test_tools.py              # Tool examples tests
    ├── test_resources.py          # Resource examples tests
    ├── test_prompts.py            # Prompt examples tests
    └── test_integration.py        # Full integration tests
```

## Quick Start

### Installation

```bash
cd chuk-mcp-server-reference
pip install -r requirements.txt
```

### Run Examples

```bash
# MCP 2025-06-18 (Core Specification - 100% Compliant)
python examples/01_minimal.py              # Start here - simplest server
python examples/02_tools_basic.py          # All tool parameter types
python examples/11_full_server.py          # Complete 2025-06-18 reference

# MCP 2025-11-25 (Latest Specification - Reference Examples)
# ⚠️  These are reference examples only - features not yet in chuk-mcp-server
python examples/12_icons_metadata.py       # Icons reference (emoji-based)
python examples/13_enhanced_elicitation.py # Enhanced elicitation reference
python examples/14_spec_2025_11_25.py      # Complete 2025-11-25 reference
```

## Example Catalog

### 1. Minimal Server
The simplest possible MCP server with one tool.

### 2. Basic Tools
Demonstrates all tool parameter types:
- String, integer, number, boolean
- Arrays and objects
- Optional and required parameters
- Default values

### 3. Advanced Tools
- Complex nested schemas
- Progress reporting during execution
- Error handling patterns
- Tool result content types (text, images, embedded resources)

### 4. Basic Resources
- Static resources with various MIME types
- List resources
- Read resource content
- Text and binary resources

### 5. Advanced Resources
- URI templates (`file://logs/{date}`)
- Resource subscriptions
- Resource update notifications
- Dynamic resource generation

### 6. Basic Prompts
- Simple prompts
- Prompts with arguments
- Multi-message prompts

### 7. Advanced Prompts
- Parameterized prompt templates
- Dynamic prompt generation
- Prompt argument validation

### 8. Sampling
- Server requests LLM completion from client
- Multi-turn conversations
- System prompts and preferences

### 9. Logging & Progress
- Log level configuration
- Progress notifications for long operations
- Progress tokens

### 10. Completion
- Argument autocompletion
- Context-aware suggestions

### 11. Full Server
Complete server with ALL features enabled - the ultimate reference.

## Testing with MCP Inspector

All examples work with [MCP Inspector](https://github.com/modelcontextprotocol/inspector):

```bash
# Run any example
python examples/11_full_server.py

# In another terminal, use MCP Inspector
npx @modelcontextprotocol/inspector
```

Configure Inspector:
- **Transport**: HTTP or STDIO
- **URL**: `http://localhost:8000/mcp` (for HTTP)
- **Command**: `python examples/11_full_server.py` (for STDIO)

## Specification Mapping

Each example includes comments mapping features to the official MCP specification:

```python
# MCP Spec: tools/list
# Version: 2025-06-18
# Reference: https://modelcontextprotocol.io/specification/2025-06-18/server/tools

@mcp.tool
def example_tool(param: str) -> str:
    """Tool description per spec."""
    return result
```

## Spec Compliance

This reference server aims for 100% compliance with the MCP specification:

- ✅ Proper JSON-RPC 2.0 formatting
- ✅ Capability negotiation
- ✅ Content type support (text, image, audio, embedded resources)
- ✅ Error codes and handling
- ✅ Notifications
- ✅ Pagination
- ✅ Progress reporting
- ✅ Cancellation

## Testing

### Run Compliance Demo

Interactive demo that tests full MCP spec compliance:

```bash
# Auto-start server and test
python examples/spec_compliance_demo.py --start-server

# Against a running server
python examples/spec_compliance_demo.py

# Against a different server
python examples/spec_compliance_demo.py --url http://localhost:3000/mcp
```

### Run Test Suite

```bash
# Run all tests
pytest

# Run protocol compliance tests (2025-06-18)
pytest tests/test_protocol_compliance.py -v

# Run example validation tests
pytest tests/test_examples.py -v

# Run 2025-11-25 feature tests (shows what's not implemented)
pytest tests/test_2025_11_25_features.py -v

# Run with coverage
pytest --cov=examples --cov-report=html
```

### MCP 2025-11-25 Feature Status

Test the implementation status of new features:

```bash
# Run feature tests - shows passing and expected failures
pytest tests/test_2025_11_25_features.py -v

# See summary of what works and what doesn't
pytest tests/test_2025_11_25_features.py::test_summary_report -v -s
```

**Results**: 3 passed (description, defaults), 5 xfailed (icons, elicitation modes)

## Documentation

- `specs/` - Detailed documentation for each spec version
- `examples/README.md` - Guide to all examples
- Each example file contains extensive inline documentation

## Contributing

Contributions should:
1. Map to specific MCP specification sections
2. Include spec version and reference URLs
3. Add tests
4. Update documentation

## Resources

- [MCP Specification](https://modelcontextprotocol.io/specification/)
- [MCP GitHub](https://github.com/modelcontextprotocol)
- [chuk-mcp-server](https://github.com/your-org/chuk-mcp-server)
- [JSON-RPC 2.0](https://www.jsonrpc.org/specification)

## License

MIT License

---

**Built with** [chuk-mcp-server](https://github.com/your-org/chuk-mcp-server) - The protocol implementation is already done, this repo just demonstrates all the features! 🚀
