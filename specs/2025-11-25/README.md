# MCP Specification 2025-11-25

Latest MCP specification version released on November 25, 2025 (One year anniversary).

## Version Information

- **Release Date**: November 25, 2025
- **Status**: Latest
- **Schema**: `https://modelcontextprotocol.io/schema/2025-11-25/schema.json`

## What's New in 2025-11-25

This release includes major enhancements across authorization, tooling, elicitation, and introduces experimental support for durable tasks.

### Major Features

#### 1. Tasks (Experimental)
New abstraction for tracking durable, long-running requests:
- **Polling support** - Query task status and results asynchronously
- **Deferred results** - Tasks can complete after initial request
- **Lifecycle tracking** - Monitor task progress
- **Enable long operations** - Handle requests that take time to complete

#### 2. Enhanced Authorization
Significant OAuth and security improvements:
- **OpenID Connect Discovery 1.0** - Standard discovery mechanism
- **Incremental scope consent** - WWW-Authenticate flow for additional permissions
- **OAuth Client ID Metadata** - Recommended client registration
- **RFC 9728 compliance** - Protected Resource Metadata discovery
- **Enhanced security** - Better origin validation, improved practices

#### 3. Tool Calling in Sampling
Servers can now request LLM sampling with tool access:
- **tools parameter** - Provide tools to the model during sampling
- **toolChoice parameter** - Control tool selection behavior
- **Recursive capabilities** - Models can use tools in responses

#### 4. Icons and Metadata
Visual enhancements across the protocol:
- **Tool icons** - Visual identification for tools
- **Resource icons** - Icons for resources and templates
- **Prompt icons** - Visual cues for prompts
- **Better UX** - Improved client presentation

#### 5. Enhanced Elicitation
Richer user input collection:
- **URL mode** - Elicit URLs from users
- **Enhanced enums** - Titled/untitled, single/multi-select
- **Default values** - Support for string, number, enum defaults
- **Better UX** - More intuitive input forms

### Minor Enhancements

#### Streaming Improvements
- **Polling SSE streams** - Server-initiated disconnection support
- **GET resumption** - Resume streams via GET regardless of origin
- **Event IDs** - Encode stream identity for better tracking

#### Schema & Standards
- **JSON Schema 2020-12** - Official default dialect
- **Decoupled payloads** - Request parameters separate from methods
- **Better error handling** - Tool execution vs protocol errors

#### Other Improvements
- **Implementation metadata** - Optional description field
- **Logging clarification** - stderr usage in stdio transport
- **Tool naming guidance** - Best practices for naming
- **Security updates** - Enhanced best practices documentation

### Previous Features (Maintained)
All features from 2025-06-18 are maintained:
- Tools, Resources, Prompts
- Sampling, Roots
- Logging, Progress, Completion
- Cancellation

## Reference Implementation Status

### Tasks
- ⏳ **Coming Soon** - Not yet implemented in chuk-mcp-server reference

### Enterprise IdP
- ⏳ **Coming Soon** - Authentication framework planned

### Core Features
- ✅ **Implemented** - See examples/11_full_server.py

## Specification Links

- [Official Spec](https://modelcontextprotocol.io/specification/2025-11-25)
- [Schema](https://github.com/modelcontextprotocol/specification/tree/main/schema/2025-11-25)
- [Announcement Blog Post](https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/)

## Migration from 2025-06-18

The 2025-11-25 specification is backward compatible with 2025-06-18. New features are additive:

1. **Tasks** - Optional new capability
   - Servers can opt-in to task support
   - Clients negotiate during initialization

2. **Enterprise IdP** - OAuth enhancement
   - Existing OAuth flows continue to work
   - Enterprise features are optional

### Breaking Changes
None - fully backward compatible.

## Feature Checklist

See [features.md](./features.md) for complete feature checklist.
