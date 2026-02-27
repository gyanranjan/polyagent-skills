---
name: agent-writer
description: >
  Write new agent definitions, skill files, and agent configurations. Use when someone
  asks to "create a new agent", "write a skill", "define an agent", or needs to
  create reusable AI agent instructions for any platform. This is the meta-skill
  for creating other skills and agents in the polyagent-skills format.
tags: [agent, skill, meta, creation, definition]
version: "1.0"
common-skills-used: [output-formatting, quality-checklist]
agents-tested: [claude-code]
---

# Agent Writer

## Purpose

Create new agent definitions and skill files that conform to the polyagent-skills portable format. This is the meta-skill — it creates other skills.

## When to Use

- User wants to create a new skill for the polyagent-skills library
- User wants to define a new agent persona or workflow
- User asks "write me a skill for X"
- User wants to convert agent-specific instructions into portable format

## Inputs

**Required:**
- What the skill/agent should do
- When it should trigger

**Optional:**
- Example inputs and expected outputs
- Common skills it should reference
- Agents it needs to work with

## Process

### Step 1: Understand Intent
Clarify what the skill should accomplish, who uses it, and what triggers it.

### Step 2: Design the Skill
Plan the process steps, inputs, outputs, and edge cases.

### Step 3: Write SKILL.md
Follow the [Skill Format Spec](../../docs/specs/skill-format-spec.md) exactly:
- YAML frontmatter with name, description, tags, version
- All required sections: Purpose, When to Use, Inputs, Process, Output Format
- References to common-skills where appropriate

### Step 4: Create Supporting Files
Add references/, examples/, and templates/ as needed.

### Step 5: Validate Portability
Check against the portability rules:
- No agent-specific syntax
- Relative paths only
- Plain Markdown only
- Self-contained steps

### Step 6: Update Adapters
Run `scripts/sync-adapters.sh` to add the new skill to all adapter files.

## Output Format

A complete skill directory: `skills/<skill-name>/SKILL.md` plus supporting files.

## Common Skills Used

- `common-skills/output-formatting.md` — For the generated skill files
- `common-skills/quality-checklist.md` — Validate the new skill
