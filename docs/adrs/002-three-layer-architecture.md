# ADR-002: Three-Layer Architecture

**Status:** Accepted
**Date:** 2025-02-27
**Deciders:** Gyan Ranjan

## Context

We need an architecture that cleanly separates what agents know (skills) from how they discover skills (adapters) from shared conventions (common patterns). Without clear separation, skill content leaks into agent-specific files, common patterns get duplicated, and the system becomes unmaintainable.

## Decision

Adopt a **three-layer architecture**:

```
Layer 3: Adapters        — Agent-specific instruction files (thin pointers)
Layer 2: Skills          — Portable, agent-agnostic skill definitions
Layer 1: Common Foundation — Shared patterns, conventions, templates
```

### Layer 1: Common Foundation (`common-skills/`)
Reusable building blocks that multiple skills reference. Examples: output formatting rules, document tail sections, quality checklists. Written once, referenced by many skills.

### Layer 2: Skill Library (`skills/`)
Individual skill definitions, each in its own directory with a `SKILL.md` and optional supporting files. Each skill is self-contained and references Layer 1 as needed.

### Layer 3: Adapters (`adapters/`)
Thin files that translate between an agent's native instruction format and the skill library. They point to Layer 2, never duplicate it.

## Consequences

### Positive
- Clear separation of concerns — each layer has one job
- Skills are maintained in exactly one place
- Adding a new agent means writing one adapter, not rewriting all skills
- Common patterns are DRY
- Easy to reason about where any piece of information lives

### Negative
- Agents must follow reference chains (adapter → skill → common-skill), which some agents handle better than others (see KI-001)
- Slightly more complex directory structure than a flat approach
- New contributors must understand the layering before contributing

### Neutral
- Install scripts must copy all three layers to target projects
- Sync scripts must keep adapters' skill lists in sync with the skill library

## Alternatives Considered

### Alternative 1: Flat Structure
All skills and adapters in one directory. Simpler but leads to naming collisions, no clear ownership, and common patterns being copy-pasted everywhere.

### Alternative 2: Per-Agent Repositories
Separate repos for each agent's skills. Maximum isolation but impossible to keep in sync. This is the problem we're solving.

### Alternative 3: Monolithic Instruction File
One giant instruction file per agent with all skills inlined. Works short-term but doesn't scale, can't be shared across agents, and hits agent context limits.

## Related

- [ADR-001: Markdown as Skill Format](001-markdown-as-skill-format.md)
- [ADR-003: Adapter Pattern](003-adapter-pattern.md)
- [Skill Format Spec](../specs/skill-format-spec.md)
