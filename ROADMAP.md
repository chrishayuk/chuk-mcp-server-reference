# MCP Reference Server - Roadmap

## Current Status

✅ **MCP 2025-06-18**: 100% Complete and Tested (16/16 tests passing)

## Future Enhancements

### MCP 2025-11-25 Features

The November 2025 specification introduced significant new features. This roadmap outlines potential implementation priorities.

#### Priority 1: Core Enhancements (Easy Wins)

##### 1. Icons and Metadata ⭐
**Effort**: Low | **Impact**: High | **Status**: 📋 Planned

Add visual metadata to existing features:
- Tool icons
- Resource icons
- Prompt icons
- Implementation description field

**Why**: Improves UX in MCP clients, low implementation effort.

##### 2. Enhanced Elicitation ⭐
**Effort**: Low | **Impact**: Medium | **Status**: 📋 Planned

Richer input collection:
- URL mode elicitation
- Titled/untitled enums
- Single/multi-select enums
- Default values for primitives

**Why**: Better user input forms, backward compatible.

##### 3. Tool Naming Guidance ⭐
**Effort**: Very Low | **Impact**: Low | **Status**: 📋 Planned

Document and demonstrate best practices:
- Naming conventions
- Description guidelines
- Schema best practices

**Why**: Educational value, documentation update only.

#### Priority 2: Advanced Features

##### 4. Tool Calling in Sampling 🎯
**Effort**: Medium | **Impact**: High | **Status**: 🔮 Future

Enable recursive tool use:
- Add `tools` parameter to sampling requests
- Add `toolChoice` parameter
- Demonstrate model using tools in responses

**Why**: Enables agentic workflows, requires client capability.

**Dependencies**: Need MCP client that supports tool calling in sampling.

##### 5. Tasks (Experimental) 🎯
**Effort**: High | **Impact**: High | **Status**: 🔮 Future

Support durable, long-running operations:
- Task creation and tracking
- Polling support
- Deferred result retrieval
- Status queries
- Lifecycle management

**Why**: Critical for long-running operations (data processing, ML training, etc).

**Dependencies**: Requires persistence layer, state management.

#### Priority 3: Enterprise Features

##### 6. Enhanced Authorization 🏢
**Effort**: High | **Impact**: Medium | **Status**: 🔮 Future

OAuth and security improvements:
- OpenID Connect Discovery 1.0
- Incremental scope consent
- OAuth Client ID Metadata Documents
- RFC 9728 compliance

**Why**: Enterprise deployments, but complex to implement and test.

**Dependencies**: OAuth infrastructure, IdP integration.

##### 7. Advanced Streaming 🔄
**Effort**: Medium | **Impact**: Low | **Status**: 🔮 Future

SSE enhancements:
- Polling SSE streams
- GET resumption
- Event ID encoding
- Server-initiated disconnection

**Why**: Better stream handling, but chuk-mcp-server may already support these.

**Dependencies**: Need to audit chuk-mcp-server SSE implementation.

#### Priority 4: Standards Compliance

##### 8. JSON Schema 2020-12 📐
**Effort**: Low | **Impact**: Low | **Status**: 📋 Planned

Update schema dialect:
- Set JSON Schema 2020-12 as default
- Update examples
- Validate schemas

**Why**: Standards compliance, backward compatible.

##### 9. Decoupled Request Payloads 🔧
**Effort**: Low | **Impact**: Low | **Status**: ✅ May already be compliant

Audit implementation:
- Check if request payloads are decoupled
- Update if needed

**Why**: Better schema organization.

**Dependencies**: Need to review chuk-mcp-server implementation.

## Implementation Timeline

### Phase 1: Quick Wins (Q1 2025)
- [ ] Icons and metadata
- [ ] Enhanced elicitation
- [ ] Tool naming guidance
- [ ] JSON Schema 2020-12

**Goal**: Improve UX and documentation with minimal effort.

### Phase 2: Advanced Features (Q2 2025)
- [ ] Tool calling in sampling (requires client support)
- [ ] Advanced streaming audit
- [ ] Decoupled payloads audit

**Goal**: Add powerful new capabilities.

### Phase 3: Enterprise & Tasks (Q3-Q4 2025)
- [ ] Tasks (experimental) with persistence
- [ ] Enhanced authorization (if demand exists)

**Goal**: Support enterprise deployments and long-running operations.

## Decision Factors

### What to Implement First?

**Consider**:
1. **User demand** - What do MCP users need most?
2. **Ecosystem readiness** - Are MCP clients ready to use these features?
3. **Implementation effort** - Low-hanging fruit first
4. **Dependencies** - What can we control vs what needs external support?

### Current Recommendations

1. **Start with icons** - Easy, high visual impact
2. **Enhanced elicitation** - Better UX, low effort
3. **Monitor ecosystem** - Wait for:
   - Client support for tool calling in sampling
   - Real-world demand for tasks
   - Enterprise OAuth requirements

## Contributing

Want to help implement these features? See [CONTRIBUTING.md](CONTRIBUTING.md) (TBD).

Priority areas:
- Icons and metadata (easy first contribution)
- Enhanced elicitation examples
- Tool calling in sampling (needs research)
- Tasks implementation (significant effort)

## Questions?

Open an issue to discuss:
- Feature priorities
- Implementation approaches
- Use cases for new features
- Timeline adjustments

---

**Note**: This roadmap is aspirational. The reference server currently focuses on the stable core spec (2025-06-18) which is production-ready and 100% tested.

**Last Updated**: 2025-11-27
