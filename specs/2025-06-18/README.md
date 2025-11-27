# MCP Specification 2025-06-18

Core MCP specification version with all fundamental features.

## Version Information

- **Release Date**: June 18, 2025
- **Status**: Stable (superseded by 2025-11-25)
- **Schema**: `https://modelcontextprotocol.io/schema/2025-06-18/schema.json`

## Overview

This is the core MCP specification that establishes all fundamental protocol features:
- Complete Tools, Resources, and Prompts support
- Client capabilities (Sampling, Roots)
- Utilities (Logging, Progress, Completion, Cancellation)
- Full content type support

## Core Features

### Server Features
- **Tools** - Executable functions for LLMs
- **Resources** - Data and context access
- **Prompts** - Templated messages and workflows

### Client Features
- **Sampling** - Server-initiated LLM interactions
- **Roots** - Filesystem/URI boundary queries

### Utilities
- **Logging** - Configurable logging with multiple levels
- **Progress** - Progress tracking for long operations
- **Completion** - Argument autocompletion
- **Cancellation** - Request cancellation support

## Reference Implementation

All features from this specification are fully implemented in the reference server.

**Primary Example**: `examples/11_full_server.py`

## Specification Structure

### Base Protocol
- JSON-RPC 2.0 messaging
- Request/Response pattern
- Notifications (fire-and-forget)
- Error handling

### Lifecycle
1. Client sends `initialize` with capabilities
2. Server responds with server capabilities
3. Client sends `initialized` notification
4. Normal operation (tools, resources, prompts)
5. Bidirectional `ping` for health checks

### Message Flow

```
Client                                  Server
  |                                        |
  |------ initialize (capabilities) ----->|
  |                                        |
  |<----- response (capabilities) ---------|
  |                                        |
  |------ initialized (notification) ---->|
  |                                        |
  |------ tools/list ------------------->|
  |<----- response (tools) ---------------|
  |                                        |
  |------ tools/call ------------------->|
  |<----- response (result) --------------|
  |                                        |
  |<----- notifications/message ----------|
  |                                        |
```

## Capabilities Example

### Server Capabilities
```json
{
  "capabilities": {
    "tools": {
      "listChanged": true
    },
    "resources": {
      "subscribe": true,
      "listChanged": true
    },
    "prompts": {
      "listChanged": true
    },
    "logging": {}
  }
}
```

### Client Capabilities
```json
{
  "capabilities": {
    "sampling": {},
    "roots": {
      "listChanged": true
    }
  }
}
```

## Content Types

All content types defined in this specification:

### TextContent
```json
{
  "type": "text",
  "text": "Content here"
}
```

### ImageContent
```json
{
  "type": "image",
  "data": "base64-encoded-data",
  "mimeType": "image/png"
}
```

### EmbeddedResource
```json
{
  "type": "resource",
  "resource": {
    "uri": "file:///path/to/file",
    "mimeType": "text/plain",
    "text": "Content"
  }
}
```

## Specification Links

- [Official Spec](https://modelcontextprotocol.io/specification/2025-06-18)
- [Schema](https://github.com/modelcontextprotocol/specification/tree/main/schema/2025-06-18)
- [Tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)
- [Resources](https://modelcontextprotocol.io/specification/2025-06-18/server/resources)
- [Prompts](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts)

## Migration

### From 2024-11-05
The 2025-06-18 specification adds:
- Enhanced prompt support with arguments
- Resource templates and subscriptions
- Progress notifications
- Completion support
- Improved error handling

### To 2025-11-25
The 2025-11-25 specification adds:
- Tasks abstraction
- Enterprise IdP support

Both migrations are backward compatible.

## Feature Checklist

See [features.md](./features.md) for complete feature checklist.
