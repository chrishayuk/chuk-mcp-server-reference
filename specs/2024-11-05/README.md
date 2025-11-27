# MCP Specification 2024-11-05

Initial MCP specification version.

## Version Information

- **Release Date**: November 5, 2024
- **Status**: Legacy (superseded by 2025-06-18 and 2025-11-25)
- **Schema**: `https://modelcontextprotocol.io/schema/2024-11-05/schema.json`

## Overview

This is the initial release of the Model Context Protocol specification. It establishes the foundational architecture and core features that all subsequent versions build upon.

## Core Features

### Server Features
- **Tools** - Basic tool support with JSON Schema validation
- **Resources** - Static and dynamic resources
- **Prompts** - Simple prompts without complex arguments

### Protocol Foundation
- JSON-RPC 2.0 messaging
- Lifecycle (initialize, initialized, ping)
- Basic capability negotiation
- Error handling

## What Was Added Later

This initial specification did not include:
- ❌ Resource templates (added in 2025-06-18)
- ❌ Resource subscriptions (added in 2025-06-18)
- ❌ Prompt arguments (enhanced in 2025-06-18)
- ❌ Progress notifications (added in 2025-06-18)
- ❌ Completion support (added in 2025-06-18)
- ❌ Tasks (added in 2025-11-25)
- ❌ Enterprise IdP (added in 2025-11-25)

## Reference Implementation

The reference server implements features beyond this specification version. For 2024-11-05 specific compatibility, use the feature flags in chuk-mcp-server.

## Migration Path

### To 2025-06-18
Recommended migration path. Adds significant enhancements while maintaining backward compatibility:
- Resource templates for dynamic URIs
- Prompt arguments for parameterization
- Progress tracking
- Completion support

### To 2025-11-25
Direct migration possible. Includes all 2025-06-18 features plus:
- Tasks abstraction
- Enterprise IdP support

## Specification Links

- [Initial Announcement](https://blog.modelcontextprotocol.io/posts/2024-11-05-mcp-launch/)
- [Schema](https://github.com/modelcontextprotocol/specification/tree/main/schema/2024-11-05)

## Historical Significance

The 2024-11-05 specification represents the birth of MCP:
- First standardized protocol for LLM context
- Established JSON-RPC foundation
- Created the Tools/Resources/Prompts architecture
- Defined capability negotiation pattern

All modern MCP features build on this foundation.
