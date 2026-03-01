# Requirement Document Template

Use this template when producing the final requirements document.

---

# Requirements: [Project/Feature Name]

**Author:** [agent + human reviewer]
**Date:** YYYY-MM-DD
**Version:** 1.0
**Status:** Draft | In Review | Approved
**Canonical TODO Ledger:** `agent.todo.md`
**GitHub Project/Repo:** [org/repo]

---

## Executive Summary

[3-5 sentences summarizing what is being built and why]

## Tooling Preflight

| Tool | Check Command | Result | Notes |
|------|---------------|--------|-------|
| Mermaid CLI (`mmdc`) | `mmdc --version` | Pass/Fail | Non-blocking; fallback to text diagrams |

## Design Readiness Handoff (Pre-Coding)

| Checkpoint | Status (Done/Deferred/Open) | Owner | Evidence/Link |
|------------|------------------------------|-------|---------------|
| Architecture pattern | Open | | |
| Language/runtime choice | Open | | |
| Database strategy | Open | | |
| Logging/observability baseline | Open | | |

Coding start rule:
- Do not start implementation until required checkpoints are `Done` or explicitly `Deferred` with owner and due date.

## Scope and Objectives

### Objectives
[What success looks like]

### Scope
[What is included]

### Out of Scope
[What is explicitly excluded]

## Stakeholders

| Role | Name/Team | Interest |
|------|-----------|----------|
| Product Owner | | |
| Development | | |
| End Users | | |

## Functional Requirements

### [Feature Area 1]

**[REQ-001]** Functional
**Title:**
**Description:**
**Rationale:**
**Priority:** Must Have | Should Have | Could Have
**Acceptance Criteria:**
-
**Dependencies:**
**Source:**

### [Feature Area 2]

...

## Non-Functional Requirements

**[NFR-001]**
**Title:**
**Description:**
**Measurable Criteria:**
**Priority:**

## Constraints

- [Technical constraints]
- [Business constraints]
- [Regulatory constraints]

## Assumptions

- [Assumption 1]
- [Assumption 2]

## Gaps and Open Questions

| # | Question | Owner | Due Date | Status |
|---|----------|-------|----------|--------|
| 1 | | | | Open |

## GitHub Traceability

| Requirement ID | GitHub Issue | Label(s) | Milestone | Owner | Status |
|----------------|--------------|----------|-----------|-------|--------|
| REQ-001 | #123 | `type:req` | v1 | | Open |

## Multi-Agent Coordination

| Artifact | Current Owner Agent | Lock Status | Handoff Needed |
|----------|---------------------|-------------|----------------|
| [path/to/file] | [codex/claude/kiro] | Locked/Free | Yes/No |

## RCA Hooks

Record defects or major risks discovered during requirement work so they can become formal RCA artifacts later.

| Ref (Issue/Task) | Symptom | Suspected Cause | Needs RCA? |
|------------------|---------|------------------|------------|
| [#123] | | | Yes/No |

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | YYYY-MM-DD | | Initial version |
