# MCP Servers

Optional MCP (Model Context Protocol) servers that provide tool capabilities to skills.

## When to Use MCP

Most skills are **instruction-only** — they tell the agent what to do using the agent's built-in capabilities. MCP servers are needed when a skill requires capabilities the agent doesn't have natively, such as calling a specific API, querying a database, or interacting with a third-party service.

## Architecture

```
Skill (SKILL.md)          →  Instructions (what to do)
MCP Server (server.ts)    →  Capabilities (how to do it)
```

Skills reference MCP servers but always provide a fallback path for agents that don't support MCP.

## Creating an MCP Server

See [ADR-004: MCP for Tool Skills](../docs/adrs/004-mcp-for-tool-skills.md) for the architectural decision.

Each MCP server should:
1. Live in its own subdirectory: `mcp-servers/<server-name>/`
2. Include a `README.md` with setup instructions
3. Follow the MCP specification
4. Be referenced by skills that need it

## Current Servers

None yet. Add servers here as skills require tool capabilities beyond what agents provide natively.
