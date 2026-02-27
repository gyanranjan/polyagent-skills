# ADR-004: MCP for Tool-Based Skills

**Status:** Accepted
**Date:** 2025-02-27
**Deciders:** Gyan Ranjan

## Context

Some skills need more than instructions — they need tool capabilities (e.g., reading email, calling APIs, querying databases). We need a way to provide tools that works across agents.

## Decision

Use **MCP (Model Context Protocol)** as the standard for tool-based skill capabilities, with **fallback alternatives** for agents that don't support MCP.

### Approach

1. Tool capabilities are implemented as MCP servers in `mcp-servers/`
2. Skills that need tools reference the MCP server AND provide a manual fallback
3. The SKILL.md documents both paths:
   - "If MCP is available, use the `mail-tools` MCP server"
   - "If MCP is not available, use the following curl commands / scripts"

### Why MCP

- Open protocol by Anthropic, but designed for broad adoption
- Claude Code supports it natively
- Kiro, Cursor, and others are adding support
- Provides a clean separation between instructions (SKILL.md) and capabilities (MCP)

## Consequences

### Positive
- Clean separation of knowledge (skills) and capabilities (tools)
- Growing ecosystem of MCP servers to leverage
- Forward-compatible as more agents adopt MCP
- Fallback paths ensure skills work even without MCP

### Negative
- MCP support is still uneven across agents (see KI-005)
- Maintaining both MCP and fallback paths adds work
- MCP server development requires more engineering than writing Markdown

### Neutral
- MCP servers are optional — most skills are instruction-only and don't need them
- The `mcp-servers/` directory may remain empty for a long time and that's fine

## Alternatives Considered

### Alternative 1: Shell Scripts Only
Simpler but less integrated with agent workflows. Agents can run scripts, but MCP provides a richer tool interface with typed inputs/outputs.

### Alternative 2: Agent-Native Tool APIs
Each agent has its own tool/function calling mechanism. Using these would mean rewriting tool integrations per agent — the same problem we're solving for skills.

### Alternative 3: No Tool Support
Only support instruction-based skills. Limiting for power-user workflows but avoids the complexity. Rejected because some skills genuinely need tool access to be useful.

## Related

- [Known Issues: KI-005](../../KNOWN_ISSUES.md)
- [ADR-002: Three-Layer Architecture](002-three-layer-architecture.md)
