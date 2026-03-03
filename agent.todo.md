# Agent TODO Ledger

Canonical cross-session task ledger for all agents working in this repository.

## Metadata

- Last Updated: 2026-03-03
- Canonical Source: this file
- Coordination Rule: single writer per artifact

## Workflow Snapshot

- Current Phase: requirement-study
- Next Phase: implementation-sketch
- Current Gate: G1 Requirements
- Next Step: Finalize open requirements decisions, then advance to G2
- Repository: https://github.com/gyanranjan/polyagent-skills
- Default Branch Strategy: trunk (main)
- **Lifecycle Process:** `common-skills/development-lifecycle-gates.md`

## Gate Status

| Gate | Name | Status | Evidence | Skip Reason |
|------|------|--------|----------|-------------|
| G0 | Discovery | Passed | `common-skills/development-lifecycle-gates.md` | — |
| G1 | Requirements | In Progress | `common-skills/development-lifecycle-gates.md` | — |
| G2 | Design | Not Started | — | — |
| G3 | POC / Spike | Not Started | — | — |
| G4 | Implementation | Not Started | — | — |
| G5 | Review | Not Started | — | — |
| G6 | Ship & Learn | Not Started | — | — |

Gate rules: See `common-skills/development-lifecycle-gates.md`. Gates are mandatory by default — skip requires explicit user request.

## Locks

| Artifact | Locked By | Since (UTC) | Purpose | Expected Release |
|----------|-----------|-------------|---------|------------------|
| (none) | — | — | — | — |

Lock policy:
- Acquire lock before major edits to shared artifacts.
- Do not edit a locked artifact owned by another agent.
- Add a handoff note if lock ownership changes.

## Now

- [ ] TASK-101 | Owner: codex | Artifact: scripts/md-to-pdf.sh | Status: in_progress | DependsOn: -

## Next

- [ ] TASK-102 | Owner: codex | Artifact: adapters/* + docs consistency | Status: todo | DependsOn: TASK-101

## Blocked

- [ ] (none)

## Decision Needed

- [ ] DEC-101 | Owner: maintainer | Decision: Require pre-PR gate checks in all adapters or Codex-only? | Options: all adapters / codex-only | Due: 2026-03-05

## Done

- [x] TASK-099 | Owner: codex | Artifact: scripts/gate-status-check.sh | Completed: 2026-03-03 07:44 UTC
- [x] TASK-100 | Owner: codex | Artifact: scripts/install-global-all.sh + adapters/codex/AGENTS.md | Completed: 2026-03-03 07:44 UTC

## Handoffs

| Time (UTC) | From | To | Task | Context | Next Step |
|------------|------|----|------|---------|-----------|
| 2026-03-03 07:44 | codex | codex | TASK-101 | Medium and high findings fixed; validating PDF + Mermaid rendering on Chromium | Finalize low-severity cleanup and report |

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
