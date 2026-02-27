---
name: requirement-study
description: >
  Analyze, write, and validate software requirements from any input — conversations,
  documents, rough notes, or existing specs. Use when someone asks to study requirements,
  create a PRD, analyze a feature request, extract requirements from a document, or
  validate completeness of existing requirements. Also triggers on phrases like
  "what do we need to build", "write me a spec", or "break this down into requirements".
tags: [requirements, prd, analysis, specification, product]
version: "1.0"
common-skills-used: [document-tail-sections, output-formatting, quality-checklist]
agents-tested: [claude-code, kiro]
---

# Requirement Study

## Purpose

Transform any input (rough notes, conversation transcripts, feature requests, existing documents) into structured, actionable software requirements. Produces a requirements document that any development team can use to plan and build.

## When to Use

- User asks to "study requirements" or "analyze requirements"
- User provides rough notes/ideas and wants them formalized
- User asks for a PRD (Product Requirements Document)
- User wants to extract requirements from an existing document
- User asks "what do we need to build for X?"
- User wants to validate completeness of existing requirements

## When NOT to Use

- User wants implementation details (use `implementation-sketch` instead)
- User wants a presentation (use `deck-creator` instead)
- User is asking about deployment/ops (use `remote-ops` instead)

## Inputs

**Required:**
- Source material — the raw input to derive requirements from (document, notes, conversation, or verbal description)

**Optional:**
- Target audience — who will read this requirements doc?
- Scope constraints — any known boundaries or limitations
- Existing requirements — if this is a refinement of existing work
- Template preference — if the user's org has a standard format

## Process

### Step 1: Understand the Domain

Read the source material completely. Identify:
- The domain/industry context
- Key stakeholders mentioned
- The problem being solved
- Any existing system or process being replaced/enhanced

Summarize your understanding in 3-5 sentences and confirm with the user before proceeding.

### Step 2: Extract Raw Requirements

Go through the source material and extract every explicit and implicit requirement. For each, note:
- The original text/context it came from
- Whether it was explicitly stated or inferred
- Initial categorization (functional, non-functional, constraint)

### Step 3: Categorize and Structure

Organize requirements into:

1. **Functional Requirements** — What the system must do
2. **Non-Functional Requirements** — Quality attributes (performance, security, scalability, usability)
3. **Constraints** — Technical, business, or regulatory limitations
4. **Assumptions** — Things assumed to be true
5. **Out of Scope** — Explicitly excluded items

### Step 4: Write Formal Requirements

For each requirement, write in this format:

```
**[REQ-NNN]** [Category]
**Title:** Short descriptive title
**Description:** Clear, unambiguous statement of the requirement
**Rationale:** Why this is needed
**Priority:** Must Have | Should Have | Could Have | Won't Have (this time)
**Acceptance Criteria:**
- Testable condition 1
- Testable condition 2
**Dependencies:** [REQ-XXX] if any
**Source:** Where this came from in the input
```

### Step 5: Identify Gaps and Ambiguities

Review the full requirement set and flag:
- Missing requirements implied but not stated
- Ambiguous requirements needing clarification
- Conflicting requirements
- Requirements that may be technically infeasible (flag for discussion)

### Step 6: Produce the Requirements Document

Assemble into a document following `common-skills/output-formatting.md`:

1. Title and metadata
2. Executive Summary (3-5 sentences)
3. Scope and Objectives
4. Stakeholders
5. Functional Requirements (grouped by feature/module)
6. Non-Functional Requirements
7. Constraints
8. Assumptions
9. Out of Scope
10. Gaps and Open Questions
11. Tail sections per `common-skills/document-tail-sections.md`

### Step 7: Quality Check

Apply `common-skills/quality-checklist.md` before delivering.

Additional requirement-specific checks:
- [ ] Every requirement has an ID, priority, and acceptance criteria
- [ ] No requirement uses vague language ("fast", "easy", "user-friendly") without measurable criteria
- [ ] Dependencies between requirements are identified
- [ ] Out of Scope section exists and is explicit

## Output Format

A Markdown document (`.md`) following the structure in Step 6. Filename: `requirement-study-<topic>.md`

## Edge Cases

- **Very rough input:** If the source material is just a few sentences, expand Step 1 to ask the user clarifying questions before proceeding
- **Existing formal spec:** If the input is already a formal spec, focus on gap analysis and validation rather than rewriting
- **Multiple stakeholders with conflicting needs:** Flag conflicts explicitly in the Gaps section rather than making judgment calls

## Common Skills Used

- `common-skills/document-tail-sections.md` — Standard document endings
- `common-skills/output-formatting.md` — Consistent formatting
- `common-skills/quality-checklist.md` — Pre-delivery quality gate
