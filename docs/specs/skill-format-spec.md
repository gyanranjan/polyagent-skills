# Spec: Skill Format

**Author:** Gyan Ranjan
**Status:** Approved
**Created:** 2025-02-27
**Updated:** 2025-02-27

---

## Summary

Defines the standard format for writing portable, agent-agnostic skills in the polyagent-skills library. Any skill conforming to this spec can be consumed by any supported agent through its adapter.

## Motivation

Different AI agents use different instruction formats. Without a standard, every skill must be rewritten per agent. This spec defines a single authoritative format that all adapters can consume.

## Detailed Design

### Directory Structure

Every skill lives in `skills/<skill-name>/` with this layout:

```
skills/<skill-name>/
├── SKILL.md              # Required: Main instructions
├── references/            # Optional: Supporting documents
│   ├── templates/         # Output templates
│   ├── examples/          # Input/output examples
│   └── *.md               # Reference material
└── assets/                # Optional: Static files (images, configs)
```

### SKILL.md Format

```markdown
---
name: <skill-name>
description: >
  One-paragraph description. Must include:
  - What the skill does
  - When to trigger it (specific phrases, contexts)
  - What kind of output it produces
tags: [tag1, tag2, tag3]
version: "1.0"
common-skills-used: [skill1, skill2]
agents-tested: [claude-code, kiro, codex]
---

# <Skill Name>

## Purpose
2-3 sentences on what this skill accomplishes.

## When to Use
Specific trigger conditions as a bulleted list.

## When NOT to Use
Explicit exclusions to prevent false triggers.

## Inputs
What the agent needs from the user before executing.
Include required vs optional inputs.

## Process

### Step 1: <Step Title>
Detailed, unambiguous instructions.
Reference files: "Read `references/template.md` for the output format."

### Step 2: <Step Title>
...

(Continue for all steps)

## Output Format
Exact description of what the skill produces.
Include examples if possible.

## Quality Checks
- [ ] Check 1
- [ ] Check 2

## Common Skills Used
- `common-skills/<name>.md` — Why it's used here

## Edge Cases
Known tricky situations and how to handle them.
```

### Portability Rules

1. **No agent-specific syntax** — No slash commands, no XML tool tags, no agent hooks
2. **Relative paths only** — `references/template.md`, never absolute paths
3. **Plain Markdown only** — Standard GFM (GitHub Flavored Markdown)
4. **Self-contained steps** — Don't assume agent memory across steps
5. **Explicit common-skill references** — Always state which common-skills are used and when to read them
6. **No inline code execution** — Skills give instructions; if tools are needed, document them as MCP servers or scripts with fallback alternatives

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier, matches directory name |
| `description` | Yes | Trigger description (< 200 words) |
| `tags` | Yes | Discovery tags |
| `version` | Yes | Semver string |
| `common-skills-used` | No | List of common-skills referenced |
| `agents-tested` | No | Agents this has been verified with |

### Naming Conventions

- Skill directories: `kebab-case` (e.g., `requirement-study`)
- SKILL.md: Always uppercase
- Reference files: `kebab-case.md`
- No spaces, no underscores in directory names

## Acceptance Criteria

- [ ] A skill conforming to this spec works with Claude Code via adapter
- [ ] Same skill works with Codex via adapter without modification
- [ ] Same skill works with Kiro via adapter without modification
- [ ] Frontmatter is parseable by standard YAML parsers
- [ ] No agent-specific syntax present in SKILL.md

## Out of Scope

- MCP server specifications (see separate spec)
- Adapter format specifications (see adapter-contract-spec.md)
- Skill evaluation/testing framework

## Dependencies

- [ADR-001: Markdown as Skill Format](../adrs/001-markdown-as-skill-format.md)
- [ADR-002: Three-Layer Architecture](../adrs/002-three-layer-architecture.md)
