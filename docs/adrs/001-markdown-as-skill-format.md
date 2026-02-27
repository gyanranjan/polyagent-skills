# ADR-001: Markdown as Universal Skill Format

**Status:** Accepted
**Date:** 2025-02-27
**Deciders:** Gyan Ranjan

## Context

We need a format for writing AI agent skills that works across Claude Code, Kiro, Codex, Gemini, Cursor, and future agents. Each agent has its own native format for instructions, but we need a single source of truth.

Options considered include JSON schemas, YAML configs, custom DSLs, and plain Markdown.

## Decision

Use **plain Markdown (GitHub Flavored Markdown)** with YAML frontmatter as the universal skill format.

Skills are written as structured `.md` files with:
- YAML frontmatter for metadata (name, description, tags, version)
- Markdown body for instructions, organized with standard headings
- Relative file references for supporting materials

## Consequences

### Positive
- Every LLM-based agent can parse Markdown natively — it's their strongest format
- Human-readable and editable without special tooling
- Git-friendly: diffs, PRs, and reviews work naturally
- YAML frontmatter is a well-established pattern (Jekyll, Hugo, Docusaurus)
- No build step or compilation required
- Can be rendered nicely on GitHub, in IDEs, and in docs sites

### Negative
- No schema enforcement at the format level (must rely on linting/validation scripts)
- Markdown is loosely structured — different authors may organize content differently
- No type safety or programmatic validation of instructions

### Neutral
- Requires a spec (skill-format-spec.md) to ensure consistency across authors
- Frontmatter parsing requires a YAML parser if programmatic access is needed

## Alternatives Considered

### Alternative 1: JSON/YAML Config Files
Highly structured but terrible for writing natural language instructions. LLMs parse them well but the authoring experience is poor for the kind of rich, step-by-step instructions skills need.

### Alternative 2: Custom DSL
Maximum expressiveness but creates a learning curve, requires tooling, and no agent understands it natively. The maintenance burden far outweighs the benefits.

### Alternative 3: Agent-Native Formats
Write in each agent's native format. This is what we're trying to escape — it leads to N copies of every skill, constant drift, and unsustainable maintenance.

## Related

- [Skill Format Spec](../specs/skill-format-spec.md)
- [ADR-002: Three-Layer Architecture](002-three-layer-architecture.md)
