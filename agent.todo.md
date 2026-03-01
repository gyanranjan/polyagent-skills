# Agent TODO Ledger

Canonical cross-session task ledger for all agents working in this repository.

## Metadata

- Last Updated: 2026-03-01
- Canonical Source: this file
- Coordination Rule: single writer per artifact

## Workflow Snapshot

- Current Phase: requirement-study
- Next Phase: implementation-sketch
- Repository: [set repo URL]
- Default Branch Strategy: [trunk | gitflow | other]

## Locks

| Artifact | Locked By | Since (UTC) | Purpose | Expected Release |
|----------|-----------|-------------|---------|------------------|
| [path/to/file] | [agent-id] | YYYY-MM-DD HH:MM | [reason] | YYYY-MM-DD HH:MM |

Lock policy:
- Acquire lock before major edits to shared artifacts.
- Do not edit a locked artifact owned by another agent.
- Add a handoff note if lock ownership changes.

## Now

- [ ] TASK-001 | Owner: [agent-id] | Artifact: [path] | Status: in_progress | DependsOn: -

## Next

- [ ] TASK-002 | Owner: [agent-id] | Artifact: [path] | Status: todo | DependsOn: TASK-001

## Blocked

- [ ] TASK-003 | Owner: [agent-id] | Blocker: [what is blocked] | Needs: [decision/input]

## Decision Needed

- [ ] DEC-001 | Owner: [agent-id] | Decision: [question] | Options: [A/B/C] | Due: YYYY-MM-DD

## Done

- [x] TASK-000 | Owner: [agent-id] | Artifact: [path] | Completed: YYYY-MM-DD HH:MM UTC

## Handoffs

| Time (UTC) | From | To | Task | Context | Next Step |
|------------|------|----|------|---------|-----------|
| YYYY-MM-DD HH:MM | [agent-a] | [agent-b] | TASK-001 | [brief context] | [clear next step] |

## GitHub Mapping

| Requirement ID | GitHub Issue | Status | Owner |
|----------------|--------------|--------|-------|
| REQ-001 | #123 | Open | [owner] |

## RCA Queue

| Incident/Issue | Severity | RCA Doc | Status | Owner |
|----------------|----------|---------|--------|-------|
| [link/id] | [sev] | [docs/rca/...md] | Open | [owner] |

<!-- BEGIN AUTO-SYNC -->
## Auto-Synced Traceability (Managed)

- Synced At (UTC): 2026-03-01 06:27
- Requirements Source: skills/requirement-study/references/requirement-template.md
- Spec Source: docs/specs/SPEC_TEMPLATE.md

### Requirements Snapshot

| Requirement ID | Title | GitHub Issue | Status | Owner |
|----------------|-------|--------------|--------|-------|
| REQ-001 | Requirement REQ-001 | (create issue) | Open | [owner] |

### Design Readiness Snapshot

| Checkpoint | Status | Source |
|------------|--------|--------|
| Architecture pattern | Open | docs/specs/SPEC_TEMPLATE.md |
| Language/runtime | Open | docs/specs/SPEC_TEMPLATE.md |
| Database strategy | Open | docs/specs/SPEC_TEMPLATE.md |
| Logging/observability baseline | Open | docs/specs/SPEC_TEMPLATE.md |

<!-- END AUTO-SYNC -->
