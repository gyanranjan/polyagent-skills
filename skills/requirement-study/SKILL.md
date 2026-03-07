---
name: requirement-study
description: >
  Analyze, write, and validate software requirements from any input — conversations,
  documents, rough notes, or existing specs. Use when someone asks to study requirements,
  create a PRD, analyze a feature request, extract requirements from a document, or
  validate completeness of existing requirements. Also triggers on phrases like
  "what do we need to build", "write me a spec", or "break this down into requirements".
tags: [requirements, prd, analysis, specification, product]
version: "1.0.0"
common-skills-used: [agent-todo-ledger, design-readiness-gate, document-tail-sections, mermaid-to-pdf, output-formatting, quality-checklist]
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

### Step 1: Preflight Tooling Check

Run a non-blocking Mermaid check for future diagram generation:

```bash
if command -v mmdc >/dev/null 2>&1; then
  mmdc --version
else
  echo "mmdc not installed; continue with text/Markdown diagrams and add TODO entry"
fi
```

If `mmdc` is missing, add a task to `agent.todo.md` under `Next` or `Blocked`.

### Interaction Protocol (Mandatory)

For all substantive responses while running this skill:
- Include `Stage: Gx <name>` and `Next: <immediate next step>`
- At each gate transition, ask 2-4 decision-oriented questions before advancing
- Challenge weak assumptions and propose stronger alternatives with rationale

### Step 2: Understand the Domain

Read the source material completely. Identify:
- The domain/industry context
- Key stakeholders mentioned
- The problem being solved
- Any existing system or process being replaced/enhanced

Summarize your understanding in 3-5 sentences and confirm with the user before proceeding.

### Step 3: Extract Raw Requirements

Go through the source material and extract every explicit and implicit requirement. For each, note:
- The original text/context it came from
- Whether it was explicitly stated or inferred
- Initial categorization (functional, non-functional, constraint)

### Step 4: Categorize and Structure

Organize requirements into:

1. **Functional Requirements** — What the system must do
2. **Non-Functional Requirements** — Quality attributes (performance, security, scalability, usability)
3. **Constraints** — Technical, business, or regulatory limitations
4. **Assumptions** — Things assumed to be true
5. **Out of Scope** — Explicitly excluded items

### Step 5: Write Formal Requirements

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

### Step 6: Identify Gaps and Ambiguities

Review the full requirement set and flag:
- Missing requirements implied but not stated
- Ambiguous requirements needing clarification
- Conflicting requirements
- Requirements that may be technically infeasible (flag for discussion)

### Step 7: Produce the Requirements Document

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
11. At least one in-block Mermaid diagram (flow, context, or dependency view)
12. Tail sections per `common-skills/document-tail-sections.md`

### Step 8: Build Design Readiness Handoff (Pre-Coding)

Prepare a pre-coding handoff using `common-skills/design-readiness-gate.md`:

- Record known decisions and unresolved items for architecture pattern, language/runtime, database strategy, and logging/observability baseline.
- Mark unresolved items as `Deferred` with owner and due date.
- Add a blocking task in `agent.todo.md` if any required gate item is open.

### Step 9: Update Cross-Session Ledger and GitHub Mapping

Update `agent.todo.md` using `common-skills/agent-todo-ledger.md`:

- Add current requirement tasks in `Now`/`Next`
- Add unresolved questions to `Decision Needed`
- Add file ownership/locks for active requirement artifacts
- Add requirement-to-issue links in `GitHub Mapping` (if GitHub IDs are available)

If GitHub integration is available, create issue stubs for `REQ-*` and reflect IDs in both the requirements doc and `agent.todo.md`.

### Step 10: Export Shareable PDF (Default)

Unless the user explicitly opts out, export a PDF copy of the requirements doc:

```bash
polyagentctl export-pdf requirement-study-<topic>.md
```

Add the generated PDF path to `agent.todo.md` gate evidence.

### Step 11: Quality Check

Apply `common-skills/quality-checklist.md` before delivering.

Additional requirement-specific checks:
- [ ] Every requirement has an ID, priority, and acceptance criteria
- [ ] No requirement uses vague language ("fast", "easy", "user-friendly") without measurable criteria
- [ ] Dependencies between requirements are identified
- [ ] Out of Scope section exists and is explicit
- [ ] At least one Mermaid diagram is included in the requirements artifact
- [ ] Shareable PDF export produced (unless user explicitly waived)

## Output Format

A Markdown document (`.md`) following the structure in Step 7. Filename: `requirement-study-<topic>.md`

## Quality Checks

- [ ] Every requirement has ID, priority, rationale, and acceptance criteria
- [ ] Non-functional requirements are measurable and testable
- [ ] Assumptions, constraints, and out-of-scope are explicit and non-overlapping
- [ ] Open questions are surfaced without silently resolving ambiguity
- [ ] Pre-coding design readiness handoff exists or unresolved items are explicitly blocked in `agent.todo.md`
- [ ] At least one in-block Mermaid diagram exists
- [ ] Shareable PDF export exists or waiver is documented

## Edge Cases

- **Very rough input:** If the source material is just a few sentences, expand Step 1 to ask the user clarifying questions before proceeding
- **Existing formal spec:** If the input is already a formal spec, focus on gap analysis and validation rather than rewriting
- **Multiple stakeholders with conflicting needs:** Flag conflicts explicitly in the Gaps section rather than making judgment calls

## Common Skills Used

- `common-skills/agent-todo-ledger.md` — Maintain user-visible cross-session task state
- `common-skills/design-readiness-gate.md` — Define pre-coding architecture and operational decision gate
- `common-skills/document-tail-sections.md` — Standard document endings
- `common-skills/mermaid-to-pdf.md` — Canonical Mermaid diagram export workflow
- `common-skills/output-formatting.md` — Consistent formatting
- `common-skills/quality-checklist.md` — Pre-delivery quality gate
