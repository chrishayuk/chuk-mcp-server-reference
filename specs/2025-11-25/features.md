# MCP Specification 2025-11-25 - Feature Checklist

Complete feature checklist for MCP specification version 2025-11-25.

## Core Protocol

- [x] JSON-RPC 2.0 messaging
- [x] Request/Response pattern
- [x] Notifications
- [x] Error handling with standard codes
- [x] Batch requests

## Lifecycle

- [x] `initialize` request
- [x] `initialized` notification
- [x] `ping` request (bidirectional)
- [x] Capability negotiation
- [x] Protocol version negotiation

## Server Features

### Tools
- [x] `tools/list` - List available tools
- [x] `tools/call` - Execute a tool
- [x] Tool input schemas (JSON Schema)
- [x] Tool descriptions
- [x] `notifications/tools/list_changed` - Tool list updates
- [x] Multiple parameter types (string, number, boolean, array, object)
- [x] Required and optional parameters
- [x] Default values

### Resources
- [x] `resources/list` - List available resources
- [x] `resources/read` - Read resource content
- [x] `resources/templates/list` - List URI templates
- [ ] `resources/subscribe` - Subscribe to resource updates
- [ ] `resources/unsubscribe` - Unsubscribe from updates
- [x] `notifications/resources/updated` - Resource change notifications
- [x] `notifications/resources/list_changed` - Resource list updates
- [x] Multiple MIME types (text/plain, text/markdown, application/json, image/*, etc.)
- [x] Text resources
- [ ] Binary resources (base64 encoded)

### Prompts
- [x] `prompts/list` - List available prompts
- [x] `prompts/get` - Get prompt with arguments
- [x] `notifications/prompts/list_changed` - Prompt list updates
- [x] Prompt arguments (required and optional)
- [x] Multi-message prompts
- [x] Prompt templates

## Client Features

### Sampling
- [ ] `sampling/createMessage` - Server-initiated LLM sampling
- [ ] Multi-turn conversations
- [ ] System prompts
- [ ] Model preferences
- [ ] Temperature and other parameters

### Roots
- [ ] `roots/list` - List filesystem/URI roots
- [ ] `notifications/roots/list_changed` - Roots updates

## Utilities

### Logging
- [x] `logging/setLevel` - Configure log verbosity
- [x] `notifications/message` - Log message output
- [x] Log levels (debug, info, notice, warning, error, critical, alert, emergency)

### Progress
- [ ] `notifications/progress` - Progress updates
- [ ] Progress tokens for long operations
- [ ] Progress total and current values

### Completion
- [ ] `completion/complete` - Argument autocompletion
- [ ] Context-aware suggestions
- [ ] Completion for tool arguments

### Cancellation
- [ ] `notifications/cancelled` - Request cancellation
- [ ] Cancellation tokens
- [ ] Graceful cancellation handling

## Content Types

- [x] TextContent - Plain and formatted text
- [x] ImageContent - Base64 encoded images
- [ ] AudioContent - Base64 encoded audio
- [x] EmbeddedResource - Embedded resource references
- [x] ResourceReference - Resource links

## New in 2025-11-25

### Major Features

#### Tasks (NEW - Experimental)
- [ ] Task creation and tracking
- [ ] Task status queries via polling
- [ ] Deferred result retrieval
- [ ] Task lifecycle management
- [ ] Task notifications
- [ ] Durable request tracking

#### Enhanced Authorization (NEW)
- [ ] OpenID Connect Discovery 1.0 support
- [ ] Incremental scope consent via WWW-Authenticate
- [ ] OAuth Client ID Metadata Documents
- [ ] RFC 9728 Protected Resource Metadata discovery
- [ ] HTTP 403 for invalid Origin headers (Streamable HTTP)

#### Tool Calling in Sampling (NEW)
- [ ] `tools` parameter in sampling
- [ ] `toolChoice` parameter
- [ ] Model can call tools during sampling

#### Metadata & Icons (NEW)
- [ ] Icons for tools
- [ ] Icons for resources
- [ ] Icons for resource templates
- [ ] Icons for prompts

#### Enhanced Elicitation (NEW)
- [ ] URL mode elicitation support
- [ ] Titled/untitled enums
- [ ] Single-select enums
- [ ] Multi-select enums
- [ ] Default values for primitives (string, number, enum)
- [ ] Enhanced ElicitResult format

### Minor Enhancements

#### Transport & Streaming
- [ ] SSE stream polling support
- [ ] Server-initiated disconnection
- [ ] GET request resumption
- [ ] Event ID encoding for stream identity

#### Schema & Validation
- [ ] JSON Schema 2020-12 as default dialect
- [ ] Decoupled request payloads from RPC methods
- [ ] Tool execution errors vs protocol errors clarification

#### Other
- [ ] `description` field in Implementation interface
- [ ] stderr logging clarification for stdio
- [ ] Tool naming guidance
- [ ] Enhanced security best practices

## Pagination

- [x] Cursor-based pagination for tools/list
- [x] Cursor-based pagination for resources/list
- [x] Cursor-based pagination for prompts/list

## Error Codes

- [x] Parse error (-32700)
- [x] Invalid request (-32600)
- [x] Method not found (-32601)
- [x] Invalid params (-32602)
- [x] Internal error (-32603)

## Legend

- [x] Implemented in chuk-mcp-server-reference
- [ ] Not yet implemented
- ⏳ Planned for future release
