# ADR-005: Workflow Orchestration and Session-Visible TODO Persistence

**Status:** Accepted
**Date:** 2026-03-01
**Deciders:** repo maintainers

## Context

The current skill set has strong single-step capabilities (`requirement-study`, `implementation-sketch`, `repo-bootstrap`, `remote-ops`) but weak cross-step continuity for the full workflow:

1. Start from plain-language notes
2. Produce requirements
3. Decide architecture/design nuances
4. Create/prepare code repository
5. Implement from specs (spec-driven development)
6. Track issues with true root-cause analysis (RCA)

Current gaps:

- No standardized local preflight check for Mermaid tooling.
- No persistent, user-visible task ledger that survives sessions.
- No default GitHub integration from the requirement phase (issues/projects/milestones from requirements).
- No explicit multi-agent coordination protocol (ownership, handoffs, lock/merge behavior).
- No required RCA template/workflow tied to incident or defect resolution.

Baseline environment observation on 2026-03-01:

- `mmdc` (Mermaid CLI): not found
- `mermaid` binary: not found
- `node` and `npm`: present

## Decision

Adopt a workflow orchestration pattern with explicit persistence and integration points.

### 1. Add Preflight Tooling Checks

Introduce a preflight check step for skills that may emit diagrams.

- Check for Mermaid CLI via `mmdc --version`.
- If missing, continue with text fallback and add a TODO entry for installation.
- Keep checks non-blocking for requirement/design phases.

### 2. Add User-Visible Persistent TODO Ledger

Create a repository-level file `agent.todo.md` as the canonical cross-session task ledger.

- Always user-visible and updated by agents at key transitions.
- Include sections: `Now`, `Next`, `Blocked`, `Done`, `Decision Needed`.
- Requirement documents may include local TODO sections, but `agent.todo.md` is the canonical shared ledger.

### 3. Integrate GitHub Earlier (Requirement Phase)

Allow requirement-stage outputs to map directly to GitHub work items.

- Map requirements to issue stubs with IDs linking back to requirement IDs.
- Track decisions/questions as issues or discussions.
- Record repository URL, default branch model, and labeling convention in the TODO ledger.

### 4. Define Multi-Agent Coordination Rules

Establish coordination conventions for concurrent agent usage.

- Single writer per artifact at a time.
- Explicit handoff notes in `agent.todo.md`.
- Required file-level ownership note before major edits.
- Conflict resolution via ADR/RFC notes rather than silent overwrite.
- Use a `Locks` table in `agent.todo.md` with `Artifact`, `Locked By`, `Since`, and `Expected Release`.
- Track agent-specific active queues in per-agent swimlanes using stable IDs (`TASK-###`, `DEC-###`).

### 5. Standardize RCA for Defects/Incidents

Define a lightweight RCA template and enforce it for significant issues.

- Problem statement, impact, timeline, root cause, contributing factors, corrective/preventive actions.
- Link RCA output to requirement/spec/issue IDs.
- Canonical template location: `docs/rca/RCA_TEMPLATE.md`.

### 6. Enforce Design Readiness Gate Before Coding

Require explicit pre-coding decisions for:

- Architecture/design pattern
- Language/runtime
- Database and migration approach
- Logging/observability baseline

If unresolved, coding tasks must remain blocked in `agent.todo.md`.

## Consequences

### Positive
- Better continuity across sessions and agents.
- Earlier planning-to-execution traceability through GitHub.
- Reduced ambiguity on ownership and next actions.
- Improved operational learning via standardized RCA.

### Negative
- More process overhead for simple tasks.
- Requires discipline to keep `agent.todo.md` current.
- Requires optional GitHub credentials/access setup for full value.

### Neutral
- Diagram generation remains optional; Mermaid check mainly improves transparency.

## Alternatives Considered

### Alternative 1: Keep TODOs embedded only inside each generated document
Rejected because cross-session continuity becomes fragmented across multiple files.

### Alternative 2: Use external project tool only (no in-repo TODO ledger)
Rejected because portability and agent interoperability are reduced in disconnected environments.

## Related

- [ADR-001: Markdown as Universal Skill Format](001-markdown-as-skill-format.md)
- [ADR-002: Three-Layer Architecture](002-three-layer-architecture.md)
- [ADR-003: Adapter Pattern for Agent Compatibility](003-adapter-pattern.md)
- [ADR-004: MCP for Tool-Based Skills](004-mcp-for-tool-skills.md)
